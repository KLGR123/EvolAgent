# Developer Plan 02

## Plan
Access ScienceDirect directly through its official website (sciencedirect.com) to search for Reference Works statistics or browse the platform's content categorization system. Look for ScienceDirect's own database metrics, content statistics pages, or publisher analytics that might show Reference Works counts by subject domain including Life Sciences and Health Sciences for 2022. Also search for any ScienceDirect annual reports, content summaries, or platform statistics that could contain the specific numerical data needed for standard deviation calculations.

## Description
This is the necessary next step because: (1) The previous comprehensive search covered external sources but may not have accessed ScienceDirect's own internal statistics or platform-specific data, (2) The developer's extensive analysis of 88 sources and 4.3M+ characters found limited Reference Works mentions, suggesting we need to go directly to the source platform, (3) Expected outcome is to find ScienceDirect's own content categorization data or platform statistics that show Reference Works counts by academic domain, (4) This direct approach to the platform mentioned in the TASK may reveal proprietary statistics or internal metrics not available through general web searches

## Semantic Examples
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

### How to Search for Information Using Google Search?

**Description**: Google Search (also known simply as Google or Google.com) is a search engine operated by Google. It allows users to search for information on the Web by entering keywords or phrases.
Search for information using Google search engine with advanced operators and filters. Requires SerpAPI key for accessing Google Search API.

**Use Cases**:
- General research and Information Gathering
- E-commerce and Shopping Research
- Professional and Business Applications
- Data Collection and Analysis
- Educational and Learning Support
- Technical and Development Research
- Professional and Business Applications

```
import os
import re
import requests

# The search query to perform. Supports advanced operators like "site:", "filetype:", quotes, minus sign
# For example: "machine learning" site:arxiv.org filetype:pdf -tutorial
query = "machine learning tutorials"
# The maximum number of results to return (default: 10)
max_results = 10
# The type of search: "search" for web results, "image" for images, "news" for news (default: "search")
type = "search"
# Time range filter. Examples: "qdr:h" (past hour), "qdr:d" (past day), "qdr:w" (past week), etc.
tbs = None
# Region/country code for search results. Examples: "us", "cn", "jp", "uk", "de", "fr", etc.
region = None

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")

# Validate search type parameter
valid_types = ["search", "image", "news"]
if type not in valid_types:
    print(f"Error: Invalid type '{type}'. Must be one of: {', '.join(valid_types)}")

# Validate time range format if provided
if tbs is not None:
    time_patterns = [
        r'^qdr:[hdwmy]$$',
        r'^qdr:[hdwmy]\d+$$',
        r'^cdr:1,cd_min:\d{2}/\d{2}/\d{4},cd_max:\d{2}/\d{2}/\d{4}$$'
    ]
  
    is_valid_tbs = any(re.match(pattern, tbs) for pattern in time_patterns)
    if not is_valid_tbs:
        print(
            f"Error: Invalid tbs format '{tbs}'. "
            "Must be one of: qdr:h, qdr:d, qdr:w, qdr:m, qdr:y, "
            "or with numbers like qdr:h12, qdr:d3, qdr:w2, qdr:m6, qdr:m2, "
            "or custom range like cdr:1,cd_min:DD/MM/YYYY,cd_max:DD/MM/YYYY"
        )

# Validate region format if provided
if region is not None:
    if not re.match(r'^[a-z]{2}$$', region.lower()):
        print(
            f"Error: Invalid region format '{region}'. "
            "Must be a valid ISO 3166-1 alpha-2 country code like 'us', 'cn', 'jp', 'uk', 'de', etc."
        )
    region = region.lower()

# Prepare API request parameters
params = {
    "q": query,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": max_results,
    "type": type,
    "tbs": tbs,
}

# Add region parameter if specified
if region is not None:
    params["gl"] = region

# Make API request to SerpAPI
response = requests.get("https://serpapi.com/search.json", params=params)

if response.status_code == 200:
    results = response.json()
else:
    print(f"Error: API request failed with status {response.status_code}: {response.text}")

# Process and return results based on search type
if type == "search":
    if not results.get("organic_results"):
        print(f"No results found for '{query}'. Try with a more general query, or remove the time restriction if used.")
    else:
        print(str(results["organic_results"]))

elif type == "image":
    if not results.get("images"):
        print(f"No images found for '{query}'. Try with a more general query, or remove the time restriction if used.")
    else:
        print(str(results["images"]))

elif type == "news":
    if not results.get("news"):
        print(f"No news found for '{query}'. Try with a more general query, or remove the time restriction if used.")
    else:
        print(str(results["news"]))
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

### How to Parse PowerPoint Presentations and Extract Structured Content?

**Description**: Parse a PowerPoint presentation and return structured content in HTML format, including text, tables, and image descriptions. This tool can analyze images within presentations and extract table data.

**Use Cases**:
- Extract text, tables, and images from PowerPoint presentations for content analysis
- Convert PowerPoint slides to structured HTML for web publishing or further processing
- Analyze and summarize slide content for meeting notes or documentation
- Retrieve and describe images within slides for accessibility or image analysis
- Extract tabular data from presentations for data analysis or reporting

```
import os
import html
import tempfile
import base64
import pptx

