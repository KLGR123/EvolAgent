# Developer Plan 01

## Plan
Search for and access the English Wikipedia article about Lego from 2022 to identify the latest version available from that year. Extract and count all images present in the article, including photographs, diagrams, logos, and any other visual content embedded within the page content.

## Description
This is the optimal starting approach because: (1) We need to locate the specific 2022 version of the Lego Wikipedia article to ensure we're analyzing the correct timeframe, (2) No previous research has been conducted, (3) Expected outcome is to access the Wikipedia page and systematically identify all images contained within the article content, (4) This directly addresses the TASK requirement to count the total number of images in the latest 2022 Lego English Wikipedia article.

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

### Development Step 5: Analyze 2022 Legume Wikipedia Logs for Content Violations and Decode ‘R’ Policy Meaning

**Description**: Search for information about the Legume Wikipedia page and identify what content violations occurred in its public logs during 2022 before December. Focus on finding the specific type of content that was violated and the associated three core policies, particularly identifying what 'R' stands for in those policies.

**Use Cases**:
- Wikipedia community management: Auditing the edit history of high-traffic plant taxonomy pages (like “Legume”) to flag all vandalism, spam, or unsourced content removals before December 2022 and ensure policy compliance.
- Academic research on collaborative editing: Extracting detailed rollback summaries and policy references from the Legume page’s 2022 logs to analyze how “No Original Research” (NOR) and “Verifiability” (V) issues evolve in botanical articles.
- Data journalism investigation: Mining the public history of articles on crop nutrition to identify when and why nutritional claims were removed or reverted, helping reporters document misinformation trends in legumes.
- Legal and copyright compliance review: Systematically collecting all entries marked “deleted,” “removed,” or “rollback” from the Legume page to verify that no copyrighted text was inadvertently retained in public edits during 2022.
- Non-profit conservation monitoring: Automating a monthly scan of endangered plant species pages (including legumes) to detect policy violations and generate alerts for curators when unsourced or promotional content appears.
- Bot development for policy enforcement: Feeding the parsed 2022 edit summaries into a custom moderation bot that recognizes “RV,” “SPAM,” and “VAND” tags to automatically revert or flag noncompliant edits in ecology-related articles.
- Digital literacy education: Leveraging real flagged entries from the Legume page to teach students about the three core Wikipedia policies (NPOV, V, NOR) and how to spot and document content violations in collaborative platforms.
- SEO and brand management: Reviewing promotional content removals on corporate-sponsored legume pages to understand why certain claims were reverted, guiding marketing teams to craft compliance-ready copy.

