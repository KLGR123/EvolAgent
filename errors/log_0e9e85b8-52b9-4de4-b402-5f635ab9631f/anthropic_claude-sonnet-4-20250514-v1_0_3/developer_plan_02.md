# Developer Plan 02

## Plan
Access the target webpage at http://web.archive.org/web/20230306063201/https://de.wikipedia.org/wiki/Thieme-Becker (the first citation reference from Carl Nebel's Wikipedia page) and systematically search for any images embedded on that page. Extract and analyze each image to identify chronological year dates written within them. Focus on finding the latest (most recent) chronological year among all dates visible in the images on this German Wikipedia page about the Thieme-Becker art encyclopedia.

## Description
This is the necessary next step because: (1) The developer successfully identified and accessed the first citation reference link from Carl Nebel's Wikipedia page, which leads to the German Wikipedia page about Thieme-Becker, (2) We have the target webpage content but need to specifically examine the images on this page to find chronological year dates, (3) Expected outcome is to locate all images on the Thieme-Becker page and identify the latest year date written within any of these images, (4) This directly addresses the TASK requirement to find the latest chronological year date in images on the webpage referenced by Carl Nebel's first citation.

## Episodic Examples
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

### Development Step 7: **Title:**  
Extract Wikipedia Access Date from Endnote on Page 11 of 'The Responsibility of Intellectuals' (2019)

**Description**: Access and download the full text of 'The Responsibility of Intellectuals' (DOI 10.2307/j.ctv9b2xdv) from JSTOR or UCL Press. Since this is a 2019 UCL Press publication available through JSTOR, retrieve the complete book content and save it to the workspace. Focus on locating page 11, identifying the second-to-last paragraph on that page, and extracting the specific endnote referenced in that paragraph. The endnote should contain a Wikipedia article citation with a November access date - extract the exact day of the month when the Wikipedia article was accessed.

**Use Cases**:
- Academic integrity auditing by university librarians to verify citation accuracy and access dates in open-access scholarly books
- Automated literature review tools for researchers needing to extract and cross-reference Wikipedia citations and their access dates across large PDF collections
- Digital humanities projects analyzing citation patterns and sources in contemporary intellectual history publications
- Legal compliance checks for publishers ensuring all Wikipedia references in academic works include proper access dates as per citation standards
- Bibliometric analysis for research impact studies, tracking the prevalence and recency of Wikipedia citations in academic monographs
- Content verification workflows for fact-checkers reviewing the reliability and timeliness of Wikipedia-sourced references in published books
- Automated metadata enrichment for digital repositories, extracting and structuring citation details (including access dates) from full-text PDFs
- Quality assurance processes in academic publishing, detecting missing or outdated access dates in Wikipedia citations before final release

