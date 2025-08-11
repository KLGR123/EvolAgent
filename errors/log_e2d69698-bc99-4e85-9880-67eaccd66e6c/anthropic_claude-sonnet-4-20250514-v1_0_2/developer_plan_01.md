# Developer Plan 01

## Plan
Search for comprehensive information about US Survivor winners and their birth dates, focusing on identifying any winners born in May. Use multiple search approaches including: (1) Search for 'US Survivor winners birth dates May born', (2) Look for Survivor winner databases or fan sites that list biographical information, (3) Search Wikipedia pages for Survivor winners with birth month details, (4) Check CBS official Survivor resources for contestant biographical data. Extract and compile a list of all US Survivor winners with their birth dates to identify those born in May.

## Description
This is the optimal starting approach because: (1) We need to identify US Survivor winners born in May before determining if there's only one, (2) No previous research has been conducted on this topic, (3) Expected outcome is to find comprehensive birth date information for US Survivor winners, specifically focusing on May births, (4) This directly addresses the TASK by establishing the foundation for identifying the unique May-born winner as of August 2023.

## Episodic Examples
### Development Step 33: Extract Survivor (US) Winners for Seasons 1–44 and Save to JSON

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Media analytics firms ingest the Survivor winners JSON into BI dashboards to correlate winner demographics with viewership trends and advertising performance
- Fan community websites automate synchronization of Survivor winner data from Wikipedia to update leaderboards, discussion forums, and comparison charts
- E-commerce merch platforms programmatically generate winner-themed product listings (e.g., “Season 10 Winner T-Shirts”) by scraping the season-winner pairs for catalog enrichment
- Data journalism teams perform longitudinal demographic and geographic analysis of Survivor champions for feature articles on reality TV evolution
- Mobile trivia and quiz apps schedule automated updates of question banks using the extracted season-winner list to ensure up-to-date game content
- Academic researchers compiling structured datasets on reality television use the JSON output to study competition design, social dynamics, and winner profiles
- TV network production crews integrate the winners list into graphic templates for end-of-season recap montages and anniversary specials
- Chatbot and virtual assistant services query the structured winner data in real time to answer user questions like “Who won Survivor Season 27?”

