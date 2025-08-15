# Developer Plan 01

## Plan
Search ScienceDirect for information about Reference Works in Life Science domains and Health Sciences as of 2022. Look for data that shows the number of Reference Works categorized by different Life Science domains and Health Sciences. Focus on finding statistical data, databases, or research metrics that would contain sample counts for Reference Works across these academic domains.

## Description
This is the optimal first step because: (1) We need to locate the specific data about Reference Works on ScienceDirect for Life Science domains and Health Sciences as of 2022, (2) No previous research has been conducted yet, (3) Expected outcome is to identify the source of Reference Works data and extract the numerical counts for each domain, (4) This establishes the foundation needed to calculate sample standard deviations and find the difference between Life Science domains and Health Sciences

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
2025-08-14 18:48:03
