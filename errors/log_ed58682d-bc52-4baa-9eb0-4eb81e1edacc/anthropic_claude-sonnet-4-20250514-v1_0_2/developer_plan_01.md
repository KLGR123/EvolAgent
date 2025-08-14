# Developer Plan 01

## Plan
Identify the King of Pop (Michael Jackson) and determine his sixth studio album, then find the fifth single from that album. Research the song structure to locate the lyrics and identify the last word that appears before the second chorus begins.

## Description
This is the optimal first step because: (1) We need to establish which artist is the 'King of Pop' and identify his sixth studio album, (2) No previous research has been conducted based on the empty HISTORY, (3) Expected outcome is to identify the specific song (fifth single from sixth album) and access its structure to analyze chorus placement, (4) This directly addresses the core TASK by systematically identifying the target song before analyzing its lyrical structure

## Episodic Examples
### Development Step 37: Identify Pre-1999 Fiona Apple and Paula Cole Albums Without Christgau Letter Grades

**Description**: Analyze the research results from workspace/christgau_comprehensive_final_complete_20250803_040620.json to determine which pre-1999 Fiona Apple and Paula Cole albums did NOT receive letter grades from Robert Christgau. Cross-reference the complete list of pre-1999 albums identified earlier with the Christgau review findings to identify albums that were either not reviewed or did not receive letter grades. Create the final alphabetized, comma-delimited list of album titles that didn't receive Christgau letter grades.

**Use Cases**:
- Music archiving teams integrating automated review checks into library management systems to flag pre-1999 Fiona Apple and Paula Cole albums lacking Robert Christgau letter grades for catalog completeness
- Academic researchers in musicology cross-referencing discographies with Christgau’s reviews to study critical reception gaps in ’90s female singer-songwriter releases for a peer-reviewed journal article
- Digital music streaming platforms implementing metadata quality assurance workflows that detect and tag albums missing authoritative Christgau ratings before public release
- Entertainment analytics companies generating completeness reports from critic datasets to identify ungraded albums in their rock criticism database, prioritizing them for manual review
- Online music encyclopedias automating editorial pipelines to highlight entries of pre-1999 records without Christgau letter grades, streamlining content enrichment workflows
- University libraries auditing their special collections of ’90s alternative albums to ensure all items have documented critical assessments, using JSON analysis to detect missing reviews
- Record label archival departments auditing legacy catalogs to identify unreviewed Fiona Apple and Paula Cole releases, supporting retrospective marketing and reissue campaigns with comprehensive press notes