```
import os
import sys
import re
import json
import requests
from bs4 import BeautifulSoup

# 1) Locate the active workspace directory
dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Fetch the standard (non-printable) Wikipedia page for Survivor
title = "Survivor_(American_TV_series)"
url = f"https://en.wikipedia.org/wiki/{title}"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US,en;q=0.9'
}
print(f"Fetching Survivor page...\nURL: {url}\n")
resp = requests.get(url, headers=headers)
resp.raise_for_status()
print(f"Page fetched successfully (status {resp.status_code})\n")

# 3) Parse HTML with BeautifulSoup
doc = BeautifulSoup(resp.text, 'html.parser')

# 4) First, scan ALL <table> tags for a simple 2-column winners-only table ['Season','Winner']
print("Scanning all tables for a simple 2-column Season→Winner table...\n")
target = None
all_tables = doc.find_all('table')
for idx, tbl in enumerate(all_tables, 1):
    first_row = tbl.find('tr')
    if not first_row:
        continue
    hdr_cells = first_row.find_all(['th', 'td'], recursive=False)
    hdr_texts = [c.get_text(strip=True).lower() for c in hdr_cells]
    print(f"Table {idx} headers: {hdr_texts}")
    if hdr_texts == ['season', 'winner']:
        target = tbl
        print(f"→ Selected simple 2-column winners-only table #{idx}. Headers match exactly ['Season','Winner']\n")
        break

# 5) Fallback: if no simple table, scan only wikitable-class tables for any containing both keywords
if not target:
    print("No exact 2-column table found; falling back to any .wikitable containing Season & Winner...\n")
    wikitables = doc.find_all('table', class_=lambda v: v and 'wikitable' in v)
    for idx, tbl in enumerate(wikitables, 1):
        first_row = tbl.find('tr')
        if not first_row:
            continue
        hdr_cells = first_row.find_all(['th', 'td'], recursive=False)
        hdr_texts = [c.get_text(strip=True).lower() for c in hdr_cells]
        if 'season' in hdr_texts and 'winner' in hdr_texts:
            target = tbl
            print(f"→ Fallback selected wikitable #{idx} with headers containing Season & Winner: {hdr_texts}\n")
            break

if not target:
    print("❌ Could not find any suitable table with Season & Winner. Exiting.")
    sys.exit(1)

# 6) Determine column indices for Season and Winner
def extract_header_indices(tbl):
    first_row = tbl.find('tr')
    hdr_cells = first_row.find_all(['th', 'td'], recursive=False)
    texts = [c.get_text(strip=True).lower() for c in hdr_cells]
    return texts.index('season'), texts.index('winner')

season_idx, winner_idx = extract_header_indices(target)
print(f"Column indices -> season: {season_idx}, winner: {winner_idx}\n")

# 7) Extract Season→Winner entries
winners = []
for row in target.find_all('tr')[1:]:  # skip header row
    cells = row.find_all(['th', 'td'], recursive=False)
    if len(cells) <= max(season_idx, winner_idx):
        continue
    season_text = cells[season_idx].get_text(strip=True)
    if not season_text.isdigit():
        continue
    season_num = int(season_text)
    if season_num < 1 or season_num > 44:
        continue
    winner_cell = cells[winner_idx]
    a_tag = winner_cell.find('a')
    if a_tag and re.search(r'[A-Za-z]', a_tag.get_text()):
        name = a_tag.get_text(strip=True)
    else:
        name = winner_cell.get_text(strip=True)
    print(f"Parsed Season {season_num} → Winner: '{name}'")
    winners.append({'season': season_num, 'winner': name})

# 8) Sort & verify count
winners_sorted = sorted(winners, key=lambda x: x['season'])
print(f"\nTotal winners extracted: {len(winners_sorted)} (expected 44)")
if len(winners_sorted) != 44:
    print("⚠️ Warning: Extracted count != 44. Verify table structure or page updates.")

# 9) Save to JSON
out_file = os.path.join(workspace_dir, 'survivor_winners_list.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"\n✅ Winners list saved to: {out_file}")

```

### Development Step 11: Extract Survivor US Season Winners (1–44) into JSON File

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Entertainment analytics dashboard for a reality‐TV network: ingest the JSON of Survivor winners to visualize season‐by‐season trends, gender breakdowns, and airtime engagement metrics.
- Automated candidate for marketing campaigns: trigger personalized emails or push notifications on each season’s finale anniversary, highlighting the winner’s name to superfans.
- Trivia mobile and web game content loader: populate question banks with “Who won season X of Survivor?” to ensure up‐to‐date, accurate quiz rounds across 44 seasons.
- Academic media studies research: merge the winners list with demographic datasets to analyze diversity and representation patterns in reality‐TV winners over time.
- Data journalism fact‐checking pipeline: integrate the scraper into a newsroom workflow to instantly verify and update articles on Survivor’s history and milestone cases.
- CMS automation for broadcaster websites: auto‐sync the latest Survivor winners into the official show page, eliminating manual data entry and reducing update errors.
- Social media archival bot: schedule daily “On this day” posts that reference the exact season number and winner name, driving historical engagement on Twitter or Instagram.
- Business intelligence for streaming services: correlate extracted winner data with viewership and subscription spikes to inform content acquisition and promotional strategies.

