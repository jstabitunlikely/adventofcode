import requests
import os
import time
import sh

def fetch_input(year, day, cache_dir='cache'):
    base_url = 'https://adventofcode.com/{}/day/{}/input'
    git = sh.Command('git')

    root = git('rev-parse --show-toplevel'.split()).strip()
    filename = f'{root}/{cache_dir}/{year}_{day}.txt'

    # Check if cached file exists and is not too old
    if os.path.exists(filename):
        file_mtime = os.path.getmtime(filename)
        if time.time() - file_mtime < 86400:  # Cache for 24 hours
            with open(filename, 'r') as f:
                return(f.read())

    # Create the request
    url = base_url.format(year, day)

    headers = {
        'Cookie': f"session={os.getenv('AOC_SESSION_COOKIE')}"
    }

    # Send the request and check the response
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Create cache directory if it doesn't exist
    os.makedirs(cache_dir, exist_ok=True)

    # Write response to cache file
    with open(filename, 'w') as f:
        f.write(response.text.strip())

    return response.text