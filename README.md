# Jobify

This repository contains the Jobify Django project. These instructions help you initialize git, create a GitHub repository, and push the project.

## Quick steps to push to GitHub

Option A — using the `gh` CLI (recommended):

```bash
git init
git add .
git commit -m "Initial commit"
# Create a new repo on GitHub and push
gh repo create <OWNER>/<REPO> --public --source=. --remote=origin --push
```

Option B — manual via GitHub website:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<OWNER>/<REPO>.git
git push -u origin main
```

Notes:
- Ensure you do not commit sensitive files (use the included `.gitignore`).
- If you want a private repo, choose `--private` with `gh repo create` or set visibility on GitHub.
