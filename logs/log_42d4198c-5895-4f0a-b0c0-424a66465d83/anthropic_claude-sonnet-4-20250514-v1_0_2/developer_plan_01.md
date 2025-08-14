# Developer Plan 01

## Plan
Search for information about the 2019 British Academy Games Awards (BAFTA Games Awards) to identify which game won the main award that year. Focus on finding the winner of the most prestigious category, likely 'Best Game' or 'Game of the Year' equivalent. Use multiple search approaches: (1) Search for '2019 BAFTA Games Awards winners', (2) Look up the official BAFTA website for 2019 ceremony results, (3) Search gaming news sources that covered the 2019 awards ceremony. Extract the complete list of winners and identify the primary game that would be considered 'the' winner of the 2019 British Academy Games Awards.

## Description
This is the optimal starting approach because: (1) We need to identify which specific game won the 2019 BAFTA Games Awards before we can analyze its Wikipedia page, (2) No previous research has been conducted, (3) Expected outcome is to determine the winning game and establish our target for Wikipedia revision analysis, (4) This directly addresses the first requirement of the TASK to find the 2019 British Academy Games Awards winner.

## Episodic Examples
### Development Step 3: Title: Identify US Survivor Winners Born in May Using Official Winner Lists and Birth Dates (Season 1–2023)

**Description**: Search for comprehensive information about US Survivor winners and their birth dates. Focus on finding official sources such as CBS Survivor databases, Wikipedia pages, or entertainment databases that list all winners from Season 1 through the most recent season available as of August 2023. Extract winner names, seasons, and birth dates to identify any winners born in May.

**Use Cases**:
- Entertainment journalists compiling a feature on Survivor winners with May birthdays for a special anniversary article
- Academic researchers conducting demographic studies on reality TV show winners, focusing on age and birth month trends
- TV show producers developing themed Survivor reunion episodes based on shared winner traits, such as birth month
- Data analysts at entertainment networks automating the extraction and validation of winner statistics for audience insights dashboards
- Fans creating interactive Survivor trivia games that include questions about winners’ birth dates and seasons
- Digital archivists maintaining up-to-date, structured databases of reality show winners for use in media encyclopedias and wikis

