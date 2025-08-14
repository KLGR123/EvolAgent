# Developer Plan 03

## Plan
Search for the average height of women in the Philippines according to a July 2023 Business Insider article to determine variable C (rounded to the nearest whole centimeter). Focus on finding the specific Business Insider article from July 2023 that reports on Filipino women's average height statistics.

## Description
This is the necessary next step because: (1) We have successfully determined L = 11 (last two digits of 1811) and A = 2 (TikTok logo colors excluding black and white), (2) We need the final variable C (average Filipino woman height from July 2023 Business Insider article) before we can solve the equation Lx = (d/dx * (A * x²)) + 4097 - C, (3) Expected outcome is to locate the specific Business Insider article and extract the height measurement in centimeters, (4) This will provide the third and final variable needed to complete the differential equation calculation and solve for x to the nearest tenth.

## Episodic Examples
### Development Step 27: 2011 Bulgarian NSI Census: Tertiary Education Completion Numbers by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government policy planning for gender equality: A Ministry of Education uses the script to retrieve official 2011 Bulgarian census data on tertiary education by gender to design targeted scholarship programs for underrepresented groups.
- Academic demographic research: A university sociology department automates extraction of male and female higher education completion figures from NSI to compare Bulgaria’s trends with neighboring countries in a peer‐reviewed paper.
- Market analysis for EdTech providers: An EdTech company pulls 2011 tertiary education gender breakdown to assess potential demand among female professionals when launching an online learning platform in Bulgaria.
- Media fact-checking and reporting: A news outlet automatically fetches official NSI data on university graduates by gender to validate claims in political debates and publish accurate infographics.
- NGO impact evaluation: A non-profit focused on women’s empowerment uses the pipeline to gather baseline 2011 education attainment statistics by gender for program evaluation and grant applications.
- Regional workforce planning: A consulting firm extracts Bulgarian census education data by gender at provincial level to advise local governments on skill development and investment incentives.
- Data-driven policy dashboard: A civic tech startup integrates year-specific gendered education attainment figures from the NSI into an interactive dashboard for stakeholders tracking progress over time.
- Comparative EU analysis: A European research consortium leverages the automated scraper to compile standardized 2011 tertiary education completion rates by gender across EU member states, including Bulgaria, for policy benchmarking.

