@echo off
title JARVIS - AI Desktop Assistant
color 0B

echo.
echo  ======================================
echo       JARVIS - SYSTEM INITIALIZING
echo  ======================================
echo.

:: --- Start Backend Server ---
echo [JARVIS] Starting Backend Core...
cd /d "D:\Jarvis_AI"
start /B "" python -m uvicorn api:app --host 127.0.0.1 --port 8000 >nul 2>&1

:: --- Wait for backend to be ready ---
echo [JARVIS] Waiting for backend...
:wait_backend
timeout /t 1 /nobreak >nul
curl -s http://127.0.0.1:8000/health >nul 2>&1
if errorlevel 1 goto wait_backend
echo [JARVIS] Backend is ONLINE.

:: --- Start Frontend Server ---
echo [JARVIS] Starting Frontend Core...
cd /d "D:\Jarvis_AI\jarvis-frontend"
start /B "" npm run dev >nul 2>&1

:: --- Wait for frontend to be ready ---
echo [JARVIS] Waiting for frontend...
:wait_frontend
timeout /t 2 /nobreak >nul
curl -s http://localhost:3000 >nul 2>&1
if errorlevel 1 goto wait_frontend
echo [JARVIS] Frontend is ONLINE.

:: --- Launch as Desktop App (Chrome App Mode) ---
echo.
echo [JARVIS] Launching Desktop Interface...
echo.

:: Try Chrome first, then Edge
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://localhost:3000 --window-size=1400,900 --disable-extensions --new-window
    goto :launched
)

if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --app=http://localhost:3000 --window-size=1400,900 --disable-extensions --new-window
    goto :launched
)

:: Fallback to Edge (always available on Windows 10/11)
start "" msedge --app=http://localhost:3000 --window-size=1400,900 --disable-extensions --new-window

:launched
echo.
echo  ======================================
echo      JARVIS PROTOCOL ALPHA - ACTIVE
echo.
echo   Press Ctrl+C to shutdown all services
echo  ======================================
echo.

:: Keep the script alive so services stay running
:keepalive
timeout /t 30 /nobreak >nul
goto keepalive
