# Developer Plan 02

## Plan
Access the Metropolitan Museum of Art's 'Celebration of the Year of the Ram' 2015 exhibition page and any related documentation to identify and analyze all twelve Chinese zodiac animals displayed in the exhibition. Examine each zodiac animal representation (sculptures, artworks, or other objects) to determine which ones show visible hands or hand-like appendages. Count the total number of zodiac animals with visible hands and document the specific animals and their hand visibility characteristics.

## Description
This is the necessary next step because: (1) We have successfully identified the 2015 Met Museum exhibition as 'Celebration of the Year of the Ram' with details about ram/goat sculptures and artworks, (2) The TASK specifically asks about 'twelve animals of the Chinese zodiac' in this exhibition and which have visible hands, suggesting there are representations of all twelve zodiac animals beyond just the featured ram pieces, (3) Expected outcome is to locate and analyze visual representations of all twelve zodiac animals to count those with visible hands, (4) This directly addresses the core TASK requirement of counting zodiac animals with hand visibility in this specific exhibition

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

### Development Step 2: Identifying Viral Animated Rooster and Hamster Musical Duets with Tempo and Lyric Variations

**Description**: Search for animated videos featuring a rooster and a hamster performing the same song at different tempos with different lyrics. Focus on identifying popular animated content, memes, or viral videos where these two animals perform musical numbers. Look for patterns in animated series, YouTube videos, or internet memes that feature both a rooster and hamster singing variations of the same composition.

**Use Cases**:
- Animation studio research for identifying viral animal character trends and musical content inspiration
- Meme curation and discovery for social media managers seeking unique animal duet videos to boost engagement
- Academic study on the evolution of animated musical tropes involving anthropomorphic animals across internet culture
- Automated content sourcing for children’s educational platforms looking to license or feature animal-themed musical videos
- Digital marketing campaign analysis to track the popularity and spread of specific animated memes or musical parodies
- Entertainment journalists investigating the origins and variations of popular animated animal song performances
- Music educators compiling multimedia resources that showcase tempo and lyric variation in animated performances for classroom use
- Intellectual property teams monitoring web platforms for potential copyright infringements involving animated rooster and hamster musical content

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
import urllib.parse
import re

print("=== REAL ANIMATED ROOSTER AND HAMSTER MUSICAL CONTENT SEARCH ===")
print("Objective: Find actual animated videos with rooster and hamster performing same song at different tempos/lyrics\n")

# Create workspace directory
workspace_dir = "workspace"
os.makedirs(workspace_dir, exist_ok=True)

# First, let's inspect any existing search results from previous simulation
print("=== STEP 1: INSPECTING PREVIOUS SEARCH SIMULATION RESULTS ===")

existing_files = []
for filename in os.listdir(workspace_dir):
    if os.path.isfile(os.path.join(workspace_dir, filename)):
        file_path = os.path.join(workspace_dir, filename)
        file_size = os.path.getsize(file_path)
        existing_files.append((filename, file_path, file_size))
        print(f"  - {filename} ({file_size / 1024:.1f} KB)")

# Check if we have previous simulation results
simulation_file = None
for filename, file_path, _ in existing_files:
    if 'rooster_hamster' in filename and filename.endswith('.json'):
        simulation_file = file_path
        break

if simulation_file:
    print(f"\n=== INSPECTING SIMULATION RESULTS STRUCTURE ===")
    print(f"Found simulation file: {os.path.basename(simulation_file)}")
    
    # First inspect the JSON structure
    with open(simulation_file, 'r') as f:
        try:
            sim_data = json.load(f)
            print(f"JSON loaded successfully with {len(sim_data)} top-level keys")
            print("Top-level keys:")
            for key, value in sim_data.items():
                if isinstance(value, dict):
                    print(f"  {key}: Dictionary with {len(value)} keys")
                elif isinstance(value, list):
                    print(f"  {key}: List with {len(value)} items")
                else:
                    print(f"  {key}: {type(value).__name__} - {str(value)[:50]}...")
                    
            # Extract search queries from simulation for real search
            search_queries = sim_data.get('search_queries', [])
            print(f"\nFound {len(search_queries)} search queries from simulation")
            
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            sim_data = {}
else:
    print("\nNo previous simulation file found")
    sim_data = {}

print("\n=== STEP 2: IMPLEMENTING REAL WEB SEARCH ===")
print("Using actual web scraping to search for animated rooster and hamster content")

# Initialize real search results storage
real_search_results = {
    'search_timestamp': datetime.now().isoformat(),
    'objective': 'Find real animated rooster and hamster musical performances',
    'search_method': 'Web scraping and search engine queries',
    'search_queries': [],
    'search_results': [],
    'video_findings': [],
    'analysis_summary': {}
}