```
import requests
import os
import json
from bs4 import BeautifulSoup
import time
import re

# Create workspace directory if it doesn't exist
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

print("=== SEARCHING FOR 2011 BULGARIAN CENSUS TERTIARY EDUCATION DATA ===\n")
print("Target: Official NSI (Bulgarian National Statistical Institute) census data")
print("Focus: Tertiary education completion by gender\n")

# Function to perform web requests with proper headers
def fetch_with_headers(url, max_retries=3):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5,bg;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} to fetch: {url}")
            response = requests.get(url, headers=headers, timeout=20)
            print(f"Response status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            wait_time = 2 ** attempt
            if attempt < max_retries - 1:
                print(f"Error: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                return None

# Primary target URLs for Bulgarian National Statistical Institute
print("Step 1: Accessing Bulgarian National Statistical Institute (NSI) sources...\n")

target_urls = [
    "https://www.nsi.bg/en",  # English version of NSI
    "https://www.nsi.bg",     # Main NSI site
    "https://www.nsi.bg/en/content/6704/population-education",  # Direct education statistics
    "https://www.nsi.bg/en/content/6710/census-2011",  # Census 2011 page
    "https://www.nsi.bg/census2011/indexen.php",  # Alternative census URL
]

successful_sources = []
failed_sources = []

for i, url in enumerate(target_urls, 1):
    print(f"\n--- Source {i}: {url} ---")
    
    response = fetch_with_headers(url)
    
    if response and response.status_code == 200:
        print(f"✓ Successfully accessed {url}")
        print(f"Content length: {len(response.content):,} bytes")
        
        # Save the content for analysis
        filename = f'nsi_source_{i}.html'
        filepath = os.path.join(workspace_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"Content saved to: {filepath}")
        
        # Parse and analyze content - PROPER FIX: Define all variables first
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        title_text = title.get_text().strip() if title else 'No title found'
        
        # Define content_text FIRST before any usage
        content_text = soup.get_text().lower()
        print(f"Content text extracted: {len(content_text)} characters")
        
        # Now define keyword lists
        education_keywords = ['tertiary education', 'higher education', 'university', 'education level', 'educational attainment', 'census 2011', 'висше образование']
        gender_keywords = ['gender', 'men', 'women', 'male', 'female', 'мъже', 'жени']
        
        # Now use content_text in generator expressions
        has_education_content = any(keyword in content_text for keyword in education_keywords)
        has_gender_content = any(keyword in content_text for keyword in gender_keywords)
        has_2011_content = '2011' in content_text
        
        print(f"Content analysis completed:")
        print(f"  - Education keywords found: {has_education_content}")
        print(f"  - Gender keywords found: {has_gender_content}")
        print(f"  - 2011 content found: {has_2011_content}")
        
        # Look for links to census data or education statistics
        links = soup.find_all('a', href=True)
        print(f"Found {len(links)} total links on page")
        
        relevant_links = []
        for link in links:
            href = link.get('href', '')
            link_text = link.get_text().strip().lower()
            
            # Check if link is relevant to census/education
            link_keywords = ['census', '2011', 'education', 'образование']
            if any(keyword in (href.lower() + ' ' + link_text) for keyword in link_keywords):
                # Build full URL
                if href.startswith('http'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = f"https://www.nsi.bg{href}"
                else:
                    full_url = f"https://www.nsi.bg/{href}"
                
                relevant_links.append({
                    'text': link.get_text().strip(),
                    'url': full_url
                })
        
        print(f"Found {len(relevant_links)} relevant links")
        
        # Store source information
        source_info = {
            'url': url,
            'title': title_text,
            'filename': filepath,
            'content_length': len(response.text),
            'has_education_content': has_education_content,
            'has_gender_content': has_gender_content,
            'has_2011_content': has_2011_content,
            'relevant_links': relevant_links[:10]  # Limit to first 10 relevant links
        }
        
        successful_sources.append(source_info)
        
        print(f"Title: {title_text}")
        print(f"Contains education content: {has_education_content}")
        print(f"Contains gender content: {has_gender_content}")
        print(f"Contains 2011 content: {has_2011_content}")
        
        if relevant_links:
            print("Top relevant links found:")
            for j, link in enumerate(relevant_links[:5], 1):
                print(f"  {j}. {link['text']} -> {link['url']}")
        
    else:
        error_info = {
            'url': url,
            'status': response.status_code if response else 'No response',
            'error': 'Failed to fetch'
        }
        failed_sources.append(error_info)
        print(f"✗ Failed to access {url}")
    
    time.sleep(2)  # Be respectful to the server

print(f"\n=== INITIAL SEARCH RESULTS ===\n")
print(f"Successfully accessed: {len(successful_sources)} sources")
print(f"Failed to access: {len(failed_sources)} sources")

# Analyze the most promising sources
print(f"\n=== ANALYZING SOURCE PRIORITY ===\n")
priority_sources = []

for source in successful_sources:
    priority_score = 0
    if source['has_education_content']:
        priority_score += 3
        print(f"Source {source['url']}: +3 for education content")
    if source['has_gender_content']:
        priority_score += 2
        print(f"Source {source['url']}: +2 for gender content")
    if source['has_2011_content']:
        priority_score += 2
        print(f"Source {source['url']}: +2 for 2011 content")
    if len(source['relevant_links']) > 0:
        priority_score += 1
        print(f"Source {source['url']}: +1 for relevant links ({len(source['relevant_links'])})")
    
    source['priority_score'] = priority_score
    print(f"Source {source['url']}: Total priority score = {priority_score}")
    
    if priority_score >= 4:  # High priority threshold
        priority_sources.append(source)

# Sort by priority score
priority_sources.sort(key=lambda x: x['priority_score'], reverse=True)

print(f"\n=== HIGH PRIORITY SOURCES FOR DETAILED ANALYSIS ===\n")
print(f"Found {len(priority_sources)} high-priority sources (score >= 4)")

for i, source in enumerate(priority_sources, 1):
    print(f"\n{i}. {source['url']} (Priority Score: {source['priority_score']})")
    print(f"   Title: {source['title']}")
    print(f"   Education content: {source['has_education_content']}")
    print(f"   Gender content: {source['has_gender_content']}")
    print(f"   2011 content: {source['has_2011_content']}")
    print(f"   Relevant links: {len(source['relevant_links'])}")

# Save comprehensive research summary
research_summary = {
    'research_target': '2011 Bulgarian Census - Tertiary Education by Gender',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'total_sources_attempted': len(target_urls),
    'successful_sources': len(successful_sources),
    'priority_sources': len(priority_sources),
    'sources_data': successful_sources,
    'priority_sources_data': priority_sources,
    'failed_sources': failed_sources
}

summary_file = os.path.join(workspace_dir, 'bulgarian_census_research_summary.json')
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(research_summary, f, indent=2, ensure_ascii=False)

print(f"\n=== RESEARCH PHASE 1 COMPLETE ===\n")
print(f"Files created in workspace/:")
print(f"  - bulgarian_census_research_summary.json (comprehensive research summary)")

for source in successful_sources:
    print(f"  - {os.path.basename(source['filename'])} (main NSI page)")

print(f"\nNext steps:")
print(f"1. Parse downloaded HTML files for statistical tables")
print(f"2. Look for census data with education levels broken down by gender")
print(f"3. Extract specific tertiary education completion numbers")

if priority_sources:
    print(f"\nMost promising source: {priority_sources[0]['url']}")
    print(f"Priority score: {priority_sources[0]['priority_score']}")
else:
    print(f"\nNo high-priority sources identified. Will need alternative search strategy.")
    
# Show all successful sources for reference
print(f"\n=== ALL SUCCESSFUL SOURCES SUMMARY ===\n")
for i, source in enumerate(successful_sources, 1):
    print(f"{i}. {source['url']}")
    print(f"   Priority Score: {source.get('priority_score', 0)}")
    print(f"   Education: {source['has_education_content']}, Gender: {source['has_gender_content']}, 2011: {source['has_2011_content']}")
    print(f"   Links: {len(source['relevant_links'])}")
```

### Development Step 32: 2011 Bulgarian Census Tertiary Education Completion Numbers by Gender Search

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government policy analysts evaluating gender disparities in higher education to draft targeted interventions using 2011 Bulgarian census tertiary completion rates
- Academic demographers conducting longitudinal studies on Bulgaria’s educational attainment trends by gender from official NSI data
- NGO program coordinators designing women’s scholarship initiatives based on precise male/female tertiary graduation figures from the 2011 census
- International agencies (e.g., UNESCO, EU Education Directorate) compiling comparative gender-parity reports across member states using Bulgaria’s census outcomes
- University strategic planners forecasting future enrollment needs by analyzing historical gender-specific completion rates in Bulgarian higher education
- Data journalists fact-checking and visualizing gender participation in tertiary education for investigative articles on Bulgaria’s social progress
- Labor market analysts assessing the supply of male and female graduates for industry skills gap reports relying on official 2011 census statistics
- Open-data platform developers automating the ingestion of NSI’s education attainment tables to provide transparent, gender-disaggregated datasets to the public

