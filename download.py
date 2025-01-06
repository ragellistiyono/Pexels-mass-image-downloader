import os
import sys
import json
import urllib.request
import zipfile
from urllib.parse import quote
from datetime import datetime

def parse_args():
    """Parse command line arguments"""
    if len(sys.argv) < 3:
        print("Usage: python download.py [query] [number_of_photos] [destination_path]")
        sys.exit(1)
        
    query = sys.argv[1]
    try:
        num_photos = int(sys.argv[2])
    except ValueError:
        print("Error: number_of_photos must be an integer")
        sys.exit(1)
        
    dest_path = os.getcwd() if len(sys.argv) < 4 else sys.argv[3]
    
    return query, num_photos, dest_path

# Load API key from api.key file
API_KEY = None
try:
    with open('api.key', 'r') as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print("Error: api.key file not found. Please create an api.key file with your Pexels API key.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading api.key: {e}")
    sys.exit(1)

class PexelsAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1/"
        self.headers = {
            "Authorization": self.api_key,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.current_page = 1
        self.total_results = 0
        self.photos = []
    
    def search(self, query, per_page=15):
        url = f"{self.base_url}search?query={quote(query)}&per_page={per_page}&page={self.current_page}"
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            self.total_results = data['total_results']
            self.photos = data['photos']
        return self.photos
    
    def search_next_page(self):
        self.current_page += 1
        return self.search(self.query, self.per_page)
    
    def get_entries(self):
        for photo in self.photos:
            yield Photo(photo)

class Photo:
    def __init__(self, data):
        self.id = data['id']
        self.url = data['url']
        self.photographer = data['photographer']
        self.description = data.get('alt', '')
        self.original = data['src']['original']
        self.large2x = data['src']['large2x']
        self.large = data['src']['large']
        self.medium = data['src']['medium']
        self.small = data['src']['small']
        self.compressed = data['src']['tiny']
        self.extension = self.original.split('.')[-1]

def download_image(url, path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.pexels.com/"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def create_zip(downloaded_files, query):
    try:
        downloads_dir = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        zip_filename = f"{timestamp}_{query.replace(' ', '_')}.zip"
        zip_path = os.path.join(downloads_dir, zip_filename)

        print(f"\nCreating zip archive: {zip_filename}")
        print(f"Progress: [{' ' * 20}] 0%", end='\r')

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_files = len(downloaded_files)
            for i, file_path in enumerate(downloaded_files):
                arcname = os.path.basename(file_path)
                zipf.write(file_path, arcname)
                progress = int((i + 1) / total_files * 20)
                percent = int((i + 1) / total_files * 100)
                print(f"Progress: [{'=' * progress}{' ' * (20 - progress)}] {percent}%", end='\r')

        print(f"\nSuccessfully created zip archive: {zip_path}")
        return zip_path

    except Exception as e:
        print(f"\nError creating zip file: {e}")
        return None

def main():
    query, total_photos, path = parse_args()
    
    # Create directory if it doesn't exist
    download_dir = os.path.join(path, query.replace(" ", "-"))
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    api = PexelsAPI(API_KEY)
    print(f"Searching for '{query}'...")
    api.search(query, per_page=min(total_photos, 80))

    if not api.photos:
        print("No photos found.")
        return

    print(f"Found {api.total_results} results. Downloading {total_photos} photos...")
    downloaded_files = []

    for i, photo in enumerate(api.get_entries()):
        if i >= total_photos:
            break

        filename = f"{i+1}.{photo.extension}"
        filepath = os.path.join(download_dir, filename)

        print(f"Downloading {i+1}/{total_photos}: {photo.original}")
        if download_image(photo.original, filepath):
            print(f"Saved to {filepath}")
            downloaded_files.append(filepath)
        else:
            print(f"Failed to download photo {i+1}")

    if downloaded_files:
        zip_path = create_zip(downloaded_files, query)
        if zip_path:
            print(f"\nAll images successfully packaged into: {zip_path}")
        else:
            print("\nFailed to create zip archive, but images were downloaded successfully.")
    else:
        print("\nNo images were downloaded, skipping zip creation.")

if __name__ == "__main__":
    main()
