# Markdown Accessibility Helper

A GitHub action that helps improve the accessibility of Markdown files in your repository by automatically adding alternative text to images that do not have it. This action uses the [microsoft/git-base-coco](https://huggingface.co/microsoft/git-base-coco) model from HuggingFace to generate alt text by default, or the describe image ability of [Azure Computer Vision Resource](https://azure.microsoft.com/en-us/products/cognitive-services/vision-services) can also be used.

## Features

- Automatically adds alternative text to images in all markdown files that do not have it.
- Supports both PNG and JPEG image formats.
- Supports both local and remote images.
- Using the Azure Computer Vision Resource, you can specify a language for alt text generation. Supported languages: en - English (Default), es - Spanish, ja - Japanese, pt - Portuguese, zh - Simplified Chinese.

## Usage

To use the Markdown Accessibility Helper action in your repository, add the following YAML code to your workflow file (e.g. .github/workflows/markdown-accessibility-helper.yaml):

```yaml
name: Markdown Accessibility Helper

# Runs only when triggered manually. You can also trigger this action on a schedule or on push or pull request events by changing the on section.
on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Markdown Accessibility
        uses: sam9111/markdown-accessibility-helper@v1.0.2
```

According to this workflow file, you can run the action manually by going to the Actions tab in your repository and selecting the Markdown Accessibility Helper workflow.

### With Azure Computer Vision Resource

```yaml
name: Markdown Accessibility Helper

# Runs only when triggered manually. You can also trigger this action on a schedule or on push or pull request events by changing the on section.
on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Markdown Accessibility
        uses: sam9111/markdown-accessibility-helper@v1.0.2
        with:
          # Azure Computer Vision Resource Key (optional)
          azure_key: ${{ secrets.AZURE_KEY }}
          # Azure Computer Vision Resource Endpoint (optional)
          azure_endpoint: ${{ secrets.AZURE_ENDPOINT }}
          # Language to use for alt text generation with Azure Computer Vision Resource (optional)
          language: 'en'|'es'|'ja'|'pt'|'zh'
```

With your Azure subscription, create a Computer Vision resource in the Azure portal to get your key and endpoint. You can use the free pricing tier (F0) which gives you 5,000 transactions free per month to try the service, and upgrade later to a paid tier if needed.

Add your Azure key and endpoint to your repository secrets.

In the with section of your workflow file, you can provide your Azure endpoint and key as secrets to access the Azure Computer Vision Resource.

You can also specify another language for alt text generation with the language parameter. The default language is English.
