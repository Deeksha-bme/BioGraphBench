# BioGraphBench 🧬
### A Biomedical Graph Neural Network (GNN) Competition

BioGraphBench is a benchmark competition that applies Graph Neural Networks (GNNs)
to biomedical data such as patient similarity graphs, biological networks, and
molecular interaction graphs.

The benchmark is designed to fairly compare **human-designed** and
**LLM-assisted** models under identical rules and constraints.

---

## 📌 What is this competition about?

Biomedical data is not isolated.  
Patients, genes, or molecules are often related to each other.

This competition represents biomedical data as a **graph**:
- Nodes → patients (or biomedical entities)
- Edges → similarity or relationship between them
- Values → numerical biomedical features (example: ECG features)

Using this graph, participants predict outcomes using GNN models.

---

## 🧠 Learning Task

**Task Type:** Node Classification

- Each node represents a patient
- Each patient has numerical biomedical values
- The goal is to predict a label for each test patient

---

## 🔁 How the Competition Works (Step by Step)

### 1. Values (Data)
- Biomedical signals are converted into numerical values
- These values become **node features**

### 2. Graph Formation
- Each patient is a node
- Patients with similar patterns are connected by edges
- This forms a patient similarity graph

### 3. Model Training
- Participants download the public data
- They train GNN models on their own system
- Any GNN method is allowed

### 4. Prediction Submission
- Participants submit only a `predictions.csv` file
- No code is uploaded or executed

### 5. Evaluation
- Predictions are evaluated using hidden test labels
- Accuracy is calculated using a fixed evaluation script

### 6. Leaderboard
- Scores are automatically added to the leaderboard
- Higher accuracy gets a higher rank

---

## 📊 Dataset Structure

```text
data/public/
 ├── train_nodes.csv
 ├── val_nodes.csv
 └── test_nodes.csv