```
import os
import json
import requests
from bs4 import BeautifulSoup
import time
import re

print('=== COMPREHENSIVE SEARCH FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES ===')
print('DOI: 10.2307/j.ctv9b2xdv')
print('Objective: Search entire book for Wikipedia citations with November access dates')
print('Status: Page 11 second-to-last paragraph had no endnote references')
print('\n' + '='*100 + '\n')

# First, let's check if we have the full book PDF downloaded
pdf_path = None
workspace_files = os.listdir('workspace')
for file in workspace_files:
    if file.endswith('.pdf') and 'responsibility' in file.lower():
        pdf_path = os.path.join('workspace', file)
        break

if not pdf_path:
    print('❌ Full book PDF not found in workspace')
    print('Available files:')
    for file in workspace_files:
        print(f'  - {file}')
    exit()

print(f'Found PDF: {pdf_path}')
file_size = os.path.getsize(pdf_path)
print(f'PDF size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')

print('\n=== EXTRACTING FULL BOOK TEXT FOR COMPREHENSIVE SEARCH ===')

try:
    from langchain_community.document_loaders import PyPDFLoader
    
    print('Loading complete PDF...')
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    
    print(f'✓ PDF loaded with {len(pages)} pages')
    
    # Combine all pages into full text
    full_book_text = '\n\n'.join([page.page_content for page in pages])
    print(f'Total book text: {len(full_book_text):,} characters')
    
    # Save full text for reference
    with open('workspace/full_book_text.txt', 'w', encoding='utf-8') as f:
        f.write('THE RESPONSIBILITY OF INTELLECTUALS - FULL BOOK TEXT\n')
        f.write('Source: UCL Press Open Access PDF\n')
        f.write('='*80 + '\n\n')
        f.write(full_book_text)
    
    print('✓ Full book text saved to workspace/full_book_text.txt')
    
    print('\n=== SEARCHING FOR ALL WIKIPEDIA REFERENCES ===')
    
    # First, let's find all Wikipedia references regardless of date
    wikipedia_general_patterns = [
        r'wikipedia[^\n]{0,300}',
        r'en\.wikipedia\.org[^\n]{0,300}',
        r'\bwikipedia\b[^\n]{0,300}'
    ]
    
    all_wikipedia_refs = []
    for pattern in wikipedia_general_patterns:
        matches = re.finditer(pattern, full_book_text, re.IGNORECASE)
        for match in matches:
            ref_text = match.group(0)
            all_wikipedia_refs.append({
                'text': ref_text,
                'position': match.start(),
                'pattern_used': pattern
            })
    
    # Remove duplicates based on position
    unique_wiki_refs = []
    seen_positions = set()
    for ref in all_wikipedia_refs:
        if ref['position'] not in seen_positions:
            seen_positions.add(ref['position'])
            unique_wiki_refs.append(ref)
    
    print(f'Found {len(unique_wiki_refs)} total Wikipedia references in the book')
    
    if unique_wiki_refs:
        print('\nFirst 10 Wikipedia references:')
        for i, ref in enumerate(unique_wiki_refs[:10], 1):
            print(f'{i}. Position {ref["position"]:,}: {ref["text"][:100]}...')
    
    print('\n=== SEARCHING FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES ===')
    
    # Comprehensive patterns for Wikipedia citations with November dates
    november_wikipedia_patterns = [
        # Wikipedia followed by November and day
        r'wikipedia[^\n]{0,400}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        r'en\.wikipedia\.org[^\n]{0,400}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        
        # November and day followed by Wikipedia
        r'november[^\n]{0,100}\d{1,2}[^\n]{0,200}wikipedia[^\n]{0,300}',
        r'\d{1,2}[^\n]{0,50}november[^\n]{0,200}wikipedia[^\n]{0,300}',
        
        # Accessed patterns
        r'accessed[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,200}wikipedia[^\n]{0,200}',
        r'wikipedia[^\n]{0,400}accessed[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        
        # More flexible patterns
        r'\bwikipedia\b[^\n]{0,500}\bnovember\b[^\n]{0,150}\b\d{1,2}\b[^\n]{0,150}',
        r'\bnovember\b[^\n]{0,150}\b\d{1,2}\b[^\n]{0,300}\bwikipedia\b[^\n]{0,300}',
        
        # URL patterns with dates
        r'https?://[^\s]*wikipedia[^\s]*[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        r'november[^\n]{0,100}\d{1,2}[^\n]{0,200}https?://[^\s]*wikipedia[^\s]*[^\n]{0,100}'
    ]
    
    november_citations = []
    for pattern in november_wikipedia_patterns:
        matches = re.finditer(pattern, full_book_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            citation_text = match.group(0)
            
            # Extract the day from November date using multiple patterns
            day_patterns = [
                r'november\s+(\d{1,2})',
                r'(\d{1,2})\s+november',
                r'november\s+(\d{1,2})(?:st|nd|rd|th)?',
                r'(\d{1,2})(?:st|nd|rd|th)?\s+november',
                r'november\s*,?\s*(\d{1,2})',
                r'(\d{1,2})\s*,?\s*november',
                r'november\s+(\d{1,2})\s*,?\s*\d{4}',
                r'(\d{1,2})\s+november\s+\d{4}'
            ]
            
            day_found = None
            for day_pattern in day_patterns:
                day_match = re.search(day_pattern, citation_text, re.IGNORECASE)
                if day_match:
                    day_found = day_match.group(1)
                    break
            
            if day_found and 1 <= int(day_found) <= 31:  # Valid day
                # Get broader context around the citation
                context_start = max(0, match.start() - 1000)
                context_end = min(len(full_book_text), match.end() + 1000)
                citation_context = full_book_text[context_start:context_end]
                
                # Determine which page this citation appears on
                char_count = 0
                page_number = 0
                for page_idx, page in enumerate(pages):
                    if char_count + len(page.page_content) >= match.start():
                        page_number = page_idx + 1
                        break
                    char_count += len(page.page_content) + 2  # +2 for \n\n separator
                
                november_citations.append({
                    'citation': citation_text,
                    'november_day': day_found,
                    'position': match.start(),
                    'context': citation_context,
                    'page_number': page_number,
                    'pattern_used': pattern
                })
    
    # Remove duplicates based on citation text and day
    unique_november_citations = []
    seen_citations = set()
    for citation in november_citations:
        citation_key = (citation['citation'].strip().lower(), citation['november_day'])
        if citation_key not in seen_citations:
            seen_citations.add(citation_key)
            unique_november_citations.append(citation)
    
    if unique_november_citations:
        print(f'\n🎯 FOUND {len(unique_november_citations)} UNIQUE WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES:')
        
        for i, citation in enumerate(unique_november_citations, 1):
            print(f'\nCitation {i}:')
            print(f'November day: {citation["november_day"]}')
            print(f'Page number: {citation["page_number"]}')
            print(f'Position in book: {citation["position"]:,}')
            print(f'Pattern used: {citation["pattern_used"]}')
            print('Citation text:')
            print('='*80)
            print(citation['citation'])
            print('='*80)
            
            # Show relevant context
            context_preview = citation['context'][:500] + '...' if len(citation['context']) > 500 else citation['context']
            print(f'Context: {context_preview}')
            print('-'*80)
        
        # Save the complete analysis
        final_analysis = {
            'source_pdf': pdf_path,
            'book_title': 'The Responsibility of Intellectuals',
            'publisher': 'UCL Press',
            'year': 2019,
            'total_pages': len(pages),
            'total_wikipedia_references': len(unique_wiki_refs),
            'wikipedia_citations_with_november_dates': unique_november_citations,
            'search_patterns_used': november_wikipedia_patterns,
            'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('workspace/comprehensive_wikipedia_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(final_analysis, f, indent=2, ensure_ascii=False)
        
        print('\n✓ Complete analysis saved to workspace/comprehensive_wikipedia_analysis.json')
        
        # Determine the final answer
        if len(unique_november_citations) == 1:
            answer_day = unique_november_citations[0]['november_day']
            page_num = unique_november_citations[0]['page_number']
            print(f'\n*** FINAL ANSWER: The Wikipedia article was accessed on November {answer_day} ***')
            print(f'(Found on page {page_num} of the book)')
        elif len(unique_november_citations) > 1:
            print(f'\n*** MULTIPLE WIKIPEDIA CITATIONS WITH NOVEMBER DATES FOUND ***')
            print('All November access dates found:')
            for i, citation in enumerate(unique_november_citations, 1):
                print(f'{i}. November {citation["november_day"]} (page {citation["page_number"]})')
            
            # Look for the one closest to page 11 or in endnotes section
            closest_to_page_11 = None
            min_distance = float('inf')
            
            for citation in unique_november_citations:
                distance = abs(citation['page_number'] - 11)
                if distance < min_distance:
                    min_distance = distance
                    closest_to_page_11 = citation
            
            if closest_to_page_11:
                answer_day = closest_to_page_11['november_day']
                page_num = closest_to_page_11['page_number']
                print(f'\n*** MOST LIKELY ANSWER (closest to page 11): November {answer_day} ***')
                print(f'(Found on page {page_num}, distance from page 11: {min_distance} pages)')
            else:
                # Default to first citation
                answer_day = unique_november_citations[0]['november_day']
                print(f'\nDefaulting to first citation: November {answer_day}')
    
    else:
        print('\n⚠ No Wikipedia citations with November access dates found')
        
        # Let's search for any date patterns with Wikipedia
        print('\nSearching for Wikipedia citations with any date patterns...')
        
        date_patterns = [
            r'wikipedia[^\n]{0,300}\d{1,2}[^\n]{0,100}\d{4}[^\n]{0,100}',  # Any date
            r'wikipedia[^\n]{0,300}accessed[^\n]{0,200}\d{4}[^\n]{0,100}',  # Accessed with year
            r'accessed[^\n]{0,200}wikipedia[^\n]{0,300}\d{4}[^\n]{0,100}',  # Accessed before wikipedia
        ]
        
        any_date_citations = []
        for pattern in date_patterns:
            matches = re.finditer(pattern, full_book_text, re.IGNORECASE)
            for match in matches:
                citation_text = match.group(0)
                any_date_citations.append(citation_text)
        
        if any_date_citations:
            print(f'Found {len(any_date_citations)} Wikipedia citations with any date patterns:')
            for i, citation in enumerate(any_date_citations[:5], 1):
                print(f'{i}. {citation[:150]}...')
        else:
            print('No Wikipedia citations with any date patterns found')
        
        # Final fallback: search for month names with Wikipedia
        print('\nSearching for Wikipedia citations with any month names...')
        
        month_patterns = [
            r'wikipedia[^\n]{0,300}(?:january|february|march|april|may|june|july|august|september|october|november|december)[^\n]{0,100}\d{1,2}[^\n]{0,100}',
            r'(?:january|february|march|april|may|june|july|august|september|october|november|december)[^\n]{0,100}\d{1,2}[^\n]{0,200}wikipedia[^\n]{0,300}'
        ]
        
        month_citations = []
        for pattern in month_patterns:
            matches = re.finditer(pattern, full_book_text, re.IGNORECASE)
            for match in matches:
                citation_text = match.group(0)
                month_citations.append(citation_text)
        
        if month_citations:
            print(f'Found {len(month_citations)} Wikipedia citations with month names:')
            for i, citation in enumerate(month_citations[:5], 1):
                print(f'{i}. {citation[:150]}...')
        else:
            print('No Wikipedia citations with month names found')

except ImportError:
    print('❌ PyPDFLoader not available - cannot extract text from PDF')
except Exception as e:
    print(f'❌ Error during comprehensive search: {str(e)}')

print('\n' + '='*100)
print('COMPREHENSIVE WIKIPEDIA SEARCH COMPLETE')
print('='*100)
print('Objective: Find Wikipedia citation with November access date from entire book')
print('Status: Searched all pages since page 11 paragraph had no endnote references')
print('\nFiles created:')
if os.path.exists('workspace'):
    for file in sorted(os.listdir('workspace')):
        if file.endswith(('.txt', '.json')):
            file_path = os.path.join('workspace', file)
            file_size = os.path.getsize(file_path)
            print(f'- {file} ({file_size:,} bytes)')
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

### Development Step 3: **Title:**  
Extract Wikipedia Access Date from Endnote on Page 11 of 'The Responsibility of Intellectuals' (2019)

**Description**: Access and download the full text of 'The Responsibility of Intellectuals' (DOI 10.2307/j.ctv9b2xdv) from JSTOR or UCL Press. Since this is a 2019 UCL Press publication available through JSTOR, retrieve the complete book content and save it to the workspace. Focus on locating page 11, identifying the second-to-last paragraph on that page, and extracting the specific endnote referenced in that paragraph. The endnote should contain a Wikipedia article citation with a November access date - extract the exact day of the month when the Wikipedia article was accessed.

**Use Cases**:
- Academic integrity verification by university librarians checking the accuracy and access dates of Wikipedia citations in scholarly books
- Automated extraction of citation metadata for digital humanities researchers compiling bibliometric datasets from open-access monographs
- Legal teams auditing referenced online materials in published works to confirm compliance with copyright and citation standards
- Publishers conducting quality control to ensure endnotes in digital books properly reference and date online sources
- Research assistants preparing annotated bibliographies by programmatically identifying and extracting Wikipedia access dates from book endnotes
- Journalists fact-checking claims in recent academic books by tracing the exact Wikipedia versions cited at specific dates
- Digital archivists preserving citation trails by extracting and archiving referenced web pages as they appeared on the cited access date
- Educational technology developers building tools that highlight and verify online references in course materials for instructors

```
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

