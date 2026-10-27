# CAIScore Desktop App

<div align="center">

**CAIScore 桌面端临床辅助评估软件 | CAIScore Clinical Prediction Desktop App**

[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest)
[![Platform](https://img.shields.io/badge/Platform-Windows_x64-0078D6.svg?logo=windows)](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest)
[![Type](https://img.shields.io/badge/Type-Green_Portable-brightgreen.svg)]()
[![Privacy](https://img.shields.io/badge/Data_Privacy-100%25_Offline-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br/>

**[ 🇨🇳 简体中文 ](#-简体中文)** &nbsp;|&nbsp; **[ 🇺🇸 English ](#-english)**

</div>

---

<br/>

# 🇨🇳 简体中文

## 🎯 软件简介

**CAIScore Desktop App** 是一款专为**肝细胞癌 (HCC)** 设计的轻量级、完全离线的桌面端临床辅助评估工具。

软件基于多算法集成框架（集成 AUCell、UCell、singscore、ssGSEA 与 Seurat AddModuleScore）计算肿瘤样本的综合基因集特征活性（CAIScore），并结合患者的年龄（Age）与临床 TNM 分期（Stage），通过严谨的 Cox 比例风险回归（CPH）列线图（Nomogram）模型，预测患者的**免疫逃逸潜能**以及 **1 至 5 年的总生存率（Overall Survival, OS）**。

> [!TIP]
> **为临床与患者深度优化**：
> - **100% 绿色便携**：软件自带独立微型计算核心，用户电脑**完全无需安装任何 R 语言或 Python 环境**。
> - **零门槛解压即用**：类似日常绿色软件，下载单个压缩包解压后双击 `CAIScore.exe` 即可启动。
> - **数据绝对私密**：全流程纯本地离线计算，不上传任何患者病历或基因数据，充分保障医疗隐私。

---

## ⚡ 快速开始（推荐下载与使用）

### 第一步：下载最新绿色单包
请从官方 Releases 页面下载单个 ZIP 压缩包（约 1.0 GB，无任何分卷碎片）：

👉 **[点击直接下载 CAIScore-v1.0.0-windows-x64.zip](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore-v1.0.0-windows-x64.zip)**  
*(备用下载地址：[GitHub Releases 发布页](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest))*

### 第二步：解压到电脑
将下载的 `CAIScore-v1.0.0-windows-x64.zip` 解压到电脑任意文件夹（例如 `D:\CAIScore\` 或桌面）。

### 第三步：双击运行
打开解压后的文件夹，直接双击 **`CAIScore.exe`** 即可打开主界面！
*(文件夹内同时提供快捷启动脚本 `Run_CAIScore_App.bat`，效果一致)*

---

## 🔬 核心功能与临床报告输出

软件提供图形化、交互式的一站式操作体验：

| 评估指标 | 临床意义与说明 |
| :--- | :--- |
| **CAIScore** | 综合 AUCell、UCell、singscore、ssGSEA、AddModuleScore 五大算法的归一化基因集活性评分 |
| **Total Points** | 列线图（Nomogram）临床综合评分，整合了 CAIScore、患者年龄与 TNM 分期 |
| **Immune Escape Ability** | 免疫逃逸能力三级分层：**低（Low）** / **中（Medium）** / **高（High）** |
| **1~5 年 OS 概率** | 分别预测患者术后 1 年、2 年、3 年、4 年、5 年的总生存概率（Overall Survival） |
| **生存概率动态曲线** | 界面直观绘制 1-5 年患者生存趋势曲线图表 |
| **报告一键导出** | 支持一键导出标准 `.csv` 表格报告，便于与临床主治医生交流与病历留存 |

---

## 📊 表达矩阵输入格式规范

用户上传的基因表达谱文件（支持制表符分隔的 `.txt` 或逗号分隔的 `.csv`）需满足标准转录组矩阵格式：

- **第一行（表头）**：第一列为基因名称标识（如 `Gene`、`Symbol`），后续各列为样本唯一编号（如 `Sample_01`, `GSM362960`）。
- **第一列**：必须为官方标准人类 Gene Symbol（例如 `CD8A`, `GZMB`, `PRF1`, `TP53`）。
- **其余数值列**：对应的基因表达量数值（推荐 TPM、FPKM 或归一化 Count）。若存在同名基因，软件将自动进行标准化合并。

### 输入格式示例：
```text
Gene	Sample_01	Sample_02	Sample_03
CD8A	12.45	8.32	15.61
GZMB	5.67	2.11	9.84
PRF1	8.90	4.56	11.23
```

> [!NOTE]
> 软件 `sample_data/` 目录中已内置标准测试文件 `test_expression.txt`。打开软件后，直接点击界面上的 **【载入示例】（Load Sample）** 即可自动填充，随后点击 **【运行】（Run）** 体验完整流程。

---

## ❓ 常见问题答疑（患者及家属必读）

<details>
<summary><b>Q1: 我的电脑从没装过 R 语言或编程软件，能用吗？</b></summary>

**完全可以！** 软件采用自包含微型运行时（Embedded Runtime），解压出来的文件夹内部已经带有专用的数学与生物计算核心。用户电脑**不需要、也千万不要额外安装任何 R 或 Python**，解压双击即可用。
</details>

<details>
<summary><b>Q2: 初次打开提示“Windows 已保护你的电脑”怎么办？</b></summary>

由于本工具为开源学术与医学公益项目，未向商业机构付费购买高昂的微软企业数字签名证书，Windows SmartScreen 可能会进行常规安全提示：
> **解决方法**：点击提示窗口中的 **【更多信息】（More info）** ➔ 点击 **【仍要运行】（Run anyway）** 即可。仅首次运行需要确认一次。
</details>

<details>
<summary><b>Q3: 上传的患者基因数据会被联网泄露吗？</b></summary>

**绝对不会！** 软件被设计为 100% 纯本地离线单机运行，内部算法已锁定为纯内存计算，不连接任何外部网络端口，不收集、不上传任何个人或医疗隐私数据。
</details>

---

## 💻 进阶用法：命令行与原生 R 脚本调用

针对生信工程师与科研人员，本软件包同样支持在无界面环境下批处理调用：

### 1. 命令行 CLI 调用（使用内置免安装 Rscript）
```powershell
.\runtime\R\bin\x64\Rscript.exe caiscore_predict_cli.R . .\sample_data\test_expression.txt 60 "Stage II" .\output_result.csv
```

### 2. 原生 R 脚本调用逻辑
```R
library(CAIScore)
library(rms)
library(survival)

# 1. 载入核心模型与特征参考基准
reference_mat <- readRDS("reference_matrix.rds")
target_genes  <- readRDS("target_genes_list.rds")
model_cph     <- readRDS("final_model_cph.rds")
saved_ddist   <- readRDS("final_datadist.rds")
options(datadist = "saved_ddist")

# 2. 读取用户表达谱矩阵（首列为 Gene Symbol，后续为样本量）
raw_expr <- read.table("test_expression.txt", header = TRUE, sep = "\t", check.names = FALSE)
gene_names <- raw_expr[, 1]
expr_data <- raw_expr[, -1, drop = FALSE]
rownames(expr_data) <- gene_names

# 3. 执行五算法集成评分
common_genes <- intersect(rownames(reference_mat), rownames(expr_data))
combined_mat <- cbind(reference_mat[common_genes, ], expr_data[common_genes, , drop = FALSE])

scores <- CAIScore(
  expr = combined_mat,
  geneset = target_genes,
  scaling = "minmax",
  summary_method = "sum",
  auc_nCores = 1,
  kcdf_type = "Gaussian",
  AMS_nbin = 10
)

# 4. 提取样本结果并结合 CPH 列线图进行 OS 生存概率预测
user_scores <- scores[colnames(expr_data), , drop = FALSE]
```

---
---

<br/>

# 🇺🇸 English

## 🎯 Overview

**CAIScore Desktop App** is a lightweight, zero-dependency, and 100% offline Windows desktop application designed for clinical prognostic prediction in **Hepatocellular Carcinoma (HCC)**.

By leveraging an ensemble scoring framework that integrates five complementary algorithms (**AUCell**, **UCell**, **singscore**, **ssGSEA**, and **AddModuleScore**), the tool quantifies composite gene set activity (**CAIScore**). It then projects patient Age, TNM Stage, and CAIScore onto a trained Cox Proportional Hazards (CPH) Nomogram to assess **Immune Escape Ability** and forecast **1- to 5-year Overall Survival (OS)** rates.

> [!TIP]
> **Key Highlights for Clinicians, Patients & Researchers**:
> - **Standalone & Portable**: Self-contained with an embedded lightweight R runtime. **No external R or Python installation is required**.
> - **Zero-Config Quick Start**: Download the single zip archive, extract it anywhere, and double-click `CAIScore.exe`.
> - **100% Local & Private**: All statistical and bioinformatic calculations take place strictly on your local machine with zero network transmission.

---

## ⚡ Quick Start (Download & Usage)

### Step 1: Download Single Archive
Download the standalone ZIP package (~1.0 GB, single package, no split multi-part archives):

👉 **[Download CAIScore-v1.0.0-windows-x64.zip](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore-v1.0.0-windows-x64.zip)**  
*(Alternative link: [GitHub Releases Page](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest))*

### Step 2: Extract to Any Folder
Extract the downloaded `CAIScore-v1.0.0-windows-x64.zip` to any folder on your computer (e.g., `D:\CAIScore\` or your Desktop).

### Step 3: Launch
Open the extracted directory and double-click **`CAIScore.exe`** to launch the GUI.  
*(A companion launcher `Run_CAIScore_App.bat` is also provided).*

---

## 🔬 Clinical Output Metrics

The graphical interface provides instant prognostic assessment upon calculation:

| Metric | Clinical Interpretation |
| :--- | :--- |
| **CAIScore** | Scaled composite activity score aggregated across AUCell, UCell, singscore, ssGSEA, and AddModuleScore |
| **Total Points** | Nomogram score integrating CAIScore, patient Age, and TNM Stage |
| **Immune Escape Ability** | Stratified immune escape classification: **Low**, **Medium**, or **High** |
| **1- to 5-Year OS** | Predicted Overall Survival probabilities at 1, 2, 3, 4, and 5 years post-surgery |
| **Survival Trend Curve** | Dynamic survival curve visualization rendered directly in the dashboard |
| **One-Click Export** | Export complete tabular clinical assessment reports in `.csv` format |

---

## 📊 Input Matrix Formatting

The user-supplied expression file (`.txt` tab-delimited or `.csv`) must follow standard bulk or single-cell transcriptome matrix conventions:

- **Row Names**: Genes (one gene per row).
- **Column Names**: Samples (one sample per column).
- **First Column**: Official human Gene Symbols (e.g., `CD8A`, `GZMB`, `PRF1`, `TP53`).
- **Remaining Columns**: Numerical expression measurements (TPM, FPKM, or normalized counts).

### Example Input Matrix:
```text
Gene	Sample_01	Sample_02	Sample_03
CD8A	12.45	8.32	15.61
GZMB	5.67	2.11	9.84
PRF1	8.90	4.56	11.23
```

> [!NOTE]
> A sample matrix `test_expression.txt` is bundled under `sample_data/`. Click **Load Sample** in the application to immediately test the full pipeline.

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>Q1: Does the computer require R or Python to be pre-installed?</b></summary>

**No.** The package is completely portable and includes its own dedicated embedded runtime. It operates independently on clean Windows installations without requiring any pre-existing programming software or environmental configurations.
</details>

<details>
<summary><b>Q2: How to bypass "Windows protected your PC" (SmartScreen)?</b></summary>

Because this academic utility is distributed as open-source without an enterprise code-signing certificate:
> Simply click **More info** ➔ **Run anyway**. This prompt only occurs on the first run.
</details>

<details>
<summary><b>Q3: Is patient data kept private?</b></summary>

**Yes, 100%.** Calculations are strictly confined to internal local memory. The application creates no external network sockets and transmits zero data outside your device.
</details>

---

## 💻 Advanced: CLI & Native R Usage

Bioinformaticians and researchers can also execute calculations non-interactively:

### 1. Command-Line CLI Execution
```powershell
.\runtime\R\bin\x64\Rscript.exe caiscore_predict_cli.R . .\sample_data\test_expression.txt 60 "Stage II" .\output_result.csv
```

### 2. Native R Script Implementation
```R
library(CAIScore)
library(rms)
library(survival)

# 1. Load trained models and baseline gene signatures
reference_mat <- readRDS("reference_matrix.rds")
target_genes  <- readRDS("target_genes_list.rds")
model_cph     <- readRDS("final_model_cph.rds")
saved_ddist   <- readRDS("final_datadist.rds")
options(datadist = "saved_ddist")

# 2. Read expression matrix
raw_expr <- read.table("test_expression.txt", header = TRUE, sep = "\t", check.names = FALSE)
gene_names <- raw_expr[, 1]
expr_data <- raw_expr[, -1, drop = FALSE]
rownames(expr_data) <- gene_names

# 3. Compute ensemble CAIScore
common_genes <- intersect(rownames(reference_mat), rownames(expr_data))
combined_mat <- cbind(reference_mat[common_genes, ], expr_data[common_genes, , drop = FALSE])

scores <- CAIScore(
  expr = combined_mat,
  geneset = target_genes,
  scaling = "minmax",
  summary_method = "sum",
  auc_nCores = 1,
  kcdf_type = "Gaussian",
  AMS_nbin = 10
)

# 4. Extract scores and project onto CPH nomogram for 1-5y survival rates
user_scores <- scores[colnames(expr_data), , drop = FALSE]
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
