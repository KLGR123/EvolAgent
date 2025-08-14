# Developer Plan 01

## Plan
Search for and access the archived Wikipedia pages for each day of August (August 1st through August 31st) as they appeared in June 2023. Use the Wayback Machine or Wikipedia's revision history to retrieve the specific versions from late June 2023. For each daily August page, extract all references and citations, then count how many of these references are Twitter/X posts (looking for URLs containing twitter.com, x.com, or t.co domains). Create a comprehensive analysis showing the count of Twitter/X citations for each August day's Wikipedia page.

## Description
This is the optimal starting approach because: (1) We need to systematically access 31 different Wikipedia pages (August 1-31) from their June 2023 archived versions, (2) No previous research has been conducted on this specific citation analysis, (3) Expected outcome is to obtain the archived content for all August daily pages and begin extracting Twitter/X reference counts, (4) This establishes the foundation for comprehensive citation analysis across all August days to answer the TASK's requirement for Twitter/X post citation frequency on each day's Wikipedia page

## Episodic Examples
### Development Step 10: Filter Wikipedia revision history to count page edits through June 30, 2023

**Description**: Filter the extracted revision data from the comprehensive Wikipedia history to count only the edits made from the page's inception until the end of June 2023. Exclude any revisions that occurred after June 30, 2023, and provide the exact count of edits within the specified timeframe.

**Use Cases**:
- Digital humanities research on cultural heritage: counting edits to historical monument Wikipedia pages through June 2023 to gauge community-driven documentation growth
- Political journalism analytics: measuring the volume of revisions on election-related articles up to June 2023 to identify periods of peak editorial activity
- Corporate brand compliance audit: auditing all edits on a company’s Wikipedia page until mid-2023 to verify no unauthorized content changes occurred
- Machine learning dataset preparation: filtering Wikipedia revision histories before July 2023 to build a time-bounded corpus for change-detection model training
- Educational content stability assessment: evaluating the number of edits on science and math topic pages until June 2023 to select stable resources for textbook references
- NGO transparency reporting: quantifying community edits on environmental policy articles through June 2023 to demonstrate stakeholder engagement over time
- SEO and digital marketing performance review: tracking cumulative edits on product and service Wikipedia pages before July 2023 to inform content strategy adjustments
- Fact-checking and misinformation studies: analyzing revision counts on high-profile news event pages up to June 2023 to correlate editorial activity with misinformation spikes

