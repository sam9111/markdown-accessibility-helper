from transformers import AutoProcessor, AutoModelForCausalLM
import requests
from PIL import Image
import re
import os
import sys

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

from PIL import Image
import sys


# Suggest alt text for an image using the Microsoft GIT model


def suggest_alt_text(image_url, azure_subscription_key, azure_endpoint):

    if azure_subscription_key and azure_endpoint:
        computervision_client = ComputerVisionClient(
            azure_endpoint, CognitiveServicesCredentials(azure_subscription_key))
    description_results = computervision_client.describe_image(image_url)
    if (len(description_results.captions) == 0):
        pass
    else:
        return description_results.captions[0].text

    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")
    image = Image.open(requests.get(image_url, stream=True).raw)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    suggested_alt_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    return suggested_alt_text

# Update all markdown files with the suggested alt text if no alt text is provided


def update_markdown_file(file_path, azure_subscription_key, azure_endpoint):
    with open(file_path, 'r') as f:
        content = f.read()
        matches = re.findall(r'\!\[(.*?)\]\((.*?)\)(?!\(|\w)', content)
        for match in matches:
            alt_text = match[0]
            image_url = match[1]
            if not alt_text:
                suggested_alt_text = suggest_alt_text(
                    image_url, azure_subscription_key, azure_endpoint)
                content = content.replace(
                    f"![]({image_url})", f"![{suggested_alt_text}]({image_url})")
    with open(file_path, 'w') as f:
        f.write(content)


if __name__ == '__main__':

    if len(sys.argv) > 2:
        azure_subscription_key = sys.argv[2]
        azure_endpoint = sys.argv[3]
    else:
        azure_subscription_key = None
        azure_endpoint = None

    repo = os.environ['GITHUB_REPOSITORY']
    repo_name = repo.split('/')[1]
    clone_url = f'https://github.com/{repo}.git'

    branch = "main"

    if os.environ['GITHUB_HEAD_REF']:
        branch = os.environ['GITHUB_HEAD_REF']

    os.system(f"git clone --depth=1 --branch={branch} {clone_url} repo")
    os.chdir('repo')

    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            update_markdown_file(
                filename, azure_subscription_key, azure_endpoint)
            os.system(f"git add {filename}")

    # Commit and push

    github_username = os.environ['GITHUB_ACTOR']
    os.system(
        f'git config --global user.email "{github_username}@users.noreply.github.com"')
    os.system(f'git config --global user.name "{github_username}"')
    os.system('git commit -m "Suggest alt text for inline images"')
    token = sys.argv[1]
    os.system(
        f"git push {clone_url.replace('https://',f'https://{github_username}:{token}@')} {branch}")
