# Developer Plan 01

## Plan
Access the latest version of Carl Nebel's Wikipedia page as it appeared in August 2023 using archived versions from the Wayback Machine or Wikipedia's revision history. Extract the complete page content and identify all citation reference links, focusing on locating the first citation reference link in the article. Document the specific URL or source that this first citation points to for subsequent analysis.

## Description
This is the optimal starting approach because: (1) We need to establish the exact state of Carl Nebel's Wikipedia page as it existed in August 2023 to ensure we're working with the correct version, (2) No previous research has been conducted, (3) Expected outcome is to obtain the archived page content and identify the first citation reference link that we'll need to follow, (4) This establishes the foundation for the multi-step process of following the citation link and then analyzing the resulting webpage for chronological year dates.

## Episodic Examples
### Development Step 4: Extract July 3 2023 LOTR Wikipedia Internal Links Toward A Song of Ice and Fire

**Description**: Access the archived Wikipedia page for 'The Lord of the Rings' (book) as it appeared at the end of July 3, 2023. Use the Wayback Machine or Wikipedia's revision history to retrieve the specific version from that date. Extract all outbound links from the page content, focusing on internal Wikipedia links that could potentially lead toward 'A Song of Ice and Fire'. Create a comprehensive list of linked pages including literature, fantasy, author, publisher, and genre-related links that might serve as stepping stones in the path-finding process.

**Use Cases**:
- Competitive product mapping for market intelligence teams: archive the Wikipedia page of a rival’s flagship product, extract outbound links, and use BFS to uncover related technologies and collaborators leading to a specific emerging competitor.
- Academic literature exploration for research librarians: retrieve an archived revision of a foundational theory page, scrape internal links, and trace a path through related journals and authors to locate a target contemporary study.
- SEO internal linking audit for digital marketing agencies: load a historical snapshot of a high-traffic Wikipedia article, extract its link network, and identify the shortest chain of links that leads to pages optimized for a target keyword.
- Educational curriculum design for e-learning platforms: access the archived “Introduction to Biology” page, gather its outbound topic links, and map a learning path toward advanced genetics content using breadth-first search.
- Historical content evolution analysis for digital archivists: pull the July 2023 version of a political event page, extract links, and reconstruct how references to a specific legislation article appeared over time by finding link paths.
- Knowledge graph augmentation for AI research teams: scrape a past revision of an ontology page, collect entity links, and build a linkage chain to a new domain-specific concept to enrich the graph with contextual relationships.
- Due diligence support for consulting firms: obtain an archived corporate biography page, scrape its network of partner and subsidiary links, and run BFS to identify the shortest route to a target industry regulation page.

```
import requests
from bs4 import BeautifulSoup
import json
import time
from collections import deque
from datetime import datetime
import os

print("=== FIXING BFS PATH-FINDING WITH DIRECT HTML SCRAPING ===")
print("Objective: Find path from LOTR links to 'A Song of Ice and Fire' using HTML scraping\n")

# Load the LOTR links data
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("❌ No workspace directory found")
    exit()

workspace_dir = workspace_dirs[0]
lotr_file = os.path.join(workspace_dir, 'lotr_wikipedia_links_july_2023.json')

print(f"Loading LOTR links from: {os.path.basename(lotr_file)}\n")

with open(lotr_file, 'r', encoding='utf-8') as f:
    lotr_data = json.load(f)

# Select high-priority starting nodes
starting_nodes = set()
target_variations = [
    "A Song of Ice and Fire",
    "Game of Thrones", 
    "George R. R. Martin",
    "George R.R. Martin",
    "George Martin",
    "A Game of Thrones"
]

print("=== SELECTING MOST PROMISING STARTING NODES ===")

# Focus on the most likely connections to fantasy literature
high_priority_nodes = [
    "High fantasy",
    "Fantasy", 
    "Epic fantasy",
    "J. R. R. Tolkien",
    "Fantasy literature",
    "The Encyclopedia of Fantasy",
    "International Fantasy Award"
]

# Add high-priority nodes if they exist in our data
for category_name, links in lotr_data.get('categorized_links', {}).items():
    for link in links:
        if isinstance(link, dict) and 'article_name' in link:
            article_name = requests.utils.unquote(link['article_name']).replace('_', ' ')
            if article_name in high_priority_nodes:
                starting_nodes.add(article_name)
                print(f"Added high-priority node: {article_name}")

# If we don't have enough high-priority nodes, add some from fantasy/literature categories
if len(starting_nodes) < 10:
    for category in ['fantasy', 'literature']:
        if category in lotr_data.get('categorized_links', {}):
            for link in lotr_data['categorized_links'][category][:5]:  # Just first 5 from each
                if isinstance(link, dict) and 'article_name' in link:
                    article_name = requests.utils.unquote(link['article_name']).replace('_', ' ')
                    starting_nodes.add(article_name)

print(f"\nTotal starting nodes selected: {len(starting_nodes)}")
for i, node in enumerate(list(starting_nodes), 1):
    print(f"  {i:2d}. {node}")

# Function to scrape Wikipedia page links directly
def get_wikipedia_links_html(page_title, max_links=50):
    """Scrape Wikipedia page links directly from HTML"""
    try:
        # Convert page title to URL format
        url_title = page_title.replace(' ', '_')
        url = f"https://en.wikipedia.org/wiki/{requests.utils.quote(url_title)}"
        
        print(f"  Scraping: {page_title}")
        print(f"  URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main content area
            main_content = soup.find('div', {'id': 'mw-content-text'})
            if not main_content:
                main_content = soup
            
            # Extract Wikipedia article links
            links = []
            for link in main_content.find_all('a', href=True):
                href = link.get('href', '')
                if href.startswith('/wiki/') and ':' not in href.split('/')[-1]:
                    # Extract article name from URL
                    article_name = href.split('/')[-1].replace('_', ' ')
                    article_name = requests.utils.unquote(article_name)
                    
                    # Filter out non-article pages
                    skip_patterns = ['File:', 'Category:', 'Template:', 'User:', 'Talk:', 'Wikipedia:', 'Help:', 'Portal:', 'Special:', 'Media:']
                    if not any(pattern in article_name for pattern in skip_patterns):
                        if article_name not in links and len(links) < max_links:
                            links.append(article_name)
            
            print(f"    Found {len(links)} article links")
            return links
            
        elif response.status_code == 404:
            print(f"    Page not found: {page_title}")
            return []
        else:
            print(f"    HTTP error {response.status_code} for {page_title}")
            return []
            
    except Exception as e:
        print(f"    Error scraping {page_title}: {str(e)}")
        return []

# Function to check if we found our target
def is_target(page_title):
    """Check if the page title matches our target variations"""
    page_lower = page_title.lower()
    for target in target_variations:
        if target.lower() == page_lower or target.lower() in page_lower:
            return True
    return False

# Function to check for promising leads
def is_promising_lead(page_title):
    """Check if page title suggests it might lead to our target"""
    page_lower = page_title.lower()
    promising_keywords = [
        'fantasy', 'epic fantasy', 'high fantasy', 'fantasy literature',
        'fantasy series', 'fantasy novel', 'fantasy author', 'fantasy writer',
        'martin', 'george', 'song', 'ice', 'fire', 'game', 'thrones',
        'contemporary fantasy', 'modern fantasy', 'fantasy saga'
    ]
    return any(keyword in page_lower for keyword in promising_keywords)

# BFS Implementation with HTML scraping
print("\n=== STARTING BREADTH-FIRST SEARCH WITH HTML SCRAPING ===")
print(f"Target variations: {target_variations}\n")

# Initialize BFS structures
queue = deque()
visited = set()
parent = {}
depth = {}
found_paths = []
max_depth = 2  # Reduced depth to be more focused
max_requests = 20  # Reduced requests due to slower HTML scraping
request_count = 0

# Add starting nodes to queue
for node in starting_nodes:
    queue.append(node)
    depth[node] = 0
    parent[node] = None

print(f"Initialized BFS queue with {len(queue)} starting nodes")
print(f"Search parameters: max_depth={max_depth}, max_requests={max_requests}\n")

# Function to reconstruct path
def get_path(node, parent_dict):
    """Reconstruct the path from start to target node"""
    path = []
    current = node
    while current is not None:
        path.append(current)
        current = parent_dict.get(current)
    return list(reversed(path))

# Main BFS loop
start_time = datetime.now()
promisingLeads = []  # Track promising leads for later analysis

while queue and request_count < max_requests:
    current_node = queue.popleft()
    
    if current_node in visited:
        continue
        
    visited.add(current_node)
    current_depth = depth[current_node]
    
    print(f"\n--- Processing: {current_node} (depth {current_depth}) ---")
    
    # Check if we found the target
    if is_target(current_node):
        path = get_path(current_node, parent)
        found_paths.append({
            'target_found': current_node,
            'path': path,
            'depth': current_depth,
            'path_length': len(path)
        })
        print(f"\n🎯 TARGET FOUND: {current_node}")
        print(f"Path length: {len(path)} steps")
        print(f"Path: {' → '.join(path)}")
        break
    
    # Don't go deeper than max_depth
    if current_depth >= max_depth:
        print(f"  Reached max depth ({max_depth}), skipping expansion")
        continue
    
    # Get outbound links from current node
    outbound_links = get_wikipedia_links_html(current_node)
    request_count += 1
    
    # Process each outbound link
    new_nodes_added = 0
    target_hints = []
    
    for link in outbound_links:
        if link not in visited:
            # Check if this is our target
            if is_target(link):
                # Found target! Add to queue and it will be processed next
                queue.appendleft(link)  # Add to front for immediate processing
                depth[link] = current_depth + 1
                parent[link] = current_node
                target_hints.append(f"TARGET: {link}")
                new_nodes_added += 1
            elif is_promising_lead(link):
                # This looks promising, prioritize it
                queue.appendleft(link)
                depth[link] = current_depth + 1
                parent[link] = current_node
                target_hints.append(f"PROMISING: {link}")
                promisingLeads.append({
                    'node': link,
                    'parent': current_node,
                    'depth': current_depth + 1
                })
                new_nodes_added += 1
            elif current_depth + 1 < max_depth:  # Only add regular nodes if we haven't reached max depth
                queue.append(link)
                depth[link] = current_depth + 1
                parent[link] = current_node
                new_nodes_added += 1
    
    print(f"  Added {new_nodes_added} new nodes to queue")
    
    if target_hints:
        print(f"  🔍 Important findings: {target_hints[:3]}")
    
    # Add delay to be respectful to Wikipedia
    time.sleep(1)
    
    # Progress update
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"  Progress: {len(visited)} visited, {len(queue)} in queue, {request_count}/{max_requests} requests")
    print(f"  Elapsed: {elapsed:.1f}s")

# Final results
print(f"\n=== SEARCH COMPLETE ===")
elapsed = (datetime.now() - start_time).total_seconds()
print(f"Search completed in {elapsed:.1f} seconds")
print(f"Nodes visited: {len(visited)}")
print(f"Requests made: {request_count}")
print(f"Paths found: {len(found_paths)}")

# Save results
search_results = {
    'search_metadata': {
        'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'elapsed_seconds': elapsed,
        'target_variations': target_variations,
        'max_depth': max_depth,
        'max_requests': max_requests,
        'requests_made': request_count,
        'nodes_visited': len(visited),
        'method': 'HTML_scraping'
    },
    'starting_nodes': list(starting_nodes),
    'paths_found': found_paths,
    'promising_leads': promisingLeads,
    'visited_nodes': list(visited)
}

results_file = os.path.join(workspace_dir, 'bfs_html_scraping_results.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False, default=str)

print(f"\n=== FINAL RESULTS ===")
if found_paths:
    print(f"\n🎉 SUCCESS: Found {len(found_paths)} path(s) to target!\n")
    for i, path_info in enumerate(found_paths, 1):
        print(f"Path {i}:")
        print(f"  Target: {path_info['target_found']}")
        print(f"  Length: {path_info['path_length']} steps")
        print(f"  Route: {' → '.join(path_info['path'])}")
        print()
else:
    print(f"\n⚠️ No direct paths found within {max_depth} steps using {max_requests} requests")
    
    if promisingLeads:
        print(f"\n🔍 Found {len(promisingLeads)} promising leads for deeper exploration:")
        for i, lead in enumerate(promisingLeads[:5], 1):
            print(f"  {i}. {lead['node']} (depth {lead['depth']})")
            print(f"     From: {lead['parent']}")
        print("\n💡 These leads suggest connections exist but require deeper search")

print(f"\n📁 Results saved to: {os.path.basename(results_file)}")
print(f"🔄 Ready for extended search or manual exploration of promising leads")
```