# The path to the PowerPoint file to be parsed, for example: "workspace/task.pptx"
pptx_path = "workspace/task.pptx"

def _is_picture(shape):
    """Check if a shape is a picture."""
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
        return True
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PLACEHOLDER:
        if hasattr(shape, "image"):
            return True
    return False

def _is_table(shape):
    """Check if a shape is a table."""
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.TABLE:
        return True
    return False

def _extract_image_content(shape, slide_num, shape_num):
    """Extract image content and analyze it."""
    # Try to get alt text first
    alt_text = ""
    alt_text = shape._element._nvXxPr.cNvPr.attrib.get("descr", "")

    if alt_text:
        return f"<p><strong>Image {slide_num}-{shape_num}:</strong> {alt_text}</p>"
    
    # If no alt text, try to extract and analyze the image
    # Extract image data
    image = shape.image
    image_bytes = image.blob
    
    # Save to temporary file for analysis
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
        temp_file.write(image_bytes)
        temp_image_path = temp_file.name

    # Use parse_image to analyze the image (requires parse_image function to be available)
    # For this example, we'll just return a placeholder
    image_analysis = "[Image content analysis would be performed here]"
    
    # Clean up temporary file
    os.unlink(temp_image_path)
    
    return f"<div><strong>Image {slide_num}-{shape_num} Analysis:</strong><br/>{image_analysis}</div>"

def _extract_table_content(shape):
    """Extract table content and return as HTML."""
    html_table = "<table border='1' style='border-collapse:collapse;'>"
    first_row = True
    
    for row in shape.table.rows:
        html_table += "<tr>"
        for cell in row.cells:
            tag = "th" if first_row else "td"
            cell_text = html.escape(cell.text.strip()) if cell.text else ""
            html_table += f"<{tag}>{cell_text}</{tag}>"
        html_table += "</tr>"
        first_row = False
    
    html_table += "</table>"
    return html_table

if not os.path.exists(pptx_path):
    print(f"Error: PowerPoint file '{pptx_path}' does not exist.")

supported_formats = ['.pptx', '.ppt']
file_ext = os.path.splitext(pptx_path)[1].lower()

if file_ext not in supported_formats:
    print(f"Error: Unsupported file format '{file_ext}'. Supported formats: {', '.join(supported_formats)}")

# Parse PowerPoint presentation using python-pptx
presentation = pptx.Presentation(pptx_path)
html_content = f"<h1>PowerPoint: {os.path.basename(pptx_path)}</h1>\n"
html_content += f"<p>Number of slides: {len(presentation.slides)}</p>\n"
html_content += "<hr/>\n"

