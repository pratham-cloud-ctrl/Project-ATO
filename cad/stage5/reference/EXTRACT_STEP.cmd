@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0extract_steps.ps1"
if errorlevel 1 pause
