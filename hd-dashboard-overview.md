type:: project-overview
project:: hd-dashboard
tags:: #overview #hand-deck #launcher #kiosk #flask #archived
updated:: 2026-09-25 (DeepSeek — ⚠️ **STATUS CORRECTED: this repo is NOT archived — it is the LIVE Hand-Deck launcher**, running at `/home/radxa/launcher` on `radxa-cubie-a7a` as `launcher.service` on **port 8080**, opened by the desktop shortcut via `start-launcher.sh`. Proved by hash: `app.py` `4ce0549cc67cc270` and `start-launcher.sh` `5df8100becefa198` are identical in the repo and on the device, while `hand-deck/launcher` and `cyberdeck/launcher` match neither. The 2026-08-27 archived status was false and it misled a decision earlier the same day (the CARTO key was stripped on the assumption this was a dead project). ⚠️ **Deployed copy = 2026-07-09 → the repo is AHEAD of the device; nothing here is live until deployed.** Earlier the same day: the shared CARTO key was REMOVED from the tile URLs (public repo) — with no key-entry UI yet, so the three CARTO layers render CARTO's "API KEY REQUIRED" watermark while OSM/Esri/local are unaffected; **that decision is worth revisiting precisely because this app is live**, and its Stadia `terrain` layer is keyless → HTTP 401 blocked tiles. The old key value stays in history deliberately; rotating at CARTO is what neutralises it. · 2026-08-27

# hd-dashboard — Overview Card

> Quick-reference card — crucial info for Filip + Haskill. Full context & changelog → `hd-dashboard/hd-dashboard.md`.
> ⚠️ **CORRECTED 2026-09-25 (DeepSeek): this repo is NOT archived — it IS the live Hand-Deck launcher.** Deployed at **`/home/radxa/launcher`** on **`radxa-cubie-a7a`** (user `radxa`), systemd user unit **`launcher.service`** (`ExecStart=/usr/bin/python3 /home/radxa/launcher/app.py`), **port 8080**, started by `~/Desktop/HandDeck-Launcher.desktop` → `/home/radxa/launcher/start-launcher.sh`, which opens Firefox kiosk at `localhost:8080`. **Verified by hash, not by prose:** `app.py` = `4ce0549cc67cc270` and `start-launcher.sh` = `5df8100becefa198` on both the repo and the device. The 2026-08-27 "archived" status was **wrong**, and it misled at least one decision (the key was stripped as if this were a dead project). ⚠️ **The deployed copy dates from 2026-07-09, so the repo is AHEAD of the device** — anything committed here is not live until deployed.
> **Deploy (run on the device):** `cp -a ~/Projects/hd-dashboard/. /home/radxa/launcher/` then `systemctl --user restart launcher.service`. ⚠️ Note the trailing `/.` — `cp -r <dir> ~/launcher` (as older docs show) copies the *directory* into the existing one and creates `~/launcher/hd-dashboard`. ⚠️ Also note `~/Projects/hand-deck/launcher/` is a **dead pre-S365 copy** — never deploy from it.

## Overview

| Field | Value |
|-------|-------|
| **Status** | 🗄️ **ARCHIVED / not-active (2026-08-27, S411).** Follows [[hand-deck-overview]], which is **⏸️ shelved** — the launcher has no host to run on while HD is down.<br>**Not deleted, deliberately:** HD's problem is **hardware**, not this code. If HD is re-brained (RK3588 / Rock-5), this launcher is expected to be **directly reusable**.<br>Last code change 2026-07-09 (`dcd0b34`) · ⚠️ one uncommitted tile-URL patch, see *Repo* |
| **Type** | app — kiosk launcher / dashboard (Flask) |
| **Device / Host** | **Hand-Deck (A7A, Radxa)** — user `radxa`<br>Runs nowhere else. HD has been offline since ~2026-07 |
| **IP / Tailscale** | — (HD offline; was reachable on the tailnet when running) |
| **Ports** | **8080** (Flask, `0.0.0.0`) |
| **Access** | `http://<HD>:8080` when HD is up — kiosk UI on the 7" panel |
| **Repo** | `github.com/Slofi/HD-dashboard`<br>Deployed at **`~/launcher` on HD** (radxa) as a **pull-only checkout**<br>HEAD `dcd0b34` (2026-07-09) — *"Fix Shutdown tile: actually close the browser + full teardown"*<br>⚠️ **`templates/map.html` is modified and uncommitted** — the 2026-08-26 CARTO key patch. Inert (HD is offline) but **not in git**; see [[map-tiles-overview]] |
| **Service** | `launcher.service` (systemd, `WantedBy=default.target`)<br>`WorkingDirectory=/home/radxa/launcher` · `ExecStart=/usr/bin/python3 …/app.py`<br>`Restart=on-failure` · needs `DISPLAY=:0` + `XDG_RUNTIME_DIR=/run/user/1000` |
| **Key paths** | On HD: `~/launcher/` (checkout + service WorkingDirectory)<br>In repo: `app.py` · `launcher.service` · `HandDeck.desktop` · `start-launcher.sh`<br>Helper scripts: `win-switcher.py` · `cycle-windows.sh` · `toggle-desktop.sh` · `toggle-switcher.sh` · `fix-alt-key.sh` |
| **What it launches** | Apps as **Vivaldi kiosks** (`--kiosk --start-fullscreen`, overscroll-history-nav disabled):<br>**OM Lite** → `http://localhost:8082/lite`<br>**OPS-TOC Lite** → `http://localhost:8090/lite`<br>Also polls `http://localhost:8090/api/gps` for GPS |
| **Features** | Self-update from the tile UI (**Version / Update / Restart**) · shutdown tile with full browser teardown · window cycling + Alt-key fix for the A7A panel |
| **Depends on** | [[hand-deck-overview]] (**the host — currently shelved, this is the blocker**) · [[overmesh-overview]] (OM Lite on :8082) · [[ops-toc-overview]] (OPS-TOC Lite + GPS on :8090) · Vivaldi browser · [[map-tiles-overview]] — CARTO basemaps need `?key=` since 2026-08-26 (patched on disk, **uncommitted**, unverified in a browser since HD is offline) |
| **Updated** | **2026-08-27 (S411 — card + main note created (they never existed, an SOP v2 gap); archived as not-active at Filip's direction, with the revival rationale recorded)** |

---

## Why it is kept and not deleted

🔴 **Filip's reasoning, 2026-08-27 — record this so nobody bins it in a later cleanup:**

> *"The HD problem is HW, if we change it, it may be useful."*

Hand-Deck was shelved because of the **A7A/PowerVR platform ceiling** — software-rendered laggy UI, no
Wayland, and a failed power-cap fix. **None of those are faults in this launcher.** The code is a
plain Flask app driving Vivaldi kiosks; it is not tied to the A7A beyond the Alt-key/window-switcher
workarounds written for that panel.

**Revival path:** if HD is re-brained onto **RK3588 / Rock-5** (the route recorded on
[[hand-deck-overview]]), this launcher should come back with little or no change — and would be
strictly *better* off, since the RK3588 fixes exactly the rendering problems the workarounds exist for.

**So: archived, not dead.** Do not delete the repo or the local checkout.

## Quick Commands

> ⚠️ All of these need **HD to be running**, which it is not. Kept for the revival.

| Command | What it does |
|---------|--------------|
| `systemctl --user status launcher` | Service state on HD |
| `systemctl --user restart launcher` | Restart the launcher |
| `journalctl --user -u launcher -n 50 --no-pager` | Recent logs |
| `cd ~/launcher && git pull` | Update the pull-only checkout (or use the in-UI Update tile) |
| `curl -s localhost:8080 -o /dev/null -w '%{http_code}\n'` | Is the launcher answering |
| `curl -s localhost:8090/api/gps` | GPS feed it depends on (OPS-TOC) |

## Troubleshooting / Recovery

- **Blank screen / kiosk won't start:** the service needs `DISPLAY=:0` and
  `XDG_RUNTIME_DIR=/run/user/1000` in its unit. Without them it starts and silently renders nothing.
- **Tiles launch nothing:** the targets are *other apps' ports* — OM Lite on **:8082**, OPS-TOC Lite on
  **:8090**. If those aren't up, the launcher is fine and its dependencies are not.
- **⚠️ There is a second, stale copy at `Projects/hand-deck/launcher/`** — **not a git repo**, superseded
  by this one when the launcher was split out at S365. `projects.md` has carried "retire stale
  `hand-deck/launcher` copy" as a TODO since then. **Still not done** — left alone during the S411
  cleanup because it is HD's own tree, not a duplicate checkout of this repo.
- **Map shows "API KEY REQUIRED":** CARTO needs `?key=` since 2026-08-26 → [[map-tiles-overview]].
  `templates/map.html` is already patched **but uncommitted**, so a fresh `git pull` on HD would
  **not** carry the fix. Commit before any revival.
- **If reviving on new hardware:** the Alt-key and window-switcher scripts (`fix-alt-key.sh`,
  `win-switcher.py`, `toggle-switcher.sh`) are **A7A/PowerVR workarounds**. Re-check whether they are
  still needed before carrying them over — on RK3588 they may be unnecessary or actively wrong.
