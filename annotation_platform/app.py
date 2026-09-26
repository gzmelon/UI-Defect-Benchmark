"""
Annotation Platform for Figma-Defect-3.5K

Flask-based web application used to collect MOS scores from 50 UX experts
over a 3-month period. Each UI component was shown to 3 independent
experts, who scored quality on a 1-100 MOS scale.

To run:
    pip install flask
    python app.py
Then open http://localhost:5000 in your browser.
"""
import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
ANNOTATIONS_FILE = "annotations.json"
RESULTS_FILE = "expert_scores.json"


def load_annotations():
    if not os.path.exists(ANNOTATIONS_FILE):
        return []
    with open(ANNOTATIONS_FILE) as f:
        return json.load(f)


def save_score(image_id, expert_id, score, comments=""):
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            results = json.load(f)
    else:
        results = []
    results.append({
        "image_id": image_id,
        "expert_id": expert_id,
        "mos_score": score,
        "comments": comments,
    })
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


@app.route("/")
def index():
    annotations = load_annotations()
    return render_template("index.html", annotations=annotations)


@app.route("/api/component/<image_id>")
def get_component(image_id):
    annotations = load_annotations()
    for ann in annotations:
        if ann["image_id"] == image_id:
            return jsonify(ann)
    return jsonify({"error": "not found"}), 404


@app.route("/api/score", methods=["POST"])
def submit_score():
    data = request.json
    required = ["image_id", "expert_id", "mos_score"]
    if not all(k in data for k in required):
        return jsonify({"error": "missing fields"}), 400
    save_score(
        data["image_id"], data["expert_id"],
        data["mos_score"], data.get("comments", ""),
    )
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
