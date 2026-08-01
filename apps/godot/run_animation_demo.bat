@echo off
setlocal
set "PROJECT_DIR=%~dp0"

if defined GODOT_EXE if exist "%GODOT_EXE%" goto run

for %%G in (godot.exe godot4.exe) do (
  where %%G >nul 2>nul
  if not errorlevel 1 (
    set "GODOT_EXE=%%G"
    goto run
  )
)

for %%G in ("%PROJECT_DIR%..\..\..\tools\godot-4.7.1\Godot_v4.7.1-stable_win64.exe" "%PROJECT_DIR%Godot_v4.7.1-stable_win64.exe" "%PROJECT_DIR%Godot_v4.6-stable_win64.exe") do (
  if exist "%%~fG" (
    set "GODOT_EXE=%%~fG"
    goto run
  )
)

echo [ERROR] Godot 4.x was not found.
echo Set GODOT_EXE to your Godot executable and run this file again.
exit /b 1

:run
echo Starting Shanhe Wuming prologue animation demo...
"%GODOT_EXE%" --path "%PROJECT_DIR%" --scene res://scenes/demo/PrologueAnimationDemo.tscn
