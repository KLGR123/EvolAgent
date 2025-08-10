# Developer Plan 01

## Plan
Fetch the World Bank API indicator data for all countries for series NY.GDS.TOTL.ZS (Gross domestic savings % of GDP) for years 2001 through 2010 inclusive, parse the JSON response, filter for countries whose annual savings values exceed 35.0 in every year of that period, and produce the final comma-separated list of country names sorted alphabetically.

## Description
This is the optimal next step because: (1) The core TASK requires identifying which countries maintained gross savings above 35% of GDP for each year from 2001–2010, (2) No data has yet been retrieved or processed, (3) Fetching and filtering the World Bank indicator data directly yields the required authoritative information, and (4) The outcome of this step is the exact list of qualifying countries needed to answer the TASK.

## Episodic Examples
### Development Step 47: Retrieve 2011 Bulgarian NSI census tertiary education completion numbers by gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government Ministry of Education uses automated scraping of the 2011 NSI census to extract gender-disaggregated tertiary completion data for designing targeted scholarship and parity programs
- A gender-equality NGO leverages the code to pull men’s and women’s university graduation rates across Bulgarian regions, pinpointing areas where additional outreach is needed
- University sociology researchers integrate the data extraction workflow into their analysis pipeline to study correlations between gendered education attainment and labor market outcomes
- Statistical consulting firms automate retrieval and parsing of NSI census spreadsheets to build interactive dashboards for clients tracking higher-education demographics by sex
- National news investigative teams use the scraper to quickly gather and verify male versus female tertiary education figures for in-depth reporting on academic access and equity
- International development agencies feed the gendered tertiary education data into predictive workforce models, informing policy briefs on future skills supply and gender balance
- Historical education trend analysts compile and compare multiple census years, including 2011, to publish longitudinal studies on gender gaps in higher education
- Corporate HR departments benchmark regional gender representation in tertiary qualifications against the 2011 Bulgarian census data to refine diversity and recruitment strategies

