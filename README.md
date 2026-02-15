<p align="center">
  <h1 align="center">BioGraphBench 🧬</h1>
  <p align="center"><b>A Biomedical Graph Neural Network (GNN) Benchmark Competition</b></p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-blue" />
  <img src="https://img.shields.io/badge/PyTorch-GNN-red" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

---

## 📌 Competition Overview

BioGraphBench is a structured benchmark designed to evaluate **Graph Neural Networks (GNNs)** on biomedical relational data such as patient similarity graphs and signal-derived feature networks.

The benchmark enables a fair comparison between:

- 🧠 Human-designed models  
- 🤖 LLM-assisted models  

under identical data, evaluation, and computational constraints.

---

## 🧠 Task Definition

**Task Type:** Node Classification  

Given:

- Adjacency matrix **A ∈ ℝ^(N×N)**
- Feature matrix **X ∈ ℝ^(N×F)**

Predict:

- Class label for each test node

Where:

- **N** = number of patients  
- **F** = number of biomedical features  

---

## 🔍 Benchmark Pipeline

Biomedical Signals  
→ Feature Extraction  
→ Graph Construction  
→ GNN Training  
→ Prediction  
→ Evaluation  
→ Leaderboard Ranking  

---

## 📊 Dataset

### Nodes
Patients represented as graph nodes.

### Features
Numerical biomedical measurements (e.g., ECG-derived features).

### Edges
Similarity-based relationships between patients.

### Splits
- Train (labels available)  
- Validation (labels available)  
- Test (labels hidden)  

---

## ⚠️ Dataset Challenges

- Class imbalance  
- Noisy signal-derived features  
- Sparse connectivity  
- Potential distribution shift  

---

## 📁 Dataset Structure
```text
data/
 ├── public/
 │    ├── train_nodes.csv
 │    ├── val_nodes.csv
 │    └── test_nodes.csv
 ├── adjacency_matrix.csv
 └── feature_matrix.csv
```
## 🖥️ Computational Constraints

- Models must train within reasonable time limits (≤ 3 hours on CPU).
- Only publicly provided dataset may be used.
- External private datasets are not allowed.
- Excessive compute-heavy architectures are discouraged.

---

## 📤 Submission Format

Participants must submit a CSV file in the following format:

```csv
node_id,predicted_label
1001,1
1002,0
1003,2

---
```
🔒 How to Submit (Encrypted)
To keep your results private, you must encrypt your submission.csv before sending a Pull Request.

Download the public_key.pem from this repo.

Run the following command to lock your file:

Bash
# Use our provided encryption tool
Python scripts/encrypt_submission.py submission.csv public_key.pem submissions/yourname.enc
Submit the .enc file via a Pull Request. Only our automated system can decrypt and score it!

```
```
## 📏 Evaluation Metric

**Primary Metric: Accuracy**

Accuracy = (Number of Correct Predictions) / (Total Test Samples)

Higher accuracy results in a higher ranking on the leaderboard.

Secondary metrics (optional reporting):
- F1-score
- Precision
- Recall

---

## 🏆 Baseline Model

A simple 2-layer Graph Convolutional Network (GCN) is provided as a reference baseline.

Architecture:
Input → GCN(64) → ReLU → GCN(num_classes)

Training Configuration:
- Optimizer: Adam
- Learning Rate: 0.01
- Epochs: 200

Baseline Validation Accuracy: **0.78**

---

## 📈 Example Results

| Model | Validation Accuracy | Test Accuracy |
|-------|--------------------|---------------|
| GCN | 0.78 | 0.76 |
| GraphSAGE | 0.81 | 0.79 |
| GAT | 0.84 | 0.82 |

*(Values shown are example benchmark results.)*

---

## 🏅 Leaderboard (Example)

| Rank | Team | Method | Test Accuracy |
|------|------|--------|--------------|
| 🥇 1 | Team Alpha | GAT | 0.86 |
| 🥈 2 | Team Beta | GraphSAGE | 0.83 |
| 🥉 3 | Team Gamma | GCN | 0.79 |

---

## 🤖 LLM Usage Policy

Allowed:
- LLM-assisted model development
- Code generation assistance

Not Allowed:
- Access to hidden test labels
- Leakage of evaluation data
- Use of external private biomedical datasets

---

## 🎯 Objective

BioGraphBench aims to:
- Advance graph-based biomedical modeling
- Encourage reproducible research
- Compare human vs LLM-assisted approaches
- Provide a standardized academic benchmark



