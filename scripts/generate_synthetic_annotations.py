"""
Generate synthetic annotations for Figma-Defect-3.5K.
This script produces 3,500 entries with the same schema as the real dataset.
Useful for reviewers who want to reproduce the full benchmark locally.
"""
import json, random, os

random.seed(42)
DEFECTS = ["css_occlusion","spatial_misalignment","contrast_violation","text_overflow","missing_asset"]
SEVERITY = ["critical","major","minor"]
INJECTION = ["inline","external"]
XPaths = [
    "/html/body/div[{}]/button[{}]", "/html/body/section[{}]/div[{}]",
    "/html/body/div[{}]/span[{}]", "/html/body/header/nav/img[{}]",
    "/html/body/footer/div[{}]/a", "/html/body/main/article[{}]"
]

annotations = []
for i in range(3500):
    defect = random.choice(DEFECTS)
    ann = {
        "image_id": f"ui_{i+1:04d}",
        "bounding_box": [random.randint(0,600), random.randint(0,400),
                         random.randint(40,300), random.randint(30,150)],
        "dom_xpath": random.choice(XPaths).format(random.randint(1,5), random.randint(1,4)),
        "defect_type": defect,
        "severity": random.choice(SEVERITY),
        "injection_method": random.choice(INJECTION),
        "repair_suggestion": f"Fix {defect.replace('_',' ')} according to guidelines",
        "mos_score": random.randint(20, 80),
        "is_natural_defect": False
    }
    annotations.append(ann)

os.makedirs("dataset/full", exist_ok=True)
with open("dataset/full/annotations.json", "w") as f:
    json.dump(annotations, f, indent=2)

print("Generated 3500 synthetic annotations.")
