<p align="center">
  <h1 align="center">BioGraphBench 🧬</h1>
  <p align="center"><b>A Privacy-Preserving GNN Benchmark for Biomedical Relational Data</b></p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9-blue" />
  <img src="https://img.shields.io/badge/PyTorch-GNN-red" />
  <img src="https://img.shields.io/badge/Framework-DGL-orange" />
  <img src="https://img.shields.io/badge/Privacy-RSA--Encrypted-green" />
</p>

---

## 📌 Competition Overview
**BioGraphBench** is a structured benchmark designed to evaluate **Graph Neural Networks (GNNs)** on biomedical relational data. In healthcare AI, data privacy is a critical bottleneck; this project introduces a **Privacy-Preserving Evaluation Pipeline** using RSA-2048 encryption to protect patient prediction data.

The benchmark enables a fair comparison between:
- 🧠 **Human-designed models** (DGL/PyTorch implementations)
- 🤖 **LLM-assisted models** (GPT/Claude generated architectures)

---

## 🏆 Current Standings
| Rank | Team | Score | Method | Status |
| :--- | :--- | :--- | :--- | :--- |
| 🥇 1 | **winner_final** | **0.2500** | GNN_V1 | Verified Baseline |

[👉 View the Full Dynamic Leaderboard here](./leaderboard.md)

---

## 🧠 Task Definition: Node Classification
**Objective:** Predict the clinical category for each test node (patient) based on their feature set and neighborhood context.



**Mathematical Framework:**
- **Adjacency Matrix $A \in \mathbb{R}^{N \times N}$:** Encodes similarity-based relationships.
- **Feature Matrix $X \in \mathbb{R}^{N \times F}$:** Numerical measurements (e.g., ECG-derived features).

---

## 🔬 Experimental Protocol (Pilot Phase)
To ensure the mathematical integrity of the **Asymmetric Encryption Layer** and the **DGL message-passing logic**, this benchmark currently utilizes a **Curated Verification Set ($N=4$)**. 

### Why this scale?
1. **Security Audit:** Validates the end-to-end flow from `encrypt_submission.py` to the automated scoring engine. 
2. **System Baseline:** The current score of **0.2500** serves as the verified baseline, confirming that the decryption-to-scoring pipeline is fully operational.
3. **Computational Constraints:** Ensures models can be trained within the $\le$ 3-hour CPU limit while maintaining reproducibility.

---

## 🔍 Benchmark Pipeline
Biomedical Signals → Feature Extraction → **Graph Construction (DGL)** → GNN Training → **RSA Encryption** → Evaluation → Leaderboard Ranking

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
## 🔒 How to Submit (Encrypted)
To maintain the integrity of the benchmark, all participants must encrypt their results before submission.

1. **Download:** Get `public_key.pem` from this repository.
2. **Encrypt:** Use the provided Python utility:

```bash
pythocripts/encrypt_submission.py submission.csv public_key.pem submissions/yourname.enc
```
3. **Submit**: Open a Pull Request with your .enc file. The CI/CD pipeline will decrypt and score it automatically.
## 📏 Evaluation Metric

* **Primary Metric:** Accuracy $= \frac{\text{Correct Predictions}}{\text{Total Test Samples}}$
* **Secondary Metrics:** F1-score, Precision, Recall.

  

---

## 🏆 Baseline Model

A reference **2-layer Graph Convolutional Network (GCN)** built in **DGL** is provided.

* **Architecture:** `Input` → `GCN(64)` → `ReLU` → `GCN(num_classes)`
* **Validation Accuracy:** 0.78

  

---

## 📚 References & Resources

* **DGL (Deep Graph Library):** Framework for message-passing and graph data handling. [DGL.ai](https://www.dgl.ai/)
* **BASIRA Lab (Imperial College London):** Aligned with affordable and inclusive AI research. [Lab Link](https://basira-lab.com/)
* **NeurIPS Benchmarks:** Inspired by the Datasets and Benchmarks Track at the NeurIPS Conference.

---

## 🎯 Research Objective

**BioGraphBench** aims to advance graph-based biomedical modeling by providing a standardized, reproducible, and secure framework for the next generation of Graph AI researchers. Developed as part of the **Imperial College London (BASIRA Lab) Rising Star Program**.
