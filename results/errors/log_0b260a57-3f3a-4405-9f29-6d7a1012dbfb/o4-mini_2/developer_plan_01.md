# Developer Plan 01

## Plan
Access ScienceDirect Advanced Search at https://www.sciencedirect.com/advanced-search, set Document Type filter to ‘Reference Works’ and Publication Year filter to ‘2022’, then capture the Subject-Area facet counts for every entry listed under the ‘Life Sciences’ category and for every entry listed under the ‘Health Sciences’ category; save those counts in workspace/life_health_reference_counts.json.

## Description
This step gathers the raw counts of Reference Works in each sub-subject of Life Sciences and Health Sciences for 2022 directly from ScienceDirect. Those counts are the data points needed to compute each category’s sample standard deviation and then determine the difference between the Life Science domains and Health Sciences. No prior data exists, so this establishes the foundation for all subsequent statistical calculations.

## Semantic Examples
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

### How to Parse PDF Files and Extract Text Content?

**Description**: Parse a PDF file and return the text content with optional page range selection. Uses the LangChain community library for document processing.

**Use Cases**:
- Research paper analysis and literature review automation
- Financial report data extraction and analysis
- Legal document review and contract analysis
- Technical manual content extraction and searchable documentation
- Government document processing and compliance checking
- Academic transcript and certificate verification
- Insurance claim document processing
- Medical record digitization and patient data extraction

```
from langchain_community.document_loaders import PyPDFLoader

# The path to the PDF file to be parsed, for example: "workspace/task.pdf"
pdf_path = "workspace/task.pdf"
# The starting page number to read from (1-indexed). If None, read from the beginning
start_page = None
# The ending page number to read to (1-indexed, inclusive). If None, read to the end
end_page = None

# Load and split PDF into pages using LangChain
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

if len(pages) == 0:
    print("No pages found in this PDF file.")

# Handle page range parameters
if start_page is not None:
    start_idx = max(0, start_page - 1)  # Convert to 0-indexed
else:
    start_idx = 0

if end_page is not None:
    end_idx = min(len(pages), end_page)  # Convert to 0-indexed (end_page is inclusive)
else:
    end_idx = len(pages)

# Validate page range
if start_idx >= len(pages):
    print(f"Error: start_page {start_page} is beyond the PDF length ({len(pages)} pages).")

if start_page is not None and end_page is not None and start_page > end_page:
    print(f"Error: start_page ({start_page}) cannot be greater than end_page ({end_page}).")

# Extract the specified page range
selected_pages = pages[start_idx:end_idx]
content = "\n".join([page.page_content for page in selected_pages])

# Check if content is too large (only for full PDF reading)
if len(content) > 100000:
    print(f"Error: PDF '{pdf_path}' content is too large ({len(content)} characters). Total pages: {len(pages)}. Please use start_page and end_page parameters to read specific page ranges.")

# Add page range information to the result if reading a subset
if start_page is not None or end_page is not None:
    actual_start = start_idx + 1
    actual_end = start_idx + len(selected_pages)
    range_info = f"[Pages {actual_start}-{actual_end} of {len(pages)} total pages]\n"
    print(range_info + content)
else:
    print(content)
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

### How to Parse PDB (Protein Data Bank) Files and Extract Structural Information?

**Description**: Parse a PDB file to extract protein structural information including models, chains, residues, and atoms. It provides detailed analysis of protein structure data.

**Use Cases**:
- Extract chain, residue, and atom information from PDB files for protein structure analysis
- Generate summaries of protein models and visualize structural components for bioinformatics research

```
import os
import warnings
from Bio.PDB import PDBParser

warnings.filterwarnings("ignore")

# The path to the PDB file to be parsed, for example: "workspace/task.pdb"
pdb_path = "workspace/task.pdb"
# The starting index for atom lines to preview (default: 0)
start_atom_idx = 0
# The ending index for atom lines to preview (default: 5)
end_atom_idx = 5

if not os.path.exists(pdb_path):
    print(f"Error: PDB file '{pdb_path}' does not exist.")

if not pdb_path.lower().endswith('.pdb'):
    print(f"Error: File must be a .pdb file. Got: {pdb_path}")