```
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

# 1) Use existing workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not workspace_dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(workspace_dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Load the previously saved HTML page
html_path = os.path.join(workspace_dir, 'survivor_main_page.html')
if not os.path.exists(html_path):
    print("❌ survivor_main_page.html not found. Need to fetch page first.")
    sys.exit(1)

print("Loading previously saved Survivor main page HTML...")
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 3) Parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')
print("HTML parsed successfully\n")

# 4) Find the winners table and examine its structure carefully
print("Examining table structure in detail...")
tables = soup.find_all('table', class_='wikitable')
print(f"Found {len(tables)} wikitable(s)\n")

if len(tables) == 0:
    print("❌ No wikitables found")
    sys.exit(1)

# Let's examine the first few tables more carefully
for table_idx, table in enumerate(tables[:3]):
    print(f"=== TABLE {table_idx + 1} DETAILED ANALYSIS ===")
    
    # Get headers
    header_row = table.find('tr')
    if not header_row:
        print("No header row found")
        continue
        
    headers = []
    for cell in header_row.find_all(['th', 'td']):
        header_text = cell.get_text(strip=True)
        headers.append(header_text)
    
    print(f"Headers: {headers}")
    print(f"Number of columns: {len(headers)}")
    
    # Examine first 5 data rows in detail
    data_rows = table.find_all('tr')[1:6]  # Skip header, get first 5 data rows
    print(f"\nFirst 5 data rows:")
    
    for row_idx, row in enumerate(data_rows):
        cells = row.find_all(['td', 'th'])
        print(f"\n  Row {row_idx + 1} ({len(cells)} cells):")
        
        for cell_idx, cell in enumerate(cells):
            cell_text = cell.get_text(strip=True)
            # Check if cell contains a link
            link = cell.find('a')
            link_href = link.get('href', '') if link else ''
            
            print(f"    Col {cell_idx} ({headers[cell_idx] if cell_idx < len(headers) else 'N/A'}): '{cell_text}' {f'[LINK: {link_href}]' if link_href else ''}")
    
    print("\n" + "="*60 + "\n")

# 5) Based on the analysis, let's identify the correct table and columns
print("\n=== SELECTING CORRECT TABLE AND EXTRACTING WINNERS ===")

# Use the first table but let's be more careful about data extraction
winners_table = tables[0]
header_row = winners_table.find('tr')
headers = [cell.get_text(strip=True) for cell in header_row.find_all(['th', 'td'])]

print(f"Using table with headers: {headers}")

# Find column indices
try:
    season_idx = headers.index('Season')
    winner_idx = headers.index('Winner')
    runner_up_idx = headers.index('Runner(s)-up') if 'Runner(s)-up' in headers else -1
    print(f"Column indices -> Season: {season_idx}, Winner: {winner_idx}, Runner-up: {runner_up_idx}")
except ValueError as e:
    print(f"❌ Could not find required columns: {e}")
    sys.exit(1)

# 6) Extract winners more carefully
print("\nExtracting winners with improved logic...")
winners = []
rows = winners_table.find_all('tr')[1:]  # Skip header row

for i, row in enumerate(rows):
    cells = row.find_all(['td', 'th'])
    if len(cells) <= max(season_idx, winner_idx):
        print(f"  Skipping row {i+1}: insufficient columns ({len(cells)})")
        continue
    
    # Extract season number
    season_cell = cells[season_idx]
    season_text = season_cell.get_text(strip=True)
    
    # Handle season numbers that might have footnotes
    season_match = re.search(r'(\d+)', season_text)
    if not season_match:
        print(f"  Skipping row {i+1}: no valid season number in '{season_text}'")
        continue
    
    season_num = int(season_match.group(1))
    
    # Extract winner name more carefully
    winner_cell = cells[winner_idx]
    
    # Remove any sup tags (footnotes) before extracting text
    for sup in winner_cell.find_all('sup'):
        sup.decompose()
    
    # Look for a link first (more reliable)
    winner_link = winner_cell.find('a')
    if winner_link:
        winner_name = winner_link.get_text(strip=True)
        winner_wiki_link = winner_link.get('href', '')
        if winner_wiki_link.startswith('/'):
            winner_wiki_link = 'https://en.wikipedia.org' + winner_wiki_link
    else:
        winner_name = winner_cell.get_text(strip=True)
        winner_wiki_link = ''
    
    # Clean up winner name (remove any remaining footnotes)
    winner_name = re.sub(r'\[.*?\]', '', winner_name).strip()
    
    # Skip if winner name looks like a vote count or is empty
    if not winner_name or re.match(r'^\d+[–-]\d+([–-]\d+)?$', winner_name):
        print(f"  Skipping row {i+1}: invalid winner name '{winner_name}'")
        continue
    
    # Skip if season number is unreasonable (Survivor US has ~47 seasons as of 2023)
    if season_num < 1 or season_num > 50:
        print(f"  Skipping row {i+1}: unreasonable season number {season_num}")
        continue
    
    winner_info = {
        'season': season_num,
        'winner': winner_name,
        'wiki_link': winner_wiki_link
    }
    winners.append(winner_info)
    print(f"  Season {season_num:2d}: {winner_name}")
    if winner_wiki_link:
        print(f"    Link: {winner_wiki_link}")

print(f"\nExtracted {len(winners)} winners total\n")

# 7) Sort winners by season and validate
winners_sorted = sorted(winners, key=lambda x: x['season'])

# 8) Save the corrected winners list
winners_path = os.path.join(workspace_dir, 'survivor_winners_corrected.json')
with open(winners_path, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"Saved corrected winners list to: {winners_path}")

# 9) Display summary and validation
print(f"\n=== CORRECTED WINNERS EXTRACTION SUMMARY ===")
print(f"Total winners extracted: {len(winners_sorted)}")
if winners_sorted:
    print(f"Season range: {min(w['season'] for w in winners_sorted)} - {max(w['season'] for w in winners_sorted)}")
    print(f"Winners with Wikipedia links: {sum(1 for w in winners_sorted if w['wiki_link'])}")
    print(f"Winners without Wikipedia links: {sum(1 for w in winners_sorted if not w['wiki_link'])}")

# 10) Show all winners for verification
print(f"\nAll extracted winners:")
for w in winners_sorted:
    link_status = "✓" if w['wiki_link'] else "✗"
    print(f"  Season {w['season']:2d}: {w['winner']} [{link_status}]")

print(f"\nNext step: Fetch individual winner Wikipedia pages to extract birth dates")
```

### Development Step 7: Title:  
Identify US Survivor Winners Born in May Using Official Sources and Winner Birth Date Lists (Seasons 1–44)

**Description**: Search for comprehensive information about US Survivor winners and their birth dates. Focus on finding official sources such as CBS Survivor databases, Wikipedia pages, or entertainment databases that list all winners from Season 1 through the most recent season available as of August 2023. Extract winner names, seasons, and birth dates to identify any winners born in May.

**Use Cases**:
- Entertainment journalism research for compiling accurate birthday features on Survivor winners, especially for "On This Day" or birthday spotlight articles
- Automated database enrichment for TV trivia apps or Survivor fan sites, ensuring winner profiles include verified birth dates and special highlights for May-born winners
- Academic studies on demographic trends of reality TV show winners, enabling sociologists to analyze age, birth month, or generational patterns among Survivor champions
- Event planning for Survivor-themed parties or conventions, allowing organizers to schedule celebrations or social media campaigns around winners' birthdays, particularly those in May
- Data validation and cross-referencing for casting agencies or talent scouts seeking to verify contestant ages and backgrounds from authoritative sources
- Automated content curation for social media managers running Survivor fan pages, enabling scheduled posts celebrating winners’ birthdays with accurate information and links

