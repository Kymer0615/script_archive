import xml.etree.ElementTree as ET
import requests
import subprocess
import argparse
from os import makedirs
from concurrent.futures import ThreadPoolExecutor

def download_file(url, destination):
    """Download a file from a web URL to a local destination."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks.
                    f.write(chunk)
                    f.flush()
        print(f"File downloaded successfully: {destination}")
    except requests.RequestException as e:
        print(url)
        print(f"An error occurred: {e}")

def extract_strings_from_plist(plist_path):
    """ Extract and print all <string> tags from a .plist file. """
    # Load the XML file
    tree = ET.parse(plist_path)
    root = tree.getroot()

    # Extract all <string> elements
    string_elements = root.findall('.//string')

    # List to hold all strings
    all_strings = []

    # Extract text from each <string> element
    for elem in string_elements:
        if elem.text is not None:
            if "http" in elem.text:
                URL = elem.text
                URL.replace("&amp;", "&")
                all_strings.append(URL)

    return all_strings

def download_files(urls, directory):
    """Download multiple files to a specified directory using multithreading."""
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_file, url, f"{directory}/{idx}.gif")
                   for idx, url in enumerate(urls)]
        # Wait for all futures to complete
        for future in futures:
            future.result()

# Main execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download WeChat stickers.')
    parser.add_argument('-dir', '--directory', type=str, help='Specify the download directory.')
    args = parser.parse_args()

    download_directory = args.directory if args.directory else None

    # Check if the directory is specified, if not ask for user input
    if download_directory is None:
        response = input("No directory specified. Would you like to specify one? (y/n): ").strip().lower()
        if response == 'y':
            download_directory = input("Please enter the download directory: ")
        else:
            # Set default directory if the user chooses not to specify
            download_directory = './wechat_stickers/'

    # Path to the shell script
    script_path = './script/wechat_sticker_download.sh'

    # Run the shell script
    result = subprocess.run([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Ensure the directory exists
    makedirs(args.directory, exist_ok=True)
    plist_path = './temp/fav.archive.plist'
    
    # Extract URLs from the plist
    url_list = extract_strings_from_plist(plist_path)
    
    # Download all files concurrently
    download_files(url_list, args.directory)