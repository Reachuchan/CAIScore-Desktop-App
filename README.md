# CAIScore Desktop App

CAIScore Desktop App is a local Windows application for CAIScore-based clinical prediction in hepatocellular carcinoma.

## Quick Download

For most users, start here:

- [One-click download and install](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore_OneClick_Install.bat)
- [Release page](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest)

How to use:

1. Click `CAIScore_OneClick_Install.bat` to download it.
2. Double-click the downloaded file.
3. The script will automatically download the required package files and start the installer.
4. After installation, open **CAIScore Desktop App** from the desktop shortcut or Start Menu.

If Windows shows a security prompt, choose `More info` and then `Run anyway`.

## What The Software Does

The app reports:

- CAIScore
- Total Points
- Immune Escape Ability
- 1-5 year overall survival probabilities
- Overall survival trend plot

## Input Format

The expression matrix should use:

- Rows as gene names
- Columns as sample names
- The first column contains gene symbols
- The remaining columns contain expression values

A sample expression matrix is bundled in the app. Users can:

- Load it directly with `Load Sample`
- Save a local copy with `Download Sample`

## Manual Download

If the one-click installer is blocked by local policy, open the [latest release page](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest) and download:

- `CAIScore_Setup.exe`
- `Install_CAIScore_From_Parts.ps1`
- `CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part001`
- `CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part002`
- `CAIScore_Desktop_Portable_Min_Fixed_v2.zip.part003`

Put them in the same folder, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\Install_CAIScore_From_Parts.ps1
```

## Build

The build scripts are included for reproducibility:

- `build_caiscore_r_app_exe.bat`
- `build_caiscore_portable_min.bat`
- `build_setup_pyinstaller.bat`

The release installer includes a local R runtime and required R packages, so end users do not need to install R.
