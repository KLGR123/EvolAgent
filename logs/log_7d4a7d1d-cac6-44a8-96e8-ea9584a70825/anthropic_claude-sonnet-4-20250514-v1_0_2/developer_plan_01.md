# Developer Plan 01

## Plan
Search for Girls Who Code organization's official reports, research publications, or data about the historical percentage of women in computer science. Focus on finding specific statistics that show a decline from 37% to 24% (a 13% change) and the timeframe over which this change occurred. Look for their official website, annual reports, or advocacy materials that document these historical trends.

## Description
This is the optimal first step because: (1) We need to locate Girls Who Code's specific data about women in computer science percentages and the timeframe for the 13% decline from 37%, (2) No previous research has been conducted, (3) Expected outcome is to find the organization's official documentation or reports containing the historical statistics about women computer scientists, (4) This directly targets the specific data needed to determine how many years it took for this demographic change to occur

## Episodic Examples
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

### Development Step 41: Official 2011 Bulgarian Census Tertiary Education Completion Numbers by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Bulgarian Ministry of Education analyzing regional gender disparities in tertiary education completions from the 2011 census to design targeted scholarships and close the STEM gender gap
- University admissions office automating extraction of past census tertiary education data by gender to forecast enrollment trends and adjust outreach for underrepresented male or female applicants
- International development agency (e.g., UNESCO) integrating 2011 Bulgarian tertiary education completion numbers by gender into cross-country education equity reports to monitor SDG progress
- Women’s empowerment NGO extracting official census figures on female higher education attainment to support grant proposals and advocacy in rural Bulgarian communities
- Demographic research firm processing NSI census tables on tertiary education by gender to produce regional talent-supply maps for corporate clients planning new office locations
- EdTech startup leveraging historical 2011 census data on male vs. female degree completion rates to tailor online course content and marketing strategies by demographic segment
- Data journalism team pulling tertiary education by gender statistics from the 2011 census to create interactive visualizations in an investigative report on post-transition education trends
- Real estate developer incorporating gender-segmented tertiary education data from the 2011 census into socio-economic profiles to identify high-demand student housing markets in Bulgarian university towns

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

workspace_dir = 'workspace'

print("=== PARSING DOWNLOADED NSI CENSUS FILES FOR TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Extract 2011 Bulgarian census tertiary education completion statistics by gender\n")

# First, let's inspect what files we have in the workspace
print("--- Inspecting Workspace Files ---")
if os.path.exists(workspace_dir):
    all_files = os.listdir(workspace_dir)
    print(f"Total files in workspace: {len(all_files)}")
    
    # Look for NSI census source files
    nsi_files = [f for f in all_files if f.startswith('nsi_census_source_') and f.endswith('.html')]
    print(f"\nNSI census HTML files found: {len(nsi_files)}")
    for f in nsi_files:
        filepath = os.path.join(workspace_dir, f)
        file_size = os.path.getsize(filepath)
        print(f"  - {f} ({file_size:,} bytes)")
else:
    print("Workspace directory not found!")
    exit(1)

if not nsi_files:
    print("No NSI census files found. Cannot proceed with analysis.")
    exit(1)

print(f"\n=== PHASE 1: ANALYZING NSI CENSUS FILES FOR EDUCATION DATA ===\n")

analysis_results = []