```
import os
import json
from bs4 import BeautifulSoup
import re
import requests
import time

workspace_dir = 'workspace'

print("=== ACCESSING 2011 BULGARIAN CENSUS TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Extract official 2011 Bulgarian census tertiary education completion statistics by gender\n")

# First, let's inspect what files we have in the workspace
print("--- Inspecting Workspace Files ---")
if os.path.exists(workspace_dir):
    all_files = os.listdir(workspace_dir)
    print(f"Total files in workspace: {len(all_files)}")
    
    # Look for analysis files
    analysis_files = [f for f in all_files if 'analysis' in f.lower() and f.endswith('.json')]
    print(f"\nAnalysis files found: {len(analysis_files)}")
    for f in analysis_files:
        print(f"  - {f}")
    
    # Look for NSI census source files
    nsi_files = [f for f in all_files if f.startswith('nsi_census_source_') and f.endswith('.html')]
    print(f"\nNSI census HTML files found: {len(nsi_files)}")
    for f in sorted(nsi_files):
        filepath = os.path.join(workspace_dir, f)
        file_size = os.path.getsize(filepath)
        print(f"  - {f} ({file_size:,} bytes)")
else:
    print("Workspace directory not found!")
    exit(1)

# Load the analysis results to understand what was found
analysis_file = os.path.join(workspace_dir, 'nsi_census_tertiary_education_final_analysis.json')

if os.path.exists(analysis_file):
    print("\n--- Loading Previous Analysis Results ---")
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    print(f"Analysis timestamp: {analysis_data['analysis_timestamp']}")
    print(f"Files analyzed: {analysis_data['files_analyzed']}")
    
    # Find the highest priority file from analysis
    if analysis_data['analysis_results']:
        top_result = analysis_data['analysis_results'][0]
        print(f"\nHighest priority file: {top_result['filename']}")
        print(f"Relevance score: {top_result['relevance_score']}")
        print(f"Education content matches: {len(top_result['education_content_matches'])}")
        
        # Show the education content that was found
        if top_result['education_content_matches']:
            print("\nKey education content found:")
            for i, match in enumerate(top_result['education_content_matches'][:5], 1):
                print(f"  {i}. {match[:150]}...")
        
        # Show download links that might contain the data
        if top_result['download_links']:
            print(f"\nDownload links found: {len(top_result['download_links'])}")
            # Look for the most promising links
            data_file_links = [link for link in top_result['download_links'] if link['is_data_file']]
            education_links = [link for link in top_result['download_links'] if 'education' in link['text'].lower() or 'census' in link['text'].lower()]
            
            print(f"Data file links: {len(data_file_links)}")
            print(f"Education-related links: {len(education_links)}")
            
            # Show most promising links
            promising_links = data_file_links + education_links
            if promising_links:
                print("\nMost promising links:")
                for i, link in enumerate(promising_links[:5], 1):
                    print(f"  {i}. '{link['text']}'")
                    print(f"     URL: {link['full_url']}")
                    print(f"     Type: {'Data file' if link['is_data_file'] else 'Web page'}")

# Based on the analysis, let's try to access the official NSI census results page
print("\n=== ACCESSING OFFICIAL NSI CENSUS RESULTS ===\n")

# From the analysis, we know there are links to census results
# Let's try to access the main census results page
census_results_urls = [
    'https://www.nsi.bg/en/content/6704/final-results-census-2011',
    'https://www.nsi.bg/en/content/6705/education',
    'https://www.nsi.bg/en/content/6710/population-education',
    'https://www.nsi.bg/census2011/PDOCS2/Census2011final_en.pdf'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for url in census_results_urls:
    print(f"Trying to access: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Successfully accessed {url}")
            print(f"Content length: {len(response.content):,} bytes")
            
            # Save the content for analysis
            filename = url.split('/')[-1].replace('.', '_') + '.html'
            if not filename.endswith('.html'):
                filename += '.html'
            
            filepath = os.path.join(workspace_dir, f'census_results_{filename}')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Content saved to: {filepath}")
            
            # Quick analysis of content
            soup = BeautifulSoup(response.text, 'html.parser')
            content_text = soup.get_text().lower()
            
            # Check for tertiary education and gender indicators
            tertiary_count = content_text.count('tertiary')
            education_count = content_text.count('education')
            male_count = content_text.count('male')
            female_count = content_text.count('female')
            men_count = content_text.count('men')
            women_count = content_text.count('women')
            
            print(f"Content analysis:")
            print(f"  Tertiary: {tertiary_count}, Education: {education_count}")
            print(f"  Male: {male_count}, Female: {female_count}, Men: {men_count}, Women: {women_count}")
            
            # Look for specific patterns
            patterns = [
                r'tertiary.*?education.*?\d+[,.]?\d*',
                r'higher.*?education.*?\d+[,.]?\d*',
                r'university.*?\d+[,.]?\d*',
                r'bachelor.*?\d+[,.]?\d*',
                r'graduate.*?\d+[,.]?\d*'
            ]
            
            found_patterns = []
            for pattern in patterns:
                matches = re.findall(pattern, content_text, re.IGNORECASE)
                found_patterns.extend(matches[:3])  # Limit to 3 per pattern
            
            if found_patterns:
                print(f"  Found {len(found_patterns)} education-related patterns:")
                for i, pattern in enumerate(found_patterns[:3], 1):
                    print(f"    {i}. {pattern[:100]}...")
            
            print("\n" + "="*50 + "\n")
            
        else:
            print(f"✗ Failed to access {url} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error accessing {url}: {str(e)}")
    
    time.sleep(2)  # Be respectful to the server

# Let's also try to access the NSI statistical data section directly
print("=== ACCESSING NSI STATISTICAL DATA SECTIONS ===\n")

nsi_data_urls = [
    'https://www.nsi.bg/en/content/6704/final-results-census-2011',
    'https://www.nsi.bg/en/content/6705/education',
    'https://www.nsi.bg/en/content/6710/population-education',
    'https://www.nsi.bg/en/content/2654/population-education-census-2011'
]

for url in nsi_data_urls:
    print(f"Accessing NSI data: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Successfully accessed NSI data page")
            
            # Save and analyze
            filename = f"nsi_data_{url.split('/')[-1]}.html"
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Data saved to: {filepath}")
            
            # Look for downloadable files
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            data_files = []
            for link in links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if any(ext in href.lower() for ext in ['.pdf', '.xls', '.xlsx', '.csv']):
                    if any(term in text.lower() for term in ['education', 'tertiary', 'census', '2011']):
                        full_url = href if href.startswith('http') else f"https://www.nsi.bg{href}"
                        data_files.append({
                            'text': text,
                            'url': full_url
                        })
            
            if data_files:
                print(f"Found {len(data_files)} relevant data files:")
                for i, file_info in enumerate(data_files[:5], 1):
                    print(f"  {i}. '{file_info['text']}'")
                    print(f"     URL: {file_info['url']}")
            
            print("\n" + "="*50 + "\n")
            
        else:
            print(f"✗ Failed - Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    time.sleep(2)

# Let's also examine the highest priority file we already have more carefully
print("=== DETAILED EXAMINATION OF HIGHEST PRIORITY FILE ===\n")

highest_priority_file = 'nsi_census_source_4.html'
file_path = os.path.join(workspace_dir, highest_priority_file)

if os.path.exists(file_path):
    print(f"Examining: {highest_priority_file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"File size: {len(html_content):,} characters")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    content_text = soup.get_text()
    
    # Look for specific census data sections
    print("\n--- Looking for Census Data Sections ---")
    
    # Search for text that mentions tertiary education with specific numbers
    tertiary_education_sections = []
    
    # Split content into paragraphs and analyze each
    paragraphs = content_text.split('\n')
    
    for i, paragraph in enumerate(paragraphs):
        para_lower = paragraph.lower().strip()
        if len(para_lower) > 20:  # Skip very short paragraphs
            # Check if paragraph contains tertiary education and gender/numbers
            has_tertiary = any(term in para_lower for term in ['tertiary', 'higher education', 'university', 'bachelor', 'master', 'degree'])
            has_gender = any(term in para_lower for term in ['male', 'female', 'men', 'women', 'sex', 'gender'])
            has_numbers = bool(re.search(r'\d+[,.]?\d*', para_lower))
            
            if has_tertiary and (has_gender or has_numbers):
                tertiary_education_sections.append({
                    'paragraph_index': i,
                    'content': paragraph.strip()[:500],  # First 500 characters
                    'has_tertiary': has_tertiary,
                    'has_gender': has_gender,
                    'has_numbers': has_numbers
                })
    
    if tertiary_education_sections:
        print(f"Found {len(tertiary_education_sections)} sections with tertiary education content:")
        for i, section in enumerate(tertiary_education_sections[:5], 1):
            print(f"\n  Section {i} (Paragraph {section['paragraph_index']}):")
            print(f"  Has tertiary: {section['has_tertiary']}, Has gender: {section['has_gender']}, Has numbers: {section['has_numbers']}")
            print(f"  Content: {section['content'][:200]}...")
    
    # Look for downloadable files mentioned in the content
    print("\n--- Looking for Downloadable Census Files ---")
    
    all_links = soup.find_all('a', href=True)
    census_files = []
    
    for link in all_links:
        href = link.get('href', '')
        text = link.get_text().strip()
        
        # Look for files that might contain 2011 census education data
        is_data_file = any(ext in href.lower() for ext in ['.pdf', '.xls', '.xlsx', '.csv', '.doc'])
        mentions_education = any(term in text.lower() for term in ['education', 'tertiary', 'university', 'degree', 'graduate'])
        mentions_2011 = '2011' in text or '2011' in href
        mentions_census = 'census' in text.lower() or 'census' in href.lower()
        
        if is_data_file and (mentions_education or mentions_2011 or mentions_census):
            full_url = href if href.startswith('http') else f"https://www.nsi.bg{href}"
            census_files.append({
                'text': text,
                'href': href,
                'full_url': full_url,
                'is_data_file': is_data_file,
                'mentions_education': mentions_education,
                'mentions_2011': mentions_2011,
                'mentions_census': mentions_census
            })
    
    if census_files:
        print(f"Found {len(census_files)} potential census data files:")
        for i, file_info in enumerate(census_files[:10], 1):
            print(f"\n  {i}. '{file_info['text']}'")
            print(f"     URL: {file_info['full_url']}")
            print(f"     Education: {file_info['mentions_education']}, 2011: {file_info['mentions_2011']}, Census: {file_info['mentions_census']}")
            if file_info['mentions_education'] and file_info['mentions_2011']:
                print(f"     *** HIGH PRIORITY - EDUCATION + 2011 ***")
    
    print(f"\n=== SUMMARY OF FINDINGS ===\n")
    print(f"Analysis completed for 2011 Bulgarian census tertiary education data by gender.")
    print(f"\nKey findings:")
    print(f"- Identified {len(tertiary_education_sections)} content sections with tertiary education information")
    print(f"- Found {len(census_files)} potential census data files")
    print(f"- Highest priority file (nsi_census_source_4.html) contains references to 'Tertiary education graduates by educational-qualification degree and sex'")
    
    if census_files:
        high_priority_files = [f for f in census_files if f['mentions_education'] and f['mentions_2011']]
        if high_priority_files:
            print(f"\n*** NEXT STEPS - ACCESS THESE HIGH PRIORITY FILES: ***")
            for i, file_info in enumerate(high_priority_files[:3], 1):
                print(f"  {i}. {file_info['text']}")
                print(f"     {file_info['full_url']}")
    
    print(f"\nThe analysis has successfully located official NSI sources that contain references to")
    print(f"'Tertiary education graduates by educational-qualification degree and sex' which directly")
    print(f"matches the PLAN objective for 2011 Bulgarian census tertiary education completion statistics by gender.")
    
else:
    print(f"Highest priority file {highest_priority_file} not found in workspace.")

print(f"\n=== ANALYSIS COMPLETE ===")
print(f"Ready to access specific census data files for exact tertiary education completion statistics by gender.")
```

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

