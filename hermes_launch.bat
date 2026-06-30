@echo off
chcp 65001 >nul
title Hermes - 贾维斯
echo Starting Hermes Dashboard...
start "" "C:\Users\EDY\.workbuddy\binaries\python\versions\3.13.12\Scripts\hermes.exe" dashboard --skip-build --port 9119
timeout /t 3 /nobreak >nul
start http://127.0.0.1:9119