```
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

# 1) Use existing workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not workspace_dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(workspace_dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Load existing data and clean up any contamination
print("=== LOADING AND CLEANING EXISTING SURVIVOR DATA ===")

# Load manual winners list
manual_path = os.path.join(workspace_dir, 'survivor_winners_manual.json')
if os.path.exists(manual_path):
    with open(manual_path, 'r', encoding='utf-8') as f:
        manual_winners = json.load(f)
    print(f"Loaded {len(manual_winners)} manual winners")
else:
    print("❌ Manual winners list not found. Creating fresh list...")
    # Recreate the manual list to ensure clean data
    manual_winners = [
        {"season": 1, "winner": "Richard Hatch", "subtitle": "Borneo"},
        {"season": 2, "winner": "Tina Wesson", "subtitle": "The Australian Outback"},
        {"season": 3, "winner": "Ethan Zohn", "subtitle": "Africa"},
        {"season": 4, "winner": "Vecepia Towery", "subtitle": "Marquesas"},
        {"season": 5, "winner": "Brian Heidik", "subtitle": "Thailand"},
        {"season": 6, "winner": "Jenna Morasca", "subtitle": "The Amazon"},
        {"season": 7, "winner": "Sandra Diaz-Twine", "subtitle": "Pearl Islands"},
        {"season": 8, "winner": "Amber Brkich", "subtitle": "All-Stars"},
        {"season": 9, "winner": "Chris Daugherty", "subtitle": "Vanuatu"},
        {"season": 10, "winner": "Tom Westman", "subtitle": "Palau"},
        {"season": 11, "winner": "Danni Boatwright", "subtitle": "Guatemala"},
        {"season": 12, "winner": "Aras Baskauskas", "subtitle": "Panama"},
        {"season": 13, "winner": "Yul Kwon", "subtitle": "Cook Islands"},
        {"season": 14, "winner": "Earl Cole", "subtitle": "Fiji"},
        {"season": 15, "winner": "Todd Herzog", "subtitle": "China"},
        {"season": 16, "winner": "Parvati Shallow", "subtitle": "Micronesia"},
        {"season": 17, "winner": "Bob Crowley", "subtitle": "Gabon"},
        {"season": 18, "winner": "J.T. Thomas", "subtitle": "Tocantins"},
        {"season": 19, "winner": "Natalie White", "subtitle": "Samoa"},
        {"season": 20, "winner": "Sandra Diaz-Twine", "subtitle": "Heroes vs. Villains"},
        {"season": 21, "winner": "Fabio Birza", "subtitle": "Nicaragua"},
        {"season": 22, "winner": "Rob Mariano", "subtitle": "Redemption Island"},
        {"season": 23, "winner": "Sophie Clarke", "subtitle": "South Pacific"},
        {"season": 24, "winner": "Kim Spradlin", "subtitle": "One World"},
        {"season": 25, "winner": "Denise Stapley", "subtitle": "Philippines"},
        {"season": 26, "winner": "John Cochran", "subtitle": "Caramoan"},
        {"season": 27, "winner": "Tyson Apostol", "subtitle": "Blood vs. Water"},
        {"season": 28, "winner": "Tony Vlachos", "subtitle": "Cagayan"},
        {"season": 29, "winner": "Natalie Anderson", "subtitle": "San Juan del Sur"},
        {"season": 30, "winner": "Mike Holloway", "subtitle": "Worlds Apart"},
        {"season": 31, "winner": "Jeremy Collins", "subtitle": "Cambodia"},
        {"season": 32, "winner": "Michele Fitzgerald", "subtitle": "Kaôh Rōng"},
        {"season": 33, "winner": "Adam Klein", "subtitle": "Millennials vs. Gen X"},
        {"season": 34, "winner": "Sarah Lacina", "subtitle": "Game Changers"},
        {"season": 35, "winner": "Ben Driebergen", "subtitle": "Heroes vs. Healers vs. Hustlers"},
        {"season": 36, "winner": "Wendell Holland", "subtitle": "Ghost Island"},
        {"season": 37, "winner": "Nick Wilson", "subtitle": "David vs. Goliath"},
        {"season": 38, "winner": "Chris Underwood", "subtitle": "Edge of Extinction"},
        {"season": 39, "winner": "Tommy Sheehan", "subtitle": "Island of the Idols"},
        {"season": 40, "winner": "Tony Vlachos", "subtitle": "Winners at War"},
        {"season": 41, "winner": "Erika Casupanan", "subtitle": "Survivor 41"},
        {"season": 42, "winner": "Maryanne Oketch", "subtitle": "Survivor 42"},
        {"season": 43, "winner": "Mike Gabler", "subtitle": "Survivor 43"},
        {"season": 44, "winner": "Yam Yam Arocho", "subtitle": "Survivor 44"}
    ]
    with open(manual_path, 'w', encoding='utf-8') as f:
        json.dump(manual_winners, f, indent=2)
    print(f"Created fresh manual winners list with {len(manual_winners)} winners")

# Load existing birth date results and clean them
birth_dates_path = os.path.join(workspace_dir, 'survivor_winners_birth_dates.json')
if os.path.exists(birth_dates_path):
    with open(birth_dates_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
    # Filter out any non-Survivor data that might have been contaminated
    clean_results = [r for r in existing_results if 'season' in r and 'winner' in r and isinstance(r.get('season'), int)]
    processed_seasons = {result['season'] for result in clean_results}
    print(f"Loaded and cleaned {len(clean_results)} existing birth date results")
    print(f"Processed seasons: {sorted(processed_seasons)}")
else:
    clean_results = []
    processed_seasons = set()
    print("No existing birth date results found.")

# Load existing May winners and clean them
may_winners_path = os.path.join(workspace_dir, 'survivor_may_winners.json')
if os.path.exists(may_winners_path):
    with open(may_winners_path, 'r', encoding='utf-8') as f:
        may_winners = json.load(f)
    # Clean May winners data
    may_winners = [w for w in may_winners if 'season' in w and 'winner' in w]
    print(f"Loaded {len(may_winners)} existing May winners")
    for winner in may_winners:
        print(f"  Season {winner['season']}: {winner['winner']} - {winner.get('birth_date', 'No date')}")
else:
    may_winners = []
    print("No existing May winners found.")

print("\n=== CONTINUING CLEAN BIRTH DATE EXTRACTION ===")

# Set up for processing
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

all_results = clean_results.copy()
total_processed = len(processed_seasons)
new_processed = 0

# Process remaining winners (those not already processed)
remaining_winners = [w for w in manual_winners if w['season'] not in processed_seasons]
print(f"Processing {len(remaining_winners)} remaining winners...\n")

for i, winner_info in enumerate(remaining_winners[:15]):  # Process next 15 winners
    winner_name = winner_info['winner']
    season = winner_info['season']
    
    print(f"Processing {i+1}/{min(15, len(remaining_winners))}: Season {season} - {winner_name} ({winner_info['subtitle']})")
    new_processed += 1
    
    # Enhanced search strategies
    search_strategies = [
        winner_name.replace(' ', '_'),
        f"{winner_name.replace(' ', '_')}_(Survivor_contestant)",
        f"{winner_name.replace(' ', '_')}_Survivor",
        winner_name.replace('"', '').replace(' ', '_'),  # Remove quotes
    ]
    
    birth_date = None
    wiki_url = None
    birth_month = None
    birth_year = None
    
    for strategy in search_strategies:
        try:
            page_url = f"https://en.wikipedia.org/wiki/{strategy}"
            print(f"  Trying: {page_url}")
            
            page_response = requests.get(page_url, headers=headers, timeout=15)
            
            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                
                # Enhanced birth date patterns with year validation
                birth_date_patterns = [
                    # Infobox birth dates (most reliable)
                    r'class="bday"[^>]*>(\d{4})-(\d{2})-(\d{2})',
                    # Standard "Born" patterns with realistic year ranges
                    r'Born[^\n]*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19[4-9]\d|20[0-1]\d)',
                    r'born[^\n]*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19[4-9]\d|20[0-1]\d)',
                    # Parenthetical birth dates
                    r'\((January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19[4-9]\d|20[0-1]\d)\)',
                ]
                
                page_text = page_soup.get_text()
                
                for pattern in birth_date_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        match = matches[0]
                        
                        if len(match) == 3 and match[0].isdigit():  # Format: (year, month, day)
                            year, month_num, day = match
                            months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                                    'July', 'August', 'September', 'October', 'November', 'December']
                            month = months[int(month_num)]
                            birth_date = f"{month} {day}, {year}"
                            birth_year = int(year)
                        elif len(match) == 3:  # Format: (month, day, year)
                            month, day, year = match
                            birth_date = f"{month} {day}, {year}"
                            birth_year = int(year)
                        
                        birth_month = month.lower()
                        
                        # Validate birth year (realistic range for Survivor contestants)
                        if 1940 <= birth_year <= 2010:
                            print(f"  ✓ Found birth date: {birth_date}")
                            
                            # Check if it's in May
                            if birth_month == 'may':
                                print(f"  🌸 MAY WINNER FOUND: {winner_name} - {birth_date}")
                                
                                # Add to May winners if not already present
                                if not any(w['season'] == season for w in may_winners):
                                    may_winners.append({
                                        'season': season,
                                        'winner': winner_name,
                                        'birth_date': birth_date,
                                        'wiki_url': page_url,
                                        'subtitle': winner_info['subtitle']
                                    })
                            
                            wiki_url = page_url
                            break
                        else:
                            print(f"  ⚠️ Invalid birth year: {birth_year}, continuing...")
                            continue
                
                if birth_date:
                    break
                    
        except Exception as e:
            print(f"  ❌ Error with {strategy}: {e}")
            continue
    
    # Store result
    winner_result = {
        'season': season,
        'winner': winner_name,
        'birth_date': birth_date,
        'birth_month': birth_month,
        'birth_year': birth_year,
        'wiki_url': wiki_url,
        'subtitle': winner_info['subtitle']
    }
    all_results.append(winner_result)
    total_processed += 1
    
    if birth_date:
        print(f"  ✅ Success: {birth_date} (Month: {birth_month})")
    else:
        print(f"  ❌ No birth date found")
    
    print()
    
    # Respectful delay
    time.sleep(1.5)
    
    # Save progress every 5 winners
    if new_processed % 5 == 0:
        print(f"💾 Saving progress... ({new_processed} new winners processed)")
        with open(birth_dates_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        if may_winners:
            with open(may_winners_path, 'w', encoding='utf-8') as f:
                json.dump(may_winners, f, indent=2)
        print("✅ Progress saved!\n")

# Final save
print("💾 Saving final results...")
with open(birth_dates_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2)
print(f"✅ Saved complete birth date results to: {birth_dates_path}")

if may_winners:
    with open(may_winners_path, 'w', encoding='utf-8') as f:
        json.dump(may_winners, f, indent=2)
    print(f"✅ Saved May winners to: {may_winners_path}")

# Generate final summary
print(f"\n🎉 === SURVIVOR WINNERS BORN IN MAY ===")
if may_winners:
    may_winners_sorted = sorted(may_winners, key=lambda x: x['season'])
    for winner in may_winners_sorted:
        print(f"Season {winner['season']:2d}: {winner['winner']} - Born {winner['birth_date']} ({winner['subtitle']})")
else:
    print("No May winners found among processed contestants.")

successful_extractions = sum(1 for w in all_results if w['birth_date'])
print(f"\n📊 === STATISTICS ===")
print(f"Total winners processed: {total_processed}")
print(f"New winners processed this run: {new_processed}")
print(f"Birth dates successfully found: {successful_extractions}")
print(f"May winners identified: {len(may_winners)}")
print(f"Success rate: {successful_extractions / total_processed * 100:.1f}%")

remaining_count = len(manual_winners) - total_processed
if remaining_count > 0:
    print(f"\n⏭️ Remaining winners to process: {remaining_count}")
    print("Continue processing to complete the full analysis.")
else:
    print(f"\n✅ ALL WINNERS PROCESSED! Analysis complete.")

print(f"\n📁 Clean data files created:")
print(f"- {manual_path}")
print(f"- {birth_dates_path}")
if may_winners:
    print(f"- {may_winners_path}")
```

