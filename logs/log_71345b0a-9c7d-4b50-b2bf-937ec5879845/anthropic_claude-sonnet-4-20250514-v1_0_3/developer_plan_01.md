# Developer Plan 01

## Plan
Search for leap days that occurred before 2008 and identify the specific dates (February 29th in leap years: 2004, 2000, 1996, 1992, etc.). Then access the Wikipedia revision history for the 'Dragon' page to examine edits made on those leap days, focusing on content removals that appear to be jokes or humorous additions. Extract the specific phrase that was removed from the page during one of these leap day edits.

## Description
This is the optimal starting approach because: (1) We need to identify the specific leap day before 2008 when a joke was removed from the Dragon Wikipedia page, (2) No previous research has been conducted, (3) Expected outcome is to locate the relevant leap day edit in Wikipedia's revision history and identify the removed joke phrase, (4) This directly targets the specific edit event described in the TASK by focusing on leap days (February 29th) in years 2004, 2000, 1996, etc.

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

### Development Step 40: Extract common disparaging word from dragon portrayal quotes in Emily Midkiff’s June 2014 Fafnir article

**Description**: Access Emily Midkiff's June 2014 article in the Fafnir journal to extract the full text and identify the specific word that was quoted from two different authors expressing distaste for the nature of dragon depictions. Parse the article content systematically to locate quotes from multiple authors that contain the same critical word about dragon portrayals.

**Use Cases**:
- Literary criticism archiving: Automatically extract and collate critical adjectives from fantasy journals to build a reference of scholarly sentiment on dragon characters for an author writing a meta-analysis
- Higher education course preparation: Pull out recurring critical terms from Midkiff’s Fafnir article to create lecture slides on contemporary scholarly critiques of mythic creatures
- Digital humanities project: Process a corpus of mythology journals to identify and compare key negative descriptors of dragons across different time periods
- Publishing industry fact-checking: Scan submitted dragon-focused manuscripts to ensure authors accurately reference and quote established criticism from academic sources
- AI-driven content moderation: Train a model to detect and flag overly critical or negative language in user-generated fantasy lore based on extracted keywords from scholarly texts
- Museum exhibit curation: Extract and summarize critical terms from historical and modern scholarship to craft exhibit labels that challenge or reinforce public perceptions of dragons
- Online encyclopedia updating: Automatically detect and update entries with historically significant critical quotes about dragons to maintain scholarly accuracy in mythological articles

```
import os
import json

# First, let's inspect the workspace to understand what files we have
workspace = 'workspace'
print('=== ANALYZING EMILY MIDKIFF ARTICLE FOR DRAGON CRITICISM QUOTES ===')
print('Objective: Find the specific word quoted from two different authors expressing distaste for dragon depictions\n')

if not os.path.exists(workspace):
    print(f'ERROR: Workspace directory {workspace} not found')
else:
    print(f'Files in workspace:')
    for file in os.listdir(workspace):
        file_path = os.path.join(workspace, file)
        if os.path.isfile(file_path):
            size = os.path.getsize(file_path)
            print(f'  - {file} ({size:,} bytes)')
    print()

# Check if we have the article text file
article_text_file = os.path.join(workspace, 'midkiff_fafnir_article_full_text.txt')
if not os.path.exists(article_text_file):
    print(f'ERROR: Article text file not found at {article_text_file}')
else:
    print(f'✓ Found article text file: {article_text_file}')
    
    # Read the full article text
    with open(article_text_file, 'r', encoding='utf-8') as f:
        article_content = f.read()
    
    print(f'Article content length: {len(article_content):,} characters\n')
    
    # Extract just the main article text (skip the header metadata)
    if '=' * 80 in article_content:
        main_text = article_content.split('=' * 80, 1)[1].strip()
    else:
        main_text = article_content
    
    print(f'Main article text length: {len(main_text):,} characters\n')
    
    print('=== STEP 1: SEARCHING FOR ACADEMIC QUOTES WITH MULTIPLE METHODS ===')
    print()
    
    # Method 1: Look for text between various quote marks
    quote_patterns = [
        ('"', '"'),  # Regular double quotes
        ('
```

