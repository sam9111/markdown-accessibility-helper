from transformers import AutoProcessor, AutoModelForCausalLM
import requests
from PIL import Image
import re
import os


def suggest_alt_text(image_url):
    processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
    model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")
    image = Image.open(requests.get(image_url, stream=True).raw)
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    suggested_alt_text = processor.batch_decode(
        generated_ids, skip_special_tokens=True)[0]
    return suggested_alt_text

# Update all markdown files with the suggested alt text


def update_markdown_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        matches = re.findall(r'\!\[(.*?)\]\((.*?)\)(?!\(|\w)', content)
        for match in matches:
            alt_text = match[0]
            image_url = match[1]
            if not alt_text:
                suggested_alt_text = suggest_alt_text(image_url)
                content = content.replace(
                    f"![]({image_url})", f"![{suggested_alt_text}]({image_url})")
    with open(file_path, 'w') as f:
        f.write(content)