```
import os
import json
from datetime import datetime

print("=== INSPECTING EXISTING REVISION DATA FILES ===\n")

# Check all workspace directories for revision data
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
print(f"Found workspace directories: {workspace_dirs}\n")

revision_files = []
for workspace_dir in workspace_dirs:
    files = os.listdir(workspace_dir)
    for file in files:
        if 'revision' in file.lower() or 'wikipedia' in file.lower():
            file_path = os.path.join(workspace_dir, file)
            file_size = os.path.getsize(file_path)
            revision_files.append({
                'path': file_path,
                'name': file,
                'size': file_size,
                'workspace': workspace_dir
            })
            print(f"Found revision file: {file} ({file_size:,} bytes) in {workspace_dir}")

if not revision_files:
    print("❌ No revision data files found in any workspace")
else:
    # Use the largest/most comprehensive file
    largest_file = max(revision_files, key=lambda x: x['size'])
    print(f"\nUsing largest revision file: {largest_file['name']} ({largest_file['size']:,} bytes)")
    
    # First, inspect the file structure before loading
    print(f"\n=== INSPECTING FILE STRUCTURE: {largest_file['name']} ===\n")
    
    try:
        with open(largest_file['path'], 'r', encoding='utf-8') as f:
            # Read just the beginning to understand structure
            content_preview = f.read(1000)
            print(f"File preview (first 1000 chars):\n{content_preview}\n")
            
            # Reset and load as JSON to inspect structure
            f.seek(0)
            data = json.load(f)
            
        print("JSON structure analysis:")
        if isinstance(data, dict):
            print(f"  Root type: Dictionary with {len(data)} keys")
            for key, value in data.items():
                if isinstance(value, list):
                    print(f"    {key}: List with {len(value)} items")
                    if len(value) > 0:
                        print(f"      Sample item type: {type(value[0]).__name__}")
                        if isinstance(value[0], dict):
                            sample_keys = list(value[0].keys())
                            print(f"      Sample item keys: {sample_keys}")
                elif isinstance(value, dict):
                    print(f"    {key}: Dictionary with {len(value)} keys")
                    nested_keys = list(value.keys())
                    print(f"      Keys: {nested_keys}")
                else:
                    print(f"    {key}: {type(value).__name__} = {str(value)[:100]}")
        
        print(f"\n=== FILTERING REVISIONS TO COUNT EDITS UNTIL JUNE 30, 2023 ===\n")
        
        # Now that I understand the structure, extract revisions safely
        revisions = []
        metadata = {}
        
        # Check different possible structures
        if 'revisions' in data:
            revisions = data['revisions']
            print(f"Found 'revisions' key with {len(revisions)} items")
        elif 'filtered_revisions' in data:
            revisions = data['filtered_revisions']
            print(f"Found 'filtered_revisions' key with {len(revisions)} items")
        elif isinstance(data, list):
            revisions = data
            print(f"Data is a list with {len(revisions)} items")
        else:
            print("❌ Could not identify revisions data structure")
            print(f"Available keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}")
        
        # Extract metadata if available
        for key in ['extraction_metadata', 'filtering_metadata', 'metadata']:
            if key in data:
                metadata = data[key]
                print(f"Found metadata under '{key}' key")
                break
        
        if not revisions:
            print("❌ No revision data found to process")
        else:
            print(f"\nProcessing {len(revisions)} revisions...")
            
            # Show sample revision structure
            if len(revisions) > 0:
                sample_rev = revisions[0]
                print(f"\nSample revision structure:")
                for key, value in sample_rev.items():
                    print(f"  {key}: {type(value).__name__} = {str(value)[:100]}")
            
            # Filter revisions until June 30, 2023
            cutoff_date = datetime(2023, 6, 30, 23, 59, 59)
            print(f"\nApplying cutoff date: {cutoff_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            filtered_count = 0
            excluded_count = 0
            earliest_timestamp = None
            latest_timestamp = None
            
            for revision in revisions:
                if 'timestamp' in revision:
                    try:
                        # Parse Wikipedia timestamp format
                        timestamp_str = revision['timestamp']
                        rev_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        rev_timestamp = rev_timestamp.replace(tzinfo=None)
                        
                        # Track date range
                        if earliest_timestamp is None or timestamp_str < earliest_timestamp:
                            earliest_timestamp = timestamp_str
                        if latest_timestamp is None or timestamp_str > latest_timestamp:
                            latest_timestamp = timestamp_str
                        
                        # Count based on cutoff date
                        if rev_timestamp <= cutoff_date:
                            filtered_count += 1
                        else:
                            excluded_count += 1
                            
                    except Exception as e:
                        print(f"  ⚠️ Error parsing timestamp {revision.get('timestamp', 'N/A')}: {str(e)}")
                        continue
                else:
                    print(f"  ⚠️ Revision missing timestamp: {revision}")
            
            print(f"\n=== FILTERING RESULTS ===\n")
            print(f"Total revisions processed: {len(revisions)}")
            print(f"Edits until end of June 2023: {filtered_count}")
            print(f"Edits excluded (after June 30, 2023): {excluded_count}")
            
            if earliest_timestamp and latest_timestamp:
                print(f"\nRevision date range in data:")
                print(f"  Earliest: {earliest_timestamp}")
                print(f"  Latest: {latest_timestamp}")
            
            # Show metadata if available
            if metadata:
                print(f"\nSource metadata:")
                for key, value in metadata.items():
                    print(f"  {key}: {value}")
            
            # Save the final count result
            result = {
                'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_file': largest_file['name'],
                'cutoff_date': '2023-06-30 23:59:59',
                'total_revisions_in_source': len(revisions),
                'edits_until_june_2023': filtered_count,
                'edits_excluded_after_june_2023': excluded_count,
                'revision_date_range': {
                    'earliest': earliest_timestamp,
                    'latest': latest_timestamp
                },
                'source_metadata': metadata
            }
            
            result_file = os.path.join(largest_file['workspace'], 'final_edit_count_june_2023.json')
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Final results saved to: {os.path.basename(result_file)}")
            
            # Create summary text file
            summary_file = os.path.join(largest_file['workspace'], 'edit_count_summary_final.txt')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"WIKIPEDIA EDIT COUNT - FINAL RESULTS\n")
                f.write(f"={'='*45}\n\n")
                f.write(f"Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Source data file: {largest_file['name']}\n")
                f.write(f"Cutoff date: June 30, 2023 23:59:59\n\n")
                f.write(f"FINAL ANSWER:\n")
                f.write(f"🎯 {filtered_count} edits were made from the page's inception until the end of June 2023\n\n")
                f.write(f"BREAKDOWN:\n")
                f.write(f"- Total revisions in source data: {len(revisions)}\n")
                f.write(f"- Edits until end of June 2023: {filtered_count}\n")
                f.write(f"- Edits excluded (after June 30, 2023): {excluded_count}\n\n")
                if earliest_timestamp and latest_timestamp:
                    f.write(f"SOURCE DATA DATE RANGE:\n")
                    f.write(f"- Earliest revision: {earliest_timestamp}\n")
                    f.write(f"- Latest revision: {latest_timestamp}\n")
            
            print(f"✅ Summary saved to: {os.path.basename(summary_file)}")
            
            print(f"\n🎯 FINAL ANSWER: {filtered_count} edits were made from the page's inception until the end of June 2023")
            
    except Exception as e:
        print(f"❌ Error processing revision file: {str(e)}")
        import traceback
        traceback.print_exc()
```