```
import os
import json
from bs4 import BeautifulSoup
import re

# Define the recursive search function BEFORE using it
def find_data_recursively(obj, path=""):
    findings = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if this key might contain relevant data
            key_lower = key.lower()
            if any(term in key_lower for term in ['gender', 'male', 'female', 'men', 'women', 'tertiary', 'education', 'university', 'higher']):
                findings.append((current_path, type(value), str(value)[:300]))
            
            # Recurse into nested structures
            findings.extend(find_data_recursively(value, current_path))
    
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            current_path = f"{path}[{i}]"
            findings.extend(find_data_recursively(item, current_path))
    
    elif isinstance(obj, str):
        # Look for numerical patterns in strings
        if re.search(r'\d+', obj) and any(term in obj.lower() for term in ['education', 'tertiary', 'university', 'male', 'female', 'gender']):
            findings.append((path, "string_with_numbers", obj[:300]))
    
    return findings

# Now examine the most promising JSON file
workspace_dir = 'workspace'
promising_file = 'bulgarian_census_tertiary_education_comprehensive_final.json'
filepath = os.path.join(workspace_dir, promising_file)

print("=== EXTRACTING 2011 BULGARIAN CENSUS TERTIARY EDUCATION DATA BY GENDER ===")
print(f"\nAnalyzing: {promising_file}\n")

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== EXAMINING DETAILED DATA STRUCTURE ===")
    
    # Focus on the detailed_data section which contains the actual findings
    if 'detailed_data' in data and isinstance(data['detailed_data'], dict):
        detailed_data = data['detailed_data']
        print(f"\nDetailed data sections: {list(detailed_data.keys())}")
        
        # Examine tertiary_education_data
        if 'tertiary_education_data' in detailed_data:
            tertiary_data = detailed_data['tertiary_education_data']
            print(f"\n--- TERTIARY EDUCATION DATA ---")
            print(f"Number of tertiary education entries: {len(tertiary_data)}")
            
            for i, entry in enumerate(tertiary_data, 1):
                print(f"\nEntry {i}:")
                print(f"  Match text: {entry.get('match_text', 'N/A')}")
                print(f"  Has gender data: {entry.get('has_gender', False)}")
                print(f"  Has 2011 data: {entry.get('has_2011', False)}")
                print(f"  Has Bulgaria data: {entry.get('has_bulgaria', False)}")
                
                # Extract specific numbers from the match text
                match_text = entry.get('match_text', '')
                if match_text:
                    # Look for patterns like "male: X years" or "female: X years"
                    male_pattern = re.search(r'male:\s*(\d+)', match_text, re.IGNORECASE)
                    female_pattern = re.search(r'female:\s*(\d+)', match_text, re.IGNORECASE)
                    total_pattern = re.search(r'total:\s*(\d+)', match_text, re.IGNORECASE)
                    
                    if male_pattern or female_pattern or total_pattern:
                        print(f"  *** NUMERICAL DATA EXTRACTED ***")
                        if total_pattern:
                            print(f"    Total: {total_pattern.group(1)}")
                        if male_pattern:
                            print(f"    Male: {male_pattern.group(1)}")
                        if female_pattern:
                            print(f"    Female: {female_pattern.group(1)}")
        
        # Examine statistical_findings
        if 'statistical_findings' in detailed_data:
            stat_findings = detailed_data['statistical_findings']
            print(f"\n--- STATISTICAL FINDINGS ---")
            print(f"Number of statistical findings: {len(stat_findings)}")
            
            for i, finding in enumerate(stat_findings, 1):
                print(f"\nFinding {i}:")
                print(f"  Type: {finding.get('type', 'N/A')}")
                print(f"  Gender: {finding.get('gender', 'N/A')}")
                print(f"  Value: {finding.get('value', 'N/A')}")
                print(f"  Unit: {finding.get('unit', 'N/A')}")
                
                # Check if this is tertiary education related
                finding_type = finding.get('type', '').lower()
                if 'education' in finding_type or 'tertiary' in finding_type:
                    print(f"  *** EDUCATION-RELATED FINDING ***")
        
        # Examine census_2011_findings - FIX THE VARIABLE NAME ERROR
        if 'census_2011_findings' in detailed_data:
            census_findings = detailed_data['census_2011_findings']
            print(f"\n--- 2011 CENSUS FINDINGS ---")
            print(f"Number of census findings: {len(census_findings)}")
            
            for i, finding in enumerate(census_findings, 1):
                print(f"\nCensus Finding {i}:")
                census_text_content = finding.get('census_text', 'N/A')
                print(f"  Census text: {census_text_content}")
                
                # Look for education-related census data - FIXED VARIABLE REFERENCE
                if any(term in census_text_content.lower() for term in ['education', 'tertiary', 'university', 'degree']):
                    print(f"  *** EDUCATION-RELATED CENSUS DATA ***")
                    
                    # Extract numbers from census text
                    numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', census_text_content)
                    if numbers:
                        print(f"  Numbers found: {numbers}")
    
    print(f"\n=== RECURSIVE SEARCH FOR ALL RELEVANT DATA ===\n")
    
    # Use the recursive function to find all relevant data
    relevant_findings = find_data_recursively(data)
    
    if relevant_findings:
        print("All relevant gender/education data found:")
        for path, data_type, content in relevant_findings:
            print(f"\nPath: {path}")
            print(f"Type: {data_type}")
            print(f"Content: {content}")
            
            # If this contains numerical data, try to extract it
            if 'male' in content.lower() and 'female' in content.lower():
                print(f"  *** CONTAINS GENDER-SPECIFIC DATA ***")
                
                # Extract all numbers from this content
                numbers = re.findall(r'\b\d+(?:\.\d+)?\b', content)
                if numbers:
                    print(f"  Numbers extracted: {numbers}")
    else:
        print("No relevant gender/education data found through recursive search.")
    
    print(f"\n=== FINAL ANALYSIS AND CONCLUSION ===\n")
    
    # Determine what type of data we actually found
    data_analysis = {
        'source_analyzed': data.get('source_file', 'Unknown'),
        'data_type_found': 'School life expectancy (years of education)',
        'is_2011_census_data': False,
        'is_tertiary_completion_rate': False,
        'actual_data_found': {
            'metric': 'School life expectancy (primary to tertiary education)',
            'year': '2016',
            'total': '14 years',
            'male': '14 years',
            'female': '14 years'
        },
        'additional_findings': {
            'literacy_rates_2015': {
                'total': '98.4%',
                'male': '98.7%', 
                'female': '98.1%'
            },
            'youth_unemployment_2018': {
                'total': '12.7%',
                'male': '13.2%',
                'female': '13.9%'
            },
            'illiteracy_2011_census': '112,778 people aged nine or more are illiterate'
        }
    }
    
    print("CONCLUSION:")
    print("✗ The analyzed data does NOT contain the target information we need.")
    print("\nWhat we found:")
    print(f"  - School life expectancy: {data_analysis['actual_data_found']['total']} for both genders (2016 data)")
    print(f"  - Literacy rates from 2015 (not tertiary education completion)")
    print(f"  - Youth unemployment rates from 2018")
    print(f"  - General illiteracy data from 2011 census")
    
    print("\nWhat we NEED but did NOT find:")
    print("  - Specific number or percentage of men who completed tertiary education (2011 census)")
    print("  - Specific number or percentage of women who completed tertiary education (2011 census)")
    print("  - Official NSI census tables showing educational attainment by gender")
    
    print("\n=== NEXT STEPS RECOMMENDATION ===\n")
    print("The current workspace contains Wikipedia demographic data, not official NSI census tables.")
    print("To find the actual 2011 Bulgarian census tertiary education completion data by gender:")
    print("\n1. Search for official NSI (National Statistical Institute) census publications")
    print("2. Look for census tables specifically about 'Educational attainment' or 'Education level'")
    print("3. Find tables that break down tertiary/higher education completion by gender")
    print("4. Target NSI URLs like: www.nsi.bg/en/content/[census-education-tables]")
    
    # Save comprehensive analysis
    final_results = {
        'objective': '2011 Bulgarian Census - Tertiary Education Completion by Gender',
        'analysis_timestamp': '2025-01-11',
        'status': 'TARGET DATA NOT FOUND',
        'data_source_analyzed': 'Wikipedia Demographics of Bulgaria',
        'findings': data_analysis,
        'recommendation': 'Search official NSI census tables for educational attainment by gender',
        'next_search_targets': [
            'NSI official census publications',
            'Educational attainment census tables', 
            'Higher education completion statistics by gender',
            'Official Bulgarian government statistical yearbooks'
        ]
    }
    
    results_file = os.path.join(workspace_dir, 'bulgarian_census_tertiary_education_final_analysis.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nFinal analysis saved to: {results_file}")
    print("\nRECOMMENDATION: Need to search for official NSI census tables with actual tertiary education completion rates by gender from 2011 Bulgarian census.")

else:
    print(f"File not found: {filepath}")
```

