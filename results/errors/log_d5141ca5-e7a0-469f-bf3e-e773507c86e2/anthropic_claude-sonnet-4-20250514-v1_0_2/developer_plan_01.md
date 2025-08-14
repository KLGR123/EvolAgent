# Developer Plan 01

## Plan
Search for and access the Wikipedia page on 'Principle of double effect' to examine its complete revision history. Extract all edits and changes made to this page from its creation to present, focusing specifically on identifying when images, pictures, or files related to St. Thomas Aquinas were first added. Look for file uploads, image insertions, or media additions in the page's edit history that reference St. Thomas Aquinas imagery.

## Description
This is the optimal starting approach because: (1) We need to locate the Wikipedia page on 'Principle of double effect' and access its complete revision history to track when St. Thomas Aquinas imagery was first added, (2) No previous research has been conducted on this specific page's edit history, (3) Expected outcome is to obtain the page's revision log and identify the specific date when a picture of St. Thomas Aquinas was first inserted, (4) This directly addresses the TASK requirement to determine the exact date (in DD/MM/YYYY format) when the St. Thomas Aquinas image was added to this philosophical concept's Wikipedia page

## Episodic Examples
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

### Development Step 2: Comprehensive revision history of “Antidisestablishmentarianism” Wikipedia page up to June 2023

**Description**: Search for and access the Wikipedia page on 'Antidisestablishmentarianism' to locate its edit history or revision log. Extract comprehensive information about all edits made to this page from its creation until June 2023, including the total number of revisions, edit timestamps, and any available metadata about the page's editing activity over time.

**Use Cases**:
- Political science trend analysis and edit conflict resolution for monitoring ideological content shifts on contentious topics
- Lexicography update automation and historical definition tracking for dictionary publishers to synchronize definitions with Wikipedia’s evolution
- Digital humanities research on collaborative editing patterns for linguistics scholars studying long-word usage and community dynamics
- Quality assurance and vandalism detection via revision metadata analysis for Wikipedia moderation teams
- Content management and SEO optimization by monitoring article update frequencies and edit summaries for digital marketing agencies
- Data engineering pipeline for populating revision metrics dashboards in enterprise knowledge management systems
- Machine learning training data preparation and feature extraction for edit classification and vandalism detection models in AI research

