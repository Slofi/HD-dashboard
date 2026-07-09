from flask import Flask, render_template, jsonify, send_from_directory, request, send_file, Response
import subprocess, os, socket, datetime, time, threading, sqlite3, io, gzip

app = Flask(__name__)

MBTILES_PATH = os.environ.get("HD_MBTILES", "/home/slofi/maps/default.mbtiles")
NOTES_DB     = os.path.join(os.path.dirname(__file__), "map_notes.db")

def _init_notes_db():
    conn = sqlite3.connect(NOTES_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS map_notes (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        lat         REAL    NOT NULL,
        lon         REAL    NOT NULL,
        name        TEXT    NOT NULL,
        description TEXT    DEFAULT '',
        emoji       TEXT    DEFAULT '📍',
        created_at  INTEGER DEFAULT (strftime('%s','now'))
    )""")
    conn.commit()
    conn.close()

_init_notes_db()

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), "static"), filename)

def get_env():
    env = os.environ.copy()
    env["DISPLAY"] = ":0"
    env["XDG_RUNTIME_DIR"] = "/run/user/1000"
    env["DBUS_SESSION_BUS_ADDRESS"] = "unix:path=/run/user/1000/bus"
    xauth = subprocess.run(
        ["bash", "-c", "ls /run/user/1000/xauth* 2>/dev/null | head -1"],
        capture_output=True, text=True).stdout.strip() or "/home/slofi/.Xauthority"
    env["XAUTHORITY"] = xauth
    return env

def is_port_open(port):
    try:
        s = socket.create_connection(("localhost", port), timeout=1)
        s.close()
        return True
    except:
        return False

def send_f11_delayed(delay=0.6):
    def _do():
        time.sleep(delay)
        subprocess.run(["xdotool", "key", "F11"],
                       env=get_env(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    threading.Thread(target=_do, daemon=True).start()

_shutdown_at = None
_accent_color = "#e8b04f"
_ACCENT_FILE  = os.path.join(os.path.dirname(__file__), ".accent")

def _load_accent():
    global _accent_color
    try:
        with open(_ACCENT_FILE) as f:
            _accent_color = f.read().strip() or _accent_color
    except OSError:
        pass
_load_accent()

APPS = [
    {
        "id":          "overmesh",
        "label":       "OM Lite",
        "icon":        "fa-tower-broadcast",
        "cmd":         ["vivaldi-stable", "--kiosk", "--start-fullscreen", "--overscroll-history-navigation=0", "--disable-features=OverscrollHistoryNavigation", "http://localhost:8082/lite"],
        "start_cmd":   ["systemctl", "--user", "start", "overmesh"],
        "stop_cmd":    ["systemctl", "--user", "stop", "overmesh"],
        "status_port": 8082,
        "fullscreen":  True,
        "stoppable":   True,
    },
    {
        "id":          "ops-toc",
        "label":       "OPS-TOC",
        "icon":        "fa-crosshairs",
        "cmd":         ["vivaldi-stable", "--kiosk", "--start-fullscreen", "--overscroll-history-navigation=0", "--disable-features=OverscrollHistoryNavigation", "http://localhost:8090/lite"],
        "start_cmd":   ["systemctl", "--user", "start", "ops-toc"],
        "stop_cmd":    ["systemctl", "--user", "stop", "ops-toc"],
        "status_port": 8090,
        "fullscreen":  True,
        "stoppable":   True,
    },
    {
        "id":          "terminal",
        "label":       "Terminal",
        "icon":        "fa-terminal",
        "cmd":         ["konsole", "--fullscreen"],
        "status_port": None,
        "fullscreen":  False,
        "stoppable":   False,
    },
    {
        "id":          "desktop",
        "label":       "Desktop",
        "icon":        "fa-desktop",
        "cmd":         ["bash", "-c", "qdbus6 org.kde.kglobalaccel /component/kwin invokeShortcut 'Show Desktop'"],
        "status_port": None,
        "fullscreen":  False,
        "stoppable":   False,
    },
    {
        "id":          "shutdown",
        "label":       "Shutdown",
        "icon":        "fa-power-off",
        "cmd":         None,
        "special":     "stop-all",
        "status_port": None,
        "fullscreen":  False,
        "stoppable":   False,
    },
]

# ── Launcher routes ──────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html", apps=APPS)

@app.route("/accent", methods=["GET"])
def get_accent():
    return jsonify({"color": _accent_color})

@app.route("/accent", methods=["POST"])
def set_accent():
    global _accent_color
    color = (request.json or {}).get("color", "").strip()
    if color:
        _accent_color = color
        try:
            with open(_ACCENT_FILE, "w") as f:
                f.write(color)
        except OSError:
            pass
    return jsonify({"ok": True, "color": _accent_color})

@app.route("/launch/<app_id>", methods=["POST"])
def launch(app_id):
    app_info = next((a for a in APPS if a["id"] == app_id), None)
    if not app_info:
        return jsonify({"error": "unknown"}), 404
    if not app_info.get("cmd"):
        return jsonify({"status": "no_action"})
    # Kill any existing Vivaldi before re-launching (clean start)
    subprocess.run(["pkill", "-f", "vivaldi-stable"], capture_output=True)
    time.sleep(0.4)
    start_cmd = app_info.get("start_cmd")
    if start_cmd:
        subprocess.run(start_cmd, capture_output=True)
        port = app_info.get("status_port")
        if port:
            for _ in range(20):
                if is_port_open(port):
                    break
                time.sleep(0.5)
        else:
            time.sleep(1)
    subprocess.Popen(app_info["cmd"], env=get_env(),
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if app_info.get("fullscreen"):
        send_f11_delayed(0.6)
    return jsonify({"status": "ok"})

@app.route("/stop/<app_id>", methods=["POST"])
def stop_app(app_id):
    app_info = next((a for a in APPS if a["id"] == app_id), None)
    if not app_info:
        return jsonify({"error": "unknown"}), 404
    stop_cmd = app_info.get("stop_cmd")
    if not stop_cmd:
        return jsonify({"status": "no_action"})
    subprocess.run(stop_cmd, capture_output=True)
    # Kill the browser too when stopping a stoppable app
    if app_info.get("stoppable"):
        subprocess.run(["pkill", "-f", "vivaldi-stable"], capture_output=True)
    return jsonify({"status": "ok"})

@app.route("/stop-all", methods=["POST"])
def stop_all():
    for a in APPS:
        sc = a.get("stop_cmd")
        if sc:
            subprocess.run(sc, capture_output=True)
    subprocess.run(["pkill", "-f", "vivaldi-stable"], capture_output=True)
    def _do():
        time.sleep(0.8)
        subprocess.run(["systemctl", "--user", "stop", "launcher"], capture_output=True)
    threading.Thread(target=_do, daemon=True).start()
    return jsonify({"status": "ok"})


CD_AP_CON  = "CD-AP"
WIFI_IFACE = "wlan0"

def cdap_status():
    try:
        r = subprocess.run(
            ["nmcli", "-t", "-f", "DEVICE,STATE,CONNECTION", "device", "status"],
            capture_output=True, text=True, timeout=3
        )
        for line in r.stdout.splitlines():
            parts = line.split(":")
            if len(parts) >= 3 and parts[0] == WIFI_IFACE:
                if parts[1] == "connected":
                    ssid = parts[2]
                    return {"connected": True, "ssid": ssid, "to_cdap": ssid == CD_AP_CON}
                return {"connected": False, "ssid": "", "to_cdap": False}
        return {"connected": False, "ssid": "", "to_cdap": False}
    except Exception:
        return {"connected": False, "ssid": "", "to_cdap": False}


def gps_fix_status():
    """Check OPS-TOC GPS for fix — returns dict with fix bool and sats."""
    try:
        import urllib.request as _ur, json as _j
        with _ur.urlopen("http://localhost:8090/api/gps", timeout=1) as r:
            d = _j.loads(r.read())
        return {
            "ok":   bool(d.get("fix")),
            "sats": d.get("sats_used", 0),
            "lat":  d.get("lat"),
            "lon":  d.get("lon"),
        }
    except Exception:
        return {"ok": False, "sats": 0, "lat": None, "lon": None}


@app.route("/toggle-cdap", methods=["POST"])
def toggle_cdap():
    try:
        st = cdap_status()
        if st["to_cdap"]:
            subprocess.run(["sudo", "nmcli", "connection", "down", CD_AP_CON],
                           capture_output=True, timeout=15)
            subprocess.run(["nmcli", "device", "connect", WIFI_IFACE],
                           capture_output=True, timeout=10)
            return jsonify({"status": "disconnected"})
        else:
            r = subprocess.run(
                ["sudo", "nmcli", "connection", "up", CD_AP_CON],
                capture_output=True, text=True, timeout=20
            )
            if r.returncode != 0:
                return jsonify({"status": "error",
                                "msg": (r.stdout + r.stderr).strip()}), 500
            return jsonify({"status": "connected"})
    except Exception as exc:
        return jsonify({"status": "error", "msg": str(exc)}), 500

@app.route("/status")
def status():
    global _shutdown_at
    result = {}
    for a in APPS:
        port = a.get("status_port")
        result[a["id"]] = is_port_open(port) if port else None
    result["time"] = datetime.datetime.now().strftime("%H:%M")
    result["date"] = datetime.datetime.now().strftime("%A %d %b %Y")
    result["shutdown_at"] = _shutdown_at
    result["cdap"] = cdap_status()
    result["gps"]  = gps_fix_status()
    return jsonify(result)

@app.route("/brightness", methods=["POST"])
def brightness():
    val = float((request.json or {}).get("value", 1.0))
    val = max(0.2, min(1.0, val))
    subprocess.run(["xrandr", "--output", "HDMI-1", "--brightness", f"{val:.2f}"],
                   env=get_env(), capture_output=True)
    return jsonify({"ok": True, "value": val})

@app.route("/shutdown-timer", methods=["POST"])
def shutdown_timer():
    global _shutdown_at
    minutes = int((request.json or {}).get("minutes", 0))
    if minutes < 1:
        return jsonify({"error": "Invalid duration"}), 400
    result = subprocess.run(["sudo", "shutdown", "-h", f"+{minutes}"],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return jsonify({"error": result.stderr.strip()}), 500
    _shutdown_at = time.time() + minutes * 60
    return jsonify({"ok": True, "shutdown_at": _shutdown_at})

@app.route("/shutdown-cancel", methods=["POST"])
def shutdown_cancel():
    global _shutdown_at
    subprocess.run(["sudo", "shutdown", "-c"], capture_output=True)
    _shutdown_at = None
    return jsonify({"ok": True})

# ── Map app routes ───────────────────────────────────────────────────────────

@app.route("/map")
def map_page():
    has_offline = os.path.exists(MBTILES_PATH)
    return render_template("map.html", has_offline=has_offline)

@app.route("/tiles/<int:z>/<int:x>/<int:y>.png")
def serve_tile(z, x, y):
    if not os.path.exists(MBTILES_PATH):
        return Response(status=204)
    y_tms = (2 ** z - 1) - y
    try:
        conn = sqlite3.connect(f"file:{MBTILES_PATH}?mode=ro", uri=True)
        row = conn.execute(
            "SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?",
            (z, x, y_tms)
        ).fetchone()
        conn.close()
        if not row:
            return Response(status=204)
        data = row[0]
        if data[:2] == b'\x1f\x8b':
            data = gzip.decompress(data)
        return send_file(io.BytesIO(data), mimetype="image/png")
    except Exception:
        return Response(status=500)

@app.route("/api/gps")
def api_gps():
    # TODO: wire to GPSD when hardware arrives
    # try:
    #     import gpsd
    #     gpsd.connect()
    #     p = gpsd.get_current()
    #     return jsonify({"fix": p.mode >= 2, "lat": p.lat, "lon": p.lon,
    #                     "alt": getattr(p, 'alt', None), "sats": p.sats})
    # except Exception:
    #     pass
    return jsonify({"fix": False, "lat": None, "lon": None, "sats": 0})

@app.route("/api/map/notes", methods=["GET"])
def get_notes():
    conn = sqlite3.connect(NOTES_DB)
    rows = conn.execute(
        "SELECT id, lat, lon, name, description, emoji, created_at FROM map_notes ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return jsonify([
        {"id": r[0], "lat": r[1], "lon": r[2], "name": r[3],
         "description": r[4], "emoji": r[5], "created_at": r[6]}
        for r in rows
    ])

@app.route("/api/map/notes", methods=["POST"])
def add_note():
    data = request.json or {}
    lat, lon = data.get("lat"), data.get("lon")
    name = (data.get("name") or "").strip()
    if not name or lat is None or lon is None:
        return jsonify({"error": "Missing required fields"}), 400
    conn = sqlite3.connect(NOTES_DB)
    cur = conn.execute(
        "INSERT INTO map_notes (lat, lon, name, description, emoji) VALUES (?, ?, ?, ?, ?)",
        (lat, lon, name, data.get("description", ""), data.get("emoji", "📍"))
    )
    note_id = cur.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"ok": True, "id": note_id})

@app.route("/api/map/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    data = request.json or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "Name required"}), 400
    conn = sqlite3.connect(NOTES_DB)
    conn.execute(
        "UPDATE map_notes SET name=?, description=?, emoji=? WHERE id=?",
        (name, data.get("description", ""), data.get("emoji", "📍"), note_id)
    )
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/api/map/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = sqlite3.connect(NOTES_DB)
    conn.execute("DELETE FROM map_notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
