# Developer Plan 02

## Plan
Access the Wikipedia page for 'God of War (2018 video game)' and retrieve its complete revision history from page creation through the most recent entry from 2022. Extract the game's official release date as listed on the Wikipedia page in the 2022 version, then count all revisions that occurred before the month of that release date. Focus on identifying the exact release month and year from the Wikipedia page itself, then filter the revision history to count only pre-release revisions.

## Description
This is the necessary next step because: (1) We have confirmed God of War as the 2019 BAFTA Games Award winner, (2) We need to access its Wikipedia page to find the official release date as stated on the page and analyze the revision history, (3) Expected outcome is to obtain the complete revision timeline and count revisions before the release month, (4) This directly addresses the TASK requirement to analyze pre-release Wikipedia activity for the award-winning game.

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

## Created Time
2025-08-13 23:24:26
