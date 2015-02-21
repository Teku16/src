@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttfUsername="Username: "
set /P TTF_GAMESERVER="Gameserver (DEFAULT: 167.114.28.238): " || ^
set TTF_GAMESERVER=167.114.28.238

rem Export the environment variables:
set ttfPassword=password
set TTF_PLAYCOOKIE=%ttfUsername%

echo ===============================
echo Starting Toontown fellowship...
echo ppython: %PPYTHON_PATH%
echo Username: %ttfUsername%
echo Gameserver: %TTF_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
