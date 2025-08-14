# Developer Plan 03

## Plan
Search the Smithsonian American Art Museum's collection to identify the two paintings whose titles are sourced from Thomas Hobbes' 'Leviathan' (1651). Use multiple search approaches: (1) Direct search of the Smithsonian American Art Museum online collection database using keywords 'Hobbes', 'Leviathan', and related terms, (2) Search for paintings with titles that quote or reference specific chapters from Leviathan, (3) Cross-reference the museum's Archives of American Art for any documentation connecting painting titles to Hobbes' work. Extract the complete titles of both paintings and identify which specific chapters from Leviathan they reference, noting the chapter numbers for final calculation.

## Description
This is the necessary next step because: (1) We have identified that Thomas Hobbes' 'Leviathan' is the source work referenced in footnote 397, but we need to find the specific paintings in the Smithsonian collection that quote from this work, (2) Previous analysis established the connection between the dissertation footnote and Smithsonian painting titles but we need the actual paintings and their chapter references, (3) Expected outcome is to locate both paintings with Leviathan-sourced titles and identify their respective chapter numbers, (4) This will provide the chapter numbers needed to calculate the absolute difference as requested in the TASK

## Episodic Examples
### Development Step 2: Metropolitan Museum Portrait Accession 29.100.5: Title, Artist, Subject, and Metadata Search

**Description**: Search for information about the Metropolitan Museum of Art portrait with accession number 29.100.5. Look for the artwork's title, artist, subject, and any available metadata or catalog information. Use multiple search approaches including: (1) Direct search on the Met Museum's official website and collection database, (2) Google search with terms 'Metropolitan Museum Art 29.100.5 accession portrait', (3) Art history databases and museum catalog searches. Extract complete details about the portrait including who is depicted in the artwork.

**Use Cases**:
- Museum collection management and automated metadata synchronization for accession 29.100.5 in digital archives
- Graduate art history research and batch extraction of portrait details for thematic analysis in academic publications
- Auction house provenance verification and authenticity checks using cross-referenced Met Museum accession metadata
- Virtual tour application development and real-time retrieval of portrait metadata for enhanced visitor engagement
- Digital marketing content enrichment and SEO optimization with official artwork titles and artist information
- Journalism fact-checking and rapid aggregation of catalog details for museum exhibit coverage
- Cultural heritage linked data integration and semantic querying across multiple collection APIs
- Conservation report automation and pre-population of restoration logs with Met Museum artwork metadata

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

print('=== METROPOLITAN MUSEUM OF ART PORTRAIT RESEARCH ===\n')
print('Target: Accession number 29.100.5')
print('Objective: Find artwork title, artist, subject, and complete metadata\n')

# Fix the syntax error by treating accession number as string
accession_number = '29.100.5'
print(f'Searching for accession number: {accession_number}')

# First, try to access the Met Museum's official collection database directly
print('Step 1: Attempting direct access to Met Museum collection database...')

# The Met has a public API and collection search
met_collection_urls = [
    f'https://www.metmuseum.org/art/collection/search/{accession_number}',
    f'https://www.metmuseum.org/art/collection/search?q={accession_number}',
    f'https://collectionapi.metmuseum.org/public/collection/v1/search?q={accession_number}',
    f'https://www.metmuseum.org/art/collection/search?accessionNumber={accession_number}'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

met_results = []
for i, url in enumerate(met_collection_urls):
    print(f'\nTrying Met URL {i+1}: {url}')
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f'Response status: {response.status_code}')
        
        if response.status_code == 200:
            print(f'✓ Successfully accessed {url}')
            
            # Save the response for analysis
            filename = f'workspace/met_direct_search_{i+1}.html'
            
            # Check if it's JSON or HTML
            try:
                json_data = response.json()
                filename = f'workspace/met_api_response_{i+1}.json'
                with open(filename, 'w') as f:
                    json.dump(json_data, f, indent=2)
                print(f'  Saved JSON response to: {filename}')
                print(f'  JSON keys: {list(json_data.keys()) if isinstance(json_data, dict) else "List with " + str(len(json_data)) + " items"}')
            except:
                # It's HTML
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f'  Saved HTML response to: {filename}')
                
                # Quick analysis of HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                title_text = title.get_text().strip() if title else 'No title found'
                print(f'  Page title: {title_text}')
                
                # Look for accession number mentions
                content_text = response.text.lower()
                if accession_number in content_text:
                    print('  *** ACCESSION NUMBER FOUND IN CONTENT ***')
                
                # Look for portrait/artwork indicators
                artwork_indicators = ['portrait', 'painting', 'artist', 'artwork', 'collection']
                found_indicators = [ind for ind in artwork_indicators if ind in content_text]
                if found_indicators:
                    print(f'  Artwork indicators found: {found_indicators}')
            
            met_results.append({
                'url': url,
                'status': response.status_code,
                'filename': filename,
                'content_length': len(response.text)
            })
            
        else:
            print(f'✗ Failed - Status: {response.status_code}')
            met_results.append({
                'url': url,
                'status': response.status_code,
                'error': f'HTTP {response.status_code}'
            })
            
    except Exception as e:
        print(f'✗ Error: {str(e)}')
        met_results.append({
            'url': url,
            'error': str(e)
        })
    
    time.sleep(2)  # Be respectful to servers

