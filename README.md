# BioGraphBench 🧬  
### A Biomedical Graph Neural Network (GNN) Benchmark Competition

BioGraphBench is a benchmark competition that applies **Graph Neural Networks (GNNs)**
to biomedical data such as **patient similarity graphs**, **biological networks**, and
**molecular interaction graphs**.

The benchmark is designed to fairly compare **human-designed** and
**LLM-assisted** models under **identical rules, data, and constraints**.

---

## 📌 What is this competition about?

Biomedical data is inherently **relational**.  
Patients, genes, or molecules are not isolated—they interact and influence each other.

This competition represents biomedical data as a **graph**:

- **Nodes** → Patients (or biomedical entities)
- **Edges** → Similarity or biological relationships
- **Values** → Numerical biomedical features (e.g., ECG-derived features)

Participants build GNN models on this graph to predict biomedical outcomes.

---

## 🧠 Learning Task

**Task Type:** Node Classification

- Each node represents a patient
- Each patient has numerical biomedical feature values
- The objective is to predict a label for each test patient

---

## 🔁 How the Competition Works

### 1. Data (Values)
- Biomedical signals are processed into numerical values
- These values form the **node feature matrix**

### 2. Graph Construction
- Each patient is represented as a node
- Similar patients are connected via edges
- This results in a **patient similarity graph**

### 3. Model Training
- Participants download the public dataset
- Models are trained locally using any GNN architecture
- Both human-designed and LLM-assisted approaches are allowed

### 4. Prediction Submission
- Participants submit predictions for test nodes
- Only prediction files are uploaded (no training code)

### 5. Evaluation
- Predictions are evaluated using hidden test labels
- Scores are computed using a fixed evaluation script

### 6. Leaderboard
- Scores are automatically added to the leaderboard
- Higher accuracy receives a higher rank

---

## 🔍 Benchmark Pipeline Overview

Biomedical Data  
→ Graph Construction  
→ GNN Training  
→ Predictions  
→ Evaluation  
→ Leaderboard

---

## 📊 Dataset

The dataset consists of biomedical entities represented as a graph.

- **Nodes:** Patients (or biomedical entities)
- **Node Features:** Numerical biomedical values derived from signals  
  (e.g., ECG-based features or clinical measurements)
- **Edges:** Similarity-based relationships between patients
- **Splits:** Train / Validation / Test

Training and validation labels are publicly available.  
Test labels are hidden and used only during automated evaluation.

### Dataset Structure

```text
data/public/
 ├── train_nodes.csv
 ├── val_nodes.csv
 └── test_nodes.csv
