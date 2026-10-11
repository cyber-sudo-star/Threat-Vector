@echo off
title Threat Vector - Instant Free Public Web Link
echo ======================================================================
echo       THREAT VECTOR - INSTANT PUBLIC WEB LINK GENERATOR
echo ======================================================================
echo.
echo 1. Making sure local Flask server is running on port 5000...
echo 2. Connecting to free public tunnel...
echo.
echo Press any key, and a live HTTPS public link will appear on your screen!
echo You can copy that HTTPS link and open it on your phone, tablet, or
echo share it with anyone in the world!
echo.
pause
echo Connecting...
ssh -p 443 -R0:localhost:5000 a.pinggy.io
pause