```
import os
import json

print("=== FINAL ANALYSIS: IDENTIFYING ALBUMS WITHOUT CHRISTGAU LETTER GRADES ===\n")
print("Objective: Create alphabetized, comma-delimited list of pre-1999 albums that did NOT receive letter grades\n")

# Load the comprehensive results file
results_file = 'workspace/christgau_comprehensive_final_complete_20250803_040620.json'

with open(results_file, 'r', encoding='utf-8') as f:
    results_data = json.load(f)

print("=== EXTRACTING ALBUM REVIEW STATUS DATA ===\n")

# Extract the target albums status data
target_albums_status = results_data.get('target_albums_status', {})

print("Complete album review status:")
for album_key, status_data in target_albums_status.items():
    found = status_data.get('found', False)
    grade = status_data.get('grade', None)
    print(f"  {album_key}:")
    print(f"    Found: {found}")
    print(f"    Grade: {grade}")
    print(f"    Has letter grade: {grade is not None}")
    print()

print("=== IDENTIFYING ALBUMS WITHOUT LETTER GRADES ===\n")

# Identify albums that did NOT receive letter grades
albums_without_grades = []

for album_key, status_data in target_albums_status.items():
    found = status_data.get('found', False)
    grade = status_data.get('grade', None)
    
    # An album didn't receive a letter grade if:
    # 1. It was not found at all (found = False), OR
    # 2. It was found but has no grade (grade = None)
    if not found or grade is None:
        # Extract just the album title from the key format "Artist - Album"
        if ' - ' in album_key:
            artist, album_title = album_key.split(' - ', 1)
            albums_without_grades.append(album_title.strip())
            print(f"Album without letter grade: {album_title.strip()}")
            print(f"  Artist: {artist.strip()}")
            print(f"  Status: {'Not found' if not found else 'Found but no grade'}")
        else:
            albums_without_grades.append(album_key)
            print(f"Album without letter grade: {album_key}")
        print()

print(f"Total albums without letter grades: {len(albums_without_grades)}")
print(f"Albums: {albums_without_grades}")

print("\n=== CREATING FINAL ALPHABETIZED LIST ===\n")

# Sort albums alphabetically
albums_without_grades_sorted = sorted(albums_without_grades)

print("Albums without Christgau letter grades (alphabetized):")
for i, album in enumerate(albums_without_grades_sorted, 1):
    print(f"  {i}. {album}")

# Create the final comma-delimited list
final_list = ', '.join(albums_without_grades_sorted)

print(f"\n=== FINAL ANSWER ===\n")
print(f"Pre-1999 Fiona Apple and Paula Cole albums that did NOT receive letter grades from Robert Christgau:")
print(f"\n{final_list}")

print(f"\n=== VERIFICATION SUMMARY ===\n")
print("Research verification:")
print(f"  Total pre-1999 target albums analyzed: {len(target_albums_status)}")
print(f"  Albums found with letter grades: {len([a for a in target_albums_status.values() if a.get('found') and a.get('grade')])}") 
print(f"  Albums without letter grades: {len(albums_without_grades)}")

# Show which albums DID receive grades for completeness
albums_with_grades = []
for album_key, status_data in target_albums_status.items():
    found = status_data.get('found', False)
    grade = status_data.get('grade', None)
    if found and grade is not None:
        if ' - ' in album_key:
            artist, album_title = album_key.split(' - ', 1)
            albums_with_grades.append(f"{album_title.strip()} (grade: {grade})")

print(f"\nAlbums that DID receive Christgau letter grades:")
for album in albums_with_grades:
    print(f"  - {album}")

# Save final results
final_results = {
    'analysis_objective': 'Identify pre-1999 Fiona Apple and Paula Cole albums without Christgau letter grades',
    'analysis_timestamp': __import__('time').strftime('%Y-%m-%d %H:%M:%S'),
    'total_albums_analyzed': len(target_albums_status),
    'albums_with_grades': len(albums_with_grades),
    'albums_without_grades': len(albums_without_grades),
    'albums_without_grades_list': albums_without_grades_sorted,
    'final_comma_delimited_answer': final_list,
    'detailed_status': {
        album_key: {
            'found': status_data.get('found', False),
            'grade': status_data.get('grade', None),
            'has_letter_grade': status_data.get('grade', None) is not None
        } for album_key, status_data in target_albums_status.items()
    }
}

with open('workspace/final_christgau_analysis_results.json', 'w') as f:
    json.dump(final_results, f, indent=2)

print(f"\n=== ANALYSIS COMPLETE ===\n")
print(f"Final results saved to: workspace/final_christgau_analysis_results.json")
print(f"\n**FINAL ANSWER**: {final_list}")
```

### Development Step 36: List Pre-1999 Fiona Apple and Paula Cole Albums Missing Christgau Letter Grades

**Description**: Analyze the research results from workspace/christgau_comprehensive_final_complete_20250803_040620.json to determine which pre-1999 Fiona Apple and Paula Cole albums did NOT receive letter grades from Robert Christgau. Cross-reference the complete list of pre-1999 albums identified earlier with the Christgau review findings to identify albums that were either not reviewed or did not receive letter grades. Create the final alphabetized, comma-delimited list of album titles that didn't receive Christgau letter grades.

**Use Cases**:
- Music librarian cross-referencing album metadata with Christgau’s archives to flag pre-1999 Fiona Apple and Paula Cole albums lacking critical letter grades for catalog completeness
- Digital music streaming service data curation team automating enrichment of album metadata by identifying pre-1999 titles without Christgau grades for targeted content recommendations
- Academic musicology researcher compiling a dataset of unreviewed pre-1999 albums by Fiona Apple and Paula Cole to study underrepresented critical reception trends
- Independent music blogger generating a list of neglected pre-1999 albums without Christgau reviews to inspire specialized review articles and blog posts
- Record label archival department auditing legacy releases to ensure all pre-1999 Fiona Apple and Paula Cole albums are matched with critical assessments, highlighting gaps for press kit updates
- Discography maintainer for a fan-run music website producing an alphabetized, comma-delimited list of albums missing Christgau letter grades to complete their online catalog
- Data engineer at a music metadata platform automating the detection of missing critical review grades, feeding this data into their recommendation engine to surface overlooked albums
- AI-driven playlist curator identifying under-reviewed pre-1999 tracks by Fiona Apple and Paula Cole to diversify playlist selections and spotlight underrated music

