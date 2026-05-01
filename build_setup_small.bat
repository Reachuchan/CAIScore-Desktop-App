@echo off
setlocal
cd /d %~dp0

set USERPROFILE=%cd%
set HOMEDRIVE=C:
set HOMEPATH=\Users\lenovo\Documents\Codex\2026-04-22-new-chat

echo [1/2] Build small setup executable...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name CAIScore_Setup ^
  --icon "assets\liver_icon.ico" ^
  setup_installer.py
if errorlevel 1 exit /b 1

echo [2/2] Copy setup to release...
copy /y "dist\CAIScore_Setup.exe" "release\CAIScore_Setup.exe" >nul
echo Setup EXE: %cd%\release\CAIScore_Setup.exe
