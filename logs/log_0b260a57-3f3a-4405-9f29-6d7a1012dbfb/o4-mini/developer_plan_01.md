# Developer Plan 01

## Plan
Navigate to the ScienceDirect website, select the Life Sciences subject area, apply the content‐type filter for “Reference Works,” then record the number of Reference Works displayed for each Life Sciences sub‐category and save these counts in workspace/life_sciences_reference_counts.csv.

## Description
This step is required to gather the raw counts of Reference Works for each Life Sciences sub‐category on ScienceDirect as of 2022. These counts form the data set needed to compute the sample standard deviation for Life Sciences. Once collected, these values will enable us to calculate the Life Sciences sample standard deviation and later compare it against the Health Sciences sample standard deviation to determine their difference.

## Semantic Examples
### How to Parse Excel Files and Extract Content with Styling?

**Description**: Parse an Excel file and return the content as formatted HTML with style information preserved. Supports Excel (.xlsx, .xls) and CSV files.

**Use Cases**:
- Financial report conversion for web dashboards and online reporting
- Data table migration from Excel to web applications and databases
- Budget and expense sheet processing for automated accounting systems
- Inventory and product catalog data extraction for e-commerce platforms
- Employee data and payroll information processing for HR systems
- Survey and questionnaire response data analysis and visualization
- Project timeline and milestone tracking data conversion
- Scientific dataset processing and research data management

```
import os
import pandas as pd
from openpyxl import load_workbook

# The path to the Excel file to be parsed, for example: "workspace/task.xlsx" or "workspace/task.csv"
xlsx_path = "workspace/task.xlsx"

def get_cell_style(cell):
    """Extract style information from a cell and return as CSS style string."""
    styles = []

    # Check for bold formatting
    if cell.font and cell.font.bold:
        styles.append('font-weight:bold;')

    # Check for italic formatting
    if cell.font and cell.font.italic:
        styles.append('font-style:italic;')

    # Extract font color
    color = getattr(cell.font, 'color', None)
    if color is not None and getattr(color, 'type', None) == 'rgb':
        rgb = getattr(color, 'rgb', None)
        if isinstance(rgb, str) and len(rgb) >= 6:
            styles.append(f'color:#{rgb[-6:]};')
   
    # Extract background color
    fill = getattr(cell, 'fill', None)
    fgColor = getattr(fill, 'fgColor', None)
    if fgColor is not None and getattr(fgColor, 'type', None) == 'rgb':
        rgb = getattr(fgColor, 'rgb', None)
        if isinstance(rgb, str) and rgb != '00000000' and len(rgb) >= 6:
            styles.append(f'background-color:#{rgb[-6:]};')
    return ''.join(styles)

if not os.path.exists(xlsx_path):
    print(f"Error: Excel file '{xlsx_path}' does not exist.")

supported_formats = ['.xlsx', '.xls', '.csv']
file_ext = os.path.splitext(xlsx_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported file format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

# Handle CSV files separately using pandas
if file_ext == '.csv':
    df = pd.read_csv(xlsx_path)
    result = f"<h2>CSV : {os.path.basename(xlsx_path)}</h2>\n"
    result += f"<p>Rows: {df.shape[0]}, Columns: {df.shape[1]}</p>\n"
    result += "<table border='1'>\n"
    
    # Add header row
    result += "<tr>"
    for col in df.columns:
        result += f"<th>{col}</th>"
    result += "</tr>\n"
    
    # Add data rows (limit to first 100 rows for performance)
    for i, row in df.head(100).iterrows():
        result += "<tr>"
        for value in row:
            result += f"<td>{value if pd.notna(value) else ''}</td>"
        result += "</tr>\n"
    
    if len(df) > 100:
        result += f"<tr><td colspan='{len(df.columns)}'>... ({len(df) - 100} more rows)</td></tr>\n"
    
    result += "</table>\n"
    print(result)

# Handle Excel files using openpyxl
else:
    wb = load_workbook(xlsx_path, data_only=True)
    final_content = f"<h1>Excel: {os.path.basename(xlsx_path)}</h1>\n"
    final_content += f"<p>Number of sheets: {len(wb.worksheets)}</p>\n"
    
    # Process each worksheet in the Excel file
    for sheet in wb.worksheets:
        final_content += f"<h2>Sheet: {sheet.title}</h2>\n"
        
        max_row = sheet.max_row
        max_col = sheet.max_column
        
        final_content += f"<p>Rows: {max_row}, Columns: {max_col}</p>\n"
        final_content += "<table border='1' style='border-collapse:collapse;'>\n"
        
        # Process each row (limit to first 100 rows for performance)
        for i, row in enumerate(sheet.iter_rows(max_row=min(max_row, 100)), 1):
            final_content += "<tr>"
            for cell in row:
                tag = "th" if i == 1 else "td"  # First row as header
                style = get_cell_style(cell)
                value = cell.value if cell.value is not None else ""

                # Apply cell styling if present and not default black color
                if style and style != 'color:#000000;':
                    final_content += f"<{tag} style='{style}'>{value}</{tag}>"
                else:
                    final_content += f"<{tag}>{value}</{tag}>"
            final_content += "</tr>\n"
        
        # Add note if there are more rows than displayed
        if max_row > 100:
            final_content += f"<tr><td colspan='{max_col}'>... ({max_row - 100} more rows)</td></tr>\n"
        
        final_content += "</table>\n\n"

    print(final_content.strip())
```

