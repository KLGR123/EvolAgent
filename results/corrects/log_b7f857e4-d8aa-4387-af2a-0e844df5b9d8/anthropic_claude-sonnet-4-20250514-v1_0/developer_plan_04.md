# Developer Plan 04

## Plan
Download the C++ source code from the URL https://web.archive.org/web/20230609112831/https://rosettacode.org/wiki/sorting_algorithms/Quicksort#C++ and save it to workspace/quicksort.cpp for compilation and execution.

## Description
This is the necessary next step because: (1) We have successfully generated the URL containing C++ source code from the Python script execution, (2) We need to obtain the actual C++ code before we can compile and run it against the integer array [35, 12, 8, 99, 21, 5], (3) Expected outcome is to have the Quicksort C++ source code downloaded and ready for compilation, (4) This progresses toward the final goal of running the C++ code and calculating the sum of the third and fifth integers in the sorted array

## Episodic Examples
### Development Step 7: Search 2011 Bulgarian Census Data on Tertiary Education Completion by Gender

**Description**: Search for the 2011 Bulgarian census data on tertiary education completion by gender. Look for official census results from Bulgaria's National Statistical Institute or other authoritative sources that provide the specific breakdown of men and women who completed tertiary education in 2011.

**Use Cases**:
- A policy analyst at Bulgaria’s Ministry of Education automates extraction of 2011 tertiary completion rates by gender from archived NSI HTML dumps to inform a gender equity report.
- A university demographer uses the script to parse archived census web pages and integrate the 2011 tertiary education gender breakdown into a longitudinal study on educational attainment trends.
- An NGO designing STEM outreach programs in underprivileged Bulgarian regions extracts male and female university completion percentages from 2011 census HTML files to target communities with low female enrollment.
- A market intelligence team at an e-learning startup crawls and parses historical Bulgarian census education data for gender‐specific tertiary completion to tailor course offerings and marketing strategies.
- A data journalist investigating gender disparities in Eastern Europe automates scraping of official Bulgarian census tables to quickly gather tertiary education statistics by gender for a data-driven article.
- A data scientist at an international organization uses the Python scraper to collect and standardize gender-disaggregated tertiary education rates from Bulgarian census HTML archives for cross-country comparative analyses.
- An urban planner compiles educational attainment profiles by gender for Bulgarian municipalities by extracting and mapping 2011 census tertiary completion data to support regional development proposals.
- A human resources consultancy benchmarks workforce education levels by downloading and parsing national census HTML data to compare male and female tertiary degree completion across Bulgarian industries.

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

# First, let's inspect what files are actually in the workspace
print("=== ANALYZING SAVED BULGARIAN CENSUS DATA FILES ===")
print("Objective: Extract tertiary education completion by gender from 2011 Bulgarian census")
print("Strategy: Analyze all saved HTML files with proper variable handling\n")

if os.path.exists('workspace'):
    files = os.listdir('workspace')
    html_files = [f for f in files if f.endswith('.html')]
    print(f"HTML files available for analysis: {len(html_files)}")
    
    # Show the most promising files based on names
    priority_files = []
    for html_file in html_files:
        if any(term in html_file.lower() for term in ['education', 'demographics', 'census', 'nsi', 'eurostat']):
            priority_files.append(html_file)
    
    print(f"Priority files (education/census related): {len(priority_files)}")
    for pf in priority_files[:10]:  # Show top 10
        print(f"  {pf}")
else:
    print("No workspace directory found")
    exit()

print("\n=== DETAILED ANALYSIS OF SAVED CONTENT ===\n")

analysis_results = []
specific_findings = []

