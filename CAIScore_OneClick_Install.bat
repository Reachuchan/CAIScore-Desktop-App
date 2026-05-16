@echo off
setlocal
set "BASE_URL=https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download"
set "WORKDIR=%~dp0CAIScore_Installer_Files"

if not exist "%WORKDIR%" mkdir "%WORKDIR%"
cd /d "%WORKDIR%"

echo Downloading CAIScore installer files...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ProgressPreference='Continue';" ^
  "function Download-WithRetry($url, $outFile, $expectedSize){" ^
  "  $methods=@('BITS','CURL');" ^
  "  foreach($method in $methods){" ^
  "    for($i=1; $i -le 3; $i++){" ^
  "      try {" ^
  "        if(Test-Path $outFile){ Remove-Item -Force $outFile }" ^
  "        Write-Host ('  Attempt ' + $i + ' via ' + $method);" ^
  "        if($method -eq 'BITS'){" ^
  "          Start-BitsTransfer -Source $url -Destination $outFile -DisplayName 'CAIScore download' -Description $url" ^
  "        } else {" ^
  "          & curl.exe --ssl-no-revoke -L --fail --retry 5 --retry-delay 5 --connect-timeout 30 --output $outFile $url;" ^
  "          if($LASTEXITCODE -ne 0){ throw ('curl exit code ' + $LASTEXITCODE) }" ^
  "        }" ^
  "        $actual=(Get-Item $outFile).Length;" ^
  "        if($actual -ne [int64]$expectedSize){ throw ('Downloaded file size mismatch: ' + $actual + ' bytes') }" ^
  "        return" ^
  "      } catch {" ^
  "        Write-Host ('    Failed: ' + $_.Exception.Message) -ForegroundColor Yellow;" ^
  "        Start-Sleep -Seconds 3" ^
  "      }" ^
  "    }" ^
  "  }" ^
  "  throw ('Download failed after multiple retries: ' + $outFile)" ^
  "}" ^
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
  "    Download-WithRetry ($base + '/' + $f.Name) $out $f.Size" ^
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