```
import os
import json
from bs4 import BeautifulSoup
import re

print("=== DEEP DIVE INTO EDIT HISTORY FOR CONTENT VIOLATIONS ===\n")
print("Objective: Extract detailed edit summaries and administrative actions from 2022\n")

# Locate workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("No workspace directory found.")
    exit()

workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Load the edit history HTML file directly for detailed parsing
history_file = None
for file in os.listdir(workspace_dir):
    if 'history' in file.lower() and file.endswith('.html'):
        history_file = os.path.join(workspace_dir, file)
        break

if not history_file or not os.path.exists(history_file):
    print("Edit history file not found.")
    exit()

print(f"Parsing edit history file: {os.path.basename(history_file)}")
file_size = os.path.getsize(history_file)
print(f"File size: {file_size:,} bytes\n")

# Parse the HTML with focus on edit summaries and administrative actions
with open(history_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, 'html.parser')

print("=== SEARCHING FOR EDIT ENTRIES WITH SUMMARIES ===\n")

# Look for edit history entries - Wikipedia edit history typically uses specific CSS classes
edit_entries = []

# Try multiple selectors for edit history entries
selectors_to_try = [
    'li.mw-history-line',  # Common class for edit history lines
    'li[class*="history"]',  # Any li with 'history' in class name
    'li[id*="mw-history"]',  # Any li with history in id
    'tr[class*="history"]',  # Table rows with history class
    'tr[class*="mw-history"]'  # MW history table rows
]

for selector in selectors_to_try:
    entries = soup.select(selector)
    if entries:
        print(f"Found {len(entries)} edit entries using selector: {selector}")
        edit_entries = entries
        break

if not edit_entries:
    print("No edit entries found with standard selectors. Trying broader search...\n")
    # Try to find any list items or table rows containing dates
    all_lis = soup.find_all('li')
    all_trs = soup.find_all('tr')
    
    # Look for elements containing 2022 dates
    potential_entries = []
    for element in all_lis + all_trs:
        element_text = element.get_text()
        if '2022' in element_text and any(month in element_text.lower() for month in ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november']):
            potential_entries.append(element)
    
    edit_entries = potential_entries
    print(f"Found {len(edit_entries)} potential edit entries containing 2022 dates\n")

print("=== ANALYZING EDIT ENTRIES FOR VIOLATIONS ===\n")

violation_entries = []
content_violations = []
policy_references = []

for i, entry in enumerate(edit_entries[:20], 1):  # Analyze first 20 entries
    entry_text = entry.get_text().strip()
    entry_html = str(entry)
    
    print(f"Edit Entry {i}:")
    print(f"Text: {entry_text[:300]}...")  # First 300 characters
    
    # Look for 2022 dates specifically before December
    before_december_2022 = False
    date_patterns = [
        r'\b(January|February|March|April|May|June|July|August|September|October|November)\s+\d{1,2},?\s+2022\b',
        r'\b2022[-/]\d{1,2}[-/]\d{1,2}\b',
        r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)\s+2022\b'
    ]
    
    for pattern in date_patterns:
        if re.search(pattern, entry_text, re.IGNORECASE):
            before_december_2022 = True
            break
    
    # Look for violation indicators in edit summaries
    violation_keywords = [
        'revert', 'reverted', 'undid', 'rollback', 'removed', 'deleted', 'blocked',
        'vandalism', 'spam', 'violation', 'policy', 'warning', 'copyright',
        'inappropriate', 'unsourced', 'unreliable', 'promotional', 'pov'
    ]
    
    found_violations = [keyword for keyword in violation_keywords if keyword.lower() in entry_text.lower()]
    
    # Look for policy abbreviations that might include 'R'
    policy_abbreviations = re.findall(r'\b[A-Z]{2,}\b', entry_text)
    r_policies = [abbrev for abbrev in policy_abbreviations if 'R' in abbrev]
    
    # Look for "three" with policy context
    three_policy_context = 'three' in entry_text.lower() and any(word in entry_text.lower() for word in ['policy', 'policies', 'rule', 'rules'])
    
    print(f"  Before December 2022: {before_december_2022}")
    print(f"  Violation keywords found: {found_violations}")
    print(f"  Policy abbreviations: {policy_abbreviations}")
    print(f"  R-containing policies: {r_policies}")
    print(f"  Three+policy context: {three_policy_context}")
    
    # Store significant entries
    if before_december_2022 and (found_violations or r_policies or three_policy_context):
        violation_entry = {
            'entry_number': i,
            'full_text': entry_text,
            'html': entry_html,
            'violation_keywords': found_violations,
            'policy_abbreviations': policy_abbreviations,
            'r_policies': r_policies,
            'three_policy_context': three_policy_context,
            'before_december_2022': before_december_2022
        }
        violation_entries.append(violation_entry)
        print(f"  *** FLAGGED AS POTENTIAL VIOLATION ENTRY ***")
    
    print()

print(f"=== FLAGGED VIOLATION ENTRIES: {len(violation_entries)} ===\n")

# Detailed analysis of flagged entries
for i, entry in enumerate(violation_entries, 1):
    print(f"VIOLATION ENTRY {i}:")
    print(f"Full text: {entry['full_text']}")
    print(f"Keywords: {entry['violation_keywords']}")
    print(f"Policy abbreviations: {entry['policy_abbreviations']}")
    print(f"R-containing policies: {entry['r_policies']}")
    print()

# Search for specific Wikipedia policy abbreviations
print("=== SEARCHING FOR COMMON WIKIPEDIA POLICY ABBREVIATIONS ===\n")

common_policies = {
    'BLP': 'Biographies of Living Persons',
    'COI': 'Conflict of Interest', 
    'NPOV': 'Neutral Point of View',
    'NOR': 'No Original Research',
    'RS': 'Reliable Sources',
    'V': 'Verifiability',
    'WEIGHT': 'Due Weight',
    'SPAM': 'Spam',
    'VAND': 'Vandalism',
    'RV': 'Revert',
    'CSD': 'Criteria for Speedy Deletion'
}

all_text = soup.get_text().lower()
found_policies = {}

for abbrev, full_name in common_policies.items():
    if abbrev.lower() in all_text or full_name.lower() in all_text:
        # Count occurrences and find context
        abbrev_count = all_text.count(abbrev.lower())
        name_count = all_text.count(full_name.lower())
        
        found_policies[abbrev] = {
            'full_name': full_name,
            'abbrev_count': abbrev_count,
            'name_count': name_count,
            'total_mentions': abbrev_count + name_count,
            'contains_r': 'R' in abbrev
        }
        
        print(f"{abbrev} ({full_name}): {abbrev_count + name_count} mentions (Contains R: {'R' in abbrev})")

print(f"\nTotal unique policies found: {len(found_policies)}")

# Look for "three core policies" specifically
print("\n=== SEARCHING FOR THREE CORE POLICIES REFERENCE ===\n")

# Wikipedia's three core content policies are typically:
# 1. Neutral Point of View (NPOV)
# 2. Verifiability (V)
# 3. No Original Research (NOR)

core_policies_patterns = [
    r'three\s+core\s+polic[iy]',
    r'three\s+content\s+polic[iy]', 
    r'three\s+fundamental\s+polic[iy]',
    r'three\s+main\s+polic[iy]',
    r'npov.*verif.*research',
    r'verif.*npov.*research',
    r'neutral.*verif.*original'
]

for pattern in core_policies_patterns:
    matches = re.finditer(pattern, all_text, re.IGNORECASE | re.DOTALL)
    for match in matches:
        start_pos = max(0, match.start() - 300)
        end_pos = min(len(all_text), match.end() + 300)
        context = all_text[start_pos:end_pos]
        
        print(f"Three core policies reference found:")
        print(f"Pattern: {pattern}")
        print(f"Match: {match.group()}")
        print(f"Context: ...{context}...")
        print()

# Save comprehensive results
final_results = {
    'research_target': 'Legume Wikipedia content violations 2022 (before December)',
    'analysis_method': 'Deep edit history parsing',
    'edit_entries_analyzed': len(edit_entries),
    'violation_entries_found': len(violation_entries),
    'flagged_violations': violation_entries,
    'policy_abbreviations_found': found_policies,
    'r_containing_policies': {k: v for k, v in found_policies.items() if 'R' in k},
    'summary': {
        'total_policies_identified': len(found_policies),
        'policies_with_r': len([k for k in found_policies.keys() if 'R' in k]),
        'potential_violation_entries': len(violation_entries)
    }
}

with open(f'{workspace_dir}/legume_deep_violation_analysis.json', 'w') as f:
    json.dump(final_results, f, indent=2, default=str)

print(f"\n=== DEEP ANALYSIS COMPLETE ===\n")
print(f"Results saved to: {workspace_dir}/legume_deep_violation_analysis.json")
print(f"Violation entries identified: {len(violation_entries)}")
print(f"Policy abbreviations found: {len(found_policies)}")
print(f"Policies containing 'R': {[k for k in found_policies.keys() if 'R' in k]}")
print(f"\nKey findings will be summarized in next analysis step.")
```

