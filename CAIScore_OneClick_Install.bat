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
  "          $job = Start-BitsTransfer -Source $url -Destination $outFile -Asynchronous -DisplayName 'CAIScore download' -Description $url -ErrorAction Stop;" ^
  "          try {" ^
  "            while($true){" ^
  "              $state = $job.JobState.ToString();" ^
  "              if($state -eq 'Transferred'){" ^
  "                Complete-BitsTransfer -BitsJob $job -ErrorAction Stop;" ^
  "                break" ^
  "              }" ^
  "              if($state -in @('Error','TransientError','Cancelled')){" ^
  "                throw ('BITS state: ' + $state)" ^
  "              }" ^
  "              Start-Sleep -Seconds 3;" ^
  "              $job = Get-BitsTransfer -JobId $job.JobId -ErrorAction Stop" ^
  "            }" ^
  "          } finally {" ^
  "            try { Remove-BitsTransfer -BitsJob $job -Confirm:$false -ErrorAction SilentlyContinue } catch {}" ^
  "          }" ^
        "        } else {" ^
  "          & curl.exe --ssl-no-revoke -L --fail --retry 8 --retry-all-errors --retry-delay 5 --connect-timeout 30 --max-time 0 --output $outFile $url;" ^
  "          if($LASTEXITCODE -ne 0){ throw ('curl exit code ' + $LASTEXITCODE) }" ^
  "        }" ^
  "        if(-not (Test-Path $outFile)){ throw 'Downloaded file was not created' }" ^
  "        $actual=(Get-Item $outFile).Length;" ^
  "        if($actual -ne [int64]$expectedSize){ throw ('Downloaded file size mismatch: ' + $actual + ' bytes') }" ^
  "        return" ^
  "      } catch {" ^
  "        Write-Host ('    Failed: ' + $_.Exception.Message) -ForegroundColor Yellow;" ^
  "        if(Test-Path $outFile){ Remove-Item -Force $outFile -ErrorAction SilentlyContinue }" ^
  "        Start-Sleep -Seconds 3" ^
  "      }" ^
  "    }" ^
  "  }" ^
  "  throw ('Download failed after multiple retries: ' + $outFile)" ^
  "}" ^
  "$files=@(" ^
  "  @{Name='CAIScore_Setup.exe'; Size=8679141}," ^
  "  @{Name='Install_CAIScore_From_Parts.ps1'; Size=1691}," ^
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
