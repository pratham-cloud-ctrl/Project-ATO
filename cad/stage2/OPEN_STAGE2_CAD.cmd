@echo off
set "ATO_STAGE2_FREECAD=E:\project workspace assests\CAD\FreeCAD\bin\FreeCAD.exe"
if not exist "%ATO_STAGE2_FREECAD%" (
  echo Set ATO_STAGE2_FREECAD in this launcher to your FreeCAD executable.
  pause
  exit /b 1
)
start "" "%ATO_STAGE2_FREECAD%" "%~dp0ATO_stage2_allocation.FCStd"
