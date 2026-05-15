# Setting up Trusted Publishing

This guide describes how to set up GitHub Trusted Publishing to upload releases to PyPI without storing an API token locally.

## What this replaces

Trusted Publishing can replace a local `twine` + API token workflow by delegating uploads to a GitHub Actions workflow with an `id-token` permission.

## PyPI setup

1. Go to https://pypi.org and navigate to your project.
2. Under **Settings → Collaborators & Teams → Add publisher** add a publisher with the following details:
   - owner: `mondi04`
   - repository: `htmforge`
   - workflow filename: `publish.yml`
   - environment: `release`

## GitHub setup

1. Go to your repository **Settings → Environments** and create a new environment named `release`.
2. No protection rules are required for personal projects; the environment is used to scope the upload permission.

## How to use

Once configured, go to the repository **Actions** tab, pick **Publish to PyPI**, and click **Run workflow**. Type `publish` into the confirmation input to start the run.

This workflow builds the distribution using `python -m build` and publishes via the PyPA publish action. It is an optional, manual alternative to using `push.py` locally.

## Note

`push.py` remains the primary local release tool and is unchanged. Trusted Publishing only provides an optional CI-based publish path.
