# Then vs Now Image Dataset Extractor

This script extracts images from the AOL "Then vs Now" article, downloads them, categorizes into past/current, and geocodes locations.

## Setup

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. Create venv: `uv venv`

3. Install packages: `source .venv/bin/activate && uv pip install requests beautifulsoup4 pillow geopy`

## Usage

1. Get the page content: Copy the output from the fetch_webpage tool into `page_content.txt`

2. Run: `source .venv/bin/activate && python parse_data.py`

3. Output: `dataset.json` with metadata, `images/` folder with downloaded images.

## Dataset Format

JSON array of objects:

- `title`: section title
- `location`: extracted location
- `date`: year
- `image`: path to image
- `category`: 'past' or 'current'
- `description`: text
- `geolocation`: {lat, lon, address} or null

For split images, it crops top as past, bottom as current.