import os
import shutil
from collections import defaultdict
import json

# ================= CONFIG =================
PROJECT_ROOT = r"D:\Face recogination project"
CELEBA_ROOT = os.path.join(PROJECT_ROOT, "Celeba")

IMAGE_DIR = os.path.join(
    CELEBA_ROOT,
    "img_align_celeba",
    "img_align_celeba"
)

IDENTITY_FILE = os.path.join(CELEBA_ROOT, "identity_CelebA.txt")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data_processed", "celeba_identities")
META_FILE = os.path.join(OUTPUT_DIR, "preprocess_meta.json")

MIN_IMAGES_PER_ID = 5
# =========================================

# --------------------------------------------------
# DO NOT REBUILD IF ALREADY EXISTS (REPRODUCIBILITY)
# --------------------------------------------------
if os.path.exists(META_FILE):
    print("[INFO] celeba_identities already built. Skipping rebuild.")
    with open(META_FILE) as f:
        meta = json.load(f)
    print(f"[INFO] Loaded metadata: {meta}")
    exit(0)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------- READ IDENTITY MAPPING ----------------
id_map = defaultdict(list)

with open(IDENTITY_FILE, "r") as f:
    for line in f:
        img, pid = line.strip().split()
        id_map[pid].append(img)

print(f"[INFO] Total identities in mapping file: {len(id_map)}")
print(f"[INFO] Image source directory: {IMAGE_DIR}")

if not os.path.isdir(IMAGE_DIR):
    raise FileNotFoundError(
        f"Image directory not found: {IMAGE_DIR}\n"
        "Check CelebA extraction path."
    )

# ---------------- PROCESS IDENTITIES ----------------
kept = 0
dropped = 0
total_images_copied = 0

for pid, images in id_map.items():
    if len(images) < MIN_IMAGES_PER_ID:
        dropped += 1
        continue

    person_id = f"id_{int(pid):06d}"
    person_dir = os.path.join(OUTPUT_DIR, person_id)
    os.makedirs(person_dir, exist_ok=True)

    copied = 0
    for img in images:
        src = os.path.join(IMAGE_DIR, img)
        dst = os.path.join(person_dir, img)

        if os.path.exists(src):
            shutil.copy(src, dst)
            copied += 1

    # ---------------- SAFETY CHECK ----------------
    if copied < MIN_IMAGES_PER_ID:
        shutil.rmtree(person_dir)
        dropped += 1
        continue

    kept += 1
    total_images_copied += copied

# ---------------- FINAL INTEGRITY CHECK ----------------
assert kept > 0, "No identities were kept!"
assert total_images_copied >= kept * MIN_IMAGES_PER_ID

# ---------------- SAVE METADATA ----------------
meta = {
    "min_images_per_id": MIN_IMAGES_PER_ID,
    "identities_total": len(id_map),
    "identities_kept": kept,
    "identities_dropped": dropped,
    "total_images_copied": total_images_copied
}

with open(META_FILE, "w") as f:
    json.dump(meta, f, indent=2)

# ---------------- SUMMARY ----------------
print("\nCelebA identity preprocessing COMPLETE.")
print(f"Identities kept   : {kept}")
print(f"Identities dropped: {dropped}")
print(f"Images copied     : {total_images_copied}")
print("Dataset is stable, logged, and reproducible.")
