type:: project
project:: hd-dashboard
status:: live
tags:: #hand-deck #launcher #kiosk #flask #live
updated:: 2026-09-25 (DeepSeek — ⚠️ **STATUS CORRECTED: LIVE, not archived.** This repo **is** the Hand-Deck launcher running on the A7A right now — `/home/radxa/launcher`, unit `launcher.service`, port 8080, opened by the desktop shortcut. Verified by hash, and only `templates/map.html` is undeployed. Earlier the same day: the shared CARTO key was removed from the tile URLs (public repo). **Revisit the no-key-entry-UI decision — this app is live**, and its default layer `voyager` is a CARTO layer, so the kiosk opens on a watermarked basemap. The old key value stays in history deliberately; rotating at CARTO is what neutralises it. Full detail → `hd-dashboard-overview.md` `updated::`) · 2026-08-27

# hd-dashboard — Hand-Deck Kiosk Launcher

> **Crucial fields (status, host, ports, service, repo, key paths, commands, troubleshooting) live on
> the card: `hd-dashboard-overview.md`.** This file holds context, decisions and changelog only.
> One fact, one home — do not copy the card's tables here.

---

## What it is

The kiosk launcher for **Hand-Deck**: a small Flask app on the A7A's 7" panel that presents tiles and
launches the field apps as full-screen Vivaldi kiosks (OM Lite, OPS-TOC Lite), plus a self-update
tile, a clean shutdown tile, and window-management helpers written for that panel.

Split out of the `hand-deck` project and put under git at **S365** so HD could pull updates rather
than being hand-edited.

---

## Status — ⚠️ CORRECTED 2026-09-25: **LIVE, not archived**

**This section said "archived 2026-08-27 (S411) … with no host to run on, the launcher is not active."** That is **false**, and it was believed for weeks. The launcher runs on the **A7A handheld right now**: `/home/radxa/launcher`, unit `launcher.service` (port 8080), started by `~/Desktop/HandDeck-Launcher.desktop` → `/home/radxa/launcher/start-launcher.sh`, opening Firefox kiosk at `localhost:8080`.

**Proof is by hash, not by prose** — the repo and the running tree agree exactly:

| file | repo (`~/Projects/hd-dashboard`) | live (`/home/radxa/launcher`) |
|---|---|---|
| `app.py` | `4ce0549cc67cc270` | `4ce0549cc67cc270` ✔ |
| `start-launcher.sh` | `5df8100becefa198` | `5df8100becefa198` ✔ |
| `templates/index.html` | `f219d47073` | `f219d47073` ✔ |
| `launcher.service` | `dd2cdc9a8a` | `dd2cdc9a8a` ✔ |
| `templates/map.html` | `db54898ce4` | `a7603bf2b6` ✗ **the only file that differs** |

So the repo is **not** far ahead of the device — exactly **one file** (`templates/map.html`) is undeployed. Everything else is byte-identical.

**Why the status was wrong, and what it cost:** the 2026-08-27 entry below was Filip's call *at that moment* — the A7A had no usable host and the project was going dormant. It was never reversed when the launcher went back into service for the deck. Catching it: the CARTO key was stripped from `templates/map.html` earlier on 2026-09-25 on the assumption this was a dead project with no users, and a key-entry field was deliberately **not** added. **That decision is worth revisiting precisely because the app is live** — and because the live default layer is `voyager`, a CARTO layer, so the kiosk today opens on a **watermarked** basemap.

**Deploy is one file** (`~/Projects/hd-dashboard` → the device): ⚠️ use the trailing `/.` — `cp -r <dir> ~/launcher` copies the *directory inside* the existing one and creates `~/launcher/hd-dashboard`.

**The 2026-08-27 archive call, kept for the record (superseded, as above):**
**Filip's call, that session.** It followed Hand-Deck, which is shelved; with no host to run on, the
launcher was believed inactive. **Archived, not deleted** — the rationale and revival path are on the card
under *Why it is kept and not deleted*. Short version, in his words:

> *"The HD problem is HW, if we change it, it may be useful."*

The A7A/PowerVR ceiling that shelved HD is a **hardware** limitation. This launcher is ordinary Flask
+ browser-kiosk code and should port to an RK3588/Rock-5 re-brain largely unchanged.

---

## Decisions

- **2026-08-27 (Filip, S411): archive `hd-dashboard`; keep the repo and the local checkout.** Reason:
  the shelving cause is HD's hardware, not this code, and a re-brain would make it useful again.
  A note pointing here was added to [[hand-deck-overview]] so it is discoverable from the HD side —
  the side Filip would actually be looking at if he revives the hardware.
- **2026-08-27 (Claude, S411): created the card AND this note — neither had ever existed.** Found while
  adding `Depends-on` pointers for the CARTO work: `hd-dashboard` was listed **Active** in
  `projects.md` with **no `.md` file of any kind** in its folder. A real SOP v2 gap, not a stale card.
  ⚠️ **Worth generalising:** the card-freshness check compares declared dates on cards that *exist*;
  a project with **no card at all** is invisible to it. Same failure shape as the S403 backup check
  that only caught backups which *broke*, never one that never existed. **A "project folder with no
  `*-overview.md`" sweep would close it** — see `report-notes.md`.
- **S365: split out of `hand-deck` into its own repo** (`Slofi/HD-dashboard`), deployed to `~/launcher`
  on HD as a pull-only checkout with in-UI self-update.

## Open / carried

- ⚠️ **`templates/map.html` is patched but UNCOMMITTED** — the 2026-08-26 CARTO key fix. Inert while
  HD is offline, but it is **not in git**, so a fresh pull on a revived HD would serve watermarked
  tiles. This is a small instance of the same pattern that left overmesh-lite with ~2 months of
  git-unbacked work. **Commit it before or during any revival.** Not committed in S411 because
  pushing was not authorised for this repo.
- 📌 **The stale `Projects/hand-deck/launcher/` copy is still there** (not a git repo, superseded at
  S365). `projects.md` has carried "retire stale copy" as a TODO since then. Deliberately **not**
  touched during the S411 checkout cleanup — that cleanup removed duplicate *git checkouts*, and this
  is part of HD's own tree. Filip's call whether it goes.

---

## Changelog

- **2026-08-27 (S411, Claude)** — **Card + main note created (neither existed); project archived as
  not-active at Filip's direction.** Details captured from the live code rather than assumed: port
  **8080**, `launcher.service` with its `DISPLAY`/`XDG_RUNTIME_DIR` requirements, the two kiosk targets
  (OM Lite :8082, OPS-TOC Lite :8090) and the GPS poll against :8090. Revival rationale recorded on the
  card; a pointer added to [[hand-deck-overview]] so it surfaces from the HD side. `projects.md` moved
  **Active → Retired/Archived**. Flagged the uncommitted `map.html` tile patch and the still-stale
  `hand-deck/launcher` copy.
- **2026-07-09** — `dcd0b34` *"Fix Shutdown tile: actually close the browser + full teardown"* — last
  code change before archiving.
- **S365** — split out of `hand-deck`, put under git, deployed pull-only to `~/launcher` on HD;
  self-update (Version/Update/Restart) added. OPS-TOC tile switched to launch Lite.
