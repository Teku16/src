#!/bin/sh
cd ..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " ttfUsername
read -p "Gameserver (DEFAULT:  www.ToontownFellowship.com): " TTF_GAMESERVER
TTF_GAMESERVER=${TTF_GAMESERVER:-"www.ToontownFellowship.com"}

# Export the environment variables:
export ttfUsername=$ttfUsername
export ttfPassword="password"
export TTF_PLAYCOOKIE=$ttfUsername
export TTF_GAMESERVER=$TTF_GAMESERVER

echo "==============================="
echo "Starting Toontown Fellowship"
echo "Username: $ttfUsername"
echo "Gameserver: $TTF_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ClientStart

