# Annotation Platform

This folder contains the source code of the custom annotation platform
used to collect MOS scores from 50 UX experts.

- `app.py`: Flask application entry point
- `templates/`: HTML templates
- `static/`: CSS/JS assets

To run locally:
```bash
pip install flask
python app.py
The platform presents each UI component with its rendered screenshot and
DOM snippet, and asks experts to score overall quality on a 1–100 MOS scale.
Each component is evaluated by 3 independent experts.
