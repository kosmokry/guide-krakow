import csv
import os
import re
from urllib.parse import urlparse, parse_qs

import gdown

OUT_DIR = "images"
CSV_FILE = "images.csv"

os.makedirs(OUT_DIR, exist_ok=True)

def file_id_from_url(url: str) -> str:
    # supports:
    # https://drive.google.com/open?id=FILE_ID
    # https://drive.google.com/file/d/FILE_ID/view?...
    if "open?id=" in url:
        parsed = urlparse(url)
        return parse_qs(parsed.query)["id"][0]
    m = re.search(r"/file/d/([^/]+)", url)
    if m:
        return m.group(1)
    raise ValueError(f"Can't parse file id: {url}")

with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = row["slug"].strip()
        url = row["drive_url"].strip()
        fid = file_id_from_url(url)

        out_path = os.path.join(OUT_DIR, f"{slug}")  # extension may vary
        # gdown will keep extension if possible; if not, we rename later manually
        print("Downloading:", slug)

        # fuzzy=True helps gdown handle different drive link formats
        downloaded = gdown.download(id=fid, output=out_path, quiet=False, fuzzy=True)

print("Done.")