# Developer Plan 01

## Plan
Research the location of the National Air and Space Museum east of the Potomac River in Washington DC to identify which specific museum building this refers to and determine the nearest Metro station. Since there are multiple Air and Space Museum locations, focus on identifying which one is east of the Potomac River and find its closest Metro station access point.

## Description
This is the optimal first step because: (1) We need to establish the starting point by identifying which National Air and Space Museum location is east of the Potomac River and its nearest Metro station, (2) No previous research has been conducted on this navigation problem, (3) Expected outcome is to identify the specific museum location and its Metro station access, (4) This provides the foundation needed to then locate Fire Station 301 DCA ARFF and Cleveland Elementary School to solve the routing problem

## Episodic Examples
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

### Development Step 2: Charles 'Pete' Conrad: NASA Astronaut Group Membership and Selection Year Identification

**Description**: Research Charles 'Pete' Conrad's NASA Astronaut Group membership to determine which astronaut group he belonged to. Look for official NASA records, astronaut biographies, or space agency databases that specify Conrad's astronaut group number and selection year. This information is typically found in NASA's official astronaut biographical data or space history resources.

**Use Cases**:
- Space history researchers compiling detailed astronaut biographies for publication or archival purposes
- Museum curators verifying astronaut group memberships for accurate exhibit labeling and educational displays
- Documentary filmmakers fact-checking astronaut selection details for on-screen graphics and narration
- Aerospace educators preparing classroom materials on NASA astronaut selection processes and group histories
- Journalists writing feature articles about Apollo missions and needing authoritative astronaut group information
- NASA archivists digitizing and cross-referencing astronaut records for internal databases and public access
- Genealogists or family historians tracing the careers of relatives involved in the space program
- Science podcast producers sourcing verified astronaut background details for episode scripts and interviews

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

print("=== RESEARCH: CHARLES 'PETE' CONRAD'S NASA ASTRONAUT GROUP ===\n")
print("Objective: Determine which NASA astronaut group Charles 'Pete' Conrad belonged to and his selection year\n")

# Create workspace directory if needed
if not os.path.exists('workspace'):
    os.makedirs('workspace')
    print("Created workspace directory")

# From the previous APOD analysis, we know Charles 'Pete' Conrad was an Apollo 12 astronaut
# Let's research his NASA astronaut group membership using official NASA sources

print("=== APPROACH 1: NASA OFFICIAL ASTRONAUT BIOGRAPHY ===\n")

# NASA maintains official astronaut biographies
nasa_astronaut_urls = [
    "https://www.nasa.gov/people/charles-pete-conrad/",
    "https://www.nasa.gov/astronauts/biographies/charles-conrad.html",
    "https://history.nasa.gov/SP-4029/Apollo_12a_Conrad_Biography.htm",
    "https://www.jsc.nasa.gov/Bios/htmlbios/conrad-cp.html"
]

print(f"Attempting to access {len(nasa_astronaut_urls)} potential NASA biography URLs for Charles Conrad...\n")

conrad_bio_data = []

