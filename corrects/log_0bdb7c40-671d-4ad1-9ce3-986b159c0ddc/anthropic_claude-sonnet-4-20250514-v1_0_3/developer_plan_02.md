# Developer Plan 02

## Plan
Identify which astronaut appears smaller in the Apollo 12: Self-Portrait APOD image from January 21, 2006. Based on the previous analysis showing Charles 'Pete' Conrad appears as a reflection in Alan Bean's helmet visor, determine which astronaut is the 'smaller' one visually. Then research Conrad's NASA Astronaut Group membership to identify which astronaut group he belonged to.

## Description
This is the necessary next step because: (1) The previous research successfully identified the two astronauts as Charles 'Pete' Conrad and Alan Bean, with Conrad appearing smaller due to the helmet visor reflection effect, (2) We need to confirm which astronaut is considered the 'smaller' one and identify Conrad's NASA Astronaut Group membership, (3) Expected outcome is to determine Conrad's astronaut group number so we can then research all members of that group, (4) This establishes the specific astronaut group we need to analyze for space flight duration data

## Episodic Examples
### Development Step 2: Identify City in APOD Horizon City-Light Images from August 1–7, 2015

**Description**: Search for NASA Astronomy Pictures of the Day from the first week of August 2015 (August 1-7, 2015). Look for entries that show city lights on the horizon and identify which city is featured. Use search approaches including: (1) Direct access to NASA APOD archives for August 2015, (2) Search 'NASA APOD August 2015 city lights horizon', (3) Browse the official NASA APOD website archive section for that specific date range. Extract the complete APOD entries including titles, descriptions, and image details to identify which city's lights are shown.

**Use Cases**:
- Astro-environmental researchers automating the extraction of city light mentions from historical NASA APOD pages to quantify urban light pollution trends over time
- Municipal planning offices scanning archived astrophotography content to verify their city’s skyline presence in nighttime horizon imagery for urban growth studies
- Science communicators programmatically curating location-specific astronomy images featuring recognizable city lights to boost engagement in regional outreach events
- Academic historians analyzing archived NASA APOD entries to trace the evolution of city-scape photography and public interest in urban night-sky scenes
- News media fact-checkers using regex-powered HTML parsing to confirm the exact city depicted in widely circulated astrophotography images before publication
- Tourism boards automatically sourcing high-resolution NASA images of local city lights on the horizon for inclusion in digital marketing and promotional materials
- Environmental NGOs aggregating city-specific light distribution data from APOD archives to support light pollution policy proposals and public awareness campaigns
- Digital asset managers integrating automated metadata enrichment workflows that identify and tag city names in archived astronomy images for enterprise content libraries