### Development Step 38: Official 2011 Bulgarian Census: Tertiary Education Completion Statistics by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government education ministry policy planning to assess regional gender disparities in tertiary graduation rates and allocate funding for targeted scholarship programs
- Academic research study on the impact of socioeconomic factors on male and female university completion across Bulgarian municipalities
- NGO evaluation of women’s empowerment initiatives by comparing pre- and post-2011 census tertiary education attainment among female beneficiaries
- University benchmarking dashboard automating extraction of gender-segmented degree completion data to inform diversity and inclusion strategies
- HR consultancy workforce analysis integrating census education statistics by gender to advise clients on talent recruitment and training investments
- Data journalism project scraping and visualizing male vs. female higher education trends from official census tables for an interactive news feature
- Real estate market intelligence tool incorporating local tertiary education completion rates by gender into demographic profiles for housing development planning

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

workspace_dir = 'workspace'

print("=== PARSING HIGH-POTENTIAL NSI CENSUS FILES FOR TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Extract 2011 Bulgarian census tertiary education completion statistics by gender\n")

# First, let's inspect what files we have in the workspace
print("--- Inspecting Workspace Files ---")
if os.path.exists(workspace_dir):
    workspace_files = os.listdir(workspace_dir)
    print(f"Files in workspace: {len(workspace_files)}")
    
    # Show relevant files
    priority_files = [f for f in workspace_files if f.startswith('priority_census_link') and f.endswith('.html')]
    analysis_files = [f for f in workspace_files if 'analysis' in f and f.endswith('.json')]
    
    print(f"\nPriority census HTML files: {len(priority_files)}")
    for f in priority_files:
        print(f"  - {f}")
    
    print(f"\nAnalysis JSON files: {len(analysis_files)}")
    for f in analysis_files:
        print(f"  - {f}")
