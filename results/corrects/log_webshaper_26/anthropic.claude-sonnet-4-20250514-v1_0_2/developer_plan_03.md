# Developer Plan #3 - anthropic.claude-sonnet-4-20250514-v1:0

**Task ID:** webshaper_26  
**Model:** anthropic.claude-sonnet-4-20250514-v1:0  
**Plan Index:** 3  
**Timestamp:** 2025-08-07 09:37:24

## Plan Content
```
Search for biographical information about Edward P. Meany to determine his date of death and verify his prosecuting attorney service until 1898. Focus on finding detailed biographical records, obituaries, death certificates, or historical documents that confirm both his death date and his specific role as a prosecuting attorney in New Jersey. Search for keywords including 'Edward P. Meany death date obituary', 'Edward P. Meany New Jersey prosecutor biography', 'Edward P. Meany died when', and cross-reference with New Jersey historical records and legal directories from the 1890s.
```

## Plan Description
```
This is the necessary next step because: (1) The previous research identified Edward P. Meany as the most viable candidate who was a 1900 Democratic National Convention delegate from New Jersey connected to Philippines annexation opposition, (2) We need to confirm his death date to complete the TASK and verify his prosecuting attorney service until 1898, (3) Expected outcome is to find definitive biographical information including his death date and confirmation of his prosecutorial role, (4) This will provide the final answer needed to complete the TASK successfully
```

## Retrieved Episodic Memory Examples
```
### Development Step 4: Identify Witnesses in 1933 Dillinger Fake-Credentials Jailbreak, Sheriff’s Death, and Pierpont-Bridgewater Convictions

**Description**: Search specifically for information about the 1933 jailbreak involving fake official credentials and a disputed escape plan found on John Dillinger that resulted in the death of a sheriff and led to Harry Pierpont's conviction. Focus on identifying who provided testimony in this case and cross-reference with any testimony that also helped convict other gang leaders from the Pierpont-Bridgewater-Northern gang. Search for keywords including '1933 jailbreak John Dillinger fake credentials', 'Harry Pierpont sheriff death conviction', 'Lima Ohio jail break 1933', 'Dillinger escape plan testimony', and 'witness testimony Pierpont conviction'.

**Use Cases**:
- Legal case preparation for defense attorneys researching witness testimony and trial records from the 1933 Dillinger jailbreak to identify procedural errors or new exculpatory evidence.
- Academic criminal history analysis for a university professor compiling and categorizing primary sources on Harry Pierpont’s conviction and related gang trials for a peer-reviewed journal article.
- True-crime journalism deep dive to automate aggregation of newspaper archives, court transcripts, and eyewitness accounts around the Lima, Ohio jailbreak and sheriff’s death for an investigative series.
- Museum exhibit content curation to source and verify authentic trial documents, testimonies, and photos for an interactive Prohibition-era crime display on John Dillinger and his associates.
- Genealogy and family-history research for descendants tracing ancestral connections to the Pierpont-Bridgewater-Northern gang through court records and witness lists from 1933.
- Digital archiving and preservation for a historical society automating the discovery and categorization of scanned legal filings, trial transcripts, and newspaper clippings relating to the sheriff’s shooting.
- Law-enforcement training module development to build detailed case studies on investigative techniques, fake credentials methods, and witness testimony cross-referencing used in the Pierpont trial for modern detective academies.

```
import os
import requests
import json
from datetime import datetime

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print("API key found, proceeding with search for 1933 Dillinger jailbreak information...")
    print("Target: Identify testimony that convicted Harry Pierpont and other gang leaders")
    print("=" * 80)

# Define targeted search queries for the 1933 jailbreak case
search_queries = [
    '1933 jailbreak John Dillinger fake credentials Harry Pierpont',
    'Lima Ohio jail break 1933 sheriff death Harry Pierpont conviction',
    'Dillinger escape plan testimony witness Harry Pierpont trial',
    'Harry Pierpont conviction testimony 1933 jailbreak sheriff killed',
    'Pierpont-Bridgewater-Northern gang witness testimony convictions',
    '1933 Lima Ohio jailbreak fake official credentials sheriff death',
    'John Dillinger disputed escape plan Harry Pierpont trial testimony',
    'witness testimony Pierpont conviction gang leaders 1933'
]

print(f"Starting comprehensive search with {len(search_queries)} targeted queries...")
print("Focus: 1933 jailbreak, fake credentials, sheriff death, Harry Pierpont conviction, witness testimony")
print("=" * 80)

# Store all search results for analysis
all_results = []

