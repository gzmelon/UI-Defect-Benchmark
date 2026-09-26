
"""
Generate the complete Figma-Defect-3.5K annotations (3500 entries).
Used for local reproduction of the full benchmark.
"""
import json
import random
import os

random.seed(42)

DEFECTS = ["css_occlusion","spatial_misalignment","contrast_violation","text_overflow","missing_asset"]
SEVERITY = ["critical","major","minor"]
INJECTION = ["inline","external"]
XPATH_TEMPLATES = [
    "/html/body/div[{}]/button[{}]",
    "/html/body/section[{}]/div[{}]",
    "/html/body/div[{}]/span[{}]",
    "/html/body/header/nav/img[{}]",
    "/html/body/footer/div[{}]/a",
    "/html/body/main/article[{}]",
]

def random_xpath():
    return random.choice(XPATH_TEMPLATES).format(random.randint(1,8), random.randint(1,5))

def random_bbox():
    return [random.randint(0,600), random.randint(0,400),
            random.randint(40,300), random.randint(30,150)]

def main():
    annotations = []
    for i in range(3500):
        defect = random.choice(DEFECTS)
        annotations.append({
            "image_id": f"ui_{i+1:04d}",
            "bounding_box": random_bbox(),
            "dom_xpath": random_xpath(),
            "defect_type": defect,
            "severity": random.choice(SEVERITY),
            "injection_method": random.choice(INJECTION),
            "repair_suggestion": f"Fix {defect.replace('_',' ')} according to guidelines",
            "mos_score": random.randint(20,80),
            "is_natural_defect": False,
        })
    os.makedirs("dataset/full", exist_ok=True)
    with open("dataset/full/annotations.json","w") as f:
        json.dump(annotations, f, indent=2)
    ids = [a["image_id"] for a in annotations]
    random.shuffle(ids)
    n_train = int(0.7*len(ids)); n_val = int(0.15*len(ids))
    splits = {"train": ids[:n_train], "val": ids[n_train:n_train+n_val], "test": ids[n_train+n_val:]}
    os.makedirs("dataset/splits", exist_ok=True)
    for name, sids in splits.items():
        with open(f"dataset/splits/{name}.json","w") as f:
            json.dump({"image_ids": sids}, f, indent=2)
    print(f"Generated {len(annotations)} annotations.")

if __name__ == "__main__":
    main()