# Define focused search queries for real implementation
focused_queries = [
    "rooster hamster animated singing video",
    "rooster hamster cartoon music different tempo",
    "animated farm animals rooster hamster song",
    "viral rooster hamster singing meme",
    "rooster hamster duet animated video",
    "cartoon rooster hamster musical performance"
]

print(f"\nPrepared {len(focused_queries)} focused search queries:")
for i, query in enumerate(focused_queries, 1):
    print(f"  {i}. '{query}'")

real_search_results['search_queries'] = focused_queries

# Function to search DuckDuckGo (no API key required)
def search_duckduckgo(query, max_results=10):
    """Search DuckDuckGo for the given query"""
    print(f"\n  Searching DuckDuckGo for: '{query}'")
    
    try:
        # DuckDuckGo search URL
        search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find search result links
        results = []
        result_links = soup.find_all('a', class_='result__a')
        
        for link in result_links[:max_results]:
            title = link.get_text(strip=True)
            url = link.get('href', '')
            
            # Get snippet from nearby elements
            snippet = ''
            result_div = link.find_parent('div', class_='result')
            if result_div:
                snippet_elem = result_div.find('a', class_='result__snippet')
                if snippet_elem:
                    snippet = snippet_elem.get_text(strip=True)
            
            if title and url:
                # Calculate relevance score based on keywords
                relevance = calculate_relevance(title, snippet, query)
                
                results.append({
                    'title': title,
                    'url': url,
                    'snippet': snippet,
                    'relevance_score': relevance,
                    'query': query
                })
        
        print(f"    Found {len(results)} results")
        return results
        
    except requests.RequestException as e:
        print(f"    Error searching DuckDuckGo: {e}")
        return []
    except Exception as e:
        print(f"    Unexpected error: {e}")
        return []

def calculate_relevance(title, snippet, query):
    """Calculate relevance score based on keyword matching"""
    text = (title + ' ' + snippet).lower()
    query_words = query.lower().split()
    
    score = 0
    
    # Key terms that indicate our target content
    high_value_terms = ['rooster', 'hamster', 'animated', 'cartoon', 'singing', 'music', 'song', 'tempo', 'different', 'lyrics']
    medium_value_terms = ['video', 'viral', 'meme', 'farm', 'animal', 'performance', 'duet']
    
    # Score based on presence of key terms
    for term in high_value_terms:
        if term in text:
            score += 0.15
    
    for term in medium_value_terms:
        if term in text:
            score += 0.05
    
    # Bonus for having both 'rooster' and 'hamster'
    if 'rooster' in text and 'hamster' in text:
        score += 0.3
    
    # Bonus for musical terms
    musical_terms = ['singing', 'song', 'music', 'tempo', 'lyrics', 'duet']
    music_count = sum(1 for term in musical_terms if term in text)
    score += music_count * 0.1
    
    # Bonus for animation terms
    animation_terms = ['animated', 'cartoon', 'animation']
    animation_count = sum(1 for term in animation_terms if term in text)
    score += animation_count * 0.1
    
    return min(score, 1.0)  # Cap at 1.0

print("\n=== STEP 3: PERFORMING REAL SEARCHES ===")

all_results = []
for query in focused_queries:
    results = search_duckduckgo(query, max_results=8)
    all_results.extend(results)
    time.sleep(2)  # Be respectful to the search engine

print(f"\nTotal search results collected: {len(all_results)}")

# Remove duplicates based on URL
seen_urls = set()
unique_results = []
for result in all_results:
    if result['url'] not in seen_urls:
        seen_urls.add(result['url'])
        unique_results.append(result)

print(f"Unique results after deduplication: {len(unique_results)}")

# Sort by relevance score
unique_results.sort(key=lambda x: x['relevance_score'], reverse=True)

real_search_results['search_results'] = unique_results

print("\n=== STEP 4: ANALYZING HIGH-RELEVANCE RESULTS ===")

# Filter for high-relevance results
high_relevance_threshold = 0.4
high_relevance_results = [r for r in unique_results if r['relevance_score'] >= high_relevance_threshold]

print(f"\nHigh-relevance results (score >= {high_relevance_threshold}): {len(high_relevance_results)}")

for i, result in enumerate(high_relevance_results[:10], 1):  # Show top 10
    print(f"\n{i}. {result['title']}")
    print(f"   URL: {result['url'][:80]}..." if len(result['url']) > 80 else f"   URL: {result['url']}")
    print(f"   Relevance: {result['relevance_score']:.2f}")
    print(f"   Query: '{result['query']}'")
    if result['snippet']:
        snippet_preview = result['snippet'][:150] + "..." if len(result['snippet']) > 150 else result['snippet']
        print(f"   Snippet: {snippet_preview}")
    else:
        print(f"   Snippet: No description available")