```
import os
import json

print("=== DETAILED ANALYSIS OF CHRISTGAU RESEARCH RESULTS ===\n")
print("Objective: Extract album review data and identify albums without letter grades\n")

# Load the comprehensive results file
results_file = 'workspace/christgau_comprehensive_final_complete_20250803_040620.json'

with open(results_file, 'r', encoding='utf-8') as f:
    results_data = json.load(f)

print("=== EXAMINING TARGET ALBUMS STATUS SECTION ===\n")

# Examine the target_albums_status section in detail
target_albums_status = results_data.get('target_albums_status', {})
print(f"Target albums status keys: {list(target_albums_status.keys())}")

for key, value in target_albums_status.items():
    print(f"\n{key.upper()}:")
    if isinstance(value, dict):
        print(f"  Type: Dictionary with {len(value)} entries")
        # Show first few entries to understand structure
        for album_key, album_data in list(value.items())[:3]:
            print(f"  Sample - {album_key}: {album_data}")
    elif isinstance(value, list):
        print(f"  Type: List with {len(value)} items")
        if value:
            print(f"  Sample items: {value[:3]}")
    else:
        print(f"  Value: {value}")

print("\n" + "="*70)
print("=== EXAMINING PREVIOUS FINDINGS SECTION ===\n")

# Examine the previous_findings section
previous_findings = results_data.get('previous_findings', {})
print(f"Previous findings keys: {list(previous_findings.keys())}")

for key, value in previous_findings.items():
    print(f"\n{key.upper()}:")
    if isinstance(value, dict):
        print(f"  Type: Dictionary with {len(value)} entries")
        # Show structure of dictionary entries
        for sub_key, sub_value in list(value.items())[:3]:
            print(f"  Sample - {sub_key}: {type(sub_value)} - {sub_value if not isinstance(sub_value, (list, dict)) else f'{len(sub_value)} items'}")
    elif isinstance(value, list):
        print(f"  Type: List with {len(value)} items")
        if value:
            print(f"  Sample items: {value[:3]}")
    else:
        print(f"  Value: {value}")

print("\n" + "="*70)
print("=== EXAMINING ADDITIONAL HTML ANALYSIS SECTION ===\n")

# Examine the additional_html_analysis section
additional_html_analysis = results_data.get('additional_html_analysis', [])
print(f"Additional HTML analysis: List with {len(additional_html_analysis)} items")

if additional_html_analysis:
    print("\nSample entries from additional HTML analysis:")
    for i, item in enumerate(additional_html_analysis[:5]):
        print(f"  Item {i+1}: {type(item)}")
        if isinstance(item, dict):
            print(f"    Keys: {list(item.keys())}")
            # Show sample values
            for key, value in list(item.items())[:3]:
                if isinstance(value, str) and len(value) > 100:
                    print(f"    {key}: {value[:100]}...")
                else:
                    print(f"    {key}: {value}")
        else:
            print(f"    Value: {item}")
        print()

print("\n" + "="*70)
print("=== EXAMINING FINAL SUCCESS METRICS ===\n")

# Examine final success metrics
final_success_metrics = results_data.get('final_success_metrics', {})
print("Final success metrics:")
for key, value in final_success_metrics.items():
    print(f"  {key}: {value}")

print("\n" + "="*70)
print("=== DETAILED DATA STRUCTURE ANALYSIS COMPLETE ===\n")
print("Now proceeding to extract actual album and review data...")
```

### Development Step 1: Identify 2020 Documentary, Director, Featuring ‘Run Home Slow’ 1963 Soundtrack Composer

