import os
import random
import shutil
import json
import argparse

# ================= ARGUMENTS =================
parser = argparse.ArgumentParser(
    description="Generate multi-face registration attacks"
)
parser.add_argument(
    "--seed",
    type=int,
    default=42,
    help="Random seed for reproducibility"
)
args = parser.parse_args()

RANDOM_SEED = args.seed
random.seed(RANDOM_SEED)
# ============================================

# ================= CONFIG ====================
PROJECT_ROOT = r"D:\Face recogination project"

BASE_DIR = os.path.join(PROJECT_ROOT, "data_processed")
CELEBA_DIR = os.path.join(BASE_DIR, "celeba_identities")
FEDERATED_DIR = os.path.join(BASE_DIR, "federated", "clients_20")
OUTPUT_DIR = os.path.join(BASE_DIR, "attack_dataset")

ATTACK_FRACTION = 0.25              # 25% malicious clients
IMAGES_PER_ID = 3
NUM_ATTACK_IDS_PER_CLIENT = 10      # realistic (10–20)
DONORS_PER_ATTACK = 2
# ============================================

# ---------------- OUTPUT DIRS ----------------
NORMAL_DIR = os.path.join(OUTPUT_DIR, "NormalPairs")
ATTACK_DIR = os.path.join(OUTPUT_DIR, "AttackPairs")
os.makedirs(NORMAL_DIR, exist_ok=True)
os.makedirs(ATTACK_DIR, exist_ok=True)

# ---------------- LOAD CLIENT FILES ----------------
clients = sorted([
    f for f in os.listdir(FEDERATED_DIR)
    if f.endswith(".txt")
])

num_clients = len(clients)
assert num_clients > 0, "No client files found!"

num_attack_clients = max(1, int(num_clients * ATTACK_FRACTION))
malicious_clients = sorted(
    random.sample(clients, num_attack_clients)
)

print(f"Random seed          : {RANDOM_SEED}")
print(f"Total clients        : {num_clients}")
print(f"Malicious clients ({num_attack_clients}): {malicious_clients}")

# ---------------- METADATA ----------------
attack_metadata = {
    "random_seed": RANDOM_SEED,
    "attack_fraction": ATTACK_FRACTION,
    "num_attack_ids_per_client": NUM_ATTACK_IDS_PER_CLIENT,
    "donors_per_attack": DONORS_PER_ATTACK,
    "malicious_clients": malicious_clients,
    "clients": []
}

# ---------------- PROCESS CLIENTS ----------------
for client in clients:
    client_path = os.path.join(FEDERATED_DIR, client)

    with open(client_path, "r") as f:
        identities = [line.strip() for line in f if line.strip()]

    valid = [
        i for i in identities
        if os.path.isdir(os.path.join(CELEBA_DIR, i))
    ]

    print(f"{client}: raw={len(identities)}, valid={len(valid)}")

    if len(valid) < 3:
        print(f"Skipping {client} (not enough valid identities)")
        continue

    client_name = client.replace(".txt", "")

    # ===================== ATTACK CLIENT =====================
    if client in malicious_clients:
        out_client = os.path.join(ATTACK_DIR, client_name)
        os.makedirs(out_client, exist_ok=True)

        attack_targets = random.sample(
            valid,
            min(NUM_ATTACK_IDS_PER_CLIENT, len(valid))
        )

        for target_id in attack_targets:
            donors = random.sample(
                [i for i in valid if i != target_id],
                k=min(DONORS_PER_ATTACK, len(valid) - 1)
            )

            tgt_dir = os.path.join(out_client, target_id)
            os.makedirs(tgt_dir, exist_ok=True)

            # ----- target images -----
            tgt_imgs = os.listdir(
                os.path.join(CELEBA_DIR, target_id)
            )
            for img in random.sample(
                tgt_imgs, min(IMAGES_PER_ID, len(tgt_imgs))
            ):
                shutil.copy(
                    os.path.join(CELEBA_DIR, target_id, img),
                    os.path.join(tgt_dir, img)
                )

            # ----- donor injections -----
            for donor in donors:
                donor_imgs = os.listdir(
                    os.path.join(CELEBA_DIR, donor)
                )
                for img in random.sample(
                    donor_imgs, min(IMAGES_PER_ID, len(donor_imgs))
                ):
                    shutil.copy(
                        os.path.join(CELEBA_DIR, donor, img),
                        os.path.join(
                            tgt_dir,
                            f"attack_{donor}_{img}"
                        )
                    )

            attack_metadata["clients"].append({
                "client": client_name,
                "type": "attack",
                "target_identity": target_id,
                "donor_identities": donors
            })

    # ===================== NORMAL CLIENT =====================
    else:
        out_client = os.path.join(NORMAL_DIR, client_name)
        os.makedirs(out_client, exist_ok=True)

        for identity in valid:
            id_dir = os.path.join(out_client, identity)
            os.makedirs(id_dir, exist_ok=True)

            imgs = os.listdir(
                os.path.join(CELEBA_DIR, identity)
            )
            for img in random.sample(
                imgs, min(IMAGES_PER_ID, len(imgs))
            ):
                shutil.copy(
                    os.path.join(CELEBA_DIR, identity, img),
                    os.path.join(id_dir, img)
                )

        attack_metadata["clients"].append({
            "client": client_name,
            "type": "normal"
        })

# ---------------- SAVE METADATA ----------------
attack_meta_path = os.path.join(
    OUTPUT_DIR, "attack_metadata.json"
)
with open(attack_meta_path, "w") as f:
    json.dump(attack_metadata, f, indent=2)

print("\n[INFO] attack_metadata.json saved to:")
print(attack_meta_path)
print("\nMulti-face registration attack generation COMPLETE.")