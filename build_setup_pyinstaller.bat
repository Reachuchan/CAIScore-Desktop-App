@echo off
setlocal
cd /d %~dp0

set USERPROFILE=%cd%
set HOMEDRIVE=C:
set HOMEPATH=\Users\lenovo\Documents\Codex\2026-04-22-new-chat

echo [1/3] Build desktop app and portable zip...
call build_caiscore_r_app_exe.bat
if errorlevel 1 exit /b 1
call build_caiscore_portable_min.bat
if errorlevel 1 exit /b 1

echo [2/3] Build setup executable...
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name CAIScore_Setup ^
  --icon "assets\liver_icon.ico" ^
  --add-data "release\CAIScore_Desktop_Portable_Min_Fixed_v2.zip;." ^
  setup_installer.py
if errorlevel 1 exit /b 1

echo [3/3] Copy setup to release...
copy /y "dist\CAIScore_Setup.exe" "release\CAIScore_Setup.exe" >nul
echo Setup EXE: %cd%\release\CAIScore_Setup.exe