**Description**: Conduct a comprehensive web search to identify the 2020 documentary that includes archival footage from the 1960s and focuses on a composer who wrote the soundtrack for the 1963 B movie 'Run Home Slow'. Search for keywords including '2020 documentary archival footage 1960s composer', 'Run Home Slow 1963 B movie soundtrack composer', 'documentary 2020 composer 1960s footage', and 'Run Home Slow soundtrack who composed'. Focus on identifying both the specific 2020 documentary title and the composer it focuses on, as well as the director of this documentary.

**Use Cases**:
- Archival film researcher verifying the composer and director details of a 1963 B-movie soundtrack for a museum retrospective
- Music licensing manager tracing rights holders of obscure 1960s film scores to secure streaming permissions
- Documentary producer sourcing background on a mid-century composer and archival footage for a new film project
- University film studies professor compiling a case study on 1960s B-movies and their music for a lecture series
- Film festival curator contextualizing archival materials and composer profiles in a 2020 retrospective lineup
- Legal team for a media company confirming public domain status of a 1963 soundtrack before re-release
- Digital archivist enriching metadata in an online film repository with documentary titles, composers, and directors
- Independent journalist researching forgotten film composers and their documentaries for a published feature article

```
import os
import json
import requests
from urllib.parse import quote

print("=== DOCUMENTARY SEARCH: 2020 FILM WITH 1960S ARCHIVAL FOOTAGE ===\n")
print("Objective: Find 2020 documentary featuring archival footage from 1960s")
print("Focus: Composer who wrote soundtrack for 1963 B movie 'Run Home Slow'\n")

# Search queries targeting different aspects of the research
search_queries = [
    "2020 documentary archival footage 1960s composer Run Home Slow 1963",
    "Run Home Slow 1963 B movie soundtrack composer documentary 2020",
    "documentary 2020 composer 1960s footage Run Home Slow",
    "Run Home Slow soundtrack who composed 2020 documentary",
    "1963 Run Home Slow composer documentary archival footage",
    "2020 documentary film composer 1960s archival Run Home Slow"
]

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print(f"Starting comprehensive search with {len(search_queries)} different query approaches\n")
    
    all_search_results = []
    
    for i, query in enumerate(search_queries, 1):
        print(f"=== SEARCH {i}/{len(search_queries)} ===")
        print(f"Query: {query}")
        
        # Prepare API request parameters
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 15,  # Get more results for comprehensive search
            "type": "search",
        }
        
        try:
            # Make API request to SerpAPI
            response = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
            
            if response.status_code == 200:
                results = response.json()
                print(f"Search successful - found {len(results.get('organic_results', []))} organic results")
                
                # Store results with query context
                search_result = {
                    'query_number': i,
                    'query_text': query,
                    'results_data': results,
                    'organic_count': len(results.get('organic_results', []))
                }
                all_search_results.append(search_result)
                
                # Analyze results for relevant keywords immediately
                if results.get("organic_results"):
                    print("\nAnalyzing results for documentary and composer keywords:\n")
                    
                    for j, result in enumerate(results['organic_results'][:8], 1):  # Check first 8 results
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No link')
                        snippet = result.get('snippet', 'No snippet')
                        
                        combined_text = f"{title} {snippet}".lower()
                        
                        print(f"Result {j}:")
                        print(f"Title: {title}")
                        print(f"URL: {link}")
                        print(f"Snippet: {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
                        
                        # Look for key documentary indicators
                        documentary_keywords = ['documentary', 'film', '2020', 'archival', 'footage']
                        found_doc_keywords = [kw for kw in documentary_keywords if kw in combined_text]
                        
                        # Look for composer/music keywords
                        music_keywords = ['composer', 'soundtrack', 'music', 'score', 'musician']
                        found_music_keywords = [kw for kw in music_keywords if kw in combined_text]
                        
                        # Look for Run Home Slow references
                        movie_keywords = ['run home slow', '1963', 'b movie', 'film']
                        found_movie_keywords = [kw for kw in movie_keywords if kw in combined_text]
                        
                        # Look for 1960s references
                        era_keywords = ['1960s', 'sixties', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969']
                        found_era_keywords = [kw for kw in era_keywords if kw in combined_text]
                        
                        # Look for director keywords
                        director_keywords = ['director', 'directed by', 'filmmaker', 'made by']
                        found_director_keywords = [kw for kw in director_keywords if kw in combined_text]
                        
                        # Highlight significant matches
                        if found_doc_keywords:
                            print(f"*** DOCUMENTARY KEYWORDS: {', '.join(found_doc_keywords)} ***")
                        
                        if found_music_keywords:
                            print(f"*** MUSIC/COMPOSER KEYWORDS: {', '.join(found_music_keywords)} ***")
                        
                        if found_movie_keywords:
                            print(f"*** RUN HOME SLOW KEYWORDS: {', '.join(found_movie_keywords)} ***")
                        
                        if found_era_keywords:
                            print(f"*** 1960S ERA KEYWORDS: {', '.join(found_era_keywords)} ***")
                        
                        if found_director_keywords:
                            print(f"*** DIRECTOR KEYWORDS: {', '.join(found_director_keywords)} ***")
                        
                        # Special attention to highly relevant results
                        relevance_score = len(found_doc_keywords) + len(found_music_keywords) + len(found_movie_keywords) + len(found_era_keywords)
                        if relevance_score >= 3:
                            print(f"*** HIGH RELEVANCE RESULT (Score: {relevance_score}/4) ***")
                        
                        # Look for specific documentary titles or composer names
                        import re
                        
                        # Pattern for potential documentary titles
                        title_patterns = [
                            r'"[^"]+"',  # Quoted titles
                            r'[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?',  # Capitalized phrases
                        ]
                        
                        for pattern in title_patterns:
                            matches = re.findall(pattern, title + ' ' + snippet)
                            if matches:
                                print(f"*** POTENTIAL TITLES FOUND: {matches} ***")
                        
                        # Pattern for composer names
                        name_patterns = [
                            r'[A-Z][a-z]+\s+[A-Z][a-z]+',  # First Last name pattern
                            r'composer\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',  # "composer FirstName LastName"
                        ]
                        
                        for pattern in name_patterns:
                            matches = re.findall(pattern, snippet)
                            if matches:
                                print(f"*** POTENTIAL COMPOSER NAMES: {matches} ***")
                        
                        print("-" * 60)
                
                print(f"\nCompleted search {i}/{len(search_queries)}\n")
                
            else:
                print(f"Search failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Error during search {i}: {str(e)}")
        
        print("=" * 70)
        print()
    
    # Save all search results for detailed analysis
    comprehensive_results = {
        'search_objective': 'Find 2020 documentary with 1960s archival footage about composer of Run Home Slow (1963)',
        'search_timestamp': '2024-12-19',
        'total_queries_executed': len(search_queries),
        'queries_used': search_queries,
        'all_search_results': all_search_results,
        'total_organic_results': sum([sr['organic_count'] for sr in all_search_results])
    }
    
    with open('workspace/documentary_search_comprehensive.json', 'w', encoding='utf-8') as f:
        json.dump(comprehensive_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== SEARCH PHASE COMPLETE ===\n")
    print(f"Total searches conducted: {len(search_queries)}")
    print(f"Total organic results collected: {comprehensive_results['total_organic_results']}")
    print(f"Results saved to: workspace/documentary_search_comprehensive.json")
    
    print("\nNext steps:")
    print("1. Analyze collected results for documentary titles and composer names")
    print("2. Focus on results mentioning 2020 documentaries with archival footage")
    print("3. Cross-reference Run Home Slow (1963) soundtrack information")
    print("4. Identify the specific documentary and its director")
```

