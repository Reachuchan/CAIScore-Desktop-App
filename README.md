# CAIScore Desktop App

CAIScore Desktop App is a local Windows application for CAIScore-based clinical prediction in hepatocellular carcinoma.

## Download

Please download the installer from the GitHub Releases page:

- `CAIScore_Setup.exe`

After installation, launch **CAIScore Desktop App** from the desktop shortcut or Start Menu.

## Input Format

The expression matrix should use:

- Rows as gene names
- Columns as sample names
- The first column contains gene symbols
- The remaining columns contain expression values

A sample expression matrix is bundled in the app. Users can:

- Load it directly with **Load Sample**
- Save a local copy with **Download Sample**

## Outputs

The app reports:

- CAIScore
- Total Points
- Immune Escape Ability
- 1-5 year overall survival probabilities
- Overall survival trend plot

## Build

The build scripts are included for reproducibility:

- `build_caiscore_r_app_exe.bat`
- `build_caiscore_portable_min.bat`
- `build_setup_pyinstaller.bat`

The release installer includes a local R runtime and required R packages, so end users do not need to install R.
