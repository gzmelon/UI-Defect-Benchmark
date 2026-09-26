"""
Natural Defect Mining from Open-Source Repositories

Mines UI defects from GitHub issues in React, Vue, and Bootstrap
repositories. Each candidate is manually validated by 3 annotators
before inclusion in the natural defect subset.

Usage:
    python scripts/mine_natural_defects.py --output dataset/natural_defects/
"""
import json
import os
import argparse
from datetime import datetime


CANDIDATE_REPOS = [
    "facebook/react",
    "vuejs/core",
    "twbs/bootstrap",
    "angular/angular",
    "sveltejs/svelte",
]

ISSUE_LABELS = ["bug", "ui", "layout", "css", "visual"]


def fetch_candidate_issues(repo: str, max_issues: int = 100):
    """
    Fetch candidate issues from GitHub API.
    Requires a GitHub token for higher rate limits.
    """
    try:
        import requests
    except ImportError:
        print("Install requests: pip install requests")
        return []

    token = os.environ.get("GITHUB_TOKEN", "")
    headers = {"Authorization": f"token {token}"} if token else {}
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {"labels": ",".join(ISSUE_LABELS), "state": "closed",
              "per_page": min(max_issues, 100)}
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        print(f"Failed to fetch {repo}: {r.status_code}")
        return []
    return r.json()


def validate_candidate(issue: dict) -> bool:
    """Heuristic validation: must have visual evidence."""
    body = (issue.get("body") or "").lower()
    return any(kw in body for kw in ["screenshot", "image", "render", "ui", "css"])


def mine(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    all_candidates = []
    for repo in CANDIDATE_REPOS:
        print(f"Mining {repo}...")
        issues = fetch_candidate_issues(repo)
        for issue in issues:
            if validate_candidate(issue):
                all_candidates.append({
                    "repo": repo,
                    "issue_number": issue["number"],
                    "title": issue["title"],
                    "url": issue["html_url"],
                    "defect_type": _classify_defect(issue["title"] + " " + (issue.get("body") or "")),
                    "validated": False,
                })
    with open(os.path.join(output_dir, "candidates.json"), "w") as f:
        json.dump(all_candidates, f, indent=2)
    print(f"Mined {len(all_candidates)} candidates. Manual validation required.")


def _classify_defect(text: str) -> str:
    text_lower = text.lower()
    if any(kw in text_lower for kw in ["overlap", "occlusion", "z-index"]):
        return "css_occlusion"
    if any(kw in text_lower for kw in ["misalign", "flex", "grid", "layout"]):
        return "spatial_misalignment"
    if any(kw in text_lower for kw in ["contrast", "color", "wcag"]):
        return "contrast_violation"
    if any(kw in text_lower for kw in ["overflow", "truncat", "text"]):
        return "text_overflow"
    if any(kw in text_lower for kw in ["missing", "broken", "404"]):
        return "missing_asset"
    return "unknown"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="dataset/natural_defects/")
    args = parser.parse_args()
    mine(args.output)