### Development Step 36: Retrieve 2011 Bulgarian census tertiary education completion counts by gender from NSI

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- National education policy planning: Ministry of Education analysts automate retrieval of 2011 Bulgarian census tables on tertiary education by gender to inform funding allocations and future program design.
- Academic demographic research: University scholars scrape and parse official census data to study historical male–female gaps in higher education across Bulgarian regions.
- Market entry demographic profiling: Consulting firms extract regional tertiary education completion rates by gender from the 2011 census to assess skilled labor availability for new investments.
- NGO gender-equality reporting: Non-profits automatically gather authoritative male and female higher-education statistics from the NSI to support advocacy and policy recommendations.
- Longitudinal trend analysis: Think-tank data teams use the link discovery and scraping script to compile and compare gender-disaggregated tertiary education data across multiple census years.
- GIS-based educational mapping: Urban planners integrate scraped 2011 census figures into geographic information systems to visualize male and female tertiary attainment at municipal level.
- Accreditation and compliance audits: Educational quality assurance bodies auto-extract gender balance metrics in higher education from the official census to verify institutional compliance.
- Public-facing dashboard feeds: Government IT departments automate collection of 2011 NSI census data on tertiary education by gender to populate interactive citizen dashboards.

```
import os
import json
from bs4 import BeautifulSoup
import re
import requests
import time

workspace_dir = 'workspace'

print("=== ANALYZING DOWNLOADED NSI CONTENT FOR CENSUS DATA NAVIGATION ===")
print("\nObjective: Find links to actual 2011 census tables with tertiary education by gender\n")

# First, let's examine the structure of the downloaded NSI files
nsi_files = [
    'www_nsi_bg_en_content_6704_population-census-2011.html',
    'www_nsi_bg_en_content_6710_population-education.html', 
    'www_nsi_bg_en.html'
]

print("=== PHASE 1: EXAMINING NSI FILE STRUCTURES ===\n")

all_relevant_links = []

for filename in nsi_files:
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
        
        # Look for navigation menu or content sections
        nav_elements = soup.find_all(['nav', 'menu', 'ul', 'div'], class_=re.compile(r'(menu|nav|content|main)', re.I))
        print(f"Navigation elements found: {len(nav_elements)}")
        
        # Look for links that might lead to census data
        all_links = soup.find_all('a', href=True)
        print(f"Total links found: {len(all_links)}")
        
        # Filter for census/education related links - PROPERLY DEFINE VARIABLES
        relevant_links = []
        for link in all_links:
            # Define variables BEFORE using them in any expression
            href_value = link.get('href', '')
            text_value = link.get_text().strip()
            text_lower = text_value.lower()
            href_lower = href_value.lower()
            
            # Check for census, education, or statistical data related terms
            relevant_terms = ['census', '2011', 'education', 'population', 'statistics', 
                            'demographic', 'data', 'table', 'result', 'publication']
            
            # Check if any relevant terms are in the link text or href
            is_relevant = False
            for term in relevant_terms:
                if term in href_lower or term in text_lower:
                    is_relevant = True
                    break
            
            if is_relevant:
                # Construct full URL
                if href_value.startswith('http'):
                    full_url = href_value
                elif href_value.startswith('/'):
                    full_url = f"https://www.nsi.bg{href_value}"
                else:
                    full_url = f"https://www.nsi.bg/en/{href_value}"
                
                relevant_links.append({
                    'text': text_value,
                    'href': href_value,
                    'full_url': full_url,
                    'source_file': filename
                })
        
        print(f"Relevant links found: {len(relevant_links)}")
        
        if relevant_links:
            print("\nTop relevant links:")
            for i, link in enumerate(relevant_links[:10], 1):
                print(f"  {i}. Text: '{link['text']}'")
                print(f"     URL: {link['full_url']}")
        
        # Add to master list
        all_relevant_links.extend(relevant_links)
        
        # Look for specific content about census or education
        text_content = soup.get_text()
        
        # Search for specific phrases that might indicate census data availability
        census_phrases = [
            'population census 2011',
            'census results',
            'educational attainment',
            'tertiary education',
            'higher education',
            'education level',
            'by gender',
            'male female',
            'statistical data',
            'census tables'
        ]
        
        found_phrases = []
        for phrase in census_phrases:
            if phrase in text_content.lower():
                # Get context around the phrase
                pattern = re.compile(f'.{{0,100}}{re.escape(phrase)}.{{0,100}}', re.IGNORECASE | re.DOTALL)
                matches = pattern.findall(text_content)
                if matches:
                    found_phrases.append((phrase, matches[0].strip()))
        
        if found_phrases:
            print(f"\nRelevant content phrases found:")
            for phrase, context in found_phrases[:5]:
                print(f"  - '{phrase}': {context[:150]}...")
        
        print("\n" + "="*60 + "\n")
    else:
        print(f"File not found: {filename}\n")

print(f"=== CONSOLIDATED RELEVANT LINKS ANALYSIS ===\n")
print(f"Total relevant links found across all NSI files: {len(all_relevant_links)}")

# Remove duplicates and prioritize by relevance
unique_links = {}
for link in all_relevant_links:
    url = link['full_url']
    if url not in unique_links:
        unique_links[url] = link

print(f"Unique relevant links: {len(unique_links)}")

# Prioritize links that are most likely to contain census education data
priority_links = []
for url, link in unique_links.items():
    score = 0
    text_lower = link['text'].lower()
    url_lower = url.lower()
    
    # Scoring system for link relevance
    if '2011' in text_lower or '2011' in url_lower:
        score += 10
    if 'census' in text_lower or 'census' in url_lower:
        score += 8
    if 'education' in text_lower or 'education' in url_lower:
        score += 6
    if 'population' in text_lower or 'population' in url_lower:
        score += 4
    if 'result' in text_lower or 'result' in url_lower:
        score += 3
    if 'table' in text_lower or 'table' in url_lower:
        score += 5
    if 'data' in text_lower or 'data' in url_lower:
        score += 2
    
    if score > 0:
        priority_links.append((score, link))

# Sort by score
priority_links.sort(key=lambda x: x[0], reverse=True)

print(f"\nTop 15 priority links for census education data:")
for i, (score, link) in enumerate(priority_links[:15], 1):
    print(f"\n{i}. Score: {score}")
    print(f"   Text: '{link['text']}'")
    print(f"   URL: {link['full_url']}")
    print(f"   Source: {link['source_file']}")

print(f"\n=== PHASE 2: ATTEMPTING TO ACCESS TOP PRIORITY CENSUS LINKS ===\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

successful_census_sources = []

# Try accessing the top 8 priority links
for i, (score, link) in enumerate(priority_links[:8], 1):
    url = link['full_url']
    print(f"{i}. Trying priority link (Score: {score}): {url}")
    print(f"   Link text: '{link['text']}'")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✓ Success! Content length: {len(response.content):,} bytes")
            
            # Save the content
            filename = f"priority_census_link_{i}.html"
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"   HTML file saved: {filename}")
            
            # Quick analysis for HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table')
            print(f"   Tables found: {len(tables)}")
            
            # Check for education/gender content
            content_text = soup.get_text().lower()
            education_indicators = {
                'tertiary': content_text.count('tertiary'),
                'education': content_text.count('education'),
                'gender': content_text.count('gender'),
                'male': content_text.count('male'),
                'female': content_text.count('female'),
                '2011': content_text.count('2011'),
                'higher': content_text.count('higher'),
                'university': content_text.count('university')
            }
            
            relevant_indicators = {k: v for k, v in education_indicators.items() if v > 0}
            if relevant_indicators:
                print(f"   Education indicators: {relevant_indicators}")
                
                # If this looks promising, mark it
                total_score = sum(relevant_indicators.values())
                if total_score > 15:
                    print(f"   *** HIGH POTENTIAL - Total indicator score: {total_score} ***")
                elif total_score > 5:
                    print(f"   ** MODERATE POTENTIAL - Total indicator score: {total_score} **")
            
            successful_census_sources.append({
                'url': url,
                'filename': filename,
                'original_text': link['text'],
                'priority_score': score,
                'content_size': len(response.content),
                'tables_found': len(tables),
                'education_indicators': relevant_indicators,
                'total_indicator_score': sum(relevant_indicators.values())
            })
            
        else:
            print(f"   ✗ Failed - Status: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    time.sleep(2)  # Be respectful to the server

print(f"\n=== PHASE 2 RESULTS ===\n")
print(f"Successfully accessed: {len(successful_census_sources)} priority census sources")

if successful_census_sources:
    print("\nSuccessful downloads (ranked by education content potential):")
    # Sort by total education indicator score
    successful_census_sources.sort(key=lambda x: x.get('total_indicator_score', 0), reverse=True)
    
    for i, source in enumerate(successful_census_sources, 1):
        print(f"\n{i}. {source['filename']}")
        print(f"   Original link text: '{source['original_text']}'")
        print(f"   Priority score: {source['priority_score']}")
        print(f"   Content size: {source['content_size']:,} bytes")
        print(f"   Tables found: {source['tables_found']}")
        print(f"   Education indicators: {source['education_indicators']}")
        print(f"   Total indicator score: {source['total_indicator_score']}")
        print(f"   URL: {source['url']}")
        
        if source['total_indicator_score'] > 15:
            print(f"   *** RECOMMENDED FOR DETAILED ANALYSIS ***")
else:
    print("No priority census sources were successfully accessed.")

# Save comprehensive analysis results
analysis_results = {
    'objective': '2011 Bulgarian Census - Tertiary Education by Gender',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'nsi_files_analyzed': len([f for f in nsi_files if os.path.exists(os.path.join(workspace_dir, f))]),
    'total_relevant_links_found': len(all_relevant_links),
    'unique_relevant_links': len(unique_links),
    'priority_links_identified': len(priority_links),
    'successful_census_sources': len(successful_census_sources),
    'census_sources_details': successful_census_sources,
    'top_priority_links': [{'score': score, 'text': link['text'], 'url': link['full_url']} for score, link in priority_links[:15]],
    'recommendation': 'Analyze downloaded priority census files for tertiary education data tables',
    'next_steps': [
        'Parse successfully downloaded census HTML files for education tables',
        'Look for gender-disaggregated tertiary education statistics', 
        'Extract specific numbers/percentages for male and female tertiary education completion',
        'Verify data is from 2011 Bulgarian census'
    ]
}

results_file = os.path.join(workspace_dir, 'nsi_priority_census_analysis_fixed.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

print(f"\n=== ANALYSIS COMPLETE ===\n")
print(f"Comprehensive analysis saved to: {results_file}")
print(f"\nNext step: Parse any successfully downloaded census files for tertiary education data by gender")
print(f"Focus on files with high education indicator scores and multiple tables")

# Show final summary
if successful_census_sources:
    high_potential = [s for s in successful_census_sources if s['total_indicator_score'] > 15]
    moderate_potential = [s for s in successful_census_sources if 5 < s['total_indicator_score'] <= 15]
    
    print(f"\n=== FINAL SUMMARY ===\n")
    print(f"High potential sources (score > 15): {len(high_potential)}")
    print(f"Moderate potential sources (score 6-15): {len(moderate_potential)}")
    print(f"Low potential sources (score 1-5): {len(successful_census_sources) - len(high_potential) - len(moderate_potential)}")
    
    if high_potential:
        print(f"\n*** PRIORITY FILES FOR NEXT ANALYSIS ***")
        for source in high_potential:
            print(f"  - {source['filename']} (score: {source['total_indicator_score']})")
else:
    print(f"\nNo census sources were successfully downloaded. May need alternative search strategy.")
```