### Development Step 18: Search Emily Midkiff’s June 2014 Dragon Depictions Article to Find Hreidmar Son-Named Journal

**Description**: Search for information about Emily Midkiff's June 2014 article, focusing on identifying the journal named after one of Hreidmar's sons from Norse mythology. Research Hreidmar's sons (Fafnir, Regin, and Otr) to determine which one has a journal named after them, then locate Midkiff's specific article from June 2014 that discusses dragon depictions and contains quotes from two different authors expressing distaste.

**Use Cases**:
- A Norse mythology scholar automating the extraction of Fafnir journal links from saved HTML search results to compile all June 2014 articles on dragon symbolism for a comprehensive literature review
- A university librarian processing archived web dumps of Fafnir to generate a JSON inventory of articles and metadata, streamlining the cataloguing of early 2010s journal issues in the institutional repository
- A PhD candidate in medieval studies using the script to locate Emily Midkiff’s June 2014 discussion on dragon depictions, quickly gathering author quotes expressing distaste for critical analysis in their dissertation
- A digital archivist at a cultural heritage center harvesting and cross‐referencing article URLs and key term counts from multiple search result files to build a searchable database of primary sources on mythological creatures
- A metadata specialist at an academic publisher automating link extraction and term frequency analysis for back‐issue content of Fafnir, integrating the results into the content management system for author and topic indexing
- An AI research assistant fixing variable scope issues in a scraper pipeline to analyze saved search pages, extract relevant academic links, and produce structured JSON inventories for downstream NLP processing
- A competitive intelligence analyst at a media monitoring agency extracting and analyzing historical references to “dragon depictions” across archival HTML files to track sentiment trends and author stances in niche publications
- A software QA engineer validating web scraping workflows by injecting pre-saved search and archive HTML pages, verifying link extraction accuracy, JSON output integrity, and bug fixes for reliable data pipeline operation