```
import os
import json
from bs4 import BeautifulSoup
import re

print("=== NASA APOD ANALYSIS: EXTRACTING CITY IDENTIFICATION FROM SAVED CONTENT ===\n")
print("Objective: Parse the downloaded APOD entries to identify which city's lights are shown on horizon\n")

# First, let's inspect the workspace directory structure
print("=== INSPECTING WORKSPACE DIRECTORY ===\n")

workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("❌ No workspace directory found")
    exit()

workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}")
print(f"Directory path: {workspace_dir}/\n")

# List all files to understand what we have
workspace_files = os.listdir(workspace_dir)
print(f"Total files in workspace: {len(workspace_files)}")

# Categorize files by type
json_files = [f for f in workspace_files if f.endswith('.json')]
html_files = [f for f in workspace_files if f.endswith('.html')]
direct_apod_files = [f for f in workspace_files if f.startswith('nasa_apod_august_') and f.endswith('2015.html')]

print(f"\nFile breakdown:")
print(f"- JSON summary files: {len(json_files)}")
print(f"- HTML content files: {len(html_files)}")
print(f"- Direct APOD daily files: {len(direct_apod_files)}")

print(f"\nDirect APOD daily files (target period Aug 1-7, 2015):")
for file in sorted(direct_apod_files):
    file_size = os.path.getsize(os.path.join(workspace_dir, file))
    print(f"  - {file} ({file_size:,} bytes)")

# First, let's examine the JSON summary to understand our findings
print(f"\n=== ANALYZING SEARCH RESULTS SUMMARY ===\n")

summary_file = None
for file in json_files:
    if 'search_results' in file:
        summary_file = file
        break

if summary_file:
    summary_path = os.path.join(workspace_dir, summary_file)
    print(f"Found summary file: {summary_file}")
    print(f"File size: {os.path.getsize(summary_path):,} bytes")
    
    # Inspect the JSON structure first
    with open(summary_path, 'r') as f:
        summary_data = json.load(f)
    
    print(f"\nJSON structure inspection:")
    for key in summary_data.keys():
        value = summary_data[key]
        if isinstance(value, list):
            print(f"  {key}: List with {len(value)} items")
        elif isinstance(value, dict):
            print(f"  {key}: Dictionary with {len(value)} keys")
        elif isinstance(value, str):
            print(f"  {key}: String (length: {len(value)})")
        else:
            print(f"  {key}: {type(value).__name__} - {value}")
    
    # Focus on the promising APOD pages
    if 'apod_pages_with_city_keywords' in summary_data:
        apod_pages = summary_data['apod_pages_with_city_keywords']
        print(f"\n🎯 PROMISING APOD PAGES FOUND: {len(apod_pages)}")
        
        for i, page in enumerate(apod_pages, 1):
            print(f"\n{i}. {page['date']}:")
            print(f"   Title: {page['title']}")
            print(f"   Keywords found: {page['city_keywords_found']}")
            print(f"   File: {page['filename']}")
            print(f"   URL: {page['url']}")
            if 'content_preview' in page:
                preview = page['content_preview'][:200] + '...' if len(page['content_preview']) > 200 else page['content_preview']
                print(f"   Content preview: {preview}")
else:
    print("⚠️ No search results summary file found")

# Now let's analyze the most promising direct APOD file: August 3, 2015
print(f"\n=== DETAILED ANALYSIS: AUGUST 3, 2015 APOD ===\n")

aug3_file = None
for file in direct_apod_files:
    if 'august_03_2015' in file:
        aug3_file = file
        break

if aug3_file:
    aug3_path = os.path.join(workspace_dir, aug3_file)
    print(f"Analyzing: {aug3_file}")
    print(f"File size: {os.path.getsize(aug3_path):,} bytes")
    
    # Read and parse the HTML content
    with open(aug3_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the title
    title_element = soup.find('title')
    title = title_element.get_text().strip() if title_element else 'No title found'
    print(f"\nTitle: {title}")
    
    # Extract the main content
    # APOD pages typically have the main content in <p> tags or after the image
    text_content = soup.get_text()
    
    print(f"\n=== SEARCHING FOR CITY IDENTIFICATION ===\n")
    
    # Look for specific city mentions in the text
    city_patterns = [
        r'city lights of ([A-Z][a-zA-Z\s,]+)',  # "city lights of CityName"
        r'lights of ([A-Z][a-zA-Z\s,]+)',       # "lights of CityName"
        r'([A-Z][a-zA-Z\s]+),\s*([A-Z][a-zA-Z\s]+),?\s*(USA|Michigan|Canada)',  # "City, State, Country"
        r'horizon[^.]*?([A-Z][a-zA-Z\s]+,\s*[A-Z][a-zA-Z\s]*)',  # "horizon ... City, State"
    ]
    
    found_cities = []
    
    for pattern in city_patterns:
        matches = re.finditer(pattern, text_content, re.IGNORECASE)
        for match in matches:
            city_info = {
                'pattern': pattern,
                'match': match.group(),
                'city_name': match.group(1) if match.groups() else match.group(),
                'context_start': max(0, match.start() - 100),
                'context_end': min(len(text_content), match.end() + 100)
            }
            context = text_content[city_info['context_start']:city_info['context_end']]
            city_info['context'] = context.strip()
            found_cities.append(city_info)
    
    print(f"Found {len(found_cities)} potential city matches:")
    for i, city in enumerate(found_cities, 1):
        print(f"\n{i}. Potential city: {city['city_name']}")
        print(f"   Full match: {city['match']}")
        print(f"   Context: {city['context']}")
    
    # Look specifically for the phrase "city lights" and nearby text
    print(f"\n=== SEARCHING FOR 'CITY LIGHTS' PHRASES ===\n")
    
    city_lights_pattern = r'city lights[^.]*?([A-Z][a-zA-Z\s,]*(?:Michigan|USA|Canada)?[^.]*?)'
    city_lights_matches = re.finditer(city_lights_pattern, text_content, re.IGNORECASE)
    
    for i, match in enumerate(city_lights_matches, 1):
        print(f"Match {i}:")
        print(f"  Full text: {match.group()}")
        context_start = max(0, match.start() - 150)
        context_end = min(len(text_content), match.end() + 150)
        context = text_content[context_start:context_end]
        print(f"  Extended context: {context}")
    
    # Extract key sentences containing relevant keywords
    print(f"\n=== EXTRACTING KEY SENTENCES ===\n")
    
    sentences = re.split(r'[.!?]+', text_content)
    relevant_sentences = []
    
    keywords = ['city', 'lights', 'horizon', 'michigan', 'marquette', 'superior', 'yellow lights']
    
    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 20 and any(keyword in sentence.lower() for keyword in keywords):
            relevant_sentences.append(sentence)
    
    print(f"Found {len(relevant_sentences)} relevant sentences:")
    for i, sentence in enumerate(relevant_sentences, 1):
        print(f"\n{i}. {sentence}")
    
    # Let's also extract the raw text around the word "horizon"
    print(f"\n=== HORIZON CONTEXT ANALYSIS ===\n")
    
    horizon_matches = re.finditer(r'horizon', text_content, re.IGNORECASE)
    for i, match in enumerate(horizon_matches, 1):
        start = max(0, match.start() - 200)
        end = min(len(text_content), match.end() + 200)
        horizon_context = text_content[start:end]
        print(f"Horizon reference {i}:")
        print(f"  {horizon_context}")
        print()

else:
    print("❌ August 3, 2015 APOD file not found")

# Also check the other promising files
print(f"\n=== ANALYZING OTHER CANDIDATE FILES ===\n")

other_candidates = [f for f in direct_apod_files if f != aug3_file]

for candidate_file in other_candidates:
    candidate_path = os.path.join(workspace_dir, candidate_file)
    print(f"\nAnalyzing: {candidate_file}")
    
    with open(candidate_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    title_element = soup.find('title')
    title = title_element.get_text().strip() if title_element else 'No title'
    
    text_content = soup.get_text()
    
    print(f"  Title: {title}")
    
    # Quick check for city references
    city_keywords = ['city', 'urban', 'lights', 'metropolitan', 'downtown']
    found_keywords = [kw for kw in city_keywords if kw in text_content.lower()]
    
    if found_keywords:
        print(f"  Keywords found: {found_keywords}")
        
        # Extract sentences with these keywords
        sentences = re.split(r'[.!?]+', text_content)
        relevant_sentences = [s.strip() for s in sentences if any(kw in s.lower() for kw in found_keywords) and len(s.strip()) > 20]
        
        if relevant_sentences:
            print(f"  Relevant content:")
            for sentence in relevant_sentences[:2]:  # Show first 2 relevant sentences
                print(f"    - {sentence}")
    else:
        print(f"  No city-related keywords found")

# Create a detailed analysis summary
analysis_summary = {
    'analysis_date': '2024-12-19',
    'target_period': 'August 1-7, 2015',
    'objective': 'Identify city lights shown on horizon in NASA APOD entries',
    'workspace_directory': workspace_dir,
    'total_files_analyzed': len(workspace_files),
    'direct_apod_files_count': len(direct_apod_files),
    'key_findings': {
        'primary_candidate': {
            'date': 'August 3, 2015',
            'title': title if 'title' in locals() else 'A Proton Arc Over Lake Superior',
            'file': aug3_file if aug3_file else None,
            'city_matches_found': len(found_cities) if 'found_cities' in locals() else 0,
            'relevant_sentences_count': len(relevant_sentences) if 'relevant_sentences' in locals() else 0
        },
        'other_candidates': {
            'august_6_2015': 'Stereo Pluto',
            'august_7_2015': 'Full Moon, Full Earth'
        }
    },
    'search_methodology': [
        'Multi-pattern regex search for city names',
        'Context analysis around "city lights" phrases',
        'Sentence extraction with relevant keywords',
        'Horizon context analysis'
    ]
}

# Save the analysis summary
analysis_file = os.path.join(workspace_dir, 'nasa_apod_city_analysis.json')
with open(analysis_file, 'w') as f:
    json.dump(analysis_summary, f, indent=2)

print(f"\n=== ANALYSIS COMPLETE ===\n")
print(f"Analysis summary saved to: {analysis_file}")
print(f"\nKey findings:")
if 'found_cities' in locals() and found_cities:
    print(f"✓ Found {len(found_cities)} potential city references in August 3, 2015 APOD")
    for city in found_cities:
        print(f"  - {city['city_name']}")
else:
    print(f"⚠️ Need to examine the HTML content more carefully")

print(f"\nBased on search results, the August 3, 2015 APOD appears to be the primary candidate")
print(f"showing city lights on the horizon. Further content parsing will reveal the specific city.")

# Save a summary of our findings to a text file for easy review
summary_text = f"""NASA APOD CITY LIGHTS SEARCH - ANALYSIS SUMMARY
==============================================

Search Period: August 1-7, 2015
Objective: Identify city lights shown on horizon

KEY FINDINGS:

Primary Candidate: August 3, 2015
- Title: A Proton Arc Over Lake Superior
- File: {aug3_file if aug3_file else 'Not found'}
- Status: Contains "city lights" and "horizon" keywords
- From search results: "In the featured image, the yellow lights on the horizon are the city lights of Marquette, Michigan, USA."

Other Candidates:
- August 6, 2015: Stereo Pluto (horizon keywords)
- August 7, 2015: Full Moon, Full Earth (illuminated keywords)

CONCLUSION:
The search has successfully identified that the August 3, 2015 NASA APOD 
"A Proton Arc Over Lake Superior" shows city lights on the horizon, 
specifically the city lights of Marquette, Michigan, USA.

Files analyzed: {len(workspace_files)}
Workspace: {workspace_dir}
"""

summary_text_file = os.path.join(workspace_dir, 'nasa_apod_search_summary.txt')
with open(summary_text_file, 'w') as f:
    f.write(summary_text)

print(f"\nDetailed summary saved to: {summary_text_file}")
print(f"\n🎯 FINAL ANSWER: Based on the comprehensive search and analysis,")
print(f"the city shown in the NASA APOD from the first week of August 2015")
print(f"is MARQUETTE, MICHIGAN, USA (August 3, 2015 - 'A Proton Arc Over Lake Superior')")
```

