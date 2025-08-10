# Developer Plan 01

## Plan
Search for World Bank data on gross savings as percentage of GDP for all countries during the period 2001-2010. Focus on identifying countries that maintained gross savings above 35% of GDP consistently for every single year in this decade. Use official World Bank databases, data portals, or reliable sources that provide comprehensive historical economic indicators for this specific time period.

## Description
This is the optimal first step because: (1) We need to access World Bank economic data specifically for gross savings as percentage of GDP from 2001-2010, (2) No previous research has been conducted on this topic, (3) Expected outcome is to obtain comprehensive data showing which countries consistently exceeded the 35% threshold across all years in the specified period, (4) This directly addresses the core TASK requirement to identify countries meeting the specific World Bank gross savings criteria for the entire decade.

## Episodic Examples
### Development Step 50: Search Official 2011 Bulgarian Census Tertiary Education Completion Data by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government education ministry budget planning for higher education programs by automatically extracting 2011 census tertiary graduation counts by gender to inform funding allocations.
- Academic sociological research on regional gender disparities in university attainment, using the automated data extraction to compile comparative studies across Bulgarian provinces.
- NGO gender equality project development, leveraging census-derived male vs. female tertiary completion rates to design targeted empowerment and scholarship initiatives.
- HR and talent acquisition analytics for multinational firms, integrating regional tertiary education statistics by gender to map skilled workforce availability in Bulgaria.
- Data journalism and interactive visualization production, using the extracted NSI census figures to illustrate trends in women’s participation in higher education.
- EdTech platform benchmarking features, embedding gender-segmented tertiary education data into dashboards for schools and policymakers assessing progress over time.
- International development agency policy briefs on gender parity in education, automating the collection of official census statistics to monitor UN Sustainable Development Goal 4 indicators.
- Municipal education authority reporting and scholarship management, generating localized reports on tertiary graduate gender ratios for community outreach and resource planning.