### Development Step 7: Legume Wikipedia 2022 Logs: Identify Violated Content Type and Define “R” in Core Policies

**Description**: Search for information about the Legume Wikipedia page and identify what content violations occurred in its public logs during 2022 before December. Focus on finding the specific type of content that was violated and the associated three core policies, particularly identifying what 'R' stands for in those policies.

**Use Cases**:
- Nonprofit Wikipedia oversight reporting: Volunteers automate extraction of 2022 content violations on the Legume page to create training materials that improve community guideline compliance.
- Media fact‐checking workflow: A newsroom integrates the solution to flag policy‐violating edits on botanical topics before December 2022 as part of their verification pipeline.
- Corporate knowledge management audit: An enterprise mirrors public Wikipedia logs into its internal wiki and uses this code to detect and remove content that breaches core policy standards.
- Academic research on online governance: Scholars parse violation incidents and policy interpretations from Legume’s logs to quantify trends in user‐generated content moderation for a peer‐reviewed study.
- AI training data curation: A machine learning engineer filters out any text from pre‐December 2022 Wikipedia dumps that violated core policies, ensuring only reliable, policy‐compliant data is used.
- Digital archival quality audit: A library’s digital preservation team runs the script on archived Wikipedia snapshots to verify adherence to NPOV, Verifiability, and No Original Research policies.
- Legal risk assessment: A consultancy analyzes public log violations for trademark or defamation risks on the Legume page, advising clients on potential exposure from user edits.

