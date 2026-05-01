@echo off
cd /d %~dp0

echo [1/3] Checking PyInstaller...
python -c "import PyInstaller; print(PyInstaller.__version__)" >nul 2>nul
if errorlevel 1 (
  echo Installing PyInstaller...
  python -m pip install pyinstaller
  if errorlevel 1 (
    echo Failed to install PyInstaller.
    pause
    exit /b 1
  )
)

echo [2/3] Building CAIScore desktop EXE...
set USERPROFILE=%cd%
set HOMEDRIVE=C:
set HOMEPATH=\Users\lenovo\Documents\Codex\2026-04-22-new-chat
python -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --windowed ^
  --name CAIScore_Desktop_App ^
  --icon "assets\\liver_icon.ico" ^
  --add-data "caiscore_source;caiscore_source" ^
  --add-data "sample_data;sample_data" ^
  --add-data "assets;assets" ^
  --add-data "caiscore_predict_cli.R;." ^
  caiscore_desktop_app.py

if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo [3/3] Build complete.
echo EXE: %~dp0dist\CAIScore_Desktop_App.exe