### Development Step 9: Pre-1999 Fiona Apple & Paula Cole Studio Albums, EPs, and Major Releases Discography

**Description**: Research and compile a comprehensive list of all albums released by Fiona Apple and Paula Cole before 1999, including their exact release dates and album titles. Focus on their studio albums, EPs, and any other significant releases during this timeframe. Use multiple music databases, discographies, and reliable sources to ensure completeness.

**Use Cases**:
- Metadata enrichment for a music streaming platform to ensure accurate listing of Fiona Apple and Paula Cole’s pre-1999 studio albums and EPs.
- Digital archive curation in a university library’s special collection on 1990s singer-songwriters, using verified release dates and titles.
- Automated content generation for a fan site’s “Complete Discography” section, pulling structured album data directly from HTML sources.
- Data provisioning for a record label’s music licensing team preparing catalogs of pre-1999 releases for synchronization and film placement.
- Background research for a music journalist writing a comparative feature on debut and sophomore albums of female alternative artists in the late ’90s.
- Input data for a recommendation engine in a music app, leveraging release chronology to build era-specific playlists.
- Quality assurance for a remastering project, cross-verifying original release dates and album titles ahead of a 90s reissue campaign.
- Bibliometric analysis in an academic study examining release patterns of female singer-songwriters during the 1990s.

