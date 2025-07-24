### How to Download Files From a URL?

**Description**: Download files from web URLs and save them to local storage with robust error handling and progress tracking. This scripts supports downloading various file types including PDFs, images, documents, datasets, archives, and media files from remote servers, APIs, or web resources.

**Use Cases**:
- Download research papers, PDFs, and academic documents from repositories like arXiv, ResearchGate, or institutional websites
- Fetch images, photos, and graphics from web sources for data analysis or machine learning projects
- Retrieve datasets, CSV files, JSON data, and API responses for data processing workflows
- Download software packages, archives (ZIP, TAR), installers, and binary files
- Save web content, HTML pages, XML feeds, and text documents for offline processing
- Fetch media files including audio, video, and multimedia content for analysis
- Download configuration files, templates, and resources from remote repositories
- Retrieve backup files, exports, and data dumps from cloud storage or web services

```
import os
import requests

# The URL of the file to download, for example https://arxiv.org/pdf/1706.03762
url = "https://arxiv.org/pdf/1706.03762"

# The path to save the downloaded file, provide a valid path with file name and extension such as "workspace/dog.png"
save_path = "workspace/target_paper.pdf"

os.makedirs(os.path.dirname(save_path), exist_ok=True)

# set the headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# download the file
response = requests.get(url, headers=headers, stream=True, timeout=50)
response.raise_for_status()
content_type = response.headers.get('content-type', 'unknown')

# write the file to the specified path
with open(save_path, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            file.write(chunk)

# get the file size
file_size = os.path.getsize(save_path)
file_size_mb = file_size / (1024 * 1024)

# print the result
print("File downloaded successfully!")
print(f"URL: {url}")
print(f"Saved to: {save_path}")
print(f"File size: {file_size} bytes ({file_size_mb:.2f} MB)")
print(f"Content type: {content_type}")
```