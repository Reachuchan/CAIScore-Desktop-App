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
  "  @{Name='CAIScore_Setup.exe'; Size=8679141}," ^
  "  @{Name='Install_CAIScore_From_Parts.ps1'; Size=768}," ^
  "  @{Name='CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part001'; Size=1992294400}," ^
  "  @{Name='CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part002'; Size=1992294400}," ^
  "  @{Name='CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part003'; Size=730086136}" ^
  ");" ^
  "$base='%BASE_URL%';" ^
  "foreach($f in $files){" ^
  "  $out=Join-Path (Get-Location) $f.Name;" ^
  "  $needDownload=$true;" ^
  "  if(Test-Path $out){" ^
  "    $actual=(Get-Item $out).Length;" ^
  "    if($actual -eq [int64]$f.Size){ $needDownload=$false } else { Remove-Item -Force $out }" ^
  "  }" ^
  "  if($needDownload){" ^
  "    Write-Host ('Downloading ' + $f.Name + ' ...');" ^
  "    & curl.exe --ssl-no-revoke -L --fail --output $out ($base + '/' + $f.Name);" ^
  "    if($LASTEXITCODE -ne 0){ throw ('Download failed: ' + $f.Name) }" ^
  "    $actual=(Get-Item $out).Length;" ^
  "    if($actual -ne [int64]$f.Size){ throw ('Downloaded file size mismatch: ' + $f.Name + ' (' + $actual + ' bytes)') }" ^
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