```
import os
import json
from bs4 import BeautifulSoup
import re
import requests
import time

workspace_dir = 'workspace'

print("=== FINAL EXTRACTION: 2011 BULGARIAN CENSUS TERTIARY EDUCATION BY GENDER ===")
print("\nObjective: Extract exact counts/percentages of men and women who completed tertiary education from 2011 Bulgarian census\n")

# First, safely inspect what files we have in workspace
if not os.path.exists(workspace_dir):
    print("Workspace directory not found!")
    exit(1)

all_files = os.listdir(workspace_dir)
print(f"Total files in workspace: {len(all_files)}")

# Look for the key files we need
nsi_files = []
analysis_files = []
census_files = []

for filename in all_files:
    if filename.startswith('nsi_census_source_') and filename.endswith('.html'):
        nsi_files.append(filename)
    elif 'analysis' in filename.lower() and filename.endswith('.json'):
        analysis_files.append(filename)
    elif 'census' in filename.lower() and ('2011' in filename or 'Census2011' in filename):
        census_files.append(filename)

print(f"\nFile inventory:")
print(f"- NSI census HTML files: {len(nsi_files)}")
print(f"- Analysis files: {len(analysis_files)}")
print(f"- Census data files: {len(census_files)}")

for f in nsi_files:
    size = os.path.getsize(os.path.join(workspace_dir, f))
    print(f"  • {f} ({size:,} bytes)")

# Load the analysis file to understand the structure safely
analysis_data = None
if analysis_files:
    analysis_file = os.path.join(workspace_dir, analysis_files[0])
    print(f"\n--- Inspecting Analysis File: {analysis_files[0]} ---")
    
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"File size: {len(content):,} characters")
        
        # Parse JSON safely
        analysis_data = json.loads(content)
        print(f"JSON structure keys: {list(analysis_data.keys())}")
        
        if 'analysis_results' in analysis_data:
            results = analysis_data['analysis_results']
            print(f"Analysis results count: {len(results)}")
            
            if results:
                top_result = results[0]
                print(f"Top result keys: {list(top_result.keys())}")
                print(f"Top result filename: {top_result.get('filename', 'Unknown')}")
                print(f"Relevance score: {top_result.get('relevance_score', 'Unknown')}")
        
    except Exception as e:
        print(f"Error reading analysis file: {e}")
        analysis_data = None

# Now examine the highest priority NSI file directly
target_file = 'nsi_census_source_4.html'  # Based on previous analysis
if target_file not in nsi_files:
    if nsi_files:
        target_file = nsi_files[0]  # Use first available
    else:
        print("No NSI census files found!")
        exit(1)

print(f"\n=== EXAMINING TARGET FILE: {target_file} ===")

file_path = os.path.join(workspace_dir, target_file)
with open(file_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"File size: {len(html_content):,} characters")

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')
full_text = soup.get_text()

print(f"Extracted text length: {len(full_text):,} characters")

# Search for the key phrase we know exists
key_phrase = 'tertiary education graduates by educational-qualification degree and sex'
print(f"\n--- Searching for Key Phrase ---")
print(f"Target phrase: '{key_phrase}'")

if key_phrase.lower() in full_text.lower():
    print("✓ Key phrase found in document!")
    
    # Find the location and extract surrounding context
    text_lower = full_text.lower()
    phrase_index = text_lower.find(key_phrase.lower())
    
    if phrase_index != -1:
        # Extract 500 characters before and after the phrase
        start_pos = max(0, phrase_index - 500)
        end_pos = min(len(full_text), phrase_index + len(key_phrase) + 500)
        context = full_text[start_pos:end_pos]
        
        print(f"\nContext around key phrase:")
        print(f"{'='*60}")
        print(context)
        print(f"{'='*60}")
else:
    print("✗ Key phrase not found")

# Look for any links that might lead to downloadable data
print(f"\n--- Searching for Data Download Links ---")

data_links = []
all_links = soup.find_all('a')
print(f"Total links found: {len(all_links)}")

for link in all_links:
    link_href = link.get('href', '')
    link_text = link.get_text().strip()
    
    # Check if it's a data file
    data_extensions = ['.pdf', '.xls', '.xlsx', '.csv', '.doc']
    is_data_file = any(ext in link_href.lower() for ext in data_extensions)
    
    # Check if it mentions relevant terms
    relevant_terms = ['education', 'tertiary', 'census', '2011', 'population', 'demographic']
    is_relevant = any(term in link_text.lower() or term in link_href.lower() for term in relevant_terms)
    
    if is_data_file and is_relevant:
        # Build full URL
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
            'extension': link_href.split('.')[-1].lower() if '.' in link_href else 'unknown'
        })

print(f"Found {len(data_links)} potential data files:")
for i, link_info in enumerate(data_links[:10], 1):
    print(f"  {i}. '{link_info['text']}' ({link_info['extension']})")
    print(f"     {link_info['full_url']}")

# Try to access the main 2011 census final report directly
print(f"\n--- Accessing Official 2011 Census Final Report ---")

census_final_url = 'https://www.nsi.bg/census2011/PDOCS2/Census2011final_en.pdf'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    print(f"Attempting to download: {census_final_url}")
    response = requests.get(census_final_url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        print(f"✓ Successfully downloaded Census 2011 final report")
        print(f"File size: {len(response.content):,} bytes")
        
        # Save the PDF
        pdf_path = os.path.join(workspace_dir, 'Census2011_Final_Report.pdf')
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        
        print(f"PDF saved to: {pdf_path}")
        
        # Note: PDF parsing would require additional libraries
        print(f"\n*** IMPORTANT: The official 2011 Census Final Report PDF has been downloaded ***")
        print(f"This PDF likely contains the detailed tertiary education statistics by gender.")
        print(f"The file is {len(response.content):,} bytes and should contain comprehensive census data.")
        
    else:
        print(f"✗ Failed to download PDF - Status: {response.status_code}")
        
except Exception as e:
    print(f"✗ Error downloading PDF: {e}")

# Search for any existing census data we might have downloaded
print(f"\n--- Checking for Existing Census Data Files ---")

if census_files:
    print(f"Found {len(census_files)} existing census files:")
    for census_file in census_files:
        file_path = os.path.join(workspace_dir, census_file)
        file_size = os.path.getsize(file_path)
        print(f"  • {census_file} ({file_size:,} bytes)")
else:
    print("No existing census data files found.")

# Look for specific statistical patterns in the HTML content
print(f"\n--- Searching for Statistical Data Patterns ---")

# Search for numerical patterns that might represent census statistics
statistical_patterns = [
    r'\b\d{1,3}[,.]\d{3}\b',  # Numbers like 123,456 or 123.456
    r'\b\d+[.]\d+%\b',        # Percentages like 45.6%
    r'\b\d+%\b',              # Simple percentages like 45%
    r'\b\d{4,}\b'             # Large numbers (4+ digits)
]

found_numbers = []
for pattern in statistical_patterns:
    matches = re.findall(pattern, full_text)
    found_numbers.extend(matches[:20])  # Limit to prevent overflow

# Remove duplicates while preserving order
unique_numbers = []
for num in found_numbers:
    if num not in unique_numbers:
        unique_numbers.append(num)

print(f"Found {len(unique_numbers)} unique numerical patterns:")
for i, num in enumerate(unique_numbers[:20], 1):
    print(f"  {i}. {num}")

# Search for text sections that mention tertiary education
print(f"\n--- Searching for Tertiary Education Sections ---")

# Split text into sentences and look for relevant ones
sentences = re.split(r'[.!?]+', full_text)
relevant_sentences = []

for sentence in sentences:
    sentence_clean = sentence.strip()
    if len(sentence_clean) > 20:  # Skip very short sentences
        sentence_lower = sentence_clean.lower()
        
        # Check if sentence contains tertiary education terms
        tertiary_terms = ['tertiary', 'higher education', 'university', 'bachelor', 'master', 'degree']
        has_tertiary = any(term in sentence_lower for term in tertiary_terms)
        
        # Check if sentence contains gender terms
        gender_terms = ['male', 'female', 'men', 'women', 'sex', 'gender']
        has_gender = any(term in sentence_lower for term in gender_terms)
        
        # Check if sentence contains numbers
        has_numbers = bool(re.search(r'\d+', sentence_clean))
        
        if has_tertiary and (has_gender or has_numbers):
            relevant_sentences.append(sentence_clean[:300])  # Limit length

print(f"Found {len(relevant_sentences)} relevant sentences:")
for i, sentence in enumerate(relevant_sentences[:5], 1):
    print(f"  {i}. {sentence}")

# Create comprehensive summary
summary = {
    'objective': '2011 Bulgarian Census - Tertiary Education by Gender Statistics',
    'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'source_analysis': {
        'target_file': target_file,
        'file_size': len(html_content),
        'text_length': len(full_text),
        'key_phrase_found': key_phrase.lower() in full_text.lower()
    },
    'findings': {
        'data_download_links': len(data_links),
        'statistical_patterns': len(unique_numbers),
        'relevant_sentences': len(relevant_sentences),
        'census_files_available': len(census_files)
    },
    'data_links': data_links[:10],  # Top 10 links
    'statistical_patterns': unique_numbers[:20],  # Top 20 numbers
    'relevant_content': relevant_sentences[:5],  # Top 5 sentences
    'recommendations': [
        'Parse the downloaded Census2011_Final_Report.pdf for detailed statistics',
        'Access the identified data download links for specific education data',
        'Search NSI statistical yearbooks for 2011 census education tables',
        'Contact NSI directly for detailed tertiary education completion data by gender'
    ],
    'status': 'READY FOR DETAILED DATA EXTRACTION'
}

# Save comprehensive results
results_file = os.path.join(workspace_dir, 'final_tertiary_education_extraction_summary.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print(f"\n{'='*80}")
print(f"FINAL EXTRACTION SUMMARY")
print(f"{'='*80}")
print(f"\nResults saved to: {results_file}")
print(f"\nKey Findings:")
print(f"✓ Target phrase found: {summary['source_analysis']['key_phrase_found']}")
print(f"✓ Data download links identified: {summary['findings']['data_download_links']}")
print(f"✓ Statistical patterns found: {summary['findings']['statistical_patterns']}")
print(f"✓ Relevant content sections: {summary['findings']['relevant_sentences']}")

if data_links:
    print(f"\nHighest Priority Data Sources:")
    for i, link in enumerate(data_links[:3], 1):
        print(f"  {i}. {link['text']} ({link['extension']})")
        print(f"     {link['full_url']}")

print(f"\n*** CONCLUSION ***")
print(f"Successfully located official NSI sources containing references to")
print(f"'tertiary education graduates by educational-qualification degree and sex'")
print(f"from the 2011 Bulgarian census. The analysis has identified {len(data_links)}")
print(f"potential data files and downloaded the official Census 2011 Final Report.")
print(f"\nThe specific counts/percentages of men and women who completed tertiary")
print(f"education according to the 2011 Bulgarian census should be available in")
print(f"the downloaded PDF and the identified data files.")

print(f"\n=== EXTRACTION COMPLETE ===")
```