print(f'\n=== MET MUSEUM DIRECT SEARCH RESULTS ===\n')
print(f'Attempted {len(met_collection_urls)} direct Met Museum URLs')
successful_met = [r for r in met_results if r.get('status') == 200]
print(f'Successful responses: {len(successful_met)}')

for result in successful_met:
    print(f'  ✓ {result["url"]} -> {result["filename"]}')

# Now use Google Search API for comprehensive search
api_key = os.getenv("SERPAPI_API_KEY")

if api_key:
    print('\n=== GOOGLE SEARCH FOR MET PORTRAIT 29.100.5 ===\n')
    
    # Multiple search queries to maximize information gathering
    search_queries = [
        f'Metropolitan Museum Art {accession_number} accession portrait',
        f'Met Museum {accession_number} painting artwork collection',
        f'"{accession_number}" Metropolitan Museum portrait artist subject',
        f'metmuseum.org {accession_number} accession number artwork'
    ]
    
    google_results = []
    
    for i, query in enumerate(search_queries):
        print(f'Search {i+1}: "{query}"')
        
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 8
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            
            if response.status_code == 200:
                results = response.json()
                
                if results.get("organic_results"):
                    print(f'  Found {len(results["organic_results"])} results')
                    
                    for j, result in enumerate(results["organic_results"]):
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No link')
                        snippet = result.get('snippet', 'No snippet')
                        
                        print(f'\n    Result {j+1}:')
                        print(f'    Title: {title}')
                        print(f'    URL: {link}')
                        print(f'    Snippet: {snippet}')
                        
                        # Check for key information
                        combined_text = f'{title} {snippet}'.lower()
                        
                        key_findings = []
                        if accession_number in combined_text:
                            key_findings.append('Accession number found')
                        if 'portrait' in combined_text:
                            key_findings.append('Portrait mentioned')
                        if 'artist' in combined_text or 'painter' in combined_text:
                            key_findings.append('Artist information')
                        if 'metmuseum.org' in link:
                            key_findings.append('Official Met Museum source')
                        
                        if key_findings:
                            print(f'    *** KEY FINDINGS: {key_findings} ***')
                        
                        google_results.append({
                            'search_query': query,
                            'result_index': j+1,
                            'title': title,
                            'link': link,
                            'snippet': snippet,
                            'key_findings': key_findings
                        })
                else:
                    print('  No organic results found')
            else:
                print(f'  Search failed with status: {response.status_code}')
                
        except Exception as e:
            print(f'  Search error: {str(e)}')
        
        time.sleep(1)  # Rate limiting
    
    # Save all Google search results
    with open('workspace/met_29_100_5_google_results.json', 'w') as f:
        json.dump(google_results, f, indent=2)
    
    print(f'\nGoogle search results saved to: workspace/met_29_100_5_google_results.json')
    print(f'Total Google results collected: {len(google_results)}')
    
    # Identify most promising results
    priority_results = [r for r in google_results if r['key_findings']]
    print(f'Priority results with key findings: {len(priority_results)}')
    
else:
    print('\nNo SERPAPI key available - skipping Google search')
    google_results = []

# Compile initial research summary
research_summary = {
    'target_accession': accession_number,
    'museum': 'Metropolitan Museum of Art',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'direct_met_searches': {
        'attempted_urls': len(met_collection_urls),
        'successful_responses': len(successful_met),
        'results': met_results
    },
    'google_searches': {
        'queries_attempted': len(search_queries) if api_key else 0,
        'total_results': len(google_results),
        'priority_results': len([r for r in google_results if r.get('key_findings')]) if google_results else 0
    },
    'files_created': [
        f for f in os.listdir('workspace') 
        if f.startswith('met_') and (f.endswith('.html') or f.endswith('.json'))
    ]
}

with open('workspace/met_portrait_research_summary.json', 'w') as f:
    json.dump(research_summary, f, indent=2)

print(f'\n=== PHASE 1 RESEARCH COMPLETE ===\n')
print(f'Research summary saved to: workspace/met_portrait_research_summary.json')
print(f'Files created in workspace: {len(research_summary["files_created"])}')  
print(f'Next step: Analyze collected data to extract portrait details')

# Quick preview of findings
if successful_met:
    print(f'\n✓ Successfully accessed {len(successful_met)} Met Museum URLs')
if google_results:
    priority_count = len([r for r in google_results if r.get('key_findings')])
    print(f'✓ Found {priority_count} priority Google results with key information')

print('\nReady for detailed analysis of collected data...')
```

### Development Step 3: Met Museum Portrait Accession 29.100.5: Title, Artist, Subject & Complete Catalog Metadata

**Description**: Search for information about the Metropolitan Museum of Art portrait with accession number 29.100.5. Look for the artwork's title, artist, subject, and any available metadata or catalog information. Use multiple search approaches including: (1) Direct search on the Met Museum's official website and collection database, (2) Google search with terms 'Metropolitan Museum Art 29.100.5 accession portrait', (3) Art history databases and museum catalog searches. Extract complete details about the portrait including who is depicted in the artwork.

**Use Cases**:
- Automated catalog synchronization for museum registrars to ensure internal databases reflect the latest Met accession details (title, artist, medium, dimensions) without manual entry
- Art historical research pipeline that aggregates portrait metadata (artist dates, subject constituents, tags) across online museum collections for a comparative study of 18th‐century portraiture
- E-learning module generator for an online art history platform that programmatically pulls portrait data (objectDate, culture, classification) to create interactive lesson plans
- Digital marketing dashboard integration that fetches high-resolution images and object URLs from the Met API in real time for promoting featured artworks on social media
- Art investment analytics tool that extracts medium, artist provenance, and object dimensions to feed valuation models and auction readiness reports
- Virtual reality museum exhibit builder that retrieves primaryImage URLs and descriptive metadata to dynamically populate immersive gallery environments
- Cultural heritage aggregator system that ingests detailed constituent and tag information from multiple museum APIs (including the Met) to enrich a centralized Linked Open Data repository
- Conservation management software that automatically extracts material and dimension metadata to schedule condition assessments and preventive preservation tasks

```
import os
import json
from bs4 import BeautifulSoup
import re

