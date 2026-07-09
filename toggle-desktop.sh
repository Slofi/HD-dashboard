#!/bin/bash
SHOWING=0
if [ "" = "1" ]; then
    DISPLAY=:0 XAUTHORITY=/home/radxa/.Xauthority wmctrl -k off
else
    DISPLAY=:0 XAUTHORITY=/home/radxa/.Xauthority wmctrl -k on
fi
