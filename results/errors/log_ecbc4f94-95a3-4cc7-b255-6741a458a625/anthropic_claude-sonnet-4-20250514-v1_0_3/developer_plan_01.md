# Developer Plan 01

## Plan
Search for and access the latest version of the 'Lego' Wikipedia article from 2022 on English Wikipedia. Extract the complete page content and systematically count all images present in the article, including inline images, gallery images, infobox images, and any other visual media elements. Identify each image by analyzing the page's HTML structure, wikitext markup, or API response to provide an accurate total count of images in the 2022 version of the Lego Wikipedia page.

## Description
This is the optimal starting approach because: (1) We need to locate the specific 2022 version of the Lego Wikipedia article to establish the correct baseline for image counting, (2) No previous research has been conducted on this image analysis task, (3) Expected outcome is to access the 2022 Lego Wikipedia page content and extract comprehensive image data from all sections, (4) This directly addresses the TASK requirement to count all images present in the latest 2022 version of the English Wikipedia Lego article.

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

### Development Step 2: Legume Wikipedia 2022 Content Violations: Identify Violated Content, Core Policies, ‘R’ Definition

**Description**: Search for information about the Legume Wikipedia page and identify what content violations occurred in its public logs during 2022 before December. Focus on finding the specific type of content that was violated and the associated three core policies, particularly identifying what 'R' stands for in those policies.

**Use Cases**:
- Automated moderation workflow for agricultural wiki: scan the 2022 edit history of the “Legume” article to flag violations of Neutral Point of View, Verifiability, and “R” (Reliable sourcing) policies and alert community administrators.
- Academic research on content censorship: analyze public logs from January–November 2022 for the Legume page to quantify removals of unsourced material and correlate them with the three core Wikipedia policies in a peer-reviewed study.
- Corporate intranet documentation audit: apply the HTML/JSON inspection pipeline to internal policy pages, detect unauthorized removals or reverts, and enforce company information governance standards after each quarterly review.
- Digital preservation tool for libraries: monitor policy breaches and vandalism on taxonomy and species articles, record every content removal incident through 2022, and archive original revisions for long-term access.
- Investigative journalism dashboard: ingest Wikipedia edit histories for high-traffic science pages (e.g., Legume) to identify sudden spikes in “removed” or “vandalism” mentions during key events and support data-driven reporting.
- NGO transparency reporting: track policy infractions across public knowledge platforms, generate monthly summaries of content violations in agricultural entries, and publish compliance metrics for donors and stakeholders.
- Government open-data monitoring: continuously inspect municipal and environmental wiki pages for unauthorized edits or policy violations, trigger security tickets for high-priority incidents, and maintain public trust in service documentation.

