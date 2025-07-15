### How to Fetch and Parse the Content of A Web Page Given a URL?

Get and parse any given webpage, extracting text content, images, and links.

```python
import requests
from bs4 import BeautifulSoup

# The URL of the webpage to get and parse, for example: "https://www.python.org", "https://arxiv.org/abs/2305.13677" and "https://amazon.com", etc.
url = "https://www.poetryfoundation.org/poems/46462/father-son-and-holy-ghost"

# The maximum number of links to extract
max_num_links = 10

# The maximum number of images to extract
max_num_images = 5

# The maximum number of text to extract
max_num_text = 3000

# The headers to use for the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Get the response from the URL
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()

# Parse the response
soup = BeautifulSoup(response.content, 'html.parser')

print(f"Webpage: {url}")
print(f"Status: {response.status_code}")
print("=" * 50)

title = soup.find('title')
if title:
    print(f"Title: {title.get_text().strip()}")

meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc and meta_desc.get('content'):
    print(f"Description: {meta_desc.get('content')}")

for script in soup(["script", "style"]):
    script.decompose()

text = soup.get_text()

lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = ' '.join(chunk for chunk in chunks if chunk)

if text:
    if len(text) > max_num_text:
        text = text[:max_num_text] + "..."
    print("Content:")
    print(repr(text))

# Extract links
links = soup.find_all('a', href=True)
if links:
    print(f"\nLinks found ({len(links)}):")
    for i, link in enumerate(links[:max_num_links]):
        href = link.get('href')
        link_text = link.get_text().strip()
        if href:
            # Make relative URLs absolute
            if href.startswith('/'):
                from urllib.parse import urljoin
                href = urljoin(url, href)
            print(f"  {i+1}. {link_text[:50]}... -> {href}")
    
    if len(links) > max_num_links:
        print(f"  ... and {len(links) - max_num_links} more links") # Print the number of links that were not printed

images = soup.find_all('img', src=True)
if images:
    print(f"\nImages found ({len(images)}):")
    for i, img in enumerate(images[:max_num_images]):
        src = img.get('src')
        alt = img.get('alt', 'No alt text')
        if src:
            # Make relative URLs absolute
            if src.startswith('/'):
                from urllib.parse import urljoin
                src = urljoin(url, src)
            print(f"  {i+1}. {alt[:30]}... -> {src}")
    
    if len(images) > max_num_images:
        print(f"  ... and {len(images) - max_num_images} more images")
```

### If needed, How to get an archived (old) version of a webpage?

Get an archived version of a webpage from the Wayback Machine.

Not all websites have snapshots available for every past moment. If no archived version is found, try to access the current website and look for historical information, or search google to find answers about the website's past.

```python
import os
import requests
from bs4 import BeautifulSoup

# The URL of the webpage to get and parse, for example: "https://imdb.com"
url = "http://www.feedmag.com/"

# The date of the archived version to get, for example: "20210101" or "2021-01-01"
date = "1996-11-04"

# Check if the webpage is available in the Wayback Machine
api_url = f"https://archive.org/wayback/available?url={url}&timestamp={date}"
avail_response = requests.get(api_url, timeout=20)

if avail_response.status_code == 200:
    avail_data = avail_response.json()
    
    if "archived_snapshots" in avail_data and "closest" in avail_data["archived_snapshots"]:
        closest = avail_data["archived_snapshots"]["closest"]
        if closest["available"]:
            archive_url = closest["url"]
            archive_date = closest["timestamp"]
        else:
            print(f"No archived version found for {url}")
    else:
        print(f"No archived version found for {url}")
else:
    print(f"Error checking archive availability for {url}")

# Get the archived version of the webpage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(archive_url, headers=headers, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.content, 'html.parser')

print(f"Archived webpage: {url}")
print(f"Archive date: {archive_date[:4]}-{archive_date[4:6]}-{archive_date[6:8]} {archive_date[8:10]}:{archive_date[10:12]}:{archive_date[12:14]}")
print(f"Archive URL: {archive_url}")

# Get the title of the webpage
title = soup.find('title')
if title:
    print(f"Title: {title.get_text().strip()}")

# Get the description of the webpage
meta_desc = soup.find('meta', attrs={'name': 'description'})
if meta_desc and meta_desc.get('content'):
    print(f"Description: {meta_desc.get('content')}")

# Remove the script and style tags
for element in soup(["script", "style"]):
    element.decompose()

# Remove the wayback tags
for element in soup.find_all(class_=lambda x: x and 'wayback' in x.lower()):
    element.decompose()

# Get the text of the webpage
text = soup.get_text()
lines = (line.strip() for line in text.splitlines())
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
text = ' '.join(chunk for chunk in chunks if chunk)

# Print the text of the webpage
if text:
    if len(text) > 3000: # Limit the text to 3000 characters, change to get more or less text
        text = text[:3000] + "..."
    print("Content:")
    print(text)

print("Note: This is an archived version from the Wayback Machine")
```