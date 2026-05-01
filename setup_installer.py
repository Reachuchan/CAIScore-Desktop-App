import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
import zipfile
from pathlib import Path
from tkinter import messagebox, ttk


APP_NAME = "CAIScore Desktop App"
ZIP_NAME = "CAIScore_Desktop_Portable_Min_Fixed_v2.zip"


def resource_dir() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        exe_dir = Path(sys.executable).resolve().parent
        if (exe_dir / ZIP_NAME).exists():
            return exe_dir
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent / "release"


def hidden_run(args):
    startupinfo = None
    creationflags = 0
    if os.name == "nt":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    return subprocess.run(args, startupinfo=startupinfo, creationflags=creationflags, check=False)


class Installer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CAIScore Setup")
        self.geometry("520x250")
        self.resizable(False, False)
        self.configure(bg="#F2F5F7")
        self.install_dir = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "CAIScoreDesktop"
        self.zip_path = resource_dir() / ZIP_NAME
        self._build()

    def _build(self):
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="CAIScore Desktop App", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Install the local CAIScore clinical prediction app.").pack(anchor="w", pady=(6, 18))
        self.status = tk.StringVar(value="Ready to install.")
        ttk.Label(frame, textvariable=self.status).pack(anchor="w", pady=(0, 8))
        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=(0, 18))
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x")
        self.install_btn = ttk.Button(buttons, text="Install", command=self.install_async)
        self.install_btn.pack(side="right")
        ttk.Button(buttons, text="Cancel", command=self.destroy).pack(side="right", padx=(0, 8))

    def install_async(self):
        self.install_btn.configure(state="disabled")
        self.progress.start(12)
        threading.Thread(target=self.install, daemon=True).start()

    def install(self):
        try:
            if not self.zip_path.exists():
                raise FileNotFoundError(f"Missing bundled package: {self.zip_path}")
            self.status.set("Preparing install folder...")
            if self.install_dir.exists():
                shutil.rmtree(self.install_dir)
            self.install_dir.mkdir(parents=True, exist_ok=True)

            self.status.set("Extracting CAIScore runtime...")
            with zipfile.ZipFile(self.zip_path, "r") as zf:
                zf.extractall(self.install_dir)

            app_dir = self.install_dir / "CAIScore_Desktop_Portable_Min"
            exe_path = app_dir / "CAIScore_Desktop_App.exe"
            if not exe_path.exists():
                raise FileNotFoundError(f"Installed app missing: {exe_path}")

            self.status.set("Creating shortcuts...")
            desktop = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Desktop"
            start_menu = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            start_menu.mkdir(parents=True, exist_ok=True)
            self.create_shortcut(desktop / "CAIScore Desktop App.lnk", exe_path, app_dir)
            self.create_shortcut(start_menu / "CAIScore Desktop App.lnk", exe_path, app_dir)

            self.status.set("Starting CAIScore...")
            subprocess.Popen([str(exe_path)], cwd=str(app_dir))
            self.progress.stop()
            messagebox.showinfo("CAIScore Setup", "Installation completed.")
            self.destroy()
        except Exception as exc:
            self.progress.stop()
            self.install_btn.configure(state="normal")
            self.status.set("Installation failed.")
            messagebox.showerror("CAIScore Setup", str(exc))

    def create_shortcut(self, link_path: Path, exe_path: Path, work_dir: Path):
        ps = (
            "$s=(New-Object -ComObject WScript.Shell).CreateShortcut('{link}');"
            "$s.TargetPath='{target}';"
            "$s.WorkingDirectory='{work}';"
            "$s.IconLocation='{target},0';"
            "$s.Save()"
        ).format(
            link=str(link_path).replace("'", "''"),
            target=str(exe_path).replace("'", "''"),
            work=str(work_dir).replace("'", "''"),
        )
        hidden_run(["powershell", "-NoProfile", "-Command", ps])


if __name__ == "__main__":
    Installer().mainloop()
