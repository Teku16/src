@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttfUsername="Username: "
set /P ttfPassword="Password: "

rem Export the environment variables:
set TTF_PLAYCOOKIE=%ttfUsername%:%ttfPassword%
set TTF_GAMESERVER=toontownfellowship.com

echo ===============================
echo Starting Toontown Fellowship...
echo ppython: %PPYTHON_PATH%
echo Username: %ttfUsername%
echo Gameserver: %TTF_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
pause
