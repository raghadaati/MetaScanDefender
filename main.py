import argparse
import requests

def scan_file(api_key, file_path):
    url = 'https://api.metadefender.com/v4/file'
    headers = {
        'apikey': api_key
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)
        
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def scan_hash(api_key, hash_value):
    url = f'https://api.metadefender.com/v4/hash/{hash_value}'
    headers = {
        'apikey': api_key
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def scan_url(api_key, url):
    url = 'https://api.metadefender.com/v4/url'
    headers = {
        'apikey': api_key
    }
    params = {
        'url': url
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_scan_result(api_key, data_id):
    url = f'https://api.metadefender.com/v4/file/{data_id}'
    headers = {
        'apikey': api_key
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def main():
    print("""
provides functions to interact with the MetaDefender API for scanning files and URLs for potential threats.
              
               
-k or --api-key: The MetaDefender API key required for authentication. This argument allows users to specify their API key directly from the command line when running the script.
-f or --file-path: The path to the file to scan. Users can specify the local file path to be scanned as an optional argument from the command line.
-H or --hash: The hash value to scan. Users can provide the hash value of a file they want to retrieve the scan result for as an optional argument from the command line.
-u or --url: The URL to scan. Users can provide the URL they want to scan for potential threats as an optional argument from the command line.
              """)
    parser = argparse.ArgumentParser(description='Meta Defender API Scanner')
    parser.add_argument('-k', '--api-key', required=True, help='Meta Defender API key')
    parser.add_argument('-f', '--file-path', help='Path to the file to scan')
    parser.add_argument('-H', '--hash', help='Hash value to scan')
    parser.add_argument('-u', '--url', help='URL to scan')

    args = parser.parse_args()
    api_key = args.api_key

    if args.file_path:
        file_path = args.file_path

        # Scan the file
        scan_data = scan_file(api_key, file_path)
        if scan_data is not None:
            data_id = scan_data['data_id']
            print(f"Scan started. Data ID: {data_id}")
        else:
            print("Error occurred while scanning the file.")
    elif args.hash:
        hash_value = args.hash

        # Scan the hash
        scan_data = scan_hash(api_key, hash_value)
        if scan_data is not None:
            data_id = scan_data['data_id']
            print(f"Scan started. Data ID: {data_id}")
        else:
            print("Error occurred while scanning the hash.")
    elif args.url:
        url = args.url

        # Scan the URL
        scan_data = scan_url(api_key, url)
        if scan_data is not None:
            data_id = scan_data['data_id']
            print(f"Scan started. Data ID: {data_id}")
        else:
            print("Error occurred while scanning the URL.")
    else:
        print("Please provide either a file path, hash value, or URL to scan.")

    # Get the scan result
    if scan_data is not None:
        scan_result = get_scan_result(api_key, data_id)
        if scan_result is not None:
            print(scan_result)
        else:
            print("Error occurred while fetching the scan result.")

if __name__ == '__main__':
    main()
