# Developer Plan 02

## Plan
Calculate the exact timeframe for the 13% decline in women computer scientists based on the Girls Who Code data. The research found that in 1995, 37% of computer scientists were women, and by 2017 it had declined to 24% (a 13 percentage point decrease). Determine the number of years between 1995 and 2017 to provide the final answer.

## Description
This calculation step is needed because: (1) The developer successfully found the key Girls Who Code statistics showing 37% women in computer science in 1995 declining to 24% by 2017, which represents exactly the 13% change specified in the TASK, (2) We have the start year (1995) and end year (2017) from the official Girls Who Code data, (3) Expected outcome is a simple calculation: 2017 - 1995 = 22 years, (4) This provides the definitive answer to how long it took for the percentage to change by 13% from the starting point of 37%

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

## Created Time
2025-08-13 18:47:12