```
import os
import json
import requests
from bs4 import BeautifulSoup

# 1) Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# 2) Fetch Survivor page with realistic User-Agent to avoid blocks
url = 'https://en.wikipedia.org/wiki/Survivor_(American_TV_series)'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/114.0.0.0 Safari/537.36'
}
print(f"Fetching page with headers: {url}")
response = requests.get(url, headers=headers)
response.raise_for_status()
print("Page fetched successfully (status code: {}).").format(response.status_code)

# 3) Save raw HTML for inspection
html_path = os.path.join(workspace_dir, 'survivor_page.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(response.text)
print(f"Saved full page HTML to: {html_path}")

# 4) Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 5) Locate the "Winners by season" section headline robustly
print("Searching for section headline containing 'winners'")
headline_span = None
for span in soup.find_all('span', class_='mw-headline'):
    text = span.get_text(strip=True)
    if 'winners' in text.lower():
        print(f"  ✓ Found headline: '{text}' (id={span.get('id')})")
        headline_span = span
        break

if not headline_span:
    # fallback: write all headlines to file for manual inspection
    print("❌ No 'winners' headline found. Dumping all section headlines to workspace/section_headlines.txt...")
    with open(os.path.join(workspace_dir, 'section_headlines.txt'), 'w', encoding='utf-8') as f:
        for span in soup.find_all('span', class_='mw-headline'):
            f.write(f"id={span.get('id')}\ttext={span.get_text(strip=True)}\n")
    raise RuntimeError("Cannot locate a section headline containing 'winners'. See workspace/section_headlines.txt.")

# 6) From that headline, find its parent heading and the next table sibling
heading_tag = headline_span.find_parent(['h2', 'h3', 'h4'])
winners_table = None
for sib in heading_tag.next_siblings:
    if getattr(sib, 'name', None) == 'table':
        # ensure it's a wikitable
        classes = sib.get('class') or []
        if 'wikitable' in classes:
            winners_table = sib
            print("Found next <table class='wikitable'> after the 'Winners' heading.")
            break
        else:
            print("  Skipped a <table> without 'wikitable' class.")
    # stop if another heading appears
    if getattr(sib, 'name', None) in ['h2', 'h3', 'h4']:
        break

if not winners_table:
    raise RuntimeError("No wikitable found immediately after 'Winners' heading.")

# 7) Parse header row for column indices
header_row = winners_table.find('tr')
header_cells = header_row.find_all(['th', 'td'], recursive=False)
headers = []
for cell in header_cells:
    # remove any footnote markers
    for sup in cell.find_all('sup'):
        sup.decompose()
    headers.append(cell.get_text(strip=True).lower())
print(f"Table headers detected: {headers}")

if 'season' not in headers or 'winner' not in headers:
    raise RuntimeError(f"Unexpected table headers; expected 'Season' and 'Winner'. Got: {headers}")
season_idx = headers.index('season')
winner_idx = headers.index('winner')
print(f"Identified column indices → season: {season_idx}, winner: {winner_idx}")

# 8) Iterate data rows and extract season-winner pairs for seasons 1–44
rows = winners_table.find_all('tr')[1:]  # skip header
winners = []
print(f"Total rows to examine (excluding header): {len(rows)}")
for row in rows:
    cells = row.find_all(['th', 'td'], recursive=False)
    if len(cells) <= max(season_idx, winner_idx):
        print(f"  Skipping row: only {len(cells)} cells")
        continue
    # parse season number
    season_cell = cells[season_idx]
    for sup in season_cell.find_all('sup'):
        sup.decompose()
    season_text = season_cell.get_text(strip=True)
    try:
        season_num = int(season_text)
    except ValueError:
        print(f"  Skipping row: invalid season '{season_text}'")
        continue
    if not (1 <= season_num <= 44):
        print(f"  Skipping season {season_num}: out of range 1–44")
        continue
    # parse winner name
    winner_cell = cells[winner_idx]
    for sup in winner_cell.find_all('sup'):
        sup.decompose()
    winner_name = winner_cell.get_text(strip=True)
    print(f"  Parsed Season {season_num} → Winner: {winner_name}")
    winners.append({'season': season_num, 'winner': winner_name})

# 9) Sort and save to JSON
winners_sorted = sorted(winners, key=lambda x: x['season'])
print(f"Total winners extracted for seasons 1–44: {len(winners_sorted)}")
if len(winners_sorted) != 44:
    print(f"⚠️ Warning: expected 44 entries but found {len(winners_sorted)}. Verify parsing logic.")
out_path = os.path.join(workspace_dir, 'survivor_winners_list.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"Winners list saved to: {out_path}")
```