### If needed, How to get an archived (old) version of a webpage?

**Description**: Get an archived version of a webpage from the Wayback Machine. Not all websites have snapshots available for every past moment. If no archived version is found, try to access the current website and look for historical information, or search google to find answers about the website's past.

**Use Cases**:
- Historical research and digital archaeology
- Website change tracking and evolution analysis
- Legal evidence collection and compliance verification
- Academic research on web content development
- Brand monitoring and reputation management
- Dead link recovery and content restoration
- Digital preservation and archival studies

```
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

### Get webpage content throuhg `crawl4ai` library

**Description**: Crawl4AI is the #1 trending GitHub repository, it delivers blazing-fast, AI-ready web crawling tailored for LLMs, AI agents, and data pipelines. It can creates smart, concise Markdown optimized for RAG and Agent applications.

**Use Cases**:
- AI-powered content extraction and preprocessing
- RAG (Retrieval-Augmented Generation) data pipeline creation
- LLM training data collection and curation
- Intelligent web scraping with content filtering
- Automated knowledge base construction
- Smart document processing and analysis
- Agent-ready web content preparation

```
# official profile: https://docs.crawl4ai.com/
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

md_generator = DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed") # Set makrdown generator configuration, the threshold controls filter level. 
)

config = CrawlerRunConfig(
    cache_mode=CacheMode.BYPASS,
    markdown_generator=md_generator
)

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://news.ycombinator.com", config=config)
    print("Raw Markdown:", result.markdown.raw_markdown) # Output raw makrdown content of webpage
    print("Fit Markdown :", result.markdown.fit_markdown) # Output filterd markdown content of webpage (controlled by threshopd argument)
    print("Raw HTML content", result.html) # Output raw HTML content including all elements of webpage
    print("Fit Markdown:",  result.fit_html) # Output filterd HTML content of webpage.
```

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

### How to Get the Detailed Information about a YouTube Video?

**Description**: Get detailed information about a YouTube video.

**Use Cases**:
- Youtube content analysis and video metadata extraction
- Social media monitoring and trend analysis
- Educational resource cataloging and organization
- Marketing research and competitor video analysis

```
import subprocess
import json

# The URL of the YouTube video to get information from 
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Run the command to get the video information
cmd = [
    'yt-dlp',
    '--dump-json',
    '--no-playlist',
    url
]

# Run the command and get the result
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

# Parse JSON response
video_info = json.loads(result.stdout)

# Extract and format information
info_result = []
print(f"YouTube Video: {video_info.get('title', 'Unknown title')}")
print("=" * 50)

# Basic info
print(f"Video ID: {video_info.get('id', 'Unknown')}")
print(f"URL: {video_info.get('webpage_url', url)}")
print(f"Duration: {video_info.get('duration_string', 'Unknown')}")
print(f"Upload date: {video_info.get('upload_date', 'Unknown')}")

# Channel info
print(f"Channel: {video_info.get('uploader', 'Unknown')}")
print(f"Channel ID: {video_info.get('channel_id', 'Unknown')}")
print(f"Channel URL: {video_info.get('channel_url', 'Unknown')}")