slide_num = 0
for slide in presentation.slides:
    slide_num += 1
    html_content += f"<h2>Slide {slide_num}</h2>\n"
    
    title = slide.shapes.title
    shape_num = 0
    
    for shape in slide.shapes:
        shape_num += 1
        
        # Process image shapes
        if _is_picture(shape):
            image_content = _extract_image_content(shape, slide_num, shape_num)
            html_content += image_content + "\n"
        
        # Process table shapes
        elif _is_table(shape):
            html_content += "<h4>Table:</h4>\n"
            table_content = _extract_table_content(shape)
            html_content += table_content + "\n"
        
        # Process text shapes
        elif shape.has_text_frame and shape.text.strip():
            if shape == title:
                html_content += f"<h3>{html.escape(shape.text.strip())}</h3>\n"
            else:
                # Process multi-level text content
                text_content = shape.text.strip()
                if text_content:
                    # Split text by line and preserve formatting
                    lines = text_content.split('\n')
                    html_content += "<div>\n"
                    for line in lines:
                        if line.strip():
                            html_content += f"<p>{html.escape(line.strip())}</p>\n"
                    html_content += "</div>\n"
    
    # Process slide notes if available
    if slide.has_notes_slide:
        notes_frame = slide.notes_slide.notes_text_frame
        if notes_frame is not None and notes_frame.text.strip():
            html_content += "<h4>Notes:</h4>\n"
            notes_text = notes_frame.text.strip()
            html_content += f"<div style='background-color:#f5f5f5;padding:10px;'>{html.escape(notes_text)}</div>\n"
    
    html_content += "<hr/>\n"

print(html_content.strip())
```

## Episodic Examples
### Development Step 8: Title:  
Verify DOI 10.2307/j.ctv9b2xdv and Locate Wikipedia Citations with November Access Dates in References

**Description**: Verify the DOI 10.2307/j.ctv9b2xdv by conducting an independent search to confirm we have the correct publication. Cross-reference the DOI with multiple academic databases and publisher sources to ensure we're analyzing the right book. If the DOI resolves to a different publication than 'The Responsibility of Intellectuals', access that correct publication instead. If the DOI is confirmed correct, perform a more targeted search specifically for endnotes, footnotes, or reference sections that might contain Wikipedia citations with November access dates, including checking for alternative formatting or citation styles that might have been missed in the previous comprehensive search.

**Use Cases**:
- Academic integrity verification for university librarians cross-checking citations in student theses against original publications
- Automated reference auditing for journal editors ensuring all cited DOIs resolve to the correct sources before publication
- Legal research teams validating cited case law and statutes in briefs by independently confirming DOIs and cross-referencing publisher records
- Digital humanities projects analyzing citation patterns in historical texts, including targeted searches for Wikipedia and web-based references
- Research grant compliance audits requiring confirmation that all referenced materials in proposals are correctly attributed and accessible
- Corporate knowledge management systems performing automated checks on internal reports to ensure external sources are properly cited and up-to-date
- Scholarly book publishers conducting pre-publication reviews to detect and correct misattributed or outdated citations in manuscripts
- Library acquisition departments verifying the authenticity and edition of requested academic books before procurement using DOI and metadata cross-referencing

```
import os
import json
import requests
from bs4 import BeautifulSoup
import time
import re

print('=== INDEPENDENT DOI VERIFICATION AND TARGETED SEARCH ===') 
print('DOI: 10.2307/j.ctv9b2xdv')
print('Objective: Verify DOI independently and perform targeted search for Wikipedia citations')
print('Status: Previous comprehensive search found no November Wikipedia citations')
print('\n' + '='*100 + '\n')

# First, let's inspect the existing workspace to understand what we have
print('=== INSPECTING EXISTING WORKSPACE FILES ===')
workspace_files = os.listdir('workspace')
print(f'Found {len(workspace_files)} files in workspace:')
for file in sorted(workspace_files):
    file_path = os.path.join('workspace', file)
    file_size = os.path.getsize(file_path)
    print(f'- {file} ({file_size:,} bytes)')