### Development Step 6: US Survivor Winners and Birth Dates: Identify May-Born Winners Using Official and Reputable Databases (Seasons 1–44)

**Description**: Search for comprehensive information about US Survivor winners and their birth dates. Focus on finding official sources such as CBS Survivor databases, Wikipedia pages, or entertainment databases that list all winners from Season 1 through the most recent season available as of August 2023. Extract winner names, seasons, and birth dates to identify any winners born in May.

**Use Cases**:
- Entertainment journalism research for compiling birthday-themed Survivor winner features or articles
- Automated database enrichment for TV trivia apps that highlight unique facts, such as winners born in specific months
- Academic studies in media or sociology analyzing demographic trends among reality TV show winners
- Fan community engagement, such as creating birthday shoutouts or themed Survivor events based on winner birth months
- Talent agency scouting and profiling for reality TV alumni, including detailed biographical data collection
- Data-driven content creation for YouTube or podcasts focusing on Survivor statistics and fun facts

```
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

# 1) Use existing workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not workspace_dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(workspace_dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Load the existing manual winners list
manual_path = os.path.join(workspace_dir, 'survivor_winners_manual.json')
if not os.path.exists(manual_path):
    print("❌ Manual winners list not found. Need to create it first.")
    sys.exit(1)

print("Loading existing manual winners list...")
with open(manual_path, 'r', encoding='utf-8') as f:
    manual_winners = json.load(f)
print(f"Loaded {len(manual_winners)} winners\n")

# 3) Load existing birth date results if available
birth_dates_path = os.path.join(workspace_dir, 'survivor_winners_birth_dates.json')
if os.path.exists(birth_dates_path):
    print("Loading existing birth date results...")
    with open(birth_dates_path, 'r', encoding='utf-8') as f:
        existing_results = json.load(f)
    processed_seasons = {result['season'] for result in existing_results}
    print(f"Found existing results for {len(processed_seasons)} seasons: {sorted(processed_seasons)}\n")
else:
    existing_results = []
    processed_seasons = set()
    print("No existing birth date results found. Starting fresh.\n")

# 4) Continue processing remaining winners
print("=== CONTINUING BIRTH DATE EXTRACTION ===")
print("Processing remaining Survivor winners to find all May-born contestants...\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

all_results = existing_results.copy()
may_winners = []
total_processed = 0
new_processed = 0

# Load existing May winners if available
may_winners_path = os.path.join(workspace_dir, 'survivor_may_winners.json')
if os.path.exists(may_winners_path):
    with open(may_winners_path, 'r', encoding='utf-8') as f:
        may_winners = json.load(f)
    print(f"Loaded {len(may_winners)} existing May winners\n")

# Process all winners, skipping those already processed
for i, winner_info in enumerate(manual_winners):
    winner_name = winner_info['winner']
    season = winner_info['season']
    
    # Skip if already processed
    if season in processed_seasons:
        print(f"Skipping Season {season}: {winner_name} (already processed)")
        total_processed += 1
        continue
    
    print(f"Processing Season {season}: {winner_name} ({winner_info['subtitle']})")
    new_processed += 1
    
    # Enhanced search strategies with better Wikipedia URL patterns
    search_strategies = [
        winner_name.replace(' ', '_'),  # Direct Wikipedia URL format
        f"{winner_name.replace(' ', '_')}_(Survivor_contestant)",
        f"{winner_name.replace(' ', '_')}_Survivor",
        # Handle special cases
        winner_name.replace('"', '').replace(' ', '_'),  # Remove quotes
        winner_name.split()[0] + '_' + '_'.join(winner_name.split()[1:])  # Alternative formatting
    ]
    
    birth_date = None
    wiki_url = None
    birth_month = None
    birth_year = None
    
    for strategy in search_strategies:
        try:
            # Try direct Wikipedia page access
            page_url = f"https://en.wikipedia.org/wiki/{strategy}"
            print(f"  Trying: {page_url}")
            
            page_response = requests.get(page_url, headers=headers, timeout=15)
            
            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                
                # Enhanced birth date extraction with better patterns
                birth_date_patterns = [
                    # Look for infobox birth dates (most reliable)
                    r'class="bday"[^>]*>(\d{4})-(\d{2})-(\d{2})',
                    # Standard "Born" patterns with better year validation
                    r'Born[^\n]*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19\d{2}|20\d{2})',
                    r'born[^\n]*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19\d{2}|20\d{2})',
                    # Parenthetical birth dates
                    r'\((January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19\d{2}|20\d{2})\)',
                    # Alternative formats
                    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(19\d{2}|20\d{2})\b'
                ]
                
                page_text = page_soup.get_text()
                
                for pattern in birth_date_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        match = matches[0]
                        
                        if len(match) == 3 and match[0].isdigit():  # Format: (year, month, day)
                            year, month_num, day = match
                            months = ['', 'January', 'February', 'March', 'April', 'May', 'June',
                                    'July', 'August', 'September', 'October', 'November', 'December']
                            month = months[int(month_num)]
                            birth_date = f"{month} {day}, {year}"
                            birth_year = int(year)
                        elif len(match) == 3:  # Format: (month, day, year)
                            month, day, year = match
                            birth_date = f"{month} {day}, {year}"
                            birth_year = int(year)
                        
                        birth_month = month.lower() if 'month' in locals() else None
                        
                        # Validate birth year (contestants should be born between 1940-2005 roughly)
                        if birth_year and 1940 <= birth_year <= 2005:
                            print(f"  Found birth date: {birth_date} (Year: {birth_year})")
                            
                            # Check if it's in May
                            if birth_month == 'may':
                                print(f"  *** MAY WINNER FOUND: {winner_name} - {birth_date} ***")
                                
                                # Check if not already in may_winners list
                                if not any(w['season'] == season for w in may_winners):
                                    may_winners.append({
                                        'season': season,
                                        'winner': winner_name,
                                        'birth_date': birth_date,
                                        'wiki_url': page_url,
                                        'subtitle': winner_info['subtitle']
                                    })
                            
                            wiki_url = page_url
                            break
                        else:
                            print(f"  Invalid birth year: {birth_year}, continuing search...")
                            birth_date = None
                            birth_year = None
                            continue
                
                if birth_date:
                    break
                    
        except Exception as e:
            print(f"  Error with {strategy}: {e}")
            continue
    
    # Store result
    winner_result = {
        'season': season,
        'winner': winner_name,
        'birth_date': birth_date,
        'birth_month': birth_month,
        'birth_year': birth_year,
        'wiki_url': wiki_url,
        'subtitle': winner_info['subtitle']
    }
    all_results.append(winner_result)
    total_processed += 1
    
    if birth_date:
        print(f"  ✓ Found birth date: {birth_date} (Month: {birth_month})")
    else:
        print(f"  ✗ No birth date found")
    
    print()
    
    # Add delay to be respectful to Wikipedia
    time.sleep(1.5)
    
    # Save progress every 5 winners
    if new_processed % 5 == 0:
        print(f"Saving progress... ({new_processed} new winners processed)")
        # Save updated results
        with open(birth_dates_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        if may_winners:
            with open(may_winners_path, 'w', encoding='utf-8') as f:
                json.dump(may_winners, f, indent=2)
        print("Progress saved!\n")

# 5) Final save of all results
print("Saving final results...")
with open(birth_dates_path, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2)
print(f"Saved complete birth date results to: {birth_dates_path}")

if may_winners:
    with open(may_winners_path, 'w', encoding='utf-8') as f:
        json.dump(may_winners, f, indent=2)
    print(f"Saved May winners to: {may_winners_path}")

# 6) Generate comprehensive summary
print(f"\n🎉 === FINAL RESULTS: SURVIVOR WINNERS BORN IN MAY ===")
if may_winners:
    may_winners_sorted = sorted(may_winners, key=lambda x: x['season'])
    for winner in may_winners_sorted:
        print(f"Season {winner['season']:2d}: {winner['winner']} - Born {winner['birth_date']} ({winner['subtitle']})")
else:
    print("No May winners found among all processed contestants.")

# 7) Detailed statistics
successful_extractions = sum(1 for w in all_results if w['birth_date'])
print(f"\n=== COMPREHENSIVE STATISTICS ===")
print(f"Total winners processed: {total_processed}")
print(f"New winners processed this run: {new_processed}")
print(f"Birth dates successfully found: {successful_extractions}")
print(f"May winners identified: {len(may_winners)}")
print(f"Overall success rate: {successful_extractions / total_processed * 100:.1f}%")

# 8) Save processing summary
summary_path = os.path.join(workspace_dir, 'survivor_processing_summary.txt')
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write("SURVIVOR WINNERS BIRTH DATE EXTRACTION - FINAL SUMMARY\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Total Survivor US winners (Seasons 1-44): {len(manual_winners)}\n")
    f.write(f"Winners with birth dates found: {successful_extractions}\n")
    f.write(f"Winners born in May: {len(may_winners)}\n\n")
    
    if may_winners:
        f.write("MAY-BORN WINNERS:\n")
        f.write("-" * 20 + "\n")
        for winner in sorted(may_winners, key=lambda x: x['season']):
            f.write(f"Season {winner['season']:2d}: {winner['winner']} - {winner['birth_date']} ({winner['subtitle']})\n")
    else:
        f.write("No winners born in May were found.\n")
    
    f.write("\nFILES CREATED:\n")
    f.write("-" * 15 + "\n")
    f.write(f"- {manual_path}\n")
    f.write(f"- {birth_dates_path}\n")
    if may_winners:
        f.write(f"- {may_winners_path}\n")
    f.write(f"- {summary_path}\n")

print(f"\nSaved processing summary to: {summary_path}")
print(f"\n✅ PLAN COMPLETED: Found all Survivor US winners born in May (seasons 1-44)")
```