### Development Step 43: Search 2011 Bulgarian NSI Census Tertiary Education Completion Data by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government education policy planning and automated extraction of gender-disaggregated tertiary graduation rates from the 2011 Bulgarian census to inform funding allocations and program development
- Academic demographic research compiling male vs. female higher education completion statistics from NSI HTML tables for peer-reviewed studies on educational inequality
- Gender‐equality NGO reporting by scraping official Bulgarian census data to generate visualizations and support grant proposals targeting university access
- Data journalism investigations into historical tertiary education trends by gender in Bulgaria, converting raw NSI tables into interactive web charts for news articles
- Market segmentation analysis for e-learning providers, extracting regional tertiary attainment figures by sex from 2011 census sources to tailor course offerings
- Public administration benchmarking by automating retrieval of NSI census statistics on male and female university graduates for cross-country EU comparisons
- Educational consultancy deliverables compiling precise gender-disaggregated graduation numbers from official census downloads to advise clients on recruitment outreach
- IT compliance audits testing and validating web-scraping pipelines against Bulgarian government HTML sources to ensure integrity of gender-based census data extracts

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

workspace_dir = 'workspace'

print("=== PARSING NSI CENSUS FILES FOR 2011 BULGARIAN TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Extract official 2011 Bulgarian census tertiary education completion statistics by gender\n")

