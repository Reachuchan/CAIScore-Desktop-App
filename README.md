# CAIScore Desktop & Web App

<div align="center">

**CAIScore 临床辅助评估软件 | CAIScore Clinical Prediction App**

[![Online Web App](https://img.shields.io/badge/Online_App-免安装在线版-E65100.svg?logo=googlechrome&logoColor=white)](https://caiscore.crq.de5.net/)
[![Release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest)
[![Windows](https://img.shields.io/badge/Windows-x64_Portable-0078D6.svg?logo=windows&logoColor=white)](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest)
[![macOS](https://img.shields.io/badge/macOS-Apple_Silicon_%26_Intel-000000.svg?logo=apple&logoColor=white)](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest)
[![Data Privacy](https://img.shields.io/badge/Data_Privacy-100%25_Offline-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br/>

**[ 🇨🇳 简体中文 ](#-简体中文)** &nbsp;|&nbsp; **[ 🇺🇸 English ](#-english)**

</div>

---

<br/>

# 🇨🇳 简体中文

## 🌟 在线免安装网页版（推荐所有用户直接使用）

针对**苹果电脑（Mac）、Windows、iPad 以及手机用户**，我们已部署了免安装的云端极速计算网页版：

👉 **[点击直接访问 CAIScore 在线网页版（https://caiscore.crq.de5.net/）](https://caiscore.crq.de5.net/)**

> [!TIP]
> **在线版优势（患者家属首选）**：
> - **零门槛秒开**：无需下载高达 1.0 GB 的离线大安装包，浏览器打开即可立即使用；
> - **跨全平台支持**：无论您使用的是苹果 Mac（M1/M2/M3/M4/Intel）、Windows 电脑还是移动设备，体验完全一致；
> - **全自动秒级计算**：直接上传表达谱矩阵，自动计算 CAIScore、免疫逃逸分级、1-5年生存概率并实时渲染生存曲线。

---

## 🎯 软件简介

**CAIScore** 是一款专为**肝细胞癌 (HCC)** 患者临床辅助评估设计的综合预测工具。

算法基于多算法集成框架（集成 AUCell、UCell、singscore、ssGSEA 与 Seurat AddModuleScore）计算肿瘤样本的综合基因集特征活性（CAIScore），并结合患者的年龄（Age）与临床 TNM 分期（Stage），通过严谨的 Cox 比例风险回归（CPH）列线图（Nomogram）模型，评估患者的**免疫逃逸潜能**以及 **1 至 5 年的总生存率（Overall Survival, OS）**。

---

## ⚡ 离线桌面端下载与使用指引

若您需要在完全无网络的机房或对患者病历隐私有严苛保密要求的环境下使用，请下载本地离线单包：

### 🪟 1. Windows 用户（64位绿色便携版）
1. **下载安装包**：👉 **[下载 CAIScore-v1.0.0-windows-x64.zip](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore-v1.0.0-windows-x64.zip)** *(约 1.0 GB)*
2. **解压文件**：下载后完整解压到电脑任意目录（例如 `D:\CAIScore\` 或桌面）；
3. **双击启动**：进入文件夹，直接双击 **`CAIScore.exe`** 即可打开主界面（无需额外安装 R 或 Python）。

### 🍎 2. macOS 苹果电脑用户（支持 Apple Silicon M系列与 Intel）
1. **下载安装包**：👉 **[下载 CAIScore-v1.0.0-macOS.zip](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore-v1.0.0-macOS.zip)**
2. **解压文件**：下载后双击解压出 `CAIScore-v1.0.0-macOS` 文件夹；
3. **启动方式（避开苹果 Gatekeeper 拦截）**：
   - **方式 A（最简推荐）**：双击运行文件夹内的 **`Start_CAIScore_Mac.command`**，脚本会自动清除苹果系统的隔离属性并直接调起程序；
   - **方式 B（手动打开）**：右键点击 **`CAIScore.app`** -> 选择【打开】(Open) -> 在弹出提示中再次点击【打开】（仅首次运行需确认一次）；
   - **方式 C（终端命令）**：若提示“应用已损坏”，打开终端执行：
     ```bash
     xattr -cr /path/to/CAIScore.app
     ```

---

## 🔬 核心功能与临床报告输出

| 评估指标 | 临床意义与说明 |
| :--- | :--- |
| **CAIScore** | 综合 5 大算法的归一化基因集活性评分 |
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
- **其余数值列**：对应的基因表达量数值（推荐 TPM、FPKM 或归一化 Count）。

### 输入格式示例：
```text
Gene	Sample_01	Sample_02	Sample_03
CD8A	12.45	8.32	15.61
GZMB	5.67	2.11	9.84
PRF1	8.90	4.56	11.23
```

> [!NOTE]
> 软件已内置标准测试文件 `test_expression.txt`。打开后点击界面上的 **【载入示例】（Load Sample）** 即可自动填充。

---

## ❓ 常见问题答疑（FAQ）

<details>
<summary><b>Q1: 优先推荐哪种使用方式？</b></summary>

**极力推荐使用【在线网页版】**（https://caiscore.crq.de5.net/）。无需下载 1GB 安装包，浏览器打开即用，计算速度与离线版完全一致，适合所有患者家属与医生。
</details>

<details>
<summary><b>Q2: 离线版数据会泄露吗？</b></summary>

**绝对不会！** 离线版被设计为 100% 纯本地离线单机运行，内部算法已锁定为纯内存串行计算，不连接任何外部网络端口，不上传任何个人或医疗隐私数据。
</details>

---
---

<br/>

# 🇺🇸 English

## 🌟 Online Web Application (Recommended for All Users)

For **macOS, Windows, iPad, and Mobile users**, a zero-install online cloud edition is live:

👉 **[Click to Access CAIScore Online Web App (https://caiscore.crq.de5.net/)](https://caiscore.crq.de5.net/)**

> [!TIP]
> **Key Highlights of the Web Edition**:
> - **Instant Access**: Zero download required (no need to download the 1.0 GB archive). Works instantly in modern browsers;
> - **Universal Compatibility**: Identical user experience across macOS (M1/M2/M3/M4/Intel), Windows, Linux, and tablets;
> - **Rapid Prognostic Forecasting**: Upload expression matrices to instantly obtain CAIScore, immune escape stratification, and 1- to 5-year OS estimates.

---

## 🎯 Overview

**CAIScore** is an ensemble prognostic framework for clinical assessment in **Hepatocellular Carcinoma (HCC)**.

Integrating five benchmark algorithms (**AUCell**, **UCell**, **singscore**, **ssGSEA**, and **AddModuleScore**), the tool quantifies composite gene signature activity (**CAIScore**). Together with patient Age and TNM Stage, it applies a trained Cox Proportional Hazards (CPH) Nomogram to project **Immune Escape Ability** and **1- to 5-year Overall Survival (OS)** rates.

---

## ⚡ Offline Desktop Downloads

For offline environments with strict medical confidentiality requirements:

### 🪟 1. Windows Users (64-bit Green Portable)
1. **Download Archive**: 👉 **[Download CAIScore-v1.0.0-windows-x64.zip](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore-v1.0.0-windows-x64.zip)** *(~1.0 GB)*
2. **Extract**: Unzip to any folder (e.g. `D:\CAIScore\` or your Desktop);
3. **Launch**: Double-click **`CAIScore.exe`** (no R or Python environment required).

### 🍎 2. macOS Users (Apple Silicon & Intel)
1. **Download Archive**: 👉 **[Download CAIScore-v1.0.0-macOS.zip](https://github.com/Reachuchan/CAIScore-Desktop-App/releases/latest/download/CAIScore-v1.0.0-macOS.zip)**
2. **Extract**: Unzip `CAIScore-v1.0.0-macOS.zip`;
3. **Launch (Bypassing macOS Gatekeeper)**:
   - **Method A (Recommended)**: Double-click **`Start_CAIScore_Mac.command`** in the extracted directory to automatically clear quarantine attributes and launch;
   - **Method B (Right-Click Open)**: Right-click **`CAIScore.app`** -> click **Open** -> click **Open** again in the prompt;
   - **Method C (Terminal)**: If macOS says the app is damaged:
     ```bash
     xattr -cr /path/to/CAIScore.app
     ```

---

## 🔬 Clinical Output Metrics

| Metric | Clinical Interpretation |
| :--- | :--- |
| **CAIScore** | Scaled composite activity score aggregated across 5 benchmark algorithms |
| **Total Points** | Nomogram score integrating CAIScore, patient Age, and TNM Stage |
| **Immune Escape Ability** | Stratified immune escape classification: **Low**, **Medium**, or **High** |
| **1- to 5-Year OS** | Predicted Overall Survival probabilities at 1, 2, 3, 4, and 5 years post-surgery |
| **Survival Trend Curve** | Dynamic survival curve visualization rendered directly in the dashboard |
| **One-Click Export** | Export complete tabular clinical assessment reports in `.csv` format |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