print('=== ACCESSING FULL TEXT OF "THE RESPONSIBILITY OF INTELLECTUALS" ===')
print('DOI: 10.2307/j.ctv9b2xdv')
print('Objective: Locate page 11, find second-to-last paragraph, extract endnote with Wikipedia citation (November access date)')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# First, let's examine the existing workspace files to understand what we have
print('=== INSPECTING EXISTING WORKSPACE FILES ===')
workspace_files = os.listdir('workspace')
if workspace_files:
    print(f'Found {len(workspace_files)} files in workspace:')
    for file in workspace_files:
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')
else:
    print('No existing files in workspace')

# Check if we have the final bibliographic record
final_record_path = 'workspace/final_bibliographic_record.json'
if os.path.exists(final_record_path):
    print('\n=== INSPECTING FINAL BIBLIOGRAPHIC RECORD ===')
    with open(final_record_path, 'r', encoding='utf-8') as f:
        biblio_data = json.load(f)
    
    print('Available keys in bibliographic record:')
    for key in biblio_data.keys():
        print(f'- {key}: {type(biblio_data[key])}')
    
    print(f'\nKey information:')
    print(f'Title: {biblio_data.get("title", "Unknown")}')
    print(f'Publisher: {biblio_data.get("publisher", "Unknown")}')
    print(f'Year: {biblio_data.get("publication_year", "Unknown")}')
    print(f'DOI URL: {biblio_data.get("doi_url", "Unknown")}')
    print(f'JSTOR URL: {biblio_data.get("jstor_url", "Unknown")}')
    
    # Check chapters/sections structure
    if 'chapters_sections' in biblio_data and biblio_data['chapters_sections']:
        print(f'\nBook structure: {len(biblio_data["chapters_sections"])} chapters/sections')
        for i, chapter in enumerate(biblio_data['chapters_sections'][:3], 1):
            print(f'{i}. {chapter.get("title", "No title")}')
            print(f'   URL: {chapter.get("url", "No URL")}')
