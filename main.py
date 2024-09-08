import json
import re
from datetime import datetime
import zipfile

with open('./articles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


extracted_data = [
    {
        'title': post.get('title'),
        'contentMarkdown': post.get('contentMarkdown'),
        'dateAdded': post.get('dateAdded')
    }
    for post in data['posts']
]


def format_date(date_str):
    try:
        date_object = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return date_object.strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # If parsing fails, return original

def clean_content_markdown(content):
    cleaned_content = content.replace('\\n', '\n').replace('\\r', '')
    return cleaned_content

markdown_data = []
for post in extracted_data:
    cleaned_content = clean_content_markdown(post['contentMarkdown'])
    formatted_date = format_date(post['dateAdded'])
    markdown_content = f"""title: {post['title']}
published_date: {formatted_date}
---------------------------------
{cleaned_content}
"""
    markdown_data.append(markdown_content)


zip_output_path = './markdown_posts.zip'
with zipfile.ZipFile(zip_output_path, 'w') as zipf:
    for idx, markdown_content in enumerate(markdown_data, 1):
        file_name = f'post_{idx}.md'
        zipf.writestr(file_name, markdown_content)

zip_output_path