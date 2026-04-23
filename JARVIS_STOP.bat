@echo off
title JARVIS — Shutting Down
color 0C

echo.
echo  [JARVIS] Terminating all services...
echo.

:: Kill the backend (uvicorn/python)
taskkill /f /im python.exe /fi "WINDOWTITLE eq *uvicorn*" >nul 2>&1
taskkill /f /im uvicorn.exe >nul 2>&1

:: Kill the frontend (node/next)
taskkill /f /im node.exe /fi "WINDOWTITLE eq *next*" >nul 2>&1

echo  [JARVIS] All services terminated.
echo.
pause