### Development Step 52: Generate JSON List of Survivor US Season 1–44 Winners

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Entertainment app development and Trivia game integration for dynamically loading Survivor winners by season into quiz modules
- Data journalism dashboard creation and interactive visualization of Survivor winner demographics (age, gender, occupation) over seasons 1–44
- Academic media studies research and statistical trend analysis on reality‐TV competition outcomes using historical winner data
- Marketing analytics for streaming platforms and ad-targeting strategies by correlating Survivor winner profiles with viewer engagement metrics
- E-learning curriculum design and hands-on web scraping exercises to teach students how to extract structured tables from live Wikipedia pages
- Podcast production workflow automation and auto-injection of the latest Survivor winners into episode show notes via JSON feeds
- Predictive modeling in data science and machine learning experiments to forecast future Survivor champions based on past winner attributes
- Broadcast operations and internal database synchronization of Survivor season winners for sponsor reporting and rights-management systems

```
import os
import sys
import requests
from bs4 import BeautifulSoup

# === DEBUGGING SCRIPT: Verify Survivor Wikipedia page and list headlines ===
# 1) Locate the active workspace directory
dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Fetch the Survivor Wikipedia page
wiki_url = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"
print(f"Fetching Survivor page...\nURL: {wiki_url}\n")
resp = requests.get(wiki_url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'en-US,en;q=0.9'
})

# 3) Check status and final URL after redirects
try:
    resp.raise_for_status()
    print(f"→ HTTP Status: {resp.status_code} OK")
    print(f"→ Final URL: {resp.url}\n")
except Exception as e:
    print(f"❌ Failed to fetch page: {e}")
    sys.exit(1)

# 4) Save a snippet of the HTML for manual inspection
snippet_path = os.path.join(workspace_dir, 'survivor_page_snippet.html')
with open(snippet_path, 'w', encoding='utf-8') as f:
    # Save first 2000 characters to inspect structure
    f.write(resp.text[:2000])
print(f"Saved HTML snippet (first 2000 chars) to: {snippet_path}\n")

# 5) Parse HTML and extract all <span class="mw-headline"> elements
soup = BeautifulSoup(resp.text, 'html.parser')
headlines = soup.find_all('span', class_='mw-headline')
print(f"Found {len(headlines)} <span class=\"mw-headline\"> elements on the page.\n")

# 6) Write the first 30 id/text pairs to a file
headlines_path = os.path.join(workspace_dir, 'survivor_headlines_list.txt')
with open(headlines_path, 'w', encoding='utf-8') as f:
    f.write("# First 30 <span class='mw-headline'> id/text pairs\n")
    for i, span in enumerate(headlines[:30], start=1):
        hid = span.get('id', '')
        text = span.get_text(strip=True)
        line = f"{i:2d}. id='{hid}'  text='{text}'"
        f.write(line + "\n")
print(f"Wrote first {min(30, len(headlines))} headlines to: {headlines_path}\n")

# 7) Print sample headlines to console
print("=== Sample headlines ===")
for i, span in enumerate(headlines[:30], start=1):
    hid = span.get('id', '')
    text = span.get_text(strip=True)
    print(f"{i:2d}. id='{hid}'  text='{text}'")
print("=== End of headlines ===")

# 8) Warn if no headlines found
if not headlines:
    print("⚠️ Warning: No .mw-headline spans found. Check the page structure or URL.")
```

