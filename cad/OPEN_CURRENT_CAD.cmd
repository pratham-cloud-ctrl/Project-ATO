@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0open-current-cad.ps1" %*
if errorlevel 1 (
  echo.
  echo The CAD launcher could not complete. Read the message above and cad\CURRENT_CAD.md.
  pause
  exit /b 1
)
