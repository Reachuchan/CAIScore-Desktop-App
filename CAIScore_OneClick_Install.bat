@echo off
setlocal
set "BASE_URL=https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download"
set "WORKDIR=%~dp0CAIScore_Installer_Files"

if not exist "%WORKDIR%" mkdir "%WORKDIR%"
cd /d "%WORKDIR%"

echo Downloading CAIScore installer files...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProgressPreference='Continue';" ^
  "$files=@(" ^
  "'CAIScore_Setup.exe'," ^
  "'Install_CAIScore_From_Parts.ps1'," ^
  "'CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part001'," ^
  "'CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part002'," ^
  "'CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part003'" ^
  ");" ^
  "$base='%BASE_URL%';" ^
  "foreach($f in $files){" ^
  "  $out=Join-Path (Get-Location) $f;" ^
  "  if(-not (Test-Path $out)){" ^
  "    Invoke-WebRequest -Uri ($base + '/' + $f) -OutFile $out" ^
  "  }" ^
  "};" ^
  "& powershell -NoProfile -ExecutionPolicy Bypass -File '.\Install_CAIScore_From_Parts.ps1'"

if errorlevel 1 (
  echo.
  echo Installation failed. Please keep this window open and contact the developer.
  pause
  exit /b 1
)

echo.
echo Installation finished.
pause