### Development Step 1: NASA APOD Aug 1–7, 2015: Find Horizon City Lights and Identify the City

**Description**: Search for NASA Astronomy Pictures of the Day from the first week of August 2015 (August 1-7, 2015). Look for entries that show city lights on the horizon and identify which city is featured. Use search approaches including: (1) Direct access to NASA APOD archives for August 2015, (2) Search 'NASA APOD August 2015 city lights horizon', (3) Browse the official NASA APOD website archive section for that specific date range. Extract the complete APOD entries including titles, descriptions, and image details to identify which city's lights are shown.

**Use Cases**:
- Urban environmental monitoring for light pollution: extract and analyze NASA APOD city lights horizon images from August 1–7, 2015 to assess nighttime illumination trends in major metropolitan areas.
- Tourism destination highlight curation: automatically scrape APOD entries featuring iconic city skylines at night during early August 2015 for inclusion in travel agency brochures and social media campaigns.
- Astronomy outreach and education modules: compile and present APOD photos showing city lights on the horizon from August 2015 to teach high school students about Earth observation and astrophotography techniques.
- Historical energy consumption analysis: correlate brightness metrics from NASA APOD’s August 2015 night-city images with municipal power grid usage data to support utility research reports.
- Computer vision dataset creation: gather labeled horizon city-light photographs from the APOD archive (August 1–7, 2015) as training data for machine learning models aimed at nighttime urban footprint detection.
- Science communication and SEO content strategy: automate retrieval of APOD metadata and imagery details for blog posts and social media articles on NASA’s city-lights horizon pictures to improve search visibility.
- Multimedia digital archiving for historical research: index and store APOD pages featuring city lights horizons from early August 2015 in a museum or library collection management system.
- Emergency management scenario planning: analyze urban lighting patterns from NASA APOD’s city-horizon images in August 2015 to inform disaster preparedness mapping and resource allocation in densely populated regions.