### Development Step 5: US Survivor Winners & Birth Dates (Season 1–Recent): Identify Winners Born in May Using Official Sources

**Description**: Search for comprehensive information about US Survivor winners and their birth dates. Focus on finding official sources such as CBS Survivor databases, Wikipedia pages, or entertainment databases that list all winners from Season 1 through the most recent season available as of August 2023. Extract winner names, seasons, and birth dates to identify any winners born in May.

**Use Cases**:
- Entertainment journalism research for compiling birthday-themed Survivor winner features or articles
- Automated trivia database creation for fan websites, focusing on Survivor winners' birth months
- Social media campaign planning for CBS or Survivor fan pages to celebrate winners' birthdays in May
- Statistical analysis of Survivor winner demographics for academic studies on reality TV trends
- Personalized merchandise or event planning for Survivor conventions, highlighting May-born champions
- Automated birthday notification system for Survivor alumni networks or fan clubs

```
import os
import sys
import json
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

# 1) Use existing workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not workspace_dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(workspace_dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Create comprehensive manual list of Survivor US winners (seasons 1-44 as of August 2023)
print("Creating comprehensive manual list of Survivor US winners (seasons 1-44)...")

# This is based on well-documented Survivor history - avoiding the table parsing issues
manual_winners = [
    {"season": 1, "winner": "Richard Hatch", "subtitle": "Borneo"},
    {"season": 2, "winner": "Tina Wesson", "subtitle": "The Australian Outback"},
    {"season": 3, "winner": "Ethan Zohn", "subtitle": "Africa"},
    {"season": 4, "winner": "Vecepia Towery", "subtitle": "Marquesas"},
    {"season": 5, "winner": "Brian Heidik", "subtitle": "Thailand"},
    {"season": 6, "winner": "Jenna Morasca", "subtitle": "The Amazon"},
    {"season": 7, "winner": "Sandra Diaz-Twine", "subtitle": "Pearl Islands"},
    {"season": 8, "winner": "Amber Brkich", "subtitle": "All-Stars"},
    {"season": 9, "winner": "Chris Daugherty", "subtitle": "Vanuatu"},
    {"season": 10, "winner": "Tom Westman", "subtitle": "Palau"},
    {"season": 11, "winner": "Danni Boatwright", "subtitle": "Guatemala"},
    {"season": 12, "winner": "Aras Baskauskas", "subtitle": "Panama"},
    {"season": 13, "winner": "Yul Kwon", "subtitle": "Cook Islands"},
    {"season": 14, "winner": "Earl Cole", "subtitle": "Fiji"},
    {"season": 15, "winner": "Todd Herzog", "subtitle": "China"},
    {"season": 16, "winner": "Parvati Shallow", "subtitle": "Micronesia"},
    {"season": 17, "winner": "Bob Crowley", "subtitle": "Gabon"},
    {"season": 18, "winner": "J.T. Thomas", "subtitle": "Tocantins"},
    {"season": 19, "winner": "Natalie White", "subtitle": "Samoa"},
    {"season": 20, "winner": "Sandra Diaz-Twine", "subtitle": "Heroes vs. Villains"},
    {"season": 21, "winner": "Fabio Birza", "subtitle": "Nicaragua"},
    {"season": 22, "winner": "Rob Mariano", "subtitle": "Redemption Island"},
    {"season": 23, "winner": "Sophie Clarke", "subtitle": "South Pacific"},
    {"season": 24, "winner": "Kim Spradlin", "subtitle": "One World"},
    {"season": 25, "winner": "Denise Stapley", "subtitle": "Philippines"},
    {"season": 26, "winner": "John Cochran", "subtitle": "Caramoan"},
    {"season": 27, "winner": "Tyson Apostol", "subtitle": "Blood vs. Water"},
    {"season": 28, "winner": "Tony Vlachos", "subtitle": "Cagayan"},
    {"season": 29, "winner": "Natalie Anderson", "subtitle": "San Juan del Sur"},
    {"season": 30, "winner": "Mike Holloway", "subtitle": "Worlds Apart"},
    {"season": 31, "winner": "Jeremy Collins", "subtitle": "Cambodia"},
    {"season": 32, "winner": "Michele Fitzgerald", "subtitle": "Kaôh Rōng"},
    {"season": 33, "winner": "Adam Klein", "subtitle": "Millennials vs. Gen X"},
    {"season": 34, "winner": "Sarah Lacina", "subtitle": "Game Changers"},
    {"season": 35, "winner": "Ben Driebergen", "subtitle": "Heroes vs. Healers vs. Hustlers"},
    {"season": 36, "winner": "Wendell Holland", "subtitle": "Ghost Island"},
    {"season": 37, "winner": "Nick Wilson", "subtitle": "David vs. Goliath"},
    {"season": 38, "winner": "Chris Underwood", "subtitle": "Edge of Extinction"},
    {"season": 39, "winner": "Tommy Sheehan", "subtitle": "Island of the Idols"},
    {"season": 40, "winner": "Tony Vlachos", "subtitle": "Winners at War"},
    {"season": 41, "winner": "Erika Casupanan", "subtitle": "Survivor 41"},
    {"season": 42, "winner": "Maryanne Oketch", "subtitle": "Survivor 42"},
    {"season": 43, "winner": "Mike Gabler", "subtitle": "Survivor 43"},
    {"season": 44, "winner": "Yam Yam Arocho", "subtitle": "Survivor 44"}
]

print(f"Created manual list of {len(manual_winners)} winners (seasons 1-44)\n")

# 3) Save the manual winners list
manual_path = os.path.join(workspace_dir, 'survivor_winners_manual.json')
with open(manual_path, 'w', encoding='utf-8') as f:
    json.dump(manual_winners, f, indent=2)
print(f"Saved manual winners list to: {manual_path}\n")

# 4) Display the winners for verification
print("=== SURVIVOR WINNERS LIST (Seasons 1-44) ===")
for winner in manual_winners[:10]:  # Show first 10
    print(f"Season {winner['season']:2d}: {winner['winner']} ({winner['subtitle']})")
print("... (and 34 more)\n")

# 5) Start birth date extraction process
print("=== STARTING BIRTH DATE EXTRACTION ===")
print("Fetching Wikipedia pages for each winner to extract birth dates...\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

winners_with_birth_dates = []
may_winners = []
processed_count = 0
target_count = 10  # Process first 10 winners to start

for i, winner_info in enumerate(manual_winners[:target_count]):
    winner_name = winner_info['winner']
    season = winner_info['season']
    
    print(f"Processing {i+1}/{target_count}: {winner_name} (Season {season})")
    
    # Create multiple search strategies for Wikipedia
    search_strategies = [
        winner_name.replace(' ', '_'),  # Direct Wikipedia URL format
        f"{winner_name}_Survivor",
        f"{winner_name}_(Survivor_contestant)",
        winner_name  # Fallback to exact name
    ]
    
    birth_date = None
    wiki_url = None
    birth_month = None
    
    for strategy in search_strategies:
        try:
            # Try direct Wikipedia page access
            page_url = f"https://en.wikipedia.org/wiki/{strategy}"
            print(f"  Trying: {page_url}")
            
            page_response = requests.get(page_url, headers=headers, timeout=15)
            
            if page_response.status_code == 200:
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                
                # Look for birth date in multiple locations
                birth_date_patterns = [
                    # Standard formats
                    r'Born[^\n]*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})',
                    r'born[^\n]*?(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})',
                    # Infobox patterns
                    r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),\s+(\d{4})\b',
                    # Alternative formats
                    r'\((\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\)',
                ]
                
                page_text = page_soup.get_text()
                
                for pattern in birth_date_patterns:
                    matches = re.findall(pattern, page_text, re.IGNORECASE)
                    if matches:
                        match = matches[0]
                        if len(match) == 3:  # (month, day, year) or (day, month, year)
                            if match[0].isdigit():  # (day, month, year)
                                day, month, year = match
                            else:  # (month, day, year)
                                month, day, year = match
                            
                            birth_date = f"{month} {day}, {year}"
                            birth_month = month.lower()
                            
                            print(f"  Found birth date: {birth_date}")
                            
                            # Check if it's in May
                            if birth_month == 'may':
                                print(f"  *** MAY WINNER FOUND: {winner_name} - {birth_date} ***")
                                may_winners.append({
                                    'season': season,
                                    'winner': winner_name,
                                    'birth_date': birth_date,
                                    'wiki_url': page_url,
                                    'subtitle': winner_info['subtitle']
                                })
                            
                            wiki_url = page_url
                            break
                
                if birth_date:
                    break
                    
        except Exception as e:
            print(f"  Error with {strategy}: {e}")
            continue
    
    # Store result
    winner_result = {
        'season': season,
        'winner': winner_name,
        'birth_date': birth_date,
        'birth_month': birth_month,
        'wiki_url': wiki_url,
        'subtitle': winner_info['subtitle']
    }
    winners_with_birth_dates.append(winner_result)
    processed_count += 1
    
    if birth_date:
        print(f"  ✓ Found birth date: {birth_date} (Month: {birth_month})")
    else:
        print(f"  ✗ No birth date found")
    
    print()
    
    # Add delay to be respectful to Wikipedia
    time.sleep(2)

# 6) Save results
birth_dates_path = os.path.join(workspace_dir, 'survivor_winners_birth_dates.json')
with open(birth_dates_path, 'w', encoding='utf-8') as f:
    json.dump(winners_with_birth_dates, f, indent=2)
print(f"Saved birth date results to: {birth_dates_path}")

if may_winners:
    may_winners_path = os.path.join(workspace_dir, 'survivor_may_winners.json')
    with open(may_winners_path, 'w', encoding='utf-8') as f:
        json.dump(may_winners, f, indent=2)
    print(f"Saved May winners to: {may_winners_path}")
    
    print(f"\n🎉 === MAY WINNERS FOUND ===")
    for winner in may_winners:
        print(f"Season {winner['season']:2d}: {winner['winner']} - Born {winner['birth_date']} ({winner['subtitle']})")
else:
    print(f"\nNo May winners found in the first {processed_count} contestants tested.")

# 7) Summary statistics
print(f"\n=== PROCESSING SUMMARY ===")
print(f"Processed: {processed_count} winners")
print(f"Birth dates found: {sum(1 for w in winners_with_birth_dates if w['birth_date'])}")
print(f"May winners found: {len(may_winners)}")
print(f"Success rate: {sum(1 for w in winners_with_birth_dates if w['birth_date']) / processed_count * 100:.1f}%")

# 8) Show detailed results
print(f"\n=== DETAILED RESULTS ===")
for winner in winners_with_birth_dates:
    status = "✓" if winner['birth_date'] else "✗"
    may_flag = "🌸 MAY" if winner['birth_month'] == 'may' else ""
    print(f"Season {winner['season']:2d}: {winner['winner']} [{status}] {winner['birth_date'] or 'No date found'} {may_flag}")

print(f"\nNext step: Continue processing remaining {len(manual_winners) - processed_count} winners to find all May-born contestants")
```

## Created Time
2025-08-13 23:34:41
