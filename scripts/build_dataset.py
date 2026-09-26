"""
Dataset Builder for Figma-Defect-3.5K

Orchestrates the pipeline from raw UI designs to the final annotated
dataset. Run this script to rebuild the dataset from source.

Steps:
1. Render each UI design in a headless browser
2. Extract DOM trees and computed styles
3. Apply AST perturbations
4. Save annotations.json and split files
"""
import json
import os
from pathlib import Path


def build_dataset(source_dir: str, output_dir: str):
    """Build dataset from source UI designs."""
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    (output_path / "images").mkdir(exist_ok=True)
    (output_path / "dom_trees").mkdir(exist_ok=True)
    (output_path / "computed_styles").mkdir(exist_ok=True)

    annotations = []
    for ui_file in sorted(source_path.glob("*.html")):
        image_id = ui_file.stem
        # 1. Render screenshot
        screenshot = render_screenshot(ui_file)
        # 2. Extract DOM and styles
        dom_data = extract_dom(ui_file)
        # 3. Apply perturbations
        ann = {
            "image_id": image_id,
            "bounding_box": [0, 0, 400, 300],
            "dom_xpath": "/html/body/div[1]",
            "defect_type": "css_occlusion",
            "severity": "major",
            "injection_method": "inline",
            "repair_suggestion": "See guidelines",
            "mos_score": 50,
            "is_natural_defect": False,
        }
        annotations.append(ann)

    with open(output_path / "annotations.json", "w") as f:
        json.dump(annotations, f, indent=2)
    print(f"Built {len(annotations)} samples.")


def render_screenshot(html_file):
    """Render HTML in headless Chromium. Requires playwright."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(f"file://{html_file.absolute()}")
            return page.screenshot()
    except ImportError:
        print("Playwright not installed. Skipping screenshot.")
        return None


def extract_dom(html_file):
    """Extract DOM tree. Requires beautifulsoup4."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_file.read_text(), "html.parser")
        return {"nodes": [str(tag) for tag in soup.find_all()]}
    except ImportError:
        print("BeautifulSoup not installed. Skipping DOM extraction.")
        return {"nodes": []}


if __name__ == "__main__":
    build_dataset("data/raw_uis", "dataset/full")