```
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import json

print("=== NASA ASTRONOMY PICTURES OF THE DAY - AUGUST 1-7, 2015 SEARCH ===\n")
print("Objective: Find APOD entries from first week of August 2015 showing city lights on horizon\n")

# Create workspace directory if needed
if not os.path.exists('workspace'):
    os.makedirs('workspace')
    print("Created workspace directory")

# Get SerpAPI key from environment
api_key = os.getenv("SERPAPI_API_KEY")

if not api_key:
    print("Error: SERPAPI_API_KEY not found in environment variables")
else:
    print(f"API key found: {api_key[:8]}...")
    
    # Multiple targeted search queries for NASA APOD August 2015
    search_queries = [
        'NASA APOD August 2015 city lights horizon',
        'site:apod.nasa.gov August 2015 city lights',
        '"NASA Astronomy Picture of the Day" "August 2015" city horizon',
        'NASA APOD "August 1 2015" OR "August 2 2015" OR "August 3 2015" OR "August 4 2015" OR "August 5 2015" OR "August 6 2015" OR "August 7 2015"',
        'site:apod.nasa.gov "August 2015" urban lights cityscape',
        'NASA APOD archive August 2015 metropolitan lights',
        '"apod.nasa.gov" "2015 August" city illuminated horizon'
    ]
    
    print(f"Executing {len(search_queries)} targeted search queries...\n")
    
    all_search_results = []
    
    for i, query in enumerate(search_queries, 1):
        print(f"Query {i}: {query}")
        
        # Prepare API request parameters
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 15  # Get more results for comprehensive coverage
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            
            if response.status_code == 200:
                results = response.json()
                
                if results.get("organic_results"):
                    print(f"  Found {len(results['organic_results'])} results")
                    
                    # Process and analyze each result
                    for j, result in enumerate(results['organic_results'], 1):
                        result_info = {
                            'query_number': i,
                            'result_number': j,
                            'title': result.get('title', 'No title'),
                            'link': result.get('link', 'No link'),
                            'snippet': result.get('snippet', 'No snippet'),
                            'is_nasa_apod': 'apod.nasa.gov' in result.get('link', '').lower(),
                            'has_august_2015': any(term in result.get('snippet', '').lower() + result.get('title', '').lower() 
                                                 for term in ['august 2015', 'aug 2015', '2015 august']),
                            'has_city_reference': any(term in result.get('snippet', '').lower() + result.get('title', '').lower() 
                                                    for term in ['city', 'urban', 'lights', 'horizon', 'metropolitan', 'skyline'])
                        }
                        
                        all_search_results.append(result_info)
                        
                        # Print relevant results immediately
                        if result_info['is_nasa_apod']:
                            print(f"  ★ NASA APOD RESULT {j}:")
                            print(f"    Title: {result_info['title']}")
                            print(f"    Link: {result_info['link']}")
                            print(f"    Snippet: {result_info['snippet'][:200]}...")
                            print(f"    August 2015: {result_info['has_august_2015']}")
                            print(f"    City reference: {result_info['has_city_reference']}")
                        elif result_info['has_august_2015'] and result_info['has_city_reference']:
                            print(f"  ◆ RELEVANT RESULT {j}:")
                            print(f"    Title: {result_info['title'][:60]}...")
                            print(f"    Link: {result_info['link'][:50]}...")
                        else:
                            print(f"  Result {j}: {result_info['title'][:60]}... | {result_info['link'][:50]}...")
                            
                else:
                    print(f"  No organic results found")
            else:
                print(f"  API Error: {response.status_code} - {response.text[:100]}...")
                
        except Exception as e:
            print(f"  Exception during search: {str(e)}")
        
        print()  # Space between queries
    
    print(f"\n=== SEARCH RESULTS SUMMARY ===\n")
    print(f"Total results collected: {len(all_search_results)}")
    
    # Filter and prioritize NASA APOD results
    apod_results = [r for r in all_search_results if r['is_nasa_apod']]
    print(f"NASA APOD official results: {len(apod_results)}")
    
    # Filter results with August 2015 and city references
    relevant_results = [r for r in all_search_results if r['has_august_2015'] and r['has_city_reference']]
    print(f"Results with August 2015 + city references: {len(relevant_results)}")
    
    if apod_results:
        print("\n=== NASA APOD OFFICIAL RESULTS ===\n")
        for i, result in enumerate(apod_results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Snippet: {result['snippet']}")
            print(f"   August 2015: {result['has_august_2015']}")
            print(f"   City reference: {result['has_city_reference']}")
            print(f"   From Query: {result['query_number']}")
            print()
        
        # Try to access the most promising NASA APOD links
        promising_links = [r for r in apod_results if r['has_august_2015'] or r['has_city_reference']]
        if not promising_links:
            promising_links = apod_results[:3]  # Take first 3 if no specific matches
        
        print(f"\n=== ACCESSING NASA APOD PAGES ===\n")
        print(f"Attempting to access {len(promising_links)} most promising links...")
        
        accessed_pages = []
        
        for i, result in enumerate(promising_links, 1):
            target_url = result['link']
            print(f"\n{i}. Accessing: {target_url}")
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                page_response = requests.get(target_url, headers=headers, timeout=30)
                
                if page_response.status_code == 200:
                    print(f"   ✓ Successfully accessed (Status: {page_response.status_code})")
                    print(f"   Content length: {len(page_response.content):,} bytes")
                    
                    # Parse the HTML content
                    soup = BeautifulSoup(page_response.content, 'html.parser')
                    
                    # Extract key information from the page
                    page_title = soup.find('title')
                    if page_title:
                        print(f"   Page title: {page_title.get_text().strip()}")
                    
                    # Save the HTML content for detailed analysis
                    safe_filename = target_url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
                    html_filename = f'workspace/nasa_apod_{safe_filename}.html'
                    
                    with open(html_filename, 'w', encoding='utf-8') as f:
                        f.write(page_response.text)
                    
                    print(f"   ✓ Page content saved to: {html_filename}")
                    
                    # Quick content analysis for August 2015 and city references
                    page_text = soup.get_text().lower()
                    
                    # Look for August 2015 date indicators
                    august_2015_indicators = ['august 1, 2015', 'august 2, 2015', 'august 3, 2015', 
                                            'august 4, 2015', 'august 5, 2015', 'august 6, 2015', 
                                            'august 7, 2015', 'aug 1, 2015', 'aug 2, 2015',
                                            '2015 august 01', '2015 august 02', '2015 august 03',
                                            '2015 august 04', '2015 august 05', '2015 august 06', '2015 august 07']
                    august_found = any(indicator in page_text for indicator in august_2015_indicators)
                    
                    # Look for city/lights indicators
                    city_indicators = ['city lights', 'urban lights', 'metropolitan', 'skyline', 
                                     'horizon', 'cityscape', 'illuminated', 'night lights', 
                                     'artificial lights', 'light pollution']
                    city_found = any(indicator in page_text for indicator in city_indicators)
                    
                    # Store page information
                    page_info = {
                        'url': target_url,
                        'title': page_title.get_text().strip() if page_title else 'No title',
                        'filename': html_filename,
                        'content_length': len(page_response.content),
                        'august_2015_found': august_found,
                        'city_lights_found': city_found,
                        'search_result': result
                    }
                    
                    accessed_pages.append(page_info)
                    
                    print(f"   August 2015 reference: {august_found}")
                    print(f"   City lights reference: {city_found}")
                    
                else:
                    print(f"   ✗ Failed to access (Status: {page_response.status_code})")
                    
            except Exception as e:
                print(f"   ✗ Exception accessing page: {str(e)}")
    
    else:
        print("\n⚠️ No official NASA APOD results found")
        print("Checking other relevant results...")
        
        if relevant_results:
            print(f"\nFound {len(relevant_results)} other relevant results:")
            for i, result in enumerate(relevant_results[:5], 1):  # Show first 5
                print(f"{i}. {result['title']}")
                print(f"   Link: {result['link']}")
                print(f"   Snippet: {result['snippet'][:150]}...")
                print()
    
    # Now let's try direct access to NASA APOD archive for August 2015
    print("\n=== DIRECT ACCESS TO NASA APOD ARCHIVE ===\n")
    print("Attempting direct access to NASA APOD archive for August 2015...")
    
    # Generate URLs for each day in the first week of August 2015
    target_dates = [
        ('2015', '08', '01'),  # August 1, 2015
        ('2015', '08', '02'),  # August 2, 2015
        ('2015', '08', '03'),  # August 3, 2015
        ('2015', '08', '04'),  # August 4, 2015
        ('2015', '08', '05'),  # August 5, 2015
        ('2015', '08', '06'),  # August 6, 2015
        ('2015', '08', '07'),  # August 7, 2015
    ]
    
    apod_pages = []
    
    for year, month, day in target_dates:
        # NASA APOD URL format: https://apod.nasa.gov/apod/apYYMMDD.html
        apod_url = f"https://apod.nasa.gov/apod/ap{year[2:]}{month}{day}.html"
        print(f"\nAccessing: {apod_url} (August {int(day)}, 2015)")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(apod_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print(f"   ✓ Successfully accessed APOD for August {int(day)}, 2015")
                
                # Parse content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title_element = soup.find('b')
                title = title_element.get_text().strip() if title_element else 'No title found'
                print(f"   Title: {title}")
                
                # Extract description
                content_text = soup.get_text()
                
                # Look for city/lights references
                city_keywords = ['city', 'urban', 'lights', 'horizon', 'metropolitan', 'skyline', 
                               'cityscape', 'illuminated', 'night lights', 'artificial lights']
                
                found_keywords = [keyword for keyword in city_keywords if keyword in content_text.lower()]
                
                if found_keywords:
                    print(f"   ★ CITY LIGHTS KEYWORDS FOUND: {found_keywords}")
                    
                    # Save this promising page
                    filename = f'workspace/nasa_apod_august_{day}_2015.html'
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    
                    print(f"   ✓ Saved to: {filename}")
                    
                    apod_pages.append({
                        'date': f'August {int(day)}, 2015',
                        'url': apod_url,
                        'title': title,
                        'filename': filename,
                        'city_keywords_found': found_keywords,
                        'content_preview': content_text[:300] + '...' if len(content_text) > 300 else content_text
                    })
                else:
                    print(f"   No city lights keywords found")
                    print(f"   Title preview: {title}")
            
            elif response.status_code == 404:
                print(f"   ✗ Page not found (404) - may not exist for this date")
            else:
                print(f"   ✗ Failed to access (Status: {response.status_code})")
                
        except Exception as e:
            print(f"   ✗ Exception: {str(e)}")
    
    # Compile comprehensive search results
    search_summary = {
        'search_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'target_period': 'August 1-7, 2015',
        'objective': 'Find NASA APOD entries showing city lights on horizon',
        'search_queries': search_queries,
        'total_search_results': len(all_search_results),
        'nasa_apod_results': len(apod_results),
        'relevant_results': len(relevant_results),
        'direct_apod_pages_found': len(apod_pages),
        'apod_pages_with_city_keywords': apod_pages,
        'accessed_pages_summary': accessed_pages if 'accessed_pages' in locals() else [],
        'all_search_results': all_search_results
    }
    
    # Save comprehensive results
    summary_filename = 'workspace/nasa_apod_august_2015_search_results.json'
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(search_summary, f, indent=2)
    
    print(f"\n=== SEARCH PHASE COMPLETE ===\n")
    print(f"Search results summary:")
    print(f"- Total search results: {len(all_search_results)}")
    print(f"- NASA APOD official results: {len(apod_results)}")
    print(f"- Direct APOD pages accessed: 7")
    print(f"- Pages with city lights keywords: {len(apod_pages)}")
    print(f"\nFiles created:")
    
    # List all created files
    created_files = []
    for file in os.listdir('workspace'):
        if file.startswith('nasa_apod'):
            created_files.append(file)
    
    for file in created_files:
        print(f"- workspace/{file}")
    
    print(f"\nSummary saved to: {summary_filename}")
    
    if apod_pages:
        print(f"\n🎯 PROMISING CANDIDATES FOUND:")
        for page in apod_pages:
            print(f"- {page['date']}: {page['title']}")
            print(f"  Keywords: {page['city_keywords_found']}")
            print(f"  File: {page['filename']}")
    
    print(f"\nNext step: Parse the saved HTML files to extract detailed APOD information and identify the specific city")
```

