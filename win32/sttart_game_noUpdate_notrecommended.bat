@echo off 
title Toontown: The Edge Console
cd C:\repos\src

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttiUsername="Username: "
set /P TTI_GAMESERVER="Gameserver (DEFAULT: toontownedge.mooo.com): " || ^
set TTI_GAMESERVER=toontownedge.mooo.com
goto launch
:replay
echo.Please press enter to launch the game again!
pause>nul
goto launch
:launch
rem Export the environment variables:
set ttiPassword=password
set TTI_PLAYCOOKIE=%ttiUsername%

echo ===============================
echo Starting Toontown: The Edge...
echo ppython: %PPYTHON_PATH%
echo Username: %ttiUsername%
echo Gameserver: %TTI_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
echo.
echo.
echo.Thank you for playing Toontown: The Edge! Press enter to login again! (without entering your username and IP again)
pause>nul
cls
goto replay