```
import os
import json
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

print("=== FIONA APPLE & PAULA COLE DISCOGRAPHY RESEARCH (PRE-1999) - RESTRUCTURED ===\n")
print("Strategy: Parse existing HTML files with completely restructured variable scoping")
print("Target: All albums released before 1999 by both artists\n")

# First, let's check what files are available in workspace
print("=== WORKSPACE INSPECTION ===")
if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    html_files = [f for f in workspace_files if f.endswith('.html')]
    json_files = [f for f in workspace_files if f.endswith('.json')]
    
    print(f"Total files in workspace: {len(workspace_files)}")
    print(f"HTML files: {len(html_files)}")
    print(f"JSON files: {len(json_files)}")
    
    for file in workspace_files:
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
else:
    print("No workspace directory found")

print(f"\n=== PARSING HTML FILES FOR ALBUM DATA ===\n")
print(f"Found {len(html_files)} HTML files to analyze")

# Initialize results structure
artist_albums = {
    'fiona_apple': {
        'artist_name': 'Fiona Apple',
        'albums_pre_1999': [],
        'sources_analyzed': [],
        'analysis_notes': []
    },
    'paula_cole': {
        'artist_name': 'Paula Cole', 
        'albums_pre_1999': [],
        'sources_analyzed': [],
        'analysis_notes': []
    }
}

# Parse each HTML file
for html_file in html_files:
    print(f"\n--- Analyzing {html_file} ---")
    
    # Determine which artist this file belongs to
    artist_key = None
    if 'fiona_apple' in html_file.lower() or 'fiona' in html_file.lower():
        artist_key = 'fiona_apple'
    elif 'paula_cole' in html_file.lower() or 'paula' in html_file.lower():
        artist_key = 'paula_cole'
    
    if not artist_key:
        print(f"  Cannot determine artist for {html_file}, skipping")
        continue
    
    print(f"  Identified as: {artist_albums[artist_key]['artist_name']}")
    
    # Load and parse HTML
    filepath = f"workspace/{html_file}"
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract page title for verification
    page_title = soup.find('title')
    title_text = page_title.get_text().strip() if page_title else 'No title'
    print(f"  Page title: {title_text}")
    
    # Record source
    artist_albums[artist_key]['sources_analyzed'].append({
        'filename': html_file,
        'title': title_text,
        'file_size': len(html_content)
    })
    
    # Look for discography sections - COMPLETELY RESTRUCTURED TO AVOID SCOPING ISSUES
    print(f"  Searching for discography information...")
    
    # Find all headings that might indicate discography sections
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    discography_headings = []
    
    # Process headings with proper scoping - no generator expressions
    discography_keywords = ['discography', 'albums', 'studio albums', 'career', 'music']
    
    for heading in headings:
        heading_text_lower = heading.get_text().lower()
        is_discography_heading = False
        
        # Check each keyword individually to avoid scoping issues
        for keyword in discography_keywords:
            if keyword in heading_text_lower:
                is_discography_heading = True
                break
        
        if is_discography_heading:
            discography_headings.append({
                'text': heading.get_text().strip(),
                'level': heading.name
            })
    
    print(f"  Found {len(discography_headings)} discography-related headings:")
    for heading in discography_headings:
        print(f"    - {heading['level'].upper()}: {heading['text']}")
    
    # Look for tables with album information
    tables = soup.find_all('table')
    print(f"  Found {len(tables)} tables")
    
    potential_album_tables = []
    
    for i, table in enumerate(tables):
        table_text = table.get_text()
        
        # Check for pre-1999 years
        pre_1999_years = re.findall(r'199[0-8]|1990|1991|1992|1993|1994|1995|1996|1997|1998', table_text)
        
        # Check for album-related terms - avoid generator expressions
        album_terms = ['album', 'studio', 'ep', 'single', 'release', 'debut']
        has_album_terms = False
        table_text_lower = table_text.lower()
        
        for term in album_terms:
            if term in table_text_lower:
                has_album_terms = True
                break
        
        if pre_1999_years and has_album_terms:
            potential_album_tables.append({
                'index': i,
                'table': table,
                'years_found': sorted(set(pre_1999_years))
            })
            print(f"    Table {i+1}: Potential album data (years: {sorted(set(pre_1999_years))})")
    
    print(f"  Identified {len(potential_album_tables)} potential album tables")
    
    # Extract album information from potential tables
    for table_info in potential_album_tables:
        table = table_info['table']
        print(f"\n    Extracting from Table {table_info['index']+1}:")
        
        # Get table headers
        headers = table.find_all('th')
        header_texts = [th.get_text().strip() for th in headers]
        print(f"      Headers: {header_texts}")
        
        # Get table rows
        rows = table.find_all('tr')
        
        for row_idx, row in enumerate(rows[1:], 1):  # Skip header row
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:  # Need at least 2 columns
                cell_texts = [cell.get_text().strip() for cell in cells]
                row_text = ' '.join(cell_texts)
                
                # Look for years in target range
                years_in_row = re.findall(r'199[0-8]|1990|1991|1992|1993|1994|1995|1996|1997|1998', row_text)
                
                if years_in_row:
                    print(f"        Row {row_idx}: {cell_texts}")
                    
                    # Try to identify album title and type
                    potential_album = {
                        'raw_data': cell_texts,
                        'years_found': sorted(set(years_in_row)),
                        'source_table': table_info['index'] + 1,
                        'source_row': row_idx
                    }
                    
                    # Determine album type
                    row_lower = row_text.lower()
                    if 'studio album' in row_lower:
                        potential_album['type'] = 'Studio Album'
                        potential_album['confidence'] = 'high'
                    elif 'ep' in row_lower:
                        potential_album['type'] = 'EP'
                        potential_album['confidence'] = 'high'
                    elif 'single' in row_lower:
                        potential_album['type'] = 'Single'
                        potential_album['confidence'] = 'medium'
                    elif 'compilation' in row_lower or 'greatest hits' in row_lower:
                        potential_album['type'] = 'Compilation'
                        potential_album['confidence'] = 'medium'
                    elif 'live' in row_lower:
                        potential_album['type'] = 'Live Album'
                        potential_album['confidence'] = 'medium'
                    else:
                        potential_album['type'] = 'Unknown'
                        potential_album['confidence'] = 'low'
                    
                    # Try to extract album title (usually the longest non-year cell)
                    title_candidates = []
                    for cell in cell_texts:
                        if len(cell) > 3 and not re.match(r'^199[0-8]$', cell) and not cell.lower() in ['studio album', 'ep', 'single']:
                            title_candidates.append(cell)
                    
                    if title_candidates:
                        potential_album['title'] = title_candidates[0]  # Take first candidate
                        potential_album['title_candidates'] = title_candidates
                    else:
                        potential_album['title'] = 'Title needs verification'
                        potential_album['title_candidates'] = []
                    
                    # Set release year (take earliest if multiple)
                    potential_album['release_year'] = min([int(year) for year in years_in_row])
                    
                    print(f"          → {potential_album['release_year']}: {potential_album['title']} ({potential_album['type']})")
                    
                    # Add to results
                    artist_albums[artist_key]['albums_pre_1999'].append(potential_album)
    
    # Also search for album mentions in the main text
    print(f"\n  Searching main text for album mentions...")
    
    # Known albums to look for
    known_albums = {
        'fiona_apple': [
            {'title': 'Tidal', 'year_hints': ['1996']},
            {'title': 'Criminal', 'year_hints': ['1996', '1997']},  # Single from Tidal
            {'title': 'Shadowboxer', 'year_hints': ['1996']}
        ],
        'paula_cole': [
            {'title': 'Harbinger', 'year_hints': ['1994']},
            {'title': 'This Fire', 'year_hints': ['1996']},
            {'title': 'Where Have All the Cowboys Gone?', 'year_hints': ['1996', '1997']},
            {'title': "I Don't Want to Wait", 'year_hints': ['1997']}
        ]
    }
    
    if artist_key in known_albums:
        page_text = soup.get_text().lower()
        
        for album_info in known_albums[artist_key]:
            album_title = album_info['title']
            if album_title.lower() in page_text:
                print(f"    Found mention of: {album_title}")
                
                # Look for year context around the mention
                for year_hint in album_info['year_hints']:
                    if year_hint in page_text:
                        print(f"      Associated with year: {year_hint}")
                        
                        # Check if we already have this album from table parsing
                        existing_album = None
                        for existing in artist_albums[artist_key]['albums_pre_1999']:
                            if album_title.lower() in existing.get('title', '').lower():
                                existing_album = existing
                                break
                        
                        if not existing_album:
                            # Add as a text-based finding
                            text_album = {
                                'title': album_title,
                                'release_year': int(year_hint),
                                'type': 'Album/Single',  # Uncertain from text
                                'confidence': 'medium',
                                'source': 'text_mention',
                                'raw_data': [f'Text mention: {album_title} ({year_hint})']
                            }
                            artist_albums[artist_key]['albums_pre_1999'].append(text_album)
                            print(f"        → Added from text: {year_hint}: {album_title}")

print(f"\n=== COMPILATION OF RESULTS ===\n")

# Sort and deduplicate albums for each artist
for artist_key, artist_data in artist_albums.items():
    print(f"--- {artist_data['artist_name']} ---")
    
    albums = artist_data['albums_pre_1999']
    
    # Sort by release year
    albums.sort(key=lambda x: x.get('release_year', 9999))
    
    print(f"Total albums/releases found: {len(albums)}")
    
    if albums:
        print("\nDetailed list:")
        for i, album in enumerate(albums, 1):
            year = album.get('release_year', 'Unknown')
            title = album.get('title', 'Unknown Title')
            album_type = album.get('type', 'Unknown')
            confidence = album.get('confidence', 'unknown')
            
            confidence_indicator = {
                'high': '🟢',
                'medium': '🟡', 
                'low': '🔴'
            }.get(confidence, '⚪')
            
            print(f"  {i}. {year}: {title} ({album_type}) {confidence_indicator}")
            
            # Show source info
            if 'source_table' in album:
                print(f"     Source: Table {album['source_table']}, Row {album['source_row']}")
            elif album.get('source') == 'text_mention':
                print(f"     Source: Text mention")
            
            # Show raw data for verification
            if 'raw_data' in album and album['raw_data']:
                print(f"     Raw: {album['raw_data']}")
            print()
    else:
        print("  No albums found in pre-1999 period")
    
    print(f"Sources analyzed: {len(artist_data['sources_analyzed'])}")
    for source in artist_data['sources_analyzed']:
        print(f"  - {source['filename']} ({source['file_size']:,} bytes)")
    print()

# Create final comprehensive report
final_report = {
    'research_target': 'Fiona Apple & Paula Cole albums released before 1999',
    'research_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'methodology': 'Wikipedia HTML parsing with table extraction and text analysis',
    'artists': artist_albums,
    'summary': {
        'fiona_apple_count': len(artist_albums['fiona_apple']['albums_pre_1999']),
        'paula_cole_count': len(artist_albums['paula_cole']['albums_pre_1999']),
        'total_releases': len(artist_albums['fiona_apple']['albums_pre_1999']) + len(artist_albums['paula_cole']['albums_pre_1999'])
    }
}

# Save comprehensive results
with open('workspace/fiona_apple_paula_cole_albums_pre_1999.json', 'w') as f:
    json.dump(final_report, f, indent=2)

print(f"=== RESEARCH COMPLETE ===\n")
print(f"Comprehensive results saved to: workspace/fiona_apple_paula_cole_albums_pre_1999.json")
print(f"\nFINAL SUMMARY:")
print(f"Fiona Apple: {final_report['summary']['fiona_apple_count']} releases found")
print(f"Paula Cole: {final_report['summary']['paula_cole_count']} releases found")
print(f"Total: {final_report['summary']['total_releases']} releases before 1999")
```

## Created Time
2025-08-14 07:07:59
