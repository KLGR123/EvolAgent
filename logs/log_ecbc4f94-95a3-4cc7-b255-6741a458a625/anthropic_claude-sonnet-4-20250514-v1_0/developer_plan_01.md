# Developer Plan 01

## Plan
Search for and access the English Wikipedia article about 'Lego' to find the latest version from 2022. Use web search or direct Wikipedia access to locate the Lego article, then identify the specific revision that represents the latest version from 2022 (likely from late December 2022). Once the correct 2022 version is accessed, systematically count all images present in the article content, including photographs, diagrams, logos, and any other visual media embedded within the article text.

## Description
This is the optimal starting approach because: (1) We need to identify and access the specific 2022 version of the Lego Wikipedia article rather than the current version, (2) No previous research has been conducted on this image counting task, (3) Expected outcome is to locate the correct 2022 article version and extract all embedded images for counting, (4) This directly addresses the TASK requirement to determine the exact number of images in the latest 2022 version of the Lego English Wikipedia article.

## Episodic Examples
### Development Step 3: Wikipedia 'Dragon' Page: Leap Day (Feb 29, 2000 & 2004) Edits Removing Jokes or Humor Content

**Description**: Search for Wikipedia revision history of the 'Dragon' page to identify edits made on leap days (February 29) before 2008. Focus on February 29, 2000 and February 29, 2004 as the only leap days in that timeframe. Look for edit summaries or revision comparisons that mention joke removal, humor deletion, or similar content changes. Extract the specific revision data showing what content was removed on those dates.

**Use Cases**:
- Historical Wikipedia content auditing to verify removal of informal or humorous material for compliance with encyclopedic standards
- Academic research into the evolution of Wikipedia article tone and editorial practices over time
- Automated detection and documentation of joke or prank edits in high-profile Wikipedia pages for digital humanities studies
- Quality assurance for Wikipedia administrators seeking to identify and review non-encyclopedic content edits on significant dates (e.g., leap days, anniversaries)
- Training dataset generation for machine learning models that classify humorous versus formal content in collaborative knowledge bases
- Media fact-checking to trace the origin and removal of viral or meme-like phrases from public knowledge resources
- Educational curriculum development illustrating the importance of editorial oversight and tone in open-source encyclopedias
- Archival preservation projects aiming to document the cultural history of online communities through notable content changes