# Let's examine the final bibliographic record to understand the publication details
final_record_path = 'workspace/final_bibliographic_record.json'
if os.path.exists(final_record_path):
    print('\n=== EXAMINING FINAL BIBLIOGRAPHIC RECORD ===')
    with open(final_record_path, 'r', encoding='utf-8') as f:
        biblio_data = json.load(f)
    
    print('Available keys in bibliographic record:')
    for key in biblio_data.keys():
        value = biblio_data[key]
        if isinstance(value, (str, int)):
            print(f'- {key}: {value}')
        elif isinstance(value, list):
            print(f'- {key}: list with {len(value)} items')
            if value and len(value) <= 3:
                for item in value:
                    print(f'  * {item}')
        elif isinstance(value, dict):
            print(f'- {key}: dict with keys {list(value.keys())}')
        else:
            print(f'- {key}: {type(value)}')
else:
    print('Final bibliographic record not found')

print('\n=== INDEPENDENT DOI VERIFICATION ===')

# Let's verify the DOI through multiple independent sources
doi = '10.2307/j.ctv9b2xdv'
print(f'Verifying DOI: {doi}')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

# 1. CrossRef API verification
print('\n1. CrossRef API Verification:')
try:
    crossref_url = f'https://api.crossref.org/works/{doi}'
    response = requests.get(crossref_url, headers=headers, timeout=15)
    print(f'   Status: {response.status_code}')
    
    if response.status_code == 200:
        crossref_data = response.json()
        work = crossref_data.get('message', {})
        
        print(f'   Title: {work.get("title", ["Unknown"])[0] if work.get("title") else "Unknown"}')
        print(f'   Publisher: {work.get("publisher", "Unknown")}')
        print(f'   Type: {work.get("type", "Unknown")}')
        print(f'   Published: {work.get("published-print", {}).get("date-parts", [["Unknown"]])[0]}')
        
        # Check if this matches our expected publication
        title = work.get('title', [''])[0].lower() if work.get('title') else ''
        if 'responsibility' in title and 'intellectuals' in title:
            print('   ✓ Confirmed: This is "The Responsibility of Intellectuals"')
        else:
            print(f'   ⚠ Warning: Title does not match expected publication')
            print(f'   Actual title: {title}')
    else:
        print(f'   ❌ CrossRef lookup failed: {response.status_code}')
except Exception as e:
    print(f'   ❌ CrossRef error: {str(e)}')

# 2. DOI.org resolution verification
print('\n2. DOI.org Resolution Verification:')
try:
    doi_url = f'https://doi.org/{doi}'
    response = requests.get(doi_url, headers=headers, timeout=15, allow_redirects=True)
    print(f'   Status: {response.status_code}')
    print(f'   Final URL: {response.url}')
    
    if response.status_code == 200:
        # Check where it redirects to
        if 'jstor.org' in response.url:
            print('   ✓ Redirects to JSTOR as expected')
        elif 'uclpress' in response.url:
            print('   ✓ Redirects to UCL Press')
        else:
            print(f'   ⚠ Redirects to unexpected domain: {response.url}')
    else:
        print(f'   ❌ DOI resolution failed: {response.status_code}')
except Exception as e:
    print(f'   ❌ DOI resolution error: {str(e)}')

# 3. Alternative identifier verification
print('\n3. Alternative Identifier Verification:')
# Check if there are alternative identifiers from CrossRef
if 'crossref_data' in locals() and crossref_data:
    work = crossref_data.get('message', {})
    
    # Look for ISBN or other identifiers
    if 'ISBN' in work:
        print(f'   ISBN found: {work["ISBN"]}')
    
    # Look for alternative URLs
    if 'URL' in work:
        print(f'   Alternative URL: {work["URL"]}')
    
    # Check for relations to other works
    if 'relation' in work:
        relations = work['relation']
        print(f'   Relations found: {list(relations.keys()) if isinstance(relations, dict) else relations}')
        
        # Look for "is-identical-to" relations
        if isinstance(relations, dict) and 'is-identical-to' in relations:
            identical_works = relations['is-identical-to']
            for related_work in identical_works:
                if 'id' in related_work:
                    alt_doi = related_work['id']
                    print(f'   Alternative DOI found: {alt_doi}')
                    
                    # Try to access this alternative DOI
                    try:
                        alt_url = f'https://doi.org/{alt_doi}'
                        alt_response = requests.get(alt_url, headers=headers, timeout=15, allow_redirects=True)
                        print(f'   Alternative DOI status: {alt_response.status_code}')
                        print(f'   Alternative DOI redirects to: {alt_response.url}')
                        
                        if alt_response.status_code == 200 and 'uclpress' in alt_response.url:
                            print('   ✓ Alternative DOI provides direct UCL Press access')
                    except Exception as alt_e:
                        print(f'   ❌ Alternative DOI error: {str(alt_e)}')

