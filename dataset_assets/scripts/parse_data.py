import re
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from PIL import Image
from io import BytesIO
import os

os.makedirs('images', exist_ok=True)

# Read the page content
with open('page_content.txt', 'r') as f:
    content = f.read()

# Split into sections
sections = re.split(r'## ', content)[1:]  # Skip the first part

data = []
geolocator = Nominatim(user_agent="then_vs_now_scraper")

for section in sections:
    lines = section.split('\n')
    title = lines[0].strip()
    
    # Find image URL
    img_match = re.search(r'!\[.*?\]\((.*?)\)', section)
    if img_match:
        img_url = img_match.group(1)
        
        # Description
        desc = re.sub(r'!\[.*?\]\(.*?\)', '', section).strip()
        
        # Extract location from title
        location_match = re.match(r'(.+?)(?:\s*\d{4}|\s*vs|\s*before|\s*after|\s*–|\s*-)', title)
        location = location_match.group(1).strip() if location_match else title
        
        # Extract dates
        years = re.findall(r'\b\d{4}\b', title + ' ' + desc)
        past_date = years[0] if years else None
        current_date = years[1] if len(years) > 1 else None
        
        # Geolocation
        try:
            location_info = geolocator.geocode(location, timeout=10)
            if location_info:
                geolocation = {
                    'lat': location_info.latitude,
                    'lon': location_info.longitude,
                    'address': location_info.address
                }
            else:
                geolocation = None
        except GeocoderTimedOut:
            geolocation = None
        
        # Download and process image
        if img_url:
            try:
                img_response = requests.get(img_url)
                img = Image.open(BytesIO(img_response.content))
                width, height = img.size
                if 'split' in desc.lower() or 'top' in desc.lower() or 'bottom' in desc.lower() or height > width * 1.5:
                    top = img.crop((0, 0, width, height//2))
                    bottom = img.crop((0, height//2, width, height))
                    past_img = f"images/{len(data)}_past.jpg"
                    current_img = f"images/{len(data)}_current.jpg"
                    top.save(past_img)
                    bottom.save(current_img)
                    data.append({
                        'title': title,
                        'location': location,
                        'date': past_date,
                        'image': past_img,
                        'category': 'past',
                        'description': desc,
                        'geolocation': geolocation
                    })
                    data.append({
                        'title': title,
                        'location': location,
                        'date': current_date,
                        'image': current_img,
                        'category': 'current',
                        'description': desc,
                        'geolocation': geolocation
                    })
                else:
                    img_name = f"images/{len(data)}.jpg"
                    img.save(img_name)
                    category = 'past' if past_date and not current_date else 'current'
                    data.append({
                        'title': title,
                        'location': location,
                        'date': past_date or current_date,
                        'image': img_name,
                        'category': category,
                        'description': desc,
                        'geolocation': geolocation
                    })
            except Exception as e:
                print(f"Error processing {img_url}: {e}")

# Save to JSON
with open('dataset.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Dataset created with", len(data), "entries")