```
import os
import json

print("=== FINAL RESULTS REVIEW: LEGUME WIKIPEDIA CONTENT VIOLATIONS ===\n")
print("Objective: Extract complete findings from final analysis file to answer PLAN questions\n")

# Locate workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("No workspace directory found.")
    exit()

workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Load the final analysis file
final_analysis_file = f'{workspace_dir}/legume_final_violation_analysis.json'
if not os.path.exists(final_analysis_file):
    print(f"Final analysis file not found: {final_analysis_file}")
    exit()

print(f"Loading final analysis file: {os.path.basename(final_analysis_file)}")
file_size = os.path.getsize(final_analysis_file)
print(f"File size: {file_size:,} bytes\n")

# First inspect the file structure
with open(final_analysis_file, 'r') as f:
    final_data = json.load(f)

print("=== FINAL ANALYSIS FILE STRUCTURE INSPECTION ===\n")
print("Top-level keys:")
for key, value in final_data.items():
    if isinstance(value, dict):
        print(f"  {key}: Dictionary with {len(value)} keys")
        for nested_key, nested_value in value.items():
            if isinstance(nested_value, list):
                print(f"    {nested_key}: List with {len(nested_value)} items")
            elif isinstance(nested_value, dict):
                print(f"    {nested_key}: Dictionary with {len(nested_value)} keys")
            else:
                print(f"    {nested_key}: {str(nested_value)[:100]}...")
    elif isinstance(value, list):
        print(f"  {key}: List with {len(value)} items")
    else:
        print(f"  {key}: {value}")

print("\n=== EXTRACTING ANSWERS TO PLAN QUESTIONS ===\n")

# Question 1: What content violations occurred in 2022 before December?
print("1. CONTENT VIOLATIONS IN 2022 (BEFORE DECEMBER):")
if 'violation_incidents_2022' in final_data:
    incidents = final_data['violation_incidents_2022']
    print(f"   Total incidents found: {len(incidents)}")
    
    if incidents:
        print("   Incident details:")
        for i, incident in enumerate(incidents[:5], 1):  # Show first 5
            print(f"     {i}. Source: {incident.get('source_file', 'Unknown')}")
            if 'match' in incident:
                print(f"        Match: {incident['match'][:150]}...")
            print(f"        Context: {incident.get('context', 'N/A')[:200]}...")
            print()
    else:
        print("   No specific violation incidents found in the data.")
else:
    print("   No violation incidents data found.")

# Question 2: What are the three core policies?
print("\n2. THREE CORE POLICIES IDENTIFIED:")
if 'three_core_policies_identified' in final_data:
    core_policies = final_data['three_core_policies_identified']
    print(f"   Policies found: {len(core_policies)}")
    
    for i, policy in enumerate(core_policies, 1):
        print(f"     {i}. {policy}")
    
    # Add Wikipedia's standard three core policies context
    print("\n   Wikipedia's three core content policies are typically:")
    print("     1. Neutral Point of View (NPOV)")
    print("     2. Verifiability (V)")
    print("     3. No Original Research (NOR)")
    
    missing_policies = []
    if 'NPOV (Neutral Point of View)' not in core_policies:
        missing_policies.append('NPOV (Neutral Point of View)')
    if 'V (Verifiability)' not in core_policies:
        missing_policies.append('V (Verifiability)')
    if 'NOR (No Original Research)' not in core_policies:
        missing_policies.append('NOR (No Original Research)')
    
    if missing_policies:
        print(f"\n   Missing from our analysis: {missing_policies}")
else:
    print("   No core policies data found.")

# Question 3: What does 'R' stand for in the policies?
print("\n3. WHAT 'R' STANDS FOR IN THE POLICIES:")
if 'r_meaning_analysis' in final_data:
    r_analysis = final_data['r_meaning_analysis']
    
    if 'most_likely_meanings' in r_analysis:
        print("   Most likely meanings:")
        for meaning in r_analysis['most_likely_meanings']:
            print(f"     - {meaning}")
    
    if 'policies_with_r' in r_analysis:
        print(f"\n   Policies containing 'R': {r_analysis['policies_with_r']}")
    
    if 'conclusion' in r_analysis:
        print(f"\n   Conclusion: {r_analysis['conclusion']}")
else:
    print("   No 'R' meaning analysis found.")

# Summary of findings
print("\n=== COMPREHENSIVE SUMMARY FOR PLAN COMPLETION ===\n")

if 'analysis_summary' in final_data:
    summary = final_data['analysis_summary']
    print("Analysis Statistics:")
    print(f"  - Total Wikipedia policies found: {summary.get('policies_found', 'N/A')}")
    print(f"  - Policies containing 'R': {summary.get('r_policies_found', 'N/A')}")
    print(f"  - Core policies identified: {summary.get('core_policies_identified', 'N/A')}")
    print(f"  - Violation incidents found: {summary.get('violation_incidents', 'N/A')}")

print("\n=== PLAN COMPLETION STATUS ===\n")
print("✓ Successfully accessed Legume Wikipedia page and related logs")
print("✓ Identified Wikipedia policy abbreviations and references")
print("✓ Found policies containing 'R' (NOR, RS, RV)")
print("✓ Determined 'R' most likely stands for 'Research' or 'Reliable'")
print("✓ Located violation incidents from 2022 before December")
print("✓ Identified components of Wikipedia's three core content policies")

print("\nFINAL ANSWERS:")
print("1. Content violations: Found 7 incidents in 2022 before December")
print("2. Three core policies: NPOV (Neutral Point of View), V (Verifiability), NOR (No Original Research)")
print("3. 'R' stands for: RESEARCH (from 'No Original Research' - NOR) or RELIABLE (from 'Reliable Sources' - RS)")

print(f"\nComplete analysis results saved in: {workspace_dir}/legume_final_violation_analysis.json")
print("\n=== LEGUME WIKIPEDIA CONTENT VIOLATIONS ANALYSIS COMPLETE ===")
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

## Created Time
2025-08-11 09:13:09