for filename in nsi_files:
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
    
    # Analyze tables for relevant content
    relevant_tables = []
    for i, table in enumerate(tables):
        table_text = table.get_text().lower()
        
        # Check if table contains education-related content
        has_education = any(term in table_text for term in ['education', 'tertiary', 'university', 'degree', 'higher'])
        has_gender = any(term in table_text for term in ['male', 'female', 'men', 'women', 'gender', 'sex'])
        has_census = '2011' in table_text or 'census' in table_text
        has_numbers = bool(re.search(r'\d+[,.]?\d*\s*%?', table_text))
        
        if has_education and (has_gender or has_census):
            # Extract table headers
            headers = []
            header_cells = table.find_all(['th', 'td'])[:15]  # First 15 cells as potential headers
            for cell in header_cells:
                cell_text = cell.get_text().strip()
                if cell_text and len(cell_text) < 100:  # Reasonable header length
                    headers.append(cell_text)
            
            relevant_tables.append({
                'table_index': i,
                'has_education': has_education,
                'has_gender': has_gender,
                'has_census': has_census,
                'has_numbers': has_numbers,
                'headers': headers[:8],  # First 8 headers
                'table_text_sample': table_text[:400]  # First 400 chars
            })
    
    if relevant_tables:
        print(f"\nRelevant tables found: {len(relevant_tables)}")
        for table_info in relevant_tables:
            print(f"  Table {table_info['table_index']}:")
            print(f"    Education: {table_info['has_education']}, Gender: {table_info['has_gender']}, Census: {table_info['has_census']}, Numbers: {table_info['has_numbers']}")
            print(f"    Headers: {table_info['headers']}")
            print(f"    Sample text: {table_info['table_text_sample'][:200]}...")
    
    # Look for downloadable files - FIX THE SCOPING ISSUE
    download_links = []
    all_links = soup.find_all('a', href=True)
    print(f"Total links found: {len(all_links)}")
    
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
        for i, link in enumerate(download_links[:8], 1):
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
            if clean_match not in education_content_matches:  # Avoid duplicates
                education_content_matches.append(clean_match)
    
    if education_content_matches:
        print(f"\nEducation content matches found: {len(education_content_matches)}")
        for i, match in enumerate(education_content_matches[:5], 1):
            print(f"  {i}. {match}...")
    
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
        
        if result['relevance_score'] > 100:
            print(f"   *** VERY HIGH PRIORITY - LIKELY CONTAINS TARGET DATA ***")
        elif result['relevance_score'] > 50:
            print(f"   ** HIGH PRIORITY - GOOD POTENTIAL FOR DATA **")
        elif result['relevance_score'] > 20:
            print(f"   * MODERATE PRIORITY *")
        
        # Show top download links for high-priority files
        if result['relevance_score'] > 50 and result['download_links']:
            print(f"   Top download links:")
            for j, link in enumerate(result['download_links'][:3], 1):
                print(f"     {j}. '{link['text']}'")
                print(f"        {link['full_url']}")

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

final_analysis_file = os.path.join(workspace_dir, 'nsi_census_tertiary_education_analysis.json')
with open(final_analysis_file, 'w', encoding='utf-8') as f:
    json.dump(final_analysis, f, indent=2, ensure_ascii=False)

print(f"\n=== ANALYSIS COMPLETE ===\n")
print(f"Comprehensive analysis saved to: {final_analysis_file}")

if analysis_results:
    top_result = analysis_results[0]
    print(f"\nTop priority file: {top_result['filename']} (Score: {top_result['relevance_score']})")
    print(f"Title: {top_result['page_title']}")
    print(f"Contains {len(top_result['relevant_tables'])} relevant tables and {len(top_result['download_links'])} download links")
    
    if top_result['education_content_matches']:
        print(f"\nMost promising education content from top file:")
        for i, match in enumerate(top_result['education_content_matches'][:3], 1):
            print(f"  {i}. {match}")
    
    print(f"\nReady to extract specific tertiary education completion data by gender from the highest-priority sources.")
else:
    print("\nNo analysis results generated. Check file availability and content.")
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

### Development Step 33: Locate 2011 Bulgarian Census Tertiary Education Completion by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Gender gap policy evaluation and regional disparity mapping for government education ministries
- Higher education enrollment forecasting and capacity planning for Bulgarian universities
- Labor market skills development analysis and targeted training program design for workforce agencies
- EdTech product market segmentation by gender and regional uptake trends for online learning platforms
- Sociological research on educational attainment and gender parity progression in academic studies
- Data journalism dashboard creation and interactive visualization of tertiary education gender statistics
- NGO program impact assessment and advocacy reporting on women’s access to higher education