result = []
result.append(f"PDB file: {os.path.basename(pdb_path)}")
result.append("=" * 50)

# Parse PDB structure using BioPython
parser = PDBParser()
structure = parser.get_structure('protein', pdb_path)

result.append("Structure Information:")
result.append(f"  Structure ID: {structure.id}")
result.append(f"  Number of models: {len(structure)}")

# Analyze each model in the structure
for model in structure:
    result.append(f"\nModel {model.id}:")
    result.append(f"  Number of chains: {len(model)}")
    
    # Analyze each chain in the model
    for chain in model:
        residues = list(chain)
        result.append(f"    Chain {chain.id}: {len(residues)} residues")
        
        if residues:
            first_res = residues[0]
            last_res = residues[-1]
            result.append(f"      First residue: {first_res.get_resname()} {first_res.get_id()[1]}")
            result.append(f"      Last residue: {last_res.get_resname()} {last_res.get_id()[1]}")
            
            # Count total atoms in this chain
            atom_count = sum(len(list(residue.get_atoms())) for residue in residues)
            result.append(f"      Total atoms: {atom_count}")

result.append("-" * 30)

# Parse basic PDB file information by reading raw text
with open(pdb_path, 'r') as f:
    lines = f.readlines()

result.append("\nBasic PDB Information:")

# Extract header information
header_lines = [line for line in lines if line.startswith('HEADER')]
if header_lines:
    result.append(f"  Header: {header_lines[0].strip()}")

# Extract title information
title_lines = [line for line in lines if line.startswith('TITLE')]
if title_lines:
    title = ' '.join([line[10:].strip() for line in title_lines])
    result.append(f"  Title: {title}")

# Count different record types in the PDB file
record_types = {}
for line in lines:
    if len(line) >= 6:
        record_type = line[:6].strip()
        record_types[record_type] = record_types.get(record_type, 0) + 1

result.append("\nRecord Types:")
for record_type, count in sorted(record_types.items()):
    result.append(f"  {record_type}: {count}")

# Extract and display sample atom lines
atom_lines = [line for line in lines if line.startswith('ATOM')]
if atom_lines:
    # Ensure indices are within bounds
    start_idx = max(0, min(start_atom_idx, len(atom_lines)))
    end_idx = max(start_idx, min(end_atom_idx, len(atom_lines)))
    
    if start_idx < end_idx:
        result.append(f"\nAtom lines ({start_idx} to {end_idx-1}):")
        for line in atom_lines[start_idx:end_idx]:
            result.append(f"  {line.strip()}")
        
        if end_idx < len(atom_lines):
            result.append(f"  ... and {len(atom_lines) - end_idx} more atoms after index {end_idx-1}")
        if start_idx > 0:
            result.append(f"  ... and {start_idx} atoms before index {start_idx}")
    else:
        result.append(f"\nNo atoms to display in range [{start_idx}, {end_idx})")
        result.append(f"  Total atoms available: {len(atom_lines)}")

# Print the complete analysis
print("\n".join(result))
```

## Episodic Examples
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

### Development Step 2: Total Peer-Reviewed Research Articles Published by Nature Journal in 2020

**Description**: Research and determine the total number of research articles (excluding book reviews, columns, editorials, and other non-research content) published by Nature journal in 2020. Focus on identifying peer-reviewed research articles that would typically involve statistical analysis and hypothesis testing.

**Use Cases**:
- Academic library research output tracking and annual reporting for institutional reviews
- Pharmaceutical R&D intelligence gathering by monitoring Nature’s 2020 publications for competitor drug discovery trends
- Grant agency compliance verification through automated counting of peer-reviewed articles by funded investigators in 2020
- Systematic review and meta-analysis support for epidemiologists collecting and filtering Nature 2020 research studies
- University department KPI dashboard automation to report faculty publication counts in top-tier journals like Nature
- Science policy analysis of publication trends in Nature 2020 to inform government funding allocations
- Biotech marketing campaign planning by extracting Nature 2020 article data containing key technology keywords

```
import os
import json

print("=== DEBUGGING AND FIXING SEARCH RESULTS ANALYSIS ===\n")

# First, locate the workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    workspace_dir = workspace_dirs[0]
    print(f"Found workspace directory: {workspace_dir}")
