#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttfUsername

# Export the environment variables:
export ttfUsername=$ttfUsername
export ttfPassword="password"
export TTF_PLAYCOOKIE=$ttfUsername
export TTF_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Fellowship"
echo "Username: $ttfUsername"
echo "Gameserver: $TTF_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart
