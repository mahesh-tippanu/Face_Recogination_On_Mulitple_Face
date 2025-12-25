import os
import random
from collections import defaultdict
import json

# ================= CONFIG =================
PROJECT_ROOT = r"D:\Face recogination project"
BASE_DIR = os.path.join(PROJECT_ROOT, "data_processed")

TRAIN_IDS_FILE = os.path.join(BASE_DIR, "splits", "train_ids.txt")
CELEBA_DIR = os.path.join(BASE_DIR, "celeba_identities")
OUTPUT_DIR = os.path.join(BASE_DIR, "federated")

CLIENT_SETTINGS = [10, 20, 50]
RANDOM_SEED = 42

MIN_IDS_PER_CLIENT = 50
MAX_IDS_PER_CLIENT = 150
# =========================================

# ---------------- LOAD & VALIDATE IDS ----------------
with open(TRAIN_IDS_FILE, "r") as f:
    raw_ids = [line.strip() for line in f if line.strip()]

celeba_folders = set(os.listdir(CELEBA_DIR))
train_ids_master = sorted([i for i in raw_ids if i in celeba_folders])

print(f"Total train IDs (raw)  : {len(raw_ids)}")
print(f"Total train IDs (valid): {len(train_ids_master)}")

if len(train_ids_master) == 0:
    raise RuntimeError("No valid identities found in celeba_identities!")

# ---------------- CREATE CLIENTS ----------------
for num_clients in CLIENT_SETTINGS:
    print(f"\nCreating {num_clients} federated clients...")

    # 🔒 RESET RNG FOR EACH SETTING (REPRODUCIBLE & FAIR)
    rng = random.Random(RANDOM_SEED + num_clients)
    train_ids = train_ids_master.copy()
    rng.shuffle(train_ids)

    out_dir = os.path.join(OUTPUT_DIR, f"clients_{num_clients}")
    os.makedirs(out_dir, exist_ok=True)

    clients = defaultdict(list)
    idx = 0

    # ---------------- PRIMARY ASSIGNMENT ----------------
    for cid in range(num_clients):
        size = rng.randint(MIN_IDS_PER_CLIENT, MAX_IDS_PER_CLIENT)

        for _ in range(size):
            if idx >= len(train_ids):
                break
            clients[cid].append(train_ids[idx])
            idx += 1

    # ---------------- DISTRIBUTE REMAINING ----------------
    remaining = train_ids[idx:]
    for rid in remaining:
        cid = rng.randint(0, num_clients - 1)
        clients[cid].append(rid)

    # ---------------- SAVE CLIENT FILES ----------------
    total_assigned = 0
    empty_clients = []

    for cid in range(num_clients):
        ids = clients[cid]
        if len(ids) == 0:
            empty_clients.append(cid)
            continue

        client_file = os.path.join(out_dir, f"client_{cid:02d}.txt")
        with open(client_file, "w") as f:
            f.write("\n".join(ids))

        total_assigned += len(ids)

    # ---------------- HARD ASSERTIONS ----------------
    assert total_assigned == len(train_ids_master), \
        "Identity loss during federated assignment!"

    assert len(empty_clients) == 0, \
        f"Empty clients detected: {empty_clients}"

    # ---------------- SAVE METADATA ----------------
    meta = {
        "num_clients": num_clients,
        "random_seed": RANDOM_SEED + num_clients,
        "min_ids_per_client": MIN_IDS_PER_CLIENT,
        "max_ids_per_client": MAX_IDS_PER_CLIENT,
        "total_train_ids": len(train_ids_master),
        "total_assigned": total_assigned
    }

    with open(os.path.join(out_dir, "federated_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    print(f"  Total identities assigned: {total_assigned}")
    print(f"  Saved to: {out_dir}")

print("\nFederated client split COMPLETE (REPRODUCIBLE & SAFE).")
