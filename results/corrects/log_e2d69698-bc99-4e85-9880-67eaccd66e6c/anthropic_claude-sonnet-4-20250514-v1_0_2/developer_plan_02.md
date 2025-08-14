# Developer Plan 02

## Plan
Analyze the comprehensive Survivor winners birth date data in the workspace files to identify which winner(s) were born in May. Extract and verify the May-born winner information from the research results, specifically checking the birth month analysis and complete research dataset.

## Description
This is the optimal next step because: (1) The developer has successfully completed comprehensive research on all 44 US Survivor winners with birth date information for 31 winners organized by birth months, (2) The research created multiple structured data files including birth month analysis that should contain the May-born winner information, (3) Expected outcome is to identify the specific Survivor winner born in May from the existing dataset, (4) This directly answers the TASK question by extracting the May birth month data from the completed research results.

## Episodic Examples
### Development Step 26: Extract Survivor US seasons 1–44 winners into workspace JSON file

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Reality TV network automating anniversary posts by extracting Survivor season–winner pairs to schedule social media campaigns
- Fan-run website generating dynamic winner profile pages for each Survivor season (1–44) from the JSON data
- Trivia app populating its quiz database with season numbers and winners for automated question generation
- Streaming service enriching episode metadata with correct Survivor winner tags to improve user recommendations
- Data journalism project analyzing gender and age trends among Survivor winners across seasons 1–44
- Academic research team importing season winners into statistical models to study competitive reality TV outcomes
- Marketing analytics dashboard correlating Survivor winner announcements with spikes in merchandise sales
- Chatbot integration that fetches and replies with Survivor winners on demand for fan Q&A interactions

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

# 2) Fetch the printable Wikipedia page for Survivor (American TV series)
page_title = "Survivor_(American_TV_series)"
url = f"https://en.wikipedia.org/w/index.php?title={page_title}&printable=yes"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'en-US,en;q=0.9'
}
print(f"Fetching Survivor printable page...\nURL: {url}\n")
response = requests.get(url, headers=headers)
response.raise_for_status()
print(f"Page fetched successfully (status code: {response.status_code})\n")

# 3) Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# 4) Find the table with both 'Season' and 'Winner' headers
tables = soup.find_all('table', class_='wikitable')
print(f"Found {len(tables)} tables with class 'wikitable'.\n")
target_table = None
for idx, tbl in enumerate(tables, start=1):
    first_row = tbl.find('tr')
    headers = [cell.get_text(strip=True).lower() for cell in first_row.find_all(['th','td'], recursive=False)]
    print(f"Table {idx} headers: {headers}")
    if 'season' in headers and 'winner' in headers:
        target_table = tbl
        print(f"→ Selected table {idx} for parsing.\n")
        break

if not target_table:
    print("❌ Could not find a table containing both 'Season' and 'Winner'. Exiting.")
    sys.exit(1)

# 5) Determine indices for 'Season' and 'Winner' columns
header_cells = target_table.find('tr').find_all(['th','td'], recursive=False)
col_names = [c.get_text(strip=True).lower() for c in header_cells]
season_idx = col_names.index('season')
winner_idx = col_names.index('winner')
print(f"Column indices -> season: {season_idx}, winner: {winner_idx}\n")

# 6) Helper to clean and extract winner name

def clean_winner(cell):
    # remove any footnotes
    for sup in cell.find_all('sup'):
        sup.decompose()
    # a) prefer <a> link texts with letters
    for a in cell.find_all('a'):
        text = a.get_text(strip=True)
        if re.search(r'[A-Za-z]', text):
            return text
    # b) next prefer <b> tag texts with letters
    for b in cell.find_all('b'):
        text = b.get_text(strip=True)
        if re.search(r'[A-Za-z]', text):
            return text
    # c) fallback: full text minus trailing vote counts
    full_text = cell.get_text(' ', strip=True)
    return re.sub(r"\s*\d+(?:[–-]\d+)*$", "", full_text).strip()

# 7) Iterate rows and extract season→winner for 1–44
winners = []
for row in target_table.find_all('tr')[1:]:  # skip header
    cells = row.find_all(['th','td'], recursive=False)
    if len(cells) <= max(season_idx, winner_idx):
        continue
    season_text = cells[season_idx].get_text(strip=True)
    try:
        season_num = int(season_text)
    except ValueError:
        continue
    if not (1 <= season_num <= 44):
        continue
    winner_name = clean_winner(cells[winner_idx])
    print(f"Parsed Season {season_num} → Winner: {winner_name}")
    winners.append({'season': season_num, 'winner': winner_name})

# 8) Sort by season and verify count
winners_sorted = sorted(winners, key=lambda x: x['season'])
print(f"\nTotal winners extracted: {len(winners_sorted)} (expected 44)")
if len(winners_sorted) != 44:
    print("⚠️ Warning: extracted count != 44. Please verify the logic.")

