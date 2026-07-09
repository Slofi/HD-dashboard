#!/bin/bash
systemctl --user start launcher
for i in $(seq 1 20); do
    nc -z localhost 8080 2>/dev/null && break
    sleep 0.5
done
vivaldi-stable --app=http://localhost:8080 --start-fullscreen
