# Markdown Accessibility Helper

A GitHub action that helps improve the accessibility of Markdown files in your repository by automatically adding alternative text to images that do not have it.

## Features

- Automatically adds alternative text to images in all markdown files that do not have it.
- Recursively searches through all markdown files in all folders.
- Supports both PNG and JPEG image formats.
- Using the Azure Computer Vision Resource, you can specify a language for alt text generation. Supported languages: en - English (Default), es - Spanish, ja - Japanese, pt - Portuguese, zh - Simplified Chinese.
- The [markdownlint-cli2-action](https://github.com/DavidAnson/markdownlint-cli2-action) runs each time to lint all the markdown files and fix errors if possible.

## Usage

> Action Permissions: This action requires read and write access to your repository to modify the markdown files. You can update the permissions for this action in the Actions tab of your repository settings under Workflows Permissions. This only needs to be done once per repository. The action will not be able to modify your repository if you do not grant it the required permissions. This action does not access any other files other than .md files in your repository. For more information, see [GitHub's documentation](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#permissions).

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
        uses: sam9111/markdown-accessibility-helper@v1.0.4
```

According to this workflow file, you can run the action manually by going to the Actions tab in your repository and selecting the Markdown Accessibility Helper workflow.

By default, the action uses the [microsoft/git-base-coco](https://huggingface.co/microsoft/git-base-coco) model from HuggingFace to generate alt text and does not require any additional configuration. You can also use the Azure Computer Vision Resource to generate alt text by following the instructions below.

### With Azure Computer Vision Resource

```yaml
name: Markdown Accessibility Helper

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Markdown Accessibility
        uses: sam9111/markdown-accessibility-helper@v1.0.4
        with:
          # Azure Computer Vision Resource Key
          azure_key: ${{ secrets.AZURE_KEY }}
          # Azure Computer Vision Resource Endpoint
          azure_endpoint: ${{ secrets.AZURE_ENDPOINT }}
          # Language to use for alt text generation with Azure Computer Vision Resource (optional)
          language: 'en'|'es'|'ja'|'pt'|'zh'
```

With your Azure subscription, create a [Computer Vision resource](https://azure.microsoft.com/en-us/products/cognitive-services/vision-services) in the Azure portal to get your key and endpoint. You can use the free pricing tier (F0) which gives you 5,000 transactions free per month to try the service, and upgrade later to a paid tier if needed.

Add your Azure key and endpoint to your repository secrets.

In the with section of your workflow file, you can provide your Azure endpoint and key as secrets to access the Azure Computer Vision Resource.

You can also specify another language for alt text generation with the language parameter. The default language is English.

## Future Plans

- [ ] Use [markdownlint](https://github.com/DavidAnson/markdownlint) to check and fix other linting issues in markdown files.
- [ ] Add support for other image formats like SVG.
- [ ] Add support for other languages for alt text generation using other models.
- [ ] Follow other suggestions given in this [link](https://www.smashingmagazine.com/2021/09/improving-accessibility-of-markdown/) for accessibility improvements in markdown files.
