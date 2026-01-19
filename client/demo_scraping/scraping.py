import requests
from bs4 import BeautifulSoup
import os
import csv
import re
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://prices.shufersal.co.il"
OUTPUT_DIR = "downloads"
METADATA_FILE = "store_locations.csv"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    store_data = []
    seen_files = set()
    page = 1
    total_files = 0
    
    while True:
        print(f"Fetching page {page}...")
        url = f"{BASE_URL}/?page={page}"
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr')
        
        # Filter for data rows to check if we should continue
        # We look for rows that have the download link
        current_page_data_rows = []
        for row in rows:
            if row.find('a', href=True) and "לחץ להורדה" in row.get_text():
                current_page_data_rows.append(row)
        
        if not current_page_data_rows:
            print(f"No data found on page {page}. Stopping.")
            break
            
        print(f"Found {len(current_page_data_rows)} files on page {page}.")
        
        for row in current_page_data_rows:
            cells = row.find_all('td')
            
            # Look for the download link
            download_link_tag = row.find('a', href=True)
            file_url = download_link_tag['href']
            if not file_url.startswith('http'):
                file_url = BASE_URL + file_url if file_url.startswith('/') else BASE_URL + '/' + file_url

            # Extract Store Name
            store_id = None
            store_location = None
            filename_base = None
            file_ext = "gz"

            for cell in cells:
                text = cell.get_text(strip=True)
                
                if not store_id and re.match(r'^\d+\s*-\s*.+', text):
                    parts = text.split('-', 1)
                    if len(parts) == 2:
                        store_id = parts[0].strip()
                        store_location = parts[1].strip()
                
                if not filename_base and (text.startswith("Price") or text.startswith("Promo") or text.startswith("Store")):
                    filename_base = text
                
                if text.upper() in ["GZ", "XML"]:
                    file_ext = text.lower()

            # If store_id is not found in text, try to extract from filename if available
            if not store_id and filename_base:
                # Filename format: Price7290027600007-001-202512072000
                # The store ID is the middle part
                match = re.search(r'-(\d{3})-', filename_base)
                if match:
                    store_id = str(int(match.group(1))) # Remove leading zeros
                    store_location = "Unknown" # We don't have location

            if store_id:
                # Construct filename
                if filename_base:
                    filename = f"{filename_base}.{file_ext}"
                else:
                    filename = file_url.split('/')[-1]
                    if not filename.endswith(f".{file_ext}"):
                        filename += f".{file_ext}"

                save_path = os.path.join(OUTPUT_DIR, filename)
                
                if filename in seen_files:
                    continue
                seen_files.add(filename)

                # print(f"Found Store {store_id}: {store_location} -> {filename}")
                
                # Download the file
                try:
                    # Check if file already exists to skip redownload (optional, but good for restart)
                    if not os.path.exists(save_path):
                        with requests.get(file_url, headers=headers, stream=True, verify=False) as r:
                            r.raise_for_status()
                            with open(save_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    f.write(chunk)
                    
                    store_data.append({
                        'store_id': store_id,
                        'location': store_location,
                        'filename': filename
                    })
                    total_files += 1
                except Exception as e:
                    print(f"Failed to download {filename}: {e}")
        
        page += 1

    # Save metadata to CSV
    if store_data:
        with open(METADATA_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['store_id', 'location', 'filename'])
            writer.writeheader()
            writer.writerows(store_data)
        print(f"Successfully processed {len(store_data)} files. Metadata saved to {METADATA_FILE}.")
    else:
        print("No store data found.")

if __name__ == "__main__":
    main()