print('\n=== CHECKING FOR DIFFERENT EDITIONS OR VERSIONS ===')

# Search for different versions of the publication
search_queries = [
    'The Responsibility of Intellectuals UCL Press 2019',
    'Responsibility Intellectuals Chomsky UCL Press',
    'The Responsibility of Intellectuals reflections 50 years'
]

for i, query in enumerate(search_queries, 1):
    print(f'\n{i}. Searching for: "{query}"')
    try:
        # Use Google Scholar search
        scholar_url = f'https://scholar.google.com/scholar?q={query.replace(" ", "+")}'
        response = requests.get(scholar_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for result titles
            result_titles = soup.find_all('h3', class_='gs_rt')
            if result_titles:
                print(f'   Found {len(result_titles)} search results:')
                for j, title_elem in enumerate(result_titles[:3], 1):
                    title_text = title_elem.get_text().strip()
                    print(f'   {j}. {title_text[:100]}...')
                    
                    # Look for links in this result
                    links = title_elem.find_all('a', href=True)
                    for link in links:
                        href = link.get('href')
                        if 'uclpress' in href or 'ucl.ac.uk' in href:
                            print(f'      UCL link: {href}')
            else:
                print('   No results found')
        else:
            print(f'   Search failed: {response.status_code}')
    except Exception as search_e:
        print(f'   Search error: {str(search_e)}')
    
    time.sleep(2)  # Be respectful to Google Scholar

print('\n=== TARGETED SEARCH FOR ENDNOTES AND REFERENCES SECTIONS ===')

# Let's check if we have the full book text and search more specifically
full_text_path = 'workspace/full_book_text.txt'
if os.path.exists(full_text_path):
    print('Loading full book text for targeted analysis...')
    
    with open(full_text_path, 'r', encoding='utf-8') as f:
        full_text = f.read()
    
    print(f'Full text length: {len(full_text):,} characters')
    
    # Search for different types of reference sections
    reference_section_patterns = [
        r'\b(notes?)\b[^\n]{0,50}\n',
        r'\b(endnotes?)\b[^\n]{0,50}\n',
        r'\b(references?)\b[^\n]{0,50}\n',
        r'\b(bibliography)\b[^\n]{0,50}\n',
        r'\b(works cited)\b[^\n]{0,50}\n',
        r'\b(sources?)\b[^\n]{0,50}\n',
        r'\b(footnotes?)\b[^\n]{0,50}\n'
    ]
    
    reference_sections = []
    for pattern in reference_section_patterns:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            section_name = match.group(1)
            position = match.start()
            
            # Get some context around this section
            context_start = max(0, position - 200)
            context_end = min(len(full_text), position + 500)
            context = full_text[context_start:context_end]
            
            reference_sections.append({
                'section_name': section_name,
                'position': position,
                'context': context
            })
    
    if reference_sections:
        print(f'\nFound {len(reference_sections)} potential reference sections:')
        for i, section in enumerate(reference_sections, 1):
            print(f'\n{i}. "{section["section_name"]}" at position {section["position"]:,}')
            print('   Context:')
            print('   ' + '-'*60)
            print('   ' + section['context'][:300].replace('\n', '\n   '))
            print('   ' + '-'*60)
    else:
        print('\nNo clear reference sections found')
    
    # Search for numbered references or citations
    print('\n=== SEARCHING FOR NUMBERED CITATIONS ===')
    
    numbered_citation_patterns = [
        r'\n\s*(\d+)\s*[\.]\s*[^\n]{20,200}',  # Numbered list items
        r'\[(\d+)\][^\n]{20,200}',  # Bracketed numbers
        r'\n\s*(\d+)\s+[A-Z][^\n]{20,200}',  # Number followed by text
    ]
    
    numbered_citations = []
    for pattern in numbered_citation_patterns:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            number = match.group(1)
            citation_text = match.group(0)
            
            # Only include reasonable citation numbers (1-200)
            if 1 <= int(number) <= 200:
                numbered_citations.append({
                    'number': int(number),
                    'text': citation_text.strip(),
                    'position': match.start()
                })
    
    # Remove duplicates and sort by number
    unique_citations = {}
    for citation in numbered_citations:
        if citation['number'] not in unique_citations:
            unique_citations[citation['number']] = citation
    
    sorted_citations = sorted(unique_citations.values(), key=lambda x: x['number'])
    
    if sorted_citations:
        print(f'Found {len(sorted_citations)} numbered citations')
        print('First 10 numbered citations:')
        for citation in sorted_citations[:10]:
            print(f'   {citation["number"]}. {citation["text"][:100]}...')
        
        # Look specifically for Wikipedia in these numbered citations
        wikipedia_numbered = []
        for citation in sorted_citations:
            if 'wikipedia' in citation['text'].lower():
                wikipedia_numbered.append(citation)
        
        if wikipedia_numbered:
            print(f'\n*** FOUND {len(wikipedia_numbered)} NUMBERED CITATIONS CONTAINING WIKIPEDIA ***')
            for citation in wikipedia_numbered:
                print(f'\nCitation {citation["number"]}:')
                print(f'Position: {citation["position"]:,}')
                print('Text:')
                print('-'*60)
                print(citation['text'])
                print('-'*60)
                
                # Check for November dates in this citation
                november_match = re.search(r'november\s+(\d{1,2})', citation['text'], re.IGNORECASE)
                if november_match:
                    day = november_match.group(1)
                    print(f'*** FOUND NOVEMBER {day} ACCESS DATE ***')
        else:
            print('\nNo numbered citations contain Wikipedia references')
    else:
        print('No numbered citations found')
    
    # Final comprehensive search for any access dates
    print('\n=== FINAL SEARCH FOR ANY ACCESS DATES ===')
    
    access_date_patterns = [
        r'accessed[^\n]{0,100}\d{4}[^\n]{0,100}',
        r'retrieved[^\n]{0,100}\d{4}[^\n]{0,100}',
        r'viewed[^\n]{0,100}\d{4}[^\n]{0,100}',
        r'\d{1,2}[^\n]{0,50}\d{4}[^\n]{0,100}accessed[^\n]{0,100}',
        r'\b\d{1,2}\s+\w+\s+\d{4}\b[^\n]{0,200}'
    ]
    
    access_dates = []
    for pattern in access_date_patterns:
        matches = re.finditer(pattern, full_text, re.IGNORECASE)
        for match in matches:
            date_text = match.group(0)
            access_dates.append({
                'text': date_text,
                'position': match.start()
            })
    
    if access_dates:
        print(f'Found {len(access_dates)} potential access dates:')
        for i, date_info in enumerate(access_dates[:10], 1):
            print(f'{i}. {date_info["text"][:100]}...')
    else:
        print('No access dates found')
else:
    print('Full book text not available for targeted search')

print('\n' + '='*100)
print('INDEPENDENT DOI VERIFICATION AND TARGETED SEARCH COMPLETE')
print('='*100)
print('Summary:')
print('- Verified DOI through multiple independent sources')
print('- Searched for alternative editions or versions')
print('- Performed targeted search for reference sections and numbered citations')
print('- Conducted final search for any access dates in the publication')
print('\nConclusion: If no Wikipedia citations with November access dates were found,')
print('this confirms the publication does not contain the target endnote as described.')
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
2025-08-14 19:04:11
