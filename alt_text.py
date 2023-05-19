from transformers import AutoProcessor, AutoModelForCausalLM
import requests
from PIL import Image
import re
import os
import sys
import io
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import sys


# Suggest alt text for an image using the Microsoft GIT model


def suggest_alt_text(image_url, azure_subscription_key, azure_endpoint, language):

    if azure_subscription_key and azure_endpoint:
        computervision_client = ComputerVisionClient(
            azure_endpoint, CognitiveServicesCredentials(azure_subscription_key))
        description_results = computervision_client.describe_image(
            image_url, language=language)
        if (len(description_results.captions) == 0):
            pass
        else:
            return description_results.captions[0].text

    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")
    try:
        response = requests.get(image_url, stream=True, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
        image = Image.open(io.BytesIO(response.content))
    except:
        print(f"Error: {image_url} is not a valid image URL")
        return None
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    suggested_alt_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    return suggested_alt_text

# Update all markdown files with the suggested alt text if no alt text is provided


def update_markdown_file(file_path, azure_subscription_key, azure_endpoint, language):
    with open(file_path, 'r') as f:
        content = f.read()

        # match all markdown images with empty alt text

        matches = re.findall(r'\!\[(.*?)\]\((.*?)\)(?!\(|\w)', content)

        for match in matches:
            alt_text = match[0]
            image_url = match[1]
            if not alt_text:
                suggested_alt_text = suggest_alt_text(
                    image_url, azure_subscription_key, azure_endpoint, language)
                content = content.replace(
                    f"![]({image_url})", f"![{suggested_alt_text}]({image_url})")

        # match all img tags with empty alt or title attributes or no alt or title attributes
        pattern = re.compile(r'<img.*?>', re.S)

        result = pattern.findall(content)

        for i in result:

            image_url = re.findall(r'src="(.*?)"', i)[0]

            # check if valid alt value is provided

            alt = re.findall(r'alt="(.*?)"', i)
            if alt:
                alt = alt[0]
            title = re.findall(r'title="(.*?)"', i)
            if title:
                title = title[0]

            # check if the img tag has empty alt or title attribute

            if 'alt=""' in i or 'title=""' or 'alt' not in i or 'title' not in i:

                suggested_alt_text = alt if alt else suggest_alt_text(
                    image_url, azure_subscription_key, azure_endpoint, language)

                title = title if title else suggested_alt_text
                content = content.replace(
                    f"{i}", f'<img src="{image_url}" alt="{suggested_alt_text}" title="{suggested_alt_text}">')

    with open(file_path, 'w') as f:
        f.write(content)


if __name__ == '__main__':

    language = "en"
    if len(sys.argv) > 2:
        azure_subscription_key = sys.argv[2]
        azure_endpoint = sys.argv[3]
        if len(sys.argv) > 4:
            language = sys.argv[4]

    else:
        azure_subscription_key = None
        azure_endpoint = None

    repo_path = sys.argv[1]

    for root, dirs, files in os.walk(repo_path):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                update_markdown_file(
                    filename, azure_subscription_key, azure_endpoint, language)