# First, inspect workspace files to understand what we have
print("--- Inspecting Workspace Files ---")
if os.path.exists(workspace_dir):
    all_files = os.listdir(workspace_dir)
    print(f"Total files in workspace: {len(all_files)}")
    
    # Look for NSI census source files
    nsi_files = [f for f in all_files if f.startswith('nsi_census_source_') and f.endswith('.html')]
    print(f"\nNSI census HTML files found: {len(nsi_files)}")
    for f in sorted(nsi_files):
        filepath = os.path.join(workspace_dir, f)
        file_size = os.path.getsize(filepath)
        print(f"  - {f} ({file_size:,} bytes)")
else:
    print("Workspace directory not found!")
    exit(1)

if not nsi_files:
    print("No NSI census files found. Cannot proceed with analysis.")
    exit(1)

print(f"\n=== PHASE 1: SYSTEMATIC ANALYSIS OF NSI CENSUS FILES ===\n")

analysis_results = []

for filename in sorted(nsi_files):
    print(f"--- Analyzing: {filename} ---")
    
    filepath = os.path.join(workspace_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"File size: {len(html_content):,} characters")
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get page title
    title = soup.find('title')
    page_title = title.get_text().strip() if title else 'No title found'
    print(f"Page title: {page_title}")
    
    # Get all text content for analysis
    content_text = soup.get_text()
    content_lower = content_text.lower()
    
    # Count key terms related to our search
    education_indicators = {
        'tertiary': content_lower.count('tertiary'),
        'higher_education': content_lower.count('higher education'),
        'university': content_lower.count('university'),
        'education': content_lower.count('education'),
        'degree': content_lower.count('degree'),
        'educational_attainment': content_lower.count('educational attainment')
    }
    
    gender_indicators = {
        'male': content_lower.count('male'),
        'female': content_lower.count('female'),
        'men': content_lower.count('men'),
        'women': content_lower.count('women'),
        'gender': content_lower.count('gender'),
        'by_sex': content_lower.count('by sex')
    }
    
    census_indicators = {
        '2011': content_lower.count('2011'),
        'census': content_lower.count('census'),
        'population': content_lower.count('population'),
        'statistics': content_lower.count('statistics')
    }
    
    print(f"Education indicators: {education_indicators}")
    print(f"Gender indicators: {gender_indicators}")
    print(f"Census indicators: {census_indicators}")
    
    # Find all tables
    tables = soup.find_all('table')
    print(f"Tables found: {len(tables)}")
    
    # Analyze tables for relevant content - FIX THE VARIABLE SCOPING ISSUE COMPLETELY
    relevant_tables = []
    for i, table in enumerate(tables):
        # DEFINE table_text FIRST at the beginning of the loop
        table_text = table.get_text().lower()
        
        # Now we can safely use table_text in all expressions
        has_education = any(term in table_text for term in ['education', 'tertiary', 'university', 'degree', 'higher'])
        has_gender = any(term in table_text for term in ['male', 'female', 'men', 'women', 'gender', 'sex'])
        has_census = '2011' in table_text or 'census' in table_text
        has_numbers = bool(re.search(r'\d+[,.]?\d*\s*%?', table_text))
        
        print(f"  Table {i}: Education={has_education}, Gender={has_gender}, Census={has_census}, Numbers={has_numbers}")
        
        if has_education or has_gender or has_census:
            # Extract table headers for analysis
            headers = []
            header_cells = table.find_all(['th', 'td'])[:15]  # First 15 cells as potential headers
            for cell in header_cells:
                cell_text = cell.get_text().strip()
                if cell_text and len(cell_text) < 100:  # Reasonable header length
                    headers.append(cell_text)
            
            # Get a sample of the table content
            table_sample = table_text[:300] if len(table_text) > 300 else table_text
            
            relevant_tables.append({
                'table_index': i,
                'has_education': has_education,
                'has_gender': has_gender,
                'has_census': has_census,
                'has_numbers': has_numbers,
                'headers': headers[:8],  # First 8 headers
                'table_text_sample': table_sample
            })
            
            print(f"    Headers: {headers[:5]}")  # Show first 5 headers
            print(f"    Sample: {table_sample[:150]}...")
    
    if relevant_tables:
        print(f"\nRelevant tables found: {len(relevant_tables)}")
    else:
        print("\nNo relevant tables found in this file")
    
    # Look for downloadable files - PROPER VARIABLE DEFINITION
    download_links = []
    all_links = soup.find_all('a', href=True)
    print(f"\nTotal links found: {len(all_links)}")
    
    for link in all_links:
        # PROPERLY DEFINE VARIABLES FIRST
        link_href = link.get('href', '')
        link_text = link.get_text().strip()
        
        # Check for data file extensions or relevant content
        is_data_file = any(ext in link_href.lower() for ext in ['.xls', '.xlsx', '.pdf', '.csv', '.doc', '.docx'])
        is_relevant_text = any(term in link_text.lower() for term in ['education', 'census', '2011', 'data', 'table', 'statistics', 'demographic'])
        
        if is_data_file or is_relevant_text:
            # Construct full URL
            if link_href.startswith('http'):
                full_url = link_href
            elif link_href.startswith('/'):
                full_url = f"https://www.nsi.bg{link_href}"
            else:
                full_url = f"https://www.nsi.bg/en/{link_href}"
            
            download_links.append({
                'text': link_text,
                'href': link_href,
                'full_url': full_url,
                'is_data_file': is_data_file,
                'is_relevant_text': is_relevant_text
            })
    
    print(f"Relevant download links found: {len(download_links)}")
    if download_links:
        print("Top download links:")
        for i, link in enumerate(download_links[:5], 1):
            print(f"  {i}. '{link['text']}'")
            print(f"     URL: {link['full_url']}")
            print(f"     Data file: {link['is_data_file']}, Relevant: {link['is_relevant_text']}")
    
    # Search for specific education content patterns
    education_content_matches = []
    
    # Patterns to find tertiary education by gender
    search_patterns = [
        r'tertiary education.*?(?:male|female|men|women|gender|sex)',
        r'higher education.*?(?:male|female|men|women|gender|sex)',
        r'university.*?(?:male|female|men|women|gender|sex)',
        r'(?:male|female|men|women).*?tertiary',
        r'(?:male|female|men|women).*?higher education',
        r'education.*?by.*?(?:gender|sex)',
        r'2011.*?census.*?education',
        r'educational attainment.*?(?:male|female)',
        r'completed.*?tertiary.*?education',
        r'bachelor.*?degree.*?(?:male|female)',
        r'university.*?graduate.*?(?:male|female)',
        r'\d+[,.]?\d*\s*%.*?(?:tertiary|higher education).*?(?:male|female)',
        r'(?:male|female).*?\d+[,.]?\d*\s*%.*?(?:tertiary|higher education)'
    ]
    
    for pattern in search_patterns:
        matches = re.findall(pattern, content_text, re.IGNORECASE | re.DOTALL)
        for match in matches[:3]:  # Limit to 3 matches per pattern
            clean_match = re.sub(r'\s+', ' ', match.strip())[:300]  # Clean and limit length
            if clean_match and clean_match not in education_content_matches:  # Avoid duplicates
                education_content_matches.append(clean_match)
    
    if education_content_matches:
        print(f"\nEducation content matches found: {len(education_content_matches)}")
        for i, match in enumerate(education_content_matches[:3], 1):
            print(f"  {i}. {match[:150]}...")
    
    # Calculate relevance score
    relevance_score = (
        sum(education_indicators.values()) * 3 +
        sum(gender_indicators.values()) * 2 +
        sum(census_indicators.values()) * 2 +
        len(relevant_tables) * 15 +
        len(education_content_matches) * 10 +
        len(download_links) * 5
    )
    
    print(f"\nRelevance score for {filename}: {relevance_score}")
    
    if relevance_score > 100:
        print("*** VERY HIGH PRIORITY - LIKELY CONTAINS TARGET DATA ***")
    elif relevance_score > 50:
        print("** HIGH PRIORITY - GOOD POTENTIAL FOR DATA **")
    elif relevance_score > 20:
        print("* MODERATE PRIORITY *")
    else:
        print("Low priority for tertiary education data")
    
    # Store analysis results
    analysis_results.append({
        'filename': filename,
        'page_title': page_title,
        'file_size': len(html_content),
        'education_indicators': education_indicators,
        'gender_indicators': gender_indicators,
        'census_indicators': census_indicators,
        'tables_count': len(tables),
        'relevant_tables': relevant_tables,
        'download_links': download_links,
        'education_content_matches': education_content_matches,
        'relevance_score': relevance_score
    })
    
    print("\n" + "="*60 + "\n")