### Development Step 7: Complete Wikipedia Edit History of ‘Antidisestablishmentarianism’: Revisions, Timestamps, Metadata Through June 2023

**Description**: Search for and access the Wikipedia page on 'Antidisestablishmentarianism' to locate its edit history or revision log. Extract comprehensive information about all edits made to this page from its creation until June 2023, including the total number of revisions, edit timestamps, and any available metadata about the page's editing activity over time.

**Use Cases**:
- Historical research and trend analysis of ideological topics by tracing how the “Antidisestablishmentarianism” page content evolved from creation to June 2023
- Journalist investigation into edit wars and contributor behavior on politically charged Wikipedia pages to identify biased or coordinated editing
- Data science project building time-series models of article length and revision frequency to predict Wikipedia content stability for niche entries
- Educational curriculum development by extracting and summarizing revision histories to teach students about collaborative writing and editorial decision-making
- Automated monitoring tool for Wikipedia administrators to detect sudden spikes in edits, vandalism, or rollback activity on specialized topic pages
- SEO content audit and competitor analysis by reviewing historical changes to long-tail keyword pages to inform site structure and optimization strategies
- Legal forensics analysis of edit metadata and timestamps to establish authorship, contribution timelines, and provenance in copyright or defamation disputes

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from urllib.parse import urljoin, quote
from collections import Counter

print("=== ANTIDISESTABLISHMENTARIANISM REVISION EXTRACTION - FINAL APPROACH ===\n")
print("Objective: Extract ALL revisions from creation until June 2023 using Wikipedia API\n")

# First, check existing workspace data to see if we have partial results
print("=== CHECKING FOR EXISTING WORKSPACE DATA ===\n")
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    print(f"Found existing workspace directories: {workspace_dirs}")
    for ws_dir in workspace_dirs:
        files = os.listdir(ws_dir)
        if files:
            print(f"\n{ws_dir} contains {len(files)} files:")
            for f in files:
                file_path = os.path.join(ws_dir, f)
                file_size = os.path.getsize(file_path)
                print(f"  - {f} ({file_size:,} bytes)")
                
                # Check if this looks like our target data
                if 'antidisestablishmentarianism' in f.lower():
                    print(f"    *** Target file found ***")
                    
                    # Inspect the file structure
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                        
                        print(f"    File contains {len(data)} top-level keys:")
                        for key, value in data.items():
                            if isinstance(value, dict):
                                print(f"      {key}: Dictionary with {len(value)} keys")
                            elif isinstance(value, list):
                                print(f"      {key}: List with {len(value)} items")
                            else:
                                print(f"      {key}: {type(value).__name__}")
                        
                        # Check if we have revision data
                        if 'all_revisions' in data and data['all_revisions']:
                            print(f"    *** Found existing revision data with {len(data['all_revisions'])} revisions ***")
                            existing_data = data
                            workspace_dir = ws_dir
                            use_existing = True
                            break
                    except Exception as e:
                        print(f"    Error reading file: {e}")
else:
    print("No existing workspace directories found")
    use_existing = False

