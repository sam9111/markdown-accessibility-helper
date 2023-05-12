# Markdown Accessibility Helper

A GitHub action that helps improve the accessibility of Markdown files in your repository by automatically adding alternative text to images that do not have it. This action uses the [microsoft/git-base-coco](https://huggingface.co/microsoft/git-base-coco) model from HuggingFace to generate alt text, or the describe image ability of [Azure Computer Vision Resource](https://azure.microsoft.com/en-us/products/cognitive-services/vision-services) can also be used.

## Features

- Automatically adds alternative text to images that do not have it.
- Uses a state-of-the-art machine learning model to generate descriptive alt text.
- Supports both PNG and JPEG image formats.
- Supports both local and remote images.
