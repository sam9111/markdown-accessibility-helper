import os
import re
import sys


def has_image_without_alt(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

        # Match all markdown images with empty alt text
        matches = re.findall(r'\!\[(.*?)\]\((.*?)\)(?!\(|\w)', content)
        for match in matches:
            alt_text = match[0]
            if not alt_text:
                return True

        # Match all img tags with empty alt attribute
        pattern = re.compile(r'<img.*?>', re.S)
        result = pattern.findall(content)

        for i in result:
            alt = re.findall(r'alt="(.*?)"', i)
            if not alt:
                return True

    return False


if __name__ == '__main__':

    md_files_without_alt = []

    for root, dirs, files in os.walk('.'):
        print(f'Checking {root}')
        for filename in files:
            print(f'Checking {filename}')
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                print(f'Checking {file_path}')
                if has_image_without_alt(file_path):
                    md_files_without_alt.append(file_path)

    print(md_files_without_alt)
    if md_files_without_alt:
        print("The following Markdown files contain images without alt text:")
        for file_path in md_files_without_alt:
            print(file_path)

        result = 'true'
    else:
        print("All Markdown files have alt text for their images.")
        result = 'false'

    with open(os.environ['GITHUB_OUTPUT'], 'w') as output_file:
        output_file.write(f'result={result}\n')
