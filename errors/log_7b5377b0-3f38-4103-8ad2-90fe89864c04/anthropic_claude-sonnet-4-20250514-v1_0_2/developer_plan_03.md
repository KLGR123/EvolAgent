# Developer Plan 03

## Plan
Search for the height of the average woman in the Philippines according to a July 2023 Business Insider article to determine the value of C (height rounded to the nearest whole centimeter). Focus on finding the specific Business Insider article from July 2023 that contains Philippine women's average height data.

## Description
This is the necessary next step because: (1) We have successfully determined L = 10 from the Venezuelan Declaration of Independence year (1810) and A = 2 from the TikTok logo colors excluding black and white, (2) We need to find the final variable C in the equation Lx = (d/dx * (A * x²)) + 4097 - C, (3) Expected outcome is to locate the specific Business Insider article from July 2023 and extract the average height of Philippine women rounded to the nearest whole centimeter, (4) Once we have all three variables (L, A, C), we can solve the complete equation 10x = (d/dx * (2 * x²)) + 4097 - C for x to the nearest tenth.

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

### Development Step 45: Find Official 2011 Bulgarian Census Tertiary Education Completion Numbers by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government policy analysis and targeted funding allocation for gender-based tertiary education initiatives in Bulgarian regions
- Academic demographic research and comparative gender gap studies in higher education using 2011 Bulgarian census data
- EdTech market intelligence and user segment estimation based on regional tertiary education attainment by gender
- NGO program evaluation and impact measurement for women’s empowerment projects using automated extraction of gender-specific education statistics
- Corporate HR localization strategy and talent pool assessment for setting up Bulgarian R&D centers based on male/female graduate distribution
- Data journalism and interactive visualization of male versus female tertiary education completion rates across Bulgarian municipalities
- Urban planning and real estate forecasting by correlating local tertiary education profiles by gender with housing demand near universities
- Public health communication segmentation and health literacy campaign design using census-derived tertiary education levels by gender

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
    
    # Analyze tables for relevant content - COMPLETELY RESTRUCTURE TO AVOID SCOPING ISSUES
    relevant_tables = []
    
    # Process each table individually to avoid variable scoping issues
    for i, table in enumerate(tables):
        # Extract table text at the very beginning
        current_table_text = table.get_text().lower()
        
        # Check content flags
        education_flag = False
        gender_flag = False
        census_flag = False
        numbers_flag = False
        
        # Check for education terms
        education_terms = ['education', 'tertiary', 'university', 'degree', 'higher']
        for term in education_terms:
            if term in current_table_text:
                education_flag = True
                break
        
        # Check for gender terms
        gender_terms = ['male', 'female', 'men', 'women', 'gender', 'sex']
        for term in gender_terms:
            if term in current_table_text:
                gender_flag = True
                break
        
        # Check for census terms
        if '2011' in current_table_text or 'census' in current_table_text:
            census_flag = True
        
        # Check for numbers
        if re.search(r'\d+[,.]?\d*\s*%?', current_table_text):
            numbers_flag = True
        
        print(f"  Table {i}: Education={education_flag}, Gender={gender_flag}, Census={census_flag}, Numbers={numbers_flag}")
        
        # If table has any relevant content, analyze further
        if education_flag or gender_flag or census_flag:
            # Extract table headers for analysis
            headers_list = []
            header_cells = table.find_all(['th', 'td'])[:15]  # First 15 cells as potential headers
            for cell in header_cells:
                cell_text = cell.get_text().strip()
                if cell_text and len(cell_text) < 100:  # Reasonable header length
                    headers_list.append(cell_text)
            
            # Get a sample of the table content
            table_sample = current_table_text[:300] if len(current_table_text) > 300 else current_table_text
            
            relevant_tables.append({
                'table_index': i,
                'has_education': education_flag,
                'has_gender': gender_flag,
                'has_census': census_flag,
                'has_numbers': numbers_flag,
                'headers': headers_list[:8],  # First 8 headers
                'table_text_sample': table_sample
            })
            
            print(f"    Headers: {headers_list[:5]}")  # Show first 5 headers
            print(f"    Sample: {table_sample[:150]}...")
    
    if relevant_tables:
        print(f"\nRelevant tables found: {len(relevant_tables)}")
    else:
        print("\nNo relevant tables found in this file")
    
    # Look for downloadable files - COMPLETELY FIX VARIABLE SCOPING
    download_links = []
    all_links = soup.find_all('a', href=True)
    print(f"\nTotal links found: {len(all_links)}")
    
    # Process each link individually to avoid scoping issues
    for link in all_links:
        # DEFINE ALL VARIABLES AT THE BEGINNING OF THE LOOP
        current_link_href = link.get('href', '')
        current_link_text = link.get_text().strip()
        
        # Check for data file extensions
        data_file_extensions = ['.xls', '.xlsx', '.pdf', '.csv', '.doc', '.docx']
        is_data_file = False
        for ext in data_file_extensions:
            if ext in current_link_href.lower():
                is_data_file = True
                break
        
        # Check for relevant text content
        relevant_terms = ['education', 'census', '2011', 'data', 'table', 'statistics', 'demographic']
        is_relevant_text = False
        for term in relevant_terms:
            if term in current_link_text.lower():
                is_relevant_text = True
                break
        
        if is_data_file or is_relevant_text:
            # Construct full URL
            if current_link_href.startswith('http'):
                full_url = current_link_href
            elif current_link_href.startswith('/'):
                full_url = f"https://www.nsi.bg{current_link_href}"
            else:
                full_url = f"https://www.nsi.bg/en/{current_link_href}"
            
            download_links.append({
                'text': current_link_text,
                'href': current_link_href,
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
2025-08-14 06:46:25