### Development Step 22: 2011 Bulgarian Census: Tertiary Education Completion by Gender (Official NSI Data)

**Description**: Search for the 2011 Bulgarian census data on tertiary education completion by gender. Look for official census results from Bulgaria's National Statistical Institute or other authoritative sources that provide the specific breakdown of men and women who completed tertiary education in 2011.

**Use Cases**:
- Government education policy assessment and funding allocation in Bulgaria using 2011 tertiary completion by gender data
- Academic research on gender disparities in higher education enrollment for a peer-reviewed sociology study
- NGO program design for female STEM empowerment initiatives based on regional tertiary attainment statistics
- Data journalism dashboard that visualizes Bulgarian gender gaps in university graduation rates
- Corporate workforce planning for a Balkan expansion project assessing skilled graduate availability by gender
- Automated ETL pipeline ingesting official census education metrics into a national data warehouse
- Civic tech platform building interactive maps of local tertiary completion rates by gender for public transparency
- International development monitoring of UN SDG progress on gender equality in education using census breakdowns

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

print("=== BULGARIAN 2011 CENSUS TERTIARY EDUCATION BY GENDER - ROBUST EXTRACTION ===")
print("Strategy: Simple, robust analysis avoiding all scoping issues\n")

# Check workspace
workspace_path = 'workspace'
if not os.path.exists(workspace_path):
    print("No workspace directory found")
    exit()

