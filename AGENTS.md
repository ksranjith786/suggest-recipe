# Agent guide — Suggest Recipe

Flask app that suggests recipes from pantry ingredients. UI uses **Dew Design** (dark glass, mint/amber accents, Fraunces + DM Sans).

## Run locally

```bash
cd project
export FLASK_ENV=development
export DATABASE_URL=sqlite:///database.db
python app.py
```

Open `http://127.0.0.1:5000/` (redirects to `/ingredients/`).

## Architecture

| Layer | Location |
|-------|----------|
| App factory | `project/app.py` |
| Routes | `project/routes/` (`ingredients`, `recipes`, `home`, `seed`, …) |
| Templates | `project/templates/` — extend `base.html` for user-facing pages |
| UI styles | `project/static/css/cyber-bistro.css` (single source of truth) |
| DB models | `project/database/` |

## UI conventions

- Do **not** add inline `<style>` blocks to templates except tiny one-offs; extend `cyber-bistro.css`.
- Preserve form field names: `meal`, `combination`, `ingredient` (backend depends on them).
- Use `url_for('static', …)` and `url_for('…')` for links; no hardcoded paths.
- Legacy templates `recipes_v0.html`, `recipes_v1.html` and old CSS files are unused by live routes—avoid editing unless migrating.

## Recipe results

`recipes.py` renders `recipes.html` with `recipe.imageURL`, match counts, and sorted-by-match-ratio list. Errors use `error.html`.