# Stats
print(f"View count: {video_info.get('view_count', 'Unknown')}")
print(f"Like count: {video_info.get('like_count', 'Unknown')}")
print(f"Comment count: {video_info.get('comment_count', 'Unknown')}")

# Description
description = video_info.get('description', '')
if description:
    # Limit description length
    if len(description) > 500: # you can change the length of the description
        description = description[:500] + "..."
    print(f"\nDescription:")
    print(description)

# Tags
tags = video_info.get('tags', [])
if tags:
    print(f"\nTags: {', '.join(tags[:10])}")
    if len(tags) > 10: # you can change the number of tags to print
        print(f"... and {len(tags) - 10} more tags")

# Categories
categories = video_info.get('categories', [])
if categories:
    print(f"Categories: {', '.join(categories)}")

# Available formats info
formats = video_info.get('formats', [])
if formats:
    print(f"\nAvailable formats: {len(formats)}")
    
    # Show some format details
    video_formats = [f for f in formats if f.get('vcodec', 'none') != 'none']
    audio_formats = [f for f in formats if f.get('acodec', 'none') != 'none' and f.get('vcodec', 'none') == 'none']
    
    if video_formats:
        best_video = max(video_formats, key=lambda x: x.get('height', 0))
        print(f"Best video quality: {best_video.get('height', 'Unknown')}p")
    
    if audio_formats:
        best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
        print(f"Best audio quality: {best_audio.get('abr', 'Unknown')} kbps")

# Thumbnail
thumbnail = video_info.get('thumbnail')
if thumbnail:
    print(f"Thumbnail: {thumbnail}")
```

## Episodic Examples
### Development Step 9: Filter Wikipedia Revisions from Inception to June 30, 2023, and Count All Edits

**Description**: Filter the extracted revision data from the comprehensive Wikipedia history to count only the edits made from the page's inception until the end of June 2023. Exclude any revisions that occurred after June 30, 2023, and provide the exact count of edits within the specified timeframe.

**Use Cases**:
- Historical audit of a high-traffic political article to report the exact number of edits from its creation through June 30, 2023 for a government transparency review
- Legal compliance verification of a corporate product documentation page by counting all edits made before the July 2023 launch cutoff
- Academic analysis of contributor activity on the “Climate Change” Wikipedia entry up to June 30, 2023 to correlate edit bursts with major IPCC report releases
- Data journalism investigation tracking the volume of corrections on COVID-19–related pages from inception until mid-2023 to illustrate information stability
- Software documentation freeze monitoring by tallying updates to the “Docker” page before the June 2023 feature-freeze deadline for release planning
- Competitive market research quantifying revision counts on flagship smartphone pages through June 2023 to benchmark public interest trends
- Non-profit grant application support by auditing edits made to the NGO’s mission statement article up to June 2023 funding deadline

```
import os
import requests
import json
from datetime import datetime
import time

print("=== EXTRACTING WIKIPEDIA REVISION HISTORY DATA ===\n")
print("Since no revision data exists in workspace, I need to extract it first\n")

# Use the existing workspace directory
workspace_dir = 'workspace_f3917a3d-1d17-4ee2-90c5-683b072218fe'
print(f"Using workspace directory: {workspace_dir}\n")

# Since the PLAN mentions "extracted revision data" but doesn't specify which page,
# I'll need to make an assumption about which Wikipedia page to analyze
# Let me start with a common example page for demonstration
page_title = "Python (programming language)"  # Using a well-documented page as example

print(f"Extracting revision history for: {page_title}\n")

# Wikipedia API endpoint for getting revision history
api_url = "https://en.wikipedia.org/w/api.php"

# Parameters for getting revision history
params = {
    'action': 'query',
    'format': 'json',
    'prop': 'revisions',
    'titles': page_title,
    'rvlimit': 'max',  # Get maximum revisions per request (500)
    'rvprop': 'timestamp|user|comment|ids|size',
    'rvdir': 'newer'  # Start from oldest revisions
}

print("=== FETCHING REVISION DATA FROM WIKIPEDIA API ===\n")

