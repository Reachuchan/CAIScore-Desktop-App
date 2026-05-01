import csv
import os
import subprocess
import sys
import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import shutil


def detect_rscript(base_dir: Path):
    bundled = [
        base_dir / "runtime" / "R" / "bin" / "Rscript.exe",
        base_dir / "runtime" / "R" / "bin" / "x64" / "Rscript.exe",
    ]
    for p in bundled:
        if p.exists():
            return str(p)

    candidates = [
        r"D:\R\R-4.3.1\bin\Rscript.exe",
        r"D:\R\R-4.3.1\bin\x64\Rscript.exe",
        r"C:\Program Files\R\R-4.3.1\bin\Rscript.exe",
        r"C:\Program Files\R\R-4.3.1\bin\x64\Rscript.exe",
        "Rscript",
    ]
    for c in candidates:
        if c == "Rscript":
            return c
        if os.path.exists(c):
            return c
    return None


class CAIScoreApp:
    def __init__(self, root):
        self.root = root
        self.exe_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path.cwd()
        self.base_dir = Path(sys._MEIPASS) if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS") else Path(__file__).resolve().parent
        self.rows = []
        self.lang = "zh"
        self.rscript = detect_rscript(self.exe_dir)

        self.root.title("CAIScore Desktop App")
        self.root.geometry("1280x860")
        self.root.minsize(1100, 760)
        self.root.configure(bg="#EFF3F7")
        self._set_icon()
        self._init_style()
        self._build_ui()
        self._refresh_text()

    def _set_icon(self):
        ico_candidates = [
            self.exe_dir / "assets" / "liver_icon.ico",
            self.base_dir / "assets" / "liver_icon.ico",
        ]
        png_candidates = [
            self.exe_dir / "assets" / "liver_icon.png",
            self.base_dir / "assets" / "liver_icon.png",
        ]
        for p in ico_candidates:
            if p.exists():
                try:
                    self.root.iconbitmap(str(p))
                    return
                except Exception:
                    pass
        for p in png_candidates:
            if p.exists():
                try:
                    self._icon_photo = tk.PhotoImage(file=str(p))
                    self.root.iconphoto(True, self._icon_photo)
                    return
                except Exception:
                    pass

    def _init_style(self):
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        style.configure("Hero.TLabel", font=("Segoe UI", 21, "bold"), foreground="#642A2A")
        style.configure("Section.TLabelframe.Label", font=("Segoe UI", 12, "bold"), foreground="#6C2D2D")
        style.configure("Run.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TFrame", background="#FFFFFF")
        style.configure("Hint.TLabel", foreground="#5E6F7D")

    def t(self, zh, en):
        return zh if self.lang == "zh" else en

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=14, style="Card.TFrame")
        container.pack(fill="both", expand=True)

        head = ttk.Frame(container)
        head.pack(fill="x", pady=(0, 8))

        self.title_label = ttk.Label(head, style="Hero.TLabel")
        self.title_label.pack(side="left")
        self.lang_btn = ttk.Button(head, width=10, command=self.toggle_lang)
        self.lang_btn.pack(side="right")

        form = ttk.LabelFrame(container, style="Section.TLabelframe", padding=12)
        form.pack(fill="x")

        self.file_label = ttk.Label(form)
        self.file_label.grid(row=0, column=0, sticky="w")
        self.file_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.file_var, width=94).grid(row=1, column=0, columnspan=2, sticky="we", padx=(0, 8), pady=(4, 8))
        self.file_btn = ttk.Button(form, command=self.pick_file)
        self.file_btn.grid(row=1, column=2, padx=(0, 8), pady=(4, 8))

        self.sample_btn = ttk.Button(form, command=self.use_sample_file)
        self.sample_btn.grid(row=1, column=7, padx=(8, 0), pady=(4, 8))

        self.download_sample_btn = ttk.Button(form, command=self.download_sample_file)
        self.download_sample_btn.grid(row=1, column=8, padx=(8, 0), pady=(4, 8))

        self.age_label = ttk.Label(form)
        self.age_label.grid(row=0, column=3, padx=(10, 0), sticky="w")
        self.age_var = tk.StringVar(value="60")
        ttk.Entry(form, textvariable=self.age_var, width=8).grid(row=1, column=3, padx=(10, 8), pady=(4, 8), sticky="w")

        self.stage_label = ttk.Label(form)
        self.stage_label.grid(row=0, column=4, sticky="w")
        self.stage_var = tk.StringVar(value="Stage II")
        ttk.Combobox(form, state="readonly", textvariable=self.stage_var, values=["Stage I", "Stage II", "Stage III", "Stage IV"], width=12).grid(row=1, column=4, padx=(0, 8), pady=(4, 8), sticky="w")

        self.run_btn = ttk.Button(form, style="Run.TButton", command=self.run_predict)
        self.run_btn.grid(row=1, column=5, padx=(8, 8), pady=(4, 8))
        self.save_btn = ttk.Button(form, command=self.export_csv)
        self.save_btn.grid(row=1, column=6, pady=(4, 8))

        self.hint_label = ttk.Label(form, style="Hint.TLabel")
        self.hint_label.grid(row=2, column=0, columnspan=7, sticky="w")

        self.status_var = tk.StringVar(value="")
        ttk.Label(container, textvariable=self.status_var, foreground="#2E4F66").pack(anchor="w", pady=(6, 8))

        top_panel = ttk.Frame(container)
        top_panel.pack(fill="x", pady=(0, 10))

        basic_box = ttk.LabelFrame(top_panel, style="Section.TLabelframe", padding=10)
        basic_box.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.metric_tree = ttk.Treeview(basic_box, columns=["Metric", "Value"], show="headings", height=4)
        self.metric_tree.heading("Metric", text="Metric")
        self.metric_tree.heading("Value", text="Value")
        self.metric_tree.column("Metric", width=220, anchor="w")
        self.metric_tree.column("Value", width=140, anchor="center")
        self.metric_tree.pack(fill="both", expand=True)

        chart_box = ttk.LabelFrame(top_panel, style="Section.TLabelframe", padding=10)
        chart_box.pack(side="left", fill="both", expand=True)
        self.canvas = tk.Canvas(chart_box, bg="#F6F4F3", height=300, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_chart())

        result_box = ttk.LabelFrame(container, style="Section.TLabelframe", padding=10)
        result_box.pack(fill="both", expand=True)
        self.columns = [
            "SampleID", "CAIScore", "Age", "Stage", "Total_Points", "Immune_Escape_Ability",
            "OS_1_Year", "OS_2_Year", "OS_3_Year", "OS_4_Year", "OS_5_Year",
        ]
        self.tree = ttk.Treeview(result_box, columns=self.columns, show="headings")
        for c in self.columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=116, anchor="center")
        self.tree.column("SampleID", width=160, anchor="w")
        self.tree.column("Immune_Escape_Ability", width=150, anchor="center")
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.tree.grid(row=0, column=0, sticky="nsew")

        y_scroll = ttk.Scrollbar(result_box, orient="vertical", command=self.tree.yview)
        y_scroll.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=y_scroll.set)
        x_scroll = ttk.Scrollbar(result_box, orient="horizontal", command=self.tree.xview)
        x_scroll.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=x_scroll.set)
        result_box.columnconfigure(0, weight=1)
        result_box.rowconfigure(0, weight=1)

    def _refresh_text(self):
        self.title_label.config(text=self.t("CAIScore 肝癌临床预测软件", "CAIScore Clinical Prediction App"))
        self.lang_btn.config(text="English" if self.lang == "zh" else "中文")
        self.file_label.config(text=self.t("表达矩阵文件", "Expression Matrix File"))
        self.file_btn.config(text=self.t("选择文件", "Browse"))
        self.sample_btn.config(text=self.t("加载示例", "Load Sample"))
        self.download_sample_btn.config(text=self.t("下载示例", "Download Sample"))
        self.age_label.config(text=self.t("年龄", "Age"))
        self.stage_label.config(text=self.t("TNM Stage", "TNM Stage"))
        self.run_btn.config(text=self.t("Run", "Run"))
        self.save_btn.config(text=self.t("导出CSV", "Export CSV"))
        self.hint_label.config(
            text=self.t(
                "输入要求：行是基因名，列是样本名。第一列必须是基因名，后续列是样本表达值。",
                "Input requirement: rows are genes and columns are samples. First column must be gene names; remaining columns are sample expression values."
            )
        )
        self.status_var.set(self.t("就绪", "Ready"))

    def toggle_lang(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self._refresh_text()
        self.update_basic_info()
        self.draw_chart()

    def pick_file(self):
        path = filedialog.askopenfilename(
            title=self.t("选择表达矩阵", "Choose expression matrix"),
            filetypes=[("Text files", "*.txt *.tsv"), ("All files", "*.*")],
        )
        if path:
            self.file_var.set(path)

    def _find_sample_expr(self):
        candidates = [
            self.exe_dir / "sample_data" / "test_expression.txt",
            self.exe_dir / "caiscore_source" / "test_expression.txt",
            self.base_dir / "caiscore_source" / "test_expression.txt",
            Path(r"D:\文献+论文\生信\CAIScore\在线网站\test_expression.txt"),
        ]
        for p in candidates:
            if p.exists():
                return p
        return None

    def use_sample_file(self):
        p = self._find_sample_expr()
        if not p:
            messagebox.showerror(self.t("错误", "Error"), self.t("未找到示例表达矩阵。", "Sample expression matrix not found."))
            return
        self.file_var.set(str(p))
        self.status_var.set(self.t("已加载示例表达矩阵，可直接点击 Run。", "Sample matrix loaded. You can click Run now."))

    def download_sample_file(self):
        p = self._find_sample_expr()
        if not p:
            messagebox.showerror(self.t("错误", "Error"), self.t("未找到示例表达矩阵。", "Sample expression matrix not found."))
            return
        save_path = filedialog.asksaveasfilename(
            title=self.t("保存示例表达矩阵", "Save sample expression matrix"),
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="test_expression.txt",
        )
        if not save_path:
            return
        shutil.copyfile(str(p), save_path)
        self.status_var.set(self.t("示例表达矩阵已下载。", "Sample expression matrix downloaded."))
        messagebox.showinfo(self.t("完成", "Done"), self.t("示例表达矩阵已保存。", "Sample expression matrix saved."))

    def _run_cmd_hidden(self, cmd):
        startupinfo = None
        creationflags = 0
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            startupinfo=startupinfo,
            creationflags=creationflags,
        )

    def run_predict(self):
        expr_file = self.file_var.get().strip()
        if not expr_file or not os.path.exists(expr_file):
            messagebox.showerror(self.t("错误", "Error"), self.t("请选择有效表达矩阵文件。", "Please choose a valid expression matrix file."))
            return
        if not self.rscript:
            messagebox.showerror(self.t("错误", "Error"), self.t("未找到Rscript，无法运行算法。", "Rscript not found."))
            return
        try:
            age = float(self.age_var.get().strip())
        except Exception:
            messagebox.showerror(self.t("错误", "Error"), self.t("年龄必须为数字。", "Age must be numeric."))
            return
        stage = self.stage_var.get().strip()
        if stage not in {"Stage I", "Stage II", "Stage III", "Stage IV"}:
            messagebox.showerror(self.t("错误", "Error"), self.t("Stage 必须是 I/II/III/IV。", "Stage must be I/II/III/IV."))
            return

        script_path = self.base_dir / "caiscore_predict_cli.R"
        if not script_path.exists():
            messagebox.showerror(self.t("错误", "Error"), f"Missing script: {script_path}")
            return

        out_csv = Path(tempfile.gettempdir()) / "caiscore_last_result.csv"
        cmd = [self.rscript, str(script_path), str(self.base_dir), expr_file, str(age), stage, str(out_csv)]

        self.status_var.set(self.t("正在计算，请稍候...", "Calculating..."))
        self.root.update_idletasks()

        try:
            p = self._run_cmd_hidden(cmd)
            if p.returncode != 0:
                err = (p.stderr or p.stdout or "").strip()
                raise RuntimeError(err if err else "R process failed.")

            rows = []
            with open(out_csv, "r", encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if not r.get("Immune_Escape_Ability"):
                        r["Immune_Escape_Ability"] = self.classify_escape(float(r.get("Total_Points", 0) or 0))
                    rows.append(r)
            self.rows = rows
            self.render_results()
            self.status_var.set(self.t(f"预测完成：{len(rows)} 个样本", f"Done: {len(rows)} samples"))
        except Exception as e:
            self.status_var.set(self.t("预测失败", "Prediction failed"))
            messagebox.showerror(self.t("错误", "Error"), str(e))

    def classify_escape(self, points):
        if points < 80:
            return "Low"
        if points < 120:
            return "Medium"
        return "High"

    def render_results(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in self.rows:
            vals = [r.get(c, "") for c in self.columns]
            self.tree.insert("", "end", values=vals)
        if self.rows:
            first = self.tree.get_children()[0]
            self.tree.selection_set(first)
            self.tree.focus(first)
        self.update_basic_info()
        self.draw_chart()

    def selected_row(self):
        sel = self.tree.selection()
        if not sel:
            return self.rows[0] if self.rows else None
        vals = self.tree.item(sel[0], "values")
        if not vals:
            return None
        row = {}
        for i, c in enumerate(self.columns):
            row[c] = vals[i] if i < len(vals) else ""
        return row

    def update_basic_info(self):
        for i in self.metric_tree.get_children():
            self.metric_tree.delete(i)
        row = self.selected_row()
        if not row:
            return
        items = [
            ("CAIScore", row.get("CAIScore", "")),
            ("Total Points", row.get("Total_Points", "")),
            ("Immune Escape Ability", row.get("Immune_Escape_Ability", "")),
            ("Sample", row.get("SampleID", "")),
        ]
        for k, v in items:
            self.metric_tree.insert("", "end", values=(k, v))

    def on_row_select(self, _event=None):
        self.update_basic_info()
        self.draw_chart()

    def draw_chart(self):
        self.canvas.delete("all")
        row = self.selected_row()
        if not row:
            self.canvas.create_text(20, 20, anchor="nw", text=self.t("暂无结果", "No result"), fill="#7A2D2D", font=("Segoe UI", 12, "bold"))
            return

        try:
            ys = [
                float(row.get("OS_1_Year", 0)),
                float(row.get("OS_2_Year", 0)),
                float(row.get("OS_3_Year", 0)),
                float(row.get("OS_4_Year", 0)),
                float(row.get("OS_5_Year", 0)),
            ]
        except Exception:
            ys = [0, 0, 0, 0, 0]

        w = max(self.canvas.winfo_width(), 720)
        h = max(self.canvas.winfo_height(), 300)
        left, right, top, bottom = 70, w - 30, 38, h - 52

        self.canvas.create_text(w / 2, 18, text=self.t("Overall Survival Trend", "Overall Survival Trend"), fill="#4F1F1F", font=("Segoe UI", 16, "bold"))
        self.canvas.create_line(left, top, left, bottom, fill="#6C2D2D", width=2)
        self.canvas.create_line(left, bottom, right, bottom, fill="#6C2D2D", width=2)

        for i in range(0, 11, 2):
            yv = i / 10
            py = bottom - (bottom - top) * yv
            self.canvas.create_line(left, py, right, py, fill="#E1D7D2", dash=(4, 4))
            self.canvas.create_text(left - 28, py, text=f"{yv:.1f}", fill="#73403F", font=("Segoe UI", 9))

        years = ["1 Year", "2 Year", "3 Year", "4 Year", "5 Year"]
        xs = []
        for i in range(5):
            x = left + i * (right - left) / 4
            xs.append(x)
            self.canvas.create_text(x, bottom + 24, text=years[i], fill="#4F1F1F", font=("Segoe UI", 10, "bold"))

        points = []
        for x, y in zip(xs, ys):
            py = bottom - (bottom - top) * max(0.0, min(1.0, y))
            points.append((x, py))

        poly = [(xs[0], bottom)] + points + [(xs[-1], bottom)]
        self.canvas.create_polygon(poly, fill="#D8CCCC", outline="")

        for i in range(4):
            self.canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1], fill="#8B3A3A", width=3)
        for (x, y), val in zip(points, ys):
            self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="#9A3D3D", outline="")
            self.canvas.create_text(x, y - 16, text=f"{val * 100:.1f}%", fill="#6C2D2D", font=("Segoe UI", 11, "bold"))

        self.canvas.create_text(20, (top + bottom) / 2, text=self.t("生存概率", "Survival Probability"), angle=90, fill="#4F1F1F", font=("Segoe UI", 10, "bold"))
        self.canvas.create_text((left + right) / 2, h - 16, text=self.t("年份", "Years"), fill="#4F1F1F", font=("Segoe UI", 10, "bold"))

    def export_csv(self):
        if not self.rows:
            messagebox.showwarning(self.t("提示", "Notice"), self.t("请先运行预测。", "Run prediction first."))
            return
        path = filedialog.asksaveasfilename(
            title=self.t("导出结果", "Export result"),
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="CAIScore_prediction_result.csv",
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.columns)
            writer.writeheader()
            for r in self.rows:
                writer.writerow({k: r.get(k, "") for k in self.columns})
        messagebox.showinfo(self.t("完成", "Done"), self.t("导出成功。", "Exported."))


def main():
    root = tk.Tk()
    CAIScoreApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
