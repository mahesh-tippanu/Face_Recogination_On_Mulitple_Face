Here is a **GitHub-ready `README.md` with badges**, written to **look professional, serious, and research-grade** — not like a hobby repo.

You can paste this **as-is** into GitHub.

---

# 🔐 Detecting Multi-Face Registration Attacks in Federated Face Recognition Systems

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Research](https://img.shields.io/badge/type-Research%20Project-purple)
![Status](https://img.shields.io/badge/status-Completed-success)
![Privacy](https://img.shields.io/badge/privacy-preserving-important)

> **Unsupervised, identity-level detection of enrollment-time attacks in federated face recognition systems.**

---

## 📌 Overview

This repository contains the complete implementation of a **security-focused research project** that studies and detects a critical enrollment-time vulnerability in federated face recognition systems known as the **Multi-Face Registration Attack**.

In this attack, a malicious federated client registers facial images from **multiple distinct individuals under a single identity label**, compromising identity integrity while remaining invisible to standard recognition accuracy metrics.

We propose a **privacy-preserving, unsupervised detection framework** based on **identity-level embedding geometry**, without using supervised labels or accessing raw biometric data.

---

## 🎯 Key Contributions

* ✔ Formal definition of the **Multi-Face Registration Attack**
* ✔ Realistic **non-IID federated enrollment simulation**
* ✔ Custom **attack dataset generation pipeline**
* ✔ **Embedding-based identity integrity analysis**
* ✔ **Unsupervised anomaly detection** using max cosine distance
* ✔ Leakage-free, reproducible experimental pipeline

---

## 🧠 Core Insight

* Legitimate identities form **compact clusters** in embedding space
* Multi-face registrations introduce **outlier geometry**
* **Maximum cosine distance** reliably exposes identity compromise

This work shifts evaluation from **accuracy-centric metrics** to **identity integrity analysis**.

---

## 🏗️ Repository Structure

```
Face recogination project/
│
├── Celeba/
│   ├── identity_CelebA.txt
│   └── img_align_celeba/
│
├── data_processed/
│   ├── celeba_identities/
│   ├── splits/
│   ├── federated/
│   │   ├── clients_10/
│   │   ├── clients_20/
│   │   └── clients_50/
│   └── attack_dataset/
│       ├── NormalPairs/
│       ├── AttackPairs/
│       └── attack_metadata.json
│
├── results/
│   ├── roc_embedding_detection.pdf
│   └── score_distribution.pdf
│
├── separate_celeba_identities.py
├── split_train_val_test.py
├── create_federated_clients.py
├── generate_multiface_attack.py
├── embedding_detection.py
│
└── README.md
```

---

## 🔁 Correct Execution Flow (IMPORTANT)

Run scripts **strictly in the following order**:

### 1️⃣ Prepare identity-wise dataset *(run once)*

```bash
python separate_celeba_identities.py
```

### 2️⃣ Create identity-disjoint splits *(run once, lock forever)*

```bash
python split_train_val_test.py
```

### 3️⃣ Generate federated clients *(safe to rerun)*

```bash
python create_federated_clients.py
```

### 4️⃣ Simulate multi-face registration attacks *(safe to rerun)*

```bash
python generate_multiface_attack.py
```

### 5️⃣ Run detection and evaluation

```bash
python embedding_detection.py
```

⚠️ **Never regenerate identity splits mid-project** — this invalidates all experiments.

---

## 🧪 Detection Method

* **Embedding Model:** ResNet-50 (pretrained, fixed extractor)
* **Normalization:** L2 normalization
* **Anomaly Score:** Maximum cosine distance to identity centroid
* **Detection Type:** Unsupervised
* **Privacy:** No raw images shared or centralized

---

## 📊 Experimental Results

### Dataset Statistics

* Total identities evaluated: **10,866**
* Normal identities: **10,824**
* Attack identities: **42**

### Detection Performance

| Metric         | Value     |
| -------------- | --------- |
| ROC-AUC        | **0.988** |
| TPR @ 1% FPR   | **71.4%** |
| TPR @ 0.1% FPR | **26.2%** |

Clear separation is observed between normal and compromised identities in embedding space.

---

## 🔐 Threat Model

* Adversary controls one or more federated clients
* Attack occurs during **identity enrollment**
* No model poisoning or adversarial images
* Operates under realistic federated constraints

---

## 🚫 Non-Goals

This project intentionally does **not** include:

* ❌ Supervised classifier training
* ❌ Grad-CAM / LIME explanations
* ❌ Centralized biometric storage
* ❌ Assumption of trusted enrollment

---

## 🚀 Future Work

* Multi-seed stability analysis (mean ± std)
* Explainable AI for forensic evidence
* Live federated training integration
* Cross-dataset and cross-modal evaluation
* Adaptive adversarial strategies

---

## 📚 References

* McMahan et al., *Communication-Efficient Learning of Deep Networks from Decentralized Data*, AISTATS 2017
* Deng et al., *ArcFace*, CVPR 2019
* Liu et al., *CelebA Dataset*, ICCV 2015

---

## 👤 Author

**Mahesh Kumar Tippanu**
M.Tech – Computer Science and Engineering
GITAM University, Visakhapatnam
📧 [maheshkumartippanu@gmail.com](mailto:maheshkumartippanu@gmail.com)

---

## 🧾 License

This project is licensed under the **MIT License** — see the `LICENSE` file for details.
