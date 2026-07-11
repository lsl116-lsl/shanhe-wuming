@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "GODOT_EXE="

if defined GODOT_BIN (
  if exist "%GODOT_BIN%" (
    set "GODOT_EXE=%GODOT_BIN%"
  )
)

if not defined GODOT_EXE (
  for %%G in (godot_console.exe godot.exe godot4.exe) do (
    for /f "delims=" %%P in ('where %%G 2^>nul') do if not defined GODOT_EXE set "GODOT_EXE=%%P"
  )
)

if not defined GODOT_EXE (
  if exist "D:\software\Godot\4.7-stable\godot_console.exe" (
    set "GODOT_EXE=D:\software\Godot\4.7-stable\godot_console.exe"
  )
)

if not defined GODOT_EXE (
  echo [ERROR] Godot 4.x was not found. Set GODOT_BIN first.
  pause
  exit /b 1
)

if not exist "%SCRIPT_DIR%\export_presets.cfg" (
  echo [ERROR] export_presets.cfg is missing.
  pause
  exit /b 1
)

if not exist "%SCRIPT_DIR%\build\windows" mkdir "%SCRIPT_DIR%\build\windows"

echo Using Godot: "%GODOT_EXE%"
echo Exporting Windows Desktop P5...
"%GODOT_EXE%" --headless --path "%SCRIPT_DIR%" --export-release "Windows Desktop" "%SCRIPT_DIR%\build\windows\ShanheWuming_P5.exe"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo [ERROR] Windows export failed with exit code %EXIT_CODE%.
  echo Make sure export templates matching this Godot version are installed.
  pause
  exit /b %EXIT_CODE%
)

if not exist "%SCRIPT_DIR%\build\windows\ShanheWuming_P5.pck" (
  echo [ERROR] ShanheWuming_P5.pck was not generated.
  pause
  exit /b 1
)

echo [OK] build\windows\ShanheWuming_P5.exe
echo [OK] build\windows\ShanheWuming_P5.pck
echo Keep the EXE and PCK in the same directory.
pause
exit /b 0