# Perform searches with different targeted queries
for i, query in enumerate(search_queries, 1):
    print(f"\nSearch {i}/{len(search_queries)}: {query}")
    print("-" * 70)
    
    # Prepare API request parameters
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "google_domain": "google.com",
        "safe": "off",
        "num": 12,  # Get sufficient results for comprehensive analysis
        "type": "search"
    }
    
    try:
        # Make API request to SerpAPI
        response = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
        
        if response.status_code == 200:
            results = response.json()
            
            if results.get("organic_results"):
                print(f"Found {len(results['organic_results'])} results for search {i}")
                
                # Process and display key results
                for j, result in enumerate(results["organic_results"], 1):
                    title = result.get('title', 'No title')
                    link = result.get('link', 'No link')
                    snippet = result.get('snippet', 'No snippet')
                    
                    print(f"\nResult {j}:")
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Snippet: {snippet}")
                    
                    # Store result with search context
                    all_results.append({
                        'search_number': i,
                        'query_text': query,
                        'result_number': j,
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                    
                    # Highlight potentially relevant results
                    combined_text = f"{title.lower()} {snippet.lower()}"
                    key_indicators = ['testimony', 'witness', 'trial', 'conviction', 'pierpont', 'sheriff', '1933', 'lima', 'jailbreak']
                    if sum(1 for term in key_indicators if term in combined_text) >= 3:
                        print("🎯 HIGHLY RELEVANT - Contains multiple key terms!")
                    
                    print("-" * 40)
            else:
                print(f"No organic results found for search {i}: '{query}'")
                all_results.append({
                    'search_number': i,
                    'query_text': query,
                    'result_number': 0,
                    'title': 'No results',
                    'link': 'N/A',
                    'snippet': 'No results found for this query'
                })
                
        else:
            print(f"Error: API request failed with status {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Error during search {i}: {str(e)}")
        continue
    
    print("\n" + "=" * 80)

# Save comprehensive search results to workspace
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_file = f"workspace/dillinger_1933_jailbreak_search_{timestamp}.json"

with open(results_file, 'w', encoding='utf-8') as f:
    json.dump({
        'search_timestamp': datetime.now().isoformat(),
        'search_focus': '1933 Dillinger jailbreak, fake credentials, Harry Pierpont conviction, witness testimony',
        'total_queries': len(search_queries),
        'total_results': len(all_results),
        'queries_executed': search_queries,
        'all_search_results': all_results
    }, f, indent=2, ensure_ascii=False)

print(f"\n\n📊 COMPREHENSIVE SEARCH SUMMARY:")
print(f"Total targeted queries executed: {len(search_queries)}")
print(f"Total results collected: {len(all_results)}")
print(f"Search results saved to: {results_file}")

# Analyze results for key testimony and conviction information
print("\n\n🔍 ANALYZING RESULTS FOR KEY TESTIMONY AND CONVICTION DETAILS:")
print("=" * 70)

# Look for results specifically mentioning testimony, trials, or convictions
testimony_results = []
pierpont_results = []
lima_jailbreak_results = []

for result in all_results:
    if result['title'] == 'No results':
        continue
        
    title_lower = result['title'].lower()
    snippet_lower = result['snippet'].lower()
    combined = f"{title_lower} {snippet_lower}"
    
    # Categorize results by relevance
    if any(term in combined for term in ['testimony', 'witness', 'trial', 'testified']):
        testimony_results.append(result)
        
    if 'pierpont' in combined:
        pierpont_results.append(result)
        
    if any(term in combined for term in ['lima', 'jailbreak', '1933']):
        lima_jailbreak_results.append(result)

print(f"\n📋 CATEGORIZED RESULTS:")
print(f"Results mentioning testimony/witnesses: {len(testimony_results)}")
print(f"Results mentioning Harry Pierpont: {len(pierpont_results)}")
print(f"Results mentioning Lima/jailbreak/1933: {len(lima_jailbreak_results)}")

# Display most promising results for testimony identification
print("\n\n🎯 MOST PROMISING RESULTS FOR TESTIMONY IDENTIFICATION:")
print("=" * 60)

if testimony_results:
    print("\n📝 TESTIMONY-RELATED RESULTS:")
    for i, result in enumerate(testimony_results[:5], 1):  # Show top 5
        print(f"\n{i}. {result['title']}")
        print(f"   Query: {result['query_text']}")
        print(f"   Link: {result['link']}")
        print(f"   Snippet: {result['snippet']}")
        print(f"   Search #{result['search_number']}, Result #{result['result_number']}")

if pierpont_results:
    print("\n\n👤 HARRY PIERPONT-RELATED RESULTS:")
    for i, result in enumerate(pierpont_results[:3], 1):  # Show top 3
        print(f"\n{i}. {result['title']}")
        print(f"   Query: {result['query_text']}")
        print(f"   Link: {result['link']}")
        print(f"   Snippet: {result['snippet']}")

print(f"\n\n📁 Next step: Analyze detailed results in {results_file}")
print("🎯 Goal: Identify specific witness who testified in Harry Pierpont's conviction")
print("🔍 Focus: Cross-reference testimony that convicted multiple gang leaders")
print("\n🏁 Search phase complete - ready for detailed analysis of historical testimony records!")
```

### Development Step 13: Locate and Confirm Chen Boda’s Death Year from Reliable Biographical Sources

**Description**: Search for the death year of Chen Boda, who was born in Hui'an County, Fujian Province (a region known for China's national intangible cultural heritage stone carving techniques), authored extensive critiques against Chiang Kai-shek's political works, and served as Mao Zedong's chief interpreter and ghostwriter. Focus on finding reliable biographical information about Chen Boda's death date, including searches for 'Chen Boda death year', 'Chen Boda biography died', and 'Chen Boda 陈伯达 death date'. Cross-reference multiple sources to confirm the exact year of his death.

**Use Cases**:
- Genealogy research automation for family historians: extracting and verifying death dates of ancestors from digitized local archives and memorial websites.
- Historical archive metadata enrichment for librarians: automatically identifying and updating death year fields in digital collections of political figures’ biographies.
- Academic research on political elite longevity: aggregating and cross-referencing death years of mid-20th century Chinese leaders to study lifespan patterns.
- Journalistic fact-checking for obituary writing: quickly confirming the death date of prominent figures by scanning saved news article HTML and authoritative biographical sources.
- Educational publishing timeline validation: ensuring history textbook publishers have accurate death years for Mao Zedong’s inner circle when compiling political chronology.
- Cultural heritage database curation: verifying biographical details (including death year) of practitioners in regional stone carving traditions to maintain national intangible cultural heritage records.
- Compliance due-diligence in international partnerships: risk analysts confirming the life status and death information of prospective foreign business associates with politically sensitive backgrounds.

```
import os
import json
from bs4 import BeautifulSoup
import re
from collections import Counter

print('=== ANALYZING SAVED HTML FILES FOR CHEN BODA DEATH YEAR ===') 
print('Fixing BeautifulSoup import error and analyzing previously saved search results\n')

# First, let's inspect what files we have in the workspace
workspace_dir = 'workspace'
html_files = []
json_files = []

if os.path.exists(workspace_dir):
    for filename in os.listdir(workspace_dir):
        if filename.endswith('.html') and 'chen_boda' in filename:
            html_files.append(filename)
        elif filename.endswith('.json') and 'chen_boda' in filename:
            json_files.append(filename)
    
    print(f'Found {len(html_files)} HTML files and {len(json_files)} JSON files:')
    for i, filename in enumerate(html_files, 1):
        print(f'  HTML {i}. {filename}')
    for i, filename in enumerate(json_files, 1):
        print(f'  JSON {i}. {filename}')
else:
    print('❌ Workspace directory not found')
    html_files = []
    json_files = []

# First, let's inspect the JSON file structure if it exists
if json_files:
    json_file = os.path.join(workspace_dir, json_files[0])
    print(f'\n📋 INSPECTING JSON FILE STRUCTURE: {json_files[0]}')
    print('-' * 60)
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        print('JSON file keys:')
        for key in json_data.keys():
            print(f'  • {key}: {type(json_data[key])}')
            if isinstance(json_data[key], list):
                print(f'    Length: {len(json_data[key])}')
            elif isinstance(json_data[key], dict):
                print(f'    Sub-keys: {list(json_data[key].keys())}')
        
        print(f'\nJSON content preview:')
        print(f'  Target person: {json_data.get("target_person", "Not found")}')
        print(f'  Objective: {json_data.get("objective", "Not found")}')
        print(f'  Total queries: {len(json_data.get("queries", []))}')
        print(f'  Results collected: {len(json_data.get("results", []))}')
        
    except Exception as e:
        print(f'Error reading JSON file: {str(e)}')

if not html_files:
    print('❌ No HTML search result files found to analyze')
    print('Need to execute searches first or check workspace directory')
else:
    print(f'\n📁 ANALYZING {len(html_files)} HTML FILES FOR CHEN BODA DEATH INFORMATION:')
    print('=' * 80)
    
    # Initialize analysis results
    analysis_results = {
        'timestamp': '2025-01-07',
        'files_analyzed': len(html_files),
        'chen_boda_mentions': [],
        'death_information': [],
        'biographical_data': [],
        'year_mentions': [],
        'chinese_content': [],
        'potential_death_years': []
    }
    
    # Analyze each HTML file
    for i, filename in enumerate(html_files, 1):
        filepath = os.path.join(workspace_dir, filename)
        print(f'\nAnalyzing File {i}: {filename}')
        print('-' * 50)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML with BeautifulSoup (now properly imported)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract all text content
            page_text = soup.get_text(separator=' ', strip=True)
            page_text_lower = page_text.lower()
            
            print(f'HTML file size: {len(html_content):,} characters')
            print(f'Extracted text size: {len(page_text):,} characters')
            
            # Look for Chen Boda mentions (both English and Chinese)
            chen_boda_indicators = {
                'chen boda': 0,
                '陈伯达': 0,
                'chen po-ta': 0,
                'chen po ta': 0
            }
            
            chen_boda_found = False
            for indicator in chen_boda_indicators.keys():
                count = page_text_lower.count(indicator)
                chen_boda_indicators[indicator] = count
                if count > 0:
                    chen_boda_found = True
            
            print(f'Chen Boda mentions: {chen_boda_indicators}')
            
            if chen_boda_found:
                print('✅ Chen Boda mentioned in this file')
                
                # Look for death-related information
                death_keywords = ['death', 'died', 'obituary', 'passed away', 'demise', '死亡', '逝世', '去世']
                death_info_found = []
                
                for keyword in death_keywords:
                    if keyword in page_text_lower:
                        # Find sentences containing the death keyword
                        sentences = re.split(r'[.!?。！？]', page_text)
                        for sentence in sentences:
                            if keyword in sentence.lower() and len(sentence.strip()) > 10:
                                # Check if Chen Boda is mentioned in the same sentence or nearby
                                sentence_lower = sentence.lower()
                                if any(indicator in sentence_lower for indicator in chen_boda_indicators.keys()):
                                    death_info_found.append({
                                        'keyword': keyword,
                                        'sentence': sentence.strip()[:300],
                                        'context': 'same_sentence'
                                    })
                                    break
                
                if death_info_found:
                    print(f'💀 Death information found: {len(death_info_found)} instances')
                    for j, info in enumerate(death_info_found, 1):
                        print(f'  {j}. Keyword: {info["keyword"]}')
                        print(f'     Sentence: {info["sentence"]}...')
                    analysis_results['death_information'].extend(death_info_found)
                else:
                    print('❓ No direct death information found in sentences with Chen Boda')
                
                # Look for year patterns (1900-2025)
                year_pattern = re.compile(r'\b(19\d{2}|20[0-2]\d)\b')
                years_found = year_pattern.findall(page_text)
                
                if years_found:
                    year_counts = Counter(years_found)
                    print(f'📅 Years mentioned: {dict(year_counts.most_common(10))}')
                    
                    # Look for years near death-related words
                    potential_death_years = []
                    for year in set(years_found):
                        for death_word in death_keywords[:5]:  # Check main English death words
                            # Find positions of year and death word
                            year_positions = [m.start() for m in re.finditer(year, page_text)]
                            death_positions = [m.start() for m in re.finditer(death_word, page_text_lower)]
                            
                            for year_pos in year_positions:
                                for death_pos in death_positions:
                                    distance = abs(year_pos - death_pos)
                                    if distance < 100:  # Within 100 characters
                                        context = page_text[max(0, min(year_pos, death_pos)-50):max(year_pos, death_pos)+100]
                                        potential_death_years.append({
                                            'year': year,
                                            'death_word': death_word,
                                            'distance': distance,
                                            'context': context.strip()
                                        })
                    
                    if potential_death_years:
                        print(f'🎯 Potential death years found: {len(potential_death_years)}')
                        for death_year in potential_death_years[:3]:  # Show top 3
                            print(f'  • {death_year["year"]} (near "{death_year["death_word"]}", distance: {death_year["distance"]} chars)')
                            print(f'    Context: {death_year["context"][:150]}...')
                        analysis_results['potential_death_years'].extend(potential_death_years)
                    
                    analysis_results['year_mentions'].extend(years_found)
                
                # Look for biographical information
                bio_keywords = ['born', 'birth', 'biography', 'biographical', 'life', 'career', '出生', '生平', '传记']
                bio_info = []
                
                for keyword in bio_keywords:
                    if keyword in page_text_lower:
                        sentences = re.split(r'[.!?。！？]', page_text)
                        for sentence in sentences:
                            if keyword in sentence.lower() and len(sentence.strip()) > 15:
                                sentence_lower = sentence.lower()
                                if any(indicator in sentence_lower for indicator in chen_boda_indicators.keys()):
                                    bio_info.append({
                                        'keyword': keyword,
                                        'sentence': sentence.strip()[:250]
                                    })
                                    break
                
                if bio_info:
                    print(f'📖 Biographical information found: {len(bio_info)} instances')
                    for info in bio_info[:2]:  # Show first 2
                        print(f'  • {info["keyword"]}: {info["sentence"]}...')
                    analysis_results['biographical_data'].extend(bio_info)
                
                # Store Chen Boda mention info
                analysis_results['chen_boda_mentions'].append({
                    'filename': filename,
                    'mentions': chen_boda_indicators,
                    'total_mentions': sum(chen_boda_indicators.values()),
                    'death_info_count': len(death_info_found),
                    'bio_info_count': len(bio_info),
                    'years_found': len(years_found),
                    'potential_death_years': len(potential_death_years) if 'potential_death_years' in locals() else 0
                })
                
            else:
                print('❌ No Chen Boda mentions found in this file')
                
        except Exception as e:
            print(f'Error analyzing {filename}: {str(e)}')
    
    print('\n' + '=' * 80)
    print('COMPREHENSIVE CHEN BODA DEATH YEAR ANALYSIS SUMMARY')
    print('=' * 80)
    
    # Summarize findings
    total_chen_boda_mentions = sum(mention['total_mentions'] for mention in analysis_results['chen_boda_mentions'])
    total_death_info = len(analysis_results['death_information'])
    total_bio_info = len(analysis_results['biographical_data'])
    total_potential_death_years = len(analysis_results['potential_death_years'])
    
    print(f'📊 ANALYSIS SUMMARY:')
    print(f'   • Files analyzed: {analysis_results["files_analyzed"]}')
    print(f'   • Total Chen Boda mentions: {total_chen_boda_mentions}')
    print(f'   • Death information instances: {total_death_info}')
    print(f'   • Biographical information instances: {total_bio_info}')
    print(f'   • Potential death years identified: {total_potential_death_years}')
    
    # Analyze potential death years
    if analysis_results['potential_death_years']:
        print(f'\n💀 DEATH YEAR ANALYSIS:')
        death_year_counts = Counter([item['year'] for item in analysis_results['potential_death_years']])
        print('Most frequently mentioned years near death-related terms:')
        for year, count in death_year_counts.most_common(5):
            print(f'  • {year}: {count} occurrences')
        
        # Show best death year candidates
        print(f'\n🎯 BEST DEATH YEAR CANDIDATES:')
        # Sort by proximity to death words (smaller distance = better)
        sorted_candidates = sorted(analysis_results['potential_death_years'], key=lambda x: x['distance'])
        
        for i, candidate in enumerate(sorted_candidates[:3], 1):
            print(f'\n{i}. YEAR: {candidate["year"]} (Distance: {candidate["distance"]} characters from "{candidate["death_word"]}")')
            print(f'   Context: {candidate["context"][:200]}...')
        
        # Determine most likely death year
        if death_year_counts:
            most_likely_year = death_year_counts.most_common(1)[0]
            print(f'\n🏆 MOST LIKELY DEATH YEAR: {most_likely_year[0]} ({most_likely_year[1]} mentions near death terms)')
    
    # Show best death information
    if analysis_results['death_information']:
        print(f'\n💀 DEATH INFORMATION FOUND:')
        for i, info in enumerate(analysis_results['death_information'][:3], 1):
            print(f'\n{i}. Keyword: {info["keyword"]}') 
            print(f'   Sentence: {info["sentence"]}')
    
    # Show biographical information
    if analysis_results['biographical_data']:
        print(f'\n📖 BIOGRAPHICAL INFORMATION:')
        for i, info in enumerate(analysis_results['biographical_data'][:3], 1):
            print(f'\n{i}. Keyword: {info["keyword"]}')
            print(f'   Content: {info["sentence"]}')
    
    # All years mentioned analysis
    if analysis_results['year_mentions']:
        all_years = Counter(analysis_results['year_mentions'])
        print(f'\n📅 ALL YEARS MENTIONED IN CHEN BODA CONTENT:')
        for year, count in all_years.most_common(10):
            print(f'  • {year}: {count} mentions')
    
    # Calculate confidence score
    confidence_score = 0
    if total_chen_boda_mentions > 0: confidence_score += 20
    if total_death_info > 0: confidence_score += 30
    if total_potential_death_years > 0: confidence_score += 25
    if total_bio_info > 0: confidence_score += 15
    if len(set([item['year'] for item in analysis_results['potential_death_years']])) == 1: confidence_score += 10  # Consistent year
    
    print(f'\n📈 CONFIDENCE SCORE: {confidence_score}/100')
    
    # Final conclusion
    print('\n' + '=' * 80)
    print('FINAL CONCLUSION ON CHEN BODA DEATH YEAR')
    print('=' * 80)
    
    if confidence_score >= 50:
        if analysis_results['potential_death_years']:
            death_year_counts = Counter([item['year'] for item in analysis_results['potential_death_years']])
            most_likely = death_year_counts.most_common(1)[0]
            print(f'✅ HIGH CONFIDENCE RESULT:')
            print(f'   Chen Boda likely died in: {most_likely[0]}')
            print(f'   Evidence strength: {most_likely[1]} mentions near death-related terms')
            print(f'   Confidence level: {confidence_score}/100')
        else:
            print('❓ Chen Boda information found but death year unclear')
    else:
        print('❌ INSUFFICIENT EVIDENCE:')
        print('   Unable to determine Chen Boda\'s death year from current search results')
        print('   Recommend additional searches or different sources')
    
    # Save comprehensive analysis
    results_file = os.path.join(workspace_dir, 'chen_boda_death_analysis.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    
    print(f'\n💾 COMPREHENSIVE ANALYSIS SAVED TO: {results_file}')

print('\n=== CHEN BODA DEATH YEAR HTML ANALYSIS COMPLETE ===')
```

### Development Step 12: Confirm Chen Boda’s Death Year Using Multiple Biographical Sources

**Description**: Search for the death year of Chen Boda, who was born in Hui'an County, Fujian Province (a region known for China's national intangible cultural heritage stone carving techniques), authored extensive critiques against Chiang Kai-shek's political works, and served as Mao Zedong's chief interpreter and ghostwriter. Focus on finding reliable biographical information about Chen Boda's death date, including searches for 'Chen Boda death year', 'Chen Boda biography died', and 'Chen Boda 陈伯达 death date'. Cross-reference multiple sources to confirm the exact year of his death.

**Use Cases**:
- Automated verification of executive biographical data for corporate websites, ensuring accurate tenure and death dates are displayed in leadership profiles
- Genealogical research data gathering by extracting ancestors’ birth and death years from multiple online archives and historical forums
- Academic historian workflow to compile and cross-reference scholars’ life spans for publication footnotes and citation databases
- Legal due-diligence automation to confirm a decedent’s death year from public obituaries and government notices when processing estate settlements
- Museum digital catalog enrichment by scraping artists’ biographical death dates from art history repositories and cultural heritage sites
- Journalistic obituary preparation tool that retrieves and validates prominent figures’ death years across news outlets and official statements
- Healthcare compliance system to flag and remove deceased patients from active records by automatically detecting death announcements online
- Marketing timeline creation for brand anniversaries, gathering company founders’ life spans from business registries and press releases

```
import os
import requests
import json
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

print('=== SEARCHING FOR CHEN BODA DEATH YEAR ===') 
print('Target: Chen Boda (陈伯达) - Mao Zedong\'s chief interpreter and ghostwriter')
print('Born: Hui\'an County, Fujian Province')
print('Known for: Critiques against Chiang Kai-shek, stone carving heritage region')
print('Objective: Find reliable death year information\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Define targeted search queries for Chen Boda's death information
search_queries = [
    'Chen Boda death year died',
    'Chen Boda 陈伯达 death date biography',
    'Chen Boda Mao Zedong interpreter death',
    'Chen Boda Fujian Hui\'an death year',
    'Chen Boda ghostwriter died when',
    '陈伯达 死亡 年份',
    'Chen Boda obituary death',
    'Chen Boda biographical death date'
]

print(f'Executing {len(search_queries)} targeted searches for Chen Boda death information:')
for i, query in enumerate(search_queries, 1):
    print(f'  {i}. {query}')

# Headers for web requests to avoid blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Initialize results storage
search_results = {
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'target_person': 'Chen Boda (陈伯达)',
    'objective': 'Find death year of Chen Boda',
    'queries': search_queries,
    'results': [],
    'death_year_candidates': [],
    'biographical_info': [],
    'analysis': {}
}

print('\n=== EXECUTING DUCKDUCKGO SEARCHES ===') 
print('=' * 60)

# Function to extract and analyze search results for biographical information
def analyze_biographical_content(html_content, query):
    """Extract and analyze biographical search results from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    results = []
    
    # Look for various result container patterns
    result_containers = soup.find_all(['div', 'article'], class_=lambda x: x and any(term in str(x).lower() for term in ['result', 'web-result', 'links_main']))
    
    if not result_containers:
        # Fallback: look for any links that might be results
        result_containers = soup.find_all('a', href=True)
    
    for container in result_containers[:20]:  # Check more results for biographical info
        try:
            # Extract title
            title_elem = container.find(['h2', 'h3', 'a']) or container
            title = title_elem.get_text().strip() if title_elem else 'No title'
            
            # Extract link
            link_elem = container.find('a', href=True) or (container if container.name == 'a' else None)
            link = link_elem.get('href') if link_elem else 'No link'
            
            # Extract snippet/description
            snippet_elem = container.find(['p', 'span', 'div'], class_=lambda x: x and 'snippet' in str(x).lower()) or container.find('p')
            snippet = snippet_elem.get_text().strip() if snippet_elem else 'No snippet'
            
            # Skip if no meaningful content
            if len(title) < 5 or title == 'No title':
                continue
                
            # Calculate relevance score for biographical information
            combined_text = f'{title} {snippet} {link}'.lower()
            
            relevance_score = 0
            matched_terms = []
            death_indicators = []
            
            # Key terms for Chen Boda biographical information
            key_terms = {
                'chen boda': 5,
                '陈伯达': 5,
                'death': 4,
                'died': 4,
                'death year': 5,
                'obituary': 4,
                'biography': 3,
                'biographical': 3,
                'mao zedong': 2,
                'interpreter': 2,
                'ghostwriter': 2,
                'fujian': 2,
                'hui\'an': 2,
                'chiang kai-shek': 2,
                'critique': 1,
                'born': 2,
                'life': 1
            }
            
            # Look for specific death year patterns
            import re
            year_patterns = re.findall(r'\b(19\d{2}|20\d{2})\b', combined_text)
            
            for term, weight in key_terms.items():
                if term in combined_text:
                    relevance_score += weight
                    matched_terms.append(term)
            
            # Check for death-related year mentions
            death_words = ['death', 'died', 'obituary', 'passed away', 'demise']
            for year in year_patterns:
                for death_word in death_words:
                    if death_word in combined_text:
                        # Check if year appears near death word (within 50 characters)
                        death_pos = combined_text.find(death_word)
                        year_pos = combined_text.find(year)
                        if abs(death_pos - year_pos) < 50:
                            death_indicators.append(f'{year} (near "{death_word}")')
                            relevance_score += 3
            
            if relevance_score > 0:  # Only include results with some relevance
                results.append({
                    'title': title[:250],
                    'link': link,
                    'snippet': snippet[:400],
                    'relevance_score': relevance_score,
                    'matched_terms': matched_terms,
                    'death_indicators': death_indicators,
                    'years_mentioned': year_patterns,
                    'query': query
                })
                
        except Exception as e:
            continue  # Skip problematic results
    
    return results

# Execute searches for Chen Boda death information
for i, query in enumerate(search_queries, 1):
    print(f'\nSearch {i}/{len(search_queries)}: {query}')
    print('-' * 50)
    
    try:
        # Construct DuckDuckGo search URL
        search_url = f'https://html.duckduckgo.com/html/?q={quote_plus(query)}'
        
        print(f'Requesting: {search_url}')
        response = requests.get(search_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f'✅ Successfully retrieved search results (Status: {response.status_code})')
            
            # Save raw HTML for reference
            html_filename = f'chen_boda_search_{i}_{query.replace(" ", "_").replace("\'", "")[:30]}.html'
            html_filepath = os.path.join('workspace', html_filename)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Raw HTML saved to: {html_filepath}')
            
            # Analyze search results
            search_results_batch = analyze_biographical_content(response.text, query)
            
            print(f'Extracted {len(search_results_batch)} relevant results')
            
            # Display high-relevance results
            high_relevance = [r for r in search_results_batch if r['relevance_score'] >= 8]
            moderate_relevance = [r for r in search_results_batch if 5 <= r['relevance_score'] < 8]
            
            if high_relevance:
                print(f'\n🎯 HIGH RELEVANCE RESULTS ({len(high_relevance)}):') 
                for j, result in enumerate(high_relevance, 1):
                    print(f'  {j}. Score: {result["relevance_score"]} | {result["title"][:100]}...')
                    print(f'     Terms: {", ".join(result["matched_terms"][:8])}')
                    print(f'     Death indicators: {result["death_indicators"]}')
                    print(f'     Years mentioned: {result["years_mentioned"]}')
                    print(f'     Link: {result["link"]}')
                    print(f'     Snippet: {result["snippet"][:200]}...')
                    print()
            
            if moderate_relevance:
                print(f'\n⭐ MODERATE RELEVANCE RESULTS ({len(moderate_relevance)}):') 
                for j, result in enumerate(moderate_relevance[:3], 1):  # Show top 3
                    print(f'  {j}. Score: {result["relevance_score"]} | {result["title"][:80]}...')
                    print(f'     Terms: {", ".join(result["matched_terms"][:5])}')
                    print(f'     Death indicators: {result["death_indicators"]}')
                    print(f'     Years: {result["years_mentioned"]}')
            
            # Store results
            search_results['results'].extend(search_results_batch)
            
            # Identify death year candidates
            death_candidates = [r for r in search_results_batch if r['death_indicators'] or 
                              (r['relevance_score'] >= 6 and any(term in r['matched_terms'] for term in ['death', 'died']))]
            
            if death_candidates:
                print(f'\n💀 DEATH YEAR CANDIDATES FOUND ({len(death_candidates)}):') 
                for candidate in death_candidates:
                    print(f'  • {candidate["title"][:120]}...')
                    print(f'    Score: {candidate["relevance_score"]} | Death indicators: {candidate["death_indicators"]}')
                    print(f'    Years: {candidate["years_mentioned"]} | Terms: {", ".join(candidate["matched_terms"][:5])}')
                    search_results['death_year_candidates'].append(candidate)
                    
        else:
            print(f'❌ Request failed with status: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error in search {i}: {str(e)}')
    
    print(f'Completed search {i}/{len(search_queries)}')
    time.sleep(3)  # Rate limiting

print('\n' + '=' * 80)
print('COMPREHENSIVE ANALYSIS OF CHEN BODA DEATH YEAR SEARCH')
print('=' * 80)

# Sort all results by relevance score
search_results['results'].sort(key=lambda x: x['relevance_score'], reverse=True)

total_results = len(search_results['results'])
print(f'Total results collected: {total_results}')
print(f'Death year candidates: {len(search_results["death_year_candidates"])}')

if search_results['results']:
    print('\n🏆 TOP 10 HIGHEST SCORING RESULTS:') 
    print('-' * 50)
    
    for i, result in enumerate(search_results['results'][:10], 1):
        print(f'{i:2d}. Score: {result["relevance_score"]} | Query: {result["query"]}')
        print(f'    Title: {result["title"][:120]}...')
        print(f'    Terms: {", ".join(result["matched_terms"][:6])}')
        print(f'    Death indicators: {result["death_indicators"]}')
        print(f'    Years mentioned: {result["years_mentioned"]}')
        print(f'    Link: {result["link"]}')
        print(f'    Snippet: {result["snippet"][:150]}...')
        print()

# Analyze death year patterns
all_death_indicators = []
all_years_mentioned = []

for result in search_results['results']:
    all_death_indicators.extend(result['death_indicators'])
    all_years_mentioned.extend(result['years_mentioned'])

from collections import Counter
death_year_frequency = Counter(all_death_indicators)
year_frequency = Counter(all_years_mentioned)

print('\n📊 DEATH YEAR ANALYSIS:')
print('-' * 30)
if death_year_frequency:
    print('Death indicators found:')
    for indicator, count in death_year_frequency.most_common(10):
        print(f'  {indicator}: {count} occurrences')
else:
    print('No specific death indicators found in search results')

print('\nAll years mentioned in results:')
for year, count in year_frequency.most_common(15):
    print(f'  {year}: {count} occurrences')

# Focus on high-confidence death year candidates
print('\n🔍 ANALYZING HIGH-CONFIDENCE DEATH YEAR CANDIDATES:')
print('-' * 60)

high_confidence_death = [r for r in search_results['results'] if r['relevance_score'] >= 8 and r['death_indicators']]
if high_confidence_death:
    for result in high_confidence_death:
        print(f'\nHigh-confidence result: {result["title"][:150]}...')
        print(f'Score: {result["relevance_score"]} | Query: {result["query"]}')
        print(f'Death indicators: {result["death_indicators"]}')
        print(f'All years mentioned: {result["years_mentioned"]}')
        print(f'Matched terms: {", ".join(result["matched_terms"])}')
        print(f'Full snippet: {result["snippet"]}')
        print(f'Link: {result["link"]}')
        print('-' * 40)
else:
    print('No high-confidence death year candidates found.')
    print('Showing moderate confidence results:')
    moderate_confidence = [r for r in search_results['results'] if r['relevance_score'] >= 5][:5]
    for result in moderate_confidence:
        print(f'\nModerate result: {result["title"][:150]}...')
        print(f'Score: {result["relevance_score"]} | Query: {result["query"]}')
        print(f'Death indicators: {result["death_indicators"]}')
        print(f'Years mentioned: {result["years_mentioned"]}')
        print(f'Matched terms: {", ".join(result["matched_terms"][:8])}')
        print(f'Snippet: {result["snippet"][:250]}...')
        print(f'Link: {result["link"]}')
        print('-' * 40)

# Save comprehensive results
results_file = os.path.join('workspace', 'chen_boda_death_year_search.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE RESULTS SAVED TO: {results_file}')

# Summary statistics
search_results['analysis'] = {
    'total_results': total_results,
    'high_relevance_count': len([r for r in search_results['results'] if r['relevance_score'] >= 8]),
    'moderate_relevance_count': len([r for r in search_results['results'] if 5 <= r['relevance_score'] < 8]),
    'death_candidates_count': len(search_results['death_year_candidates']),
    'death_indicators_found': len(all_death_indicators),
    'unique_years_mentioned': len(set(all_years_mentioned)),
    'most_common_death_indicators': dict(death_year_frequency.most_common(3)),
    'most_common_years': dict(year_frequency.most_common(5))
}

print(f'\n📈 FINAL STATISTICS:')
print(f'   • Total results: {search_results["analysis"]["total_results"]}')
print(f'   • High relevance (8+): {search_results["analysis"]["high_relevance_count"]}')
print(f'   • Moderate relevance (5-7): {search_results["analysis"]["moderate_relevance_count"]}')
print(f'   • Death year candidates: {search_results["analysis"]["death_candidates_count"]}')
print(f'   • Death indicators found: {search_results["analysis"]["death_indicators_found"]}')
print(f'   • Unique years mentioned: {search_results["analysis"]["unique_years_mentioned"]}')
print(f'   • Most common years: {list(search_results["analysis"]["most_common_years"].keys())}')

print('\n🎯 PRELIMINARY FINDINGS:')
if search_results['analysis']['death_indicators_found'] > 0:
    print('✅ Death-related information found in search results')
    print('✅ Specific death year indicators identified')
    if search_results['analysis']['most_common_death_indicators']:
        most_likely = list(search_results['analysis']['most_common_death_indicators'].keys())[0]
        print(f'✅ Most frequently mentioned death indicator: {most_likely}')
else:
    print('❓ No specific death indicators found - may need more targeted searches')
    print('❓ Consider searching biographical databases or academic sources')

print('\n📋 NEXT STEPS:')
print('1. 🔍 Review saved HTML files for additional biographical context')
print('2. 🔍 Follow up on high-relevance links for detailed biographical information') 
print('3. 🔍 Cross-reference multiple sources to confirm death year')
print('4. 🔍 Search academic databases or Chinese biographical sources')
print('5. 🔍 Look for obituaries or official death announcements')

print('\n=== CHEN BODA DEATH YEAR SEARCH PHASE COMPLETE ===')
```
```

## Development History
*(This section will be updated as development progresses)*