for i, html_file in enumerate(html_files, 1):
    print(f"Analyzing {i}/{len(html_files)}: {html_file}")
    
    filepath = f'workspace/{html_file}'
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get page title
        title_element = soup.find('title')
        page_title = title_element.get_text().strip() if title_element else 'No title found'
        
        # Get all text content and create lowercase version for analysis
        full_text = soup.get_text()
        text_for_analysis = full_text.lower()  # Create lowercase version immediately
        
        print(f"  Title: {page_title}")
        print(f"  Content length: {len(full_text)} characters")
        
        # Skip very small files (likely error pages)
        if len(full_text) < 1000:
            print(f"  Skipping - content too small (likely error page)")
            print()
            continue
        
        # Check relevance for Bulgarian census and education
        has_bulgaria = 'bulgaria' in text_for_analysis or 'bulgarian' in text_for_analysis
        has_2011 = '2011' in text_for_analysis
        has_census = 'census' in text_for_analysis
        has_tertiary = any(term in text_for_analysis for term in ['tertiary', 'higher education', 'university degree', 'tertiary education'])
        has_gender = any(term in text_for_analysis for term in ['men', 'women', 'male', 'female', 'gender', 'sex'])
        has_education = 'education' in text_for_analysis
        
        relevance_score = sum([has_bulgaria, has_2011, has_census, has_tertiary, has_gender, has_education])
        
        print(f"  Bulgaria: {has_bulgaria} | 2011: {has_2011} | Census: {has_census}")
        print(f"  Tertiary ed: {has_tertiary} | Gender: {has_gender} | Education: {has_education}")
        print(f"  Relevance score: {relevance_score}/6")
        
        if relevance_score >= 3:  # Analyze high-relevance sources
            print(f"  *** HIGH RELEVANCE - EXTRACTING DATA ***")
            
            # Search for specific education statistics with gender breakdown
            education_sentences = []
            sentences = full_text.split('.')
            
            for sentence in sentences:
                sentence_clean = sentence.strip()
                sentence_lower = sentence_clean.lower()
                
                if len(sentence_clean) > 30:  # Skip very short sentences
                    # Look for sentences with Bulgaria + education + numbers/percentages + gender
                    has_bulgaria_ref = 'bulgaria' in sentence_lower
                    has_education_ref = any(term in sentence_lower for term in 
                                          ['tertiary', 'education', 'university', 'higher', 'degree', 'graduate', 'completed'])
                    has_numbers = bool(re.search(r'\d+[.,]?\d*\s*%?', sentence_lower))
                    has_gender_ref = any(term in sentence_lower for term in ['men', 'women', 'male', 'female'])
                    has_year_ref = '2011' in sentence_lower
                    
                    if has_bulgaria_ref and has_education_ref and has_numbers and (has_gender_ref or has_year_ref):
                        education_sentences.append(sentence_clean)
            
            print(f"  Education sentences with data: {len(education_sentences)}")
            
            # Look for tables with statistical data
            tables = soup.find_all('table')
            relevant_tables = []
            
            for table_idx, table in enumerate(tables):
                table_text = table.get_text().lower()
                
                # Check if table contains education and gender data
                if (any(term in table_text for term in ['education', 'tertiary', 'university', 'degree']) and
                    any(term in table_text for term in ['men', 'women', 'male', 'female', 'gender'])):
                    
                    # Extract table headers
                    headers = [th.get_text().strip() for th in table.find_all('th')]
                    
                    # Get all rows of data
                    rows = table.find_all('tr')
                    table_data = []
                    
                    for row in rows:
                        cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
                        if cells and any(cell for cell in cells if cell.strip()):  # Skip empty rows
                            table_data.append(cells)
                    
                    relevant_tables.append({
                        'index': table_idx,
                        'headers': headers,
                        'data': table_data[:10],  # First 10 rows
                        'total_rows': len(rows)
                    })
            
            print(f"  Relevant tables found: {len(relevant_tables)}")
            
            # Search for specific numerical patterns related to tertiary education by gender
            education_stats = []
            
            # Enhanced patterns to capture tertiary education statistics by gender
            stat_patterns = [
                r'tertiary education.*?(\d+[.,]?\d*\s*%?).*?(?:men|women|male|female)',
                r'(?:men|women|male|female).*?tertiary education.*?(\d+[.,]?\d*\s*%?)',
                r'university.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)',
                r'(?:men|women|male|female).*?university.*?(\d+[.,]?\d*\s*%?)',
                r'higher education.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)',
                r'(?:men|women|male|female).*?higher education.*?(\d+[.,]?\d*\s*%?)',
                r'completed.*?tertiary.*?(\d+[.,]?\d*\s*%?)',
                r'degree.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)',
                r'2011.*?education.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)'
            ]
            
            for pattern in stat_patterns:
                matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    # Get extended context around the match
                    start = max(0, match.start() - 300)
                    end = min(len(full_text), match.end() + 300)
                    context = full_text[start:end].strip()
                    
                    # Check if context mentions Bulgaria and is relevant
                    context_lower = context.lower()
                    if 'bulgaria' in context_lower or 'bulgarian' in context_lower:
                        education_stats.append({
                            'pattern': pattern,
                            'match': match.group(),
                            'context': context,
                            'source_file': html_file
                        })
            
            print(f"  Education statistics found: {len(education_stats)}")
            
            # Look for specific census data patterns
            census_patterns = [
                r'2011.*?census.*?tertiary.*?(\d+[.,]?\d*)',
                r'census.*?2011.*?education.*?(\d+[.,]?\d*)',
                r'population.*?tertiary.*?education.*?(\d+[.,]?\d*)',
                r'completed.*?tertiary.*?2011.*?(\d+[.,]?\d*)'
            ]
            
            for pattern in census_patterns:
                matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    start = max(0, match.start() - 200)
                    end = min(len(full_text), match.end() + 200)
                    context = full_text[start:end].strip()
                    
                    if 'bulgaria' in context.lower():
                        specific_findings.append({
                            'type': 'census_data',
                            'pattern': pattern,
                            'match': match.group(),
                            'context': context,
                            'source_file': html_file
                        })
            
            # Show key findings from this source
            if education_sentences:
                print(f"  Key sentence: {education_sentences[0][:200]}...")
            
            if education_stats:
                print(f"  Key statistic: {education_stats[0]['match']}")
                print(f"  Context: {education_stats[0]['context'][:150]}...")
            
            if relevant_tables and relevant_tables[0]['headers']:
                print(f"  Table headers: {relevant_tables[0]['headers'][:5]}")
            
            # Store comprehensive analysis for this source
            analysis_results.append({
                'filename': html_file,
                'title': page_title,
                'relevance_score': relevance_score,
                'content_length': len(full_text),
                'education_sentences': education_sentences[:5],  # Top 5
                'education_statistics': education_stats[:3],     # Top 3
                'relevant_tables': relevant_tables[:2],          # Top 2
                'has_bulgaria': has_bulgaria,
                'has_2011': has_2011,
                'has_census': has_census,
                'has_tertiary': has_tertiary,
                'has_gender': has_gender
            })
            
            # Add all education stats to specific findings
            for stat in education_stats:
                specific_findings.append({
                    'type': 'education_statistic',
                    'pattern': stat['pattern'],
                    'match': stat['match'],
                    'context': stat['context'],
                    'source_file': html_file
                })
        
        print()
        
    except Exception as e:
        print(f"  ✗ Error analyzing {html_file}: {str(e)}")
        print()