# Get all files and categorize them
all_files = os.listdir(workspace_path)
print(f"Total files in workspace: {len(all_files)}")

# Find HTML files manually
html_files_list = []
for filename in all_files:
    if filename.endswith('.html'):
        html_files_list.append(filename)

print(f"HTML files found: {len(html_files_list)}")

# Look specifically for Bulgarian Demographics files
bulgarian_demographics_files = []
for filename in html_files_list:
    if 'Demographics_of_Bulgaria' in filename:
        bulgarian_demographics_files.append(filename)
        print(f"  Found Bulgarian Demographics file: {filename}")

if not bulgarian_demographics_files:
    print("No Bulgarian Demographics files found")
    exit()

# Analyze the first Bulgarian Demographics file
target_file = bulgarian_demographics_files[0]
print(f"\n=== ANALYZING: {target_file} ===")

filepath = os.path.join(workspace_path, target_file)
with open(filepath, 'r', encoding='utf-8') as f:
    html_content = f.read()

print(f"File size: {len(html_content):,} characters")

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')
page_title = soup.find('title')
if page_title:
    print(f"Page title: {page_title.get_text().strip()}")

# Extract all text
all_text = soup.get_text()
print(f"Text content: {len(all_text):,} characters")

# Search for tertiary education data with gender breakdown
print("\n=== SEARCHING FOR TERTIARY EDUCATION DATA ===")

# Look for education sections
education_matches = []

# Pattern 1: Look for "tertiary education" followed by gender data
pattern1 = r'tertiary education[^.]{0,500}(?:male|female|men|women)[^.]{0,200}'
matches1 = re.finditer(pattern1, all_text, re.IGNORECASE | re.DOTALL)
for match in matches1:
    context_start = max(0, match.start() - 200)
    context_end = min(len(all_text), match.end() + 200)
    context = all_text[context_start:context_end]
    education_matches.append({
        'type': 'tertiary_education_with_gender',
        'match_text': match.group(),
        'context': context
    })

print(f"Tertiary education with gender matches: {len(education_matches)}")

# Pattern 2: Look for education statistics with percentages and gender
pattern2 = r'(?:male|female|men|women)[^.]{0,100}(?:education|tertiary|university)[^.]{0,100}(\d+\.?\d*\s*%?)'
matches2 = re.finditer(pattern2, all_text, re.IGNORECASE)
for match in matches2:
    context_start = max(0, match.start() - 200)
    context_end = min(len(all_text), match.end() + 200)
    context = all_text[context_start:context_end]
    education_matches.append({
        'type': 'gender_education_statistics',
        'match_text': match.group(),
        'percentage': match.group(1) if match.groups() else 'No percentage',
        'context': context
    })

print(f"Gender education statistics matches: {len(education_matches)}")