```
import os
import json
from bs4 import BeautifulSoup

print('=== ANALYZING SEARCH RESULTS FOR EMILY MIDKIFF ARTICLE ===')
print('Objective: Fix variable scope issues and extract Emily Midkiff article from saved search results')
print('Strategy: Analyze saved search result files to locate and access the target article\n')

# Define workspace path
workspace = 'workspace'
if not os.path.exists(workspace):
    print(f'ERROR: Workspace directory {workspace} does not exist')
else:
    print(f'✓ Workspace directory found: {workspace}')

print('\n=== STEP 1: INSPECTING SAVED SEARCH RESULT FILES ===')
print()

# First, let's understand what search result files we have
try:
    workspace_files = os.listdir(workspace)
    search_files = [f for f in workspace_files if 'search_results' in f and f.endswith('.html')]
    
    print(f'Found {len(search_files)} search result files:')
    for i, filename in enumerate(search_files, 1):
        filepath = os.path.join(workspace, filename)
        file_size = os.path.getsize(filepath)
        print(f'  {i}. {filename} ({file_size:,} bytes)')
except Exception as e:
    print(f'Error listing search files: {str(e)}')

print('\n=== STEP 2: ANALYZING MOST PROMISING SEARCH RESULTS ===')
print()

# Based on the HISTORY, we know these searches found relevant terms:
# - Emily Midkiff: found 'june(2)' 
# - Midkiff: found 'june(2)'
# - dragon depictions: found 'dragon(1)', 'june(2)'
# - June 2014: found '2014(7)', 'june(5)'

priority_search_files = [
    'search_results_Emily_Midkiff.html',
    'search_results_Midkiff.html', 
    'search_results_dragon_depictions.html',
    'search_results_June_2014.html'
]

for search_file in priority_search_files:
    search_path = os.path.join(workspace, search_file)
    if os.path.exists(search_path):
        print(f'Analyzing: {search_file}')
        
        try:
            with open(search_path, 'r', encoding='utf-8') as f:
                search_content = f.read()
            
            search_soup = BeautifulSoup(search_content, 'html.parser')
            search_text = search_soup.get_text().lower()
            
            print(f'  Content length: {len(search_content):,} characters')
            
            # Count key terms to verify our search worked
            key_terms = {
                'midkiff': search_text.count('midkiff'),
                'emily': search_text.count('emily'),
                'dragon': search_text.count('dragon'),
                'june': search_text.count('june'),
                '2014': search_text.count('2014'),
                'depiction': search_text.count('depiction'),
                'distaste': search_text.count('distaste')
            }
            
            print('  Key term counts:')
            for term, count in key_terms.items():
                if count > 0:
                    print(f'    {term}: {count} occurrences')
            
            # Look for article links - fix the variable scope issue from previous attempts
            article_links = search_soup.find_all('a', href=True)
            relevant_links = []
            
            for link in article_links:
                href = link.get('href', '')
                link_text = link.get_text().strip()  # FIX: Define link_text variable properly
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    full_url = f'https://fafnir.journal.fi{href}'
                elif not href.startswith('http'):
                    full_url = f'https://fafnir.journal.fi/{href}'
                else:
                    full_url = href
                
                # Check if this looks like an article link with relevant content
                link_text_lower = link_text.lower()
                href_lower = href.lower()
                
                # Look for article patterns and relevant terms
                is_article = '/article/' in href_lower or '/view/' in href_lower
                has_relevant_terms = any(term in link_text_lower for term in ['midkiff', 'dragon', '2014', 'june'])
                is_substantial = len(link_text.strip()) > 10
                
                if (is_article or has_relevant_terms) and is_substantial:
                    relevant_links.append({
                        'url': full_url,
                        'text': link_text[:150],
                        'href': href,
                        'is_article': is_article,
                        'has_relevant_terms': has_relevant_terms
                    })
            
            print(f'  Found {len(relevant_links)} potentially relevant links:')
            for i, link in enumerate(relevant_links[:5], 1):
                print(f'    {i}. "{link["text"]}"')
                print(f'       URL: {link["url"]}')
                print(f'       Article link: {link["is_article"]}, Relevant terms: {link["has_relevant_terms"]}')
                print()
            
            # If we found promising links, save them for access
            if relevant_links:
                links_data = {
                    'search_file': search_file,
                    'key_terms_found': key_terms,
                    'relevant_links': relevant_links[:10],
                    'analysis_timestamp': 'search_results_analyzed'
                }
                
                links_file = os.path.join(workspace, f'extracted_links_{search_file.replace(".html", ".json")}')
                with open(links_file, 'w', encoding='utf-8') as f:
                    json.dump(links_data, f, indent=2, ensure_ascii=False)
                
                print(f'  ✓ Link analysis saved to: {os.path.basename(links_file)}')
        
        except Exception as e:
            print(f'  Error analyzing {search_file}: {str(e)}')
        
        print()
    else:
        print(f'  ⚠ File not found: {search_file}')

print('=== STEP 3: ANALYZING ARCHIVE FILES FOR 2014 CONTENT ===')
print()

# Also check the archive files we saved
archive_files = [f for f in workspace_files if 'archive' in f and f.endswith('.html')]

for archive_file in archive_files:
    if '2014' in archive_file:
        archive_path = os.path.join(workspace, archive_file)
        print(f'Analyzing archive file: {archive_file}')
        
        try:
            with open(archive_path, 'r', encoding='utf-8') as f:
                archive_content = f.read()
            
            archive_soup = BeautifulSoup(archive_content, 'html.parser')
            archive_text = archive_soup.get_text().lower()
            
            # Look for 2014 and Midkiff content
            archive_terms = {
                'midkiff': archive_text.count('midkiff'),
                'emily': archive_text.count('emily'),
                'dragon': archive_text.count('dragon'),
                'june': archive_text.count('june'),
                '2014': archive_text.count('2014')
            }
            
            print('  Archive content analysis:')
            for term, count in archive_terms.items():
                if count > 0:
                    print(f'    {term}: {count} occurrences')
            
            # If this archive page has relevant content, extract article links
            if archive_terms['midkiff'] > 0 or (archive_terms['2014'] > 0 and archive_terms['june'] > 0):
                print('  🎯 RELEVANT CONTENT FOUND IN ARCHIVE!')
                
                archive_links = archive_soup.find_all('a', href=True)
                archive_article_links = []
                
                for link in archive_links:
                    href = link.get('href', '')
                    link_text = link.get_text().strip()
                    
                    if href.startswith('/'):
                        full_url = f'https://fafnir.journal.fi{href}'
                    elif not href.startswith('http'):
                        full_url = f'https://fafnir.journal.fi/{href}'
                    else:
                        full_url = href
                    
                    # Look for article links
                    if '/article/' in href.lower() or '/view/' in href.lower():
                        archive_article_links.append({
                            'url': full_url,
                            'text': link_text[:100],
                            'href': href
                        })
                
                if archive_article_links:
                    print(f'  Found {len(archive_article_links)} article links in archive:')
                    for i, link in enumerate(archive_article_links[:3], 1):
                        print(f'    {i}. "{link["text"]}"')
                        print(f'       URL: {link["url"]}')
        
        except Exception as e:
            print(f'  Error analyzing {archive_file}: {str(e)}')
        
        print()

print('=== STEP 4: CREATING COMPREHENSIVE LINK INVENTORY ===')
print()

# Compile all the promising links we've found
all_promising_links = []

# Check all the extracted link files we created
for filename in os.listdir(workspace):
    if filename.startswith('extracted_links_') and filename.endswith('.json'):
        link_file_path = os.path.join(workspace, filename)
        
        try:
            with open(link_file_path, 'r', encoding='utf-8') as f:
                link_data = json.load(f)
            
            if 'relevant_links' in link_data:
                for link in link_data['relevant_links']:
                    link['source_search'] = filename
                    all_promising_links.append(link)
        
        except Exception as e:
            print(f'Error reading {filename}: {str(e)}')

# Remove duplicates based on URL
unique_links = []
seen_urls = set()

for link in all_promising_links:
    if link['url'] not in seen_urls:
        seen_urls.add(link['url'])
        unique_links.append(link)

print(f'Found {len(unique_links)} unique promising links across all searches:')
for i, link in enumerate(unique_links, 1):
    print(f'  {i}. "{link["text"]}"')
    print(f'     URL: {link["url"]}')
    print(f'     Source: {link.get("source_search", "unknown")}')
    print(f'     Article link: {link.get("is_article", False)}')
    print()

# Save the comprehensive link inventory
link_inventory = {
    'research_objective': 'Find Emily Midkiff June 2014 article in Fafnir journal about dragon depictions',
    'total_unique_links': len(unique_links),
    'promising_links': unique_links,
    'search_files_analyzed': [f for f in workspace_files if 'search_results' in f],
    'archive_files_analyzed': [f for f in workspace_files if 'archive' in f],
    'next_steps': 'Access the most promising article links to find Emily Midkiff content',
    'inventory_timestamp': 'comprehensive_analysis_complete'
}

inventory_file = os.path.join(workspace, 'emily_midkiff_link_inventory.json')
with open(inventory_file, 'w', encoding='utf-8') as f:
    json.dump(link_inventory, f, indent=2, ensure_ascii=False)

print('=== STEP 5: FINAL ANALYSIS SUMMARY ===')
print()

print('🎯 *** SEARCH RESULT ANALYSIS COMPLETE ***')
print('✅ Fixed variable scope issues from previous attempts')
print('✅ Successfully analyzed all saved search result files')
print('✅ Extracted and categorized relevant article links')
print('✅ Created comprehensive inventory of promising leads')
print(f'✅ Found {len(unique_links)} unique links to investigate')
print(f'✅ Complete analysis saved to: {os.path.basename(inventory_file)}')

print('\n📋 PLAN COMPLETION STATUS:')
print('- ✅ Norse mythology research: Hreidmar\'s sons are Fafnir (dragon), Regin, Otr')
print('- ✅ Journal identification: Fafnir journal named after the dragon son')
print('- ✅ Website access: Successfully accessed Fafnir journal')
print('- ✅ Search implementation: Multiple search strategies executed')
print('- ✅ Results analysis: Search results processed and links extracted')
print('- 🔍 Next: Access promising article links to locate Emily Midkiff\'s specific article')

print('\n📁 KEY FILES FOR NEXT STEPS:')
print(f'  - Link inventory: {os.path.basename(inventory_file)}')
for filename in os.listdir(workspace):
    if filename.startswith('extracted_links_'):
        print(f'  - Detailed analysis: {filename}')

print('\n*** SEARCH ANALYSIS EXECUTION COMPLETE ***')
print('Ready to access the most promising article links to complete the research objective')
```

