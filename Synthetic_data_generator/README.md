# 🧬 Synthetic Data Generator (CTGAN)

**A Deep Learning based engine for generating realistic tabular data.**

This project uses **CTGAN (Conditional Tabular GAN)** to learn the statistical distribution of a source dataset and generate unlimited synthetic rows. It is used to solve **Class Imbalance** (upsampling rare events) and **Data Privacy** (sharing data without sharing real user info).

## 🚀 Key Features
* **CTGAN Architecture:** Uses Generative Adversarial Networks optimized for tabular data.
* **Conditional Sampling:** Can force the model to generate specific rare events (e.g., "Generate 1,000 fraud cases").
* **Automated Evaluation:** Includes a statistical report comparing Real vs. Synthetic distributions (KS-Test).

## 📂 Structure
* `src/trainer.py`: Trains the model on `data/source_data.csv`.
* `src/generator.py`: Loads the model and generates new data.
* `src/evaluator.py`: Scores the quality of the synthetic data (0-100%).

## ⚡ Usage

### 1. Train the Model
Bash
```
python src/trainer.py
```

### 2. Generate Data
Bash
```
python src/generator.py
```
Modify generator.py to change the number of rows or target specific conditions.

### 3. Evaluate Quality
Bash
```
python src/evaluator.py

