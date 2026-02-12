BioGraphBench 🧬
A Biomedical Graph Neural Network (GNN) Benchmark Competition

BioGraphBench is a structured benchmark competition designed to evaluate Graph Neural Networks (GNNs) on biomedical relational data such as patient similarity graphs, biological networks, and molecular interaction systems.

The benchmark ensures a fair comparison between human-designed and LLM-assisted models under identical data, rules, and computational constraints.

📌 Competition Overview

Biomedical data is inherently relational.
Patients, genes, and molecules interact and influence one another rather than existing independently.

BioGraphBench models this relational structure as a graph:

Nodes → Patients (or biomedical entities)

Edges → Similarity or biological relationships

Node Features (Values) → Numerical biomedical measurements (e.g., ECG-derived features)

Participants must design GNN models to predict biomedical outcomes using this graph structure.

🧠 Learning Task

Task Type: Node Classification

Each node represents a patient

Each patient has numerical biomedical features

The objective is to predict a class label for each test node

🔁 Competition Workflow
1️⃣ Data Preparation

Biomedical signals are processed into structured numerical values forming the node feature matrix (X).

2️⃣ Graph Construction

Patients are represented as nodes

Similar patients are connected via similarity-based edges

This forms the patient similarity graph

3️⃣ Model Training

Participants download the public dataset

Any GNN architecture may be used

Both human-designed and LLM-assisted approaches are allowed

4️⃣ Prediction Submission

Participants submit prediction files for test nodes

Only predictions are uploaded (no training code required)

5️⃣ Evaluation

Predictions are evaluated using hidden test labels

A fixed evaluation script ensures fairness

6️⃣ Leaderboard

Scores are ranked automatically

Higher accuracy results in higher ranking

🔍 Benchmark Pipeline

Biomedical Data
→ Graph Construction
→ GNN Training
→ Predictions
→ Evaluation
→ Leaderboard

📊 Dataset Description

The dataset represents biomedical entities as a graph.

Nodes

Patients (or biomedical entities)

Node Features

Numerical biomedical values derived from signals (e.g., ECG features, clinical measurements)

Edges

Similarity-based relationships between patients

Data Splits

Training Set (labels available)

Validation Set (labels available)

Test Set (labels hidden)

Test labels are strictly used for automated evaluation only.

🧮 Graph Specification

Let:

A ∈ ℝ^(N×N) denote the adjacency matrix representing patient similarity

X ∈ ℝ^(N×F) denote the node feature matrix

Where:

N = number of patients (nodes)

F = number of biomedical features per patient

The graph may be sparse. Self-loops may optionally be added depending on the GNN architecture.

⚠️ Dataset Challenges

The dataset reflects real-world biomedical complexity:

Class imbalance between outcome categories

Noise in biomedical signal-derived features

Sparse graph connectivity

Potential distribution shift between train and test splits

These challenges encourage robust and generalizable modeling approaches.

📁 Dataset Structure
data/
 ├── public/
 │    ├── train_nodes.csv
 │    ├── val_nodes.csv
 │    └── test_nodes.csv
 ├── adjacency_matrix.csv
 └── feature_matrix.csv

🖥️ Computational Constraints

To ensure fairness:

Models must be trainable on a single standard GPU

Excessive compute-heavy architectures are discouraged

External private datasets are not allowed

📤 Submission Policy

Submit a CSV file containing:

node_id

predicted_label

No access to test labels is allowed

Submission format must strictly follow provided template

🤖 LLM Usage Policy

This benchmark explicitly allows:

Human-designed models

LLM-assisted model development

However:

LLMs may not access hidden test data

LLM-generated code must follow dataset and compute constraints

Evaluation fairness is strictly maintained

🎯 Evaluation Metric

Primary metric:

Accuracy

(Additional metrics such as F1-score may be reported depending on dataset characteristics.)

🏆 Objective

The goal of BioGraphBench is to:

Evaluate relational learning in biomedical contexts

Encourage reproducible graph-based modeling

Compare human and LLM-assisted approaches under standardized conditions

This benchmark is part of an academic competition series focused on Graph Deep Learning (GDL) in biomedical applications.
