import requests
from re import sub
import os

def download_attachement(attachement_links):
    for link in attachement_links:
        req = requests.get(link)
        if req.status_code == 200:
            filename = os.path.join(os.getcwd(), 'Attachements', sub(r'[^\w.-]', '_', link.split('/')[-1]))
            if os.path.exists(filename):
                print(f"File {filename} already exists. Skipping download.")
                continue
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    f.write(chunk)