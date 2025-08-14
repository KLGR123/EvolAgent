# Developer Plan 01

## Plan
Search for comprehensive information about US Survivor winners and their birth dates. Focus on finding official sources such as CBS Survivor databases, Wikipedia pages listing all winners, or entertainment databases that contain biographical information including birth months for all winners of the US version of Survivor through Season 44 (as of August 2023).

## Description
This is the optimal first step because: (1) We need to identify all US Survivor winners and their birth dates to determine who was born in May, (2) No previous research has been conducted yet, (3) Expected outcome is to obtain a comprehensive dataset of Survivor winners with their birth month information, (4) This directly addresses the core TASK of finding the May-born winner by first establishing the complete winner roster with birth date details

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

### Development Step 34: Extract Survivor US Seasons 1–44 winners into workspace/survivor_winners_list.json

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Automated content update for a reality TV fan site: scrape the Survivor winners list each season to refresh the “Past Champions” section without manual edits.
- Data journalism for entertainment reporting: extract season-by-season winners to analyze demographic trends and publish an interactive infographic on a news outlet.
- Machine learning feature pipeline in media analytics: incorporate historical Survivor winner names as a categorical input when training a model to predict future reality-show outcomes.
- Business intelligence dashboard for a TV network: integrate the JSON of Survivor winners with viewership and advertising revenue data to identify which champions drove audience spikes.
- Academic study on gender and diversity in reality television: gather winner names across 44 seasons, link to demographic profiles, and run statistical tests for a communications research paper.
- Podcast episode automation for Survivor recaps: pull the latest winner’s name from Wikipedia into show notes and social posts immediately after finale night.
- QA and regression testing for a mobile trivia app: validate the in-app Survivor winners database against the freshly scraped JSON to catch content drift or missing entries.
- Social media marketing campaign analysis: correlate announcement dates from the scraped winners list with Twitter hashtag volume to gauge fan engagement over time.

```
import os
import sys
import re
import json
import requests
from bs4 import BeautifulSoup

# 1) Locate active workspace directory
dirs = [d for d in os.listdir('.') if d.startswith('workspace') and os.path.isdir(d)]
if not dirs:
    print("❌ No workspace directory found. Exiting.")
    sys.exit(1)
workspace_dir = max(dirs, key=lambda d: os.path.getmtime(d))
print(f"Using workspace directory: {workspace_dir}\n")

# 2) Fetch Survivor Wikipedia page
page_title = "Survivor_(American_TV_series)"
url = f"https://en.wikipedia.org/wiki/{page_title}"
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US,en;q=0.9'
}
print(f"Fetching Survivor page...\nURL: {url}\n")
resp = requests.get(url, headers=headers)
resp.raise_for_status()
print(f"Page fetched successfully (status {resp.status_code})\n")

# 3) Parse HTML
doc = BeautifulSoup(resp.text, 'html.parser')

# 4) Locate "Winners" section and its first following table
print("Locating 'Winners' section table...\n")
target = None
span = doc.find('span', {'id': 'Winners'})
if span and span.parent:
    # traverse siblings after the <h2> containing this span
    for sib in span.parent.next_siblings:
        if sib.name == 'table':
            target = sib
            print("→ Selected winners-only table from 'Winners' section\n")
            break

# 5) Fallback: scan all wikitable tables if not found
if not target:
    print("Could not find by section id; falling back to scanning .wikitable tables...\n")
    wikitables = doc.find_all('table', class_=lambda c: c and 'wikitable' in c)
    for idx, tbl in enumerate(wikitables, 1):
        # check if header row has exactly Season & Winner
        first = tbl.find('tr')
        if not first:
            continue
        hdrs = [th.get_text(strip=True).lower() for th in first.find_all(['th','td'], recursive=False)]
        if hdrs == ['season', 'winner']:
            target = tbl
            print(f"→ Fallback: selected simple 2-col table #{idx} with headers {hdrs}\n")
            break

if not target:
    print("❌ Could not find any suitable winners table. Exiting.")
    sys.exit(1)

# 6) Determine column indices
first = target.find('tr')
cols = [c.get_text(strip=True).lower() for c in first.find_all(['th','td'], recursive=False)]
season_idx = cols.index('season')
winner_idx = cols.index('winner')
print(f"Column indices -> season: {season_idx}, winner: {winner_idx}\n")

# 7) Extract season→winner pairs
winners = []
for row in target.find_all('tr')[1:]:  # skip header
    cells = row.find_all(['th','td'], recursive=False)
    if len(cells) <= max(season_idx, winner_idx):
        continue
    s = cells[season_idx].get_text(strip=True)
    if not s.isdigit():
        continue
    season = int(s)
    if not (1 <= season <= 44):
        continue
    cell = cells[winner_idx]
    a = cell.find('a')
    if a and re.search(r'[A-Za-z]', a.get_text()):
        name = a.get_text(strip=True)
    else:
        name = cell.get_text(strip=True)
    print(f"Parsed Season {season} → Winner: '{name}'")
    winners.append({'season': season, 'winner': name})

# 8) Sort and verify
winners_sorted = sorted(winners, key=lambda x: x['season'])
print(f"\nTotal winners extracted: {len(winners_sorted)} (expected 44)")
if len(winners_sorted) != 44:
    print("⚠️ Warning: extracted count != 44. Verify table structure.")

# 9) Save to JSON
out_file = os.path.join(workspace_dir, 'survivor_winners_list.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"\n✅ Winners list saved to: {out_file}")

```

## Created Time
2025-08-13 20:05:01