### Development Step 8: Extract July 3 2023 LOTR Wikipedia Outbound Links Toward A Song of Ice and Fire

**Description**: Access the archived Wikipedia page for 'The Lord of the Rings' (book) as it appeared at the end of July 3, 2023. Use the Wayback Machine or Wikipedia's revision history to retrieve the specific version from that date. Extract all outbound links from the page content, focusing on internal Wikipedia links that could potentially lead toward 'A Song of Ice and Fire'. Create a comprehensive list of linked pages including literature, fantasy, author, publisher, and genre-related links that might serve as stepping stones in the path-finding process.

**Use Cases**:
- Digital humanities research: mapping interlinking between fantasy literature pages on Wikipedia to analyze the thematic evolution from “The Lord of the Rings” to “A Song of Ice and Fire”
- Fan community website automation: extracting and categorizing internal links from the July 3, 2023 LOTR archive to automatically update character, location, and lore indexes
- Publishing market intelligence: analyzing Tolkien‐related outbound links and award categories to identify emerging authors and genre trends for editorial acquisition strategies
- Educational content auditing: retrieving archived Wikipedia snapshots and extracting author and genre links to ensure digital course materials cover all relevant literary themes
- Recommendation engine enhancement: using categorized fantasy and literature links to build graph-based book suggestions connecting Tolkien’s works to George R.R. Martin in a subscription reading platform
- Library digital archives quality control: monitoring Wikipedia revision history and link extraction to validate and enrich metadata for epic fantasy holdings
- SEO optimization for a literature blog: auditing outbound Wikipedia links from archived articles to update affiliate and resource pages with accurate genre and author cross‐references
- Wikipedia editorial QA: extracting archived link structures to detect missing or broken internal references and automate edit suggestions for epic fantasy articles

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from urllib.parse import unquote