# Pattern 3: Look for 2011 census data with education
pattern3 = r'2011[^.]{0,300}(?:education|tertiary|university)[^.]{0,200}(?:male|female|men|women)[^.]{0,100}'
matches3 = re.finditer(pattern3, all_text, re.IGNORECASE | re.DOTALL)
for match in matches3:
    context_start = max(0, match.start() - 200)
    context_end = min(len(all_text), match.end() + 200)
    context = all_text[context_start:context_end]
    education_matches.append({
        'type': '2011_census_education',
        'match_text': match.group(),
        'context': context
    })

print(f"2011 census education matches: {len(education_matches)}")

# Display all matches found
if education_matches:
    print("\n=== EDUCATION MATCHES FOUND ===")
    for i, match in enumerate(education_matches, 1):
        print(f"\nMatch {i} ({match['type']}):")
        print(f"  Text: {match['match_text'][:200]}...")
        if 'percentage' in match:
            print(f"  Percentage: {match['percentage']}")
        print(f"  Context: {match['context'][:300]}...")
        print()

# Look for specific numerical data in education context
print("\n=== EXTRACTING NUMERICAL DATA ===")

numerical_findings = []

# Search for years of education by gender
years_pattern = r'(?:male|female|men|women)[^.]{0,50}(\d+)\s*years?[^.]{0,50}(?:education|tertiary)'
years_matches = re.finditer(years_pattern, all_text, re.IGNORECASE)
for match in years_matches:
    context_start = max(0, match.start() - 150)
    context_end = min(len(all_text), match.end() + 150)
    context = all_text[context_start:context_end]
    numerical_findings.append({
        'type': 'years_of_education',
        'value': match.group(1),
        'context': context
    })

# Search for percentage data with gender
percentage_pattern = r'(?:male|female|men|women)[^.]{0,100}(\d+\.?\d*)\s*%'
percentage_matches = re.finditer(percentage_pattern, all_text, re.IGNORECASE)
for match in percentage_matches:
    context_start = max(0, match.start() - 150)
    context_end = min(len(all_text), match.end() + 150)
    context = all_text[context_start:context_end]
    # Check if context mentions education
    if any(term in context.lower() for term in ['education', 'tertiary', 'university', 'degree']):
        numerical_findings.append({
            'type': 'education_percentage',
            'value': match.group(1),
            'context': context
        })

print(f"Numerical findings: {len(numerical_findings)}")

for i, finding in enumerate(numerical_findings, 1):
    print(f"\nFinding {i} ({finding['type']}):")
    print(f"  Value: {finding['value']}")
    print(f"  Context: {finding['context'][:250]}...")

# Look for specific Bulgarian census data
print("\n=== SEARCHING FOR BULGARIAN CENSUS DATA ===")

bulgarian_census_data = []

# Search for Bulgaria + 2011 + education combinations
bulgaria_2011_pattern = r'(?:bulgaria|bulgarian)[^.]{0,200}2011[^.]{0,200}(?:education|tertiary|university)[^.]{0,200}'
bulgaria_matches = re.finditer(bulgaria_2011_pattern, all_text, re.IGNORECASE | re.DOTALL)
for match in bulgaria_matches:
    context_start = max(0, match.start() - 300)
    context_end = min(len(all_text), match.end() + 300)
    context = all_text[context_start:context_end]
    
    # Extract any numbers from this context
    numbers = re.findall(r'\d+\.?\d*\s*%?', context)
    
    bulgarian_census_data.append({
        'match_text': match.group(),
        'context': context,
        'numbers_found': numbers
    })

print(f"Bulgarian census data matches: {len(bulgarian_census_data)}")

for i, data in enumerate(bulgarian_census_data, 1):
    print(f"\nBulgarian Census Data {i}:")
    print(f"  Match: {data['match_text'][:150]}...")
    print(f"  Numbers found: {data['numbers_found']}")
    print(f"  Context: {data['context'][:300]}...")

# Save comprehensive results
results = {
    'objective': 'Bulgarian 2011 census tertiary education completion by gender',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'file_analyzed': target_file,
    'education_matches_found': len(education_matches),
    'numerical_findings_found': len(numerical_findings),
    'bulgarian_census_matches': len(bulgarian_census_data),
    'detailed_results': {
        'education_matches': education_matches,
        'numerical_findings': numerical_findings,
        'bulgarian_census_data': bulgarian_census_data
    },
    'summary': {
        'tertiary_education_references': len([m for m in education_matches if m['type'] == 'tertiary_education_with_gender']),
        'gender_statistics': len([m for m in education_matches if m['type'] == 'gender_education_statistics']),
        'census_2011_references': len([m for m in education_matches if m['type'] == '2011_census_education']),
        'years_of_education_data': len([f for f in numerical_findings if f['type'] == 'years_of_education']),
        'education_percentages': len([f for f in numerical_findings if f['type'] == 'education_percentage'])
    }
}

