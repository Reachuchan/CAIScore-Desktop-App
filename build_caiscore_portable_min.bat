@echo off
setlocal
cd /d %~dp0

set EXE_PATH=dist\CAIScore_Desktop_App.exe
set R_SRC=D:\R\R-4.3.1
set OUT_DIR=release\CAIScore_Desktop_Portable_Min
set ZIP_PATH=release\CAIScore_Desktop_Portable_Min_Fixed_v2.zip

if not exist "%EXE_PATH%" (
  echo EXE not found. Build it first...
  call build_caiscore_r_app_exe.bat
  if errorlevel 1 exit /b 1
)

if not exist "%R_SRC%\bin\Rscript.exe" (
  echo R runtime not found: %R_SRC%
  exit /b 1
)

echo [1/4] Prepare output folder...
if exist "%OUT_DIR%" rmdir /s /q "%OUT_DIR%"
mkdir "%OUT_DIR%\runtime\R\library"

echo [2/4] Copy app and R runtime core...
copy /y "%EXE_PATH%" "%OUT_DIR%\CAIScore_Desktop_App.exe" >nul
xcopy "%R_SRC%\bin" "%OUT_DIR%\runtime\R\bin\" /E /I /H /Y >nul
xcopy "%R_SRC%\etc" "%OUT_DIR%\runtime\R\etc\" /E /I /H /Y >nul
xcopy "%R_SRC%\share" "%OUT_DIR%\runtime\R\share\" /E /I /H /Y >nul
xcopy "%R_SRC%\modules" "%OUT_DIR%\runtime\R\modules\" /E /I /H /Y >nul
if exist "assets" xcopy "assets" "%OUT_DIR%\assets\" /E /I /H /Y >nul
if exist "sample_data" xcopy "sample_data" "%OUT_DIR%\sample_data\" /E /I /H /Y >nul

echo [3/4] Copy required R packages...
for /f "usebackq delims=" %%p in ("required_r_packages.txt") do (
  if exist "%R_SRC%\library\%%p" (
    xcopy "%R_SRC%\library\%%p" "%OUT_DIR%\runtime\R\library\%%p\" /E /I /H /Y >nul
  )
)

for %%p in (base compiler datasets graphics grDevices grid methods parallel splines stats stats4 tcltk tools utils) do (
  if exist "%R_SRC%\library\%%p" (
    xcopy "%R_SRC%\library\%%p" "%OUT_DIR%\runtime\R\library\%%p\" /E /I /H /Y >nul
  )
)

(
  echo @echo off
  echo cd /d %%~dp0
  echo start "" ".\CAIScore_Desktop_App.exe"
) > "%OUT_DIR%\Run_CAIScore_App.bat"

echo [4/4] Create zip (bsdtar)...
if exist "%ZIP_PATH%" del /f /q "%ZIP_PATH%"
tar -a -c -f "%ZIP_PATH%" -C "release" "CAIScore_Desktop_Portable_Min"

echo Done.
echo Folder: %cd%\%OUT_DIR%
echo Zip   : %cd%\%ZIP_PATH%
