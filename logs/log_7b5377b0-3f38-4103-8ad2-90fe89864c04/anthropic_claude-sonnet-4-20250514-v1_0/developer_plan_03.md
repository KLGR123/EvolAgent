# Developer Plan 03

## Plan
Search for the height of the average woman in the Philippines according to a July 2023 Business Insider article to determine the value of C (height rounded to the nearest whole centimeter). Conduct a comprehensive web search using multiple approaches: (1) Search for 'Business Insider July 2023 average woman height Philippines', (2) Look up Business Insider articles from July 2023 about Filipino women's height statistics, (3) Search for 'Philippines women average height 2023 Business Insider', (4) Cross-reference the specific Business Insider publication to confirm the exact height measurement. Extract the height value and round it to the nearest whole centimeter as specified in the task.

## Description
This is the optimal next step because: (1) We have successfully determined L = 11 (Venezuelan independence 1811) and A = 2 (TikTok logo colors), and now need C (Filipino women's height) as the final variable in the equation Lx = (d/dx * (A * x²)) + 4097 - C, (2) The previous searches established two of three required variables, (3) Expected outcome is to obtain the specific height measurement from the July 2023 Business Insider article, rounded to the nearest whole centimeter, (4) This will provide all three variables needed to solve the differential equation and find the value of x to the nearest tenth.

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

### Development Step 37: Search 2011 NSI Bulgarian Census for Tertiary Education Completion Numbers by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government policy design and budget allocation for the Bulgarian Ministry of Education, using 2011 tertiary education completion numbers by gender to identify funding gaps between men and women
- Scholarship program targeting by an education-focused NGO, leveraging gender-disaggregated tertiary attainment data to prioritize underrepresented groups in specific regions
- Academic research on gender disparities in higher education, integrating precise male vs. female completion counts from the 2011 census into a comparative EU study
- Data journalism feature for a major Bulgarian news outlet, visualizing regional variations in tertiary graduation rates by gender to highlight social equity trends
- Market analysis for an edtech startup entering the Bulgarian market, assessing the male/female tertiary-educated population to tailor product offerings and marketing campaigns
- Workforce development planning by an international consultancy, using census-derived gender breakdowns of higher education attainment to advise corporate training initiatives
- UNESCO or World Bank report preparation, incorporating exact 2011 Bulgarian tertiary education statistics by gender into global education index assessments

```
import os
import json
from bs4 import BeautifulSoup
import re

workspace_dir = 'workspace'

print("=== PARSING HIGH-POTENTIAL NSI CENSUS FILES FOR TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Extract 2011 Bulgarian census tertiary education completion statistics by gender\n")

# First, let's check what analysis results we have from the previous step
analysis_file = os.path.join(workspace_dir, 'nsi_priority_census_analysis_fixed.json')
if os.path.exists(analysis_file):
    print("--- Loading Previous Analysis Results ---")
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
    print("Previous analysis file not found. Will examine all priority census files.")
    high_potential_sources = []

# Define the priority files to analyze based on previous results
priority_files = [
    'priority_census_link_5.html',  # Education and Lifelong Learning (score: 91)
    'priority_census_link_2.html',  # Census (score: 80)
    'priority_census_link_7.html',  # Population (Demography, Migration and Projections) (score: 79)
    'priority_census_link_6.html',  # Supply Use Tables (score: 79)
    'priority_census_link_8.html'   # Population Grid (score: 79)
]

print(f"\n=== PHASE 1: EXAMINING PRIORITY FILE STRUCTURES ===\n")

file_analysis_results = []

for filename in priority_files:
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
        
        # Look for links to data files or detailed census results
        data_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            text = link.get_text().strip()
            
            # Look for links to Excel files, PDFs, or census data
            if any(ext in href.lower() for ext in ['.xls', '.xlsx', '.pdf', '.csv']) or \
               any(term in text.lower() for term in ['download', 'data', 'table', 'census', '2011', 'education']):
                
                # Construct full URL
                if href.startswith('http'):
                    full_url = href
                elif href.startswith('/'):
                    full_url = f"https://www.nsi.bg{href}"
                else:
                    full_url = f"https://www.nsi.bg/en/{href}"
                
                data_links.append({
                    'text': text,
                    'href': href,
                    'full_url': full_url
                })
        
        print(f"Data file links found: {len(data_links)}")
        if data_links:
            print("Top data links:")
            for i, link in enumerate(data_links[:5], 1):
                print(f"  {i}. '{link['text']}' -> {link['full_url']}")
        
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
            r'educational attainment.*?(?:male|female)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, content_text, re.IGNORECASE | re.DOTALL)
            if matches:
                for match in matches[:3]:  # Limit to first 3 matches per pattern
                    # Clean up the match
                    clean_match = re.sub(r'\s+', ' ', match.strip())[:200]
                    education_content.append(clean_match)
        
        if education_content:
            print(f"\nEducation-related content found:")
            for i, content in enumerate(education_content[:5], 1):
                print(f"  {i}. {content}...")
        
        # Look for tables that might contain education data
        relevant_tables = []
        for i, table in enumerate(tables):
            table_text = table.get_text().lower()
            
            # Check if table contains education and gender related terms
            has_education = any(term in table_text for term in ['education', 'tertiary', 'higher', 'university'])
            has_gender = any(term in table_text for term in ['male', 'female', 'men', 'women', 'gender'])
            has_2011 = '2011' in table_text
            
            if has_education and (has_gender or has_2011):
                relevant_tables.append({
                    'table_index': i,
                    'has_education': has_education,
                    'has_gender': has_gender,
                    'has_2011': has_2011,
                    'table_text_sample': table_text[:300]
                })
        
        if relevant_tables:
            print(f"\nRelevant tables found: {len(relevant_tables)}")
            for table_info in relevant_tables:
                print(f"  Table {table_info['table_index']}: Education={table_info['has_education']}, Gender={table_info['has_gender']}, 2011={table_info['has_2011']}")
                print(f"    Sample: {table_info['table_text_sample'][:150]}...")
        
        # Store analysis results
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
            'potential_score': len(relevant_tables) * 10 + len(education_content) * 5 + len(data_links) * 3
        })
        
        print(f"Potential score for this file: {file_analysis_results[-1]['potential_score']}")
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
        print(f"   Tables: {result['tables_count']}, Data links: {result['data_links_count']}, Education content: {result['education_content_count']}")
        print(f"   Relevant tables: {result['relevant_tables_count']}")
        
        if result['potential_score'] > 20:
            print(f"   *** HIGH PRIORITY FOR DETAILED ANALYSIS ***")
        elif result['potential_score'] > 10:
            print(f"   ** MODERATE PRIORITY **")

# Save detailed analysis results
detailed_analysis = {
    'objective': '2011 Bulgarian Census - Tertiary Education by Gender - File Analysis',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'files_analyzed': len(file_analysis_results),
    'file_analysis_results': file_analysis_results,
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
print(f"\nNext step: Focus on highest-scoring files for data extraction")

if file_analysis_results:
    top_file = file_analysis_results[0]
    print(f"\nTop priority file: {top_file['filename']} (Score: {top_file['potential_score']})")
    print(f"This file has {top_file['relevant_tables_count']} relevant tables and {top_file['data_links_count']} data links")
    print(f"Ready for detailed table parsing and data extraction")
```

### Development Step 26: Search Official 2011 Bulgarian Census Data for Tertiary Education Completion by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Analysis of regional gender disparities in higher education to inform targeted scholarship and grant programs by public policy analysts
- Academic demographic research for publishing a longitudinal study on tertiary education attainment trends by gender in scholarly journals
- NGO impact evaluation for women’s empowerment initiatives using census-derived tertiary education completion rates to measure program effectiveness
- Market demand assessment by EdTech companies to tailor online course offerings based on regional male and female higher‐education levels
- Investigative journalism fact‐checking of gender parity in universities for feature articles on education equality and social development
- Municipal workforce planning to identify local skill shortages and plan vocational training initiatives using gender‐segmented tertiary education data
- EU grant proposal preparation requiring detailed gender breakdowns of tertiary education attainment to justify funding allocations for educational projects
- Corporate site‐selection analysis by multinational firms evaluating the local talent pool’s education levels and gender composition before opening new offices

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
        
        # Parse and analyze content - FIX: Define content_text BEFORE using it
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('title')
        title_text = title.get_text().strip() if title else 'No title found'
        
        # FIXED: Define content_text before using it in generator expressions
        content_text = soup.get_text().lower()
        
        # Look for education and census related content
        education_keywords = ['tertiary education', 'higher education', 'university', 'education level', 'educational attainment', 'census 2011', 'висше образование']
        gender_keywords = ['gender', 'men', 'women', 'male', 'female', 'мъже', 'жени']
        
        has_education_content = any(keyword in content_text for keyword in education_keywords)
        has_gender_content = any(keyword in content_text for keyword in gender_keywords)
        has_2011_content = '2011' in content_text
        
        # Look for links to census data or education statistics
        links = soup.find_all('a', href=True)
        relevant_links = []
        
        for link in links:
            href = link.get('href', '')
            link_text = link.get_text().strip().lower()
            
            if any(keyword in (href.lower() + ' ' + link_text) for keyword in ['census', '2011', 'education', 'образование']):
                full_url = href if href.startswith('http') else f"https://www.nsi.bg{href}" if href.startswith('/') else f"https://www.nsi.bg/{href}"
                relevant_links.append({
                    'text': link.get_text().strip(),
                    'url': full_url
                })
        
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
        print(f"Found {len(relevant_links)} relevant links")
        
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
priority_sources = []
for source in successful_sources:
    priority_score = 0
    if source['has_education_content']:
        priority_score += 3
    if source['has_gender_content']:
        priority_score += 2
    if source['has_2011_content']:
        priority_score += 2
    if len(source['relevant_links']) > 0:
        priority_score += 1
    
    source['priority_score'] = priority_score
    if priority_score >= 4:  # High priority threshold
        priority_sources.append(source)

# Sort by priority score
priority_sources.sort(key=lambda x: x['priority_score'], reverse=True)

print(f"\n=== HIGH PRIORITY SOURCES FOR DETAILED ANALYSIS ===\n")
print(f"Found {len(priority_sources)} high-priority sources")

for i, source in enumerate(priority_sources, 1):
    print(f"\n{i}. {source['url']} (Priority Score: {source['priority_score']})")
    print(f"   Title: {source['title']}")
    print(f"   Education content: {source['has_education_content']}")
    print(f"   Gender content: {source['has_gender_content']}")
    print(f"   2011 content: {source['has_2011_content']}")
    print(f"   Relevant links: {len(source['relevant_links'])}")

# Follow up on the most relevant links from priority sources
print(f"\n=== FOLLOWING UP ON RELEVANT LINKS ===\n")

additional_sources = []
for source in priority_sources[:2]:  # Check top 2 priority sources
    print(f"Following links from: {source['url']}")
    
    for link_info in source['relevant_links'][:3]:  # Check top 3 links from each source
        link_url = link_info['url']
        link_text = link_info['text']
        
        print(f"\nChecking link: {link_text}")
        print(f"URL: {link_url}")
        
        response = fetch_with_headers(link_url)
        
        if response and response.status_code == 200:
            print(f"✓ Successfully accessed link")
            
            # Save this content too
            safe_filename = re.sub(r'[^\w\-_\.]', '_', link_text)[:50]
            filename = f'nsi_link_{safe_filename}.html'
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Quick analysis of this linked content
            soup = BeautifulSoup(response.content, 'html.parser')
            content_text = soup.get_text().lower()
            
            # Look for specific tertiary education data
            tertiary_indicators = ['tertiary education', 'higher education', 'university degree', 'bachelor', 'master', 'висше образование']
            has_tertiary_data = any(indicator in content_text for indicator in tertiary_indicators)
            
            # Look for statistical tables or data
            tables = soup.find_all('table')
            has_tables = len(tables) > 0
            
            additional_info = {
                'source_url': source['url'],
                'link_text': link_text,
                'link_url': link_url,
                'filename': filepath,
                'has_tertiary_data': has_tertiary_data,
                'has_tables': has_tables,
                'table_count': len(tables),
                'content_length': len(response.text)
            }
            
            additional_sources.append(additional_info)
            
            print(f"   Saved to: {filename}")
            print(f"   Has tertiary education data: {has_tertiary_data}")
            print(f"   Has tables: {has_tables} ({len(tables)} tables found)")
            
        else:
            print(f"✗ Failed to access link")
        
        time.sleep(2)

# Save comprehensive research summary
research_summary = {
    'research_target': '2011 Bulgarian Census - Tertiary Education by Gender',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'total_sources_attempted': len(target_urls),
    'successful_sources': len(successful_sources),
    'priority_sources': len(priority_sources),
    'additional_links_checked': len(additional_sources),
    'sources_data': successful_sources,
    'priority_sources_data': priority_sources,
    'additional_sources_data': additional_sources,
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

for source in additional_sources:
    print(f"  - {os.path.basename(source['filename'])} (linked content)")

print(f"\nNext steps:")
print(f"1. Parse downloaded HTML files for statistical tables")
print(f"2. Look for census data with education levels broken down by gender")
print(f"3. Extract specific tertiary education completion numbers")

if priority_sources:
    print(f"\nMost promising source: {priority_sources[0]['url']}")
    print(f"Priority score: {priority_sources[0]['priority_score']}")
else:
    print(f"\nNo high-priority sources identified. Will need alternative search strategy.")
```

### Development Step 35: Search Official 2011 Bulgarian Census Tertiary Education Completion Figures by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government policy planning for the Bulgarian Ministry of Education to quantify the male–female gap in tertiary degree completion and tailor scholarship programs by region.
- Academic sociology research analyzing 2011 census tertiary education figures by gender to study long-term trends in Bulgarian educational attainment and publish in peer-reviewed journals.
- Non-profit gender-equality advocacy using disaggregated census data to identify municipalities where women’s higher education rates lag and design targeted community outreach initiatives.
- EdTech market analysis by educational technology companies to map regions with low tertiary completion and prioritize e-learning platform deployments for underserved student populations.
- International development reporting for the European Commission or World Bank to benchmark Bulgaria’s progress in closing gender disparities in higher education against other EU member states.
- Data journalism investigations visualizing 2011 census tables on tertiary education by gender to produce interactive web articles highlighting regional inequality hotspots.
- Freelance data-visualization consulting delivering interactive dashboards to NGOs and local governments, showing detailed male vs. female tertiary attainment percentages for strategic planning.

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
        
        # Filter for census/education related links - FIX THE VARIABLE SCOPING
        relevant_links = []
        for link in all_links:
            link_href = link.get('href', '')
            link_text = link.get_text().strip().lower()
            
            # Look for census, education, or statistical data related links
            if any(term in link_href.lower() or term in link_text for term in [
                'census', '2011', 'education', 'population', 'statistics', 
                'demographic', 'data', 'table', 'result', 'publication'
            ]):
                full_url = link_href if link_href.startswith('http') else f"https://www.nsi.bg{link_href}" if link_href.startswith('/') else f"https://www.nsi.bg/en/{link_href}"
                
                relevant_links.append({
                    'text': link.get_text().strip(),
                    'href': link_href,
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

print(f"\nTop 10 priority links for census education data:")
for i, (score, link) in enumerate(priority_links[:10], 1):
    print(f"\n{i}. Score: {score}")
    print(f"   Text: '{link['text']}'")
    print(f"   URL: {link['full_url']}")
    print(f"   Source: {link['source_file']}")

print(f"\n=== PHASE 2: ATTEMPTING TO ACCESS TOP PRIORITY CENSUS LINKS ===\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

successful_census_sources = []

# Try accessing the top 5 priority links
for i, (score, link) in enumerate(priority_links[:5], 1):
    url = link['full_url']
    print(f"{i}. Trying priority link (Score: {score}): {url}")
    
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
            if tables:
                print(f"   Tables found: {len(tables)}")
            
            # Check for education/gender content
            content_text = soup.get_text().lower()
            education_indicators = {
                'tertiary': content_text.count('tertiary'),
                'education': content_text.count('education'),
                'gender': content_text.count('gender'),
                'male': content_text.count('male'),
                'female': content_text.count('female'),
                '2011': content_text.count('2011')
            }
            
            relevant_indicators = {k: v for k, v in education_indicators.items() if v > 0}
            if relevant_indicators:
                print(f"   Education indicators: {relevant_indicators}")
                
                # If this looks promising, mark it
                total_score = sum(relevant_indicators.values())
                if total_score > 10:
                    print(f"   *** HIGH POTENTIAL - Total indicator score: {total_score} ***")
            
            successful_census_sources.append({
                'url': url,
                'filename': filename,
                'original_text': link['text'],
                'priority_score': score,
                'content_size': len(response.content),
                'tables_found': len(tables),
                'education_indicators': relevant_indicators
            })
            
        else:
            print(f"   ✗ Failed - Status: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
    
    time.sleep(2)  # Be respectful to the server

print(f"\n=== PHASE 2 RESULTS ===\n")
print(f"Successfully accessed: {len(successful_census_sources)} priority census sources")

if successful_census_sources:
    print("\nSuccessful downloads (ranked by potential):")
    # Sort by education indicators total
    successful_census_sources.sort(key=lambda x: sum(x.get('education_indicators', {}).values()), reverse=True)
    
    for i, source in enumerate(successful_census_sources, 1):
        print(f"\n{i}. {source['filename']}")
        print(f"   Original link text: '{source['original_text']}'")
        print(f"   Priority score: {source['priority_score']}")
        print(f"   Content size: {source['content_size']:,} bytes")
        print(f"   Tables found: {source['tables_found']}")
        print(f"   Education indicators: {source['education_indicators']}")
        print(f"   URL: {source['url']}")
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
    'top_priority_links': [{'score': score, 'text': link['text'], 'url': link['full_url']} for score, link in priority_links[:10]],
    'recommendation': 'Analyze downloaded priority census files for tertiary education data tables',
    'next_steps': [
        'Parse successfully downloaded census HTML files for education tables',
        'Look for gender-disaggregated tertiary education statistics',
        'Extract specific numbers/percentages for male and female tertiary education completion',
        'Verify data is from 2011 Bulgarian census'
    ]
}

results_file = os.path.join(workspace_dir, 'nsi_priority_census_analysis.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

print(f"\n=== ANALYSIS COMPLETE ===\n")
print(f"Comprehensive analysis saved to: {results_file}")
print(f"\nNext step: Parse any successfully downloaded census files for tertiary education data by gender")
print(f"Focus on files with high education indicator scores and multiple tables")
```

## Created Time
2025-08-14 06:14:33