else:
    print("Workspace directory not found!")
    exit(1)

# Load previous analysis if available
analysis_file = os.path.join(workspace_dir, 'nsi_priority_census_analysis_fixed.json')
if os.path.exists(analysis_file):
    print("\n--- Loading Previous Analysis Results ---")
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    print(f"Analysis timestamp: {analysis_data.get('analysis_timestamp', 'Unknown')}")
    print(f"Successful census sources: {analysis_data.get('successful_census_sources', 0)}")
    
    # Get the high-potential sources
    census_sources = analysis_data.get('census_sources_details', [])
    high_potential_sources = [s for s in census_sources if s.get('total_indicator_score', 0) > 15]
    
    print(f"\nHigh-potential sources identified: {len(high_potential_sources)}")
    for i, source in enumerate(high_potential_sources, 1):
        print(f"  {i}. {source['filename']} - Score: {source['total_indicator_score']}")
        print(f"     Original text: '{source['original_text']}'")
        print(f"     Tables found: {source['tables_found']}")
else:
    print("Previous analysis file not found. Will examine all available priority census files.")
    high_potential_sources = []

# Define the priority files to analyze
priority_files_to_analyze = [
    'priority_census_link_5.html',  # Education and Lifelong Learning (score: 91)
    'priority_census_link_2.html',  # Census (score: 80)
    'priority_census_link_7.html',  # Population (Demography, Migration and Projections) (score: 79)
    'priority_census_link_6.html',  # Supply Use Tables (score: 79)
    'priority_census_link_8.html'   # Population Grid (score: 79)
]

print(f"\n=== PHASE 1: EXAMINING PRIORITY FILE STRUCTURES ===\n")

file_analysis_results = []

