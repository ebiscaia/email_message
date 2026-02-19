#!/bin/sh

if [ ! -f /auth/files/auth.json ] && [ ! -f /auth/files/auth.json.example ]; then 
    echo "Adding example of config file..."
    cp /defaults/auth.json.example /auth/files/
fi

exec main.py
