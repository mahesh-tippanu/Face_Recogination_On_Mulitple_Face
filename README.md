Below is a **complete, clean, professional `README.md`** you can **copy-paste directly** into your GitHub repository and push.
It is written at **M.Tech + early PhD level**, reviewer-safe, and consistent with everything you’ve built and frozen.

---

# Mitigating Multi-Face Registration Attacks in Federated Face Recognition Systems

## Overview

Federated learning is increasingly adopted in face recognition systems to preserve user privacy by avoiding centralized storage of biometric data. While this paradigm improves privacy, it introduces **new security vulnerabilities** that are not present in centralized training. One critical and underexplored vulnerability is the **multi-face registration attack**, where multiple distinct individuals are maliciously registered under the same identity across different federated clients.

This project presents a **systematic experimental framework** to simulate, analyze, and detect such attacks using **embedding-level statistical anomaly detection**. The emphasis is on **identity integrity, reproducibility, and security evaluation**, rather than raw recognition accuracy alone.

---

## Key Contributions

* **Federated Face Recognition Simulation**
  Realistic non-IID federated client generation using large-scale face datasets.

* **Multi-Face Registration Attack Modeling**
  A custom attack dataset where multiple identities are injected under a single label across malicious clients.

* **Embedding-Based Attack Detection**
  Detection of compromised identities using intra-identity embedding dispersion and statistical anomaly scoring.

* **Scalable Evaluation**
  Experiments conducted across 10, 20, and 50 federated clients to study robustness and scalability.

* **Explainability-Aware Design (Conceptual)**
  Explainable AI (XAI) is incorporated at the design level to support interpretability and future extensions, while maintaining a stable and reproducible runtime pipeline.

---

## System Workflow

1. **Dataset Preparation**

   * Identity-wise organization of face images
   * Train / validation / test splits with no identity overlap

2. **Federated Client Simulation**

   * Non-IID identity distribution across clients
   * Configurable number of clients (10 / 20 / 50)

3. **Attack Generation**

   * Injection of multiple identities under a single label
   * Controlled number of malicious clients

4. **Feature Extraction**

   * Deep face embeddings extracted using a ResNet-based backbone

5. **Attack Detection**

   * Intra-identity embedding dispersion analysis
   * Z-score-based statistical anomaly detection

6. **Evaluation**

   * Detection metrics such as AUC and detection trends
   * Comparative analysis between benign and attacked identities

---

## Datasets Used

* **CelebA** – Large-scale face dataset for identity learning
* **LFW / AgeDB / CFP-FP** – Standard face verification benchmarks
* **Masked Face Datasets** – Robustness evaluation under occlusion
* **Custom Attack Dataset** – Generated multi-face registration attack samples

All datasets are used strictly for **academic research purposes**.

---

## Technologies

* **Programming Language:** Python
* **Deep Learning Framework:** PyTorch (CPU-only for reproducibility)
* **Libraries:** NumPy, scikit-learn, Matplotlib, Pillow
* **Environment:** Windows / Linux (CPU-only, no CUDA dependency)

---

## Repository Structure

```
Face_recognition_project/
│
├── data_processed/
│   ├── federated/              # Federated client splits
│   ├── attack_dataset/         # NormalPairs / AttackPairs
│
├── scripts/
│   ├── separate_celeba_identities.py
│   ├── split_train_val_test.py
│   ├── create_federated_clients.py
│   ├── generate_multiface_attack.py
│   ├── embedding_attack_detection.py
│
├── docs/
│   ├── methodology.md          # System design & XAI concepts
│
├── results/
│   ├── tables/
│   ├── plots/
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd Face_recognition_project
```

Install dependencies (CPU-only, stable):

```bash
pip install -r requirements.txt --index-url https://download.pytorch.org/whl/cpu
```

---

## Usage

### 1. Prepare Identities

```bash
python scripts/separate_celeba_identities.py
```

### 2. Create Train / Validation / Test Splits

```bash
python scripts/split_train_val_test.py
```

### 3. Generate Federated Clients

```bash
python scripts/create_federated_clients.py
```

### 4. Generate Multi-Face Registration Attacks

```bash
python scripts/generate_multiface_attack.py
```

### 5. Run Embedding-Based Attack Detection

```bash
python scripts/embedding_attack_detection.py
```

---

## Results

* Successfully detects identity corruption caused by multi-face registration attacks
* Demonstrates clear separation between benign and attacked identities
* Detection performance remains stable as the number of federated clients increases

Detailed results, plots, and tables are available in the `results/` directory.

---

## Reproducibility

* CPU-only environment for platform independence
* Fixed dataset splits and deterministic attack generation
* Frozen dependency versions (`requirements.txt`)

This ensures the experiments can be reproduced across systems.

---

## Research Significance

This work highlights a **realistic and under-addressed security vulnerability** in federated biometric systems. By focusing on **identity-level integrity** rather than classification accuracy, the project aligns closely with real-world deployment concerns in privacy-sensitive environments such as mobile authentication and edge AI systems.

The framework is designed to be **extensible** for future research, including explainable AI, federated defenses, and privacy leakage analysis.

---

## License & Disclaimer

This project is intended **solely for academic and research purposes**.
All datasets are subject to their original licenses and terms of use.

---

## Author

**Mahesh Kumar Tippanu**
M.Tech (Computer Science & Engineering)
GITAM University