# Save comprehensive analysis results
print("=== COMPILATION OF FINDINGS ===\n")

final_results = {
    'search_objective': 'Bulgarian 2011 census tertiary education completion by gender',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'files_analyzed': len(html_files),
    'relevant_sources': len(analysis_results),
    'specific_findings_count': len(specific_findings),
    'analysis_results': analysis_results,
    'specific_findings': specific_findings
}

with open('workspace/bulgarian_tertiary_education_final_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(final_results, f, indent=2, ensure_ascii=False)

print(f"Final analysis saved to: workspace/bulgarian_tertiary_education_final_analysis.json")
print(f"Files analyzed: {len(html_files)}")
print(f"Relevant sources: {len(analysis_results)}")
print(f"Specific findings: {len(specific_findings)}")

# Display summary of key findings
if analysis_results:
    print("\n=== SUMMARY OF RELEVANT SOURCES ===\n")
    
    # Sort by relevance score
    analysis_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    for i, result in enumerate(analysis_results, 1):
        print(f"{i}. {result['title']} (Score: {result['relevance_score']}/6)")
        print(f"   File: {result['filename']}")
        print(f"   Content: {result['content_length']} chars")
        
        if result['education_sentences']:
            print(f"   Finding: {result['education_sentences'][0][:150]}...")
        
        if result['education_statistics']:
            print(f"   Statistic: {result['education_statistics'][0]['match']}")
        
        print()

if specific_findings:
    print("=== SPECIFIC TERTIARY EDUCATION FINDINGS ===\n")
    
    for i, finding in enumerate(specific_findings[:10], 1):  # Show top 10
        print(f"{i}. Type: {finding['type']}")
        print(f"   Match: {finding['match']}")
        print(f"   Source: {finding['source_file']}")
        print(f"   Context: {finding['context'][:200]}...")
        print()

print("=== ANALYSIS COMPLETE ===\n")
print("Bulgarian 2011 census tertiary education data by gender has been systematically extracted")
print("All findings saved to workspace for detailed review and verification")
```

### Development Step 9: Search and Download 'Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?' PDF

**Description**: Conduct a web search for the University of Leicester paper titled "Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?" and download the full PDF of that paper into workspace/dragon_diet_fish_bag.pdf.

**Use Cases**:
- Automated retrieval of quarterly 10-K and 10-Q PDF filings from sec.gov for building up-to-date financial models in investment banking
- Scheduled download of the latest ISO standard PDFs from iso.org to ensure manufacturing quality processes remain compliant
- Bulk acquisition of peer-reviewed articles in PDF format from institute domains (e.g., site:ieee.org) for training a machine-learning literature review tool
- Periodic scraping of government tender documents (site:gov.uk) to gather upcoming procurement PDFs for bid-management platforms
- Automated collection of safety data sheets (MSDS) in PDF form from chemical supplier sites to update laboratory compliance systems
- Real-time fetching of competitor product spec-sheet PDFs from electronics manufacturer domains to feed a dynamic pricing intelligence dashboard
- Routine extraction of policy white papers from think-tank websites for policy–impact analysis and briefing preparation
- Scheduled download of academic conference proceedings in PDF from university repositories to populate a citation database for researchers

```
import os
import requests

# Step 1: Ensure workspace directory exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)
print(f"[INFO] Workspace directory: {workspace}")

# Step 2: Define paper title and site-specific search query
title = "Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?"
query = f'site:le.ac.uk "{title}" filetype:pdf'
print(f"[INFO] Search query for site-specific PDF: {query}\n")

# Common headers for HTTP requests
headers = {'User-Agent': 'Mozilla/5.0'}

# Step 3: Fetch DuckDuckGo HTML for site:le.ac.uk search
print("[INFO] Fetching DuckDuckGo search results restricted to le.ac.uk...")
ddg_url = 'https://duckduckgo.com/html/'
ddg_resp = requests.get(ddg_url, params={'q': query}, headers=headers, timeout=30)
ddg_resp.raise_for_status()
path_ddg = os.path.join(workspace, 'site_le_duckduckgo_search.html')
with open(path_ddg, 'w', encoding='utf-8') as f:
    f.write(ddg_resp.text)
print(f"[DONE] Saved DuckDuckGo HTML to: {path_ddg}\n")

# Step 4: Fetch Bing HTML for site:le.ac.uk search
print("[INFO] Fetching Bing search results restricted to le.ac.uk...")
bing_url = 'https://www.bing.com/search'
bing_resp = requests.get(bing_url, params={'q': query}, headers=headers, timeout=30)
bing_resp.raise_for_status()
path_bing = os.path.join(workspace, 'site_le_bing_search.html')
with open(path_bing, 'w', encoding='utf-8') as f:
    f.write(bing_resp.text)
print(f"[DONE] Saved Bing HTML to: {path_bing}\n")

# Step 5: Next steps for parsing
print("[INFO] ===== INTERMEDIATE OUTPUTS READY =====")
print(f"- Inspect {path_ddg} to identify how PDF links or redirect parameters are structured in DuckDuckGo results.")
print(f"- Inspect {path_bing} to examine the HTML structure of Bing results and locate .pdf link patterns on le.ac.uk.")
print("After inspection, implement parsing logic to extract the actual PDF URL and perform the download to workspace/dragon_diet_fish_bag.pdf.")
```

### Development Step 56: Extract 2011 Bulgarian Census Tertiary Education Graduates by Gender from PDF file

**Description**: Extract the specific tertiary education completion data by gender from the downloaded Census2011final_en.pdf file in the workspace. Parse the document to locate the section containing tertiary education graduates by educational-qualification degree and sex, then extract the exact numbers of men and women who completed tertiary education according to the 2011 Bulgarian census.

**Use Cases**:
- Government policy analysis for designing gender-targeted higher education initiatives by extracting male and female tertiary graduation rates from national census data
- Academic research on regional gender disparities in university attainment, automating the extraction of precise graduate counts by sex for statistical studies
- Corporate human resources diversity planning by analyzing local workforce qualifications from census figures on men’s and women’s tertiary education completion
- Nonprofit program evaluation to monitor progress on gender equality in education by retrieving exact numbers of male and female degree holders from official census reports
- Data journalism for investigative stories on the gender gap in higher education, quickly pulling out tertiary graduate statistics by sex from extensive PDF documents
- EdTech product personalization that adapts learning modules based on regional gender-specific higher education completion trends derived from census data
- International development reporting to track UN Sustainable Development Goal 4 (quality education and gender parity) by extracting sex-disaggregated tertiary education figures from the latest census PDF

```
import os
from langchain_community.document_loaders import PyPDFLoader

# Use the correct PDF file path found in the previous step
pdf_path = "workspace_e0c10771-d627-4fd7-9694-05348e54ee36/census_2011_Census2011final_en.pdf"
print(f"Loading PDF file: {pdf_path}")
print(f"File size: {os.path.getsize(pdf_path)} bytes ({os.path.getsize(pdf_path)/1024/1024:.2f} MB)")

# Load and examine the PDF structure
print("\nLoading PDF with LangChain PyPDFLoader...")
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

print(f"Total pages in PDF: {len(pages)}")

if len(pages) == 0:
    print("ERROR: No pages found in PDF")
else:
    print("\n=== SEARCHING FOR TERTIARY EDUCATION DATA BY GENDER ===")
    
    # Enhanced search for education-related content
    education_keywords = ['tertiary', 'higher education', 'university', 'degree', 'graduate', 'qualification', 'educational attainment', 'education level', 'completed education']
    gender_keywords = ['men', 'women', 'male', 'female', 'sex', 'gender', 'by sex', 'by gender']
    numerical_patterns = ['total', 'number', 'persons', 'population']
    
    relevant_pages = []
    
    for i, page in enumerate(pages):
        content = page.page_content.lower()
        
        # Check if page contains education, gender, and numerical data
        has_education = any(keyword in content for keyword in education_keywords)
        has_gender = any(keyword in content for keyword in gender_keywords)
        has_numbers = any(char.isdigit() for char in page.page_content)
        has_numerical_context = any(pattern in content for pattern in numerical_patterns)
        
        # Score the relevance of each page
        relevance_score = 0
        if has_education: 
            relevance_score += 2
        if has_gender: 
            relevance_score += 2  
        if has_numbers: 
            relevance_score += 1
        if has_numerical_context: 
            relevance_score += 1
        
        if relevance_score >= 3:  # Minimum threshold for relevance
            relevant_pages.append((i, relevance_score))
            print(f"\n📄 Page {i+1} (relevance score: {relevance_score})")
            
            # Show keywords found - fix the variable scope issue
            found_edu = []
            found_gender = []
            for kw in education_keywords:
                if kw in content:
                    found_edu.append(kw)
            for kw in gender_keywords:
                if kw in content:
                    found_gender.append(kw)
                    
            print(f"  Education keywords: {found_edu}")
            print(f"  Gender keywords: {found_gender}")
            
            # Show a preview of the page content
            preview = page.page_content[:400].replace('\n', ' ').strip()
            print(f"  Preview: {preview}...")
    
    # Sort by relevance score (highest first)
    relevant_pages.sort(key=lambda x: x[1], reverse=True)
    print(f"\nFound {len(relevant_pages)} potentially relevant pages")
    
    # Examine the most relevant pages in detail
    if relevant_pages:
        print("\n=== DETAILED EXAMINATION OF MOST RELEVANT PAGES ===")
        
        for page_idx, score in relevant_pages[:3]:  # Examine top 3 most relevant pages
            print(f"\n{'='*60}")
            print(f"PAGE {page_idx+1} (Relevance Score: {score})")
            print(f"{'='*60}")
            content = pages[page_idx].page_content
            print(content)
            print(f"{'='*60}")
            
            # Look for specific patterns that might indicate tertiary education data
            lines = content.split('\n')
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                if ('tertiary' in line_lower or 'higher' in line_lower or 'university' in line_lower) and any(char.isdigit() for char in line):
                    print(f"\n*** POTENTIAL TERTIARY EDUCATION DATA (Line {line_num}): {line.strip()} ***")
    else:
        print("\n⚠️ No highly relevant pages found. Searching with broader criteria...")
        
        # Broader search for any education-related content
        for i, page in enumerate(pages[:30]):  # Check first 30 pages
            content = page.page_content.lower()
            if any(keyword in content for keyword in ['education', 'qualification', 'attainment', 'level']):
                print(f"\nPage {i+1} contains education-related content:")
                preview = page.page_content[:300].replace('\n', ' ').strip()
                print(f"Preview: {preview}...")
                
                # Check for tables or structured data
                if '|' in page.page_content or 'table' in content:
                    print("  ↳ This page appears to contain tabular data")

print("\n=== PDF ANALYSIS COMPLETE ===")
```

### Development Step 49: Download University of Leicester’s “Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?” PDF

**Description**: Conduct a web search for the University of Leicester paper titled "Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?" and download the full PDF of that paper into workspace/dragon_diet_fish_bag.pdf.

**Use Cases**:
- Financial report retrieval and parsing from corporate investor relations sites for automated quarterly earnings analysis
- Legal case brief extraction and download from court archives for law firms’ evidence preparation
- Medical guideline acquisition and integration into hospital decision support systems for clinical protocol updates
- Patent document harvesting and indexing from patent office websites for intellectual property research teams
- Environmental regulation PDF collection and compliance audit automation for industrial facilities
- Academic article gathering for systematic literature reviews in meta-analysis projects
- Technical whitepaper download and summarization for R&D product development roadmaps

```
import os
import sys
import re
import requests
from bs4 import BeautifulSoup

# --- Configuration ---
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Exact paper title to search for
title = "Can Hiccup Supply Enough Fish to Maintain a Dragon's Diet?"
# DuckDuckGo HTML interface URL
ddg_url = 'https://html.duckduckgo.com/html/'
# Browser-like headers to avoid simple blocks
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Three progressive search queries\queries = [
    f'filetype:pdf "{title}" site:lra.le.ac.uk',
    f'filetype:pdf "{title}" site:le.ac.uk',
    f'filetype:pdf "{title}"'
]

# Output file paths
ddg_html_path   = os.path.join(workspace, 'ddg_search.html')
pdf_list_path  = os.path.join(workspace, 'ddg_pdf_urls.txt')
pdf_out_path   = os.path.join(workspace, 'dragon_diet_fish_bag.pdf')

all_candidates = []
print("[INFO] Starting DuckDuckGo GET-based PDF search...")
for q in queries:
    print(f"[INFO] Query: {q}")
    try:
        resp = requests.get(ddg_url, params={'q': q}, headers=headers, timeout=30)
        print(f"[INFO] HTTP status: {resp.status_code}")
    except Exception as e:
        print(f"[WARN] Request error for query '{q}': {e}")
        continue
    if resp.status_code != 200:
        print(f"[WARN] Non-200 status for '{q}', skipping.\n")
        continue

    # Save the first successful HTML for manual inspection
    if not os.path.exists(ddg_html_path):
        with open(ddg_html_path, 'w', encoding='utf-8') as f:
            f.write(resp.text)
        print(f"[SAVE] DuckDuckGo HTML → {ddg_html_path}")

    soup = BeautifulSoup(resp.text, 'html.parser')
    candidates = set()

    # 1) DuckDuckGo result links: <a class="result__a" href=...>
    for a in soup.find_all('a', class_='result__a', href=True):
        href = a['href']
        if '.pdf' in href.lower():
            candidates.add(href)
            print(f"    [FOUND] PDF link (result__a): {href}")

    # 2) Any <a href> ending with .pdf or containing .pdf?
    for a in soup.find_all('a', href=True):
        href = a['href']
        low = href.lower()
        if low.endswith('.pdf') or '.pdf?' in low:
            candidates.add(href)
            print(f"    [FOUND] PDF link (href): {href}")

    # 3) Regex fallback for raw PDF URLs
    pattern = r'https?://[^\s"\'<>]+?\.pdf(?:\?[^\s"\'<>]*)?'
    for match in re.findall(pattern, resp.text, flags=re.IGNORECASE):
        candidates.add(match)
        print(f"    [FOUND] PDF via regex: {match}")

    # Decode any DuckDuckGo redirect wrappers (uddg=)
    for link in candidates:
        if 'uddg=' in link:
            m = re.search(r'uddg=([^&]+)', link)
            url = requests.utils.unquote(m.group(1)) if m else link
        else:
            url = link
        all_candidates.append(url)

    if all_candidates:
        print(f"[INFO] {len(all_candidates)} candidate(s) found; stopping queries.")
        break
    else:
        print(f"[INFO] No PDF links for '{q}'. Trying next.\n")

# If no candidates found, exit with error
if not all_candidates:
    print("[ERROR] No PDF candidates found after all queries.")
    print(f"Inspect '{ddg_html_path}' and refine your parsing logic.")
    sys.exit(1)

# Deduplicate and save candidate URLs\unique = []
for url in all_candidates:
    if url not in unique:
        unique.append(url)
with open(pdf_list_path, 'w', encoding='utf-8') as f:
    for u in unique:
        f.write(u + '\n')
print(f"[SAVE] Candidate PDF URLs → {pdf_list_path}")

# Function to download a PDF

def download_pdf(url, out_path):
    print(f"[INFO] Downloading PDF from: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=60)
        print(f"[INFO] Download status: {r.status_code}")
    except Exception as e:
        print(f"[ERROR] Download error: {e}")
        return False
    if r.status_code == 200 and len(r.content) > 10000:
        with open(out_path, 'wb') as f:
            f.write(r.content)
        size = os.path.getsize(out_path)
        print(f"[SUCCESS] Saved PDF → {out_path} ({size} bytes)")
        return True
    else:
        print(f"[WARN] Bad response or file too small ({len(r.content)} bytes)")
        return False

# Attempt to download each candidate until success
for url in unique:
    if download_pdf(url, pdf_out_path):
        sys.exit(0)

print(f"[ERROR] All downloads failed. Try another link from {pdf_list_path}.")
sys.exit(1)
```

## Created Time
2025-08-08 18:19:27
