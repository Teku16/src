@echo off 
title Toontown Edge Console
echo.UPDATING CLIENT THIS MAY TAKE A MINUTE
cd C:/repos/resources
git fetch origin master --quiet
echo.RESOURCES ARE DONE UPDATING...NOW SYSTEM FILES
cd C:/repos/src
git fetch origin master --quiet
cls
echo.Successfully updated Toontown Edge files!
echo.

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttiUsername="Username: "
set /P TTI_GAMESERVER="Gameserver (DEFAULT: toontownedge.mooo.com): " || ^
set TTI_GAMESERVER=toontownedge.mooo.com
goto launch
:replay
echo.Please press enter to launch the game again! (not sufficient for an update)
pause>nul
goto launch
:launch
rem Export the environment variables:
set ttiPassword=password
set TTI_PLAYCOOKIE=%ttiUsername%

echo ===============================
echo Starting Toontown Edge...
rem echo ppython: %PPYTHON_PATH%
echo Username: %ttiUsername%
echo Gameserver: %TTI_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStart
echo.
echo.
echo.Thank you for playing Toontown Edge! Press enter to login again! (without entering your username and IP again)
pause>nul
cls
goto replay