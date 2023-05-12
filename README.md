# Markdown Accessibility Helper

A GitHub action that helps improve the accessibility of Markdown files in your repository by automatically adding alternative text to images that do not have it. This action uses the [microsoft/git-base-coco](https://huggingface.co/microsoft/git-base-coco) model from HuggingFace to generate alt text, or the describe image ability of [Azure Computer Vision Resource](https://azure.microsoft.com/en-us/products/cognitive-services/vision-services) can also be used.

## Features

- Automatically adds alternative text to images in all markdown files that do not have it.
- Supports both PNG and JPEG image formats.
- Supports both local and remote images.

## Usage

To use the Markdown Accessibility Helper action in your repository, add the following YAML code to your workflow file (e.g. .github/workflows/markdown-accessibility-helper.yaml):

```yaml
name: My Workflow

# Runs only when triggered manually

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Markdown Accessibility
        uses: sam9111/markdown-accessibility-helper@main
        with:
          # The GitHub token to use for authentication
          # Default: ${{ github.token }}
          token: ${{ secrets.GITHUB_TOKEN }}
          # Azure Computer Vision Resource Key (optional)
          azure_key: ${{ secrets.AZURE_KEY }}
          # Azure Computer Vision Resource Endpoint (optional)
          azure_endpoint: ${{ secrets.AZURE_ENDPOINT }}
          # Language to use for alt text generation with Azure Computer Vision Resource (optional)
          language: "en"
```