# Create new workspace if needed
if not ('use_existing' in locals() and use_existing):
    workspace_dir = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(workspace_dir, exist_ok=True)
    print(f"\nCreated new workspace directory: {workspace_dir}\n")
    
    # DEFINE ALL CONSTANTS AND CONFIGURATION
    PAGE_TITLE = "Antidisestablishmentarianism"
    CUTOFF_DATE = "2023-06-30T23:59:59Z"  # End of June 2023
    API_ENDPOINT = "https://en.wikipedia.org/w/api.php"
    MAX_REQUESTS = 50  # Reasonable limit
    REQUEST_DELAY = 1.5
    
    print(f"Configuration:")
    print(f"  Target page: {PAGE_TITLE}")
    print(f"  Cutoff date: {CUTOFF_DATE}")
    print(f"  API endpoint: {API_ENDPOINT}")
    print(f"  Max requests: {MAX_REQUESTS}")
    print(f"  Request delay: {REQUEST_DELAY} seconds\n")
    
    # Set up headers for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Function to parse timestamp - FIXED VERSION
    def parse_timestamp(timestamp_str):
        """Parse Wikipedia timestamp format to datetime object"""
        try:
            # Wikipedia timestamps are in format: 2023-06-30T23:59:59Z
            # Remove 'Z' and parse
            clean_timestamp = timestamp_str.replace('Z', '')
            return datetime.strptime(clean_timestamp, '%Y-%m-%dT%H:%M:%S')
        except Exception as e:
            print(f"  Warning: timestamp parsing error for {timestamp_str}: {e}")
            return None
    
    # Function to check if timestamp is before cutoff - FIXED VERSION
    def is_before_cutoff(timestamp_str, cutoff_str):
        """Check if timestamp is before the cutoff date"""
        try:
            timestamp = parse_timestamp(timestamp_str)
            cutoff = parse_timestamp(cutoff_str)
            if timestamp and cutoff:
                return timestamp <= cutoff
            else:
                return True  # If parsing fails, include the revision
        except Exception as e:
            print(f"  Warning: cutoff comparison error: {e}")
            return True
    
    # Function to make API request
    def make_api_request(api_endpoint, params, request_headers, delay=1.0):
        """Make API request with rate limiting and error handling"""
        try:
            print(f"  Making API request to: {api_endpoint}")
            print(f"  Parameters: {list(params.keys())}")
            
            time.sleep(delay)  # Respectful rate limiting
            response = requests.get(api_endpoint, params=params, headers=request_headers, timeout=30)
            
            print(f"  API response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  API response received and parsed successfully")
                    return data
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error: {str(e)}")
                    print(f"Raw response: {response.text[:500]}")
                    return None
            else:
                print(f"❌ API request failed: HTTP {response.status_code}")
                print(f"Response text: {response.text[:500]}")
                return None
        except Exception as e:
            print(f"❌ API request error: {str(e)}")
            return None
    
    # Start comprehensive revision extraction
    print("=== STARTING COMPREHENSIVE REVISION EXTRACTION ===\n")
    
    all_revisions = []
    continue_token = None
    total_requests = 0
    revisions_after_cutoff = 0
    
    print(f"Starting extraction with max {MAX_REQUESTS} API requests...\n")
    
    while total_requests < MAX_REQUESTS:
        total_requests += 1
        
        # Build API parameters
        api_params = {
            'action': 'query',
            'format': 'json',
            'titles': PAGE_TITLE,
            'prop': 'revisions',
            'rvlimit': '500',  # Maximum allowed per request
            'rvprop': 'timestamp|user|comment|size|ids|flags',
            'rvdir': 'older'  # Start from newest and go backwards
        }
        
        # Add continuation token if we have one
        if continue_token:
            api_params.update(continue_token)
            print(f"  Using continuation: {continue_token}")
        
        print(f"Request {total_requests}: Fetching up to 500 revisions...")
        
        # Make the API request
        api_data = make_api_request(API_ENDPOINT, api_params, headers, delay=REQUEST_DELAY)
        
        if not api_data:
            print(f"❌ Failed to get API response, stopping extraction")
            break
        
        print(f"  Processing API response...")
        
        # Process the response
        if 'query' not in api_data or 'pages' not in api_data['query']:
            print(f"❌ Unexpected API response structure")
            print(f"API response keys: {list(api_data.keys())}")
            if 'query' in api_data:
                print(f"Query keys: {list(api_data['query'].keys())}")
            break
        
        pages = api_data['query']['pages']
        page_found = False
        
        print(f"  Found {len(pages)} pages in response")
        
        for page_id, page_data in pages.items():
            print(f"  Processing page ID: {page_id}")
            
            if 'missing' in page_data:
                print(f"❌ Page '{PAGE_TITLE}' not found")
                break
            
            if 'revisions' not in page_data:
                print(f"❌ No revisions found in response")
                print(f"Page data keys: {list(page_data.keys())}")
                break
            
            page_found = True
            revisions = page_data['revisions']
            print(f"  Retrieved {len(revisions)} revisions")
            
            # Process each revision with FIXED timestamp parsing
            revisions_before_cutoff_batch = 0
            revisions_after_cutoff_batch = 0
            oldest_timestamp = None
            newest_timestamp = None
            
            for revision in revisions:
                timestamp = revision.get('timestamp', '')
                
                # Track date range
                if not oldest_timestamp or timestamp < oldest_timestamp:
                    oldest_timestamp = timestamp
                if not newest_timestamp or timestamp > newest_timestamp:
                    newest_timestamp = timestamp
                
                # Check if revision is before cutoff date using FIXED function
                if is_before_cutoff(timestamp, CUTOFF_DATE):
                    all_revisions.append(revision)
                    revisions_before_cutoff_batch += 1
                else:
                    revisions_after_cutoff += 1
                    revisions_after_cutoff_batch += 1
            
            print(f"  Date range: {oldest_timestamp} to {newest_timestamp}")
            print(f"  Revisions before June 2023 (this batch): {revisions_before_cutoff_batch}")
            print(f"  Revisions after June 2023 (this batch): {revisions_after_cutoff_batch}")
            print(f"  Total collected so far: {len(all_revisions)}")
            
            # Check if we should continue
            if 'continue' in api_data:
                continue_token = api_data['continue']
                print(f"  More data available, continuing...")
            else:
                print(f"  ✅ Reached end of revision history")
                break
        
        if not page_found:
            print(f"❌ No valid page data found")
            break
        
        # If no continuation token, we're done
        if 'continue' not in api_data:
            print(f"\n✅ Complete revision history extracted!")
            break
        
        print()  # Empty line for readability
    
    print(f"\n=== EXTRACTION COMPLETE ===\n")
    print(f"Total API requests made: {total_requests}")
    print(f"Total revisions collected: {len(all_revisions)}")
    print(f"Revisions after June 2023 (excluded): {revisions_after_cutoff}")
    
    if len(all_revisions) == 0:
        print("❌ No revisions were collected")
        
        # Save empty result for debugging
        debug_data = {
            'extraction_metadata': {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'target_page': PAGE_TITLE,
                'cutoff_date': CUTOFF_DATE,
                'api_requests_made': total_requests,
                'total_revisions_collected': 0,
                'status': 'failed - no revisions collected'
            }
        }
        
        debug_file = os.path.join(workspace_dir, 'extraction_debug.json')
        with open(debug_file, 'w', encoding='utf-8') as f:
            json.dump(debug_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Debug data saved to: {os.path.basename(debug_file)}")
        existing_data = None
    else:
        # Sort revisions by timestamp (oldest first)
        all_revisions.sort(key=lambda x: x.get('timestamp', ''))
        
        # Create comprehensive dataset
        existing_data = {
            'extraction_metadata': {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'target_page': PAGE_TITLE,
                'cutoff_date': CUTOFF_DATE,
                'api_requests_made': total_requests,
                'total_revisions_collected': len(all_revisions),
                'revisions_after_cutoff_excluded': revisions_after_cutoff,
                'extraction_method': 'Wikipedia API with pagination'
            },
            'all_revisions': all_revisions
        }
        
        # Save main data file
        data_file = os.path.join(workspace_dir, 'antidisestablishmentarianism_complete_history.json')
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Complete revision data saved to: {os.path.basename(data_file)}")
        print(f"   File size: {os.path.getsize(data_file):,} bytes")

# Now analyze the data we have (either existing or newly extracted)
if existing_data and 'all_revisions' in existing_data and existing_data['all_revisions']:
    print(f"\n=== COMPREHENSIVE REVISION ANALYSIS ===\n")
    
    all_revisions = existing_data['all_revisions']
    
    # Extract key statistics
    timestamps = [rev.get('timestamp', '') for rev in all_revisions if rev.get('timestamp')]
    users = [rev.get('user', 'Unknown') for rev in all_revisions]
    sizes = [rev.get('size', 0) for rev in all_revisions if isinstance(rev.get('size'), int)]
    comments = [rev.get('comment', '') for rev in all_revisions]
    revision_ids = [rev.get('revid', 0) for rev in all_revisions if rev.get('revid')]
    
    # Basic statistics
    print(f"📊 COMPREHENSIVE STATISTICS:")
    print(f"  Total revisions extracted: {len(all_revisions)}")
    if timestamps:
        print(f"  Date range: {min(timestamps)} to {max(timestamps)}")
        print(f"  Page creation date: {min(timestamps)}")
        print(f"  Last edit before June 2023: {max(timestamps)}")
    print(f"  Unique contributors: {len(set(users))}")
    if sizes:
        print(f"  Average page size: {sum(sizes) // len(sizes)} bytes")
        print(f"  Size range: {min(sizes)} to {max(sizes)} bytes")
    if revision_ids:
        print(f"  Revision ID range: {min(revision_ids)} to {max(revision_ids)}")
    
    # User activity analysis
    user_counts = Counter(users)
    top_users = user_counts.most_common(10)
    
    print(f"\n👥 TOP 10 MOST ACTIVE CONTRIBUTORS:")
    for i, (user, count) in enumerate(top_users, 1):
        print(f"  {i:2d}. {user}: {count} edits")
    
    # Temporal analysis
    years = {}
    months = {}
    for timestamp in timestamps:
        if timestamp:
            year = timestamp[:4]
            month = timestamp[:7]  # YYYY-MM
            years[year] = years.get(year, 0) + 1
            months[month] = months.get(month, 0) + 1
    
    print(f"\n📅 EDITING ACTIVITY BY YEAR:")
    for year in sorted(years.keys()):
        print(f"  {year}: {years[year]} edits")
    
    # Show most active months
    top_months = sorted(months.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\n📅 TOP 5 MOST ACTIVE MONTHS:")
    for month, count in top_months:
        print(f"  {month}: {count} edits")
    
    # Sample revisions
    print(f"\n📝 KEY REVISION SAMPLES:")
    print(f"\nFIRST REVISION (Page Creation):")
    first_rev = all_revisions[0]
    for key, value in first_rev.items():
        print(f"  {key}: {value}")
    
    if len(all_revisions) > 1:
        print(f"\nMOST RECENT REVISION (Before June 2023):")
        last_rev = all_revisions[-1]
        for key, value in last_rev.items():
            print(f"  {key}: {value}")
    
    # Save comprehensive analysis
    print(f"\n=== SAVING COMPREHENSIVE ANALYSIS ===\n")
    
    # Update existing data with analysis
    analysis_data = {
        'extraction_metadata': existing_data.get('extraction_metadata', {}),
        'statistics': {
            'total_revisions': len(all_revisions),
            'unique_users': len(set(users)),
            'average_size': sum(sizes) // len(sizes) if sizes else 0,
            'size_range': {
                'min': min(sizes) if sizes else 0,
                'max': max(sizes) if sizes else 0
            },
            'revision_id_range': {
                'min': min(revision_ids) if revision_ids else 0,
                'max': max(revision_ids) if revision_ids else 0
            },
            'date_range': {
                'earliest': min(timestamps) if timestamps else None,
                'latest': max(timestamps) if timestamps else None
            },
            'edits_by_year': years,
            'edits_by_month': dict(top_months),
            'top_users': dict(top_users)
        },
        'all_revisions': all_revisions
    }
    
    # Save main data file
    data_file = os.path.join(workspace_dir, 'antidisestablishmentarianism_complete_history.json')
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Complete analysis saved to: {os.path.basename(data_file)}")
    print(f"   File size: {os.path.getsize(data_file):,} bytes")
    
    # Create summary report
    summary_file = os.path.join(workspace_dir, 'revision_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"ANTIDISESTABLISHMENTARIANISM - COMPLETE REVISION HISTORY\n")
        f.write(f"={'='*60}\n\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Target Page: {existing_data.get('extraction_metadata', {}).get('target_page', 'Antidisestablishmentarianism')}\n")
        f.write(f"Cutoff Date: {existing_data.get('extraction_metadata', {}).get('cutoff_date', '2023-06-30')}\n\n")
        
        f.write(f"EXTRACTION RESULTS:\n")
        f.write(f"- Total revisions collected: {len(all_revisions)}\n")
        if timestamps:
            f.write(f"- Date range: {min(timestamps)} to {max(timestamps)}\n")
        f.write(f"- Unique contributors: {len(set(users))}\n\n")
        
        f.write(f"TEMPORAL DISTRIBUTION:\n")
        for year in sorted(years.keys()):
            f.write(f"- {year}: {years[year]} edits\n")
        
        f.write(f"\nTOP CONTRIBUTORS:\n")
        for i, (user, count) in enumerate(top_users[:5], 1):
            f.write(f"- {i}. {user}: {count} edits\n")
        
        f.write(f"\nPAGE EVOLUTION:\n")
        if timestamps:
            f.write(f"- Created: {min(timestamps)}\n")
            f.write(f"- Last edit before June 2023: {max(timestamps)}\n")
        if sizes:
            f.write(f"- Size evolution: {min(sizes)} to {max(sizes)} bytes\n")
    
    print(f"✅ Summary report saved to: {os.path.basename(summary_file)}")
    
    # Create CSV export for easy analysis
    csv_file = os.path.join(workspace_dir, 'revisions_export.csv')
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write('revision_id,parent_id,timestamp,user,size,comment\n')
        for rev in all_revisions:
            # Escape commas and quotes in comments
            comment = rev.get('comment', '').replace('"', '""')
            f.write(f"{rev.get('revid', '')},{rev.get('parentid', '')},{rev.get('timestamp', '')},{rev.get('user', '')},{rev.get('size', '')},\"{comment}\"\n")
    
    print(f"✅ CSV export saved to: {os.path.basename(csv_file)}")
    
    print(f"\n=== MISSION ACCOMPLISHED ===\n")
    print(f"🎉 Successfully extracted complete revision history!")
    print(f"📊 {len(all_revisions)} total revisions from {min(timestamps) if timestamps else 'unknown'} to {max(timestamps) if timestamps else 'unknown'}")
    print(f"👥 {len(set(users))} unique contributors over {len(years)} years")
    print(f"📁 All data saved to workspace: {workspace_dir}")
    print(f"✅ Ready for detailed analysis and reporting")
    
    # Final summary for the PLAN
    print(f"\n=== PLAN COMPLETION SUMMARY ===\n")
    print(f"✅ OBJECTIVE ACHIEVED: Comprehensive edit history extracted")
    print(f"📋 Total revisions from creation until June 2023: {len(all_revisions)}")
    print(f"📅 Complete temporal coverage: {min(timestamps) if timestamps else 'N/A'} to {max(timestamps) if timestamps else 'N/A'}")
    print(f"🔍 Comprehensive metadata extracted: timestamps, users, comments, sizes, revision IDs")
    print(f"📊 Statistical analysis completed: user activity, temporal distribution, page evolution")
    print(f"💾 Multiple output formats created: JSON (structured), TXT (summary), CSV (spreadsheet)")
    
else:
    print(f"\n❌ No revision data available for analysis")
    print(f"The extraction may have failed or no revisions were found before June 2023")
```

### Development Step 6: Extract Revision History and Metadata for Wikipedia’s "Antidisestablishmentarianism" Page Through June 2023

**Description**: Search for and access the Wikipedia page on 'Antidisestablishmentarianism' to locate its edit history or revision log. Extract comprehensive information about all edits made to this page from its creation until June 2023, including the total number of revisions, edit timestamps, and any available metadata about the page's editing activity over time.

**Use Cases**:
- Academic linguistics research tracking the evolution of the Antidisestablishmentarianism entry to study semantic shifts in complex English terms over decades
- Brand reputation management monitoring corporate Wikipedia pages for unauthorized edits and ensuring immediate reverts to protect brand image
- Political analysis auditing revision logs of election and policy articles to detect shifts in narrative and influence public opinion studies
- Healthcare compliance auditing the edit history of pharmaceutical entries to document safety information changes and maintain accurate public health guidance
- SEO competitive analysis extracting revision histories of competitor product pages to identify feature updates and adjust marketing strategies
- Cultural heritage archiving building comprehensive archives of historical topic pages to preserve versioned content in digital libraries
- Cybersecurity misinformation detection analyzing edit patterns on crisis event pages to flag potential coordinated misinformation campaigns
- Investigative journalism reconstructing chronological edit trails of controversial topic pages to fact-check allegations and track source shifts

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import time
from urllib.parse import urljoin, quote
from collections import Counter

print("=== ANTIDISESTABLISHMENTARIANISM REVISION EXTRACTION - FIXED APPROACH ===\n")
print("Objective: Extract ALL revisions from creation until June 2023 using Wikipedia API\n")

# First, check if we have any existing workspace data
print("=== CHECKING FOR EXISTING WORKSPACE DATA ===\n")
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    print(f"Found existing workspace directories: {workspace_dirs}")
    for ws_dir in workspace_dirs:
        files = os.listdir(ws_dir)
        if files:
            print(f"\n{ws_dir} contains {len(files)} files:")
            for f in files:
                file_path = os.path.join(ws_dir, f)
                file_size = os.path.getsize(file_path)
                print(f"  - {f} ({file_size:,} bytes)")
                
                # Check if this looks like our target data
                if 'antidisestablishmentarianism' in f.lower() or 'debug' in f.lower():
                    print(f"    *** Potentially relevant file ***")
        else:
            print(f"\n{ws_dir} is empty")
else:
    print("No existing workspace directories found")

# Create new workspace directory
workspace_dir = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(workspace_dir, exist_ok=True)
print(f"\nCreated new workspace directory: {workspace_dir}\n")

# DEFINE ALL CONSTANTS AND CONFIGURATION
PAGE_TITLE = "Antidisestablishmentarianism"
CUTOFF_DATE = "2023-06-30T23:59:59Z"  # End of June 2023
API_ENDPOINT = "https://en.wikipedia.org/w/api.php"  # Pass as parameter to avoid scope issues
MAX_REQUESTS = 100
REQUEST_DELAY = 1.5

print(f"Configuration:")
print(f"  Target page: {PAGE_TITLE}")
print(f"  Cutoff date: {CUTOFF_DATE}")
print(f"  API endpoint: {API_ENDPOINT}")
print(f"  Max requests: {MAX_REQUESTS}")
print(f"  Request delay: {REQUEST_DELAY} seconds\n")

# Set up headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to make API request - PASS API_URL AS PARAMETER TO AVOID SCOPE ISSUES
def make_api_request(api_endpoint, params, request_headers, delay=1.0):
    """Make API request with rate limiting and error handling"""
    try:
        print(f"  Making API request to: {api_endpoint}")
        print(f"  Parameters: {list(params.keys())}")
        
        time.sleep(delay)  # Respectful rate limiting
        response = requests.get(api_endpoint, params=params, headers=request_headers, timeout=30)
        
        print(f"  API response status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  API response received and parsed successfully")
                return data
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {str(e)}")
                print(f"Raw response: {response.text[:500]}")
                return None
        else:
            print(f"❌ API request failed: HTTP {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            return None
    except Exception as e:
        print(f"❌ API request error: {str(e)}")
        return None

# Function to parse timestamp and check if it's before cutoff
def is_before_cutoff(timestamp_str, cutoff_str):
    """Check if timestamp is before the cutoff date"""
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        cutoff = datetime.fromisoformat(cutoff_str.replace('Z', '+00:00'))
        return timestamp <= cutoff
    except Exception as e:
        print(f"  Warning: timestamp parsing error for {timestamp_str}: {e}")
        return True  # If parsing fails, include the revision

# Start comprehensive revision extraction
print("=== STARTING COMPREHENSIVE REVISION EXTRACTION ===\n")

all_revisions = []
continue_token = None
total_requests = 0
revisions_after_cutoff = 0

print(f"Starting extraction with max {MAX_REQUESTS} API requests...\n")

while total_requests < MAX_REQUESTS:
    total_requests += 1
    
    # Build API parameters
    api_params = {
        'action': 'query',
        'format': 'json',
        'titles': PAGE_TITLE,
        'prop': 'revisions',
        'rvlimit': '500',  # Maximum allowed per request
        'rvprop': 'timestamp|user|comment|size|ids|flags',
        'rvdir': 'older'  # Start from newest and go backwards
    }
    
    # Add continuation token if we have one
    if continue_token:
        api_params.update(continue_token)
        print(f"  Using continuation: {continue_token}")
    
    print(f"Request {total_requests}: Fetching up to 500 revisions...")
    
    # Make the API request - PASS ALL PARAMETERS TO AVOID SCOPE ISSUES
    api_data = make_api_request(API_ENDPOINT, api_params, headers, delay=REQUEST_DELAY)
    
    if not api_data:
        print(f"❌ Failed to get API response, stopping extraction")
        break
    
    print(f"  Processing API response...")
    
    # Process the response
    if 'query' not in api_data or 'pages' not in api_data['query']:
        print(f"❌ Unexpected API response structure")
        print(f"API response keys: {list(api_data.keys())}")
        if 'query' in api_data:
            print(f"Query keys: {list(api_data['query'].keys())}")
        break
    
    pages = api_data['query']['pages']
    page_found = False
    
    print(f"  Found {len(pages)} pages in response")
    
    for page_id, page_data in pages.items():
        print(f"  Processing page ID: {page_id}")
        
        if 'missing' in page_data:
            print(f"❌ Page '{PAGE_TITLE}' not found")
            break
        
        if 'revisions' not in page_data:
            print(f"❌ No revisions found in response")
            print(f"Page data keys: {list(page_data.keys())}")
            break
        
        page_found = True
        revisions = page_data['revisions']
        print(f"  Retrieved {len(revisions)} revisions")
        
        # Process each revision
        revisions_before_cutoff_batch = 0
        revisions_after_cutoff_batch = 0
        oldest_timestamp = None
        newest_timestamp = None
        
        for revision in revisions:
            timestamp = revision.get('timestamp', '')
            
            # Track date range
            if not oldest_timestamp or timestamp < oldest_timestamp:
                oldest_timestamp = timestamp
            if not newest_timestamp or timestamp > newest_timestamp:
                newest_timestamp = timestamp
            
            # Check if revision is before cutoff date
            if is_before_cutoff(timestamp, CUTOFF_DATE):
                all_revisions.append(revision)
                revisions_before_cutoff_batch += 1
            else:
                revisions_after_cutoff += 1
                revisions_after_cutoff_batch += 1
        
        print(f"  Date range: {oldest_timestamp} to {newest_timestamp}")
        print(f"  Revisions before June 2023 (this batch): {revisions_before_cutoff_batch}")
        print(f"  Revisions after June 2023 (this batch): {revisions_after_cutoff_batch}")
        print(f"  Total collected so far: {len(all_revisions)}")
        
        # Check if we should continue
        if 'continue' in api_data:
            continue_token = api_data['continue']
            print(f"  More data available, continuing...")
        else:
            print(f"  ✅ Reached end of revision history")
            break
    
    if not page_found:
        print(f"❌ No valid page data found")
        break
    
    # If no continuation token, we're done
    if 'continue' not in api_data:
        print(f"\n✅ Complete revision history extracted!")
        break
    
    print()  # Empty line for readability

print(f"\n=== EXTRACTION COMPLETE ===\n")
print(f"Total API requests made: {total_requests}")
print(f"Total revisions collected: {len(all_revisions)}")
print(f"Revisions after June 2023 (excluded): {revisions_after_cutoff}")

if len(all_revisions) == 0:
    print("❌ No revisions were collected")
    print("This could indicate:")
    print("  - API access issues")
    print("  - Page doesn't exist")
    print("  - All revisions are after June 2023")
    print("  - Network connectivity problems")
    
    # Save empty result for debugging
    debug_data = {
        'extraction_metadata': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target_page': PAGE_TITLE,
            'cutoff_date': CUTOFF_DATE,
            'api_requests_made': total_requests,
            'total_revisions_collected': 0,
            'status': 'failed - no revisions collected'
        }
    }
    
    debug_file = os.path.join(workspace_dir, 'extraction_debug.json')
    with open(debug_file, 'w', encoding='utf-8') as f:
        json.dump(debug_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Debug data saved to: {os.path.basename(debug_file)}")
    
else:
    # Sort revisions by timestamp (oldest first)
    all_revisions.sort(key=lambda x: x.get('timestamp', ''))
    
    print(f"\n=== REVISION ANALYSIS ===\n")
    
    # Extract key statistics
    timestamps = [rev.get('timestamp', '') for rev in all_revisions if rev.get('timestamp')]
    users = [rev.get('user', 'Unknown') for rev in all_revisions]
    sizes = [rev.get('size', 0) for rev in all_revisions if isinstance(rev.get('size'), int)]
    comments = [rev.get('comment', '') for rev in all_revisions]
    revision_ids = [rev.get('revid', 0) for rev in all_revisions if rev.get('revid')]
    
    # Basic statistics
    print(f"📊 Basic Statistics:")
    print(f"  Total revisions: {len(all_revisions)}")
    if timestamps:
        print(f"  Date range: {min(timestamps)} to {max(timestamps)}")
        print(f"  Page creation date: {min(timestamps)}")
        print(f"  Last edit before June 2023: {max(timestamps)}")
    print(f"  Unique users: {len(set(users))}")
    if sizes:
        print(f"  Average page size: {sum(sizes) // len(sizes)} bytes")
        print(f"  Size range: {min(sizes)} to {max(sizes)} bytes")
    if revision_ids:
        print(f"  Revision ID range: {min(revision_ids)} to {max(revision_ids)}")
    
    # User activity analysis
    user_counts = Counter(users)
    top_users = user_counts.most_common(10)
    
    print(f"\n👥 Top 10 Most Active Users:")
    for i, (user, count) in enumerate(top_users, 1):
        print(f"  {i:2d}. {user}: {count} edits")
    
    # Temporal analysis
    years = {}
    months = {}
    for timestamp in timestamps:
        if timestamp:
            year = timestamp[:4]
            month = timestamp[:7]  # YYYY-MM
            years[year] = years.get(year, 0) + 1
            months[month] = months.get(month, 0) + 1
    
    print(f"\n📅 Edits by Year:")
    for year in sorted(years.keys()):
        print(f"  {year}: {years[year]} edits")
    
    # Show most active months
    top_months = sorted(months.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\n📅 Top 5 Most Active Months:")
    for month, count in top_months:
        print(f"  {month}: {count} edits")
    
    # Sample revisions
    print(f"\n📝 Sample Revisions:")
    print(f"\nFirst revision (page creation):")
    first_rev = all_revisions[0]
    for key, value in first_rev.items():
        print(f"  {key}: {value}")
    
    if len(all_revisions) > 1:
        print(f"\nMost recent revision (before June 2023):")
        last_rev = all_revisions[-1]
        for key, value in last_rev.items():
            print(f"  {key}: {value}")
    
    # Save comprehensive data
    print(f"\n=== SAVING COMPREHENSIVE DATA ===\n")
    
    # Create comprehensive dataset
    comprehensive_data = {
        'extraction_metadata': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target_page': PAGE_TITLE,
            'cutoff_date': CUTOFF_DATE,
            'api_requests_made': total_requests,
            'total_revisions_collected': len(all_revisions),
            'revisions_after_cutoff_excluded': revisions_after_cutoff,
            'date_range': {
                'earliest': min(timestamps) if timestamps else None,
                'latest': max(timestamps) if timestamps else None
            },
            'extraction_method': 'Wikipedia API with pagination'
        },
        'statistics': {
            'total_revisions': len(all_revisions),
            'unique_users': len(set(users)),
            'average_size': sum(sizes) // len(sizes) if sizes else 0,
            'size_range': {
                'min': min(sizes) if sizes else 0,
                'max': max(sizes) if sizes else 0
            },
            'revision_id_range': {
                'min': min(revision_ids) if revision_ids else 0,
                'max': max(revision_ids) if revision_ids else 0
            },
            'edits_by_year': years,
            'edits_by_month': dict(top_months),
            'top_users': dict(top_users)
        },
        'all_revisions': all_revisions
    }
    
    # Save main data file
    data_file = os.path.join(workspace_dir, 'antidisestablishmentarianism_complete_history.json')
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Complete revision data saved to: {os.path.basename(data_file)}")
    print(f"   File size: {os.path.getsize(data_file):,} bytes")
    
    # Create summary report
    summary_file = os.path.join(workspace_dir, 'revision_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"ANTIDISESTABLISHMENTARIANISM - COMPLETE REVISION HISTORY\n")
        f.write(f"={'='*60}\n\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Target Page: {PAGE_TITLE}\n")
        f.write(f"Cutoff Date: {CUTOFF_DATE}\n\n")
        
        f.write(f"EXTRACTION RESULTS:\n")
        f.write(f"- Total API requests: {total_requests}\n")
        f.write(f"- Total revisions collected: {len(all_revisions)}\n")
        f.write(f"- Revisions excluded (after June 2023): {revisions_after_cutoff}\n")
        if timestamps:
            f.write(f"- Date range: {min(timestamps)} to {max(timestamps)}\n")
        f.write(f"- Unique contributors: {len(set(users))}\n\n")
        
        f.write(f"TEMPORAL DISTRIBUTION:\n")
        for year in sorted(years.keys()):
            f.write(f"- {year}: {years[year]} edits\n")
        
        f.write(f"\nTOP CONTRIBUTORS:\n")
        for i, (user, count) in enumerate(top_users[:5], 1):
            f.write(f"- {i}. {user}: {count} edits\n")
        
        f.write(f"\nPAGE EVOLUTION:\n")
        if timestamps:
            f.write(f"- Created: {min(timestamps)}\n")
            f.write(f"- Last edit before June 2023: {max(timestamps)}\n")
        if sizes:
            f.write(f"- Size evolution: {min(sizes)} to {max(sizes)} bytes\n")
    
    print(f"✅ Summary report saved to: {os.path.basename(summary_file)}")
    
    # Create CSV export for easy analysis
    csv_file = os.path.join(workspace_dir, 'revisions_export.csv')
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write('revision_id,parent_id,timestamp,user,size,comment\n')
        for rev in all_revisions:
            # Escape commas and quotes in comments
            comment = rev.get('comment', '').replace('"', '""')
            f.write(f"{rev.get('revid', '')},{rev.get('parentid', '')},{rev.get('timestamp', '')},{rev.get('user', '')},{rev.get('size', '')},\"{comment}\"\n")
    
    print(f"✅ CSV export saved to: {os.path.basename(csv_file)}")
    
    print(f"\n=== EXTRACTION SUCCESS ===\n")
    print(f"🎉 Successfully extracted complete revision history!")
    print(f"📊 {len(all_revisions)} revisions from {min(timestamps) if timestamps else 'unknown'} to {max(timestamps) if timestamps else 'unknown'}")
    print(f"👥 {len(set(users))} unique contributors")
    print(f"📁 All data saved to workspace: {workspace_dir}")
    print(f"✅ Ready for detailed analysis and reporting")
    
    # Final summary for the PLAN
    print(f"\n=== PLAN COMPLETION SUMMARY ===\n")
    print(f"✅ OBJECTIVE ACHIEVED: Comprehensive edit history extracted")
    print(f"📋 Total revisions from creation until June 2023: {len(all_revisions)}")
    print(f"📅 Complete temporal coverage: {min(timestamps) if timestamps else 'N/A'} to {max(timestamps) if timestamps else 'N/A'}")
    print(f"🔍 Comprehensive metadata extracted: timestamps, users, comments, sizes, revision IDs")
    print(f"📊 Statistical analysis completed: user activity, temporal distribution, page evolution")
    print(f"💾 Multiple output formats created: JSON (structured), TXT (summary), CSV (spreadsheet)")
```

### Development Step 4: Aggregate complete edit history of Wikipedia’s ‘Antidisestablishmentarianism’ page: revision count, timestamps, metadata through June 2023

**Description**: Search for and access the Wikipedia page on 'Antidisestablishmentarianism' to locate its edit history or revision log. Extract comprehensive information about all edits made to this page from its creation until June 2023, including the total number of revisions, edit timestamps, and any available metadata about the page's editing activity over time.

**Use Cases**:
- Digital humanities research mapping discourse shifts by extracting complete revision histories of ideological Wikipedia pages to analyze changes in public sentiment and language use over time
- Corporate compliance and brand monitoring teams auditing every edit to a company’s Wikipedia page to detect unauthorized changes, document content liability, and prepare PR or legal responses
- Legal evidence preparation for law firms collecting verifiable historical logs of Wikipedia edits in defamation or intellectual property disputes to establish content provenance and timelines
- Natural language processing development teams building datasets of incremental text changes from revision logs to train models on diff detection, summarization, and automated edit suggestions
- Cybersecurity and wiki-moderation automation systems analyzing historical revision metadata patterns to flag anomalous or vandalistic edits in near real time
- Academic educators generating interactive timelines and classroom materials that visualize major edits, contributor activity, and content evolution for media literacy courses
- SEO and content-strategy consultants analyzing the evolution of high-value topic pages to identify strategic content expansions, editorial consensus shifts, and engagement trends

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import time
from urllib.parse import urljoin, quote

print("=== COMPREHENSIVE ANTIDISESTABLISHMENTARIANISM REVISION EXTRACTION ===\n")
print("Objective: Extract ALL revisions from creation until June 2023 using Wikipedia API\n")

# Create workspace directory
workspace_dir = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(workspace_dir, exist_ok=True)
print(f"Created workspace directory: {workspace_dir}\n")

# Define the target page and cutoff date
page_title = "Antidisestablishmentarianism"
cutoff_date = "2023-06-30T23:59:59Z"  # End of June 2023
print(f"Target page: {page_title}")
print(f"Cutoff date: {cutoff_date} (end of June 2023)\n")

# Wikipedia API endpoint - DEFINED EARLY TO AVOID SCOPE ISSUES
api_url = "https://en.wikipedia.org/w/api.php"
print(f"API endpoint: {api_url}\n")

# Set up headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to make API request with rate limiting
def make_api_request(params, delay=1.0):
    """Make API request with rate limiting and error handling"""
    try:
        print(f"  Making API request with params: {list(params.keys())}")
        time.sleep(delay)  # Respectful rate limiting
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        
        print(f"  API response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  API response received successfully")
            return data
        else:
            print(f"❌ API request failed: HTTP {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            return None
    except Exception as e:
        print(f"❌ API request error: {str(e)}")
        return None

# Function to parse timestamp and check if it's before cutoff
def is_before_cutoff(timestamp_str, cutoff_str):
    """Check if timestamp is before the cutoff date"""
    try:
        from datetime import datetime
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        cutoff = datetime.fromisoformat(cutoff_str.replace('Z', '+00:00'))
        return timestamp <= cutoff
    except Exception as e:
        print(f"  Warning: timestamp parsing error for {timestamp_str}: {e}")
        return True  # If parsing fails, include the revision

# Start comprehensive revision extraction
print("=== STARTING COMPREHENSIVE REVISION EXTRACTION ===\n")

all_revisions = []
continue_token = None
page_processed = 0
total_requests = 0
max_requests = 200  # Reasonable limit to avoid overwhelming the API

print(f"Starting extraction with max {max_requests} API requests...\n")

while total_requests < max_requests:
    total_requests += 1
    
    # Build API parameters
    api_params = {
        'action': 'query',
        'format': 'json',
        'titles': page_title,
        'prop': 'revisions',
        'rvlimit': '500',  # Maximum allowed per request
        'rvprop': 'timestamp|user|comment|size|ids|flags',
        'rvdir': 'older'  # Start from newest and go backwards
    }
    
    # Add continuation token if we have one
    if continue_token:
        api_params.update(continue_token)
        print(f"  Using continuation: {continue_token}")
    
    print(f"Request {total_requests}: Fetching up to 500 revisions...")
    
    # Make the API request
    api_data = make_api_request(api_params, delay=1.5)
    
    if not api_data:
        print(f"❌ Failed to get API response, stopping extraction")
        break
    
    print(f"  Processing API response...")
    
    # Process the response
    if 'query' not in api_data or 'pages' not in api_data['query']:
        print(f"❌ Unexpected API response structure")
        print(f"API response keys: {list(api_data.keys())}")
        if 'query' in api_data:
            print(f"Query keys: {list(api_data['query'].keys())}")
        break
    
    pages = api_data['query']['pages']
    page_found = False
    
    print(f"  Found {len(pages)} pages in response")
    
    for page_id, page_data in pages.items():
        print(f"  Processing page ID: {page_id}")
        
        if 'missing' in page_data:
            print(f"❌ Page '{page_title}' not found")
            break
        
        if 'revisions' not in page_data:
            print(f"❌ No revisions found in response")
            print(f"Page data keys: {list(page_data.keys())}")
            break
        
        page_found = True
        revisions = page_data['revisions']
        print(f"  Retrieved {len(revisions)} revisions")
        
        # Process each revision
        revisions_before_cutoff = 0
        revisions_after_cutoff = 0
        oldest_timestamp = None
        newest_timestamp = None
        
        for revision in revisions:
            timestamp = revision.get('timestamp', '')
            
            # Track date range
            if not oldest_timestamp or timestamp < oldest_timestamp:
                oldest_timestamp = timestamp
            if not newest_timestamp or timestamp > newest_timestamp:
                newest_timestamp = timestamp
            
            # Check if revision is before cutoff date
            if is_before_cutoff(timestamp, cutoff_date):
                all_revisions.append(revision)
                revisions_before_cutoff += 1
            else:
                revisions_after_cutoff += 1
        
        print(f"  Date range: {oldest_timestamp} to {newest_timestamp}")
        print(f"  Revisions before June 2023: {revisions_before_cutoff}")
        print(f"  Revisions after June 2023: {revisions_after_cutoff}")
        print(f"  Total collected so far: {len(all_revisions)}")
        
        # Check if we should continue
        if 'continue' in api_data:
            continue_token = api_data['continue']
            print(f"  More data available, continuing with token: {continue_token}")
        else:
            print(f"  ✅ Reached end of revision history")
            break
    
    if not page_found:
        print(f"❌ No valid page data found")
        break
    
    # If no continuation token, we're done
    if 'continue' not in api_data:
        print(f"\n✅ Complete revision history extracted!")
        break
    
    print()  # Empty line for readability

print(f"\n=== EXTRACTION COMPLETE ===\n")
print(f"Total API requests made: {total_requests}")
print(f"Total revisions collected: {len(all_revisions)}")

if len(all_revisions) == 0:
    print("❌ No revisions were collected")
    print("This could indicate:")
    print("  - API access issues")
    print("  - Page doesn't exist")
    print("  - All revisions are after June 2023")
    print("  - Network connectivity problems")
else:
    # Sort revisions by timestamp (oldest first)
    all_revisions.sort(key=lambda x: x.get('timestamp', ''))
    
    print(f"\n=== REVISION ANALYSIS ===\n")
    
    # Extract key statistics
    timestamps = [rev.get('timestamp', '') for rev in all_revisions if rev.get('timestamp')]
    users = [rev.get('user', 'Unknown') for rev in all_revisions]
    sizes = [rev.get('size', 0) for rev in all_revisions if isinstance(rev.get('size'), int)]
    comments = [rev.get('comment', '') for rev in all_revisions]
    
    # Basic statistics
    print(f"📊 Basic Statistics:")
    print(f"  Total revisions: {len(all_revisions)}")
    print(f"  Date range: {min(timestamps)} to {max(timestamps)}")
    print(f"  Unique users: {len(set(users))}")
    print(f"  Average page size: {sum(sizes) // len(sizes) if sizes else 0} bytes")
    print(f"  Size range: {min(sizes) if sizes else 0} to {max(sizes) if sizes else 0} bytes")
    
    # User activity analysis
    from collections import Counter
    user_counts = Counter(users)
    top_users = user_counts.most_common(10)
    
    print(f"\n👥 Top 10 Most Active Users:")
    for i, (user, count) in enumerate(top_users, 1):
        print(f"  {i:2d}. {user}: {count} edits")
    
    # Temporal analysis
    years = {}
    for timestamp in timestamps:
        if timestamp:
            year = timestamp[:4]
            years[year] = years.get(year, 0) + 1
    
    print(f"\n📅 Edits by Year:")
    for year in sorted(years.keys()):
        print(f"  {year}: {years[year]} edits")
    
    # Sample revisions
    print(f"\n📝 Sample Revisions:")
    print(f"\nFirst revision (page creation):")
    first_rev = all_revisions[0]
    for key, value in first_rev.items():
        print(f"  {key}: {value}")
    
    print(f"\nMost recent revision (before June 2023):")
    last_rev = all_revisions[-1]
    for key, value in last_rev.items():
        print(f"  {key}: {value}")
    
    # Save comprehensive data
    print(f"\n=== SAVING COMPREHENSIVE DATA ===\n")
    
    # Create comprehensive dataset
    comprehensive_data = {
        'extraction_metadata': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target_page': page_title,
            'cutoff_date': cutoff_date,
            'api_requests_made': total_requests,
            'total_revisions_collected': len(all_revisions),
            'date_range': {
                'earliest': min(timestamps) if timestamps else None,
                'latest': max(timestamps) if timestamps else None
            },
            'extraction_method': 'Wikipedia API with pagination'
        },
        'statistics': {
            'total_revisions': len(all_revisions),
            'unique_users': len(set(users)),
            'average_size': sum(sizes) // len(sizes) if sizes else 0,
            'size_range': {
                'min': min(sizes) if sizes else 0,
                'max': max(sizes) if sizes else 0
            },
            'edits_by_year': years,
            'top_users': dict(top_users)
        },
        'all_revisions': all_revisions
    }
    
    # Save main data file
    data_file = os.path.join(workspace_dir, 'antidisestablishmentarianism_complete_history.json')
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(comprehensive_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Complete revision data saved to: {os.path.basename(data_file)}")
    print(f"   File size: {os.path.getsize(data_file):,} bytes")
    
    # Create summary report
    summary_file = os.path.join(workspace_dir, 'revision_summary.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"ANTIDISESTABLISHMENTARIANISM - COMPLETE REVISION HISTORY\n")
        f.write(f"={'='*60}\n\n")
        f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Target Page: {page_title}\n")
        f.write(f"Cutoff Date: {cutoff_date}\n\n")
        
        f.write(f"EXTRACTION RESULTS:\n")
        f.write(f"- Total API requests: {total_requests}\n")
        f.write(f"- Total revisions collected: {len(all_revisions)}\n")
        f.write(f"- Date range: {min(timestamps)} to {max(timestamps)}\n")
        f.write(f"- Unique contributors: {len(set(users))}\n\n")
        
        f.write(f"TEMPORAL DISTRIBUTION:\n")
        for year in sorted(years.keys()):
            f.write(f"- {year}: {years[year]} edits\n")
        
        f.write(f"\nTOP CONTRIBUTORS:\n")
        for i, (user, count) in enumerate(top_users[:5], 1):
            f.write(f"- {i}. {user}: {count} edits\n")
        
        f.write(f"\nPAGE EVOLUTION:\n")
        f.write(f"- Created: {min(timestamps)}\n")
        f.write(f"- Last edit before June 2023: {max(timestamps)}\n")
        f.write(f"- Size evolution: {min(sizes) if sizes else 0} to {max(sizes) if sizes else 0} bytes\n")
    
    print(f"✅ Summary report saved to: {os.path.basename(summary_file)}")
    
    # Create CSV export for easy analysis
    csv_file = os.path.join(workspace_dir, 'revisions_export.csv')
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write('revision_id,parent_id,timestamp,user,size,comment\n')
        for rev in all_revisions:
            # Escape commas and quotes in comments
            comment = rev.get('comment', '').replace('"', '""')
            f.write(f"{rev.get('revid', '')},{rev.get('parentid', '')},{rev.get('timestamp', '')},{rev.get('user', '')},{rev.get('size', '')},\"{comment}\"\n")
    
    print(f"✅ CSV export saved to: {os.path.basename(csv_file)}")
    
    print(f"\n=== EXTRACTION SUCCESS ===\n")
    print(f"🎉 Successfully extracted complete revision history!")
    print(f"📊 {len(all_revisions)} revisions from {min(timestamps)} to {max(timestamps)}")
    print(f"👥 {len(set(users))} unique contributors")
    print(f"📁 All data saved to workspace: {workspace_dir}")
    print(f"✅ Ready for detailed analysis and reporting")
```

### Development Step 7: Extract internal LOTR Wikipedia links (July 3, 2023) toward 'A Song of Ice and Fire'

**Description**: Access the archived Wikipedia page for 'The Lord of the Rings' (book) as it appeared at the end of July 3, 2023. Use the Wayback Machine or Wikipedia's revision history to retrieve the specific version from that date. Extract all outbound links from the page content, focusing on internal Wikipedia links that could potentially lead toward 'A Song of Ice and Fire'. Create a comprehensive list of linked pages including literature, fantasy, author, publisher, and genre-related links that might serve as stepping stones in the path-finding process.

**Use Cases**:
- Comparative literature research in academia: retrieve the July 3, 2023 snapshot of “The Lord of the Rings” Wikipedia to map links toward “A Song of Ice and Fire,” enabling scholars to analyze thematic influences and authorial networks between epic fantasy sagas.
- Digital humanities project for narrative evolution: extract and categorize internal links from archived medieval literature pages to build a temporal knowledge graph visualizing genre trends, myth motifs, and author collaborations across Wikipedia revisions.
- SEO and competitive intelligence for publishing houses: access historical versions of book and author Wikipedia entries to extract outbound link profiles, track competitor backlink strategies, and inform marketing teams on evolving partnership and citation opportunities.
- Fact-checking and content audit for journalism: automate retrieval of archived wiki revisions to verify changes in author credits, publisher associations, and award mentions on high-profile literary pages, ensuring accurate reporting of publication histories.
- Semantic web and recommendation engine enrichment: harvest categorized internal Wikipedia links from archived fantasy articles to populate a time-aware ontology of authors, genres, and characters, powering AI-driven book recommendation systems.
- Legal and intellectual property due diligence: compile a comprehensive list of publisher, author, and award links from archived literary wiki snapshots to reconstruct citation trails and support negotiations in copyright and licensing agreements.
- Digital library metadata enhancement: integrate extracted character, place, and genre link data from a July 2023 snapshot of “The Lord of the Rings” into catalog records, improving thematic search, discovery, and user engagement for fantasy collections.

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from urllib.parse import urljoin, unquote

print("=== ACCESSING ARCHIVED WIKIPEDIA PAGE: THE LORD OF THE RINGS (JULY 3, 2023) ===")
print("Objective: Retrieve archived version and extract all outbound links\n")

# Create workspace directory
workspace_dir = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(workspace_dir, exist_ok=True)
print(f"Created workspace directory: {workspace_dir}\n")

# Define the target page and date
url = "https://en.wikipedia.org/wiki/The_Lord_of_the_Rings"
archive_date = "20230703"  # July 3, 2023

print(f"Target URL: {url}")
print(f"Target date: July 3, 2023 ({archive_date})\n")

# Check if archived version is available in Wayback Machine
print("=== CHECKING WAYBACK MACHINE AVAILABILITY ===")
api_url = f"https://archive.org/wayback/available?url={url}&timestamp={archive_date}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    print(f"Checking availability: {api_url}")
    avail_response = requests.get(api_url, headers=headers, timeout=30)
    
    if avail_response.status_code == 200:
        avail_data = avail_response.json()
        print(f"API Response status: {avail_response.status_code}")
        print(f"Response data keys: {list(avail_data.keys()) if avail_data else 'No data'}")
        
        if "archived_snapshots" in avail_data and "closest" in avail_data["archived_snapshots"]:
            closest = avail_data["archived_snapshots"]["closest"]
            print(f"Closest snapshot found: {closest.get('available', 'Unknown status')}")
            
            if closest.get("available"):
                archive_url = closest["url"]
                archive_timestamp = closest["timestamp"]
                
                # Format the timestamp for display
                formatted_date = f"{archive_timestamp[:4]}-{archive_timestamp[4:6]}-{archive_timestamp[6:8]} {archive_timestamp[8:10]}:{archive_timestamp[10:12]}:{archive_timestamp[12:14]}"
                
                print(f"\n✅ Archive found!")
                print(f"Archive URL: {archive_url}")
                print(f"Archive timestamp: {archive_timestamp}")
                print(f"Formatted date: {formatted_date}")
            else:
                print(f"\n❌ No archived version available for {url} on {archive_date}")
                exit()
        else:
            print(f"\n❌ No archived snapshots found for {url}")
            exit()
    else:
        print(f"❌ Error checking archive availability: HTTP {avail_response.status_code}")
        exit()
        
except Exception as e:
    print(f"❌ Error accessing Wayback Machine API: {str(e)}")
    exit()

# Retrieve the archived page
print(f"\n=== RETRIEVING ARCHIVED PAGE ===")
print(f"Fetching: {archive_url}")

try:
    response = requests.get(archive_url, headers=headers, timeout=60)
    
    if response.status_code == 200:
        print(f"✅ Successfully retrieved archived page")
        print(f"Content length: {len(response.content):,} bytes")
        print(f"Content type: {response.headers.get('content-type', 'Unknown')}")
    else:
        print(f"❌ Failed to retrieve archived page: HTTP {response.status_code}")
        exit()
        
except Exception as e:
    print(f"❌ Error retrieving archived page: {str(e)}")
    exit()

# Parse the HTML content
print(f"\n=== PARSING HTML CONTENT ===")
soup = BeautifulSoup(response.content, 'html.parser')

# Get page title
title_element = soup.find('title')
page_title = title_element.get_text().strip() if title_element else 'Unknown'
print(f"Page title: {page_title}")

# Find the main content area (avoiding Wayback Machine navigation)
main_content = soup.find('div', {'id': 'mw-content-text'})
if not main_content:
    # Alternative selectors for content
    main_content = soup.find('div', {'class': 'mw-parser-output'})
if not main_content:
    main_content = soup.find('div', {'id': 'bodyContent'})
if not main_content:
    print("⚠️ Could not find main content div, using entire body")
    main_content = soup

print(f"Main content area identified: {main_content.name if hasattr(main_content, 'name') else 'Unknown'}")

# Extract all outbound links
print(f"\n=== EXTRACTING OUTBOUND LINKS ===")

all_links = []
internal_wikipedia_links = []
external_links = []
other_links = []

# Find all anchor tags with href attributes
for link_element in main_content.find_all('a', href=True):
    href = link_element.get('href', '')
    link_text = link_element.get_text().strip()
    
    # Skip empty hrefs or just anchors
    if not href or href.startswith('#'):
        continue
    
    # Skip Wayback Machine specific links
    if 'web.archive.org' in href or 'archive.org' in href:
        continue
    
    # Categorize links
    if href.startswith('/wiki/'):
        # Internal Wikipedia link
        article_name = href.split('/')[-1]
        article_name = unquote(article_name).replace('_', ' ')
        
        # Filter out non-article pages
        skip_prefixes = ['File:', 'Category:', 'Template:', 'User:', 'Talk:', 'Wikipedia:', 'Help:', 'Portal:', 'Special:', 'Media:']
        if not any(article_name.startswith(prefix) for prefix in skip_prefixes):
            internal_wikipedia_links.append({
                'article_name': article_name,
                'link_text': link_text,
                'href': href,
                'type': 'internal_wikipedia'
            })
    
    elif href.startswith('http://') or href.startswith('https://'):
        # External link
        external_links.append({
            'url': href,
            'link_text': link_text,
            'type': 'external'
        })
    
    else:
        # Other types of links
        other_links.append({
            'href': href,
            'link_text': link_text,
            'type': 'other'
        })
    
    # Add to comprehensive list
    all_links.append({
        'href': href,
        'link_text': link_text,
        'article_name': unquote(href.split('/')[-1]).replace('_', ' ') if href.startswith('/wiki/') else None
    })

print(f"\n=== LINK EXTRACTION RESULTS ===")
print(f"Total links found: {len(all_links)}")
print(f"Internal Wikipedia links: {len(internal_wikipedia_links)}")
print(f"External links: {len(external_links)}")
print(f"Other links: {len(other_links)}")

# Categorize internal Wikipedia links by potential relevance
print(f"\n=== CATEGORIZING INTERNAL WIKIPEDIA LINKS ===")

# Define categories based on potential relevance to fantasy literature connections
categories = {
    'fantasy': [],
    'literature': [],
    'authors': [],
    'publishers': [],
    'awards': [],
    'genres': [],
    'tolkien_related': [],
    'characters': [],
    'places': [],
    'other': []
}

# Keywords for categorization
keywords = {
    'fantasy': ['fantasy', 'epic', 'myth', 'legend', 'saga', 'dragon', 'magic', 'wizard'],
    'literature': ['literature', 'novel', 'book', 'story', 'narrative', 'fiction', 'prose'],
    'authors': ['author', 'writer', 'poet', 'novelist', 'tolkien'],
    'publishers': ['publisher', 'publishing', 'press', 'books', 'edition'],
    'awards': ['award', 'prize', 'honor', 'recognition'],
    'genres': ['genre', 'adventure', 'heroic', 'medieval', 'ancient'],
    'tolkien_related': ['tolkien', 'middle', 'earth', 'hobbit', 'ring', 'shire', 'gondor'],
    'characters': ['frodo', 'gandalf', 'aragorn', 'legolas', 'gimli', 'boromir', 'sam', 'merry', 'pippin'],
    'places': ['shire', 'rohan', 'gondor', 'mordor', 'rivendell', 'isengard', 'minas']
}

for link in internal_wikipedia_links:
    article_name = link['article_name'].lower()
    categorized = False
    
    # Check each category
    for category, category_keywords in keywords.items():
        if any(keyword in article_name for keyword in category_keywords):
            categories[category].append(link)
            categorized = True
            break
    
    # If not categorized, put in 'other'
    if not categorized:
        categories['other'].append(link)

# Display categorization results
for category, links in categories.items():
    if links:  # Only show categories with links
        print(f"\n{category.upper()}: {len(links)} links")
        # Show first 5 examples
        for i, link in enumerate(links[:5], 1):
            print(f"  {i}. {link['article_name']}")
        if len(links) > 5:
            print(f"  ... and {len(links) - 5} more")

# Save comprehensive results
print(f"\n=== SAVING RESULTS TO WORKSPACE ===")

# Save the complete data
lotr_data = {
    'extraction_metadata': {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_url': url,
        'archive_date_requested': archive_date,
        'archive_url': archive_url,
        'archive_timestamp': archive_timestamp,
        'formatted_archive_date': formatted_date,
        'page_title': page_title
    },
    'link_statistics': {
        'total_links': len(all_links),
        'internal_wikipedia_links': len(internal_wikipedia_links),
        'external_links': len(external_links),
        'other_links': len(other_links)
    },
    'categorized_links': categories,
    'all_internal_wikipedia_links': internal_wikipedia_links,
    'external_links': external_links,
    'raw_html_saved': False
}

# Save main data file
data_file = os.path.join(workspace_dir, 'lotr_wikipedia_links_july_2023.json')
with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(lotr_data, f, indent=2, ensure_ascii=False)

print(f"✅ Main data saved to: {os.path.basename(data_file)}")
print(f"   File size: {os.path.getsize(data_file):,} bytes")

# Save raw HTML for reference
html_file = os.path.join(workspace_dir, 'lotr_wikipedia_july_2023.html')
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(response.text)

lotr_data['raw_html_saved'] = True
print(f"✅ Raw HTML saved to: {os.path.basename(html_file)}")
print(f"   File size: {os.path.getsize(html_file):,} bytes")

# Update the JSON with HTML info
with open(data_file, 'w', encoding='utf-8') as f:
    json.dump(lotr_data, f, indent=2, ensure_ascii=False)

# Create summary report
summary_file = os.path.join(workspace_dir, 'extraction_summary.txt')
with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(f"THE LORD OF THE RINGS - WIKIPEDIA LINK EXTRACTION SUMMARY\n")
    f.write(f"={'='*60}\n\n")
    f.write(f"Archive Date: {formatted_date}\n")
    f.write(f"Source URL: {url}\n")
    f.write(f"Archive URL: {archive_url}\n")
    f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write(f"LINK STATISTICS:\n")
    f.write(f"- Total links found: {len(all_links)}\n")
    f.write(f"- Internal Wikipedia links: {len(internal_wikipedia_links)}\n")
    f.write(f"- External links: {len(external_links)}\n")
    f.write(f"- Other links: {len(other_links)}\n\n")
    
    f.write(f"CATEGORIZED INTERNAL LINKS:\n")
    for category, links in categories.items():
        if links:
            f.write(f"- {category.capitalize()}: {len(links)} links\n")
    
    f.write(f"\nHIGH-PRIORITY FANTASY/LITERATURE CONNECTIONS:\n")
    priority_categories = ['fantasy', 'literature', 'authors', 'genres']
    for category in priority_categories:
        if categories[category]:
            f.write(f"\n{category.upper()}:\n")
            for link in categories[category][:10]:  # First 10 in each category
                f.write(f"  - {link['article_name']}\n")

print(f"✅ Summary report saved to: {os.path.basename(summary_file)}")

print(f"\n=== EXTRACTION COMPLETE ===")
print(f"📊 Successfully extracted {len(internal_wikipedia_links)} internal Wikipedia links")
print(f"🎯 Identified {sum(len(links) for cat, links in categories.items() if cat in ['fantasy', 'literature', 'authors', 'genres'])} high-priority links")
print(f"📁 All data saved to workspace: {workspace_dir}")
print(f"🔍 Ready for path-finding analysis to 'A Song of Ice and Fire'")

# Quick preview of most promising links
print(f"\n=== MOST PROMISING LINKS FOR PATH-FINDING ===")
promising_links = []
for category in ['fantasy', 'literature', 'authors', 'awards']:
    promising_links.extend(categories[category][:3])  # Top 3 from each

if promising_links:
    print(f"Top {len(promising_links)} most promising connections:")
    for i, link in enumerate(promising_links, 1):
        print(f"  {i:2d}. {link['article_name']}")
else:
    print("⚠️ No high-priority fantasy/literature connections found")

print(f"\n✅ Archive extraction and link categorization completed successfully!")
```

## Created Time
2025-08-11 06:15:05