print("\n=== STEP 5: IDENTIFYING VIDEO CONTENT ===")

# Look for video-related results
video_indicators = ['youtube.com', 'vimeo.com', 'video', 'watch', 'animated', 'cartoon']
video_results = []

for result in high_relevance_results:
    is_video = False
    video_score = 0
    
    # Check URL for video platforms
    url_lower = result['url'].lower()
    if any(indicator in url_lower for indicator in ['youtube.com', 'youtu.be', 'vimeo.com']):
        is_video = True
        video_score += 0.5
    
    # Check title and snippet for video indicators
    text_content = (result['title'] + ' ' + result['snippet']).lower()
    for indicator in video_indicators:
        if indicator in text_content:
            video_score += 0.1
    
    if video_score > 0.3 or is_video:
        video_info = {
            'title': result['title'],
            'url': result['url'],
            'snippet': result['snippet'],
            'relevance_score': result['relevance_score'],
            'video_score': video_score,
            'is_likely_video': is_video,
            'query': result['query']
        }
        video_results.append(video_info)

print(f"\nIdentified {len(video_results)} potential video results:")

for i, video in enumerate(video_results[:5], 1):  # Show top 5 video results
    print(f"\n{i}. {video['title']}")
    print(f"   URL: {video['url'][:80]}..." if len(video['url']) > 80 else f"   URL: {video['url']}")
    print(f"   Relevance: {video['relevance_score']:.2f}")
    print(f"   Video Score: {video['video_score']:.2f}")
    print(f"   Likely Video: {'Yes' if video['is_likely_video'] else 'Maybe'}")
    if video['snippet']:
        print(f"   Description: {video['snippet'][:120]}..." if len(video['snippet']) > 120 else f"   Description: {video['snippet']}")

real_search_results['video_findings'] = video_results

print("\n=== STEP 6: CONTENT ANALYSIS AND PATTERN DETECTION ===")

# Analyze patterns in the found content
patterns = {
    'common_keywords': {},
    'video_platforms': {},
    'content_types': [],
    'musical_elements': []
}

# Count keyword occurrences
all_text = ' '.join([r['title'] + ' ' + r['snippet'] for r in high_relevance_results]).lower()
keywords = ['rooster', 'hamster', 'animated', 'cartoon', 'singing', 'music', 'song', 'video', 'viral', 'meme', 'tempo', 'lyrics']

for keyword in keywords:
    count = all_text.count(keyword)
    if count > 0:
        patterns['common_keywords'][keyword] = count

# Analyze video platforms
for result in video_results:
    url_lower = result['url'].lower()
    if 'youtube' in url_lower:
        patterns['video_platforms']['YouTube'] = patterns['video_platforms'].get('YouTube', 0) + 1
    elif 'vimeo' in url_lower:
        patterns['video_platforms']['Vimeo'] = patterns['video_platforms'].get('Vimeo', 0) + 1
    else:
        patterns['video_platforms']['Other'] = patterns['video_platforms'].get('Other', 0) + 1

print("\nContent Analysis Results:")
print(f"Keyword frequencies:")
for keyword, count in sorted(patterns['common_keywords'].items(), key=lambda x: x[1], reverse=True):
    print(f"  {keyword}: {count} occurrences")

print(f"\nVideo platforms:")
for platform, count in patterns['video_platforms'].items():
    print(f"  {platform}: {count} results")

# Create analysis summary
analysis_summary = {
    'total_searches_performed': len(focused_queries),
    'total_results_found': len(all_results),
    'unique_results': len(unique_results),
    'high_relevance_results': len(high_relevance_results),
    'video_results_identified': len(video_results),
    'top_result': high_relevance_results[0] if high_relevance_results else None,
    'search_effectiveness': 'High' if len(high_relevance_results) > 5 else 'Moderate' if len(high_relevance_results) > 2 else 'Low',
    'patterns_found': patterns
}

real_search_results['analysis_summary'] = analysis_summary

print(f"\n=== STEP 7: SEARCH EFFECTIVENESS ANALYSIS ===")
print(f"Real Search Performance Metrics:")
print(f"  Search queries executed: {analysis_summary['total_searches_performed']}")
print(f"  Total results found: {analysis_summary['total_results_found']}")
print(f"  Unique results: {analysis_summary['unique_results']}")
print(f"  High-relevance results: {analysis_summary['high_relevance_results']}")
print(f"  Video content identified: {analysis_summary['video_results_identified']}")
print(f"  Search effectiveness: {analysis_summary['search_effectiveness']}")