print("=== ACCESSING THE LORD OF THE RINGS WIKIPEDIA PAGE FOR LINK EXTRACTION ===")
print("Objective: Extract all outbound links for path-finding analysis\n")

# First, check if we have any existing workspace or data
print("=== CHECKING FOR EXISTING WORKSPACE DATA ===")
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    print(f"Found existing workspace directories: {workspace_dirs}")
    # Check if we already have LOTR link data
    for ws_dir in workspace_dirs:
        files = os.listdir(ws_dir)
        lotr_files = [f for f in files if 'lotr' in f.lower() and 'link' in f.lower()]
        if lotr_files:
            print(f"\nFound existing LOTR link data in {ws_dir}:")
            for f in lotr_files:
                file_path = os.path.join(ws_dir, f)
                file_size = os.path.getsize(file_path)
                print(f"  - {f} ({file_size:,} bytes)")
            
            # Let's inspect the structure of the existing data
            largest_file = max(lotr_files, key=lambda f: os.path.getsize(os.path.join(ws_dir, f)))
            print(f"\nInspecting structure of largest file: {largest_file}")
            
            try:
                with open(os.path.join(ws_dir, largest_file), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print("\nFile structure:")
                for key, value in data.items():
                    if isinstance(value, dict):
                        print(f"  {key}: Dictionary with {len(value)} keys")
                        for nested_key, nested_value in value.items():
                            if isinstance(nested_value, list):
                                print(f"    {nested_key}: List with {len(nested_value)} items")
                            elif isinstance(nested_value, dict):
                                print(f"    {nested_key}: Dictionary with {len(nested_value)} keys")
                            else:
                                print(f"    {nested_key}: {type(nested_value).__name__} = {nested_value}")
                    elif isinstance(value, list):
                        print(f"  {key}: List with {len(value)} items")
                    else:
                        print(f"  {key}: {type(value).__name__} = {value}")
                
                # If we have good data, use it; otherwise proceed with new extraction
                if 'all_internal_wikipedia_links' in data or 'categorized_links' in data:
                    print(f"\n✅ Found existing comprehensive LOTR link data!")
                    print(f"Using existing data from: {ws_dir}/{largest_file}")
                    existing_data = data
                    workspace_dir = ws_dir
                    use_existing = True
                else:
                    print(f"\n⚠️ Existing data incomplete, will extract fresh data")
                    use_existing = False
            except Exception as e:
                print(f"\n❌ Error reading existing data: {e}")
                use_existing = False
            
            if 'use_existing' in locals() and use_existing:
                break
else:
    print("No existing workspace found")
    use_existing = False

# If no existing data, extract fresh data from current or archived version
if not ('use_existing' in locals() and use_existing):
    # Create new workspace
    workspace_dir = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(workspace_dir, exist_ok=True)
    print(f"\nCreated new workspace: {workspace_dir}")
    
    # Try alternative approaches for getting the page
    print("\n=== ATTEMPTING ALTERNATIVE ACCESS METHODS ===")
    
    # Method 1: Try current Wikipedia page (as fallback)
    print("\n1. Trying current Wikipedia page as fallback...")
    
    url = "https://en.wikipedia.org/wiki/The_Lord_of_the_Rings"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Successfully accessed current Wikipedia page")
            print(f"Content length: {len(response.content):,} bytes")
            
            # Parse the content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get page title
            title_element = soup.find('title')
            page_title = title_element.get_text().strip() if title_element else 'Unknown'
            print(f"Page title: {page_title}")
            
            # Find main content area
            main_content = soup.find('div', {'id': 'mw-content-text'})
            if not main_content:
                main_content = soup.find('div', {'class': 'mw-parser-output'})
            if not main_content:
                main_content = soup.find('div', {'id': 'bodyContent'})
            if not main_content:
                print("⚠️ Could not find main content div, using entire body")
                main_content = soup
            
            print(f"Main content area identified")
            
            # Extract all outbound links
            print(f"\n=== EXTRACTING OUTBOUND LINKS ===")
            
            all_links = []
            internal_wikipedia_links = []
            external_links = []
            
            # Process all anchor tags with href attributes
            for link_element in main_content.find_all('a', href=True):
                href = link_element.get('href', '')
                link_text = link_element.get_text().strip()
                
                # Skip empty hrefs or just anchors
                if not href or href.startswith('#'):
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
            
            # Categorize internal Wikipedia links by relevance
            print(f"\n=== CATEGORIZING INTERNAL WIKIPEDIA LINKS ===")
            
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
            
            lotr_data = {
                'extraction_metadata': {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'source_url': url,
                    'method': 'current_wikipedia_page',
                    'page_title': page_title,
                    'note': 'Extracted from current Wikipedia page as July 3, 2023 archive was not available'
                },
                'link_statistics': {
                    'total_links': len(all_links),
                    'internal_wikipedia_links': len(internal_wikipedia_links),
                    'external_links': len(external_links)
                },
                'categorized_links': categories,
                'all_internal_wikipedia_links': internal_wikipedia_links,
                'external_links': external_links
            }
            
            # Save main data file
            data_file = os.path.join(workspace_dir, 'lotr_wikipedia_links_july_2023.json')
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(lotr_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Main data saved to: {os.path.basename(data_file)}")
            print(f"   File size: {os.path.getsize(data_file):,} bytes")
            
            # Save raw HTML for reference
            html_file = os.path.join(workspace_dir, 'lotr_wikipedia_current.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"✅ Raw HTML saved to: {os.path.basename(html_file)}")
            print(f"   File size: {os.path.getsize(html_file):,} bytes")
            
            existing_data = lotr_data
            
        else:
            print(f"❌ Failed to access current Wikipedia page: HTTP {response.status_code}")
            exit()
            
    except Exception as e:
        print(f"❌ Error accessing Wikipedia page: {str(e)}")
        exit()

# Now analyze the data we have (either existing or newly extracted)
print(f"\n=== ANALYZING EXTRACTED LINKS FOR PATH-FINDING ===")

if 'existing_data' in locals():
    # Get high-priority links for fantasy literature connections
    high_priority_links = []
    
    if 'categorized_links' in existing_data:
        categories = existing_data['categorized_links']
        priority_categories = ['fantasy', 'literature', 'authors', 'awards', 'genres']
        
        for category in priority_categories:
            if category in categories:
                high_priority_links.extend(categories[category])
        
        print(f"\nHigh-priority links for fantasy literature connections: {len(high_priority_links)}")
        
        # Show top connections in each priority category
        for category in priority_categories:
            if category in categories and categories[category]:
                print(f"\n{category.upper()}: {len(categories[category])} links")
                for i, link in enumerate(categories[category][:5], 1):
                    print(f"  {i}. {link['article_name']}")
                if len(categories[category]) > 5:
                    print(f"  ... and {len(categories[category]) - 5} more")
    
    # Create a summary of the most promising stepping stones
    print(f"\n=== MOST PROMISING STEPPING STONES TO 'A SONG OF ICE AND FIRE' ===")
    
    # These are the types of links most likely to lead to George R.R. Martin
    stepping_stones = []
    
    for link in high_priority_links:
        article_name = link['article_name'].lower()
        if any(keyword in article_name for keyword in 
               ['fantasy literature', 'fantasy author', 'epic fantasy', 'high fantasy', 
                'fantasy award', 'fantasy series', 'contemporary fantasy', 'fantasy novel']):
            stepping_stones.append(link)
    
    if stepping_stones:
        print(f"\nFound {len(stepping_stones)} direct fantasy literature stepping stones:")
        for i, stone in enumerate(stepping_stones, 1):
            print(f"  {i}. {stone['article_name']}")
    else:
        print("\nNo direct fantasy literature stepping stones found")
        print("Alternative approach: Look for broader literature/genre connections")
    
    # Save analysis results
    analysis_results = {
        'analysis_metadata': {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source_data': 'existing_data' if 'use_existing' in locals() and use_existing else 'newly_extracted',
            'total_internal_links': len(existing_data.get('all_internal_wikipedia_links', [])),
            'high_priority_links': len(high_priority_links),
            'direct_stepping_stones': len(stepping_stones) if stepping_stones else 0
        },
        'high_priority_links': high_priority_links,
        'stepping_stones': stepping_stones if stepping_stones else [],
        'path_finding_ready': True
    }
    
    analysis_file = os.path.join(workspace_dir, 'lotr_path_finding_analysis.json')
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✅ Path-finding analysis saved to: {os.path.basename(analysis_file)}")
    
    print(f"\n=== EXTRACTION AND ANALYSIS COMPLETE ===")
    print(f"📊 Total internal Wikipedia links extracted: {len(existing_data.get('all_internal_wikipedia_links', []))}")
    print(f"🎯 High-priority fantasy/literature links: {len(high_priority_links)}")
    print(f"🔗 Direct stepping stones identified: {len(stepping_stones) if stepping_stones else 0}")
    print(f"📁 All data saved to workspace: {workspace_dir}")
    print(f"✅ Ready for path-finding analysis to 'A Song of Ice and Fire'")
    
    # Show next steps
    print(f"\n=== NEXT STEPS FOR PATH-FINDING ===")
    print(f"1. Use the extracted links as starting points for BFS search")
    print(f"2. Focus on high-priority fantasy/literature connections")
    print(f"3. Look for connections through authors, awards, and genre pages")
    print(f"4. Target variations: 'A Song of Ice and Fire', 'Game of Thrones', 'George R.R. Martin'")
    
else:
    print("❌ No data available for analysis")
```

## Created Time
2025-08-08 23:03:49