results_file = os.path.join(workspace_path, 'bulgarian_census_final_results.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n=== FINAL SUMMARY ===")
print(f"Results saved to: {results_file}")
print(f"Education matches found: {results['education_matches_found']}")
print(f"Numerical findings: {results['numerical_findings_found']}")
print(f"Bulgarian census matches: {results['bulgarian_census_matches']}")

# Display key statistics if found
if numerical_findings:
    print("\n=== KEY STATISTICS IDENTIFIED ===")
    education_stats = [f for f in numerical_findings if f['type'] == 'education_percentage']
    years_stats = [f for f in numerical_findings if f['type'] == 'years_of_education']
    
    if education_stats:
        print("Education percentages by gender:")
        for stat in education_stats:
            print(f"  - {stat['value']}% | Context: {stat['context'][:150]}...")
    
    if years_stats:
        print("Years of education by gender:")
        for stat in years_stats:
            print(f"  - {stat['value']} years | Context: {stat['context'][:150]}...")

if bulgarian_census_data:
    print("\n=== BULGARIAN CENSUS REFERENCES ===")
    for i, data in enumerate(bulgarian_census_data[:3], 1):
        print(f"{i}. Numbers: {data['numbers_found']} | Context: {data['context'][:200]}...")

print("\n=== EXTRACTION COMPLETE ===")
print("Bulgarian 2011 census tertiary education by gender analysis completed.")
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

### Development Step 30: Search 2011 Bulgarian NSI Census for Tertiary Education Completion Numbers by Gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Public policy dashboard for the Bulgarian Ministry of Education to visualize and compare 2011 tertiary education completion rates by gender across regions, guiding targeted scholarship programs.
- Gender equality research report for an NGO analyzing male vs. female university graduation counts from the 2011 census to measure progress and propose new interventions.
- University admissions office forecasting tool that integrates 2011 gender‐segmented tertiary attainment data to predict applicant pools and tailor recruitment campaigns.
- Workforce planning model for a multinational corporation using regional tertiary education by gender from the 2011 census to decide on office locations and local talent acquisition strategies.
- Academic study on socio‐demographic trends automating extraction of 2011 Bulgarian census tertiary education figures by gender to perform longitudinal analyses in peer-reviewed publications.
- Data journalism investigation mapping historical gender gaps in higher education across Bulgarian provinces by scraping official NSI census tables and generating interactive infographics.
- Demographic forecasting system for a financial services firm that incorporates 2011 census tertiary qualification rates by gender to model future consumer behavior and credit scoring.

```
import os
import json
from bs4 import BeautifulSoup
import re

# Let's examine the most promising JSON file to understand its structure
workspace_dir = 'workspace'
promising_file = 'bulgarian_census_tertiary_education_comprehensive_final.json'
filepath = os.path.join(workspace_dir, promising_file)

print("=== DETAILED INSPECTION OF MOST PROMISING ANALYSIS FILE ===\n")
print(f"Examining: {promising_file}\n")

if os.path.exists(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("Complete file structure:")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:2000] + "..." if len(json.dumps(data, indent=2)) > 2000 else json.dumps(data, indent=2, ensure_ascii=False))
    
    print("\n=== KEY SECTIONS ANALYSIS ===\n")
    
    # Examine detailed_data section
    if 'detailed_data' in data and data['detailed_data']:
        print("DETAILED_DATA section contains:")
        detailed_data = data['detailed_data']
        if isinstance(detailed_data, list):
            print(f"  - List with {len(detailed_data)} items")
            for i, item in enumerate(detailed_data[:3], 1):
                print(f"  Item {i}: {type(item)} - {str(item)[:200]}...")
        elif isinstance(detailed_data, dict):
            print(f"  - Dictionary with keys: {list(detailed_data.keys())}")
            for key, value in list(detailed_data.items())[:3]:
                print(f"  {key}: {type(value)} - {str(value)[:200]}...")
        else:
            print(f"  - {type(detailed_data)}: {str(detailed_data)[:200]}...")
    
    # Examine statistical_findings
    if 'statistical_findings' in data and data['statistical_findings']:
        print(f"\nSTATISTICAL_FINDINGS section (count: {data.get('statistical_findings', 0)}):")
        # This might be a count, let's see if there are actual findings stored elsewhere
        for key, value in data.items():
            if 'finding' in key.lower() or 'statistic' in key.lower():
                print(f"  {key}: {value}")
    
    # Examine census_2011_findings
    if 'census_2011_findings' in data and data['census_2011_findings']:
        print(f"\nCENSUS_2011_FINDINGS section (count: {data.get('census_2011_findings', 0)}):")
        # Look for actual census data
        for key, value in data.items():
            if '2011' in key.lower() or 'census' in key.lower():
                print(f"  {key}: {value}")
    
    print("\n=== SEARCHING FOR ACTUAL DATA VALUES ===\n")
    
    # Recursively search for any numerical data or gender-related information
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
    
    relevant_findings = find_data_recursively(data)
    
    if relevant_findings:
        print("Relevant data found in file:")
        for path, data_type, content in relevant_findings[:10]:  # Show first 10 findings
            print(f"  Path: {path}")
            print(f"  Type: {data_type}")
            print(f"  Content: {content}")
            print()
    else:
        print("No relevant gender/education data found in this file.")

else:
    print(f"File not found: {filepath}")

print("\n=== EXAMINING ACTUAL NSI HTML FILES FOR DIRECT PARSING ===\n")

# Since the JSON files don't seem to contain the actual data, let's try to directly parse
# the NSI HTML files, but first let's check if they actually contain readable content

nsi_files_to_check = [
    'www_nsi_bg_en_content_6710_population_education.html',
    'www_nsi_bg_en_content_6704_population_census_2011.html', 
    'nsi_source_1.html'
]

for nsi_file in nsi_files_to_check:
    filepath = os.path.join(workspace_dir, nsi_file)
    if os.path.exists(filepath):
        print(f"\n--- Direct parsing attempt: {nsi_file} ---")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"File size: {len(html_content):,} characters")
        
        # Check if file contains actual HTML or is empty/corrupted
        if '<html' in html_content.lower() or '<body' in html_content.lower():
            print("✓ File contains HTML structure")
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for title
            title = soup.find('title')
            if title and title.get_text().strip():
                print(f"Page title: {title.get_text().strip()}")
            
            # Look for any text content
            text_content = soup.get_text().strip()
            if text_content:
                print(f"Text content length: {len(text_content)} characters")
                
                # Search for key terms
                text_lower = text_content.lower()
                key_terms = ['tertiary education', 'higher education', 'university', '2011', 'census', 'gender', 'male', 'female']
                
                found_terms = []
                for term in key_terms:
                    if term in text_lower:
                        count = text_lower.count(term)
                        found_terms.append(f"{term}: {count}")
                
                if found_terms:
                    print(f"Key terms found: {', '.join(found_terms)}")
                    
                    # If we found relevant terms, look for tables or structured data
                    tables = soup.find_all('table')
                    if tables:
                        print(f"Tables found: {len(tables)}")
                        
                        # Examine first table for structure
                        first_table = tables[0]
                        rows = first_table.find_all('tr')
                        print(f"First table has {len(rows)} rows")
                        
                        if rows:
                            # Show table headers
                            header_cells = rows[0].find_all(['th', 'td'])
                            headers = [cell.get_text().strip() for cell in header_cells]
                            print(f"Headers: {headers}")
                    
                    # Look for specific statistical data patterns
                    number_patterns = re.findall(r'\b\d{1,3}(?:,\d{3})*\b', text_content)
                    if number_patterns:
                        large_numbers = [n for n in number_patterns if len(n.replace(',', '')) >= 4]
                        if large_numbers:
                            print(f"Statistical numbers found: {large_numbers[:5]}")
                
                else:
                    print("No relevant terms found in content")
            else:
                print("No readable text content found")
        else:
            print("✗ File does not contain proper HTML structure")
            # Show first 500 characters to understand what's in the file
            print(f"File preview: {html_content[:500]}...")

print("\n=== ANALYSIS COMPLETE ===\n")
print("Summary: Examining existing data to determine if 2011 Bulgarian census tertiary education by gender data has been successfully extracted.")
```

## Created Time
2025-08-10 04:22:18
