@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttfUsername="Username: "

rem Export the environment variables:
set ttfPassword=password
set TTF_PLAYCOOKIE=%ttfUsername%
set TTF_GAMESERVER=127.0.0.1

echo ===============================
echo Starting Toontown Fellowship...
echo ppython: %PPYTHON_PATH%
echo Username: %ttfUsername%
echo Gameserver: %TTF_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