### Development Step 50: Extract Survivor (US) Winners for Seasons 1–44 into JSON File

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- TV analytics platform aggregating Survivor winners to visualize winning trends and demographic shifts across seasons for network executives
- Entertainment news site automating the creation of “On this day” articles by pulling past Survivor champion names and win dates
- Data journalism project analyzing the correlation between Survivor winners’ backgrounds (e.g., age, profession) and jury voting outcomes
- Reality TV fan app generating personalized trivia quizzes using season-winner data to engage superfans with custom leaderboards
- Academic study on game theory applying historical Survivor winner data to model strategic alliance patterns over multiple seasons
- Social media scheduling tool auto-posting anniversary shoutouts for each Survivor winner to drive engagement on franchise channels
- Market research consultancy compiling a JSON dataset of Survivor champions to advise casting directors on contestant archetypes
- Machine learning pipeline training a predictive model using past Survivor winners’ profiles and season variables to forecast future victors

```
import os
import sys
import requests
from bs4 import BeautifulSoup

# === DEBUG STEP: Verify fetched HTML and extract all mw-headline spans ===
# 1) Locate the active workspace directory
dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Fetch the Survivor Wikipedia page
wiki_url = "https://en.wikipedia.org/wiki/Survivor_(American_TV_series)"
print(f"Fetching Survivor page...\nURL: {wiki_url}")
resp = requests.get(wiki_url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'en-US,en;q=0.9'
})
print(f"→ Final URL after redirects: {resp.url}")
print(f"→ HTTP status code: {resp.status_code}")

# 3) Save a snippet of the page for manual inspection
snippet_path = os.path.join(workspace_dir, 'survivor_page_snippet.html')
with open(snippet_path, 'w', encoding='utf-8') as f:
    # Save only first 1000 characters to avoid massive file
    f.write(resp.text[:1000])
print(f"Saved first 1000 chars of page to: {snippet_path}\n")

# 4) Parse HTML and list all <span class="mw-headline"> elements
soup = BeautifulSoup(resp.text, 'html.parser')
headlines = soup.find_all('span', class_='mw-headline')
print(f"Found {len(headlines)} spans with class 'mw-headline'\n")

# 5) Write out the first 30 headline ids and texts for examination
titles_path = os.path.join(workspace_dir, 'survivor_headlines_list.txt')
with open(titles_path, 'w', encoding='utf-8') as f:
    f.write("# List of first 30 <span class='mw-headline'> id/text pairs\n")
    for i, span in enumerate(headlines[:30], start=1):
        hid = span.get('id', '')
        text = span.get_text(strip=True)
        line = f"{i:2d}. id='{hid}' text='{text}'"
        f.write(line + "\n")

print(f"Wrote first {min(30, len(headlines))} headline entries to: {titles_path}\n")
print("=== Sample headlines ===")
for i, span in enumerate(headlines[:30], start=1):
    hid = span.get('id', '')
    text = span.get_text(strip=True)
    print(f"{i:2d}. id='{hid}' text='{text}'")
print("=== End of headlines list ===")

# 6) If no headlines found, warn the tester
if not headlines:
    print("⚠️ Warning: No .mw-headline spans found. The page structure may differ or the fetch failed.")
```

### Development Step 31: Extract Survivor (US) Seasons 1–44 Winners into JSON File

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Survivor fan portal dynamic leaderboards and season recap pages powered by automated winner data extraction
- Reality TV analytics dashboard correlating season winners with viewer ratings and demographic trends for media researchers
- Podcast episode generator for Survivor-focused shows, auto-populating show notes and social posts with the latest winner list
- Trivia mobile app backend that fetches and updates Survivor winner questions by season for daily quiz challenges
- Merchandise design workflow that pulls winner names to create commemorative T-shirt prints and collectible posters each season
- Diversity and representation report in academic studies, using extracted winner data to examine gender and age trends across Survivor’s history
- Marketing campaign automation for anniversary promotions, dynamically inserting winners’ names into email and ad templates