for i, url in enumerate(nasa_astronaut_urls, 1):
    print(f"URL {i}: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"  ✓ Successfully accessed (Status: {response.status_code})")
            print(f"  Content length: {len(response.content):,} bytes")
            
            # Parse the content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract page title
            page_title = soup.find('title')
            title_text = page_title.get_text().strip() if page_title else 'No title found'
            print(f"  Page title: {title_text}")
            
            # Save the HTML content
            html_filename = f'workspace/conrad_bio_{i}.html'
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  ✓ HTML saved to: {html_filename}")
            
            # Extract text content
            page_text = soup.get_text()
            
            # Search for astronaut group information
            print(f"\n  === SEARCHING FOR ASTRONAUT GROUP INFORMATION ===\n")
            
            # Key phrases that indicate astronaut group membership
            group_keywords = [
                'astronaut group',
                'group 2',
                'group two', 
                'second group',
                'selected',
                'selection',
                'chosen',
                'recruited',
                '1962',  # Group 2 was selected in 1962
                'new nine',  # Group 2 was known as "The New Nine"
                'next nine'
            ]
            
            found_keywords = []
            keyword_contexts = []
            
            for keyword in group_keywords:
                if keyword.lower() in page_text.lower():
                    found_keywords.append(keyword)
                    
                    # Find context around the keyword
                    import re
                    matches = list(re.finditer(re.escape(keyword), page_text, re.IGNORECASE))
                    
                    for match in matches[:2]:  # Show first 2 matches
                        start = max(0, match.start() - 200)
                        end = min(len(page_text), match.end() + 300)
                        context = page_text[start:end].strip()
                        
                        keyword_contexts.append({
                            'keyword': keyword,
                            'context': context
                        })
                        
                        print(f"  Found '{keyword}' - Context: ...{context[:150]}...")
            
            # Look for specific years and group numbers
            print(f"\n  === SEARCHING FOR SPECIFIC DATES AND GROUP NUMBERS ===\n")
            
            # Search for patterns like "Group 2", "1962", etc.
            group_patterns = [
                r'[Gg]roup\s+(\d+|[Tt]wo|2)',
                r'(\d{4})\s+astronaut',
                r'astronaut\s+(\d{4})',
                r'selected\s+in\s+(\d{4})',
                r'chosen\s+in\s+(\d{4})',
                r'[Nn]ew\s+[Nn]ine',
                r'[Nn]ext\s+[Nn]ine'
            ]
            
            pattern_matches = []
            
            for pattern in group_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                if matches:
                    print(f"  Pattern '{pattern}' found: {matches}")
                    pattern_matches.extend(matches)
                    
                    # Get context for these matches
                    for match_obj in re.finditer(pattern, page_text, re.IGNORECASE):
                        start = max(0, match_obj.start() - 150)
                        end = min(len(page_text), match_obj.end() + 150)
                        context = page_text[start:end].strip()
                        print(f"    Context: ...{context}...")
            
            # Store biography data
            bio_entry = {
                'url': url,
                'url_number': i,
                'title': title_text,
                'html_filename': html_filename,
                'content_length': len(page_text),
                'found_keywords': found_keywords,
                'keyword_contexts': keyword_contexts,
                'pattern_matches': pattern_matches,
                'access_successful': True
            }
            
            conrad_bio_data.append(bio_entry)
            
            # Save clean text for this biography
            text_filename = f'workspace/conrad_bio_{i}_text.txt'
            with open(text_filename, 'w', encoding='utf-8') as f:
                f.write(f"Charles 'Pete' Conrad Biography - Source {i}\n")
                f.write(f"URL: {url}\n")
                f.write(f"Title: {title_text}\n")
                f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 80 + "\n")
                f.write(page_text)
            
            print(f"  ✓ Text saved to: {text_filename}")
            
        elif response.status_code == 404:
            print(f"  ✗ Page not found (404)")
            conrad_bio_data.append({
                'url': url,
                'url_number': i,
                'access_successful': False,
                'error': '404 Not Found'
            })
        else:
            print(f"  ✗ Failed to access (Status: {response.status_code})")
            conrad_bio_data.append({
                'url': url,
                'url_number': i,
                'access_successful': False,
                'error': f'HTTP {response.status_code}'
            })
            
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        conrad_bio_data.append({
            'url': url,
            'url_number': i,
            'access_successful': False,
            'error': str(e)
        })
    
    print()  # Space between URLs

print("=== APPROACH 2: NASA ASTRONAUT GROUP HISTORICAL RECORDS ===\n")

# Access NASA's historical astronaut group information
nasa_group_urls = [
    "https://www.nasa.gov/astronauts/",
    "https://history.nasa.gov/SP-4029/Apollo_00g_Table_of_Contents.htm",
    "https://www.jsc.nasa.gov/history/oral_histories/astronauts.htm",
    "https://en.wikipedia.org/wiki/NASA_Astronaut_Group_2"  # As a reference source
]

print(f"Accessing {len(nasa_group_urls)} NASA astronaut group historical sources...\n")

group_data = []