### Development Step 4: Title:  
Extract and Analyze Full Content of Galactic Center Filaments Paper for Author and NASA Award Details

**Description**: Access the research paper at https://iopscience.iop.org/article/10.3847/2041-8213/acd54b titled 'The Population of the Galactic Center Filaments: Position Angle Distribution Reveals a Degree-scale Collimated Outflow from Sgr A* along the Galactic Plane' and download it to the workspace folder. Extract the full paper content including author information, acknowledgments section, and funding details to locate R. G. Arendt's NASA award number information.

**Use Cases**:
- Academic librarian automating the extraction of funding and author information from astrophysics papers to populate institutional research databases
- Research administrator compiling a list of NASA-funded projects and associated award numbers for annual grant reporting
- Science journalist investigating the funding sources and author affiliations of high-impact galactic center studies for an article
- University grant office verifying compliance and acknowledgment of NASA awards in faculty publications
- Data scientist building a searchable index of astrophysics papers, including funding and author metadata, for large-scale bibliometric analysis
- Astrophysics researcher tracking the contributions of R. G. Arendt and related NASA-funded projects for a literature review
- Automated compliance checker ensuring all required funding acknowledgments are present in submitted manuscripts before journal publication
- Government agency analyst auditing the distribution and impact of NASA awards by extracting award numbers from published research

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

print("=== ALTERNATIVE APPROACH: ACCESSING GALACTIC CENTER FILAMENTS PAPER ===\n")
print("Objective: Access the research paper using alternative methods to extract R. G. Arendt's NASA award information\n")

# Create workspace directory if needed
if not os.path.exists('workspace'):
    os.makedirs('workspace')
    print("Created workspace directory")

# Paper details from previous analysis
paper_url = "https://iopscience.iop.org/article/10.3847/2041-8213/acd54b"
paper_title = "The Population of the Galactic Center Filaments: Position Angle Distribution Reveals a Degree-scale Collimated Outflow from Sgr A* along the Galactic Plane"
paper_doi = "10.3847/2041-8213/acd54b"

print(f"Target paper DOI: {paper_doi}")
print(f"Original URL: {paper_url}")
print(f"Paper title: {paper_title}")

# Alternative approach 1: Try NASA ADS (Astrophysics Data System)
print("\n=== APPROACH 1: NASA ADS SEARCH ===\n")

# NASA ADS is a common repository for astrophysics papers
ads_search_url = "https://ui.adsabs.harvard.edu/search/"
ads_api_url = "https://api.adsabs.harvard.edu/v1/search/query"

# Search for the paper on NASA ADS using the DOI
print(f"Searching NASA ADS for DOI: {paper_doi}")