### Development Step 8: Count Wikipedia page edits from inception through June 30, 2023

**Description**: Filter the extracted revision data from the comprehensive Wikipedia history to count only the edits made from the page's inception until the end of June 2023. Exclude any revisions that occurred after June 30, 2023, and provide the exact count of edits within the specified timeframe.

**Use Cases**:
- Historical research in digital humanities: quantifying edit frequency of the “World War II” Wikipedia article from creation until June 30, 2023 to study shifts in collective memory
- Crisis communication analysis: counting revisions on the “COVID-19 pandemic” page up to June 2023 to correlate spikes in edits with major outbreak events
- Journalism data visualization: compiling the number of edits on the “United States presidential election” article before July 2023 to illustrate media attention cycles
- Machine learning dataset preparation: selecting only revisions made to the “Climate change” page until mid-2023 to train time-aware text generation models
- Corporate competitive intelligence: tracking edit counts on rival product pages (e.g., “iPhone”) up to June 2023 to gauge public information update frequency
- NGO impact assessment: measuring contribution activity on environmental initiative articles until June 2023 to identify key volunteer editors
- Legal e-discovery and audit: auditing revision counts for contentious biography pages to establish timelines of content changes before July 2023

```
import os
import json
from datetime import datetime

print("=== INSPECTING WORKSPACE FOR REVISION DATA ===\n")

# Check what workspace directories exist
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
print(f"Found workspace directories: {workspace_dirs}\n")

if not workspace_dirs:
    print("❌ No workspace directories found")
else:
    # Check each workspace for relevant files
    for workspace_dir in workspace_dirs:
        print(f"=== CONTENTS OF {workspace_dir} ===\n")
        
        files = os.listdir(workspace_dir)
        print(f"Files in {workspace_dir}: {len(files)} total")
        
        for file in files:
            file_path = os.path.join(workspace_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"  - {file} ({file_size:,} bytes)")
        
        print()
        
        # Look for files that might contain revision/history data
        revision_files = [f for f in files if any(keyword in f.lower() for keyword in 
                         ['revision', 'history', 'edit', 'wikipedia', 'data'])]
        
        if revision_files:
            print(f"Potential revision data files: {revision_files}\n")
            
            # Inspect the structure of the most promising files
            for rev_file in revision_files[:3]:  # Check first 3 files
                file_path = os.path.join(workspace_dir, rev_file)
                print(f"=== INSPECTING STRUCTURE OF {rev_file} ===\n")
                
                try:
                    # Check if it's a JSON file
                    if rev_file.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        print(f"JSON file structure:")
                        if isinstance(data, dict):
                            print(f"  Type: Dictionary with {len(data)} top-level keys")
                            for key, value in data.items():
                                if isinstance(value, list):
                                    print(f"    {key}: List with {len(value)} items")
                                    if len(value) > 0:
                                        print(f"      Sample item type: {type(value[0]).__name__}")
                                        if isinstance(value[0], dict) and len(value[0]) > 0:
                                            sample_keys = list(value[0].keys())[:5]
                                            print(f"      Sample item keys: {sample_keys}")
                                elif isinstance(value, dict):
                                    print(f"    {key}: Dictionary with {len(value)} keys")
                                    if len(value) > 0:
                                        nested_keys = list(value.keys())[:5]
                                        print(f"      Keys: {nested_keys}")
                                else:
                                    print(f"    {key}: {type(value).__name__} = {str(value)[:100]}")
                        
                        elif isinstance(data, list):
                            print(f"  Type: List with {len(data)} items")
                            if len(data) > 0:
                                print(f"  Sample item type: {type(data[0]).__name__}")
                                if isinstance(data[0], dict):
                                    sample_keys = list(data[0].keys())[:5]
                                    print(f"  Sample item keys: {sample_keys}")
                    
                    # Check if it's HTML
                    elif rev_file.endswith('.html'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()[:2000]  # First 2000 characters
                        
                        print(f"HTML file preview (first 2000 chars):")
                        print(f"  Content starts with: {content[:200]}...")
                        
                        # Look for revision-related patterns
                        revision_indicators = ['revision', 'timestamp', 'edit', 'diff', 'history']
                        found_indicators = [ind for ind in revision_indicators if ind in content.lower()]
                        print(f"  Found revision indicators: {found_indicators}")
                    
                    # Check if it's plain text
                    else:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()[:1000]  # First 1000 characters
                        
                        print(f"Text file preview (first 1000 chars):")
                        print(f"  Content: {content[:300]}...")
                        
                        # Look for date patterns
                        import re
                        date_patterns = re.findall(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{4}\d{2}\d{2}', content)
                        if date_patterns:
                            print(f"  Found date patterns: {date_patterns[:5]}")
                
                except Exception as e:
                    print(f"  ❌ Error reading {rev_file}: {str(e)}")
                
                print()
        
        else:
            print("No obvious revision data files found in this workspace\n")
```

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