else:
    print('Final bibliographic record not found')

# Now let's try to access the full text through JSTOR
print('\n=== ATTEMPTING TO ACCESS FULL TEXT VIA JSTOR ===')

# Set up headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Try to access the main JSTOR book page
jstor_main_url = 'https://www.jstor.org/stable/j.ctv9b2xdv'
print(f'Accessing main JSTOR page: {jstor_main_url}')

try:
    response = requests.get(jstor_main_url, headers=headers, timeout=30)
    print(f'JSTOR main page status: {response.status_code}')
    print(f'Final URL: {response.url}')
    print(f'Content length: {len(response.content):,} bytes')
    
    if response.status_code == 200:
        # Save the main page for analysis
        with open('workspace/jstor_main_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print('✓ JSTOR main page saved to workspace/jstor_main_page.html')
        
        # Parse the page to look for full-text access options
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text().lower()
        
        # Look for "read online", "full text", "PDF", or similar access options
        access_indicators = [
            'read online', 'full text', 'download pdf', 'view pdf',
            'open access', 'free access', 'read book', 'view book'
        ]
        
        found_access_options = []
        for indicator in access_indicators:
            if indicator in page_text:
                found_access_options.append(indicator)
        
        if found_access_options:
            print(f'\n✓ Found access indicators: {found_access_options}')
        else:
            print('\n⚠ No obvious access indicators found in page text')
        
        # Look for links that might provide full-text access
        access_links = []
        
        # Search for various types of access links
        link_selectors = [
            'a[href*="pdf"]',
            'a[href*="read"]',
            'a[href*="view"]',
            'a[href*="download"]',
            'a[href*="full"]',
            'a[href*="text"]',
            '.pdf-link a',
            '.read-link a',
            '.download-link a',
            '.access-link a'
        ]
        
        for selector in link_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute
                        if href.startswith('/'):
                            href = urljoin(jstor_main_url, href)
                        
                        link_text = link.get_text().strip()
                        if len(link_text) > 0 and len(link_text) < 100:  # Reasonable link text length
                            access_links.append({
                                'url': href,
                                'text': link_text,
                                'selector': selector
                            })
            except Exception as e:
                print(f'Error with selector {selector}: {str(e)}')
        
        # Remove duplicates
        unique_links = []
        seen_urls = set()
        for link in access_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_links.append(link)
        
        print(f'\nFound {len(unique_links)} potential access links:')
        for i, link in enumerate(unique_links[:10], 1):  # Show first 10
            print(f'{i}. "{link["text"]}" -> {link["url"]}')
            print(f'   (Found via: {link["selector"]})')
        
        # Look specifically for chapter/section links that might contain page 11
        chapter_links = []
        for link in unique_links:
            link_url = link['url'].lower()
            link_text = link['text'].lower()
            
            # Check if this might be a chapter or section link
            if any(indicator in link_url or indicator in link_text for indicator in 
                   ['chapter', 'section', 'pdf', 'ctv9b2xdv']):
                chapter_links.append(link)
        
        if chapter_links:
            print(f'\n*** FOUND {len(chapter_links)} POTENTIAL CHAPTER/SECTION LINKS ***')
            for i, link in enumerate(chapter_links[:5], 1):
                print(f'{i}. "{link["text"]}" -> {link["url"]}')
        
        # Try to access the first promising link
        if chapter_links:
            print('\n=== ATTEMPTING TO ACCESS FIRST CHAPTER/SECTION LINK ===')
            first_link = chapter_links[0]
            print(f'Trying: {first_link["text"]} -> {first_link["url"]}')
            
            try:
                chapter_response = requests.get(first_link['url'], headers=headers, timeout=30)
                print(f'Chapter access status: {chapter_response.status_code}')
                print(f'Content type: {chapter_response.headers.get("content-type", "unknown")}')
                print(f'Content length: {len(chapter_response.content):,} bytes')
                
                if chapter_response.status_code == 200:
                    content_type = chapter_response.headers.get('content-type', '').lower()
                    
                    if 'pdf' in content_type:
                        print('\n*** PDF CONTENT DETECTED ***')
                        pdf_path = 'workspace/responsibility_intellectuals_chapter.pdf'
                        
                        with open(pdf_path, 'wb') as pdf_file:
                            pdf_file.write(chapter_response.content)
                        
                        file_size = os.path.getsize(pdf_path)
                        print(f'✓ PDF saved to: {pdf_path}')
                        print(f'File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
                        
                        # Try to extract text from PDF if possible
                        try:
                            print('\nAttempting to extract text from PDF...')
                            from langchain_community.document_loaders import PyPDFLoader
                            
                            loader = PyPDFLoader(pdf_path)
                            pages = loader.load_and_split()
                            
                            print(f'✓ PDF loaded successfully with {len(pages)} pages')
                            
                            # Look for page 11 specifically
                            if len(pages) >= 11:
                                page_11_content = pages[10].page_content  # Page 11 is index 10
                                print(f'\n=== PAGE 11 CONTENT FOUND ===') 
                                print(f'Page 11 length: {len(page_11_content):,} characters')
                                print(f'\nFirst 500 characters of page 11:')
                                print('='*80)
                                print(page_11_content[:500] + '...')
                                print('='*80)
                                
                                # Save page 11 content
                                with open('workspace/page_11_content.txt', 'w', encoding='utf-8') as f:
                                    f.write(page_11_content)
                                print('\n✓ Page 11 content saved to workspace/page_11_content.txt')
                                
                                # Look for the second-to-last paragraph
                                paragraphs = [p.strip() for p in page_11_content.split('\n\n') if p.strip()]
                                print(f'\nFound {len(paragraphs)} paragraphs on page 11')
                                
                                if len(paragraphs) >= 2:
                                    second_to_last_para = paragraphs[-2]
                                    print(f'\n=== SECOND-TO-LAST PARAGRAPH ON PAGE 11 ===')
                                    print('='*80)
                                    print(second_to_last_para)
                                    print('='*80)
                                    
                                    # Look for endnote references in this paragraph
                                    endnote_patterns = [
                                        r'\b(\d+)\b',  # Simple numbers
                                        r'\[(\d+)\]',  # Numbers in brackets
                                        r'\((\d+)\)',  # Numbers in parentheses
                                        r'\b(\d+)\.',  # Numbers with periods
                                        r'see note (\d+)',  # "see note X" format
                                        r'note (\d+)',  # "note X" format
                                    ]
                                    
                                    found_endnotes = []
                                    for pattern in endnote_patterns:
                                        matches = re.findall(pattern, second_to_last_para, re.IGNORECASE)
                                        if matches:
                                            for match in matches:
                                                if match.isdigit() and int(match) <= 100:  # Reasonable endnote number
                                                    found_endnotes.append(int(match))
                                    
                                    # Remove duplicates and sort
                                    found_endnotes = sorted(list(set(found_endnotes)))
                                    
                                    if found_endnotes:
                                        print(f'\n*** FOUND ENDNOTE REFERENCES: {found_endnotes} ***')
                                        
                                        # Now we need to find the actual endnotes
                                        print('\n=== SEARCHING FOR ENDNOTES SECTION ===')
                                        
                                        # Combine all pages to search for endnotes
                                        full_text = '\n\n'.join([page.page_content for page in pages])
                                        
                                        # Look for endnotes section
                                        endnotes_indicators = [
                                            'notes', 'endnotes', 'references', 'footnotes',
                                            'bibliography', 'works cited'
                                        ]
                                        
                                        endnotes_section_found = False
                                        for indicator in endnotes_indicators:
                                            pattern = rf'\b{indicator}\b'
                                            matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
                                            if matches:
                                                print(f'Found "{indicator}" section at {len(matches)} locations')
                                                endnotes_section_found = True
                                        
                                        # Search for specific endnote numbers with Wikipedia citations
                                        print('\n=== SEARCHING FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATE ===')
                                        
                                        # Look for Wikipedia citations with November access dates
                                        wikipedia_patterns = [
                                            r'wikipedia[^\n]*november[^\n]*accessed[^\n]*',
                                            r'en\.wikipedia\.org[^\n]*november[^\n]*',
                                            r'accessed[^\n]*november[^\n]*wikipedia[^\n]*',
                                            r'november[^\n]*\d{1,2}[^\n]*wikipedia[^\n]*',
                                            r'wikipedia[^\n]*accessed[^\n]*november[^\n]*\d{1,2}[^\n]*'
                                        ]
                                        
                                        wikipedia_citations = []
                                        for pattern in wikipedia_patterns:
                                            matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                                            for match in matches:
                                                citation_text = match.group(0)
                                                # Extract the day from November date
                                                day_match = re.search(r'november\s+(\d{1,2})', citation_text, re.IGNORECASE)
                                                if day_match:
                                                    day = day_match.group(1)
                                                    wikipedia_citations.append({
                                                        'citation': citation_text,
                                                        'november_day': day,
                                                        'position': match.start()
                                                    })
                                        
                                        if wikipedia_citations:
                                            print(f'\n🎯 FOUND {len(wikipedia_citations)} WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES:')
                                            
                                            for i, citation in enumerate(wikipedia_citations, 1):
                                                print(f'\nCitation {i}:')
                                                print(f'November day: {citation["november_day"]}')
                                                print(f'Position in text: {citation["position"]}')
                                                print('Citation text:')
                                                print('='*60)
                                                print(citation['citation'])
                                                print('='*60)
                                            
                                            # Save the Wikipedia citations
                                            citations_data = {
                                                'source_file': pdf_path,
                                                'page_11_paragraph_count': len(paragraphs),
                                                'second_to_last_paragraph': second_to_last_para,
                                                'endnote_references_found': found_endnotes,
                                                'wikipedia_citations': wikipedia_citations,
                                                'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                                            }
                                            
                                            with open('workspace/wikipedia_citations_analysis.json', 'w', encoding='utf-8') as f:
                                                json.dump(citations_data, f, indent=2, ensure_ascii=False)
                                            
                                            print('\n✓ Wikipedia citations analysis saved to workspace/wikipedia_citations_analysis.json')
                                            
                                            # Extract the specific day for the answer
                                            if len(wikipedia_citations) == 1:
                                                answer_day = wikipedia_citations[0]['november_day']
                                                print(f'\n*** ANSWER FOUND: The Wikipedia article was accessed on November {answer_day} ***')
                                            elif len(wikipedia_citations) > 1:
                                                print(f'\n*** MULTIPLE WIKIPEDIA CITATIONS FOUND - Need to determine which is from page 11 endnote ***')
                                                for i, citation in enumerate(wikipedia_citations, 1):
                                                    print(f'Option {i}: November {citation["november_day"]}')
                                        else:
                                            print('\n⚠ No Wikipedia citations with November access dates found')
                                            print('Searching for any Wikipedia references...')
                                            
                                            # Broader search for Wikipedia
                                            wiki_matches = re.finditer(r'wikipedia[^\n]{0,200}', full_text, re.IGNORECASE)
                                            wiki_refs = [match.group(0) for match in wiki_matches]
                                            
                                            if wiki_refs:
                                                print(f'Found {len(wiki_refs)} general Wikipedia references:')
                                                for i, ref in enumerate(wiki_refs[:5], 1):
                                                    print(f'{i}. {ref[:100]}...')
                                    else:
                                        print('\n⚠ No endnote references found in second-to-last paragraph')
                                        print('Showing paragraph content for manual inspection:')
                                        print(second_to_last_para)
                                else:
                                    print(f'\n⚠ Page 11 has fewer than 2 paragraphs ({len(paragraphs)} found)')
                                    if paragraphs:
                                        print('Available paragraphs:')
                                        for i, para in enumerate(paragraphs, 1):
                                            print(f'{i}. {para[:100]}...')
                            else:
                                print(f'\n⚠ PDF has only {len(pages)} pages, page 11 not available')
                                print('Available pages:')
                                for i, page in enumerate(pages[:5], 1):
                                    preview = page.page_content[:100].replace('\n', ' ')
                                    print(f'Page {i}: {preview}...')
                        
                        except ImportError:
                            print('⚠ PyPDFLoader not available - PDF saved but text extraction skipped')
                        except Exception as pdf_error:
                            print(f'❌ PDF text extraction error: {str(pdf_error)}')
                    
                    elif 'html' in content_type:
                        print('\n*** HTML CONTENT DETECTED ***')
                        
                        # Save HTML content
                        with open('workspace/chapter_content.html', 'w', encoding='utf-8') as f:
                            f.write(chapter_response.text)
                        print('✓ HTML content saved to workspace/chapter_content.html')
                        
                        # Parse HTML for text content
                        chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')
                        
                        # Remove navigation and non-content elements
                        for element in chapter_soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                            element.decompose()
                        
                        chapter_text = chapter_soup.get_text()
                        print(f'\nExtracted HTML text length: {len(chapter_text):,} characters')
                        print(f'First 300 characters: {chapter_text[:300]}...')
                        
                        # Save extracted text
                        with open('workspace/chapter_text_content.txt', 'w', encoding='utf-8') as f:
                            f.write(chapter_text)
                        print('✓ Chapter text content saved to workspace/chapter_text_content.txt')
                    
                    else:
                        print(f'\n*** UNKNOWN CONTENT TYPE: {content_type} ***')
                        print('Saving raw content for analysis')
                        
                        with open('workspace/unknown_content.txt', 'w', encoding='utf-8') as f:
                            f.write(chapter_response.text)
                        print('✓ Raw content saved to workspace/unknown_content.txt')
                
                else:
                    print(f'❌ Chapter access failed with status: {chapter_response.status_code}')
            
            except Exception as chapter_error:
                print(f'❌ Error accessing chapter: {str(chapter_error)}')
        
        else:
            print('\n⚠ No chapter/section links found to try')
    
    else:
        print(f'❌ JSTOR main page access failed with status: {response.status_code}')

except Exception as e:
    print(f'❌ Error accessing JSTOR: {str(e)}')

print('\n' + '='*100)
print('FULL TEXT ACCESS ATTEMPT SUMMARY')
print('='*100)
print('Objective: Access full text to find page 11, second-to-last paragraph, and Wikipedia endnote with November access date')
print('\nFiles created in workspace:')
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')

print('\n*** NEXT STEP: Analyze extracted content for the specific Wikipedia citation ***')
```

## Created Time
2025-08-11 06:45:05
