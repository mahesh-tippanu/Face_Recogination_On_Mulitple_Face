import os
import random

# ================= CONFIG =================
DATA_DIR = r"D:\Face recogination project\data_processed\celeba_identities"
OUTPUT_DIR = r"D:\Face recogination project\data_processed\splits"

TRAIN_RATIO = 0.70
VAL_RATIO   = 0.15
TEST_RATIO  = 0.15

# 🔒 Fixed seed — splits created ONCE and reused
RANDOM_SEED = 42
# ========================================

assert abs(TRAIN_RATIO + VAL_RATIO + TEST_RATIO - 1.0) < 1e-6

os.makedirs(OUTPUT_DIR, exist_ok=True)

train_file = os.path.join(OUTPUT_DIR, "train_ids.txt")
val_file   = os.path.join(OUTPUT_DIR, "val_ids.txt")
test_file  = os.path.join(OUTPUT_DIR, "test_ids.txt")

# =====================================================
# LOAD EXISTING SPLITS (DO NOT RECREATE)
# =====================================================
if all(os.path.exists(f) for f in [train_file, val_file, test_file]):
    print("[INFO] Existing splits found. Loading (LOCKED).")

    with open(train_file) as f:
        train_ids = [l.strip() for l in f if l.strip()]
    with open(val_file) as f:
        val_ids = [l.strip() for l in f if l.strip()]
    with open(test_file) as f:
        test_ids = [l.strip() for l in f if l.strip()]

else:
    # ---------------- LIST IDENTITIES ----------------
    identities = sorted([
        d for d in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, d))
    ])

    print(f"[INFO] Total identities available: {len(identities)}")

    if len(identities) == 0:
        raise RuntimeError("No identities found in celeba_identities!")

    # ---------------- SHUFFLE (ONCE ONLY) ----------------
    random.seed(RANDOM_SEED)
    random.shuffle(identities)

    n_total = len(identities)
    n_train = int(n_total * TRAIN_RATIO)
    n_val   = int(n_total * VAL_RATIO)

    train_ids = identities[:n_train]
    val_ids   = identities[n_train:n_train + n_val]
    test_ids  = identities[n_train + n_val:]

    # ---------------- SAVE SPLITS ----------------
    with open(train_file, "w") as f:
        f.write("\n".join(train_ids))
    with open(val_file, "w") as f:
        f.write("\n".join(val_ids))
    with open(test_file, "w") as f:
        f.write("\n".join(test_ids))

    print("[INFO] New identity splits created and LOCKED.")

# ---------------- SANITY CHECKS (MANDATORY) ----------------
assert len(train_ids) > 0, "Train split empty!"
assert len(val_ids) > 0, "Validation split empty!"
assert len(test_ids) > 0, "Test split empty!"

assert len(set(train_ids) & set(val_ids)) == 0, "Train/Val leakage!"
assert len(set(train_ids) & set(test_ids)) == 0, "Train/Test leakage!"
assert len(set(val_ids) & set(test_ids)) == 0, "Val/Test leakage!"

# ---------------- SUMMARY ----------------
print("\nSplit summary (IDENTITY-DISJOINT):")
print(f"  Train: {len(train_ids)} identities")
print(f"  Val  : {len(val_ids)} identities")
print(f"  Test : {len(test_ids)} identities")

print("\nSplits are fixed, reproducible, and safe.")
