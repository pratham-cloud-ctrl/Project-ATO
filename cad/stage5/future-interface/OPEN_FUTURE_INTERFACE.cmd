@echo off
setlocal
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
start "" "E:\project workspace assests\CAD\FreeCAD\bin\FreeCAD.exe" "%~dp0open_future_interface.FCMacro"
