@echo off
chcp 65001 >nul
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
  for %%G in (godot.exe godot4.exe) do (
    for /f "delims=" %%P in ('where %%G 2^>nul') do if not defined GODOT_EXE set "GODOT_EXE=%%P"
  )
)

if not defined GODOT_EXE (
  if exist "%LOCALAPPDATA%\Programs\Godot\Godot.exe" (
    set "GODOT_EXE=%LOCALAPPDATA%\Programs\Godot\Godot.exe"
  )
)
if not defined GODOT_EXE (
  if exist "%ProgramFiles%\Godot\Godot.exe" (
    set "GODOT_EXE=%ProgramFiles%\Godot\Godot.exe"
  )
)

if not defined GODOT_EXE (
  echo [错误] 未找到 Godot 4.x。
  echo 请安装 Godot 4.x 稳定版，并将 GODOT_BIN 指向 Godot 可执行文件。
  echo 示例: set GODOT_BIN=C:\Tools\Godot\Godot_v4.7-stable_win64.exe
  pause
  exit /b 1
)

echo 使用 Godot: "%GODOT_EXE%"
"%GODOT_EXE%" --path "%SCRIPT_DIR%" %*
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo [错误] 游戏启动失败，退出代码: %EXIT_CODE%
  pause
)

exit /b %EXIT_CODE%