```
import os
import json

print("=== WORKSPACE INSPECTION FOR LEGUME VIOLATION ANALYSIS ===\n")
print("Objective: Inspect downloaded files and understand their structure before detailed parsing\n")

# Check workspace directory structure
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
print(f"Workspace directories found: {workspace_dirs}")

# Use the most recent workspace directory
if workspace_dirs:
    workspace_dir = workspace_dirs[0]  # Should be the one from previous execution
    print(f"Using workspace directory: {workspace_dir}\n")
    
    # List all files in workspace
    workspace_files = os.listdir(workspace_dir)
    print(f"Files in workspace ({len(workspace_files)} total):")
    
    for file in workspace_files:
        file_path = os.path.join(workspace_dir, file)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            print(f"  - {file} ({file_size:,} bytes)")
    
    print()  # Empty line
    
    # First, inspect the JSON analysis file to understand what was found
    json_files = [f for f in workspace_files if f.endswith('.json')]
    print(f"=== JSON ANALYSIS FILES ({len(json_files)}) ===\n")
    
    for json_file in json_files:
        json_path = os.path.join(workspace_dir, json_file)
        print(f"Inspecting: {json_file}")
        
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        print("Top-level keys:")
        for key, value in data.items():
            if isinstance(value, list):
                print(f"  {key}: List with {len(value)} items")
            elif isinstance(value, dict):
                print(f"  {key}: Dictionary with {len(value)} keys")
            else:
                print(f"  {key}: {value}")
        
        # Show sources_data structure if present
        if 'sources_data' in data and data['sources_data']:
            print("\n  sources_data sample (first source):")
            first_source = data['sources_data'][0]
            for key, value in first_source.items():
                if isinstance(value, list) and len(value) > 5:
                    print(f"    {key}: List with {len(value)} items - First 5: {value[:5]}")
                else:
                    print(f"    {key}: {value}")
        
        print()  # Empty line
    
    # Now inspect HTML files
    html_files = [f for f in workspace_files if f.endswith('.html')]
    print(f"=== HTML FILES ANALYSIS ({len(html_files)}) ===\n")
    
    for html_file in html_files:
        html_path = os.path.join(workspace_dir, html_file)
        file_size = os.path.getsize(html_path)
        
        print(f"HTML File: {html_file}")
        print(f"Size: {file_size:,} bytes")
        
        # Determine what type of page this is based on filename
        if 'talk' in html_file.lower():
            page_type = "TALK PAGE - May contain policy discussions"
        elif 'history' in html_file.lower():
            page_type = "EDIT HISTORY - May contain violation records"
        elif 'legume' in html_file.lower() and 'talk' not in html_file.lower() and 'history' not in html_file.lower():
            page_type = "MAIN ARTICLE - Current content"
        else:
            page_type = "UNKNOWN PAGE TYPE"
        
        print(f"Type: {page_type}")
        
        # Quick content preview (first few lines)
        with open(html_path, 'r', encoding='utf-8') as f:
            first_lines = []
            for i in range(3):
                line = f.readline().strip()
                if line:
                    first_lines.append(line)
        
        print("Preview (first 3 non-empty lines):")
        for i, line in enumerate(first_lines, 1):
            preview = line[:100] + "..." if len(line) > 100 else line
            print(f"  {i}: {preview}")
        
        # Check for key indicators in file
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content_lower = content.lower()
        
        # Key indicators to look for
        key_indicators = {
            '2022_references': content_lower.count('2022'),
            'policy_mentions': content_lower.count('policy'),
            'violation_mentions': content_lower.count('violation'),
            'revert_mentions': content_lower.count('revert'),
            'december_mentions': content_lower.count('december'),
            'november_mentions': content_lower.count('november'),
            'october_mentions': content_lower.count('october'),
            'content_removal': content_lower.count('removed'),
            'vandalism_mentions': content_lower.count('vandalism')
        }
        
        print("Key indicator counts:")
        for indicator, count in key_indicators.items():
            if count > 0:
                print(f"  {indicator}: {count}")
        
        # Determine priority for analysis
        priority_score = sum([count for count in key_indicators.values()])
        print(f"Priority score: {priority_score}")
        
        if priority_score > 10:
            print("  *** HIGH PRIORITY - Contains many relevant indicators ***")
        elif priority_score > 5:
            print("  *** MEDIUM PRIORITY - Contains some relevant indicators ***")
        else:
            print("  Low priority - Few relevant indicators")
        
        print()  # Empty line
    
    # Summary and next steps
    print("=== INSPECTION SUMMARY ===\n")
    print(f"Workspace directory: {workspace_dir}")
    print(f"Total files: {len(workspace_files)}")
    print(f"JSON files: {len(json_files)}")
    print(f"HTML files: {len(html_files)}")
    
    # Identify which file to analyze first
    if html_files:
        print("\nRecommended analysis order:")
        print("1. Edit history page - Most likely to contain violation records")
        print("2. Talk page - May contain policy discussions")
        print("3. Main article - For context")
    
else:
    print("No workspace directories found. Need to re-run data collection.")

print("\n=== INSPECTION COMPLETE ===\nNext: Parse HTML files for specific content violations and policy information")
```

## Created Time
2025-08-14 02:07:33
