"""
DOM-Only Heuristic Baseline
Rule-based defect detection using only the serialized DOM.

This baseline serves as a lower bound for comparison. It cannot detect
visual defects such as CSS occlusion or spatial misalignment, because
those defects require rendered pixel information.

Reference: Table 3, row 1 of the paper.
Expected performance: Precision 68.5%, Recall 42.1%, F1 0.521.
"""
import re
from typing import Dict, List


def detect_defects(dom_snippet: str, computed_styles: Dict[str, str]) -> List[Dict]:
    """
    Rule-based detection over serialized DOM and computed styles.

    Args:
        dom_snippet: Serialized HTML string
        computed_styles: Mapping from selector → style dict

    Returns:
        List of detected defects, each with type, severity, xpath.
    """
    defects = []

    # Rule 1: Missing ARIA attributes on interactive elements
    for m in re.finditer(r'<(button|a|input)[^>]*>', dom_snippet):
        tag = m.group(0)
        if 'aria-label' not in tag and 'aria-labelledby' not in tag:
            defects.append({
                "defect_type": "missing_aria",
                "severity": "major",
                "xpath": _find_xpath(dom_snippet, m.start()),
                "repair_suggestion": "Add aria-label or aria-labelledby",
            })

    # Rule 2: Inline style with extreme z-index (potential occlusion)
    for selector, styles in computed_styles.items():
        z = styles.get("z-index", "")
        if z and z.lstrip("-").isdigit() and abs(int(z)) > 1000:
            defects.append({
                "defect_type": "css_occlusion",
                "severity": "major",
                "xpath": selector,
                "repair_suggestion": "Reduce z-index or restructure stacking context",
            })

    # Rule 3: position:absolute without parent position:relative
    for selector, styles in computed_styles.items():
        if styles.get("position") == "absolute":
            parent_sel = _parent_selector(selector)
            if parent_sel and computed_styles.get(parent_sel, {}).get("position") != "relative":
                defects.append({
                    "defect_type": "spatial_misalignment",
                    "severity": "major",
                    "xpath": selector,
                    "repair_suggestion": "Set parent position:relative",
                })

    # Rule 4: Missing image src
    for m in re.finditer(r'<img[^>]*>', dom_snippet):
        tag = m.group(0)
        if 'src=' not in tag or 'src=""' in tag or "src=''" in tag:
            defects.append({
                "defect_type": "missing_asset",
                "severity": "critical",
                "xpath": _find_xpath(dom_snippet, m.start()),
                "repair_suggestion": "Provide valid image src or use placeholder",
            })

    return defects


def _find_xpath(html: str, pos: int) -> str:
    """Approximate XPath by counting preceding tags of the same type."""
    prefix = html[:pos]
    tag_match = re.search(r'<(\w+)[^>]*$', prefix)
    if not tag_match:
        return "/html/body"
    tag = tag_match.group(1)
    count = len(re.findall(rf'<{tag}\b', prefix))
    return f"/html/body//{tag}[{count}]"


def _parent_selector(selector: str) -> str:
    """Get the parent selector from a CSS-like selector string."""
    parts = selector.rsplit(" > ", 1)
    return parts[0] if len(parts) > 1 else ""


if __name__ == "__main__":
    sample_dom = '<html><body><button>Click</button><img src=""></body></html>'
    sample_styles = {
        "body > div.banner": {"position": "absolute", "z-index": "9999"},
    }
    defects = detect_defects(sample_dom, sample_styles)
    for d in defects:
        print(d)
