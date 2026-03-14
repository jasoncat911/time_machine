import json
import requests
import os

# Load dataset
with open('dataset.json', 'r') as f:
    data = json.load(f)

# Create images directory
os.makedirs('images', exist_ok=True)

for item in data:
    img_url = item['image_url']
    title = item['title'].replace('/', '_').replace(' ', '_')[:50]  # Sanitize filename
    filename = f"images/{title}.jpg"
    
    try:
        response = requests.get(img_url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")

print("Download complete")