```
import os
import json
from datetime import datetime

print("=== INSPECTING WORKSPACE DATA STRUCTURE ===\n")
print("Objective: Understand the structure of collected data before implementing comprehensive extraction\n")

# Find workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("❌ No workspace directory found")
    exit()

workspace_dir = workspace_dirs[0]  # Use the most recent one
print(f"Using workspace directory: {workspace_dir}\n")

# List all files in workspace
workspace_files = os.listdir(workspace_dir)
print(f"Files in workspace ({len(workspace_files)} total):")

for file in workspace_files:
    file_path = os.path.join(workspace_dir, file)
    if os.path.isfile(file_path):
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")

print()

# First, inspect the JSON file structure
json_files = [f for f in workspace_files if f.endswith('.json')]
print(f"=== INSPECTING JSON FILES ({len(json_files)}) ===\n")

for json_file in json_files:
    json_path = os.path.join(workspace_dir, json_file)
    print(f"Analyzing: {json_file}")
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("Top-level structure:")
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"  {key}: Dictionary with {len(value)} keys")
                # Show nested structure for important keys
                if key in ['query', 'continue']:
                    print(f"    Nested keys: {list(value.keys())}")
            elif isinstance(value, list):
                print(f"  {key}: List with {len(value)} items")
                if len(value) > 0:
                    print(f"    First item type: {type(value[0]).__name__}")
                    if isinstance(value[0], dict):
                        print(f"    First item keys: {list(value[0].keys())}")
            else:
                print(f"  {key}: {type(value).__name__} = {value}")
        
        # If this looks like API data, inspect the revision structure
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            print(f"\n  API Data Analysis:")
            for page_id, page_data in pages.items():
                print(f"    Page ID: {page_id}")
                print(f"    Page keys: {list(page_data.keys())}")
                
                if 'revisions' in page_data:
                    revisions = page_data['revisions']
                    print(f"    Revisions: {len(revisions)} found")
                    
                    if revisions:
                        print(f"    Sample revision structure:")
                        sample_rev = revisions[0]
                        for rev_key, rev_value in sample_rev.items():
                            print(f"      {rev_key}: {type(rev_value).__name__} = {rev_value}")
                        
                        # Check date range
                        timestamps = [rev.get('timestamp', '') for rev in revisions]
                        if timestamps:
                            print(f"    Date range: {min(timestamps)} to {max(timestamps)}")
        
        # Check for continuation data
        if 'continue' in data:
            print(f"\n  Continuation data available: {data['continue']}")
            print(f"    This indicates more revisions are available via pagination")
        
        print()
        
    except Exception as e:
        print(f"  ❌ Error reading {json_file}: {str(e)}")
        print()

# Now inspect HTML files to understand their content
html_files = [f for f in workspace_files if f.endswith('.html')]
print(f"=== INSPECTING HTML FILES ({len(html_files)}) ===\n")

for html_file in html_files:
    html_path = os.path.join(workspace_dir, html_file)
    file_size = os.path.getsize(html_path)
    
    print(f"HTML File: {html_file}")
    print(f"Size: {file_size:,} bytes")
    
    # Determine file type and priority
    if 'history' in html_file.lower():
        file_type = "EDIT HISTORY PAGE - Contains revision list and pagination"
        priority = "HIGH"
    elif 'main' in html_file.lower():
        file_type = "MAIN ARTICLE PAGE - Contains current content"
        priority = "MEDIUM"
    else:
        file_type = "UNKNOWN PAGE TYPE"
        priority = "LOW"
    
    print(f"Type: {file_type}")
    print(f"Analysis Priority: {priority}")
    
    # Quick content inspection
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            # Read first few lines for preview
            content_preview = []
            for i in range(5):
                line = f.readline().strip()
                if line:
                    content_preview.append(line)
        
        print("Content preview (first 5 non-empty lines):")
        for i, line in enumerate(content_preview, 1):
            preview = line[:100] + "..." if len(line) > 100 else line
            print(f"  {i}: {preview}")
        
        # Check for key indicators
        with open(html_path, 'r', encoding='utf-8') as f:
            full_content = f.read()
        
        content_lower = full_content.lower()
        
        # Key indicators for edit history analysis
        indicators = {
            'revision_entries': content_lower.count('mw-changeslist-date'),
            'user_links': content_lower.count('mw-userlink'),
            'edit_summaries': content_lower.count('class="comment"'),
            'pagination_links': content_lower.count('offset='),
            'timestamps_2023': content_lower.count('2023'),
            'timestamps_2022': content_lower.count('2022'),
            'timestamps_2021': content_lower.count('2021'),
            'older_revisions': content_lower.count('older'),
            'revision_ids': content_lower.count('revid')
        }
        
        print("Key indicators found:")
        for indicator, count in indicators.items():
            if count > 0:
                status = "🔥" if count > 50 else "✅" if count > 10 else "⚠️" if count > 0 else "❌"
                print(f"  {status} {indicator}: {count}")
        
        # Calculate analysis priority score
        priority_score = sum([
            indicators['revision_entries'] * 5,
            indicators['user_links'] * 3,
            indicators['edit_summaries'] * 3,
            indicators['pagination_links'] * 10,
            indicators['timestamps_2023'] * 2,
            indicators['timestamps_2022'] * 3,
            indicators['timestamps_2021'] * 3
        ])
        
        print(f"Analysis priority score: {priority_score}")
        
        if priority_score > 500:
            print("  🎯 HIGHEST PRIORITY - Rich revision data available")
        elif priority_score > 100:
            print("  ⭐ HIGH PRIORITY - Good revision data available")
        elif priority_score > 20:
            print("  ✅ MEDIUM PRIORITY - Some revision data available")
        else:
            print("  ⚠️ LOW PRIORITY - Limited revision data")
        
        print()
        
    except Exception as e:
        print(f"  ❌ Error inspecting {html_file}: {str(e)}")
        print()

# Summary and next steps
print("=== WORKSPACE INSPECTION SUMMARY ===\n")

# Determine the best approach based on available data
api_data_available = any('api' in f.lower() for f in json_files)
history_page_available = any('history' in f.lower() for f in html_files)

print(f"📊 Data Sources Available:")
print(f"  API data: {'✅' if api_data_available else '❌'}")
print(f"  HTML history page: {'✅' if history_page_available else '❌'}")
print(f"  Total files: {len(workspace_files)}")

# Recommend next steps
print(f"\n🎯 Recommended Implementation Strategy:")

if api_data_available and history_page_available:
    print("  1. HYBRID APPROACH - Use both API and HTML parsing")
    print("     • API for structured data and efficient pagination")
    print("     • HTML parsing as backup and validation")
    print("     • Cross-reference both sources for completeness")
elif api_data_available:
    print("  1. API-FIRST APPROACH - Use Wikipedia API with pagination")
    print("     • Implement rvlimit and rvcontinue for complete history")
    print("     • Filter by timestamp to get data until June 2023")
elif history_page_available:
    print("  1. HTML PARSING APPROACH - Parse history page with pagination")
    print("     • Follow 'older' links to traverse complete history")
    print("     • Extract revision data from HTML structure")
else:
    print("  ❌ INSUFFICIENT DATA - Need to re-collect data")

print(f"\n📋 Implementation Requirements:")
print(f"  • Implement pagination to get ALL revisions from creation")
print(f"  • Add date filtering to only include revisions before June 2023")
print(f"  • Extract comprehensive metadata: timestamp, user, size, comment, revision ID")
print(f"  • Handle rate limiting and respectful API usage")
print(f"  • Create comprehensive output with statistics and analysis")

print(f"\n✅ Workspace inspection complete - Ready for comprehensive extraction implementation")
```