# 9) Write to JSON
output_path = os.path.join(workspace_dir, 'survivor_winners_list.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"✅ Winners list saved to: {output_path}")
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

### Development Step 35: Extract Survivor Seasons 1–44 Winners to JSON File

**Description**: Access the Wikipedia page https://en.wikipedia.org/wiki/Survivor_(American_TV_series) and extract the table of winners for seasons 1 through 44, saving each season number with its corresponding winner name into workspace/survivor_winners_list.json.

**Use Cases**:
- Television analytics team automating the ingestion of Survivor winners per season to correlate champion demographics with Nielsen ratings and optimize future programming decisions
- Reality TV fan site updating its historical champions database daily by extracting the latest Survivor winner entries for interactive timeline features
- Data scientist training a predictive model on 44 seasons of Survivor outcomes, using the winners JSON alongside game mechanics to forecast likely future champions
- Marketing analyst cross-referencing Survivor winners with their post-show endorsement deals to evaluate influencer potential and tailor brand partnership strategies
- Academic researcher performing a longitudinal gender‐representation study on reality TV champions by processing the season-winner list for statistical significance tests
- Mobile trivia app developer automating question generation by importing Survivor winners into the question bank, ensuring up-to-date challenges for quiz players
- Data journalist crafting an interactive infographic of Survivor season finales by feeding the extracted winners JSON into a visualization pipeline
- Chatbot integration for streaming platforms, leveraging the Survivor winners list to answer user queries about past champions in real time

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

# 2) Fetch the Survivor Wikipedia page
page_title = "Survivor_(American_TV_series)"
url = f"https://en.wikipedia.org/wiki/{page_title}"
print(f"Fetching Survivor page...\nURL: {url}\n")
resp = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0',
    'Accept-Language': 'en-US,en;q=0.9'
})
resp.raise_for_status()
print(f"Page fetched successfully (status {resp.status_code})\n")

# 3) Parse HTML
doc = BeautifulSoup(resp.text, 'html.parser')

target = None
# 4) Try to select the first table immediately after the 'Winners' section heading
print("Locating 'Winners' section then its first following <table>...\n")
span = doc.find('span', id='Winners')
if span:
    h2 = span.find_parent('h2')
    if h2:
        tbl = h2.find_next('table')
        if tbl:
            target = tbl
            print("→ Selected table following the 'Winners' section.\n")

# 5) Fallback: scan all .wikitable tables for headers containing both 'season' & 'winner'
if not target:
    print("Fallback: scanning all .wikitable tables for headers containing 'Season' & 'Winner'...\n")
    wikitables = doc.find_all('table', class_=lambda v: v and 'wikitable' in v)
    for idx, tbl in enumerate(wikitables, 1):
        first_row = tbl.find('tr')
        if not first_row:
            continue
        hdrs = [th.get_text(strip=True).lower() for th in first_row.find_all(['th','td'], recursive=False)]
        print(f"Table {idx} headers: {hdrs}")
        if 'season' in hdrs and 'winner' in hdrs:
            target = tbl
            print(f"→ Selected wikitable #{idx} with headers containing Season & Winner.\n")
            break

if not target:
    print("❌ Could not find any suitable winners table. Exiting.")
    sys.exit(1)

# 6) Determine which columns are Season and Winner
def get_header_indices(tbl):
    first = tbl.find('tr')
    texts = [c.get_text(strip=True).lower() for c in first.find_all(['th','td'], recursive=False)]
    return texts.index('season'), texts.index('winner')

season_idx, winner_idx = get_header_indices(target)
print(f"Column indices -> season: {season_idx}, winner: {winner_idx}\n")

# 7) Extract (season -> winner) pairs
winners = []
for row in target.find_all('tr')[1:]:  # skip header
    cells = row.find_all(['th','td'], recursive=False)
    if len(cells) <= max(season_idx, winner_idx):
        continue
    # parse season number
    s_text = cells[season_idx].get_text(strip=True)
    m = re.match(r"^(\d+)", s_text)
    if not m:
        continue
    season = int(m.group(1))
    if not (1 <= season <= 44):
        continue
    # extract winner name(s)
    winner_cell = cells[winner_idx]
    a_tags = winner_cell.find_all('a')
    if a_tags:
        # join all hyperlink texts (handles joint winners)
        names = [a.get_text(strip=True) for a in a_tags if re.search(r"[A-Za-z]", a.get_text())]
        name = " & ".join(names) if names else winner_cell.get_text(strip=True)
    else:
        name = winner_cell.get_text(strip=True)
    print(f"Parsed Season {season} → Winner: '{name}'")
    winners.append({'season': season, 'winner': name})

# 8) Sort and verify
ewinners_sorted = sorted(winners, key=lambda x: x['season'])
print(f"\nTotal winners extracted: {len(winners_sorted)} (expected 44)")
if len(winners_sorted) != 44:
    print("⚠️ Warning: extracted count != 44. Verify table structure.")
else:
    missing = [w['season'] for w in winners_sorted if not w['winner']]
    if missing:
        print(f"⚠️ Seasons with missing winner names: {missing}")

# 9) Write to JSON
out_path = os.path.join(workspace_dir, 'survivor_winners_list.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(winners_sorted, f, indent=2)
print(f"\n✅ Winners list saved to: {out_path}")
```

## Created Time
2025-08-13 20:15:55
