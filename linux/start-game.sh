#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttfUsername
read -p "Gameserver (DEFAULT:  167.114.28.238): " TTF_GAMESERVER
TTF_GAMESERVER=${TTF_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export ttfUsername=$ttfUsername
export ttfPassword="password"
export TTF_PLAYCOOKIE=$ttfUsername
export TTF_GAMESERVER=$ttf_GAMESERVER

echo "==============================="
echo "Starting Toontown fellowship"
echo "Username: $ttfUsername"
echo "Gameserver: $TTF_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart
