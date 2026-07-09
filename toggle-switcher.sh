#!/bin/bash
if pgrep -f win-switcher.py > /dev/null; then
    pkill -f win-switcher.py
else
    DISPLAY=:0 XAUTHORITY=/home/radxa/.Xauthority python3 /home/radxa/launcher/win-switcher.py
fi
