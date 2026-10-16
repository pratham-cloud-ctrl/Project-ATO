@echo off
set "ATO_FREECAD=E:\project workspace assests\CAD\FreeCAD\bin\FreeCAD.exe"
if not exist "%ATO_FREECAD%" (
  echo FreeCAD was not found at the configured laptop path.
  echo Open ATO_stage5_reference_full.FCStd with FreeCAD 1.1 or later.
  pause
  exit /b 1
)
start "" "%ATO_FREECAD%" "%~dp0open_reference_inspection.FCMacro"
