@echo off
setlocal
if not defined ATO_FREECAD_EXE set "ATO_FREECAD_EXE=E:\project workspace assests\CAD\FreeCAD\bin\FreeCAD.exe"
if not exist "%ATO_FREECAD_EXE%" (
 echo Set ATO_FREECAD_EXE to your FreeCAD executable.
 pause
 exit /b 1
)
start "" "%ATO_FREECAD_EXE%" "%~dp0ATO_reference_assembly.FCStd"
