import subprocess
import json
import numpy as np
import re
import os

# ================= CONFIG =================
PYTHON_EXE = "python"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTACK_SCRIPT = os.path.join(BASE_DIR, "generate_multiface_attack.py")
DETECT_SCRIPT = os.path.join(BASE_DIR, "embedding_detection.py")

SEEDS = [0, 1, 2, 3, 4]
OUTPUT_JSON = os.path.join("results", "multiseed_results.json")
# =========================================

os.makedirs("results", exist_ok=True)

results = []

print("===== MULTI-SEED EXPERIMENTS START =====")

for seed in SEEDS:
    print(f"\n>>> Running experiment with seed = {seed}")

    # ---------------- STEP 1: Generate attacks ----------------
    print("[1/2] Generating multi-face registration attacks...")
    subprocess.run(
        [PYTHON_EXE, ATTACK_SCRIPT, "--seed", str(seed)],
        check=True
    )

    # Load attack metadata
    meta_path = os.path.join(
        "data_processed", "attack_dataset", "attack_metadata.json"
    )
    with open(meta_path) as f:
        attack_meta = json.load(f)

    num_attack_ids = sum(
        1 for c in attack_meta["clients"] if c["type"] == "attack"
    )

    # ---------------- STEP 2: Run detection ----------------
    print("[2/2] Running embedding-based detection...")
    proc = subprocess.run(
        [PYTHON_EXE, DETECT_SCRIPT],
        capture_output=True,
        text=True,
        check=True
    )

    stdout = proc.stdout
    print(stdout)

    # ---------------- PARSE METRICS ----------------
    roc_auc = None
    tpr_1 = None
    tpr_01 = None

    for line in stdout.splitlines():
        if "ROC-AUC" in line:
            roc_auc = float(re.search(r"([0-9]*\.[0-9]+)", line).group(1))
        elif "TPR @ FPR = 1%" in line:
            tpr_1 = float(re.search(r"([0-9]*\.[0-9]+)", line).group(1))
        elif "TPR @ FPR = 0.1%" in line:
            tpr_01 = float(re.search(r"([0-9]*\.[0-9]+)", line).group(1))

    if roc_auc is None or tpr_1 is None:
        raise RuntimeError(f"Failed to parse metrics for seed {seed}")

    results.append({
        "seed": seed,
        "num_attack_identities": num_attack_ids,
        "roc_auc": roc_auc,
        "tpr_1pct": tpr_1,
        "tpr_0.1pct": tpr_01
    })

# ---------------- SAVE RESULTS ----------------
with open(OUTPUT_JSON, "w") as f:
    json.dump(results, f, indent=2)

# ---------------- SUMMARY ----------------
roc_vals = np.array([r["roc_auc"] for r in results])
tpr1_vals = np.array([r["tpr_1pct"] for r in results])

print("\n===== MULTI-SEED SUMMARY =====")
print(f"Seeds           : {SEEDS}")
print(f"ROC-AUC         : {roc_vals.mean():.3f} ± {roc_vals.std():.3f}")
print(f"TPR @ 1% FPR    : {tpr1_vals.mean():.3f} ± {tpr1_vals.std():.3f}")
print(f"Saved results → {OUTPUT_JSON}")

print("\n===== MULTI-SEED EXPERIMENTS COMPLETE =====")