for i, url in enumerate(nasa_group_urls, 1):
    print(f"Group Source {i}: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"  ✓ Successfully accessed (Status: {response.status_code})")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            # Save HTML
            group_html_filename = f'workspace/astronaut_groups_{i}.html'
            with open(group_html_filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"  ✓ HTML saved to: {group_html_filename}")
            
            # Search for Conrad specifically in group listings
            print(f"\n  === SEARCHING FOR CONRAD IN GROUP LISTINGS ===\n")
            
            conrad_patterns = [
                'Conrad',
                'Pete Conrad',
                'Charles Conrad',
                'C. Conrad',
                'Charles \"Pete\" Conrad',
                'Charles P. Conrad'
            ]
            
            conrad_found = False
            conrad_contexts = []
            
            for pattern in conrad_patterns:
                if pattern in page_text:
                    conrad_found = True
                    print(f"  ★ Found '{pattern}' in group source")
                    
                    # Get context around Conrad's name
                    import re
                    matches = list(re.finditer(re.escape(pattern), page_text, re.IGNORECASE))
                    
                    for match in matches[:2]:  # Show first 2 matches
                        start = max(0, match.start() - 250)
                        end = min(len(page_text), match.end() + 250)
                        context = page_text[start:end].strip()
                        
                        conrad_contexts.append({
                            'pattern': pattern,
                            'context': context
                        })
                        
                        print(f"    Context: ...{context[:200]}...")
                    break  # Found Conrad, no need to check other patterns
            
            if not conrad_found:
                print(f"  Conrad not found in this source")
            
            # Look for Group 2 or "New Nine" information
            print(f"\n  === SEARCHING FOR GROUP 2 / NEW NINE INFORMATION ===\n")
            
            group2_keywords = [
                'Group 2',
                'group two',
                'New Nine',
                'Next Nine',
                'second group',
                '1962',
                'September 1962'
            ]
            
            group2_info = []
            
            for keyword in group2_keywords:
                if keyword.lower() in page_text.lower():
                    print(f"  Found '{keyword}' in group source")
                    
                    # Get context
                    matches = list(re.finditer(re.escape(keyword), page_text, re.IGNORECASE))
                    
                    for match in matches[:1]:  # Show first match
                        start = max(0, match.start() - 300)
                        end = min(len(page_text), match.end() + 400)
                        context = page_text[start:end].strip()
                        
                        group2_info.append({
                            'keyword': keyword,
                            'context': context
                        })
                        
                        print(f"    Context: ...{context[:250]}...")
            
            group_entry = {
                'url': url,
                'source_number': i,
                'html_filename': group_html_filename,
                'conrad_found': conrad_found,
                'conrad_contexts': conrad_contexts,
                'group2_info': group2_info,
                'access_successful': True
            }
            
            group_data.append(group_entry)
            
        else:
            print(f"  ✗ Failed to access (Status: {response.status_code})")
            group_data.append({
                'url': url,
                'source_number': i,
                'access_successful': False,
                'error': f'HTTP {response.status_code}'
            })
            
    except Exception as e:
        print(f"  ✗ Exception: {str(e)}")
        group_data.append({
            'url': url,
            'source_number': i,
            'access_successful': False,
            'error': str(e)
        })
    
    print()  # Space between sources

print("=== COMPREHENSIVE ANALYSIS AND SUMMARY ===\n")

# Compile all findings
research_summary = {
    'research_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'objective': "Determine Charles 'Pete' Conrad's NASA astronaut group membership",
    'astronaut_name': "Charles 'Pete' Conrad",
    'biography_sources': conrad_bio_data,
    'group_sources': group_data,
    'successful_bio_accesses': len([entry for entry in conrad_bio_data if entry.get('access_successful')]),
    'successful_group_accesses': len([entry for entry in group_data if entry.get('access_successful')])
}

# Analyze findings for astronaut group determination
print("FINDINGS ANALYSIS:")
print(f"Successfully accessed {research_summary['successful_bio_accesses']} biography sources")
print(f"Successfully accessed {research_summary['successful_group_accesses']} group sources")

# Look for consistent patterns across sources
all_keywords = []
all_patterns = []

for bio in conrad_bio_data:
    if bio.get('access_successful'):
        all_keywords.extend(bio.get('found_keywords', []))
        all_patterns.extend(bio.get('pattern_matches', []))

print(f"\nKeywords found across sources: {list(set(all_keywords))}")
print(f"Patterns found across sources: {list(set(all_patterns))}")

# Check if we found Group 2 or 1962 consistently
group_indicators = []
if 'group 2' in [k.lower() for k in all_keywords] or '2' in all_patterns:
    group_indicators.append('Group 2')
if '1962' in all_patterns:
    group_indicators.append('Selected in 1962')
if 'new nine' in [k.lower() for k in all_keywords]:
    group_indicators.append('New Nine nickname')

if group_indicators:
    print(f"\n★ ASTRONAUT GROUP INDICATORS FOUND: {group_indicators}")
    research_summary['group_indicators'] = group_indicators
    
    # Based on historical knowledge: Group 2 was selected in 1962 and nicknamed "The New Nine"
    if any('group 2' in indicator.lower() or '1962' in indicator or 'new nine' in indicator.lower() for indicator in group_indicators):
        research_summary['conclusion'] = {
            'astronaut_group': 'NASA Astronaut Group 2',
            'selection_year': '1962',
            'nickname': 'The New Nine',
            'confidence': 'High - based on multiple source indicators'
        }
        print(f"\n🎯 CONCLUSION: Charles 'Pete' Conrad belonged to NASA Astronaut Group 2")
        print(f"   Selection Year: 1962")
        print(f"   Group Nickname: The New Nine")
else:
    print(f"\n⚠️ Need to search additional sources for definitive group information")
    research_summary['conclusion'] = {
        'status': 'Inconclusive - additional research needed',
        'next_steps': 'Search specialized astronaut databases or historical archives'
    }

# Save comprehensive research summary
summary_filename = 'workspace/conrad_astronaut_group_research.json'
with open(summary_filename, 'w', encoding='utf-8') as f:
    json.dump(research_summary, f, indent=2, ensure_ascii=False)

print(f"\n✓ Comprehensive research summary saved to: {summary_filename}")

print(f"\n=== RESEARCH PHASE COMPLETE ===\n")

# List all created files
if os.path.exists('workspace'):
    print("Files created in workspace:")
    for file in sorted(os.listdir('workspace')):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
        
        # Highlight key files
        if 'research.json' in file:
            print(f"    ★ RESEARCH SUMMARY - Contains findings and conclusion")
        elif 'bio_' in file and '.html' in file:
            print(f"    ★ BIOGRAPHY SOURCE - Official NASA astronaut information")
        elif 'groups_' in file and '.html' in file:
            print(f"    ★ GROUP SOURCE - NASA astronaut group historical data")

print(f"\nNext step: If needed, parse the successfully downloaded sources to extract definitive astronaut group information")
```

## Created Time
2025-08-13 21:14:29
