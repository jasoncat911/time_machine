import json
import os
from PIL import Image

# Load dataset
with open('dataset.json', 'r') as f:
    data = json.load(f)

# Create split_images directory
os.makedirs('split_images', exist_ok=True)

for item in data:
    title = item['title'].replace('/', '_').replace(' ', '_')[:50]
    img_path = f"images/{title}.jpg"
    
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path)
            width, height = img.size
            
            # Assume vertical split, top half past, bottom half current
            past_img = img.crop((0, 0, width, height // 2))
            current_img = img.crop((0, height // 2, width, height))
            
            past_path = f"split_images/{title}_past.jpg"
            current_path = f"split_images/{title}_current.jpg"
            
            past_img.save(past_path)
            current_img.save(current_path)
            
            # Update dataset with paths
            item['past_image_path'] = past_path
            item['current_image_path'] = current_path
            
            print(f"Split {img_path}")
        except Exception as e:
            print(f"Failed to split {img_path}: {e}")
    else:
        print(f"Image not found: {img_path}")

# Save updated dataset
with open('dataset.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Splitting complete")