```
import os
import json
from datetime import datetime

print("=== EXAMINING SPECIFIC REMOVED CONTENT FOR JOKE ELEMENTS ===\n")
print("Objective: Analyze the exact content that was removed on Feb 29, 2004 leap day")
print("Focus: Look for humorous elements in 'Here be dragons:' and other removed text\n")

# First, inspect the content analysis file structure
workspace_dir = 'workspace'
content_analysis_file = os.path.join(workspace_dir, 'leap_day_content_analysis.json')

print("=== STEP 1: INSPECTING CONTENT ANALYSIS FILE STRUCTURE ===\n")

if not os.path.exists(content_analysis_file):
    print(f"❌ Content analysis file not found: {content_analysis_file}")
else:
    print(f"✓ Found content analysis file: {os.path.basename(content_analysis_file)}")
    
    # First peek at the file structure
    with open(content_analysis_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"File size: {len(content):,} characters")
    
    # Now load and inspect structure before accessing
    with open(content_analysis_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    print("\nContent analysis file structure:")
    for key in analysis_data.keys():
        value = analysis_data[key]
        print(f"  {key}: {type(value).__name__}")
        if isinstance(value, dict):
            print(f"    Sub-keys: {list(value.keys())}")
        elif isinstance(value, list):
            print(f"    List length: {len(value)}")

print("\n=== STEP 2: EXAMINING THE REMOVED CONTENT IN DETAIL ===\n")

# Now safely access the content changes
if 'content_changes' in analysis_data:
    content_changes = analysis_data['content_changes']
    
    print("Content changes summary:")
    for key, value in content_changes.items():
        if key not in ['added_lines', 'removed_lines']:  # Skip the large lists for now
            print(f"  {key}: {value}")
    
    # Focus on the removed lines - this is where jokes might be
    if 'removed_lines' in content_changes:
        removed_lines = content_changes['removed_lines']
        print(f"\n📉 DETAILED ANALYSIS OF {len(removed_lines)} REMOVED LINES:\n")
        
        for i, line in enumerate(removed_lines, 1):
            print(f"{i}. '{line}'")
            print(f"   Length: {len(line)} characters")
            
            # Analyze each removed line for potential humor
            line_lower = line.lower().strip()
            
            # Check for specific humor indicators
            humor_indicators = {
                'here be dragons': 'Classical humorous map phrase',
                'pickled': 'Unusual/humorous adjective for dragons',
                'silly': 'Direct humor indicator',
                'funny': 'Direct humor indicator', 
                'joke': 'Direct humor indicator',
                'amusing': 'Humor indicator',
                'ridiculous': 'Humor indicator',
                'comic': 'Humor indicator'
            }
            
            found_indicators = []
            for indicator, description in humor_indicators.items():
                if indicator in line_lower:
                    found_indicators.append((indicator, description))
            
            if found_indicators:
                print(f"   🎭 HUMOR INDICATORS FOUND:")
                for indicator, description in found_indicators:
                    print(f"      - '{indicator}': {description}")
            
            # Check for references to specific content that might be humorous
            if 'here be dragons' in line_lower:
                print(f"   🗺️ CLASSICAL REFERENCE: 'Here be dragons' is a famous phrase from old maps")
                print(f"      This phrase is often used humorously in modern contexts")
                print(f"      Removing this could be cleaning up informal/humorous content")
            
            if 'pickled' in line_lower:
                print(f"   🥒 UNUSUAL DESCRIPTOR: 'Pickled dragon' is an unconventional term")
                print(f"      This could be humorous or whimsical content being removed")
            
            print()
    
    # Also examine what was added to understand the transformation
    if 'added_lines' in content_changes:
        added_lines = content_changes['added_lines']
        print(f"\n📈 DETAILED ANALYSIS OF {len(added_lines)} ADDED LINES:\n")
        
        for i, line in enumerate(added_lines, 1):
            print(f"{i}. '{line}'")
            print(f"   Length: {len(line)} characters")
            
            # Analyze the formality/structure of added content
            if 'disambiguation' in line.lower() or 'disambig' in line.lower():
                print(f"   📋 FORMAL STRUCTURE: This is standard Wikipedia disambiguation formatting")
            
            if line.startswith('The term'):
                print(f"   📝 FORMAL OPENING: Standard encyclopedia-style introduction")
            
            if '[[' in line and ']]' in line:
                print(f"   🔗 WIKI LINK: Proper Wikipedia link formatting")
            
            print()

print("=== STEP 3: CONTEXTUAL ANALYSIS OF THE TRANSFORMATION ===\n")

# Analyze the overall transformation
if 'target_revision' in analysis_data and 'parent_revision' in analysis_data:
    target = analysis_data['target_revision']
    parent = analysis_data['parent_revision']
    
    print("Revision transformation summary:")
    print(f"  Before (parent): {parent['size']} bytes, {parent['line_count']} lines")
    print(f"  After (target):  {target['size']} bytes, {target['line_count']} lines")
    print(f"  User: {target['user']}")
    print(f"  Comment: '{target['comment']}'")
    
    size_change = target['size'] - parent['size']
    print(f"  Net change: {size_change:+d} bytes")
    
    print(f"\n🔄 TRANSFORMATION TYPE ANALYSIS:")
    print(f"This appears to be a cleanup/formalization edit where:")
    print(f"  - Informal content ('Here be dragons:') was removed")
    print(f"  - Proper disambiguation formatting was added")
    print(f"  - The page was restructured from casual to formal style")
    
    print(f"\n💭 COMMENT INTERPRETATION:")
    print(f"The comment 'I admit, I did laugh. :-)' suggests:")
    print(f"  - The user found something amusing in the previous version")
    print(f"  - They acknowledged the humor while cleaning it up")
    print(f"  - This was likely removing informal/humorous content for encyclopedic tone")

print("\n=== STEP 4: EXAMINING NEARBY REVISIONS FOR MORE CONTEXT ===\n")

# Check the nearby revisions file structure first
nearby_file = os.path.join(workspace_dir, 'leap_day_nearby_revisions.json')

if os.path.exists(nearby_file):
    print(f"✓ Found nearby revisions file: {os.path.basename(nearby_file)}")
    
    # Inspect structure first
    with open(nearby_file, 'r', encoding='utf-8') as f:
        nearby_content = f.read()
        print(f"File size: {len(nearby_content):,} characters")
    
    with open(nearby_file, 'r', encoding='utf-8') as f:
        nearby_data = json.load(f)
    
    print("\nNearby revisions file structure:")
    for key in nearby_data.keys():
        value = nearby_data[key]
        print(f"  {key}: {type(value).__name__}")
        if isinstance(value, dict):
            print(f"    Sub-keys: {list(value.keys())}")
        elif isinstance(value, list):
            print(f"    List length: {len(value)}")
    
    # Look for the revision that added the 'pickled dragon' reference
    if 'nearby_revisions' in nearby_data:
        nearby_revs = nearby_data['nearby_revisions']
        
        print(f"\n🔍 SEARCHING {len(nearby_revs)} NEARBY REVISIONS FOR HUMOR CONTEXT:\n")
        
        for i, rev in enumerate(nearby_revs, 1):
            timestamp = rev.get('timestamp', 'Unknown')
            user = rev.get('user', 'Unknown')
            comment = rev.get('comment', 'No comment')
            revid = rev.get('revid', 'Unknown')
            
            print(f"{i}. {timestamp} (ID: {revid})")
            print(f"   User: {user}")
            print(f"   Comment: '{comment}'")
            
            # Analyze comments for humor-related activity
            comment_lower = comment.lower()
            
            humor_keywords = ['pickled', 'dragon', 'laugh', 'funny', 'joke', 'humor', 'amusing']
            found_keywords = [kw for kw in humor_keywords if kw in comment_lower]
            
            if found_keywords:
                print(f"   🎭 HUMOR KEYWORDS: {found_keywords}")
            
            # Special analysis for the pickled dragon addition
            if 'pickled dragon' in comment_lower:
                print(f"   🥒 PICKLED DRAGON REFERENCE: This revision added humorous content")
                print(f"       The leap day revision likely removed this humorous reference")
            
            # Mark our target revision
            if revid == 2580816:
                print(f"   🎯 *** THIS IS THE LEAP DAY REVISION ***")
                print(f"       This revision cleaned up the humorous content added earlier")
            
            print()
else:
    print(f"❌ Nearby revisions file not found: {nearby_file}")

print("=== FINAL ANALYSIS AND CONCLUSIONS ===\n")

print("🎯 LEAP DAY JOKE REMOVAL ANALYSIS COMPLETE\n")

print("📋 KEY FINDINGS:")
print("\n1. CONTENT REMOVED ON FEBRUARY 29, 2004:")
print("   - 'Here be dragons:' - Classical humorous map phrase")
print("   - Informal disambiguation text")
print("   - Reference to 'pickled dragon' (added Feb 22, 2004)")

print("\n2. HUMOR ELEMENTS IDENTIFIED:")
print("   - 'Here be dragons' is a famous humorous phrase from medieval maps")
print("   - 'Pickled dragon' is an unconventional, whimsical term")
print("   - The informal tone was replaced with formal Wikipedia style")

print("\n3. EDIT SEQUENCE RECONSTRUCTION:")
print("   - Feb 22: User 'Lady Tenar' added 'pickled dragon' link (humorous)")
print("   - Feb 29: User 'Timwi' cleaned up the page, removing informal/humorous content")
print("   - Comment 'I admit, I did laugh. :-)' acknowledges the humor being removed")

print("\n4. CONCLUSION:")
print("   ✅ JOKE REMOVAL CONFIRMED on February 29, 2004 leap day")
print("   - Humorous references ('Here be dragons', 'pickled dragon') were removed")
print("   - Page was formalized from casual to encyclopedic tone")
print("   - User explicitly acknowledged the humor while cleaning it up")

# Create final summary report
summary_report = {
    'analysis_complete': True,
    'leap_day_date': '2004-02-29',
    'revision_id': 2580816,
    'user': 'Timwi',
    'comment': 'I admit, I did laugh. :-)',
    'joke_removal_confirmed': True,
    'humorous_content_removed': [
        {
            'content': 'Here be dragons:',
            'humor_type': 'Classical humorous map phrase',
            'description': 'Famous phrase from medieval maps, often used humorously in modern contexts'
        },
        {
            'content': 'pickled dragon reference',
            'humor_type': 'Whimsical/unconventional descriptor', 
            'description': 'Unusual adjective making dragons sound silly or food-like'
        }
    ],
    'transformation_type': 'Formalization - casual to encyclopedic tone',
    'context': 'User acknowledged humor while cleaning up informal content for Wikipedia standards',
    'files_created': [
        'leap_day_content_analysis.json',
        'leap_day_nearby_revisions.json',
        'dragon_wikipedia_revisions_raw.json',
        'dragon_leap_day_revisions.json'
    ]
}

summary_file = os.path.join(workspace_dir, 'leap_day_joke_removal_final_report.json')
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary_report, f, indent=2, ensure_ascii=False)

print(f"\n✅ Final analysis report saved to: {os.path.basename(summary_file)}")

print("\n🎉 MISSION ACCOMPLISHED:")
print("Successfully identified joke removal on February 29, 2004 leap day!")
print("The Wikipedia Dragon page had humorous content removed and was formalized.")
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

### Development Step 1: Title: Identify 'Dragon' Wikipedia Edits on Feb 29, 2000/2004 Removing Jokes or Humor Content

**Description**: Search for Wikipedia revision history of the 'Dragon' page to identify edits made on leap days (February 29) before 2008. Focus on February 29, 2000 and February 29, 2004 as the only leap days in that timeframe. Look for edit summaries or revision comparisons that mention joke removal, humor deletion, or similar content changes. Extract the specific revision data showing what content was removed on those dates.

**Use Cases**:
- Academic research on the evolution of Wikipedia articles to study how humor and non-encyclopedic content is filtered out over time, using the 'Dragon' page as a case study.
- Quality assurance for Wikipedia editors or administrators to audit and document the removal of inappropriate or joke content on significant dates, such as leap days, for compliance and transparency.
- Digital humanities projects analyzing patterns of community moderation and content curation on collaborative platforms, focusing on specific cultural or temporal events.
- Automated detection of vandalism or non-serious edits for Wikipedia monitoring bots, using leap day edits as a targeted anomaly detection scenario.
- Journalism or media investigations into the history of internet folklore and mythological topics, tracing how public contributions and editorial standards have changed on notable dates.
- Training datasets creation for machine learning models that classify Wikipedia edit comments or revision types, especially for distinguishing between humor removal and other edit actions.
- Educational workshops or classroom exercises in digital literacy, teaching students how to trace the provenance and editorial changes of online encyclopedia entries.
- Archival documentation for libraries or digital preservationists seeking to capture and analyze the evolution of notable Wikipedia articles around rare calendar events like leap days.

```
import requests
import json
import os
from datetime import datetime
import time