else:
    print("No workspace directory found. Creating one...")
    workspace_dir = 'workspace'
    os.makedirs(workspace_dir, exist_ok=True)

print(f"\nInspecting files in {workspace_dir}:")
for file in os.listdir(workspace_dir):
    file_path = os.path.join(workspace_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"  - {file} ({file_size:,} bytes)")

# Look for search results file
search_files = [f for f in os.listdir(workspace_dir) if 'search_results' in f and f.endswith('.json')]

if search_files:
    search_file = search_files[0]
    search_file_path = os.path.join(workspace_dir, search_file)
    print(f"\nFound search results file: {search_file}")
    
    # First, inspect the structure before loading
    print("\n=== INSPECTING SEARCH RESULTS FILE STRUCTURE ===\n")
    
    with open(search_file_path, 'r') as f:
        # Read first 1000 characters to understand structure
        f.seek(0)
        sample_content = f.read(1000)
        print("First 1000 characters of file:")
        print(sample_content)
        print("...\n")
    
    # Now load and inspect the full structure
    with open(search_file_path, 'r') as f:
        try:
            search_data = json.load(f)
            print("Successfully loaded JSON data")
            print(f"Data type: {type(search_data)}")
            
            if isinstance(search_data, list):
                print(f"List with {len(search_data)} items")
                if search_data:
                    print("\nFirst item structure:")
                    first_item = search_data[0]
                    for key, value in first_item.items():
                        if isinstance(value, list):
                            print(f"  {key}: List with {len(value)} items")
                        elif isinstance(value, dict):
                            print(f"  {key}: Dictionary with {len(value)} keys")
                        else:
                            print(f"  {key}: {type(value).__name__} - {str(value)[:100]}...")
            
            elif isinstance(search_data, dict):
                print(f"Dictionary with {len(search_data)} keys")
                print("\nTop-level keys:")
                for key, value in search_data.items():
                    if isinstance(value, list):
                        print(f"  {key}: List with {len(value)} items")
                    elif isinstance(value, dict):
                        print(f"  {key}: Dictionary with {len(value)} keys")
                    else:
                        print(f"  {key}: {type(value).__name__} - {str(value)[:100]}...")
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("File may be corrupted or incomplete")
    
    print("\n=== CORRECTED ANALYSIS OF SEARCH RESULTS ===\n")
    
    # Now properly analyze the search results for Nature 2020 data
    with open(search_file_path, 'r') as f:
        search_data = json.load(f)
    
    # Handle different possible structures
    all_results = []
    
    if isinstance(search_data, list):
        # If it's a list of search query results
        for search_query_data in search_data:
            if isinstance(search_query_data, dict) and 'results' in search_query_data:
                query = search_query_data.get('query', 'Unknown query')
                results = search_query_data.get('results', [])
                print(f"Query: {query}")
                print(f"Results found: {len(results)}")
                all_results.extend(results)
            elif isinstance(search_query_data, dict):
                # Direct result format
                all_results.append(search_query_data)
    
    elif isinstance(search_data, dict):
        # If it's a single search result or has a different structure
        if 'organic_results' in search_data:
            all_results = search_data['organic_results']
        elif 'results' in search_data:
            all_results = search_data['results']
        else:
            # Treat the whole dict as a single result
            all_results = [search_data]
    
    print(f"\nTotal results to analyze: {len(all_results)}")
    
    # Now analyze for Nature journal 2020 research article information
    nature_related_results = []
    
    for i, result in enumerate(all_results):
        if not isinstance(result, dict):
            continue
            
        title = result.get('title', '').lower()
        url = result.get('link', result.get('url', ''))
        snippet = result.get('snippet', result.get('description', '')).lower()
        
        # Look for Nature journal related content with 2020 data
        relevance_indicators = {
            'nature_journal': 'nature' in title or 'nature' in snippet,
            'year_2020': '2020' in title or '2020' in snippet or '2020' in url,
            'publication_stats': any(term in title or term in snippet for term in ['publication', 'article', 'research', 'annual', 'report', 'statistics']),
            'official_nature': 'nature.com' in url,
            'editorial_content': any(term in title or term in snippet for term in ['editorial', 'annual review', 'year in review'])
        }
        
        relevance_score = sum(relevance_indicators.values())
        
        if relevance_score >= 2:  # At least 2 indicators must match
            nature_related_results.append({
                'title': result.get('title', 'No title'),
                'url': url,
                'snippet': result.get('snippet', result.get('description', 'No snippet')),
                'relevance_score': relevance_score,
                'indicators': {k: v for k, v in relevance_indicators.items() if v}
            })
    
    # Sort by relevance score
    nature_related_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"\n=== NATURE JOURNAL 2020 RELEVANT RESULTS ===\n")
    print(f"Found {len(nature_related_results)} relevant results:\n")
    
    for i, result in enumerate(nature_related_results[:10], 1):
        print(f"{i}. {result['title']}")
        print(f"   URL: {result['url']}")
        print(f"   Relevance Score: {result['relevance_score']}")
        print(f"   Matching Indicators: {list(result['indicators'].keys())}")
        print(f"   Snippet: {result['snippet'][:200]}...\n")
    
    # Save the corrected analysis
    corrected_analysis = {
        'total_search_results_analyzed': len(all_results),
        'nature_2020_relevant_results': len(nature_related_results),
        'top_relevant_sources': nature_related_results[:10],
        'analysis_timestamp': '2025-01-06',
        'search_focus': 'Nature journal 2020 research article count'
    }
    
    corrected_file = os.path.join(workspace_dir, 'corrected_nature_2020_analysis.json')
    with open(corrected_file, 'w') as f:
        json.dump(corrected_analysis, f, indent=2)
    
    print(f"=== CORRECTED ANALYSIS SAVED ===")
    print(f"Analysis saved to: {corrected_file}")
    print(f"Ready to proceed with accessing the most promising sources")
    
    if nature_related_results:
        print(f"\nNext step: Access top {min(3, len(nature_related_results))} most relevant sources")
        print("to extract Nature journal 2020 research article publication count")
    else:
        print("\nNo highly relevant sources found. Will need to try direct approach")
        print("to Nature journal website or alternative search strategies")
        