### Development Step 5: Compile Antidisestablishmentarianism Wikipedia Revision History: Total Edits, Timestamps, Metadata Until June 2023

**Description**: Search for and access the Wikipedia page on 'Antidisestablishmentarianism' to locate its edit history or revision log. Extract comprehensive information about all edits made to this page from its creation until June 2023, including the total number of revisions, edit timestamps, and any available metadata about the page's editing activity over time.

**Use Cases**:
- Journalistic investigation tracking edit patterns on politically sensitive Wikipedia pages to identify potential lobbying influences and provide evidence in news articles
- Legal compliance auditing by law firms extracting complete revision history of high-profile article pages to prepare defamation or IP infringement cases with documented edit timelines
- Academic research in political science analyzing longitudinal changes in the definition of ideological terms like Antidisestablishmentarianism to chart conceptual evolution over decades
- Machine learning dataset creation for automated vandalism detection by extracting metadata and user activity patterns from Wikipedia revision logs to train classification models
- Digital humanities timeline visualization of semantic shifts by mapping article size, comment, and edit frequency data onto interactive graphs illustrating the cultural impact of specific terms
- Corporate reputation management monitoring brand-related Wikipedia pages for unauthorized content or defamation by collecting real-time revision metadata and alerting PR teams to critical edits
- Search engine optimization strategy development analyzing historical keyword usage and page size evolution on Wikipedia entries to inform on-page SEO best practices and content structure
- Government transparency reporting archiving pre-policy-change Wikipedia revision histories to comply with open data mandates and allow public auditing of edits before legislative updates