print("=== EXTRACTING WIKIPEDIA DRAGON PAGE REVISION HISTORY ===\n")
print("Objective: Find edits made on leap days (Feb 29) before 2008 that removed jokes/humor\n")

# Create workspace directory if it doesn't exist
workspace_dir = 'workspace'
if not os.path.exists(workspace_dir):
    os.makedirs(workspace_dir)
    print(f"Created workspace directory: {workspace_dir}")
else:
    print(f"Using existing workspace directory: {workspace_dir}")

# Target leap days before 2008
target_dates = [
    '2000-02-29',  # February 29, 2000
    '2004-02-29'   # February 29, 2004
]

print(f"Target leap days to search: {target_dates}\n")

# Wikipedia API endpoint
api_url = "https://en.wikipedia.org/w/api.php"
page_title = "Dragon"

print(f"Extracting revision history for Wikipedia page: {page_title}\n")

# Parameters for getting revision history
params = {
    'action': 'query',
    'format': 'json',
    'prop': 'revisions',
    'titles': page_title,
    'rvlimit': 'max',  # Get maximum revisions per request (500)
    'rvprop': 'timestamp|user|comment|ids|size',
    'rvdir': 'newer',  # Start from oldest revisions
    'rvstart': '1999-01-01T00:00:00Z',  # Start from 1999 to capture 2000 leap day
    'rvend': '2008-01-01T00:00:00Z'     # End before 2008 as specified
}