for filename in priority_files_to_analyze:
    filepath = os.path.join(workspace_dir, filename)
    if os.path.exists(filepath):
        print(f"--- Analyzing: {filename} ---")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"File size: {len(html_content):,} characters")
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get page title
        title = soup.find('title')
        if title:
            print(f"Page title: {title.get_text().strip()}")
        
        # Look for main content areas
        main_content = soup.find('main') or soup.find('div', class_='content') or soup.find('body')
        if main_content:
            content_text = main_content.get_text()
        else:
            content_text = soup.get_text()
        
        # Find all tables
        tables = soup.find_all('table')
        print(f"Tables found: {len(tables)}")
        
        # Look for links to data files or detailed census results - FIX THE VARIABLE SCOPING
        data_links = []
        for link in soup.find_all('a', href=True):
            # Define variables BEFORE using them
            link_href = link.get('href', '')
            link_text = link.get_text().strip()
            
            # Look for links to Excel files, PDFs, or census data
            has_data_file = any(ext in link_href.lower() for ext in ['.xls', '.xlsx', '.pdf', '.csv'])
            has_relevant_text = any(term in link_text.lower() for term in ['download', 'data', 'table', 'census', '2011', 'education'])
            
            if has_data_file or has_relevant_text:
                # Construct full URL
                if link_href.startswith('http'):
                    full_url = link_href
                elif link_href.startswith('/'):
                    full_url = f"https://www.nsi.bg{link_href}"
                else:
                    full_url = f"https://www.nsi.bg/en/{link_href}"
                
                data_links.append({
                    'text': link_text,
                    'href': link_href,
                    'full_url': full_url,
                    'has_data_file': has_data_file,
                    'has_relevant_text': has_relevant_text
                })
        
        print(f"Data file links found: {len(data_links)}")
        if data_links:
            print("Top data links:")
            for i, link in enumerate(data_links[:8], 1):
                print(f"  {i}. '{link['text']}'")
                print(f"     URL: {link['full_url']}")
                print(f"     Data file: {link['has_data_file']}, Relevant text: {link['has_relevant_text']}")
        
        # Search for specific education-related content
        education_content = []
        
        # Look for text patterns that might indicate tertiary education statistics
        education_patterns = [
            r'tertiary education.*?(?:male|female|men|women|gender)',
            r'higher education.*?(?:male|female|men|women|gender)',
            r'university.*?(?:male|female|men|women|gender)',
            r'(?:male|female|men|women).*?tertiary',
            r'(?:male|female|men|women).*?higher education',
            r'education.*?(?:by gender|gender breakdown)',
            r'2011.*?census.*?education',
            r'educational attainment.*?(?:male|female)',
            r'completed.*?tertiary.*?education',
            r'bachelor.*?degree.*?(?:male|female)',
            r'university.*?graduate.*?(?:male|female)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, content_text, re.IGNORECASE | re.DOTALL)
            if matches:
                for match in matches[:3]:  # Limit to first 3 matches per pattern
                    # Clean up the match
                    clean_match = re.sub(r'\s+', ' ', match.strip())[:200]
                    education_content.append(clean_match)
        
        if education_content:
            print(f"\nEducation-related content found: {len(education_content)}")
            for i, content in enumerate(education_content[:5], 1):
                print(f"  {i}. {content}...")
        
        # Look for tables that might contain education data
        relevant_tables = []
        for i, table in enumerate(tables):
            table_text = table.get_text().lower()
            
            # Check if table contains education and gender related terms
            has_education = any(term in table_text for term in ['education', 'tertiary', 'higher', 'university', 'degree'])
            has_gender = any(term in table_text for term in ['male', 'female', 'men', 'women', 'gender'])
            has_2011 = '2011' in table_text
            has_numbers = bool(re.search(r'\d+[,.]?\d*\s*%?', table_text))  # Look for numbers/percentages
            
            if has_education and (has_gender or has_2011):
                # Extract table headers for better analysis
                headers = []
                for th in table.find_all(['th', 'td'])[:10]:  # First 10 cells as potential headers
                    header_text = th.get_text().strip()
                    if header_text:
                        headers.append(header_text)
                
                relevant_tables.append({
                    'table_index': i,
                    'has_education': has_education,
                    'has_gender': has_gender,
                    'has_2011': has_2011,
                    'has_numbers': has_numbers,
                    'headers': headers[:5],  # First 5 headers
                    'table_text_sample': table_text[:300]
                })
        
        if relevant_tables:
            print(f"\nRelevant tables found: {len(relevant_tables)}")
            for table_info in relevant_tables:
                print(f"  Table {table_info['table_index']}: Education={table_info['has_education']}, Gender={table_info['has_gender']}, 2011={table_info['has_2011']}, Numbers={table_info['has_numbers']}")
                print(f"    Headers: {table_info['headers']}")
                print(f"    Sample: {table_info['table_text_sample'][:150]}...")
        
        # Look for specific census data indicators
        census_indicators = {
            'tertiary_mentions': content_text.lower().count('tertiary'),
            'higher_education_mentions': content_text.lower().count('higher education'),
            'university_mentions': content_text.lower().count('university'),
            'male_mentions': content_text.lower().count('male'),
            'female_mentions': content_text.lower().count('female'),
            'gender_mentions': content_text.lower().count('gender'),
            'census_2011_mentions': len(re.findall(r'2011.*?census|census.*?2011', content_text, re.IGNORECASE)),
            'percentage_numbers': len(re.findall(r'\d+[,.]?\d*\s*%', content_text))
        }
        
        print(f"\nCensus data indicators:")
        for indicator, count in census_indicators.items():
            if count > 0:
                print(f"  {indicator}: {count}")
        
        # Store analysis results
        potential_score = (
            len(relevant_tables) * 15 +  # Relevant tables are most important
            len(education_content) * 8 +  # Education content is very important
            len(data_links) * 5 +         # Data links are important
            census_indicators['census_2011_mentions'] * 10 +  # 2011 census mentions
            census_indicators['percentage_numbers'] * 3       # Statistical data
        )
        
        file_analysis_results.append({
            'filename': filename,
            'file_size': len(html_content),
            'tables_count': len(tables),
            'data_links_count': len(data_links),
            'data_links': data_links,
            'education_content_count': len(education_content),
            'education_content': education_content,
            'relevant_tables_count': len(relevant_tables),
            'relevant_tables': relevant_tables,
            'census_indicators': census_indicators,
            'potential_score': potential_score
        })
        
        print(f"\nPotential score for this file: {potential_score}")
        if potential_score > 50:
            print("*** VERY HIGH POTENTIAL FOR CENSUS DATA ***")
        elif potential_score > 25:
            print("** HIGH POTENTIAL FOR CENSUS DATA **")
        elif potential_score > 10:
            print("* MODERATE POTENTIAL FOR CENSUS DATA *")
        
        print("\n" + "="*60 + "\n")
    else:
        print(f"File not found: {filename}\n")

# Sort files by potential score
file_analysis_results.sort(key=lambda x: x['potential_score'], reverse=True)

print(f"=== PHASE 1 RESULTS SUMMARY ===\n")
print(f"Files analyzed: {len(file_analysis_results)}")

if file_analysis_results:
    print("\nFiles ranked by potential to contain tertiary education data by gender:")
    for i, result in enumerate(file_analysis_results, 1):
        print(f"\n{i}. {result['filename']} (Score: {result['potential_score']})")
        print(f"   File size: {result['file_size']:,} characters")
        print(f"   Tables: {result['tables_count']}, Relevant tables: {result['relevant_tables_count']}")
        print(f"   Data links: {result['data_links_count']}, Education content: {result['education_content_count']}")
        
        # Show key indicators
        indicators = result['census_indicators']
        key_indicators = {k: v for k, v in indicators.items() if v > 0}
        if key_indicators:
            print(f"   Key indicators: {key_indicators}")
        
        if result['potential_score'] > 50:
            print(f"   *** VERY HIGH PRIORITY FOR DETAILED ANALYSIS ***")
        elif result['potential_score'] > 25:
            print(f"   ** HIGH PRIORITY FOR DETAILED ANALYSIS **")
        elif result['potential_score'] > 10:
            print(f"   * MODERATE PRIORITY *")

# Save detailed analysis results
detailed_analysis = {
    'objective': '2011 Bulgarian Census - Tertiary Education by Gender - File Analysis',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'files_analyzed': len(file_analysis_results),
    'file_analysis_results': file_analysis_results,
    'summary': {
        'very_high_potential': len([r for r in file_analysis_results if r['potential_score'] > 50]),
        'high_potential': len([r for r in file_analysis_results if 25 < r['potential_score'] <= 50]),
        'moderate_potential': len([r for r in file_analysis_results if 10 < r['potential_score'] <= 25]),
        'low_potential': len([r for r in file_analysis_results if r['potential_score'] <= 10])
    },
    'next_steps': [
        'Extract data from highest-scoring files',
        'Parse relevant tables for tertiary education statistics',
        'Download and analyze data file links',
        'Look for specific male/female tertiary education completion numbers'
    ]
}

analysis_output_file = os.path.join(workspace_dir, 'nsi_census_files_detailed_analysis.json')
with open(analysis_output_file, 'w', encoding='utf-8') as f:
    json.dump(detailed_analysis, f, indent=2, ensure_ascii=False)

print(f"\n=== DETAILED ANALYSIS COMPLETE ===\n")
print(f"Detailed analysis saved to: {analysis_output_file}")

if file_analysis_results:
    top_file = file_analysis_results[0]
    print(f"\nTop priority file: {top_file['filename']} (Score: {top_file['potential_score']})")
    print(f"This file has:")
    print(f"  - {top_file['relevant_tables_count']} relevant tables")
    print(f"  - {top_file['data_links_count']} data links")
    print(f"  - {top_file['education_content_count']} education content matches")
    
    # Show the most promising data links from the top file
    if top_file['data_links']:
        print(f"\nMost promising data links from {top_file['filename']}:")
        for i, link in enumerate(top_file['data_links'][:5], 1):
            print(f"  {i}. '{link['text']}'")
            print(f"     {link['full_url']}")
    
    print(f"\nReady for detailed table parsing and data extraction from the top-scoring files.")
else:
    print("\nNo files were successfully analyzed. Check file availability.")
```

### Development Step 39: 2011 Bulgarian NSI Census: Tertiary Education Completion by Gender – Counts and Percentages

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government education policy planning and gender gap analysis: Using the 2011 tertiary completion figures by men and women to adjust funding and scholarship programs targeting underrepresented groups
- University admissions forecasting and equity program evaluation: Leveraging historical gender breakdowns in higher education to predict enrollment trends and measure outreach initiatives’ effectiveness
- Non-profit advocacy reporting on gender disparities: Extracting census data to support NGO reports and campaigns aimed at closing the tertiary education gap between men and women
- Educational publishing market research: Analyzing regional and gender-specific tertiary attainment rates to tailor textbook and e-learning product development for under-served cohorts
- Academic demographic studies for comparative research: Incorporating Bulgarian 2011 census tertiary completion numbers by gender into cross-national analyses of higher education trends in Eastern Europe
- Media fact-checking and infographic creation: Sourcing official census tables on male versus female tertiary graduates to produce accurate visual stories for news outlets and blogs
- Urban planning and resource allocation: Mapping district-level tertiary education completion rates by gender to guide local authorities in placing vocational centers and adult learning programs

```
import os
import json
from bs4 import BeautifulSoup
import re
import time
import requests

workspace_dir = 'workspace'

print("=== SEARCHING FOR OFFICIAL 2011 BULGARIAN CENSUS TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Find exact counts/percentages of men and women who completed tertiary education in 2011 Bulgarian census\n")

# Let's start with a direct approach - search for official NSI census publications
print("=== PHASE 1: DIRECT SEARCH FOR 2011 CENSUS EDUCATION PUBLICATIONS ===")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Try to access the main 2011 census page directly
census_2011_urls = [
    'https://www.nsi.bg/census2011/',
    'https://www.nsi.bg/en/content/6704/population-census-2011',
    'https://www.nsi.bg/en/content/6710/population-education',
    'https://www.nsi.bg/en/statistical-data/151'  # Census data section
]

successful_sources = []

for i, url in enumerate(census_2011_urls, 1):
    print(f"{i}. Accessing: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✓ Success! Content length: {len(response.content):,} bytes")
            
            # Save the content
            filename = f"census_2011_source_{i}.html"
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"   HTML file saved: {filename}")
            
            # Quick analysis for relevant content
            soup = BeautifulSoup(response.content, 'html.parser')
            content_text = soup.get_text().lower()
            
            # Look for education and gender indicators
            education_indicators = {
                'tertiary': content_text.count('tertiary'),
                'higher_education': content_text.count('higher education'),
                'university': content_text.count('university'),
                'education': content_text.count('education'),
                'male': content_text.count('male'),
                'female': content_text.count('female'),
                'gender': content_text.count('gender'),
                'men': content_text.count('men'),
                'women': content_text.count('women')
            }
            
            relevant_indicators = {k: v for k, v in education_indicators.items() if v > 0}
            if relevant_indicators:
                print(f"   Education/gender indicators: {relevant_indicators}")
            
            # Look for downloadable files (Excel, PDF)
            download_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if any(ext in href.lower() for ext in ['.xls', '.xlsx', '.pdf', '.csv']):
                    # Construct full URL
                    if href.startswith('http'):
                        full_url = href
                    elif href.startswith('/'):
                        full_url = f"https://www.nsi.bg{href}"
                    else:
                        full_url = f"https://www.nsi.bg/en/{href}"
                    
                    download_links.append({
                        'text': text,
                        'url': full_url,
                        'type': href.split('.')[-1].lower() if '.' in href else 'unknown'
                    })
            
            if download_links:
                print(f"   Download links found: {len(download_links)}")
                for j, dl in enumerate(download_links[:5], 1):
                    print(f"     {j}. {dl['type'].upper()}: '{dl['text']}' -> {dl['url']}")
            
            successful_sources.append({
                'url': url,
                'filename': filename,
                'content_size': len(response.content),
                'education_indicators': relevant_indicators,
                'download_links': download_links
            })
            
        else:
            print(f"   ✗ Failed - Status: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    time.sleep(2)  # Be respectful to the server

print(f"\n=== PHASE 1 RESULTS ===")
print(f"Successfully accessed: {len(successful_sources)} census sources")

# Now let's look for specific census publications or data tables
print(f"\n=== PHASE 2: SEARCHING FOR SPECIFIC CENSUS EDUCATION TABLES ===")

# Search for common census publication patterns
search_patterns = [
    'education level',
    'educational attainment',
    'tertiary education',
    'higher education',
    'population by education',
    'education and gender',
    'demographic characteristics',
    'census results education'
]

for source in successful_sources:
    print(f"\n--- Analyzing {source['filename']} for education data ---")
    
    filepath = os.path.join(workspace_dir, source['filename'])
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for links that might contain education statistics
    education_links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        text = link.get_text().strip()
        
        # Check if link text or href contains education-related terms
        text_lower = text.lower()
        href_lower = href.lower()
        
        is_education_related = False
        for pattern in search_patterns:
            if pattern in text_lower or pattern in href_lower:
                is_education_related = True
                break
        
        # Also check for general census results or statistical data
        if not is_education_related:
            general_terms = ['results', 'data', 'statistics', 'tables', 'publication', 'report']
            if any(term in text_lower for term in general_terms) and ('2011' in text_lower or '2011' in href_lower):
                is_education_related = True
        
        if is_education_related:
            # Construct full URL
            if href.startswith('http'):
                full_url = href
            elif href.startswith('/'):
                full_url = f"https://www.nsi.bg{href}"
            else:
                full_url = f"https://www.nsi.bg/en/{href}"
            
            education_links.append({
                'text': text,
                'href': href,
                'full_url': full_url
            })
    
    if education_links:
        print(f"Found {len(education_links)} education-related links:")
        for i, link in enumerate(education_links[:8], 1):
            print(f"  {i}. '{link['text']}'")
            print(f"     {link['full_url']}")
        
        # Try to access the most promising education links
        print(f"\n--- Accessing top education links from {source['filename']} ---")
        
        for i, link in enumerate(education_links[:3], 1):
            print(f"\nTrying education link {i}: {link['full_url']}")
            print(f"Link text: '{link['text']}'")
            
            try:
                response = requests.get(link['full_url'], headers=headers, timeout=15)
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"✓ Success! Content length: {len(response.content):,} bytes")
                    
                    # Save the content
                    link_filename = f"education_link_{source['filename'].split('.')[0]}_{i}.html"
                    link_filepath = os.path.join(workspace_dir, link_filename)
                    
                    with open(link_filepath, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"Saved: {link_filename}")
                    
                    # Quick analysis
                    link_soup = BeautifulSoup(response.content, 'html.parser')
                    link_content = link_soup.get_text().lower()
                    
                    # Look for specific tertiary education data
                    tertiary_count = link_content.count('tertiary')
                    gender_count = link_content.count('male') + link_content.count('female')
                    numbers_count = len(re.findall(r'\d+[,.]?\d*\s*%?', link_content))
                    
                    print(f"Content analysis: tertiary={tertiary_count}, gender_terms={gender_count}, numbers={numbers_count}")
                    
                    # Look for tables with potential data
                    tables = link_soup.find_all('table')
                    if tables:
                        print(f"Tables found: {len(tables)}")
                        
                        # Analyze first few tables for education data
                        for j, table in enumerate(tables[:3], 1):
                            table_text = table.get_text().lower()
                            if 'education' in table_text and ('male' in table_text or 'female' in table_text):
                                print(f"  Table {j}: Contains education and gender data")
                                print(f"    Sample: {table_text[:200]}...")
                    
                    if tertiary_count > 0 and gender_count > 0:
                        print(f"*** POTENTIAL DATA SOURCE - Contains tertiary education and gender information ***")
                
                else:
                    print(f"✗ Failed - Status: {response.status_code}")
                    
            except Exception as e:
                print(f"✗ Error: {str(e)}")
            
            time.sleep(2)
    else:
        print("No education-related links found")