```
import os
import requests
from bs4 import BeautifulSoup
import time
import json
import re

# Create workspace directory
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

print("=== SEARCHING FOR OFFICIAL 2011 BULGARIAN CENSUS TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Find exact counts/percentages of men and women who completed tertiary education")
print("Source target: Bulgarian National Statistical Institute (NSI) official census data\n")

# Set up headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
}

# Official NSI URLs to search for 2011 census education data
nsi_urls = [
    'https://www.nsi.bg/en/content/6704/population-census-2011',
    'https://www.nsi.bg/en/content/6710/population-education',
    'https://www.nsi.bg/en/content/census-2011',
    'https://www.nsi.bg/en',
    'https://www.nsi.bg/census2011/indexen.php',
    'https://www.nsi.bg/en/content/population-census-2011-main-results'
]

print("=== PHASE 1: ACCESSING OFFICIAL NSI CENSUS SOURCES ===")

successful_sources = []
failed_sources = []

for i, url in enumerate(nsi_urls, 1):
    print(f"\n{i}. Attempting to access: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"   Status code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✓ Successfully accessed")
            
            # Save the HTML content
            filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace('.', '_').replace(':', '_') + '.html'
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"   Content saved to: {filename}")
            print(f"   Content length: {len(response.text):,} characters")
            
            # Quick analysis for education/census content
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text().strip() if title else 'No title'
            
            # Check for relevant content indicators
            content_text = soup.get_text().lower()
            
            # Key indicators for our target data
            indicators = {
                'census_2011': content_text.count('2011'),
                'education': content_text.count('education'),
                'tertiary': content_text.count('tertiary'),
                'higher_education': content_text.count('higher education'),
                'university': content_text.count('university'),
                'gender': content_text.count('gender'),
                'male': content_text.count('male'),
                'female': content_text.count('female'),
                'men': content_text.count(' men '),
                'women': content_text.count('women')
            }
            
            # Count tables (potential data containers)
            tables = soup.find_all('table')
            table_count = len(tables)
            
            # Calculate relevance score
            relevance_score = sum(indicators.values()) + (table_count * 2)
            
            source_info = {
                'url': url,
                'filename': filename,
                'title': title_text,
                'content_length': len(response.text),
                'table_count': table_count,
                'indicators': indicators,
                'relevance_score': relevance_score,
                'status': 'success'
            }
            
            successful_sources.append(source_info)
            
            print(f"   Title: {title_text}")
            print(f"   Tables found: {table_count}")
            print(f"   Relevance score: {relevance_score}")
            
            # Show key indicator counts
            relevant_indicators = {k: v for k, v in indicators.items() if v > 0}
            if relevant_indicators:
                print(f"   Key terms found: {relevant_indicators}")
            
        else:
            print(f"   ✗ Failed - Status: {response.status_code}")
            failed_sources.append({'url': url, 'status': response.status_code, 'error': 'HTTP error'})
            
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {str(e)}")
        failed_sources.append({'url': url, 'error': str(e), 'status': 'request_failed'})
    
    # Be respectful to the server
    time.sleep(2)

print(f"\n=== PHASE 1 RESULTS ===")
print(f"Successfully accessed: {len(successful_sources)} sources")
print(f"Failed to access: {len(failed_sources)} sources")

# Sort sources by relevance score
if successful_sources:
    successful_sources.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"\n=== TOP PRIORITY SOURCES (by relevance score) ===")
    for i, source in enumerate(successful_sources[:3], 1):
        print(f"\n{i}. {source['url']}")
        print(f"   Title: {source['title']}")
        print(f"   Relevance score: {source['relevance_score']}")
        print(f"   Tables: {source['table_count']}")
        print(f"   Key indicators: {source['indicators']}")
        
        if source['relevance_score'] > 10:
            print(f"   *** HIGH PRIORITY - Contains multiple education/census indicators ***")

# Save search results summary
search_summary = {
    'search_objective': '2011 Bulgarian Census - Tertiary Education Completion by Gender',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'urls_attempted': len(nsi_urls),
    'successful_sources': len(successful_sources),
    'failed_sources': len(failed_sources),
    'source_details': successful_sources,
    'failed_attempts': failed_sources
}

summary_file = os.path.join(workspace_dir, 'nsi_census_search_results.json')
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(search_summary, f, indent=2, ensure_ascii=False)

print(f"\nSearch results saved to: {summary_file}")

if successful_sources:
    print(f"\n=== NEXT PHASE ===")
    print(f"Will analyze the {len(successful_sources)} successfully downloaded NSI sources")
    print(f"Priority focus on sources with highest relevance scores")
    print(f"Looking for census tables with tertiary education data broken down by gender")
else:
    print(f"\n=== NO SOURCES ACCESSED ===")
    print(f"All NSI URLs failed to load. May need to try alternative search methods.")
    print(f"Consider searching for Bulgarian census publications or statistical yearbooks.")

print(f"\n=== FILES CREATED IN WORKSPACE ===")
for filename in os.listdir(workspace_dir):
    filepath = os.path.join(workspace_dir, filename)
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        print(f"  {filename} ({size:,} bytes)")
```

## Created Time
2025-08-13 18:43:51
