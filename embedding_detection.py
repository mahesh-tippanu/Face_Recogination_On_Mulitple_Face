import os
import numpy as np
from PIL import Image
from sklearn.metrics import roc_curve, auc
import torch
from torchvision import models, transforms
import matplotlib.pyplot as plt

# ================= CONFIG =================
PROJECT_ROOT = r"D:\Face recogination project"
BASE_DIR = os.path.join(PROJECT_ROOT, "data_processed")

ATTACK_DIR = os.path.join(BASE_DIR, "attack_dataset", "AttackPairs")
NORMAL_DIR = os.path.join(BASE_DIR, "attack_dataset", "NormalPairs")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "results")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----- ABLATION SWITCH -----
SCORE_MODE = "max"   # "max" (ours) or "mean"
# ==========================

# ---------------- DEVICE ----------------
device = "cpu"

# ---------------- MODEL ----------------
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.fc = torch.nn.Identity()
model.eval().to(device)

# ---------------- TRANSFORM ----------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ---------------- EMBEDDING FUNCTION ----------------
@torch.no_grad()
def get_embedding(img_path):
    img = Image.open(img_path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    emb = model(x).squeeze().cpu().numpy()
    return emb / np.linalg.norm(emb)

# ---------------- IDENTITY SCORE ----------------
def compute_identity_score(identity_dir):
    imgs = [
        os.path.join(identity_dir, f)
        for f in os.listdir(identity_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    if len(imgs) < 2:
        return None

    embeddings = []
    for img in imgs:
        try:
            embeddings.append(get_embedding(img))
        except Exception:
            continue

    if len(embeddings) < 2:
        return None

    embeddings = np.vstack(embeddings)

    center = embeddings.mean(axis=0)
    center = center / np.linalg.norm(center)

    distances = 1.0 - np.dot(embeddings, center)

    if SCORE_MODE == "mean":
        return distances.mean()

    # default: max
    return distances.max()

# ---------------- COLLECT SAMPLES ----------------
y_true, y_score = [], []

# ---- NORMAL ----
for client in os.listdir(NORMAL_DIR):
    client_path = os.path.join(NORMAL_DIR, client)
    if not os.path.isdir(client_path):
        continue

    for identity in os.listdir(client_path):
        id_path = os.path.join(client_path, identity)
        if not os.path.isdir(id_path):
            continue

        score = compute_identity_score(id_path)
        if score is not None:
            y_true.append(0)
            y_score.append(score)

# ---- ATTACK ----
for client in os.listdir(ATTACK_DIR):
    client_path = os.path.join(ATTACK_DIR, client)
    if not os.path.isdir(client_path):
        continue

    for identity in os.listdir(client_path):
        id_path = os.path.join(client_path, identity)
        if not os.path.isdir(id_path):
            continue

        score = compute_identity_score(id_path)
        if score is not None:
            y_true.append(1)
            y_score.append(score)

# ---------------- SANITY CHECK ----------------
y_true = np.array(y_true)
y_score = np.array(y_score)

print(f"[INFO] Total samples : {len(y_true)}")
print(f"[INFO] Attack samples: {(y_true == 1).sum()}")
print(f"[INFO] Normal samples: {(y_true == 0).sum()}")

if len(np.unique(y_true)) < 2:
    raise RuntimeError("ROC cannot be computed: only one class present.")

# ---------------- ROC + AUC ----------------
fpr, tpr, _ = roc_curve(y_true, y_score)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(6, 6), dpi=300)
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}", linewidth=2)
plt.plot([0, 1], [0, 1], "k--", linewidth=1)
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title(f"ROC ({SCORE_MODE} cosine distance)")
plt.legend(loc="lower right")
plt.grid(True)

roc_path = os.path.join(OUTPUT_DIR, "roc_embedding_detection.pdf")
plt.savefig(roc_path, bbox_inches="tight")
plt.close()

# ---------------- METRICS ----------------
def tpr_at_fpr(target_fpr):
    idx = np.where(fpr <= target_fpr)[0]
    return tpr[idx[-1]] if len(idx) else 0.0

print("\n========== RESULTS ==========")
print(f"SCORE_MODE        : {SCORE_MODE}")
print(f"ROC-AUC          : {roc_auc:.4f}")
print(f"TPR @ FPR = 1%   : {tpr_at_fpr(0.01):.4f}")
print(f"TPR @ FPR = 0.1% : {tpr_at_fpr(0.001):.4f}")
print(f"ROC curve saved  : {roc_path}")

# ================= SCORE DISTRIBUTION =================
normal_scores = y_score[y_true == 0]
attack_scores = y_score[y_true == 1]

plt.figure(figsize=(7, 5), dpi=300)

plt.hist(normal_scores, bins=50, density=True, alpha=0.6, label="Normal")
plt.hist(attack_scores, bins=50, density=True, alpha=0.7, label="Attack")

plt.xlabel("Anomaly Score (Cosine Distance)")
plt.ylabel("Density")
plt.title(f"Score Distribution ({SCORE_MODE} cosine distance)")
plt.legend()
plt.grid(True)

score_plot_path = os.path.join(OUTPUT_DIR, "score_distribution.pdf")
plt.savefig(score_plot_path, bbox_inches="tight")
plt.close()

print(f"Score distribution plot saved to: {score_plot_path}")