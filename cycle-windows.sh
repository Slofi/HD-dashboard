#!/bin/bash
DISPLAY=:0
XAUTHORITY=/home/radxa/.Xauthority
export DISPLAY XAUTHORITY

# Get all normal window IDs (skip desktop/docks)
WINDOWS=$(wmctrl -l | awk '$2 != "-1" {print $1}')

if [ -z "$WINDOWS" ]; then exit 0; fi

# Get active window ID (hex, with leading 0x)
ACTIVE_HEX=$(xprop -root _NET_ACTIVE_WINDOW | awk '{print $5}' | tr -d ',')
ACTIVE_DEC=$(printf '%d' "$ACTIVE_HEX" 2>/dev/null || echo 0)

FIRST=""
NEXT=""
FOUND=0

for WID in $WINDOWS; do
    WID_DEC=$(printf '%d' "$WID")
    [ -z "$FIRST" ] && FIRST="$WID"
    if [ "$FOUND" = "1" ]; then
        NEXT="$WID"
        break
    fi
    [ "$WID_DEC" = "$ACTIVE_DEC" ] && FOUND=1
done

# If active was last (or not found), wrap to first
[ -z "$NEXT" ] && NEXT="$FIRST"

[ -n "$NEXT" ] && wmctrl -ia "$NEXT"