else:
    print("\nNo search results file found. Starting fresh search approach...")
    
    # If no previous search results, let's try a direct approach
    print("\n=== DIRECT APPROACH: NATURE JOURNAL 2020 RESEARCH ===\n")
    
    # Try to search for specific Nature 2020 information
    import requests
    
    api_key = os.getenv("SERPAPI_API_KEY")
    
    if api_key:
        print("Conducting focused search for Nature 2020 publication data...\n")
        
        # More specific queries for Nature journal data
        focused_queries = [
            'site:nature.com "2020" "articles published" OR "research articles"',
            '"Nature journal" "2020" "publication statistics" OR "annual report"',
            '"Nature" journal 2020 editorial "year in review" publications',
            'Nature.com 2020 "research articles" count statistics'
        ]
        
        focused_results = []
        
        for query in focused_queries:
            print(f"Searching: {query}")
            
            params = {
                "q": query,
                "api_key": api_key,
                "engine": "google",
                "num": 5
            }
            
            try:
                response = requests.get("https://serpapi.com/search.json", params=params)
                if response.status_code == 200:
                    results = response.json()
                    if results.get("organic_results"):
                        focused_results.extend(results["organic_results"])
                        print(f"  Found {len(results['organic_results'])} results")
                    else:
                        print("  No results found")
                else:
                    print(f"  Search failed: {response.status_code}")
            except Exception as e:
                print(f"  Error: {e}")
        
        if focused_results:
            focused_file = os.path.join(workspace_dir, 'focused_nature_2020_search.json')
            with open(focused_file, 'w') as f:
                json.dump(focused_results, f, indent=2)
            
            print(f"\nFocused search results saved to: {focused_file}")
            print(f"Found {len(focused_results)} total results to analyze")
        
    else:
        print("No API key available. Will try alternative approaches...")

print("\n=== DEBUG AND ANALYSIS PHASE COMPLETE ===")
print("\nFiles in workspace:")
for file in os.listdir(workspace_dir):
    file_path = os.path.join(workspace_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"  - {file} ({file_size:,} bytes)")
```

## Created Time
2025-08-14 15:17:23