```
import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import time
from urllib.parse import urljoin, quote
from collections import Counter

print("=== COMPREHENSIVE ANTIDISESTABLISHMENTARIANISM REVISION EXTRACTION ===\n")
print("Objective: Extract ALL revisions from creation until June 2023 using Wikipedia API\n")

# Create workspace directory
workspace_dir = f"workspace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(workspace_dir, exist_ok=True)
print(f"Created workspace directory: {workspace_dir}\n")

# DEFINE ALL GLOBAL VARIABLES FIRST TO AVOID SCOPE ISSUES
page_title = "Antidisestablishmentarianism"
cutoff_date = "2023-06-30T23:59:59Z"  # End of June 2023
api_url = "https://en.wikipedia.org/w/api.php"  # DEFINED EARLY TO AVOID SCOPE ISSUES

print(f"Target page: {page_title}")
print(f"Cutoff date: {cutoff_date} (end of June 2023)")
print(f"API endpoint: {api_url}\n")

# Set up headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Function to make API request with rate limiting
def make_api_request(params, delay=1.0):
    """Make API request with rate limiting and error handling"""
    try:
        print(f"  Making API request to: {api_url}")
        print(f"  Parameters: {list(params.keys())}")
        
        time.sleep(delay)  # Respectful rate limiting
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        
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
max_requests = 100  # Reasonable limit to avoid overwhelming the API
revisions_after_cutoff = 0

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
            if is_before_cutoff(timestamp, cutoff_date):
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
            'target_page': page_title,
            'cutoff_date': cutoff_date,
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
            'target_page': page_title,
            'cutoff_date': cutoff_date,
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
        f.write(f"Target Page: {page_title}\n")
        f.write(f"Cutoff Date: {cutoff_date}\n\n")
        
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

### Development Step 3: Extract Antidisestablishmentarianism Wikipedia Revision History and Metadata Up to June 2023

**Description**: Search for and access the Wikipedia page on 'Antidisestablishmentarianism' to locate its edit history or revision log. Extract comprehensive information about all edits made to this page from its creation until June 2023, including the total number of revisions, edit timestamps, and any available metadata about the page's editing activity over time.

**Use Cases**:
- For a digital humanities scholar analyzing the semantic shifts of controversial terms, use the pipeline to extract the full ‘Antidisestablishmentarianism’ revision log and measure how definitions and emphasis changed from inception to June 2023.
- For a machine learning engineer building a vandalism detection model, fetch every edit’s metadata on ‘Antidisestablishmentarianism’—including user, timestamp, comment and size—to create a labeled dataset of benign vs. malicious contributions.
- For a journalist fact-checking a disputed claim, compile the complete edit history of ‘Antidisestablishmentarianism’ through June 2023 to pinpoint when and by whom key statements were added, modified or removed.
- For a plagiarism investigator tracing unauthorized content reuse, retrieve all revisions of ‘Antidisestablishmentarianism’ to compare versions, document original contributors, and produce an evidentiary timeline of text changes.
- For an instructor teaching collaborative knowledge workflows, export the ‘Antidisestablishmentarianism’ edit history to illustrate real-world peer-review dynamics, peak editing periods, and the influence of top contributors.
- For an SEO and brand reputation manager monitoring term usage, adapt the solution to extract Wikipedia revisions of targeted pages, detect when promotional or misleading text is introduced, and log responsible user accounts.
- For a data analyst visualizing community engagement trends, use the comprehensive ‘Antidisestablishmentarianism’ revision dataset to plot annual edit volumes, identify spikes in activity, and correlate them with external events (e.g., academic publications).
- For a compliance officer in a non-profit, maintain an auditable archive of all policy-related Wikipedia changes by regularly extracting and storing full revision histories—ensuring transparency and fulfilling reporting obligations.

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

# Set up headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Wikipedia API endpoint
api_url = "https://en.wikipedia.org/w/api.php"

# Function to make API request with rate limiting
def make_api_request(params, delay=1.0):
    """Make API request with rate limiting and error handling"""
    try:
        time.sleep(delay)  # Respectful rate limiting
        response = requests.get(api_url, params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API request failed: HTTP {response.status_code}")
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
    except:
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
    
    print(f"Request {total_requests}: Fetching up to 500 revisions...")
    if continue_token:
        print(f"  Using continuation: {continue_token}")
    
    # Make the API request
    api_data = make_api_request(api_params, delay=1.5)
    
    if not api_data:
        print(f"❌ Failed to get API response, stopping extraction")
        break
    
    # Process the response
    if 'query' not in api_data or 'pages' not in api_data['query']:
        print(f"❌ Unexpected API response structure")
        break
    
    pages = api_data['query']['pages']
    page_found = False
    
    for page_id, page_data in pages.items():
        if 'missing' in page_data:
            print(f"❌ Page '{page_title}' not found")
            break
        
        if 'revisions' not in page_data:
            print(f"❌ No revisions found in response")
            break
        
        page_found = True
        revisions = page_data['revisions']
        print(f"  Retrieved {len(revisions)} revisions")
        
        # Process each revision
        revisions_before_cutoff = 0
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
                # We've reached revisions after June 2023, but continue
                # since we're going backwards in time
                pass
        
        print(f"  Date range: {oldest_timestamp} to {newest_timestamp}")
        print(f"  Revisions before June 2023: {revisions_before_cutoff}")
        print(f"  Total collected so far: {len(all_revisions)}")
        
        # Check if we should continue
        if 'continue' in api_data:
            continue_token = api_data['continue']
            print(f"  More data available, continuing...")
        else:
            print(f"  ✅ Reached end of revision history")
            break
    
    if not page_found:
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
            # Escape commas in comments
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

## Created Time
2025-08-13 22:32:05
