type:: project-overview
project:: hd-dashboard
tags:: #overview #hand-deck #launcher #kiosk #flask #live
updated:: 2026-09-26 (DeepSeek — the checkout was **moved out of `Projects/Archive/` to `~/Projects/hd-dashboard/`** (Filip's call), and the **doc fork was reconciled into one file**: the tracked copy on `origin/main` and this working tree's untracked copy are now the same file, the checkout is **current with `origin/main` (`37247b0`, was 9 behind; **pushed as `76b0566` on 2026-09-26**)**, and the dirty `templates/map.html` that re-added the **OLD, REVOKED** CARTO key was **discarded, not merged**) · 2026-09-25 (DeepSeek — ⚠️ **STATUS CORRECTED: this repo is NOT archived — it is the LIVE Hand-Deck launcher**, running at `/home/radxa/launcher` on `radxa-cubie-a7a` as `launcher.service` on **port 8080**, opened by the desktop shortcut via `start-launcher.sh`. Proved by hash: `app.py` `4ce0549cc67cc270` and `start-launcher.sh` `5df8100becefa198` are identical in the repo and on the device, while the (since-deleted) `hand-deck/launcher` copy and `cyberdeck/launcher` matched neither. The 2026-08-27 archived status was false and it misled a decision earlier the same day (the CARTO key was stripped on the assumption this was a dead project). ⚠️ **Deployed copy = 2026-07-09 → the repo is AHEAD of the device; nothing here is live until deployed.** Earlier the same day: the shared CARTO key was REMOVED from the tile URLs (public repo)) · 2026-08-27

# hd-dashboard — Overview Card

> Quick-reference card — crucial info for Filip + Haskill. Full context & changelog → `hd-dashboard/hd-dashboard.md`.
> ⚠️ **CORRECTED 2026-09-25 (DeepSeek): this repo is NOT archived — it IS the live Hand-Deck launcher.** Deployed at **`/home/radxa/launcher`** on **`radxa-cubie-a7a`** (user `radxa`), systemd user unit **`launcher.service`** (`ExecStart=/usr/bin/python3 /home/radxa/launcher/app.py`), **port 8080**, started by `~/Desktop/HandDeck-Launcher.desktop` → `/home/radxa/launcher/start-launcher.sh`, which opens Firefox kiosk at `localhost:8080`. **Verified by hash, not by prose:** `app.py` = `4ce0549cc67cc270` and `start-launcher.sh` = `5df8100becefa198` on both the repo and the device. The 2026-08-27 "archived" status was **wrong**, and it misled at least one decision (the key was stripped as if this were a dead project). ⚠️ **The deployed copy dates from 2026-07-09, so the repo is AHEAD of the device** — anything committed here is not live until deployed.
> **Deploy (run on the device):** `cp -a ~/Projects/hd-dashboard/. /home/radxa/launcher/` then `systemctl --user restart launcher.service`. ⚠️ Note the trailing `/.` — `cp -r <dir> ~/launcher` (as older docs show) copies the *directory* into the existing one and creates `~/launcher/hd-dashboard`. ⚠️ Also note `~/Projects/hand-deck/launcher/` — the **dead pre-S365 copy this line used to warn about — was DELETED 2026-09-26** (backup tarball in `~/DeepSeek-Home/notes/snapshots-2026-09-26/`); this repo is now the only source.
> 📦 **2026-09-26 (DeepSeek, Filip's call) — folder + doc fork fixed.** The checkout was **moved out of `Archive/` to `~/Projects/hd-dashboard/`** — the path the deploy line above already assumed. These two doc files had **two homes** (tracked on `origin/main` *and* untracked in the working tree, of different vintages); they are now **one tracked copy**, the checkout is **current with `origin/main`**, and the working tree's `templates/map.html` (which re-added the **OLD, REVOKED** CARTO key) was **discarded**. Nothing in the repo is deployed by this — the device still runs the 2026-07-09 copy (plus the one-file map fix).

## Overview

| Field | Value |
|-------|-------|
| **Status** | ✅ **LIVE — verified 2026-09-25 (DeepSeek); folder moved 2026-09-26.** The earlier **ARCHIVED / not-active** status (2026-08-27, S411) was **false**: HD was re-brained to a **Radxa Cubie A7A**, and this launcher runs there as `launcher.service` on **:8080**, kiosk UI on the 7″ panel, opened by `~/Desktop/HandDeck-Launcher.desktop` → `start-launcher.sh` — confirmed serving (service active, `/` 200, map page serving the deployed file). It read as archived for weeks **only because the checkout lived under `Projects/Archive/`**. Last upstream code change 2026-07-09 (`dcd0b34`). |
| **Type** | app — kiosk launcher / dashboard (Flask) |
| **Device / Host** | **Hand-Deck (A7A, Radxa Cubie A7A)** — user `radxa`, tailnet host **`cubie-a7a-hd`**<br>Runs nowhere else. Powered on **occasionally, not daily** (hand-deck was revived 2026-09-07); **offline 2026-09-26 11:00 CEST**, last seen ~8 h earlier — the old "HD offline since ~2026-07" here was stale |
| **IP / Tailscale** | **100.123.67.117** (`cubie-a7a-hd`) · ⚠️ one of only two tailnet nodes with **key expiry enabled — expires 2026-12-03**; when it lapses HD drops off the tailnet silently and needs re-auth at the machine (detail in `projects.md`) |
| **Ports** | **8080** (Flask, `0.0.0.0`) |
| **Access** | `http://<HD>:8080` when HD is up — kiosk UI on the 7" panel |
| **Repo** | `github.com/Slofi/HD-dashboard` · checkout **`~/Projects/hd-dashboard/`** (was `Projects/Archive/hd-dashboard/`) · **current with `origin/main` `76b0566`** (both 2026-09-26 doc commits **pushed**)<br>Deployed at **`~/launcher` on HD** (radxa) as a **pull-only checkout** — ⚠️ **the deployed copy is older than the repo; nothing here is live until deployed**<br>✅ 2026-09-26: the card + note are **tracked** again (one home), and the working tree's revoked-key `map.html` patch was discarded |
| **Service** | `launcher.service` (systemd, `WantedBy=default.target`)<br>`WorkingDirectory=/home/radxa/launcher` · `ExecStart=/usr/bin/python3 …/app.py`<br>`Restart=on-failure` · needs `DISPLAY=:0` + `XDG_RUNTIME_DIR=/run/user/1000` |
| **Key paths** | On HD: `~/launcher/` (checkout + service WorkingDirectory)<br>In repo: `app.py` · `launcher.service` · `HandDeck.desktop` · `start-launcher.sh`<br>Helper scripts: `win-switcher.py` · `cycle-windows.sh` · `toggle-desktop.sh` · `toggle-switcher.sh` · `fix-alt-key.sh` |
| **What it launches** | Apps as **Vivaldi kiosks** (`--kiosk --start-fullscreen`, overscroll-history-nav disabled):<br>**OM Lite** → `http://localhost:8082/lite`<br>**OPS-TOC Lite** → `http://localhost:8090/lite`<br>Also polls `http://localhost:8090/api/gps` for GPS |
| **Features** | Self-update from the tile UI (**Version / Update / Restart**) · shutdown tile with full browser teardown · window cycling + Alt-key fix for the A7A panel |
| **Depends on** | [[hand-deck-overview]] (**the host** — powered on occasionally) · [[overmesh-overview]] (OM Lite on :8082) · [[ops-toc-overview]] (OPS-TOC Lite + GPS on :8090) · Vivaldi browser · [[map-tiles-overview]] — CARTO basemaps need `?key=` since 2026-08-26; the per-provider key handling is now **committed** (`bbf663b`) and deployed, with a keyless fallback (offline `local` pack, then Esri) |
| **Updated** | **2026-09-26 (DeepSeek — folder moved out of `Archive/`; the doc fork reconciled into one tracked copy; checkout brought current with `origin/main` and the revoked-key `map.html` patch discarded; host/IP filled in from the tailnet)** · **2026-09-25 (DeepSeek — status corrected to LIVE)** · **2026-08-27 (S411 — card + main note created (they never existed, an SOP v2 gap); archived as not-active at Filip's direction, with the revival rationale recorded)** |

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

**So: archived then, LIVE now** (the status was corrected 2026-09-25 — it had not been true since HD was re-brained).
Do not delete the repo or the local checkout; the reasoning above is why it is *kept*.

## Quick Commands

> ⚠️ All of these need **HD to be running**, which it is only **occasionally** (not daily) — verify it is up first.

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
- ✅ **The stale copy at `Projects/hand-deck/launcher/` was DELETED 2026-09-26 (Filip's go).** It was a dead
  pre-S365 copy (`STALE-DO-NOT-USE.md`; 291-line `app.py` from 2026-06-30 vs the real 473) that had already
  misled twice. It **predated this repo**, so its code was in no git history — a **backup tarball** was taken
  first: `~/DeepSeek-Home/notes/snapshots-2026-09-26/hand-deck-launcher-STALE-pre-S365-2026-09-26.tar.gz`.
- **Map shows "API KEY REQUIRED":** CARTO needs `?key=` since 2026-08-26 → [[map-tiles-overview]].
  ✅ This is **fixed and committed** (`bbf663b`: per-provider own-key handling, keyless fallback → offline
  `local` pack, then Esri) and deployed to the device — the older "patched but uncommitted" warning here
  was true until 2026-09-25.
- **If reviving on new hardware:** the Alt-key and window-switcher scripts (`fix-alt-key.sh`,
  `win-switcher.py`, `toggle-switcher.sh`) are **A7A/PowerVR workarounds**. Re-check whether they are
  still needed before carrying them over — on RK3588 they may be unnecessary or actively wrong.