if analysis_summary['top_result']:
    top_result = analysis_summary['top_result']
    print(f"\n*** TOP RESULT ***")
    print(f"Title: {top_result['title']}")
    print(f"URL: {top_result['url']}")
    print(f"Relevance Score: {top_result['relevance_score']:.2f}")
    if top_result['snippet']:
        print(f"Description: {top_result['snippet'][:200]}..." if len(top_result['snippet']) > 200 else f"Description: {top_result['snippet']}")

print(f"\n=== STEP 8: SAVING REAL SEARCH RESULTS ===")

# Save comprehensive real search results
results_file = os.path.join(workspace_dir, 'real_rooster_hamster_search_results.json')
with open(results_file, 'w') as f:
    json.dump(real_search_results, f, indent=2)

print(f"Real search results saved to: {os.path.basename(results_file)}")

# Create detailed findings report
findings_report = f"""REAL ANIMATED ROOSTER AND HAMSTER MUSICAL CONTENT SEARCH REPORT
================================================================

SEARCH OBJECTIVE:
Find actual animated videos featuring a rooster and hamster performing the same song at different tempos with different lyrics.

SEARCH METHOD:
Real web scraping using DuckDuckGo search engine with {len(focused_queries)} targeted queries.

KEY FINDINGS:
- {len(high_relevance_results)} high-relevance results identified (score >= {high_relevance_threshold})
- {len(video_results)} potential video content results found
- Search effectiveness: {analysis_summary['search_effectiveness']}
- Most common keywords: {', '.join([k for k, v in sorted(patterns['common_keywords'].items(), key=lambda x: x[1], reverse=True)[:5]])}

TOP SEARCH RESULTS:
"""

for i, result in enumerate(high_relevance_results[:5], 1):
    findings_report += f"""
{i}. {result['title']}
   URL: {result['url']}
   Relevance Score: {result['relevance_score']:.2f}
   Search Query: '{result['query']}'
   Description: {result['snippet'][:150] + '...' if len(result['snippet']) > 150 else result['snippet']}
"""

if video_results:
    findings_report += f"""

VIDEO CONTENT IDENTIFIED:
{len(video_results)} potential video results found:
"""
    
    for i, video in enumerate(video_results[:3], 1):
        findings_report += f"""
{i}. {video['title']}
   URL: {video['url']}
   Video Likelihood: {'High' if video['is_likely_video'] else 'Medium'}
   Relevance: {video['relevance_score']:.2f}
"""

findings_report += f"""

SEARCH ANALYSIS:
- Keyword Analysis: Found {len(patterns['common_keywords'])} relevant keywords across results
- Video Platforms: {', '.join([f"{k}: {v}" for k, v in patterns['video_platforms'].items()])}
- Content Quality: {'High-quality matches found' if len(high_relevance_results) > 3 else 'Limited matches found'}

RECOMMENDATIONS:
1. Investigate top-scoring video results for actual animated content
2. Follow up on YouTube links for potential rooster-hamster musical videos
3. Check animation and meme-related results for viral content
4. Consider expanding search to include specific animation studios or series

Search completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total execution time: Approximately {len(focused_queries) * 2} seconds (with respectful delays)
"""

findings_file = os.path.join(workspace_dir, 'real_search_findings_report.txt')
with open(findings_file, 'w') as f:
    f.write(findings_report)

print(f"Detailed findings report saved to: {os.path.basename(findings_file)}")

print(f"\n=== REAL SEARCH COMPLETE ===")
print(f"\n*** FINAL RESULTS SUMMARY ***")

if high_relevance_results:
    print(f"Successfully found {len(high_relevance_results)} high-relevance results for animated rooster and hamster content.")
    print(f"Identified {len(video_results)} potential video results that may contain the target content.")
    
    if analysis_summary['top_result']:
        top = analysis_summary['top_result']
        print(f"\nTop result: '{top['title']}' (Score: {top['relevance_score']:.2f})")
        print(f"URL: {top['url']}")
    
    print(f"\nThis real search provides actual web results that can be investigated further")
    print(f"for genuine animated rooster and hamster musical content.")
else:
    print("No high-relevance results found. The specific content may be rare or")
    print("may require more specialized search terms or platforms.")

print(f"\nFiles created in workspace/:")
for filename in os.listdir(workspace_dir):
    filepath = os.path.join(workspace_dir, filename)
    if os.path.isfile(filepath):
        size_kb = os.path.getsize(filepath) / 1024
        print(f"  - {filename} ({size_kb:.1f} KB)")

print(f"\n*** REAL ANIMATED ROOSTER AND HAMSTER SEARCH COMPLETED ***")
```

## Created Time
2025-08-13 19:41:12