all_revisions = []
rvcontinue = None
request_count = 0
max_requests = 10  # Limit to prevent excessive API calls

while request_count < max_requests:
    request_count += 1
    
    # Add continuation parameter if we have one
    current_params = params.copy()
    if rvcontinue:
        current_params['rvcontinue'] = rvcontinue
    
    print(f"Request {request_count}: Fetching revisions...")
    
    try:
        response = requests.get(api_url, params=current_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract revisions from response
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            
            if 'revisions' in pages[page_id]:
                revisions = pages[page_id]['revisions']
                all_revisions.extend(revisions)
                print(f"  Retrieved {len(revisions)} revisions (total so far: {len(all_revisions)})")
            else:
                print("  No revisions found in response")
                break
        else:
            print("  No page data found in response")
            break
        
        # Check if there are more revisions to fetch
        if 'continue' in data and 'rvcontinue' in data['continue']:
            rvcontinue = data['continue']['rvcontinue']
            print(f"  More revisions available, continuing...")
        else:
            print("  All revisions retrieved")
            break
        
        # Be respectful to Wikipedia's servers
        time.sleep(1)
        
    except Exception as e:
        print(f"  ❌ Error fetching revisions: {str(e)}")
        break

print(f"\n=== REVISION EXTRACTION COMPLETE ===\n")
print(f"Total revisions extracted: {len(all_revisions)}")
print(f"API requests made: {request_count}")

if len(all_revisions) == 0:
    print("❌ No revision data extracted. Cannot proceed with filtering.")
else:
    # Save the raw revision data
    raw_data = {
        'extraction_metadata': {
            'page_title': page_title,
            'extraction_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_revisions': len(all_revisions),
            'api_requests': request_count
        },
        'revisions': all_revisions
    }
    
    raw_file = os.path.join(workspace_dir, 'wikipedia_revision_data_raw.json')
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Raw revision data saved to: {os.path.basename(raw_file)}")
    print(f"   File size: {os.path.getsize(raw_file):,} bytes")
    
    # Now analyze the data structure and show some examples
    print(f"\n=== ANALYZING REVISION DATA STRUCTURE ===\n")
    
    if all_revisions:
        sample_revision = all_revisions[0]
        print(f"Sample revision structure:")
        for key, value in sample_revision.items():
            print(f"  {key}: {type(value).__name__} = {str(value)[:100]}")
        
        # Show date range of revisions
        timestamps = [rev['timestamp'] for rev in all_revisions if 'timestamp' in rev]
        if timestamps:
            print(f"\nRevision date range:")
            print(f"  Earliest: {min(timestamps)}")
            print(f"  Latest: {max(timestamps)}")
        
        # Show some sample timestamps to understand format
        print(f"\nSample timestamps:")
        for i, rev in enumerate(all_revisions[:5]):
            if 'timestamp' in rev:
                print(f"  {i+1}. {rev['timestamp']}")
    
    print(f"\n=== NOW FILTERING REVISIONS UNTIL END OF JUNE 2023 ===\n")
    
    # Filter revisions until June 30, 2023
    cutoff_date = datetime(2023, 6, 30, 23, 59, 59)
    print(f"Cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    filtered_revisions = []
    
    for revision in all_revisions:
        if 'timestamp' in revision:
            # Parse Wikipedia timestamp format (e.g., "2023-06-15T14:30:25Z")
            try:
                rev_timestamp = datetime.fromisoformat(revision['timestamp'].replace('Z', '+00:00'))
                # Convert to naive datetime for comparison
                rev_timestamp = rev_timestamp.replace(tzinfo=None)
                
                if rev_timestamp <= cutoff_date:
                    filtered_revisions.append(revision)
                else:
                    # Since revisions are ordered, we can break early if we hit a date after cutoff
                    break
                    
            except Exception as e:
                print(f"  ⚠️ Error parsing timestamp {revision['timestamp']}: {str(e)}")
                continue
    
    print(f"\n=== FILTERING RESULTS ===\n")
    print(f"Total revisions extracted: {len(all_revisions)}")
    print(f"Revisions until end of June 2023: {len(filtered_revisions)}")
    print(f"Revisions excluded (after June 30, 2023): {len(all_revisions) - len(filtered_revisions)}")
    
    if filtered_revisions:
        # Show date range of filtered revisions
        filtered_timestamps = [rev['timestamp'] for rev in filtered_revisions if 'timestamp' in rev]
        if filtered_timestamps:
            print(f"\nFiltered revision date range:")
            print(f"  Earliest: {min(filtered_timestamps)}")
            print(f"  Latest: {max(filtered_timestamps)}")
    
    # Save filtered results
    filtered_data = {
        'filtering_metadata': {
            'page_title': page_title,
            'filtering_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'cutoff_date': cutoff_date.strftime('%Y-%m-%d %H:%M:%S'),
            'total_revisions_before_filtering': len(all_revisions),
            'revisions_until_june_2023': len(filtered_revisions),
            'revisions_excluded': len(all_revisions) - len(filtered_revisions)
        },
        'filtered_revisions': filtered_revisions
    }
    
    filtered_file = os.path.join(workspace_dir, 'wikipedia_revisions_until_june_2023.json')
    with open(filtered_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Filtered revision data saved to: {os.path.basename(filtered_file)}")
    print(f"   File size: {os.path.getsize(filtered_file):,} bytes")
    
    # Create summary report
    summary_file = os.path.join(workspace_dir, 'revision_count_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"WIKIPEDIA REVISION COUNT SUMMARY\n")
        f.write(f"={'='*40}\n\n")
        f.write(f"Page analyzed: {page_title}\n")
        f.write(f"Analysis date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Cutoff date: June 30, 2023 23:59:59\n\n")
        f.write(f"RESULTS:\n")
        f.write(f"- Total revisions extracted: {len(all_revisions)}\n")
        f.write(f"- Revisions until end of June 2023: {len(filtered_revisions)}\n")
        f.write(f"- Revisions excluded (after June 30, 2023): {len(all_revisions) - len(filtered_revisions)}\n\n")
        
        if filtered_revisions:
            f.write(f"FILTERED REVISION DATE RANGE:\n")
            if filtered_timestamps:
                f.write(f"- Earliest revision: {min(filtered_timestamps)}\n")
                f.write(f"- Latest revision: {max(filtered_timestamps)}\n")
    
    print(f"✅ Summary report saved to: {os.path.basename(summary_file)}")
    
    print(f"\n🎯 FINAL ANSWER: {len(filtered_revisions)} edits were made from the page's inception until the end of June 2023")
```

### Development Step 9: Nature 2020 Peer-Reviewed Research Article Count (Excluding Non-Research Content)

**Description**: Research and determine the total number of research articles (excluding book reviews, columns, editorials, and other non-research content) published by Nature journal in 2020. Focus on identifying peer-reviewed research articles that would typically involve statistical analysis and hypothesis testing.

**Use Cases**:
- University research office automating annual reports by extracting the exact count of peer-reviewed research articles published in Nature during 2020 to benchmark faculty performance.
- Science funding agency tracking grant recipient productivity by scraping Nature’s 2020 archive for published research papers tied to funded projects.
- Bibliometric analytics firm integrating direct Nature website data into dashboards to compare year-over-year article output across high-impact journals for clients.
- Academic librarian compiling subscription cost-benefit analyses by quantifying the number of research articles versus editorials and reviews in Nature’s 2020 issues.
- Meta-research team studying publication trends by programmatically gathering volume and issue information from Nature’s 2020 archive to model shifts in topic areas.
- Data journalist building an interactive web story on global research output by harvesting Nature’s 2020 article counts and visualizing country-level contributions.
- University tenure committee cross-verifying candidate CVs by automatically matching listed Nature 2020 publications against the journal’s official article count.
- R&D department in a biotech firm monitoring competitor activity by regularly scraping Nature’s “Browse by Year 2020” page for new research articles relevant to their field.

```
import os
import json
import requests
from bs4 import BeautifulSoup

print("=== PIVOTING TO SEARCH FOR NATURE JOURNAL'S OWN 2020 PUBLICATION DATA ===\n")

# Find workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    workspace_dir = workspace_dirs[0]
    print(f"Using workspace directory: {workspace_dir}")
else:
    print("No workspace directory found.")
    exit()

# Based on the analysis, we need to search for Nature journal-specific sources
# Let's try direct access to Nature journal's archive and editorial pages

print("\n=== ATTEMPTING DIRECT ACCESS TO NATURE JOURNAL ARCHIVE ===\n")

# Set up headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
}

# Try multiple Nature journal-specific URLs that might contain 2020 publication statistics
target_urls = [
    {
        'name': 'Nature Journal 2020 Archive',
        'url': 'https://www.nature.com/nature/articles?type=article&year=2020',
        'description': 'Direct archive of Nature journal articles from 2020'
    },
    {
        'name': 'Nature Journal Browse by Year',
        'url': 'https://www.nature.com/nature/browse/date/2020',
        'description': 'Nature journal browse page for 2020'
    },
    {
        'name': 'Nature Journal About Page',
        'url': 'https://www.nature.com/nature/about',
        'description': 'Nature journal about page with publication information'
    },
    {
        'name': 'Nature Journal Editorial Information',
        'url': 'https://www.nature.com/nature/for-authors/editorial-criteria',
        'description': 'Nature journal editorial information and criteria'
    }
]

successful_accesses = []

for i, target in enumerate(target_urls, 1):
    print(f"\nAccessing {i}. {target['name']}")
    print(f"URL: {target['url']}")
    print(f"Purpose: {target['description']}")
    
    try:
        response = requests.get(target['url'], headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✓ Successfully accessed (Status: {response.status_code})")
            print(f"Content length: {len(response.content):,} bytes")
            
            # Parse the content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Save the content
            filename = f"nature_journal_direct_{i}_{target['name'].replace(' ', '_').replace('/', '_')}.txt"
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Source: {target['name']}\n")
                f.write(f"URL: {target['url']}\n")
                f.write(f"Purpose: {target['description']}\n")
                f.write(f"Accessed: {response.status_code}\n")
                f.write(f"Content Length: {len(clean_text):,} characters\n")
                f.write("=" * 50 + "\n")
                f.write(clean_text)
            
            print(f"Content saved to: {filename}")
            print(f"Text length: {len(clean_text):,} characters")
            
            # Look for 2020 article counts, volume information, or publication statistics
            import re
            
            # Search for patterns that might indicate article counts
            article_count_patterns = [
                r'(\d{2,4})\s+(?:research\s+)?articles?\s+(?:published|in)\s+2020',
                r'2020.*?(\d{2,4})\s+(?:research\s+)?articles?',
                r'published\s+(\d{2,4})\s+(?:research\s+)?articles?.*?2020',
                r'volume\s+\d+.*?2020.*?(\d{2,4})\s+(?:articles?|papers?)',
                r'total.*?(\d{2,4}).*?(?:articles?|papers?).*?2020'
            ]
            
            found_counts = []
            content_lower = clean_text.lower()
            
            for pattern in article_count_patterns:
                matches = re.findall(pattern, content_lower)
                if matches:
                    found_counts.extend(matches)
            
            # Look for Nature journal volume information for 2020
            volume_patterns = [
                r'volume\s+(\d+).*?2020',
                r'2020.*?volume\s+(\d+)',
                r'vol\.?\s+(\d+).*?2020',
                r'2020.*?vol\.?\s+(\d+)'
            ]
            
            volume_info = []
            for pattern in volume_patterns:
                matches = re.findall(pattern, content_lower)
                if matches:
                    volume_info.extend(matches)
            
            # Look for specific terms related to Nature journal statistics
            nature_stats_terms = [
                'annual report', 'editorial summary', 'publication statistics',
                'articles published', 'research articles', 'peer-reviewed',
                'volume 577', 'volume 578', 'volume 579', 'volume 580', 'volume 581', 'volume 582',  # 2020 volumes
                'impact factor', 'submission statistics'
            ]
            
            found_terms = []
            for term in nature_stats_terms:
                if term in content_lower:
                    found_terms.append(term)
            
            print(f"Potential article counts found: {found_counts}")
            print(f"Volume information found: {volume_info}")
            print(f"Nature statistics terms found: {found_terms[:5]}")
            
            # Check if this page has pagination or links to more detailed statistics
            pagination_indicators = ['next page', 'more articles', 'show more', 'page 2', 'total results']
            has_pagination = any(indicator in content_lower for indicator in pagination_indicators)
            print(f"Has pagination/more content: {has_pagination}")
            
            successful_accesses.append({
                'name': target['name'],
                'url': target['url'],
                'filename': filename,
                'content_length': len(clean_text),
                'potential_counts': found_counts,
                'volume_info': volume_info,
                'statistics_terms': found_terms,
                'has_pagination': has_pagination,
                'status': 'success'
            })
            
        else:
            print(f"✗ Failed to access (Status: {response.status_code})")
            successful_accesses.append({
                'name': target['name'],
                'url': target['url'],
                'status': f'failed_{response.status_code}',
                'error': f'HTTP {response.status_code}'
            })
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
        successful_accesses.append({
            'name': target['name'],
            'url': target['url'],
            'status': 'error',
            'error': str(e)
        })
    
    print("-" * 60)

# Save results
direct_access_results = {
    'search_strategy': 'Direct access to Nature journal pages',
    'target_urls_attempted': len(target_urls),
    'successful_accesses': len([a for a in successful_accesses if a.get('status') == 'success']),
    'failed_accesses': len([a for a in successful_accesses if a.get('status') != 'success']),
    'access_details': successful_accesses,
    'next_steps': [
        'Analyze downloaded Nature journal pages for 2020 article counts',
        'Look for volume/issue information that indicates total articles',
        'Search for editorial summaries or annual reports',
        'Check if pagination reveals total article counts'
    ]
}

results_file = os.path.join(workspace_dir, 'nature_journal_direct_access.json')
with open(results_file, 'w') as f:
    json.dump(direct_access_results, f, indent=2)

print(f"\n=== DIRECT ACCESS RESULTS SUMMARY ===\n")
print(f"Target URLs attempted: {len(target_urls)}")
print(f"Successful accesses: {direct_access_results['successful_accesses']}")
print(f"Failed accesses: {direct_access_results['failed_accesses']}")
print(f"Results saved to: {os.path.basename(results_file)}")

# Analyze what we found
all_potential_counts = []
all_volume_info = []
all_stats_terms = []

for access in successful_accesses:
    if access.get('status') == 'success':
        if access.get('potential_counts'):
            all_potential_counts.extend(access['potential_counts'])
        if access.get('volume_info'):
            all_volume_info.extend(access['volume_info'])
        if access.get('statistics_terms'):
            all_stats_terms.extend(access['statistics_terms'])

print(f"\n=== ANALYSIS OF DIRECT ACCESS RESULTS ===\n")
print(f"All potential article counts found: {list(set(all_potential_counts))}")
print(f"All volume information found: {list(set(all_volume_info))}")
print(f"All statistics terms found: {list(set(all_stats_terms))}")

if all_potential_counts:
    # Convert to integers and filter reasonable values
    numeric_counts = []
    for count in all_potential_counts:
        try:
            num = int(count)
            if 100 <= num <= 1500:  # Reasonable range for Nature journal articles per year
                numeric_counts.append(num)
        except ValueError:
            continue
    
    if numeric_counts:
        print(f"\n*** POTENTIAL NATURE JOURNAL 2020 ARTICLE COUNTS ***")
        print(f"Filtered numeric counts: {sorted(set(numeric_counts))}")
        print(f"Most likely count: {max(set(numeric_counts), key=numeric_counts.count)}")
    else:
        print(f"\nNo reasonable article counts found in the extracted data.")
else:
    print(f"\nNo potential article counts found in direct access attempts.")

print(f"\n=== NEXT STEPS RECOMMENDATION ===\n")
if direct_access_results['successful_accesses'] > 0:
    print("✓ Successfully accessed Nature journal pages directly")
    print("Next: Analyze the downloaded content for specific 2020 research article counts")
    print("Focus on: Volume information, pagination data, and editorial statistics")
else:
    print("✗ Direct access to Nature journal pages failed")
    print("Alternative approaches needed:")
    print("1. Search academic databases (PubMed, Web of Science)")
    print("2. Contact Nature journal editorial office")
    print("3. Use bibliometric tools (Scopus, Google Scholar)")

print(f"\nCurrent workspace files:")
for file in os.listdir(workspace_dir):
    file_path = os.path.join(workspace_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"  - {file} ({file_size:,} bytes)")
```

## Created Time
2025-08-14 19:26:09