# Sort by relevance score
analysis_results.sort(key=lambda x: x['relevance_score'], reverse=True)

print(f"=== ANALYSIS SUMMARY ===\n")
print(f"Files analyzed: {len(analysis_results)}")

if analysis_results:
    print("\nFiles ranked by relevance to tertiary education by gender:")
    for i, result in enumerate(analysis_results, 1):
        print(f"\n{i}. {result['filename']} (Score: {result['relevance_score']})")
        print(f"   Title: {result['page_title']}")
        print(f"   Size: {result['file_size']:,} characters")
        print(f"   Tables: {result['tables_count']}, Relevant: {len(result['relevant_tables'])}")
        print(f"   Download links: {len(result['download_links'])}")
        print(f"   Education matches: {len(result['education_content_matches'])}")
        
        # Show key indicators for high-scoring files
        if result['relevance_score'] > 30:
            print(f"   Education indicators: {result['education_indicators']}")
            print(f"   Gender indicators: {result['gender_indicators']}")
            print(f"   Census indicators: {result['census_indicators']}")
        
        # Show top download links for files with good potential
        if result['download_links'] and result['relevance_score'] > 30:
            print(f"   Top download links:")
            for j, link in enumerate(result['download_links'][:3], 1):
                print(f"     {j}. '{link['text']}'")
                print(f"        {link['full_url']}")
                if link['is_data_file']:
                    print(f"        *** DATA FILE - HIGH PRIORITY ***")

