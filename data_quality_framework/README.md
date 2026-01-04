# 🛡️ Data Quality & Auto-Repair Framework

**A production-ready Python framework for automated data auditing and cleaning.**

Data cleaning typically consumes 80% of a Data Scientist's time. This project automates that "dirty work" by providing a modular pipeline to **audit** datasets for errors and **auto-repair** them based on configurable logic. It is designed to be the first step in any ML pipeline, ensuring garbage-in does not lead to garbage-out.

---

## 🚀 Key Features

### 1. 🔍 Automated Auditing (`src/audits.py`)
Diagnoses dataset health before you even touch it.
* **Missing Value Detection:** Flags columns with nulls.
* **Duplicate Scanning:** Identifies repeated rows.
* **Schema Validation:** Detects text in numeric columns (e.g., "1,000" or errors).
* **Cardinality Check:** Flags categorical columns with too many unique values (high dimensionality risk).

### 2. 🔧 Auto-Repair Engine (`src/repairs.py`)
Fixes the issues found during the audit.
* **Smart Imputation:** Fills missing values with Median (numeric) or Mode (categorical).
* **Text Normalization:** Standardizes inconsistent strings (e.g., converts `"  Electronics "` → `"electronics"`).
* **Outlier Capping:** Caps extreme values using Z-Score thresholds (default: 3 std dev).
* **Deduplication:** Automatically removes duplicate records.

### 3. 📊 Health Reporting (`src/reporter.py`)
* Generates a **JSON log** tracking the dataset's state "Before vs. After".
* Logs every action taken for full reproducibility.

---

## 📂 Project Structure

```text
data_quality_framework/
│
├── src/                        # Core Library Code
│   ├── audits.py               # Logic for detecting data issues
│   ├── repairs.py              # Logic for fixing data issues
│   └── reporter.py             # Generates JSON summaries
│
├── tests/                      # Unit Tests
│   └── test_repairs.py         # Verifies imputation and dedup logic
│
├── examples/                   # Demo Scripts
│   ├── generate_fake_data.py   # Creates a messy dataset for testing
│   └── demo_full_pipeline.py   # Runs the full Audit -> Repair -> Report flow
│
├── requirements.txt            # Python dependencies
└── README.md                   # Documentation
```

# 🛠️ Installation & Setup
### 1. Clone the repository
Bash
```text
git clone [https://github.com/rajatkkhairnar/The-Data-flower.git](https://github.com/rajatkkhairnar/The-Data-flower.git)
cd The-Data-flower/data_quality_framework
```
### 2. Install dependencies
It is recommended to use a virtual environment.

Bash
```
pip install -r requirements.txt
```
# ⚡ Usage Guide
### Step 1: Generate Dummy Data
First, we need some "dirty" data to test the tool. Run the generation script to create a raw CSV with intentional errors (nulls, duplicates, outliers).

Bash
```
python examples/generate_fake_data.py
Output: Created data/raw_data.csv
```
### Step 2: Run the Pipeline
### Execute the full cleaning workflow. This will audit the data, apply fixes, and save the clean version.

Bash
```
python examples/demo_full_pipeline.py
```
Output: Created data/clean_data.csv and data/quality_report.json

### Step 3: Check the Results
### You can view the audit report to see exactly what changed:

Bash
```
# On Windows
type data\quality_report.json

# On Mac/Linux
cat data/quality_report.json
```
