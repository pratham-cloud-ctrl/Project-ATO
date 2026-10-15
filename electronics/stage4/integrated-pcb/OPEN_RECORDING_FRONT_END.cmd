@echo off
setlocal
if not defined ATO_KICAD_BIN set "ATO_KICAD_BIN=E:\project workspace assests\EDA\KiCAD\bin"
if not exist "%ATO_KICAD_BIN%\pcbnew.exe" (
  echo Set ATO_KICAD_BIN to your KiCad 10 bin directory.
  pause
  exit /b 1
)
start "" "%ATO_KICAD_BIN%\pcbnew.exe" "%~dp0boards\recording-front-end\recording_front_end.kicad_pcb"