### Development Step 2: Wikipedia 'Dragon' Page: Edits Removing Jokes on Leap Days (Feb 29, 2000 & 2004) Before 2008

**Description**: Search for Wikipedia revision history of the 'Dragon' page to identify edits made on leap days (February 29) before 2008. Focus on February 29, 2000 and February 29, 2004 as the only leap days in that timeframe. Look for edit summaries or revision comparisons that mention joke removal, humor deletion, or similar content changes. Extract the specific revision data showing what content was removed on those dates.

**Use Cases**:
- Academic research on Wikipedia content evolution, specifically tracking the addition and removal of humorous or non-encyclopedic material in high-traffic articles for studies on collaborative editing behavior
- Digital humanities projects analyzing how internet culture and humor have been moderated or removed from public knowledge bases over time, using leap day edits as unique temporal markers
- Automated quality assurance for Wikipedia editors or bots, flagging and reviewing edits made on rare dates (like leap days) to detect unusual or potentially disruptive changes
- Media fact-checking and journalism investigations into the history of specific Wikipedia articles, identifying when jokes or misinformation were inserted or removed, especially around notable dates
- Educational curriculum development, providing students with real-world examples of digital literacy by tracing how Wikipedia handles vandalism or joke content in popular articles
- Legal or compliance audits for organizations relying on Wikipedia data, ensuring that extracted content does not include inappropriate or humorous material that was later removed
- Historical documentation and archiving for digital librarians, preserving snapshots of Wikipedia articles on leap days to study how public knowledge changes on rare calendar dates
- Community moderation analysis for Wikimedia Foundation or similar organizations, evaluating the effectiveness of community-driven joke or vandalism removal processes by examining leap day revision histories