```
import os
import sys
import re
import json
import requests
from bs4 import BeautifulSoup

# 1) Locate the active workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not workspace_dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(workspace_dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Fetch the printable Wikipedia page for Survivor
page = "Survivor_(American_TV_series)"
url = f"https://en.wikipedia.org/w/index.php?title={page}&printable=yes"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US,en;q=0.9'
}
print(f"Fetching Survivor printable page...\nURL: {url}\n")
resp = requests.get(url, headers=headers)
resp.raise_for_status()
print(f"Page fetched successfully (status {resp.status_code})\n")

# 3) Parse HTML with BeautifulSoup
doc = BeautifulSoup(resp.text, 'html.parser')

# 4) Locate the "winners-only" table: exactly 2 columns, headers contain 'season' and 'winner'
tables = doc.find_all('table', class_='wikitable')
target = None
print(f"Found {len(tables)} wikitable(s). Scanning for a 2-column winners-only table...\n")
for idx, tbl in enumerate(tables, 1):
    first_row = tbl.find('tr')
    if not first_row:
        continue
    hdr_cells = first_row.find_all(['th','td'], recursive=False)
    hdr_texts = [c.get_text(strip=True).lower() for c in hdr_cells]
    print(f"Table {idx} header texts: {hdr_texts}")
    # pick if exactly 2 headers and both 'season' and 'winner' appear
    if len(hdr_texts) == 2 and any('season' in t for t in hdr_texts) and any('winner' in t for t in hdr_texts):
        target = tbl
        print(f"→ Selected simple winners-only table #{idx} with headers {hdr_texts}\n")
        break

# fallback: any table containing both 'season' & 'winner'
if not target:
    print("No 2-column table found; falling back to any table containing 'Season' & 'Winner'...\n")
    for idx, tbl in enumerate(tables, 1):
        first_row = tbl.find('tr')
        if not first_row:
            continue
        hdr_cells = first_row.find_all(['th','td'], recursive=False)
        hdr_texts = [c.get_text(strip=True).lower() for c in hdr_cells]
        if any('season' in t for t in hdr_texts) and any('winner' in t for t in hdr_texts):
            target = tbl
            print(f"→ Fallback selected table #{idx} with headers {hdr_texts}\n")
            break

if not target:
    print("❌ Could not find any suitable table with Season & Winner. Exiting.")
    sys.exit(1)

# 5) Determine the column indices for Season and Winner
first = target.find('tr')
cols = [c.get_text(strip=True).lower() for c in first.find_all(['th','td'], recursive=False)]
season_idx = cols.index('season')
winner_idx = cols.index('winner')
print(f"Column indices -> season: {season_idx}, winner: {winner_idx}\n")

# 6) Extract season→winner pairs
winners = []
for row in target.find_all('tr')[1:]:  # skip header
    cells = row.find_all(['th','td'], recursive=False)
    if len(cells) <= max(season_idx, winner_idx):
        continue
    s_txt = cells[season_idx].get_text(strip=True)
    if not s_txt.isdigit():
        continue
    season_num = int(s_txt)
    if season_num < 1 or season_num > 44:
        continue
    # prefer <a> tag text
    winner_cell = cells[winner_idx]
    a = winner_cell.find('a')
    if a and re.search(r'[A-Za-z]', a.get_text()):
        name = a.get_text(strip=True)
    else:
        name = winner_cell.get_text(strip=True)
    print(f"Parsed Season {season_num} → Winner: '{name}'")
    winners.append({'season': season_num, 'winner': name})

# 7) Sort and validate
winners_sorted = sorted(winners, key=lambda x: x['season'])
print(f"\nTotal winners extracted: {len(winners_sorted)} (expected 44)")
if len(winners_sorted) != 44:
    print("⚠️ Warning: extracted count != 44. Please verify logic and page structure.")
else:
    missing = [w['season'] for w in winners_sorted if not w['winner']]
    if missing:
        print(f"⚠️ Seasons with empty winners: {missing}")

# 8) Write to JSON
out_path = os.path.join(workspace_dir, 'survivor_winners_list.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"\n✅ Winners list saved to: {out_path}")

```

## Created Time
2025-08-11 02:47:38