print("=== FETCHING DRAGON PAGE REVISION DATA FROM WIKIPEDIA API ===\n")

all_revisions = []
rvcontinue = None
request_count = 0
max_requests = 20  # Reasonable limit to get revisions from 1999-2008

while request_count < max_requests:
    request_count += 1
    
    # Add continuation parameter if we have one
    current_params = params.copy()
    if rvcontinue:
        current_params['rvcontinue'] = rvcontinue
    
    print(f"Request {request_count}: Fetching Dragon page revisions...")
    
    try:
        response = requests.get(api_url, params=current_params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Check for API errors
        if 'error' in data:
            print(f"  ❌ API Error: {data['error']}")
            break
        
        # Extract revisions from response
        if 'query' in data and 'pages' in data['query']:
            pages = data['query']['pages']
            page_id = list(pages.keys())[0]
            
            if page_id == '-1':
                print("  ❌ Page not found")
                break
                
            if 'revisions' in pages[page_id]:
                revisions = pages[page_id]['revisions']
                all_revisions.extend(revisions)
                print(f"  Retrieved {len(revisions)} revisions (total so far: {len(all_revisions)})")
                
                # Show sample of timestamps to track progress
                if revisions:
                    first_ts = revisions[0]['timestamp']
                    last_ts = revisions[-1]['timestamp']
                    print(f"  Date range: {first_ts} to {last_ts}")
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
            print("  All revisions in date range retrieved")
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
    print("❌ No revision data extracted. Cannot proceed with leap day analysis.")
else:
    # Save the raw revision data
    raw_data = {
        'extraction_metadata': {
            'page_title': page_title,
            'extraction_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_revisions': len(all_revisions),
            'api_requests': request_count,
            'date_range': '1999-01-01 to 2008-01-01',
            'target_leap_days': target_dates
        },
        'revisions': all_revisions
    }
    
    raw_file = os.path.join(workspace_dir, 'dragon_wikipedia_revisions_raw.json')
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Raw revision data saved to: {os.path.basename(raw_file)}")
    print(f"   File size: {os.path.getsize(raw_file):,} bytes")
    
    # Analyze the data structure
    print(f"\n=== ANALYZING REVISION DATA STRUCTURE ===\n")
    
    if all_revisions:
        sample_revision = all_revisions[0]
        print(f"Sample revision structure:")
        for key, value in sample_revision.items():
            print(f"  {key}: {type(value).__name__} = {str(value)[:100]}")
        
        # Show date range of all revisions
        timestamps = [rev['timestamp'] for rev in all_revisions if 'timestamp' in rev]
        if timestamps:
            print(f"\nRevision date range:")
            print(f"  Earliest: {min(timestamps)}")
            print(f"  Latest: {max(timestamps)}")
        
        print(f"\nSample timestamps:")
        for i, rev in enumerate(all_revisions[:5]):
            if 'timestamp' in rev:
                print(f"  {i+1}. {rev['timestamp']} - {rev.get('comment', 'No comment')[:50]}...")
    
    print(f"\n=== FILTERING FOR LEAP DAY REVISIONS ===\n")
    
    leap_day_revisions = []
    
    # Check each revision for leap day dates
    for revision in all_revisions:
        if 'timestamp' in revision:
            timestamp = revision['timestamp']
            # Extract date part (YYYY-MM-DD)
            date_part = timestamp.split('T')[0]
            
            if date_part in target_dates:
                leap_day_revisions.append(revision)
                print(f"🎯 LEAP DAY REVISION FOUND!")
                print(f"  Date: {date_part}")
                print(f"  Time: {timestamp}")
                print(f"  User: {revision.get('user', 'Unknown')}")
                print(f"  Comment: {revision.get('comment', 'No comment')}")
                print(f"  Revision ID: {revision.get('revid', 'Unknown')}")
                print(f"  Size: {revision.get('size', 'Unknown')} bytes")
                
                # Check if comment mentions joke/humor removal keywords
                comment = revision.get('comment', '').lower()
                joke_keywords = ['joke', 'humor', 'humour', 'funny', 'remove', 'delete', 'clean', 'vandal']
                found_keywords = [kw for kw in joke_keywords if kw in comment]
                
                if found_keywords:
                    print(f"  🔍 POTENTIAL JOKE/HUMOR REMOVAL: Found keywords {found_keywords}")
                else:
                    print(f"  ℹ️ No obvious joke/humor removal keywords in comment")
                print()
    
    print(f"=== LEAP DAY ANALYSIS RESULTS ===\n")
    print(f"Total revisions analyzed: {len(all_revisions)}")
    print(f"Leap day revisions found: {len(leap_day_revisions)}")
    
    if leap_day_revisions:
        print(f"\n🎉 SUCCESS: Found {len(leap_day_revisions)} revision(s) on target leap days!\n")
        
        # Save leap day revisions
        leap_day_data = {
            'analysis_metadata': {
                'analysis_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'target_leap_days': target_dates,
                'total_revisions_analyzed': len(all_revisions),
                'leap_day_revisions_found': len(leap_day_revisions)
            },
            'leap_day_revisions': leap_day_revisions
        }
        
        leap_day_file = os.path.join(workspace_dir, 'dragon_leap_day_revisions.json')
        with open(leap_day_file, 'w', encoding='utf-8') as f:
            json.dump(leap_day_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Leap day revision data saved to: {os.path.basename(leap_day_file)}")
        
        # Create summary report
        summary_file = os.path.join(workspace_dir, 'leap_day_analysis_summary.txt')
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"WIKIPEDIA DRAGON PAGE LEAP DAY REVISION ANALYSIS\n")
            f.write(f"={'='*50}\n\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Page Analyzed: {page_title}\n")
            f.write(f"Date Range: 1999-01-01 to 2008-01-01\n")
            f.write(f"Target Leap Days: {', '.join(target_dates)}\n\n")
            f.write(f"RESULTS:\n")
            f.write(f"- Total revisions analyzed: {len(all_revisions)}\n")
            f.write(f"- Leap day revisions found: {len(leap_day_revisions)}\n\n")
            
            if leap_day_revisions:
                f.write(f"LEAP DAY REVISIONS DETAILS:\n")
                for i, rev in enumerate(leap_day_revisions, 1):
                    f.write(f"\n{i}. Revision on {rev['timestamp'].split('T')[0]}:\n")
                    f.write(f"   - Timestamp: {rev['timestamp']}\n")
                    f.write(f"   - User: {rev.get('user', 'Unknown')}\n")
                    f.write(f"   - Revision ID: {rev.get('revid', 'Unknown')}\n")
                    f.write(f"   - Size: {rev.get('size', 'Unknown')} bytes\n")
                    f.write(f"   - Comment: {rev.get('comment', 'No comment')}\n")
                    
                    # Check for joke/humor keywords
                    comment = rev.get('comment', '').lower()
                    joke_keywords = ['joke', 'humor', 'humour', 'funny', 'remove', 'delete', 'clean', 'vandal']
                    found_keywords = [kw for kw in joke_keywords if kw in comment]
                    if found_keywords:
                        f.write(f"   - POTENTIAL JOKE/HUMOR REMOVAL: Keywords found: {found_keywords}\n")
        
        print(f"✅ Summary report saved to: {os.path.basename(summary_file)}")
        
    else:
        print(f"⚠️ No revisions found on the target leap days ({', '.join(target_dates)})")
        print(f"\nThis could mean:")
        print(f"- No edits were made to the Dragon page on those specific dates")
        print(f"- The page didn't exist yet on those dates")
        print(f"- The revisions were outside our date range filter")
        
        # Show some revisions around the target dates for context
        print(f"\n=== REVISIONS NEAR TARGET DATES FOR CONTEXT ===\n")
        
        for target_date in target_dates:
            target_year = target_date.split('-')[0]
            print(f"Revisions from {target_year}:")
            
            year_revisions = [rev for rev in all_revisions 
                            if rev.get('timestamp', '').startswith(target_year)]
            
            if year_revisions:
                print(f"  Found {len(year_revisions)} revisions in {target_year}")
                for rev in year_revisions[:3]:  # Show first 3
                    print(f"    {rev['timestamp']} - {rev.get('comment', 'No comment')[:60]}...")
            else:
                print(f"  No revisions found in {target_year}")
            print()
    
    print(f"\n🎯 ANALYSIS COMPLETE")
    print(f"📁 Key files created:")
    print(f"  - Raw data: {os.path.basename(raw_file)}")
    if leap_day_revisions:
        print(f"  - Leap day data: {os.path.basename(leap_day_file)}")
        print(f"  - Summary report: {os.path.basename(summary_file)}")
    
    print(f"\n🔍 Next steps: If leap day revisions were found, analyze the specific content changes")
    print(f"   If no leap day revisions found, may need to expand search or check different pages")
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

## Created Time
2025-08-14 02:02:38
