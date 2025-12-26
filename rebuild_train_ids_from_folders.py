import os
import random

# ================= CONFIG =================
PROJECT_ROOT = r"D:\Face recogination project"
BASE_DIR = os.path.join(PROJECT_ROOT, "data_processed")

CELEBA_DIR = os.path.join(BASE_DIR, "celeba_identities")
SPLITS_DIR = os.path.join(BASE_DIR, "splits")

TRAIN_RATIO = 0.70
VAL_RATIO   = 0.15
TEST_RATIO  = 0.15

# 🔒 Fixed seed — splits created ONCE and reused
RANDOM_SEED = 42
# ========================================

os.makedirs(SPLITS_DIR, exist_ok=True)

train_file = os.path.join(SPLITS_DIR, "train_ids.txt")
val_file   = os.path.join(SPLITS_DIR, "val_ids.txt")
test_file  = os.path.join(SPLITS_DIR, "test_ids.txt")

# -------------------------------------------------
# IF SPLITS EXIST → LOAD (DO NOT RE-SHUFFLE)
# -------------------------------------------------
if all(os.path.exists(f) for f in [train_file, val_file, test_file]):
    print("[INFO] Existing identity splits found. Loading (LOCKED).")

    with open(train_file) as f:
        train_ids = [l.strip() for l in f if l.strip()]
    with open(val_file) as f:
        val_ids = [l.strip() for l in f if l.strip()]
    with open(test_file) as f:
        test_ids = [l.strip() for l in f if l.strip()]

else:
    # ---------------- LOAD IDENTITIES ----------------
    ids = sorted([
        d for d in os.listdir(CELEBA_DIR)
        if os.path.isdir(os.path.join(CELEBA_DIR, d))
    ])

    print(f"[INFO] Total identities found in CelebA: {len(ids)}")

    if len(ids) == 0:
        raise RuntimeError("No identity folders found in celeba_identities!")

    # ---------------- SHUFFLE (ONCE ONLY) ----------------
    random.seed(RANDOM_SEED)
    random.shuffle(ids)

    # ---------------- SPLIT ----------------
    n = len(ids)
    n_train = int(TRAIN_RATIO * n)
    n_val   = int(VAL_RATIO * n)

    train_ids = ids[:n_train]
    val_ids   = ids[n_train:n_train + n_val]
    test_ids  = ids[n_train + n_val:]

    # ---------------- SAVE SPLITS ----------------
    with open(train_file, "w") as f:
        f.write("\n".join(train_ids))
    with open(val_file, "w") as f:
        f.write("\n".join(val_ids))
    with open(test_file, "w") as f:
        f.write("\n".join(test_ids))

    print("[INFO] New identity splits created and LOCKED.")

# ---------------- SANITY CHECK (MANDATORY) ----------------
assert len(train_ids) > 0, "Train split empty!"
assert len(val_ids) > 0, "Validation split empty!"
assert len(test_ids) > 0, "Test split empty!"

assert len(set(train_ids) & set(val_ids)) == 0, "Train/Val identity leakage!"
assert len(set(train_ids) & set(test_ids)) == 0, "Train/Test identity leakage!"
assert len(set(val_ids) & set(test_ids)) == 0, "Val/Test identity leakage!"

# ---------------- SUMMARY ----------------
print("\nSplit summary (IDENTITY-DISJOINT):")
print(f"  Train: {len(train_ids)} identities")
print(f"  Val  : {len(val_ids)} identities")
print(f"  Test : {len(test_ids)} identities")

print("\nSplits are identity-disjoint and reproducible.")
