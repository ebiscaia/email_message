#!/bin/sh

if [ ! -f /app/files/auth.json ] && [ ! -f /app/files/auth.json.example ]; then 
    echo "Adding example of config file..."
    cp /defaults/auth.json.example /app/files/
fi

exec main.py