```
import os
import json
import requests
import time
from datetime import datetime, timedelta

print("=== ANALYZING LEAP DAY REVISION CONTENT CHANGES ===\n")
print("Objective: Examine the actual content changes in the Feb 29, 2004 revision")
print("Strategy: Compare revision content with parent revision and check surrounding edits\n")

# First, let's inspect the leap day revision data we found
workspace_dir = 'workspace'
leap_day_file = os.path.join(workspace_dir, 'dragon_leap_day_revisions.json')

print("=== STEP 1: INSPECTING SAVED LEAP DAY REVISION DATA ===\n")

if not os.path.exists(leap_day_file):
    print(f"❌ Leap day revision file not found: {leap_day_file}")
else:
    print(f"✓ Found leap day revision file: {os.path.basename(leap_day_file)}")
    
    # First inspect the structure before loading
    with open(leap_day_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"File size: {len(content):,} characters")
    
    # Now load and examine the structure
    with open(leap_day_file, 'r', encoding='utf-8') as f:
        leap_day_data = json.load(f)
    
    print("\nLeap day data structure:")
    for key in leap_day_data.keys():
        print(f"  {key}: {type(leap_day_data[key]).__name__}")
    
    if 'leap_day_revisions' in leap_day_data:
        revisions = leap_day_data['leap_day_revisions']
        print(f"\nFound {len(revisions)} leap day revision(s)")
        
        for i, rev in enumerate(revisions, 1):
            print(f"\nRevision {i} details:")
            for key, value in rev.items():
                print(f"  {key}: {value}")
            
            # Store the revision details for content analysis
            target_revid = rev.get('revid')
            parent_revid = rev.get('parentid')
            timestamp = rev.get('timestamp')
            user = rev.get('user')
            comment = rev.get('comment')
            size = rev.get('size')
            
            print(f"\n🎯 TARGET REVISION FOR CONTENT ANALYSIS:")
            print(f"  Revision ID: {target_revid}")
            print(f"  Parent ID: {parent_revid}")
            print(f"  Date: {timestamp}")
            print(f"  User: {user}")
            print(f"  Comment: '{comment}'")
            print(f"  Size: {size} bytes")

print("\n=== STEP 2: FETCHING REVISION CONTENT FOR COMPARISON ===\n")

# Wikipedia API endpoint for getting revision content
api_url = "https://en.wikipedia.org/w/api.php"

def get_revision_content(revid):
    """Get the full content of a specific revision"""
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'revisions',
        'revids': revid,
        'rvprop': 'content|timestamp|user|comment|ids|size'
    }
    
    try:
        print(f"  Fetching content for revision {revid}...")
        response = requests.get(api_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            
            if 'revisions' in pages[page_id] and len(pages[page_id]['revisions']) > 0:
                revision = pages[page_id]['revisions'][0]
                if '*' in revision:  # Content is in the '*' field
                    content = revision['*']
                    print(f"    ✓ Retrieved content: {len(content):,} characters")
                    return {
                        'content': content,
                        'revid': revision.get('revid'),
                        'timestamp': revision.get('timestamp'),
                        'user': revision.get('user'),
                        'comment': revision.get('comment'),
                        'size': revision.get('size')
                    }
                else:
                    print(f"    ❌ No content field found in revision")
                    return None
            else:
                print(f"    ❌ No revision data found")
                return None
        else:
            print(f"    ❌ No page data in API response")
            return None
            
    except Exception as e:
        print(f"    ❌ Error fetching revision {revid}: {str(e)}")
        return None

# Get content for both the target revision and its parent
print("Fetching target revision content...")
target_content = get_revision_content(target_revid)
time.sleep(1)  # Be respectful to Wikipedia's servers

print("\nFetching parent revision content...")
parent_content = get_revision_content(parent_revid)
time.sleep(1)

print("\n=== STEP 3: ANALYZING CONTENT DIFFERENCES ===\n")

if target_content and parent_content:
    target_text = target_content['content']
    parent_text = parent_content['content']
    
    print(f"Target revision ({target_revid}): {len(target_text):,} characters")
    print(f"Parent revision ({parent_revid}): {len(parent_text):,} characters")
    print(f"Size difference: {len(target_text) - len(parent_text):+,} characters")
    
    # Simple difference analysis
    if len(target_text) > len(parent_text):
        print("\n📈 CONTENT WAS ADDED (target is larger than parent)")
        change_type = "ADDITION"
    elif len(target_text) < len(parent_text):
        print("\n📉 CONTENT WAS REMOVED (target is smaller than parent)")
        change_type = "REMOVAL"
    else:
        print("\n🔄 CONTENT WAS MODIFIED (same size, likely text changes)")
        change_type = "MODIFICATION"
    
    # Find the differences by splitting into lines
    target_lines = target_text.split('\n')
    parent_lines = parent_text.split('\n')
    
    print(f"\nTarget revision: {len(target_lines)} lines")
    print(f"Parent revision: {len(parent_lines)} lines")
    
    # Simple line-by-line comparison to identify changes
    print("\n=== IDENTIFYING SPECIFIC CHANGES ===\n")
    
    # Convert to sets to find added/removed lines
    target_line_set = set(target_lines)
    parent_line_set = set(parent_lines)
    
    added_lines = target_line_set - parent_line_set
    removed_lines = parent_line_set - target_line_set
    
    print(f"Lines added: {len(added_lines)}")
    print(f"Lines removed: {len(removed_lines)}")
    
    # Show the changes
    if added_lines:
        print("\n➕ LINES ADDED:")
        for i, line in enumerate(list(added_lines)[:10], 1):  # Show first 10
            if line.strip():  # Skip empty lines
                print(f"  {i}. {line[:100]}{'...' if len(line) > 100 else ''}")
    
    if removed_lines:
        print("\n➖ LINES REMOVED:")
        for i, line in enumerate(list(removed_lines)[:10], 1):  # Show first 10
            if line.strip():  # Skip empty lines
                print(f"  {i}. {line[:100]}{'...' if len(line) > 100 else ''}")
    
    # Look for joke/humor related content in the changes
    print("\n=== SEARCHING FOR HUMOR/JOKE CONTENT ===\n")
    
    humor_keywords = ['joke', 'humor', 'humour', 'funny', 'laugh', 'comic', 'amusing', 'witty', 'silly', 'ridiculous']
    
    def check_humor_content(lines, line_type):
        humor_found = []
        for line in lines:
            line_lower = line.lower()
            found_keywords = [kw for kw in humor_keywords if kw in line_lower]
            if found_keywords:
                humor_found.append({
                    'line': line,
                    'keywords': found_keywords
                })
        
        if humor_found:
            print(f"🎭 HUMOR-RELATED CONTENT {line_type}:")
            for item in humor_found:
                print(f"  Keywords {item['keywords']}: {item['line'][:150]}{'...' if len(item['line']) > 150 else ''}")
        else:
            print(f"  No obvious humor-related content in {line_type.lower()} lines")
        
        return humor_found
    
    added_humor = check_humor_content(added_lines, "ADDED")
    removed_humor = check_humor_content(removed_lines, "REMOVED")
    
    # Save the content analysis
    content_analysis = {
        'analysis_metadata': {
            'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'target_revision_id': target_revid,
            'parent_revision_id': parent_revid,
            'leap_day_date': '2004-02-29',
            'change_type': change_type
        },
        'target_revision': {
            'revid': target_content['revid'],
            'timestamp': target_content['timestamp'],
            'user': target_content['user'],
            'comment': target_content['comment'],
            'size': target_content['size'],
            'content_length': len(target_text),
            'line_count': len(target_lines)
        },
        'parent_revision': {
            'revid': parent_content['revid'],
            'timestamp': parent_content['timestamp'],
            'user': parent_content['user'],
            'comment': parent_content['comment'],
            'size': parent_content['size'],
            'content_length': len(parent_text),
            'line_count': len(parent_lines)
        },
        'content_changes': {
            'size_difference': len(target_text) - len(parent_text),
            'lines_added': len(added_lines),
            'lines_removed': len(removed_lines),
            'added_lines': list(added_lines)[:20],  # Save first 20 for space
            'removed_lines': list(removed_lines)[:20],
            'humor_content_added': added_humor,
            'humor_content_removed': removed_humor
        }
    }
    
    analysis_file = os.path.join(workspace_dir, 'leap_day_content_analysis.json')
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(content_analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Content analysis saved to: {os.path.basename(analysis_file)}")
    
else:
    print("❌ Could not retrieve content for comparison")

print("\n=== STEP 4: CHECKING SURROUNDING REVISIONS ===\n")
print("Looking for revisions before and after the leap day to find joke removal context...")

# Load the raw revision data to find revisions around the leap day
raw_file = os.path.join(workspace_dir, 'dragon_wikipedia_revisions_raw.json')
if os.path.exists(raw_file):
    with open(raw_file, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    all_revisions = raw_data.get('revisions', [])
    
    # Find revisions around February 29, 2004
    target_date = datetime(2004, 2, 29)
    nearby_revisions = []
    
    for rev in all_revisions:
        if 'timestamp' in rev:
            try:
                rev_datetime = datetime.fromisoformat(rev['timestamp'].replace('Z', '+00:00')).replace(tzinfo=None)
                time_diff = abs((rev_datetime - target_date).days)
                
                # Get revisions within 7 days of the leap day
                if time_diff <= 7:
                    nearby_revisions.append({
                        'revision': rev,
                        'days_from_target': (rev_datetime - target_date).days,
                        'datetime': rev_datetime
                    })
            except:
                continue
    
    # Sort by datetime
    nearby_revisions.sort(key=lambda x: x['datetime'])
    
    print(f"Found {len(nearby_revisions)} revisions within 7 days of Feb 29, 2004:")
    
    for i, item in enumerate(nearby_revisions, 1):
        rev = item['revision']
        days_diff = item['days_from_target']
        
        print(f"\n{i}. {rev['timestamp']} ({days_diff:+d} days)")
        print(f"   User: {rev.get('user', 'Unknown')}")
        print(f"   Comment: {rev.get('comment', 'No comment')}")
        print(f"   Size: {rev.get('size', 'Unknown')} bytes")
        
        # Check for joke/humor keywords in comments
        comment = rev.get('comment', '').lower()
        joke_keywords = ['joke', 'humor', 'humour', 'funny', 'laugh', 'remove', 'delete', 'clean', 'vandal', 'revert']
        found_keywords = [kw for kw in joke_keywords if kw in comment]
        
        if found_keywords:
            print(f"   🔍 RELEVANT KEYWORDS: {found_keywords}")
        
        # Highlight the leap day revision
        if rev.get('revid') == target_revid:
            print(f"   🎯 *** THIS IS THE LEAP DAY REVISION ***")
    
    # Save nearby revisions analysis
    nearby_data = {
        'search_metadata': {
            'target_date': '2004-02-29',
            'search_window_days': 7,
            'revisions_found': len(nearby_revisions)
        },
        'nearby_revisions': [item['revision'] for item in nearby_revisions]
    }
    
    nearby_file = os.path.join(workspace_dir, 'leap_day_nearby_revisions.json')
    with open(nearby_file, 'w', encoding='utf-8') as f:
        json.dump(nearby_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Nearby revisions analysis saved to: {os.path.basename(nearby_file)}")

else:
    print("❌ Raw revision data file not found")

print("\n=== ANALYSIS SUMMARY ===\n")
print("🎯 LEAP DAY REVISION ANALYSIS COMPLETE")
print("\n📋 FINDINGS:")
print(f"- Found 1 revision on February 29, 2004 (ID: {target_revid})")
print(f"- Comment: '{comment}' suggests humorous content was involved")
print(f"- Content analysis shows whether content was added, removed, or modified")
print(f"- Surrounding revisions provide context for joke-related activity")

print("\n📁 FILES CREATED:")
print(f"- Content analysis: leap_day_content_analysis.json")
print(f"- Nearby revisions: leap_day_nearby_revisions.json")

print("\n🔍 INTERPRETATION:")
print("The comment 'I admit, I did laugh. :-)' suggests this revision was likely")
print("RESPONDING to humorous content rather than removing it. The actual content")
print("changes will show whether jokes were added or removed on this leap day.")
print("\nIf no joke removal is found in this revision, the surrounding revisions")
print("may contain the actual joke removal that this comment references.")
```

## Created Time
2025-08-11 09:58:17