print('=== PHASE 2: ANALYZING COLLECTED MET MUSEUM DATA ===\n')
print('Objective: Extract portrait details from collected HTML and JSON files\n')

# First, let's inspect the workspace directory and understand what files we have
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    workspace_dir = workspace_dirs[0]
    print(f'Found workspace directory: {workspace_dir}')
else:
    workspace_dir = 'workspace'
    print(f'Using default workspace directory: {workspace_dir}')

if os.path.exists(workspace_dir):
    files = os.listdir(workspace_dir)
    print(f'Files in {workspace_dir}: {files}\n')
    
    # Inspect each file to understand the data structure
    print('=== INSPECTING COLLECTED FILES ===\n')
    
    for filename in files:
        filepath = os.path.join(workspace_dir, filename)
        print(f'Analyzing: {filename}')
        
        if filename.endswith('.json'):
            # Inspect JSON structure first
            print('  File type: JSON')
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    print(f'  Structure: Dictionary with keys: {list(data.keys())}')
                    for key, value in data.items():
                        if isinstance(value, list):
                            print(f'    {key}: List with {len(value)} items')
                            if len(value) > 0:
                                print(f'      First item type: {type(value[0])}')
                                if len(value) <= 5:
                                    print(f'      Items: {value}')
                        elif isinstance(value, dict):
                            print(f'    {key}: Dictionary with {len(value)} keys')
                        else:
                            print(f'    {key}: {type(value).__name__} = {value}')
                elif isinstance(data, list):
                    print(f'  Structure: List with {len(data)} items')
                    if len(data) > 0:
                        print(f'    First item: {data[0]}')
                
            except Exception as e:
                print(f'  Error reading JSON: {e}')
        
        elif filename.endswith('.html'):
            # Inspect HTML structure
            print('  File type: HTML')
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                print(f'  Content length: {len(html_content)} characters')
                
                # Quick check for accession number
                if '29.100.5' in html_content:
                    print('  *** Contains accession number 29.100.5 ***')
                
                # Parse with BeautifulSoup to understand structure
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.find('title')
                if title:
                    print(f'  Page title: {title.get_text().strip()}')
                
                # Look for key elements that might contain artwork info
                artwork_elements = soup.find_all(['h1', 'h2', 'h3', 'div'], class_=re.compile(r'(artwork|title|artist|object)', re.I))
                if artwork_elements:
                    print(f'  Found {len(artwork_elements)} potential artwork elements')
                
            except Exception as e:
                print(f'  Error reading HTML: {e}')
        
        print()
    
    # Now let's focus on the most promising files - the API response and HTML files with accession number
    print('=== DETAILED ANALYSIS OF KEY FILES ===\n')
    
    # Start with the Met API JSON response
    api_files = [f for f in files if 'api_response' in f and f.endswith('.json')]
    if api_files:
        api_file = api_files[0]
        print(f'Analyzing Met API response: {api_file}')
        
        with open(os.path.join(workspace_dir, api_file), 'r') as f:
            api_data = json.load(f)
        
        print(f'API Response structure:')
        print(f'  Total results: {api_data.get("total", "Unknown")}')
        
        if 'objectIDs' in api_data and api_data['objectIDs']:
            object_ids = api_data['objectIDs']
            print(f'  Object IDs found: {len(object_ids)}')
            print(f'  Object IDs: {object_ids}')
            
            # The Met API requires a second call to get object details
            print('\n  Attempting to fetch detailed object information...')
            
            import requests
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            detailed_objects = []
            for obj_id in object_ids[:3]:  # Limit to first 3 objects to avoid overwhelming output
                try:
                    detail_url = f'https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}'
                    print(f'    Fetching: {detail_url}')
                    
                    response = requests.get(detail_url, headers=headers, timeout=15)
                    if response.status_code == 200:
                        obj_data = response.json()
                        detailed_objects.append(obj_data)
                        
                        # Check if this is our target object
                        acc_num = obj_data.get('accessionNumber', '')
                        title = obj_data.get('title', 'No title')
                        artist = obj_data.get('artistDisplayName', 'Unknown artist')
                        
                        print(f'      Object ID {obj_id}:')
                        print(f'        Accession: {acc_num}')
                        print(f'        Title: {title}')
                        print(f'        Artist: {artist}')
                        
                        if acc_num == '29.100.5':
                            print(f'        *** FOUND TARGET PORTRAIT! ***')
                            
                            # Extract complete details
                            portrait_details = {
                                'accession_number': acc_num,
                                'title': title,
                                'artist_display_name': artist,
                                'artist_begin_date': obj_data.get('artistBeginDate', ''),
                                'artist_end_date': obj_data.get('artistEndDate', ''),
                                'object_date': obj_data.get('objectDate', ''),
                                'medium': obj_data.get('medium', ''),
                                'dimensions': obj_data.get('dimensions', ''),
                                'department': obj_data.get('department', ''),
                                'culture': obj_data.get('culture', ''),
                                'period': obj_data.get('period', ''),
                                'classification': obj_data.get('classification', ''),
                                'object_url': obj_data.get('objectURL', ''),
                                'primary_image': obj_data.get('primaryImage', ''),
                                'repository': obj_data.get('repository', ''),
                                'object_name': obj_data.get('objectName', ''),
                                'tags': obj_data.get('tags', []),
                                'constituents': obj_data.get('constituents', [])
                            }
                            
                            # Save detailed portrait information
                            with open(os.path.join(workspace_dir, 'portrait_29_100_5_details.json'), 'w') as f:
                                json.dump(portrait_details, f, indent=2)
                            
                            print(f'\n=== PORTRAIT DETAILS EXTRACTED ===\n')
                            print(f'Accession Number: {portrait_details["accession_number"]}')
                            print(f'Title: {portrait_details["title"]}')
                            print(f'Artist: {portrait_details["artist_display_name"]}')
                            print(f'Artist Dates: {portrait_details["artist_begin_date"]} - {portrait_details["artist_end_date"]}')
                            print(f'Object Date: {portrait_details["object_date"]}')
                            print(f'Medium: {portrait_details["medium"]}')
                            print(f'Dimensions: {portrait_details["dimensions"]}')
                            print(f'Department: {portrait_details["department"]}')
                            print(f'Classification: {portrait_details["classification"]}')
                            print(f'Object URL: {portrait_details["object_url"]}')
                            
                            # Look for subject information in constituents or tags
                            if portrait_details['constituents']:
                                print(f'\nConstituents (subjects/people depicted):')
                                for constituent in portrait_details['constituents']:
                                    if isinstance(constituent, dict):
                                        name = constituent.get('name', 'Unknown')
                                        role = constituent.get('role', 'Unknown role')
                                        print(f'  - {name} ({role})')
                            
                            if portrait_details['tags']:
                                print(f'\nTags:')
                                for tag in portrait_details['tags'][:10]:  # Show first 10 tags
                                    if isinstance(tag, dict):
                                        term = tag.get('term', 'Unknown term')
                                        print(f'  - {term}')
                            
                            print(f'\nDetailed portrait information saved to: portrait_29_100_5_details.json')
                            break
                    else:
                        print(f'      Failed to fetch object {obj_id}: HTTP {response.status_code}')
                        
                except Exception as e:
                    print(f'      Error fetching object {obj_id}: {e}')
                
                import time
                time.sleep(1)  # Rate limiting
        else:
            print('  No object IDs found in API response')
    
    # Also analyze HTML files for additional context
    html_files = [f for f in files if f.endswith('.html') and '29.100.5' in open(os.path.join(workspace_dir, f), 'r', encoding='utf-8').read()]
    
    if html_files:
        print(f'\n=== ANALYZING HTML FILES WITH ACCESSION NUMBER ===\n')
        
        for html_file in html_files:
            print(f'Analyzing: {html_file}')
            
            with open(os.path.join(workspace_dir, html_file), 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for specific patterns around the accession number
            text_content = soup.get_text()
            lines = text_content.split('\n')
            
            # Find lines containing the accession number and surrounding context
            accession_context = []
            for i, line in enumerate(lines):
                if '29.100.5' in line:
                    # Get surrounding lines for context
                    start = max(0, i-3)
                    end = min(len(lines), i+4)
                    context_lines = lines[start:end]
                    accession_context.extend(context_lines)
            
            if accession_context:
                print('  Context around accession number:')
                for line in accession_context[:20]:  # Limit output
                    line = line.strip()
                    if line:
                        print(f'    {line}')
            
            print()

else:
    print(f'Workspace directory {workspace_dir} not found')

print('\n=== PHASE 2 ANALYSIS COMPLETE ===\n')
print('Successfully extracted portrait details from Met Museum API')
print('All artwork information has been compiled and saved to workspace files')
```

### Development Step 1: Search Met Museum Portrait Accession 29.100.5: Title, Artist, Subject, Metadata

**Description**: Search for information about the Metropolitan Museum of Art portrait with accession number 29.100.5. Look for the artwork's title, artist, subject, and any available metadata or catalog information. Use multiple search approaches including: (1) Direct search on the Met Museum's official website and collection database, (2) Google search with terms 'Metropolitan Museum Art 29.100.5 accession portrait', (3) Art history databases and museum catalog searches. Extract complete details about the portrait including who is depicted in the artwork.

**Use Cases**:
- Museum collections management and digital archive enrichment by automatically fetching accession 29.100.5 metadata from the Met Museum website into internal cataloging systems
- Art marketplace listing automation integrating real-time retrieval of official title, artist, and subject for artwork 29.100.5 to populate e-commerce product pages with authoritative museum data
- University art history research dataset compilation that bulk-scrapes portrait details (starting with accession 29.100.5) across multiple museum APIs for statistical analysis of 19th-century portraiture trends
- Educational platform content generation dynamically pulling high-resolution images and metadata of accession 29.100.5 to create interactive lecture slides and online course modules on portrait art
- Cultural heritage mobile guide app offering on-demand lookup of accession 29.100.5 details to deliver location-based audio tours and descriptive cards for museum visitors
- Art authentication and provenance verification service cross-referencing the Met’s accession 29.100.5 metadata via API and Google search results to confirm ownership history and artist attribution
- Digital humanities text analysis pipeline extracting and normalizing descriptive metadata (artist, subject, date) from accession 29.100.5 as part of a corpus for NLP-driven insights on art historical narratives
- Virtual reality exhibition builder fetching live metadata and imagery for accession 29.100.5 to automatically populate virtual gallery spaces with accurate artwork details and contextual information

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

print('=== METROPOLITAN MUSEUM OF ART PORTRAIT RESEARCH ===\n')
print('Target: Accession number 29.100.5')
print('Objective: Find artwork title, artist, subject, and complete metadata\n')

# First, try to access the Met Museum's official collection database directly
print('Step 1: Attempting direct access to Met Museum collection database...')

# The Met has a public API and collection search
met_collection_urls = [
    f'https://www.metmuseum.org/art/collection/search/{29.100.5}',
    f'https://www.metmuseum.org/art/collection/search?q=29.100.5',
    'https://collectionapi.metmuseum.org/public/collection/v1/search?q=29.100.5',
    'https://www.metmuseum.org/art/collection/search?accessionNumber=29.100.5'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

met_results = []
for i, url in enumerate(met_collection_urls):
    print(f'\nTrying Met URL {i+1}: {url}')
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f'Response status: {response.status_code}')
        
        if response.status_code == 200:
            print(f'✓ Successfully accessed {url}')
            
            # Save the response for analysis
            filename = f'workspace/met_direct_search_{i+1}.html'
            
            # Check if it's JSON or HTML
            try:
                json_data = response.json()
                filename = f'workspace/met_api_response_{i+1}.json'
                with open(filename, 'w') as f:
                    json.dump(json_data, f, indent=2)
                print(f'  Saved JSON response to: {filename}')
                print(f'  JSON keys: {list(json_data.keys()) if isinstance(json_data, dict) else "List with " + str(len(json_data)) + " items"}')
            except:
                # It's HTML
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f'  Saved HTML response to: {filename}')
                
                # Quick analysis of HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                title_text = title.get_text().strip() if title else 'No title found'
                print(f'  Page title: {title_text}')
                
                # Look for accession number mentions
                content_text = response.text.lower()
                if '29.100.5' in content_text:
                    print('  *** ACCESSION NUMBER FOUND IN CONTENT ***')
                
                # Look for portrait/artwork indicators
                artwork_indicators = ['portrait', 'painting', 'artist', 'artwork', 'collection']
                found_indicators = [ind for ind in artwork_indicators if ind in content_text]
                if found_indicators:
                    print(f'  Artwork indicators found: {found_indicators}')
            
            met_results.append({
                'url': url,
                'status': response.status_code,
                'filename': filename,
                'content_length': len(response.text)
            })
            
        else:
            print(f'✗ Failed - Status: {response.status_code}')
            met_results.append({
                'url': url,
                'status': response.status_code,
                'error': f'HTTP {response.status_code}'
            })
            
    except Exception as e:
        print(f'✗ Error: {str(e)}')
        met_results.append({
            'url': url,
            'error': str(e)
        })
    
    time.sleep(2)  # Be respectful to servers

print(f'\n=== MET MUSEUM DIRECT SEARCH RESULTS ===\n')
print(f'Attempted {len(met_collection_urls)} direct Met Museum URLs')
successful_met = [r for r in met_results if r.get('status') == 200]
print(f'Successful responses: {len(successful_met)}')

for result in successful_met:
    print(f'  ✓ {result["url"]} -> {result["filename"]}')

# Now use Google Search API for comprehensive search
api_key = os.getenv("SERPAPI_API_KEY")

if api_key:
    print('\n=== GOOGLE SEARCH FOR MET PORTRAIT 29.100.5 ===\n')
    
    # Multiple search queries to maximize information gathering
    search_queries = [
        'Metropolitan Museum Art 29.100.5 accession portrait',
        'Met Museum 29.100.5 painting artwork collection',
        '"29.100.5" Metropolitan Museum portrait artist subject',
        'metmuseum.org 29.100.5 accession number artwork'
    ]
    
    google_results = []
    
    for i, query in enumerate(search_queries):
        print(f'Search {i+1}: "{query}"')
        
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 8
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            
            if response.status_code == 200:
                results = response.json()
                
                if results.get("organic_results"):
                    print(f'  Found {len(results["organic_results"])} results')
                    
                    for j, result in enumerate(results["organic_results"]):
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No link')
                        snippet = result.get('snippet', 'No snippet')
                        
                        print(f'\n    Result {j+1}:')
                        print(f'    Title: {title}')
                        print(f'    URL: {link}')
                        print(f'    Snippet: {snippet}')
                        
                        # Check for key information
                        combined_text = f'{title} {snippet}'.lower()
                        
                        key_findings = []
                        if '29.100.5' in combined_text:
                            key_findings.append('Accession number found')
                        if 'portrait' in combined_text:
                            key_findings.append('Portrait mentioned')
                        if 'artist' in combined_text or 'painter' in combined_text:
                            key_findings.append('Artist information')
                        if 'metmuseum.org' in link:
                            key_findings.append('Official Met Museum source')
                        
                        if key_findings:
                            print(f'    *** KEY FINDINGS: {key_findings} ***')
                        
                        google_results.append({
                            'search_query': query,
                            'result_index': j+1,
                            'title': title,
                            'link': link,
                            'snippet': snippet,
                            'key_findings': key_findings
                        })
                else:
                    print('  No organic results found')
            else:
                print(f'  Search failed with status: {response.status_code}')
                
        except Exception as e:
            print(f'  Search error: {str(e)}')
        
        time.sleep(1)  # Rate limiting
    
    # Save all Google search results
    with open('workspace/met_29_100_5_google_results.json', 'w') as f:
        json.dump(google_results, f, indent=2)
    
    print(f'\nGoogle search results saved to: workspace/met_29_100_5_google_results.json')
    print(f'Total Google results collected: {len(google_results)}')
    
    # Identify most promising results
    priority_results = [r for r in google_results if r['key_findings']]
    print(f'Priority results with key findings: {len(priority_results)}')
    
else:
    print('\nNo SERPAPI key available - skipping Google search')
    google_results = []

# Compile initial research summary
research_summary = {
    'target_accession': '29.100.5',
    'museum': 'Metropolitan Museum of Art',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'direct_met_searches': {
        'attempted_urls': len(met_collection_urls),
        'successful_responses': len(successful_met),
        'results': met_results
    },
    'google_searches': {
        'queries_attempted': len(search_queries) if api_key else 0,
        'total_results': len(google_results),
        'priority_results': len([r for r in google_results if r.get('key_findings')]) if google_results else 0
    },
    'files_created': [
        f for f in os.listdir('workspace') 
        if f.startswith('met_') and (f.endswith('.html') or f.endswith('.json'))
    ]
}

with open('workspace/met_portrait_research_summary.json', 'w') as f:
    json.dump(research_summary, f, indent=2)

print(f'\n=== PHASE 1 RESEARCH COMPLETE ===\n')
print(f'Research summary saved to: workspace/met_portrait_research_summary.json')
print(f'Files created in workspace: {len(research_summary["files_created"])}')
print(f'Next step: Analyze collected data to extract portrait details')

# Quick preview of findings
if successful_met:
    print(f'\n✓ Successfully accessed {len(successful_met)} Met Museum URLs')
if google_results:
    priority_count = len([r for r in google_results if r.get('key_findings')])
    print(f'✓ Found {priority_count} priority Google results with key information')

print('\nReady for detailed analysis of collected data...')
```

### Development Step 9: Download Westerink’s "A Dark Trace" from Project MUSE and Extract Chapter 2’s Influential Author

**Description**: Access and download the full text of 'A Dark Trace: Sigmund Freud on the Sense of Guilt' by H. Westerink from Project MUSE using DOI 10.1353/book.24372. Since the book was confirmed to be open access, retrieve the complete text and save it to workspace/dark_trace_freud_book.pdf or appropriate format. Focus on locating and extracting Chapter 2 content to identify the author who influenced Freud's belief in 'endopsychic myths'. If the full book is not directly downloadable, extract Chapter 2 specifically or access the book's table of contents to determine the exact chapter title and content structure.

**Use Cases**:
- Legal due diligence in corporate mergers: automatically download open-access regulatory codes in PDF, search for “antitrust” and “competition” term variations, extract and summarize context to identify potential deal blockers.
- Pharmaceutical literature review automation: fetch clinical trial protocols via DOI, load full-text PDFs, search for “double-blind” and “placebo” mentions, and extract methodological passages along with author names for evidence synthesis.
- Patent portfolio analysis for semiconductor R&D: retrieve patent documents from public repositories, scan PDFs for “heterojunction” and “quantum well” variants, extract inventor citations and contextual explanations to map technology lineage.
- Historical philosophy research on Nietzsche and Kant: access digitized editions of 19th-century works, locate references to “categorical imperative” or “will to power,” and extract surrounding paragraphs to trace cross-author influences.
- Competitive intelligence from SEC filings: download publicly available 10-K and 10-Q reports, search for “risk factor,” “liquidity risk,” and “market volatility” variations, and pull relevant excerpts for financial analysis dashboards.
- Academic curriculum design from open textbooks: ingest complete PDF textbooks via DOIs, locate chapter summaries or “learning objectives” headings, extract and compile structured outlines for course syllabi.
- Investigative journalism document mining: import leaked policy PDFs, search for “whistleblower,” “confidential,” and “internal memo” terms, extract context with names and dates to support storytelling.
- Compliance monitoring in healthcare: load clinical guideline PDFs, scan for “contraindication,” “adverse effect,” and “off-label” variations, and extract detailed sections with authoring bodies for automated policy updates.

```
from langchain_community.document_loaders import PyPDFLoader
import os
import json

print('=== SEARCHING ENTIRE BOOK FOR "ENDOPSYCHIC MYTHS" REFERENCES ===')
print('Objective: Since Chapter 2 did not contain "endopsychic" references, search the complete book to locate this specific term and identify the influencing author\n')

# Load the PDF and search the entire document
workspace_files = os.listdir('workspace')
pdf_files = [f for f in workspace_files if f.endswith('.pdf')]

if pdf_files:
    pdf_path = os.path.join('workspace', pdf_files[0])
    print(f'Searching entire PDF: {pdf_path}')
    
    try:
        # Load the complete PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        print(f'✓ PDF loaded successfully')
        print(f'Total pages to search: {len(pages)}')
        
        # Combine all pages into full text
        full_text = '\n\n'.join([page.page_content for page in pages])
        print(f'Total document length: {len(full_text):,} characters')
        
        # Search for "endopsychic" variations
        endopsychic_variations = [
            'endopsychic myth',
            'endopsychic myths',
            'endopsychic',
            'endo-psychic',
            'endopsychical'
        ]
        
        print('\n=== SEARCHING FOR ENDOPSYCHIC VARIATIONS ===')
        
        found_endopsychic = False
        full_text_lower = full_text.lower()
        
        for variation in endopsychic_variations:
            count = full_text_lower.count(variation.lower())
            if count > 0:
                print(f'✓ Found "{variation}": {count} occurrences')
                found_endopsychic = True
                
                # Extract all positions for this variation
                positions = []
                start = 0
                while True:
                    pos = full_text_lower.find(variation.lower(), start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + 1
                
                print(f'\n--- EXTRACTING ALL "{variation.upper()}" REFERENCES ({len(positions)} found) ---')
                
                for i, pos in enumerate(positions, 1):
                    # Extract substantial context around each occurrence
                    context_start = max(0, pos - 1000)
                    context_end = min(len(full_text), pos + 1200)
                    context = full_text[context_start:context_end]
                    
                    # Determine which page this occurs on
                    char_count = 0
                    page_num = 0
                    for page_idx, page in enumerate(pages):
                        if char_count + len(page.page_content) >= pos:
                            page_num = page_idx + 1
                            break
                        char_count += len(page.page_content) + 2  # +2 for \n\n separator
                    
                    print(f'\n🎯 REFERENCE {i} - Position {pos} (Page ~{page_num}):')
                    print('='*120)
                    print(context)
                    print('='*120)
                    
                    # Analyze this passage for author influences
                    context_lower = context.lower()
                    potential_authors = [
                        'jung', 'carl jung', 'c.g. jung', 'c. g. jung',
                        'nietzsche', 'friedrich nietzsche', 'f. nietzsche',
                        'schopenhauer', 'arthur schopenhauer', 'a. schopenhauer',
                        'kant', 'immanuel kant', 'i. kant',
                        'darwin', 'charles darwin', 'c. darwin',
                        'hegel', 'georg hegel', 'g.w.f. hegel',
                        'goethe', 'johann wolfgang von goethe',
                        'lamarck', 'jean-baptiste lamarck'
                    ]
                    
                    mentioned_authors = []
                    for author in potential_authors:
                        if author in context_lower:
                            mentioned_authors.append(author)
                    
                    if mentioned_authors:
                        print(f'\n*** AUTHORS MENTIONED IN THIS PASSAGE: {[author.title() for author in mentioned_authors]} ***')
                        
                        # Look for specific influence language
                        influence_phrases = [
                            'influenced by', 'influence of', 'influenced freud',
                            'borrowed from', 'adopted from', 'derived from',
                            'took from', 'learned from', 'inspired by',
                            'following', 'based on', 'according to'
                        ]
                        
                        found_influence_language = []
                        for phrase in influence_phrases:
                            if phrase in context_lower:
                                found_influence_language.append(phrase)
                        
                        if found_influence_language:
                            print(f'🔍 INFLUENCE LANGUAGE DETECTED: {found_influence_language}')
                            print('\n🎯 THIS PASSAGE LIKELY CONTAINS THE ANSWER! 🎯')
                        
                        # Look for direct statements about endopsychic myths
                        myth_context_phrases = [
                            'concept of endopsychic', 'idea of endopsychic', 'notion of endopsychic',
                            'endopsychic concept', 'endopsychic idea', 'endopsychic notion',
                            'belief in endopsychic', 'theory of endopsychic'
                        ]
                        
                        found_myth_context = []
                        for phrase in myth_context_phrases:
                            if phrase in context_lower:
                                found_myth_context.append(phrase)
                        
                        if found_myth_context:
                            print(f'💡 ENDOPSYCHIC CONCEPT LANGUAGE: {found_myth_context}')
                    
                    else:
                        print('\nNo specific authors mentioned in this immediate passage')
                        print('Searching for author names in broader context...')
                        
                        # Expand search area for author names
                        expanded_start = max(0, pos - 2000)
                        expanded_end = min(len(full_text), pos + 2000)
                        expanded_context = full_text[expanded_start:expanded_end]
                        expanded_lower = expanded_context.lower()
                        
                        broader_authors = []
                        for author in potential_authors:
                            if author in expanded_lower:
                                broader_authors.append(author)
                        
                        if broader_authors:
                            print(f'Authors in broader context: {[author.title() for author in broader_authors]}')
                    
                    print(f'\n{"-"*120}\n')
            else:
                print(f'✗ "{variation}": Not found')
        
        if not found_endopsychic:
            print('\n⚠ No "endopsychic" variations found in the entire document')
            print('The term may be referenced differently or may not be the exact phrase used')
            
            # Search for related mythological concepts that might be the actual term
            print('\n=== SEARCHING FOR ALTERNATIVE MYTHOLOGICAL CONCEPTS ===')
            
            alternative_terms = [
                'unconscious myth',
                'psychic myth',
                'mental myth',
                'psychological myth',
                'inner myth',
                'primitive myth',
                'ancestral memory',
                'collective unconscious',
                'phylogenetic',
                'archaic heritage',
                'primal fantasies',
                'inherited memory'
            ]
            
            found_alternatives = []
            
            for term in alternative_terms:
                count = full_text_lower.count(term.lower())
                if count > 0:
                    found_alternatives.append((term, count))
                    print(f'✓ Found "{term}": {count} occurrences')
            
            if found_alternatives:
                print(f'\n=== EXAMINING TOP ALTERNATIVE CONCEPTS ===')
                
                # Focus on the most promising alternative (highest count)
                top_alternative = max(found_alternatives, key=lambda x: x[1])
                term, count = top_alternative
                
                print(f'\nExamining most frequent alternative: "{term}" ({count} occurrences)')
                
                positions = []
                start = 0
                while True:
                    pos = full_text_lower.find(term.lower(), start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + 1
                
                # Show first few occurrences
                for i, pos in enumerate(positions[:3], 1):
                    context_start = max(0, pos - 800)
                    context_end = min(len(full_text), pos + 1000)
                    context = full_text[context_start:context_end]
                    
                    # Determine page number
                    char_count = 0
                    page_num = 0
                    for page_idx, page in enumerate(pages):
                        if char_count + len(page.page_content) >= pos:
                            page_num = page_idx + 1
                            break
                        char_count += len(page.page_content) + 2
                    
                    print(f'\nAlternative Reference {i} - "{term}" (Page ~{page_num}):')
                    print('='*100)
                    print(context)
                    print('='*100)
                    
                    # Check for author influences
                    context_lower = context.lower()
                    mentioned_authors = []
                    for author in ['jung', 'nietzsche', 'schopenhauer', 'kant', 'darwin', 'lamarck']:
                        if author in context_lower:
                            mentioned_authors.append(author)
                    
                    if mentioned_authors:
                        print(f'\nAuthors mentioned: {[a.title() for a in mentioned_authors]}')
                    
                    print(f'\n{"-"*100}\n')
        
        # Also search for direct references to key authors with mythological context
        print('\n=== SEARCHING FOR AUTHORS WITH MYTHOLOGICAL/INHERITANCE CONTEXT ===')
        
        key_authors_with_context = [
            ('jung', ['myth', 'mythology', 'collective', 'archetype']),
            ('lamarck', ['inheritance', 'inherited', 'acquired', 'transmission']),
            ('darwin', ['inheritance', 'heredity', 'evolution', 'acquired']),
            ('nietzsche', ['myth', 'mythology', 'cultural', 'psychological'])
        ]
        
        for author, context_terms in key_authors_with_context:
            author_positions = []
            start = 0
            while True:
                pos = full_text_lower.find(author.lower(), start)
                if pos == -1:
                    break
                author_positions.append(pos)
                start = pos + 1
            
            if author_positions:
                print(f'\n--- {author.upper()} REFERENCES WITH MYTHOLOGICAL CONTEXT ---')
                
                relevant_passages = []
                for pos in author_positions:
                    context_start = max(0, pos - 500)
                    context_end = min(len(full_text), pos + 700)
                    context = full_text[context_start:context_end]
                    context_lower = context.lower()
                    
                    # Check if this passage contains relevant mythological context
                    has_context = any(term in context_lower for term in context_terms)
                    if has_context:
                        relevant_passages.append((pos, context))
                
                if relevant_passages:
                    print(f'Found {len(relevant_passages)} relevant passages for {author.title()}:')
                    
                    for i, (pos, context) in enumerate(relevant_passages[:2], 1):
                        # Determine page
                        char_count = 0
                        page_num = 0
                        for page_idx, page in enumerate(pages):
                            if char_count + len(page.page_content) >= pos:
                                page_num = page_idx + 1
                                break
                            char_count += len(page.page_content) + 2
                        
                        print(f'\n{author.title()} Passage {i} (Page ~{page_num}):')
                        print('='*90)
                        print(context)
                        print('='*90)
                else:
                    print(f'No mythological context found for {author.title()}')
        
        # Save comprehensive search results
        search_results = {
            'search_objective': 'Find author who influenced Freud\'s belief in "endopsychic myths"',
            'document_stats': {
                'total_pages': len(pages),
                'total_characters': len(full_text)
            },
            'endopsychic_search': {
                'variations_searched': endopsychic_variations,
                'found_endopsychic': found_endopsychic,
                'total_occurrences': sum(full_text_lower.count(v.lower()) for v in endopsychic_variations)
            },
            'alternative_terms_found': found_alternatives if 'found_alternatives' in locals() else [],
            'search_timestamp': '2025-01-21 13:00:00'
        }
        
        results_file = 'workspace/complete_book_endopsychic_search_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print(f'\n*** COMPLETE BOOK SEARCH RESULTS ***')
        print(f'✓ Searched {len(pages)} pages ({len(full_text):,} characters)')
        print(f'✓ Endopsychic references found: {found_endopsychic}')
        
        if found_endopsychic:
            print('🎯 SUCCESS: Found "endopsychic" references in the book!')
            print('The extracted passages above should reveal the author who influenced Freud')
        else:
            print('⚠ "Endopsychic" not found - the term may be referenced differently')
            if 'found_alternatives' in locals() and found_alternatives:
                print(f'Alternative concepts found: {[term for term, count in found_alternatives]}')
        
        print(f'✓ Complete search results saved to: {results_file}')
        
    except Exception as e:
        print(f'❌ Error during complete book search: {str(e)}')

else:
    print('❌ No PDF files found in workspace')

print('\n=== COMPLETE BOOK SEARCH FINISHED ===')
print('Objective: Locate the specific author who influenced Freud\'s concept of "endopsychic myths"')
print('Status: Comprehensive search of entire book completed')
```

## Created Time
2025-08-14 04:52:47
