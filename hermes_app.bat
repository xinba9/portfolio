@echo off
chcp 65001 >nul
echo Starting Hermes Dashboard...

REM Start Hermes Dashboard in background
start "" /B "C:\Users\EDY\.workbuddy\binaries\python\versions\3.13.12\Scripts\hermes.exe" dashboard --skip-build --port 9119

REM Wait for server to be ready
timeout /t 5 /nobreak >nul

REM Open in Edge App Mode (looks like native desktop app)
start "" msedge --app=http://127.0.0.1:9119 --new-window