# Save comprehensive search results
search_results = {
    'objective': '2011 Bulgarian Census - Tertiary Education by Gender',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'successful_sources': len(successful_sources),
    'sources_analyzed': successful_sources,
    'methodology': [
        'Direct access to NSI 2011 census pages',
        'Search for education-related links and publications',
        'Download and analyze census data sources',
        'Look for tertiary education statistics by gender'
    ],
    'next_steps': [
        'Parse downloaded HTML files for data tables',
        'Extract specific tertiary education completion numbers by gender',
        'Verify data is from official 2011 Bulgarian census',
        'Calculate percentages if only raw numbers are available'
    ]
}

results_file = os.path.join(workspace_dir, 'bulgarian_census_tertiary_education_search.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False)

print(f"\n=== SEARCH COMPLETE ===")
print(f"Search results saved to: {results_file}")
print(f"\nFiles created in workspace:")

# List all files created
if os.path.exists(workspace_dir):
    created_files = [f for f in os.listdir(workspace_dir) if f.startswith(('census_2011_source_', 'education_link_'))]
    for filename in created_files:
        filepath = os.path.join(workspace_dir, filename)
        file_size = os.path.getsize(filepath)
        print(f"  - {filename} ({file_size:,} bytes)")

print(f"\nNext step: Parse the downloaded census files to extract the specific tertiary education completion data by gender from the 2011 Bulgarian census.")
```

## Created Time
2025-08-14 07:15:14
