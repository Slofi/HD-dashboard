#!/bin/bash
# Wait for plasmashell to finish loading (KDE overrides xmodmap on startup)
sleep 6
DISPLAY=:0
XAUTHORITY=/home/radxa/.Xauthority
export DISPLAY XAUTHORITY

# Remap Alt key (keycode 108 = ISO_Level3_Shift) to real Alt (Mod1)
xmodmap -e "keycode 108 = Alt_L"
xmodmap -e "add mod1 = Alt_L"

sleep 1

# Restart kwin so it re-registers Alt+F4/Alt+Tab grabs with new modifier map
KWIN_PID=$(pgrep kwin_x11)
if [ -n "$KWIN_PID" ]; then
    DBUS=$(cat /proc/$KWIN_PID/environ | tr '\0' '\n' | grep DBUS_SESSION_BUS_ADDRESS | head -1)
    export $DBUS
    XDG_RUNTIME_DIR=$(cat /proc/$KWIN_PID/environ | tr '\0' '\n' | grep XDG_RUNTIME_DIR | head -1 | cut -d= -f2-)
    export XDG_RUNTIME_DIR
fi
nohup kwin_x11 --replace > /tmp/kwin-startup.log 2>&1 &