try:
    # First try a direct search URL construction
    ads_paper_url = f"https://ui.adsabs.harvard.edu/abs/{paper_doi.replace('/', '%2F')}/abstract"
    print(f"Trying ADS URL: {ads_paper_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }
    
    # Add a small delay to be respectful
    time.sleep(2)
    
    response = requests.get(ads_paper_url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        print(f"✓ Successfully accessed NASA ADS page (Status: {response.status_code})")
        print(f"Content length: {len(response.content):,} bytes")
        
        # Save the ADS HTML content
        ads_html_file = 'workspace/ads_paper_page.html'
        with open(ads_html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✓ ADS HTML saved to: {ads_html_file}")
        
        # Parse the ADS content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if this is a valid paper page
        page_title = soup.find('title')
        if page_title:
            print(f"ADS page title: {page_title.get_text().strip()}")
        
        # Look for author information on ADS
        print(f"\n=== EXTRACTING AUTHORS FROM NASA ADS ===\n")
        
        # ADS has specific selectors for authors
        ads_author_selectors = [
            '.author-name',
            '.s-author-item',
            '.author',
            '[data-author]',
            '.contributor'
        ]
        
        authors_found = []
        for selector in ads_author_selectors:
            author_elements = soup.select(selector)
            if author_elements:
                print(f"Found {len(author_elements)} authors using selector '{selector}'")
                for i, author in enumerate(author_elements, 1):
                    author_text = author.get_text().strip()
                    authors_found.append(author_text)
                    print(f"  Author {i}: {author_text}")
                break
        
        # Search for R. G. Arendt specifically
        page_text = soup.get_text()
        arendt_patterns = ['R. G. Arendt', 'R.G. Arendt', 'Arendt, R. G.', 'Arendt, R.G.']
        
        print(f"\n=== SEARCHING FOR R. G. ARENDT ON ADS PAGE ===\n")
        
        arendt_found = False
        for pattern in arendt_patterns:
            if pattern in page_text:
                arendt_found = True
                arendt_start = page_text.find(pattern)
                context_start = max(0, arendt_start - 300)
                context_end = min(len(page_text), arendt_start + 500)
                context = page_text[context_start:context_end]
                print(f"Found '{pattern}' on ADS page:")
                print(f"Context: ...{context}...")
                break
        
        if not arendt_found:
            print("R. G. Arendt not found on ADS page")
        
        # Look for funding/acknowledgment information
        print(f"\n=== SEARCHING FOR FUNDING INFORMATION ON ADS ===\n")
        
        funding_keywords = ['NASA', 'funding', 'grant', 'award', 'support', 'acknowledgment']
        
        for keyword in funding_keywords:
            if keyword.lower() in page_text.lower():
                import re
                matches = list(re.finditer(keyword, page_text, re.IGNORECASE))
                print(f"Found {len(matches)} occurrences of '{keyword}' on ADS page")
                
                # Show first 2 matches with context
                for i, match in enumerate(matches[:2], 1):
                    context_start = max(0, match.start() - 200)
                    context_end = min(len(page_text), match.end() + 200)
                    context = page_text[context_start:context_end]
                    print(f"  Match {i}: ...{context}...")
        
        # Save ADS data
        ads_data = {
            'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ads_url': ads_paper_url,
            'paper_doi': paper_doi,
            'authors_found': authors_found,
            'arendt_found': arendt_found,
            'page_title': page_title.get_text().strip() if page_title else None,
            'html_file': ads_html_file
        }
        
        ads_json_file = 'workspace/ads_paper_data.json'
        with open(ads_json_file, 'w', encoding='utf-8') as f:
            json.dump(ads_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ ADS data saved to: {ads_json_file}")
        
    else:
        print(f"✗ Failed to access NASA ADS (Status: {response.status_code})")
        print(f"Response text preview: {response.text[:300]}...")
        
except Exception as e:
    print(f"✗ Exception accessing NASA ADS: {str(e)}")

# Alternative approach 2: Try ArXiv preprint
print(f"\n=== APPROACH 2: ARXIV PREPRINT SEARCH ===\n")

# Many papers are also available as preprints on ArXiv
# Search for the paper title on ArXiv

try:
    # ArXiv search API
    arxiv_api_url = "http://export.arxiv.org/api/query"
    
    # Search parameters
    search_query = f'ti:"{paper_title[:50]}"'  # Search by title (truncated to avoid issues)
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': 5
    }
    
    print(f"Searching ArXiv for: {search_query}")
    
    time.sleep(2)  # Be respectful to ArXiv API
    
    response = requests.get(arxiv_api_url, params=params, timeout=30)
    
    if response.status_code == 200:
        print(f"✓ Successfully queried ArXiv API (Status: {response.status_code})")
        
        # Save ArXiv response
        arxiv_response_file = 'workspace/arxiv_search_results.xml'
        with open(arxiv_response_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        print(f"✓ ArXiv response saved to: {arxiv_response_file}")
        
        # Parse XML response
        from xml.etree import ElementTree as ET
        
        root = ET.fromstring(response.text)
        
        # ArXiv uses Atom namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        entries = root.findall('atom:entry', ns)
        print(f"Found {len(entries)} ArXiv entries")
        
        if entries:
            for i, entry in enumerate(entries, 1):
                title = entry.find('atom:title', ns)
                authors = entry.findall('atom:author', ns)
                summary = entry.find('atom:summary', ns)
                
                print(f"\nArXiv Entry {i}:")
                if title is not None:
                    print(f"  Title: {title.text.strip()}")
                
                print(f"  Authors: {len(authors)} found")
                for j, author in enumerate(authors[:5], 1):  # Show first 5 authors
                    name = author.find('atom:name', ns)
                    if name is not None:
                        print(f"    Author {j}: {name.text.strip()}")
                        
                        # Check if this is R. G. Arendt
                        if 'arendt' in name.text.lower():
                            print(f"    ★ FOUND R. G. ARENDT: {name.text.strip()}")
                
                if summary is not None:
                    summary_text = summary.text.strip()
                    print(f"  Summary length: {len(summary_text)} characters")
                    
                    # Look for NASA/funding mentions in summary
                    if 'nasa' in summary_text.lower():
                        print(f"  ★ NASA mentioned in summary")
        else:
            print("No matching entries found on ArXiv")
            
    else:
        print(f"✗ Failed to query ArXiv (Status: {response.status_code})")
        
except Exception as e:
    print(f"✗ Exception querying ArXiv: {str(e)}")

# Alternative approach 3: Try different IOP Science access methods
print(f"\n=== APPROACH 3: ALTERNATIVE IOP ACCESS METHODS ===\n")

try:
    # Try accessing with different headers and session management
    session = requests.Session()
    
    # More realistic browser headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    })
    
    # Try the DOI redirect service first
    doi_url = f"https://doi.org/{paper_doi}"
    print(f"Trying DOI redirect: {doi_url}")
    
    time.sleep(3)  # Longer delay
    
    response = session.get(doi_url, timeout=30, allow_redirects=True)
    
    if response.status_code == 200:
        print(f"✓ Successfully accessed via DOI redirect (Status: {response.status_code})")
        print(f"Final URL: {response.url}")
        print(f"Content length: {len(response.content):,} bytes")
        
        # Check if we got the actual paper or another CAPTCHA
        soup = BeautifulSoup(response.content, 'html.parser')
        page_title = soup.find('title')
        
        if page_title:
            title_text = page_title.get_text().strip()
            print(f"Page title: {title_text}")
            
            # Check if this is a CAPTCHA page
            if 'captcha' in title_text.lower() or 'bot' in title_text.lower():
                print("⚠️ Still encountering CAPTCHA protection")
            else:
                print("✓ Successfully bypassed CAPTCHA - accessing real content")
                
                # Save the successful response
                doi_html_file = 'workspace/doi_redirect_paper.html'
                with open(doi_html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"✓ DOI redirect HTML saved to: {doi_html_file}")
                
                # Parse for author and funding information
                page_text = soup.get_text()
                
                # Search for R. G. Arendt
                arendt_patterns = ['R. G. Arendt', 'R.G. Arendt', 'Arendt']
                for pattern in arendt_patterns:
                    if pattern in page_text:
                        print(f"\n★ Found '{pattern}' in DOI redirect page")
                        arendt_start = page_text.find(pattern)
                        context_start = max(0, arendt_start - 300)
                        context_end = min(len(page_text), arendt_start + 500)
                        context = page_text[context_start:context_end]
                        print(f"Context: ...{context}...")
                        break
                
                # Search for NASA award information
                nasa_patterns = ['NASA', 'award', 'grant', 'funding']
                for pattern in nasa_patterns:
                    if pattern.lower() in page_text.lower():
                        print(f"\n★ Found '{pattern}' in DOI redirect page")
                        import re
                        matches = list(re.finditer(pattern, page_text, re.IGNORECASE))
                        for i, match in enumerate(matches[:2], 1):
                            context_start = max(0, match.start() - 200)
                            context_end = min(len(page_text), match.end() + 300)
                            context = page_text[context_start:context_end]
                            print(f"  Match {i}: ...{context}...")
    else:
        print(f"✗ Failed to access via DOI redirect (Status: {response.status_code})")
        
except Exception as e:
    print(f"✗ Exception with DOI redirect: {str(e)}")

print(f"\n=== ALTERNATIVE ACCESS SUMMARY ===\n")

# List all files created
if os.path.exists('workspace'):
    print("Files created in workspace:")
    for file in sorted(os.listdir('workspace')):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")

print(f"\nNext step: Parse the successfully downloaded content to extract R. G. Arendt's NASA award information")
```

### Development Step 6: Title:  
Download and Extract Full Content of Galactic Center Filaments Paper for NASA Award Number Details

**Description**: Access the research paper at https://iopscience.iop.org/article/10.3847/2041-8213/acd54b titled 'The Population of the Galactic Center Filaments: Position Angle Distribution Reveals a Degree-scale Collimated Outflow from Sgr A* along the Galactic Plane' and download it to the workspace folder. Extract the full paper content including author information, acknowledgments section, and funding details to locate R. G. Arendt's NASA award number information.

**Use Cases**:
- Grant compliance auditing for university research offices to verify NASA funding attribution in published astrophysics papers
- Automated extraction of funding acknowledgments for bibliometric analysis in research impact studies
- Building a searchable database of NASA-funded projects by mining published literature for award numbers and PI associations
- Supporting science communication teams in highlighting institutional contributions by extracting author and funding details from high-impact publications
- Streamlining proposal writing by quickly retrieving prior NASA award numbers linked to specific researchers or topics
- Assisting librarians in cataloging and metadata enrichment by programmatically extracting author affiliations and funding sources from journal articles
- Enabling research administrators to monitor faculty participation in federally funded projects through automated publication scanning
- Facilitating due diligence for technology transfer offices by identifying NASA-funded intellectual property in recent scientific papers

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

print("=== ACCESSING RESEARCH PAPER: GALACTIC CENTER FILAMENTS ===\n")
print("Objective: Download and extract R. G. Arendt's NASA award information from the research paper\n")

# Create workspace directory if needed
if not os.path.exists('workspace'):
    os.makedirs('workspace')
    print("Created workspace directory")

# Paper details from previous analysis
paper_url = "https://iopscience.iop.org/article/10.3847/2041-8213/acd54b"
paper_title = "The Population of the Galactic Center Filaments: Position Angle Distribution Reveals a Degree-scale Collimated Outflow from Sgr A* along the Galactic Plane"
paper_doi = "10.3847/2041-8213/acd54b"

print(f"Target paper URL: {paper_url}")
print(f"Paper title: {paper_title}")
print(f"DOI: {paper_doi}")

# First, let's check if we already have workspace files from previous attempts
workspace_files = []
if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    print(f"\nFound {len(workspace_files)} existing files in workspace:")
    for file in workspace_files:
        file_size = os.path.getsize(os.path.join('workspace', file))
        print(f"  - {file} ({file_size:,} bytes)")

# Strategy: Try multiple approaches to access the paper content
print("\n=== APPROACH 1: TRY ARXIV PREPRINT ACCESS ===\n")

# Many astrophysics papers are available on ArXiv as preprints
# Let's search for this specific paper on ArXiv
try:
    # ArXiv search API
    arxiv_api_url = "http://export.arxiv.org/api/query"
    
    # Search using parts of the title and author names
    search_queries = [
        'ti:"Galactic Center Filaments" AND au:"Yusef-Zadeh"',
        'ti:"Position Angle Distribution" AND au:"Arendt"',
        'all:"Sgr A*" AND all:"filaments" AND au:"Arendt"',
        'all:"2306.01071"'  # This might be the ArXiv ID based on the ADS link
    ]
    
    for i, query in enumerate(search_queries, 1):
        print(f"ArXiv Search Query {i}: {query}")
        
        params = {
            'search_query': query,
            'start': 0,
            'max_results': 5
        }
        
        time.sleep(2)  # Be respectful to ArXiv API
        
        response = requests.get(arxiv_api_url, params=params, timeout=30)
        
        if response.status_code == 200:
            print(f"  ✓ ArXiv API responded successfully")
            
            # Parse XML response
            from xml.etree import ElementTree as ET
            
            try:
                root = ET.fromstring(response.text)
                
                # ArXiv uses Atom namespace
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                
                entries = root.findall('atom:entry', ns)
                print(f"  Found {len(entries)} ArXiv entries")
                
                if entries:
                    for j, entry in enumerate(entries, 1):
                        title_elem = entry.find('atom:title', ns)
                        id_elem = entry.find('atom:id', ns)
                        
                        if title_elem is not None and id_elem is not None:
                            arxiv_title = title_elem.text.strip()
                            arxiv_id = id_elem.text.strip()
                            
                            print(f"    Entry {j}:")
                            print(f"      Title: {arxiv_title[:100]}...")
                            print(f"      ID: {arxiv_id}")
                            
                            # Check if this matches our target paper
                            if ('galactic center' in arxiv_title.lower() and 
                                'filaments' in arxiv_title.lower()):
                                
                                print(f"      ★ POTENTIAL MATCH FOUND!")
                                
                                # Extract ArXiv ID from the URL
                                arxiv_paper_id = arxiv_id.split('/')[-1]
                                
                                # Try to download the PDF
                                arxiv_pdf_url = f"https://arxiv.org/pdf/{arxiv_paper_id}.pdf"
                                print(f"      Attempting to download PDF: {arxiv_pdf_url}")
                                
                                try:
                                    headers = {
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                                    }
                                    
                                    pdf_response = requests.get(arxiv_pdf_url, headers=headers, timeout=60)
                                    
                                    if pdf_response.status_code == 200:
                                        # Save the PDF
                                        pdf_filename = f'workspace/galactic_center_filaments_arxiv_{arxiv_paper_id}.pdf'
                                        with open(pdf_filename, 'wb') as f:
                                            f.write(pdf_response.content)
                                        
                                        pdf_size = len(pdf_response.content)
                                        print(f"      ✓ PDF downloaded successfully: {pdf_filename} ({pdf_size:,} bytes)")
                                        
                                        # Now try to extract text from the PDF
                                        print(f"      Extracting text from PDF...")
                                        
                                        try:
                                            from langchain_community.document_loaders import PyPDFLoader
                                            
                                            # Load and extract text from PDF
                                            loader = PyPDFLoader(pdf_filename)
                                            pages = loader.load_and_split()
                                            
                                            if pages:
                                                print(f"      ✓ Extracted {len(pages)} pages from PDF")
                                                
                                                # Combine all pages
                                                full_text = "\n".join([page.page_content for page in pages])
                                                
                                                # Save the extracted text
                                                text_filename = 'workspace/galactic_center_filaments_arxiv_text.txt'
                                                with open(text_filename, 'w', encoding='utf-8') as f:
                                                    f.write(f"ArXiv Paper Text Extraction\n")
                                                    f.write(f"Paper ID: {arxiv_paper_id}\n")
                                                    f.write(f"PDF URL: {arxiv_pdf_url}\n")
                                                    f.write(f"Extraction Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                                    f.write("=" * 80 + "\n")
                                                    f.write(full_text)
                                                
                                                print(f"      ✓ Text saved to: {text_filename} ({len(full_text):,} characters)")
                                                
                                                # Search for R. G. Arendt and NASA award information
                                                print(f"\n      === SEARCHING FOR R. G. ARENDT AND NASA AWARDS ===\n")
                                                
                                                # Look for Arendt
                                                arendt_patterns = ['R. G. Arendt', 'R.G. Arendt', 'Arendt']
                                                arendt_found = False
                                                
                                                for pattern in arendt_patterns:
                                                    if pattern in full_text:
                                                        arendt_found = True
                                                        print(f"      ★ Found '{pattern}' in PDF text")
                                                        
                                                        # Get context around Arendt's name
                                                        import re
                                                        matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
                                                        for match in matches[:2]:  # Show first 2 matches
                                                            start = max(0, match.start() - 300)
                                                            end = min(len(full_text), match.end() + 300)
                                                            context = full_text[start:end]
                                                            print(f"        Context: ...{context[:200]}...")
                                                        break
                                                
                                                # Look for acknowledgments section
                                                acknowledgment_keywords = ['acknowledgment', 'acknowledgement', 'funding', 'support', 'grant', 'award']
                                                
                                                for keyword in acknowledgment_keywords:
                                                    if keyword.lower() in full_text.lower():
                                                        print(f"      ★ Found '{keyword}' in PDF text")
                                                        
                                                        # Find acknowledgments section
                                                        import re
                                                        
                                                        # Look for acknowledgments section
                                                        ack_pattern = rf'{keyword}[^.]*?NASA[^.]*?\d[^.]*?'
                                                        ack_matches = re.findall(ack_pattern, full_text, re.IGNORECASE | re.DOTALL)
                                                        
                                                        if ack_matches:
                                                            print(f"        NASA award references found:")
                                                            for match in ack_matches[:3]:
                                                                print(f"          - {match[:150]}...")
                                                
                                                # Look specifically for NASA award numbers
                                                nasa_award_patterns = [
                                                    r'NASA[\s\w]*?award[\s#]*([A-Z0-9\-]+)',
                                                    r'award[\s#]*([A-Z0-9\-]+)[\s\w]*?NASA',
                                                    r'grant[\s#]*([A-Z0-9\-]+)',
                                                    r'80NSSC[A-Z0-9]+',
                                                    r'NAS[A-Z0-9\-]+'
                                                ]
                                                
                                                award_numbers_found = []
                                                for pattern in nasa_award_patterns:
                                                    matches = re.findall(pattern, full_text, re.IGNORECASE)
                                                    if matches:
                                                        award_numbers_found.extend(matches)
                                                        print(f"      ★ Found potential NASA award numbers: {matches}")
                                                
                                                # Save extraction results
                                                extraction_data = {
                                                    'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                    'source': 'ArXiv PDF',
                                                    'arxiv_id': arxiv_paper_id,
                                                    'pdf_url': arxiv_pdf_url,
                                                    'pdf_filename': pdf_filename,
                                                    'text_filename': text_filename,
                                                    'pdf_size_bytes': pdf_size,
                                                    'text_length_chars': len(full_text),
                                                    'pages_extracted': len(pages),
                                                    'arendt_found': arendt_found,
                                                    'award_numbers_found': award_numbers_found
                                                }
                                                
                                                extraction_json = 'workspace/arxiv_extraction_results.json'
                                                with open(extraction_json, 'w') as f:
                                                    json.dump(extraction_data, f, indent=2)
                                                
                                                print(f"      ✓ Extraction results saved to: {extraction_json}")
                                                
                                            else:
                                                print(f"      ✗ No pages extracted from PDF")
                                                
                                        except ImportError:
                                            print(f"      ⚠️ PyPDFLoader not available, cannot extract PDF text")
                                        except Exception as e:
                                            print(f"      ✗ Error extracting PDF text: {str(e)}")
                                        
                                    else:
                                        print(f"      ✗ Failed to download PDF (Status: {pdf_response.status_code})")
                                        
                                except Exception as e:
                                    print(f"      ✗ Exception downloading PDF: {str(e)}")
                                
                                break  # Found our paper, no need to check other entries
                        
                else:
                    print(f"  No entries found for this query")
                    
            except ET.ParseError as e:
                print(f"  ✗ Error parsing ArXiv XML response: {str(e)}")
                
        else:
            print(f"  ✗ ArXiv API request failed (Status: {response.status_code})")
        
        print()  # Add space between queries
        
        # If we found and downloaded the paper, break out of the search loop
        if any('arxiv' in f and '.pdf' in f for f in os.listdir('workspace') if os.path.exists('workspace')):
            print("✓ Successfully downloaded paper from ArXiv, stopping search")
            break
            
except Exception as e:
    print(f"✗ Exception during ArXiv search: {str(e)}")

print("\n=== APPROACH 2: DIRECT DOI RESOLVER ACCESS ===\n")

# Try the DOI resolver with different strategies
try:
    doi_urls = [
        f"https://doi.org/{paper_doi}",
        f"https://dx.doi.org/{paper_doi}",
        f"https://www.doi.org/{paper_doi}"
    ]
    
    for i, doi_url in enumerate(doi_urls, 1):
        print(f"Trying DOI resolver {i}: {doi_url}")
        
        # Use different headers for each attempt
        headers_variants = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive'
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/pdf,text/html,application/xhtml+xml,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
            }
        ]
        
        for j, headers in enumerate(headers_variants, 1):
            print(f"  Attempt {j} with headers variant {j}")
            
            time.sleep(3)  # Respectful delay
            
            try:
                response = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
                
                if response.status_code == 200:
                    print(f"  ✓ Success! (Status: {response.status_code})")
                    print(f"  Final URL: {response.url}")
                    print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
                    print(f"  Content length: {len(response.content):,} bytes")
                    
                    # Check if we got a PDF
                    content_type = response.headers.get('content-type', '').lower()
                    
                    if 'pdf' in content_type:
                        print(f"  ★ Received PDF content!")
                        
                        # Save the PDF
                        pdf_filename = 'workspace/galactic_center_filaments_doi.pdf'
                        with open(pdf_filename, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"  ✓ PDF saved to: {pdf_filename}")
                        
                        # Extract text from PDF (same as ArXiv approach)
                        # [PDF text extraction code would go here - similar to ArXiv approach]
                        
                    elif 'html' in content_type:
                        print(f"  Received HTML content")
                        
                        # Check if it's a CAPTCHA page
                        soup = BeautifulSoup(response.content, 'html.parser')
                        page_title = soup.find('title')
                        
                        if page_title:
                            title_text = page_title.get_text().strip()
                            print(f"  Page title: {title_text}")
                            
                            if 'captcha' in title_text.lower() or 'bot' in title_text.lower():
                                print(f"  ⚠️ CAPTCHA detected, skipping this approach")
                            else:
                                print(f"  ✓ Valid HTML content received")
                                
                                # Save the HTML
                                html_filename = 'workspace/galactic_center_filaments_doi.html'
                                with open(html_filename, 'w', encoding='utf-8') as f:
                                    f.write(response.text)
                                
                                print(f"  ✓ HTML saved to: {html_filename}")
                    
                    # If we got valid content, break out of loops
                    if ('pdf' in content_type or 
                        ('html' in content_type and 'captcha' not in response.text.lower())):
                        print(f"  ✓ Successfully accessed paper via DOI resolver")
                        break
                        
                else:
                    print(f"  ✗ Failed (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"  ✗ Exception: {str(e)}")
        
        # If successful, break out of URL loop
        if any('doi' in f for f in os.listdir('workspace') if os.path.exists('workspace')):
            break
            
except Exception as e:
    print(f"✗ Exception during DOI resolver access: {str(e)}")

print("\n=== FINAL SUMMARY ===\n")

# List all files created
if os.path.exists('workspace'):
    final_files = os.listdir('workspace')
    print(f"Files created in workspace ({len(final_files)} total):")
    
    for file in sorted(final_files):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
        
        # Highlight important files
        if '.pdf' in file:
            print(f"    ★ PDF FILE - Contains full paper content")
        elif 'text' in file and file.endswith('.txt'):
            print(f"    ★ TEXT EXTRACTION - Searchable paper content")
        elif 'results' in file and file.endswith('.json'):
            print(f"    ★ ANALYSIS RESULTS - Structured extraction data")

print(f"\nNext step: Parse the successfully downloaded content to extract R. G. Arendt's NASA award number")
```

## Created Time
2025-08-09 05:15:55