# Save comprehensive analysis
final_analysis = {
    'objective': '2011 Bulgarian Census - Tertiary Education by Gender Analysis',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'files_analyzed': len(analysis_results),
    'analysis_results': analysis_results,
    'summary': {
        'very_high_priority': len([r for r in analysis_results if r['relevance_score'] > 100]),
        'high_priority': len([r for r in analysis_results if 50 < r['relevance_score'] <= 100]),
        'moderate_priority': len([r for r in analysis_results if 20 < r['relevance_score'] <= 50]),
        'low_priority': len([r for r in analysis_results if r['relevance_score'] <= 20])
    },
    'next_steps': [
        'Access highest-priority download links for detailed census data',
        'Parse relevant tables for specific tertiary education statistics',
        'Extract male/female tertiary education completion numbers',
        'Verify data is from official 2011 Bulgarian census'
    ]
}

final_analysis_file = os.path.join(workspace_dir, 'nsi_census_tertiary_education_final_analysis.json')
with open(final_analysis_file, 'w', encoding='utf-8') as f:
    json.dump(final_analysis, f, indent=2, ensure_ascii=False)

print(f"\n=== COMPREHENSIVE ANALYSIS COMPLETE ===\n")
print(f"Analysis results saved to: {final_analysis_file}")

if analysis_results:
    top_result = analysis_results[0]
    print(f"\nHighest priority file: {top_result['filename']} (Score: {top_result['relevance_score']})")
    print(f"Title: {top_result['page_title']}")
    print(f"Contains {len(top_result['relevant_tables'])} relevant tables and {len(top_result['download_links'])} download links")
    
    if top_result['education_content_matches']:
        print(f"\nMost promising education content from top file:")
        for i, match in enumerate(top_result['education_content_matches'][:3], 1):
            print(f"  {i}. {match[:200]}...")
    
    if top_result['download_links']:
        print(f"\nMost promising download links from top file:")
        for i, link in enumerate(top_result['download_links'][:5], 1):
            print(f"  {i}. '{link['text']}'")
            print(f"     {link['full_url']}")
            if link['is_data_file']:
                print(f"     *** DATA FILE - HIGH PRIORITY FOR DOWNLOAD ***")
    
    print(f"\nReady to extract specific tertiary education completion data by gender from the highest-priority sources.")
    
    # Show the most promising files for next steps
    high_priority_files = [r for r in analysis_results if r['relevance_score'] > 30]
    if high_priority_files:
        print(f"\n=== NEXT STEPS RECOMMENDATIONS ===\n")
        print(f"Files with good potential for tertiary education data: {len(high_priority_files)}")
        for result in high_priority_files:
            print(f"\n- {result['filename']} (Score: {result['relevance_score']})")
            if result['download_links']:
                data_files = [link for link in result['download_links'] if link['is_data_file']]
                if data_files:
                    print(f"  Contains {len(data_files)} downloadable data files")
                    for df in data_files[:2]:
                        print(f"    - {df['text']}: {df['full_url']}")
else:
    print("\nNo analysis results generated. Check file availability and content.")
```

## Created Time
2025-08-10 04:20:26
