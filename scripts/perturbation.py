"""
AST Perturbation Injection for Figma-Defect-3.5K

Injects 5 categories of defects into valid HTML/CSS, generating
synthetic training data. 50% of perturbations are inline (style
attribute) and 50% are external (embedded stylesheet).
"""
import random
from typing import Literal


def inject_occlusion(html: str, inline: bool = True) -> str:
    """Inject z-index/position overlap defect."""
    if inline:
        return html.replace(
            "<body>",
            '<body><div style="position:absolute;top:50px;z-index:9999;'
            'background:red;width:100%;height:100px;">'
            "Overlay</div>"
        )
    else:
        return html.replace(
            "</head>",
            "<style>.overlay{position:absolute;top:50px;z-index:9999;"
            "background:red;width:100%;height:100px;}</style></head>"
        ).replace("<body>", '<body><div class="overlay">Overlay</div>')


def inject_misalignment(html: str, inline: bool = True) -> str:
    """Inject flexbox/grid misalignment."""
    style = "display:flex;flex-direction:column;align-items:flex-start;"
    if inline:
        return html.replace("<body>", f'<body><div style="{style}">')
    else:
        return html.replace(
            "</head>", f"<style>.misaligned{{{style}}}</style></head>"
        ).replace("<body>", '<body><div class="misaligned">')


def inject_contrast(html: str, inline: bool = True) -> str:
    """Inject WCAG contrast violation."""
    style = "color:#777;background:#888;"
    if inline:
        return html.replace("<body>", f'<body><p style="{style}">Low contrast</p>')
    else:
        return html.replace(
            "</head>", f"<style>.lowcontrast{{{style}}}</style></head>"
        ).replace("<body>", '<body><p class="lowcontrast">Low contrast</p>')


def inject_overflow(html: str, inline: bool = True) -> str:
    """Inject text overflow."""
    style = "width:100px;white-space:nowrap;overflow:visible;"
    if inline:
        return html.replace("<body>", f'<body><div style="{style}">Very long text exceeding container</div>')
    else:
        return html.replace(
            "</head>", f"<style>.overflow{{{style}}}</style></head>"
        ).replace("<body>", '<body><div class="overflow">Very long text</div>')


def inject_missing_asset(html: str, inline: bool = True) -> str:
    """Inject broken image."""
    return html.replace("<body>", '<body><img src="/nonexistent.png" alt="broken">')


INJECTORS = {
    "css_occlusion": inject_occlusion,
    "spatial_misalignment": inject_misalignment,
    "contrast_violation": inject_contrast,
    "text_overflow": inject_overflow,
    "missing_asset": inject_missing_asset,
}


def apply_random_perturbation(html: str, seed: int = 42):
    """Apply a random perturbation and return (perturbed_html, defect_type, injection_method)."""
    random.seed(seed)
    defect_type = random.choice(list(INJECTORS.keys()))
    inline = random.choice([True, False])
    perturbed = INJECTORS[defect_type](html, inline=inline)
    return perturbed, defect_type, "inline" if inline else "external"


if __name__ == "__main__":
    sample = "<html><head></head><body><p>Hello</p></body></html>"
    for defect in INJECTORS:
        perturbed, dtype, method = apply_random_perturbation(sample)
        print(f"{dtype} ({method}): {len(perturbed)} chars")
