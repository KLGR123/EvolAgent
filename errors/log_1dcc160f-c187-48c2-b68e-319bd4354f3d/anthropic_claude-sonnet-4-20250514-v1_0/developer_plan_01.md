# Developer Plan 01

## Plan
Search OpenReview.net for papers accepted at the NeurIPS 2022 Conference by authors named Yuri. Focus on identifying papers where an author's first name is 'Yuri' and extract their acceptance status and recommendation details. Look for papers with 'certain' recommendation status specifically. Use OpenReview's search functionality or API to filter by conference (NeurIPS 2022), author name (Yuri), and acceptance status.

## Description
This is the optimal first step because: (1) We need to systematically search OpenReview.net for NeurIPS 2022 papers by authors named Yuri to establish the baseline dataset, (2) No previous research has been conducted, (3) Expected outcome is to identify all papers by authors named Yuri at NeurIPS 2022 and their recommendation statuses, (4) This directly targets the specific conference, author name, and platform mentioned in the TASK to find papers with 'certain' recommendations

## Episodic Examples
### Development Step 1: AI Regulation Papers from arXiv (June 2022): Extract Axis Label Words from Three-Axis Figure

**Description**: Search arXiv.org for AI regulation papers originally submitted in June 2022. Focus on identifying papers that discuss artificial intelligence regulation, policy, governance, or related topics. Look for papers with submission dates in June 2022 and examine their content to find one containing a figure with three axes where each axis has label words at both ends. Extract the specific words used as axis labels in this figure.

**Use Cases**:
- Academic literature review for a university research team studying the evolution of AI regulation frameworks in mid-2022
- Automated policy landscape mapping for a government agency evaluating global trends in AI governance
- Corporate compliance team tracking recent scholarly discussions on AI ethics and regulatory challenges for risk assessment
- Legal analysts identifying precedent-setting academic papers on AI policy to inform technology law cases
- Think tank researchers extracting multidimensional frameworks from figures in AI regulation papers to visualize governance models
- Data scientists building a curated dataset of AI regulation literature with annotated axis labels for machine learning model training
- Journal editors screening June 2022 submissions for innovative visualizations of AI governance concepts
- Educational content creators sourcing authoritative diagrams from academic papers to illustrate AI policy concepts in online courses

```
import os
import requests
import json
from datetime import datetime
import time

print('=== SEARCHING ARXIV FOR AI REGULATION PAPERS FROM JUNE 2022 ===')
print('Objective: Find papers on AI regulation/policy/governance submitted in June 2022')
print('Target: Locate paper with figure having three axes with label words at both ends\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# arXiv API base URL
arxiv_base_url = 'http://export.arxiv.org/api/query'

# Search terms for AI regulation papers
search_queries = [
    'artificial intelligence regulation',
    'AI policy governance', 
    'artificial intelligence policy',
    'AI regulation framework',
    'machine learning governance',
    'AI ethics policy',
    'artificial intelligence governance'
]

print('=== STEP 1: SEARCHING ARXIV WITH MULTIPLE QUERY TERMS ===')

all_papers = []
search_results = {}

for i, query in enumerate(search_queries, 1):
    print(f'\nSearch {i}/{len(search_queries)}: "{query}"')
    
    # arXiv search parameters
    params = {
        'search_query': f'all:"{query}"',
        'start': 0,
        'max_results': 50,  # Get more results to filter by date
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(arxiv_base_url, params=params, timeout=30)
        print(f'Status code: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw XML response
            xml_file = os.path.join(workspace, f'arxiv_search_{i}_{query.replace(" ", "_")}.xml')
            with open(xml_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f'✓ Raw XML saved to: {xml_file}')
            
            # Parse XML to extract paper information
            import xml.etree.ElementTree as ET
            
            try:
                root = ET.fromstring(response.text)
                
                # Define XML namespaces
                namespaces = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }
                
                entries = root.findall('atom:entry', namespaces)
                print(f'Found {len(entries)} papers for query "{query}"')
                
                query_papers = []
                
                for entry in entries:
                    # Extract paper details
                    title_elem = entry.find('atom:title', namespaces)
                    title = title_elem.text.strip() if title_elem is not None else 'No title'
                    
                    summary_elem = entry.find('atom:summary', namespaces)
                    summary = summary_elem.text.strip() if summary_elem is not None else 'No summary'
                    
                    published_elem = entry.find('atom:published', namespaces)
                    published = published_elem.text.strip() if published_elem is not None else 'No date'
                    
                    # Get arXiv ID and PDF link
                    id_elem = entry.find('atom:id', namespaces)
                    arxiv_id = id_elem.text.strip() if id_elem is not None else 'No ID'
                    
                    # Extract arXiv ID from URL
                    if 'arxiv.org/abs/' in arxiv_id:
                        arxiv_id = arxiv_id.split('/')[-1]
                    
                    # Construct PDF URL
                    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
                    
                    # Get authors
                    authors = []
                    author_elems = entry.findall('atom:author', namespaces)
                    for author_elem in author_elems:
                        name_elem = author_elem.find('atom:name', namespaces)
                        if name_elem is not None:
                            authors.append(name_elem.text.strip())
                    
                    paper_info = {
                        'title': title,
                        'authors': authors,
                        'summary': summary,
                        'published': published,
                        'arxiv_id': arxiv_id,
                        'pdf_url': pdf_url,
                        'search_query': query
                    }
                    
                    query_papers.append(paper_info)
                    all_papers.append(paper_info)
                
                search_results[query] = query_papers
                print(f'✓ Extracted {len(query_papers)} papers from XML')
                
            except ET.ParseError as e:
                print(f'Error parsing XML for query "{query}": {str(e)}')
                continue
        
        else:
            print(f'Failed to search arXiv: {response.status_code}')
            continue
    
    except Exception as e:
        print(f'Error searching for "{query}": {str(e)}')
        continue
    
    # Small delay between requests to be respectful to arXiv
    time.sleep(1)

print(f'\n=== STEP 2: FILTERING PAPERS BY JUNE 2022 SUBMISSION DATE ===')
print(f'Total papers found across all queries: {len(all_papers)}')

# Filter papers by June 2022 submission date
june_2022_papers = []

for paper in all_papers:
    published_date = paper['published']
    
    # Parse the date (arXiv format: 2022-06-15T17:59:59Z)
    try:
        if published_date and published_date != 'No date':
            # Extract year and month from date string
            if published_date.startswith('2022-06'):
                june_2022_papers.append(paper)
                print(f'✓ June 2022 paper found: "{paper["title"][:80]}..."')
                print(f'  Published: {published_date}')
                print(f'  arXiv ID: {paper["arxiv_id"]}')
                print(f'  Authors: {", ".join(paper["authors"][:3])}{", ..." if len(paper["authors"]) > 3 else ""}')
                print()
    
    except Exception as e:
        print(f'Error parsing date for paper: {str(e)}')
        continue

print(f'\n=== FILTERING RESULTS ===')
print(f'Papers from June 2022: {len(june_2022_papers)}')

if june_2022_papers:
    # Save June 2022 papers for detailed analysis
    june_papers_file = os.path.join(workspace, 'arxiv_june_2022_ai_regulation_papers.json')
    with open(june_papers_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_date': datetime.now().isoformat(),
            'total_papers_found': len(all_papers),
            'june_2022_papers_count': len(june_2022_papers),
            'search_queries_used': search_queries,
            'june_2022_papers': june_2022_papers
        }, f, indent=2, ensure_ascii=False)
    
    print(f'✓ June 2022 papers saved to: {june_papers_file}')
    
    # Display summary of June 2022 papers
    print(f'\n=== JUNE 2022 AI REGULATION PAPERS SUMMARY ===')
    for i, paper in enumerate(june_2022_papers, 1):
        print(f'\n{i}. Title: {paper["title"]}')
        print(f'   arXiv ID: {paper["arxiv_id"]}')
        print(f'   Published: {paper["published"]}')
        print(f'   Authors: {", ".join(paper["authors"][:2])}{", ..." if len(paper["authors"]) > 2 else ""}')
        print(f'   PDF: {paper["pdf_url"]}')
        print(f'   Summary preview: {paper["summary"][:200]}...')
    
    print(f'\n=== NEXT STEPS ===')
    print(f'✓ Found {len(june_2022_papers)} AI regulation papers from June 2022')
    print(f'✓ Ready to download and analyze PDFs for figures with three axes')
    print(f'✓ Will search for figures with axis labels at both ends')
    
else:
    print('\n⚠ No papers found from June 2022 with current search terms')
    print('May need to try broader search terms or different date filtering approach')
    
    # Save all search results for analysis
    all_results_file = os.path.join(workspace, 'arxiv_all_search_results.json')
    with open(all_results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_date': datetime.now().isoformat(),
            'total_papers_found': len(all_papers),
            'search_queries_used': search_queries,
            'all_papers': all_papers[:20]  # Save first 20 for inspection
        }, f, indent=2, ensure_ascii=False)
    
    print(f'All search results saved to: {all_results_file}')
    print('Will analyze date patterns and try alternative approaches')

print('\n*** ARXIV SEARCH PHASE COMPLETE ***')
```

### Development Step 10: Identifying Society Descriptors in August 11, 2016 arXiv Physics and Society Papers Using AI Regulation Axis Labels

**Description**: Search arXiv.org for Physics and Society articles submitted on August 11, 2016. Look for papers in the physics.soc-ph category or related social physics topics from that specific date. Once found, analyze the content to determine which of the six axis label words from the June 2022 AI regulation paper (standardized, localized, egalitarian, utilitarian, subjective, objective) is used to describe a type of society in the August 11, 2016 Physics and Society article.

**Use Cases**:
- Academic literature review automation for researchers studying the evolution of societal models in physics-related social science papers
- Policy analysis for AI governance experts seeking historical context on regulatory axis labels in scientific discourse
- Bibliometric studies by librarians tracking the prevalence of specific societal descriptors in physics and society publications over time
- Automated content scanning for think tanks evaluating how terms like "egalitarian" or "utilitarian" are used in scientific literature to inform policy recommendations
- Curriculum development for university instructors designing courses on the intersection of physics, society, and regulatory frameworks
- Trend analysis for science journalists investigating shifts in academic language around social organization in physics research
- Grant proposal support for research teams needing evidence of prior work on standardized or localized societal models in physics
- AI-powered alerts for research administrators monitoring new publications that align with institutional focus areas in social physics

```
import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re

print('=== EXPANDING SEARCH TO ENTIRE AUGUST 2016 FOR PHYSICS AND SOCIETY PAPERS ===')
print('Objective: Find physics.soc-ph papers from August 2016 containing axis label words')
print('Strategy: Expand to full month since specific dates yielded no results\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# First, inspect the previous expanded search results to understand what we found
expanded_results_file = os.path.join(workspace, 'arxiv_physics_society_expanded_dates.json')

if os.path.exists(expanded_results_file):
    print('=== INSPECTING PREVIOUS EXPANDED SEARCH RESULTS ===')
    print(f'File size: {os.path.getsize(expanded_results_file):,} bytes')
    
    # Read first 300 characters to understand structure
    with open(expanded_results_file, 'r', encoding='utf-8') as f:
        sample_content = f.read(300)
        print('First 300 characters of expanded results:')
        print(sample_content)
        print('...\n')
    
    # Load and inspect the structure safely
    with open(expanded_results_file, 'r', encoding='utf-8') as f:
        expanded_data = json.load(f)
    
    print('Expanded search results structure:')
    for key, value in expanded_data.items():
        if isinstance(value, list):
            print(f'  {key}: List with {len(value)} items')
        elif isinstance(value, dict):
            print(f'  {key}: Dictionary with {len(value)} keys')
        else:
            print(f'  {key}: {type(value).__name__} = {value}')
    
    target_words = expanded_data.get('target_words', ['standardized', 'localized', 'egalitarian', 'utilitarian', 'subjective', 'objective'])
    date_range_searched = expanded_data.get('date_range_searched', [])
    papers_with_words = expanded_data.get('papers_with_target_words_count', 0)
    
    print(f'\nPrevious search details:')
    print(f'Target words: {target_words}')
    print(f'Date range searched: {date_range_searched}')
    print(f'Papers with target words found: {papers_with_words}')
    print(f'Unique papers found: {expanded_data.get("unique_papers_count", 0)}\n')
else:
    print('Previous expanded search results not found, using default settings')
    target_words = ['standardized', 'localized', 'egalitarian', 'utilitarian', 'subjective', 'objective']

# Since no papers were found in the specific week, let's try a different approach:
# 1. Search for papers from August 2016 (entire month)
# 2. Look at papers from 2016 in general that might be relevant
# 3. Focus on finding ANY physics.soc-ph papers that contain our target words

print('=== NEW STRATEGY: COMPREHENSIVE AUGUST 2016 SEARCH ===')
print('Approach: Search for physics.soc-ph papers from August 2016 containing target words')
print('Focus: Find papers that use axis label words to describe types of society\n')

# arXiv API base URL
base_url = 'http://export.arxiv.org/api/query'

# More comprehensive search approach
comprehensive_queries = [
    'cat:physics.soc-ph AND (standardized OR localized)',
    'cat:physics.soc-ph AND (egalitarian OR utilitarian)', 
    'cat:physics.soc-ph AND (subjective OR objective)',
    'cat:physics.soc-ph AND society',
    'cat:physics.soc-ph AND social',
    'physics.soc-ph standardized',
    'physics.soc-ph localized',
    'physics.soc-ph egalitarian',
    'physics.soc-ph utilitarian',
    'physics.soc-ph subjective',
    'physics.soc-ph objective',
]

print(f'Using {len(comprehensive_queries)} comprehensive search queries\n')

all_candidate_papers = []
search_results = []

for i, query in enumerate(comprehensive_queries, 1):
    print(f'Search {i}/{len(comprehensive_queries)}: "{query}"')
    
    # Parameters for arXiv API
    params = {
        'search_query': query,
        'start': 0,
        'max_results': 100,  # Reasonable limit per query
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        
        if response.status_code == 200:
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # Extract papers from XML
            query_papers = []
            august_2016_papers = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                # Extract basic information
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                title = title_elem.text.strip() if title_elem is not None else 'No title'
                
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                summary = summary_elem.text.strip() if summary_elem is not None else 'No summary'
                
                published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                published = published_elem.text.strip() if published_elem is not None else 'No date'
                
                # Extract arXiv ID
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                arxiv_url = id_elem.text.strip() if id_elem is not None else ''
                arxiv_id = arxiv_url.split('/')[-1] if arxiv_url else 'No ID'
                
                # Extract categories
                categories = []
                for category in entry.findall('{http://arxiv.org/schemas/atom}category'):
                    term = category.get('term')
                    if term:
                        categories.append(term)
                
                # Extract authors
                authors = []
                for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                    if name_elem is not None:
                        authors.append(name_elem.text.strip())
                
                # Create paper record
                paper = {
                    'title': title,
                    'authors': authors,
                    'summary': summary,
                    'published': published,
                    'arxiv_id': arxiv_id,
                    'pdf_url': f'https://arxiv.org/pdf/{arxiv_id}.pdf',
                    'categories': categories,
                    'search_query': query
                }
                
                query_papers.append(paper)
                
                # Check if this is from August 2016
                if published:
                    try:
                        paper_date = published.split('T')[0]  # Get YYYY-MM-DD part
                        if paper_date.startswith('2016-08'):
                            august_2016_papers.append(paper)
                            print(f'  ✓ Found August 2016 paper: {title[:50]}... ({arxiv_id})')
                    except:
                        continue
            
            print(f'  Total papers: {len(query_papers)}, August 2016: {len(august_2016_papers)}')
            all_candidate_papers.extend(query_papers)
            
            search_results.append({
                'query': query,
                'total_papers': len(query_papers),
                'august_2016_papers': len(august_2016_papers),
                'papers': query_papers
            })
            
        else:
            print(f'  Error: HTTP {response.status_code}')
            search_results.append({
                'query': query,
                'error': f'HTTP {response.status_code}',
                'total_papers': 0,
                'august_2016_papers': 0,
                'papers': []
            })
            
    except Exception as e:
        print(f'  Exception: {str(e)}')
        search_results.append({
            'query': query,
            'error': str(e),
            'total_papers': 0,
            'august_2016_papers': 0,
            'papers': []
        })
    
    print()

# Remove duplicates and filter for August 2016 and target words
unique_papers = {}
august_2016_papers = []
papers_with_target_words = []

for paper in all_candidate_papers:
    arxiv_id = paper.get('arxiv_id', 'unknown')
    if arxiv_id not in unique_papers:
        unique_papers[arxiv_id] = paper
        
        # Check if from August 2016
        published = paper.get('published', '')
        if published and published.startswith('2016-08'):
            august_2016_papers.append(paper)
        
        # Check for target words in title and summary
        title = paper.get('title', '').lower()
        summary = paper.get('summary', '').lower()
        combined_text = f'{title} {summary}'
        
        found_words = []
        for word in target_words:
            if word.lower() in combined_text:
                found_words.append(word)
        
        if found_words:
            paper['found_target_words'] = found_words
            papers_with_target_words.append(paper)

print(f'=== COMPREHENSIVE SEARCH RESULTS SUMMARY ===')
print(f'Total papers found: {len(all_candidate_papers)}')
print(f'Unique papers: {len(unique_papers)}')
print(f'August 2016 papers: {len(august_2016_papers)}')
print(f'Papers with target words: {len(papers_with_target_words)}\n')

# Show August 2016 papers
if august_2016_papers:
    print(f'=== AUGUST 2016 PHYSICS AND SOCIETY PAPERS ===')
    for i, paper in enumerate(august_2016_papers, 1):
        print(f'{i}. {paper.get("title", "No title")}')
        print(f'   arXiv ID: {paper.get("arxiv_id", "No ID")}')
        print(f'   Published: {paper.get("published", "No date")}')
        print(f'   Categories: {paper.get("categories", [])}')
        print(f'   Search query: {paper.get("search_query", "Unknown")}')
        
        # Check for target words in this specific paper
        title = paper.get('title', '').lower()
        summary = paper.get('summary', '').lower()
        combined_text = f'{title} {summary}'
        
        found_words = []
        for word in target_words:
            if word.lower() in combined_text:
                found_words.append(word)
        
        if found_words:
            print(f'   *** CONTAINS TARGET WORDS: {found_words} ***')
        
        print()

# Show papers with target words (regardless of date)
if papers_with_target_words:
    print(f'=== PAPERS CONTAINING TARGET WORDS (ANY DATE) ===')
    for i, paper in enumerate(papers_with_target_words[:10], 1):  # Show top 10
        print(f'{i}. {paper.get("title", "No title")}')
        print(f'   arXiv ID: {paper.get("arxiv_id", "No ID")}')
        print(f'   Published: {paper.get("published", "No date")}')
        print(f'   Target words found: {paper.get("found_target_words", [])}')
        print(f'   Categories: {paper.get("categories", [])}')
        print()

# Save comprehensive results
comprehensive_results = {
    'search_date': datetime.now().isoformat(),
    'objective': 'Find Physics and Society papers from August 2016 containing axis label words',
    'target_words': target_words,
    'search_queries': comprehensive_queries,
    'total_papers_found': len(all_candidate_papers),
    'unique_papers_count': len(unique_papers),
    'august_2016_papers_count': len(august_2016_papers),
    'papers_with_target_words_count': len(papers_with_target_words),
    'august_2016_papers': august_2016_papers,
    'papers_with_target_words': papers_with_target_words,
    'search_results_by_query': search_results
}

comprehensive_file = os.path.join(workspace, 'arxiv_comprehensive_august_2016_search.json')
with open(comprehensive_file, 'w', encoding='utf-8') as f:
    json.dump(comprehensive_results, f, indent=2, ensure_ascii=False)

print(f'✓ Comprehensive search results saved to: {comprehensive_file}')

if august_2016_papers:
    # Check if any August 2016 papers contain target words
    august_papers_with_words = [p for p in august_2016_papers if any(word.lower() in f"{p.get('title', '')} {p.get('summary', '')}".lower() for word in target_words)]
    
    if august_papers_with_words:
        print(f'\n🎯 SUCCESS! Found {len(august_papers_with_words)} August 2016 papers with target words!')
        print('Next step: Download and analyze these papers for usage describing "type of society"')
        
        for paper in august_papers_with_words:
            title = paper.get('title', '').lower()
            summary = paper.get('summary', '').lower()
            combined_text = f'{title} {summary}'
            
            found_words = [word for word in target_words if word.lower() in combined_text]
            print(f'\n📄 {paper.get("title", "No title")} ({paper.get("arxiv_id", "No ID")})')
            print(f'   Target words: {found_words}')
            print(f'   Published: {paper.get("published", "No date")}')
    else:
        print(f'\n⚠ Found {len(august_2016_papers)} August 2016 papers but none contain target words in title/abstract')
        print('Next step: Download and analyze full paper content for target words')
else:
    print(f'\n⚠ No August 2016 Physics and Society papers found')
    if papers_with_target_words:
        print(f'However, found {len(papers_with_target_words)} papers from other dates containing target words')
        print('Consider analyzing these papers or expanding the date range further')
    else:
        print('No papers found containing target words in any timeframe')
        print('May need to reconsider search strategy or target word variations')

print('\n*** COMPREHENSIVE AUGUST 2016 SEARCH COMPLETE ***')
```

### Development Step 2: Extract Axis Labels from a Three-Axis Figure in June 2022 arXiv AI Regulation Papers

**Description**: Search arXiv.org for AI regulation papers originally submitted in June 2022. Focus on identifying papers that discuss artificial intelligence regulation, policy, governance, or related topics. Look for papers with submission dates in June 2022 and examine their content to find one containing a figure with three axes where each axis has label words at both ends. Extract the specific words used as axis labels in this figure.

**Use Cases**:
- Academic literature review automation for policy researchers investigating the evolution of AI regulation frameworks in mid-2022
- Legal tech firms compiling evidence of regulatory trends for AI compliance consulting and client briefings
- Government agencies tracking the emergence of AI governance topics to inform national policy development
- Think tanks or NGOs mapping the landscape of AI ethics scholarship for strategic advocacy planning
- University instructors preparing course materials on AI policy by sourcing recent, relevant case studies and figures
- Data journalists visualizing the growth and focus areas of AI regulation research for news features
- Corporate compliance teams benchmarking their AI governance practices against the latest academic insights
- AI startup founders identifying gaps in regulatory research to guide responsible product development and investor communications

```
import os
import requests
import json
from datetime import datetime
import time
import xml.etree.ElementTree as ET

print('=== EXPANDED ARXIV SEARCH FOR AI REGULATION PAPERS FROM JUNE 2022 ===')
print('Objective: Find papers on AI regulation/policy/governance submitted in June 2022')
print('Strategy: Use broader search terms and different matching approaches\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# First, let's inspect the existing results to understand what we found
existing_file = os.path.join(workspace, 'arxiv_june_2022_ai_regulation_papers.json')
if os.path.exists(existing_file):
    print('=== INSPECTING EXISTING SEARCH RESULTS ===')
    with open(existing_file, 'r', encoding='utf-8') as f:
        existing_data = json.load(f)
    
    print(f'Previous search found {existing_data.get("june_2022_papers_count", 0)} papers from June 2022')
    print(f'Search queries used: {existing_data.get("search_queries_used", [])}\n')
    
    if 'june_2022_papers' in existing_data:
        for paper in existing_data['june_2022_papers']:
            print(f'Found paper: "{paper["title"]}"')
            print(f'Summary preview: {paper["summary"][:150]}...')
            print(f'This appears to be about: {"AI regulation" if any(term in paper["summary"].lower() for term in ["regulation", "policy", "governance", "ethics"]) else "Technical AI/ML methods"}\n')

# arXiv API base URL
arxiv_base_url = 'http://export.arxiv.org/api/query'

# Expanded search terms - using broader and more varied approaches
expanded_search_queries = [
    # Broader policy terms without exact phrase matching
    'artificial intelligence AND policy',
    'AI AND governance',
    'machine learning AND regulation',
    'algorithmic AND accountability',
    'AI AND ethics AND policy',
    'artificial intelligence AND law',
    'AI AND safety AND policy',
    'machine learning AND ethics',
    'algorithmic AND bias AND policy',
    'AI AND fairness AND regulation',
    'artificial intelligence AND society',
    'AI AND transparency',
    'machine learning AND fairness',
    'algorithmic AND governance',
    'AI AND responsible',
    # More specific regulatory terms
    'AI regulation',
    'algorithmic regulation',
    'AI policy',
    'machine learning policy',
    'AI governance',
    'algorithmic governance',
    'AI ethics',
    'responsible AI',
    'AI accountability',
    'algorithmic accountability'
]

print(f'=== STEP 1: EXPANDED SEARCH WITH {len(expanded_search_queries)} QUERY TERMS ===')

all_papers = []
search_results = {}

for i, query in enumerate(expanded_search_queries, 1):
    print(f'\nSearch {i}/{len(expanded_search_queries)}: "{query}"')
    
    # arXiv search parameters - using different search approaches
    if ' AND ' in query:
        # For AND queries, search in all fields
        search_query = f'all:{query}'
    else:
        # For single terms, search in title, abstract, and keywords
        search_query = f'ti:"{query}" OR abs:"{query}"'
    
    params = {
        'search_query': search_query,
        'start': 0,
        'max_results': 100,  # Increased to get more results
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(arxiv_base_url, params=params, timeout=30)
        print(f'Status code: {response.status_code}')
        
        if response.status_code == 200:
            # Parse XML to extract paper information
            try:
                root = ET.fromstring(response.text)
                
                # Define XML namespaces
                namespaces = {
                    'atom': 'http://www.w3.org/2005/Atom',
                    'arxiv': 'http://arxiv.org/schemas/atom'
                }
                
                entries = root.findall('atom:entry', namespaces)
                print(f'Found {len(entries)} papers for query "{query}"')
                
                query_papers = []
                
                for entry in entries:
                    # Extract paper details
                    title_elem = entry.find('atom:title', namespaces)
                    title = title_elem.text.strip() if title_elem is not None else 'No title'
                    
                    summary_elem = entry.find('atom:summary', namespaces)
                    summary = summary_elem.text.strip() if summary_elem is not None else 'No summary'
                    
                    published_elem = entry.find('atom:published', namespaces)
                    published = published_elem.text.strip() if published_elem is not None else 'No date'
                    
                    # Get arXiv ID and PDF link
                    id_elem = entry.find('atom:id', namespaces)
                    arxiv_id = id_elem.text.strip() if id_elem is not None else 'No ID'
                    
                    # Extract arXiv ID from URL
                    if 'arxiv.org/abs/' in arxiv_id:
                        arxiv_id = arxiv_id.split('/')[-1]
                    
                    # Construct PDF URL
                    pdf_url = f'https://arxiv.org/pdf/{arxiv_id}.pdf'
                    
                    # Get authors
                    authors = []
                    author_elems = entry.findall('atom:author', namespaces)
                    for author_elem in author_elems:
                        name_elem = author_elem.find('atom:name', namespaces)
                        if name_elem is not None:
                            authors.append(name_elem.text.strip())
                    
                    # Get categories
                    categories = []
                    category_elems = entry.findall('atom:category', namespaces)
                    for cat_elem in category_elems:
                        term = cat_elem.get('term')
                        if term:
                            categories.append(term)
                    
                    paper_info = {
                        'title': title,
                        'authors': authors,
                        'summary': summary,
                        'published': published,
                        'arxiv_id': arxiv_id,
                        'pdf_url': pdf_url,
                        'categories': categories,
                        'search_query': query
                    }
                    
                    query_papers.append(paper_info)
                    all_papers.append(paper_info)
                
                search_results[query] = query_papers
                print(f'✓ Extracted {len(query_papers)} papers from XML')
                
            except ET.ParseError as e:
                print(f'Error parsing XML for query "{query}": {str(e)}')
                continue
        
        else:
            print(f'Failed to search arXiv: {response.status_code}')
            continue
    
    except Exception as e:
        print(f'Error searching for "{query}": {str(e)}')
        continue
    
    # Small delay between requests to be respectful to arXiv
    time.sleep(0.5)

print(f'\n=== STEP 2: FILTERING PAPERS BY JUNE 2022 AND RELEVANCE ===') 
print(f'Total papers found across all queries: {len(all_papers)}')

# Remove duplicates based on arXiv ID
unique_papers = {}
for paper in all_papers:
    arxiv_id = paper['arxiv_id']
    if arxiv_id not in unique_papers:
        unique_papers[arxiv_id] = paper
    else:
        # Keep the one with more search queries (indicates higher relevance)
        existing_queries = unique_papers[arxiv_id].get('matching_queries', [unique_papers[arxiv_id]['search_query']])
        new_queries = existing_queries + [paper['search_query']]
        unique_papers[arxiv_id]['matching_queries'] = list(set(new_queries))

print(f'Unique papers after deduplication: {len(unique_papers)}')

# Filter papers by June 2022 submission date and relevance
june_2022_papers = []
relevant_keywords = [
    'regulation', 'policy', 'governance', 'ethics', 'law', 'legal', 'regulatory',
    'accountability', 'transparency', 'fairness', 'bias', 'responsible', 'safety',
    'society', 'social', 'impact', 'framework', 'guidelines', 'standards',
    'compliance', 'oversight', 'audit', 'explainable', 'interpretable'
]

for paper in unique_papers.values():
    published_date = paper['published']
    
    # Parse the date (arXiv format: 2022-06-15T17:59:59Z)
    try:
        if published_date and published_date != 'No date':
            # Extract year and month from date string
            if published_date.startswith('2022-06'):
                # Check if the paper is actually about AI regulation/policy
                title_lower = paper['title'].lower()
                summary_lower = paper['summary'].lower()
                combined_text = f'{title_lower} {summary_lower}'
                
                # Count relevant keywords
                relevance_score = sum(1 for keyword in relevant_keywords if keyword in combined_text)
                
                # Also check for AI/ML terms to ensure it's AI-related
                ai_terms = ['artificial intelligence', 'ai ', 'machine learning', 'ml ', 'deep learning', 'neural', 'algorithm']
                has_ai_terms = any(term in combined_text for term in ai_terms)
                
                paper['relevance_score'] = relevance_score
                paper['has_ai_terms'] = has_ai_terms
                
                # Include if it has both AI terms and policy relevance
                if has_ai_terms and relevance_score > 0:
                    june_2022_papers.append(paper)
                    print(f'✓ Relevant June 2022 paper found: "{paper["title"][:80]}..."')
                    print(f'  Published: {published_date}')
                    print(f'  arXiv ID: {paper["arxiv_id"]}')
                    print(f'  Relevance score: {relevance_score} (keywords: {[kw for kw in relevant_keywords if kw in combined_text][:5]})')
                    print(f'  Categories: {paper.get("categories", [])[:3]}')
                    print(f'  Authors: {", ".join(paper["authors"][:2])}{"..." if len(paper["authors"]) > 2 else ""}')
                    print()
                elif published_date.startswith('2022-06'):
                    print(f'⚠ June 2022 paper found but low relevance: "{paper["title"][:60]}..."')
                    print(f'  Relevance score: {relevance_score}, Has AI terms: {has_ai_terms}')
                    print()
    
    except Exception as e:
        print(f'Error parsing date for paper: {str(e)}')
        continue

print(f'\n=== FILTERING RESULTS ===') 
print(f'Relevant AI regulation papers from June 2022: {len(june_2022_papers)}')

if june_2022_papers:
    # Sort by relevance score
    june_2022_papers.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
    
    # Save June 2022 papers for detailed analysis
    june_papers_file = os.path.join(workspace, 'arxiv_june_2022_ai_regulation_papers_expanded.json')
    with open(june_papers_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_date': datetime.now().isoformat(),
            'total_papers_found': len(all_papers),
            'unique_papers_count': len(unique_papers),
            'june_2022_relevant_papers_count': len(june_2022_papers),
            'search_queries_used': expanded_search_queries,
            'relevance_keywords': relevant_keywords,
            'june_2022_papers': june_2022_papers
        }, f, indent=2, ensure_ascii=False)
    
    print(f'✓ June 2022 relevant papers saved to: {june_papers_file}')
    
    # Display summary of June 2022 papers
    print(f'\n=== JUNE 2022 AI REGULATION PAPERS SUMMARY (RANKED BY RELEVANCE) ===')
    for i, paper in enumerate(june_2022_papers, 1):
        print(f'\n{i}. Title: {paper["title"]}')
        print(f'   arXiv ID: {paper["arxiv_id"]}')
        print(f'   Published: {paper["published"]}')
        print(f'   Relevance Score: {paper.get("relevance_score", 0)}')
        print(f'   Categories: {", ".join(paper.get("categories", [])[:3])}')
        print(f'   Authors: {", ".join(paper["authors"][:2])}{"..." if len(paper["authors"]) > 2 else ""}')
        print(f'   PDF: {paper["pdf_url"]}')
        print(f'   Summary preview: {paper["summary"][:200]}...')
        
        # Show matching search queries if available
        if 'matching_queries' in paper:
            print(f'   Matched queries: {", ".join(paper["matching_queries"][:3])}{"..." if len(paper.get("matching_queries", [])) > 3 else ""}')
    
    print(f'\n=== NEXT STEPS ===')
    print(f'✓ Found {len(june_2022_papers)} relevant AI regulation papers from June 2022')
    print(f'✓ Papers ranked by policy relevance (regulation/governance keywords)')
    print(f'✓ Ready to download and analyze PDFs for figures with three axes')
    print(f'✓ Will search for figures with axis labels at both ends')
    
else:
    print('\n⚠ No relevant AI regulation papers found from June 2022')
    print('Will save all search results for further analysis')
    
    # Save all search results for analysis
    all_results_file = os.path.join(workspace, 'arxiv_expanded_search_results.json')
    with open(all_results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_date': datetime.now().isoformat(),
            'total_papers_found': len(all_papers),
            'unique_papers_count': len(unique_papers),
            'search_queries_used': expanded_search_queries,
            'sample_papers': list(unique_papers.values())[:10]  # Save first 10 for inspection
        }, f, indent=2, ensure_ascii=False)
    
    print(f'All expanded search results saved to: {all_results_file}')
    print('Will analyze results and consider alternative approaches')

print('\n*** EXPANDED ARXIV SEARCH PHASE COMPLETE ***')
```

### Development Step 8: Identifying Society Type Labels in August 11, 2016 arXiv Physics and Society Papers Using AI Regulation Axes

**Description**: Search arXiv.org for Physics and Society articles submitted on August 11, 2016. Look for papers in the physics.soc-ph category or related social physics topics from that specific date. Once found, analyze the content to determine which of the six axis label words from the June 2022 AI regulation paper (standardized, localized, egalitarian, utilitarian, subjective, objective) is used to describe a type of society in the August 11, 2016 Physics and Society article.

**Use Cases**:
- Academic literature review automation for researchers studying the historical evolution of societal models in physics-related social science papers
- Regulatory policy analysis for government agencies tracking the prevalence of specific societal descriptors (e.g., "egalitarian", "utilitarian") in scientific discourse
- AI ethics curriculum development by educators seeking real-world examples of society types as discussed in physics and society literature
- Bibliometric studies by librarians or information scientists quantifying the use of standardized versus localized societal frameworks in arXiv publications over time
- Automated content curation for science communicators highlighting trends in social physics research on specific dates or periods
- Grant proposal support for research teams needing evidence of prior work using particular societal descriptors in the context of AI regulation
- Competitive intelligence gathering for think tanks analyzing how academic language around society types aligns with emerging policy debates
- Historical trend analysis for sociologists investigating shifts in the academic framing of society types within the physics and society domain

```
import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, date
import re

print('=== SEARCHING ARXIV FOR PHYSICS AND SOCIETY ARTICLES FROM AUGUST 11, 2016 ===')
print('Objective: Find physics.soc-ph papers from August 11, 2016 that use axis label words')
print('Target words: standardized, localized, egalitarian, utilitarian, subjective, objective\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# First, let's inspect the previous results to confirm the axis label words
three_axis_file = os.path.join(workspace, 'three_axis_figure_answer.json')
if os.path.exists(three_axis_file):
    print('=== CONFIRMING AXIS LABEL WORDS FROM JUNE 2022 PAPER ===')
    with open(three_axis_file, 'r', encoding='utf-8') as f:
        axis_data = json.load(f)
    
    print(f'Paper: {axis_data.get("paper_title", "Unknown")}') 
    print(f'Figure: {axis_data.get("figure_reference", "Unknown")}')
    
    identified_axes = axis_data.get('identified_axes', [])
    all_labels = axis_data.get('all_axis_labels_found', [])
    
    print('\nIdentified three axes:')
    for axis in identified_axes:
        print(f'  {axis}')
    
    print(f'\nAll axis labels found: {all_labels}')
    
    # Extract the six key words we need to search for
    target_words = ['standardized', 'localized', 'egalitarian', 'utilitarian', 'subjective', 'objective']
    confirmed_words = [word for word in target_words if word in all_labels]
    
    print(f'\nConfirmed target words to search for: {confirmed_words}')
    print('\n' + '='*60 + '\n')
else:
    print('Previous axis analysis not found, using default target words')
    target_words = ['standardized', 'localized', 'egalitarian', 'utilitarian', 'subjective', 'objective']
    confirmed_words = target_words

# Now search arXiv for Physics and Society papers from August 11, 2016
print('=== SEARCHING ARXIV FOR PHYSICS AND SOCIETY PAPERS - AUGUST 11, 2016 ===')
print('Target date: 2016-08-11')
print('Categories: physics.soc-ph (Physics and Society)\n')

# arXiv API base URL
base_url = 'http://export.arxiv.org/api/query'

# Search queries for Physics and Society papers
search_queries = [
    'cat:physics.soc-ph',  # Direct category search
    'physics AND society',  # General physics and society
    'social physics',       # Social physics topics
    'sociophysics',        # Sociophysics
    'physics.soc-ph',      # Alternative category format
]

print(f'Using {len(search_queries)} search strategies for Physics and Society papers\n')

all_papers = []
search_results = []

for i, query in enumerate(search_queries, 1):
    print(f'Search {i}/{len(search_queries)}: "{query}"')
    
    # Parameters for arXiv API
    params = {
        'search_query': query,
        'start': 0,
        'max_results': 200,  # Get more results to find papers from specific date
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=30)
        print(f'Status code: {response.status_code}')
        
        if response.status_code == 200:
            # Parse XML response
            root = ET.fromstring(response.content)
            
            # Extract papers from XML
            papers = []
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                # Extract basic information
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                title = title_elem.text.strip() if title_elem is not None else 'No title'
                
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                summary = summary_elem.text.strip() if summary_elem is not None else 'No summary'
                
                published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                published = published_elem.text.strip() if published_elem is not None else 'No date'
                
                # Extract arXiv ID
                id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                arxiv_url = id_elem.text.strip() if id_elem is not None else ''
                arxiv_id = arxiv_url.split('/')[-1] if arxiv_url else 'No ID'
                
                # Extract categories
                categories = []
                for category in entry.findall('{http://arxiv.org/schemas/atom}category'):
                    term = category.get('term')
                    if term:
                        categories.append(term)
                
                # Extract authors
                authors = []
                for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                    if name_elem is not None:
                        authors.append(name_elem.text.strip())
                
                # Create paper record
                paper = {
                    'title': title,
                    'authors': authors,
                    'summary': summary,
                    'published': published,
                    'arxiv_id': arxiv_id,
                    'pdf_url': f'https://arxiv.org/pdf/{arxiv_id}.pdf',
                    'categories': categories,
                    'search_query': query
                }
                
                papers.append(paper)
            
            print(f'Found {len(papers)} papers for query "{query}"')
            all_papers.extend(papers)
            
            search_results.append({
                'query': query,
                'papers_found': len(papers),
                'papers': papers
            })
            
        else:
            print(f'Error: HTTP {response.status_code}')
            search_results.append({
                'query': query,
                'error': f'HTTP {response.status_code}',
                'papers_found': 0,
                'papers': []
            })
            
    except Exception as e:
        print(f'Exception: {str(e)}')
        search_results.append({
            'query': query,
            'error': str(e),
            'papers_found': 0,
            'papers': []
        })
    
    print()

print(f'=== SEARCH RESULTS SUMMARY ===')
print(f'Total papers found across all queries: {len(all_papers)}')

# Remove duplicates based on arXiv ID
unique_papers = {}
for paper in all_papers:
    arxiv_id = paper.get('arxiv_id', 'unknown')
    if arxiv_id not in unique_papers:
        unique_papers[arxiv_id] = paper
    else:
        # Add search query to existing paper if different
        existing_query = unique_papers[arxiv_id].get('search_query', '')
        new_query = paper.get('search_query', '')
        if new_query not in existing_query:
            unique_papers[arxiv_id]['search_query'] = f"{existing_query}, {new_query}"

print(f'Unique papers after deduplication: {len(unique_papers)}')

# Filter papers by date - looking for August 11, 2016
target_date = '2016-08-11'
august_11_papers = []

print(f'\n=== FILTERING FOR AUGUST 11, 2016 SUBMISSIONS ===')
print(f'Target date: {target_date}\n')

for paper in unique_papers.values():
    published_date = paper.get('published', '')
    
    # Extract date from published timestamp (format: 2016-08-11T17:58:23Z)
    if published_date:
        try:
            # Parse the date part
            date_part = published_date.split('T')[0]  # Get YYYY-MM-DD part
            
            if date_part == target_date:
                august_11_papers.append(paper)
                print(f'✓ Found August 11, 2016 paper:')
                print(f'  Title: {paper.get("title", "No title")[:80]}...')
                print(f'  arXiv ID: {paper.get("arxiv_id", "Unknown")}')
                print(f'  Published: {published_date}')
                print(f'  Categories: {paper.get("categories", [])}')
                print(f'  Search query: {paper.get("search_query", "Unknown")}')
                print()
                
        except Exception as e:
            print(f'Error parsing date for paper {paper.get("arxiv_id", "unknown")}: {e}')

print(f'Papers found from August 11, 2016: {len(august_11_papers)}')

# Save search results
search_data = {
    'search_date': datetime.now().isoformat(),
    'target_date': target_date,
    'target_words': confirmed_words,
    'search_queries': search_queries,
    'total_papers_found': len(all_papers),
    'unique_papers_count': len(unique_papers),
    'august_11_papers_count': len(august_11_papers),
    'august_11_papers': august_11_papers,
    'search_results': search_results
}

results_file = os.path.join(workspace, 'arxiv_physics_society_august_11_2016.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_data, f, indent=2, ensure_ascii=False)

print(f'\n✓ Search results saved to: {results_file}')

if august_11_papers:
    print(f'\n=== NEXT STEPS ===')
    print(f'Found {len(august_11_papers)} Physics and Society papers from August 11, 2016')
    print('Next step: Download and analyze these papers to search for the target words:')
    print(f'Target words: {confirmed_words}')
    print('Looking for usage describing "type of society"')
else:
    print(f'\n⚠ No papers found from August 11, 2016')
    print('May need to:')
    print('1. Expand date range to nearby dates')
    print('2. Try different search strategies')
    print('3. Check if papers were submitted on different dates but published on Aug 11')

print('\n*** ARXIV PHYSICS AND SOCIETY SEARCH COMPLETE ***')
```

### Development Step 9: Identifying Society Type Axis Labels in August 11, 2016 Physics and Society arXiv Articles

**Description**: Search arXiv.org for Physics and Society articles submitted on August 11, 2016. Look for papers in the physics.soc-ph category or related social physics topics from that specific date. Once found, analyze the content to determine which of the six axis label words from the June 2022 AI regulation paper (standardized, localized, egalitarian, utilitarian, subjective, objective) is used to describe a type of society in the August 11, 2016 Physics and Society article.

**Use Cases**:
- Academic literature review automation for researchers studying societal models in physics and AI regulation
- Policy analysis for government agencies tracking historical trends in AI governance terminology within scientific papers
- Automated detection of regulatory language in physics and society publications for legal tech platforms
- Curriculum development for university courses on sociophysics, enabling instructors to source relevant papers with specific societal descriptors
- Corporate R&D intelligence gathering for tech companies monitoring academic discourse on AI ethics and societal impact
- Data-driven journalism workflows for reporters investigating the evolution of societal classification in scientific literature
- Bibliometric analysis for librarians curating collections on social physics and regulatory frameworks
- Grant proposal support for research teams needing evidence of terminology usage in foundational studies on AI and society

```
import os
import json
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import re

print('=== EXPANDING SEARCH TO NEARBY DATES AROUND AUGUST 11, 2016 ===')
print('Objective: Find Physics and Society papers from August 8-14, 2016 timeframe')
print('Strategy: Expand date range since no papers found on exact date\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# First, inspect the previous search results to understand what we found
previous_results_file = os.path.join(workspace, 'arxiv_physics_society_august_11_2016.json')

if os.path.exists(previous_results_file):
    print('=== INSPECTING PREVIOUS SEARCH RESULTS ===')
    print(f'File size: {os.path.getsize(previous_results_file):,} bytes')
    
    # Read first 500 characters to understand structure
    with open(previous_results_file, 'r', encoding='utf-8') as f:
        sample_content = f.read(500)
        print('First 500 characters of previous results:')
        print(sample_content)
        print('...\n')
    
    # Load and inspect the full structure
    with open(previous_results_file, 'r', encoding='utf-8') as f:
        previous_data = json.load(f)
    
    print('Previous search results structure:')
    for key, value in previous_data.items():
        if isinstance(value, list):
            print(f'  {key}: List with {len(value)} items')
        elif isinstance(value, dict):
            print(f'  {key}: Dictionary with {len(value)} keys')
        else:
            print(f'  {key}: {type(value).__name__} = {value}')
    
    target_words = previous_data.get('target_words', ['standardized', 'localized', 'egalitarian', 'utilitarian', 'subjective', 'objective'])
    print(f'\nConfirmed target words: {target_words}')
    print(f'Previous search found {previous_data.get("unique_papers_count", 0)} unique papers')
    print(f'Papers from August 11, 2016: {previous_data.get("august_11_papers_count", 0)}\n')
else:
    print('Previous search results not found, using default target words')
    target_words = ['standardized', 'localized', 'egalitarian', 'utilitarian', 'subjective', 'objective']

# Define expanded date range around August 11, 2016
base_date = datetime(2016, 8, 11)
date_range = []

# Create date range from August 8-14, 2016 (7 days total)
for i in range(-3, 4):  # -3 to +3 days from August 11
    target_date = base_date + timedelta(days=i)
    date_range.append(target_date.strftime('%Y-%m-%d'))

print(f'=== EXPANDED DATE RANGE SEARCH ===')
print(f'Searching dates: {date_range}')
print(f'Total date range: {len(date_range)} days\n')

# arXiv API base URL
base_url = 'http://export.arxiv.org/api/query'

# Focus on the most effective search queries from previous attempt
focused_queries = [
    'cat:physics.soc-ph',  # Direct category search - most effective
    'social physics',       # Social physics topics
    'sociophysics',        # Sociophysics
]

print(f'Using {len(focused_queries)} focused search queries\n')

all_papers_by_date = {}
date_search_results = []

for date_str in date_range:
    print(f'=== SEARCHING FOR DATE: {date_str} ===')
    
    date_papers = []
    
    for i, query in enumerate(focused_queries, 1):
        print(f'  Query {i}/{len(focused_queries)}: "{query}"')
        
        # Parameters for arXiv API - get more results to find papers from specific dates
        params = {
            'search_query': query,
            'start': 0,
            'max_results': 300,  # Increased to get more comprehensive results
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            response = requests.get(base_url, params=params, timeout=30)
            
            if response.status_code == 200:
                # Parse XML response
                root = ET.fromstring(response.content)
                
                # Extract papers from XML
                query_papers = []
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    # Extract basic information
                    title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                    title = title_elem.text.strip() if title_elem is not None else 'No title'
                    
                    summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                    summary = summary_elem.text.strip() if summary_elem is not None else 'No summary'
                    
                    published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                    published = published_elem.text.strip() if published_elem is not None else 'No date'
                    
                    # Extract arXiv ID
                    id_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                    arxiv_url = id_elem.text.strip() if id_elem is not None else ''
                    arxiv_id = arxiv_url.split('/')[-1] if arxiv_url else 'No ID'
                    
                    # Extract categories
                    categories = []
                    for category in entry.findall('{http://arxiv.org/schemas/atom}category'):
                        term = category.get('term')
                        if term:
                            categories.append(term)
                    
                    # Extract authors
                    authors = []
                    for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                        name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                        if name_elem is not None:
                            authors.append(name_elem.text.strip())
                    
                    # Check if this paper matches our target date
                    if published:
                        try:
                            paper_date = published.split('T')[0]  # Get YYYY-MM-DD part
                            
                            if paper_date == date_str:
                                paper = {
                                    'title': title,
                                    'authors': authors,
                                    'summary': summary,
                                    'published': published,
                                    'arxiv_id': arxiv_id,
                                    'pdf_url': f'https://arxiv.org/pdf/{arxiv_id}.pdf',
                                    'categories': categories,
                                    'search_query': query,
                                    'target_date': date_str
                                }
                                
                                query_papers.append(paper)
                                date_papers.append(paper)
                                
                                print(f'    ✓ Found paper from {date_str}:')
                                print(f'      Title: {title[:60]}...')
                                print(f'      arXiv ID: {arxiv_id}')
                                print(f'      Categories: {categories}')
                                
                        except Exception as e:
                            continue
                
                print(f'    Papers found for {date_str}: {len(query_papers)}')
                
            else:
                print(f'    Error: HTTP {response.status_code}')
                
        except Exception as e:
            print(f'    Exception: {str(e)}')
    
    all_papers_by_date[date_str] = date_papers
    print(f'  Total papers found for {date_str}: {len(date_papers)}\n')

# Compile all found papers
all_found_papers = []
for date_papers in all_papers_by_date.values():
    all_found_papers.extend(date_papers)

# Remove duplicates based on arXiv ID
unique_papers = {}
for paper in all_found_papers:
    arxiv_id = paper.get('arxiv_id', 'unknown')
    if arxiv_id not in unique_papers:
        unique_papers[arxiv_id] = paper

print(f'=== EXPANDED SEARCH RESULTS SUMMARY ===')
print(f'Date range searched: {date_range[0]} to {date_range[-1]}')
print(f'Total papers found: {len(all_found_papers)}')
print(f'Unique papers after deduplication: {len(unique_papers)}\n')

# Show papers by date
for date_str in date_range:
    papers_count = len(all_papers_by_date.get(date_str, []))
    if papers_count > 0:
        print(f'{date_str}: {papers_count} papers')
        for paper in all_papers_by_date[date_str][:3]:  # Show first 3 papers per date
            print(f'  - {paper.get("title", "No title")[:50]}... ({paper.get("arxiv_id", "No ID")})')
        if papers_count > 3:
            print(f'  ... and {papers_count - 3} more papers')
        print()

if unique_papers:
    print(f'=== ANALYZING PAPERS FOR TARGET WORDS ===')
    print(f'Target words: {target_words}\n')
    
    # Quick text analysis to find papers containing target words
    papers_with_target_words = []
    
    for paper in unique_papers.values():
        title = paper.get('title', '').lower()
        summary = paper.get('summary', '').lower()
        combined_text = f'{title} {summary}'
        
        found_words = []
        for word in target_words:
            if word.lower() in combined_text:
                found_words.append(word)
        
        if found_words:
            paper['found_target_words'] = found_words
            papers_with_target_words.append(paper)
            
            print(f'✓ Paper contains target words: {found_words}')
            print(f'  Title: {paper.get("title", "No title")}')
            print(f'  arXiv ID: {paper.get("arxiv_id", "No ID")}')
            print(f'  Date: {paper.get("target_date", "Unknown")}')
            print(f'  Categories: {paper.get("categories", [])}')
            print()
    
    print(f'Papers containing target words: {len(papers_with_target_words)}')
    
    # Save expanded search results
    expanded_results = {
        'search_date': datetime.now().isoformat(),
        'date_range_searched': date_range,
        'target_words': target_words,
        'search_queries': focused_queries,
        'total_papers_found': len(all_found_papers),
        'unique_papers_count': len(unique_papers),
        'papers_with_target_words_count': len(papers_with_target_words),
        'papers_by_date': all_papers_by_date,
        'papers_with_target_words': papers_with_target_words,
        'all_unique_papers': list(unique_papers.values())
    }
    
    expanded_file = os.path.join(workspace, 'arxiv_physics_society_expanded_dates.json')
    with open(expanded_file, 'w', encoding='utf-8') as f:
        json.dump(expanded_results, f, indent=2, ensure_ascii=False)
    
    print(f'✓ Expanded search results saved to: {expanded_file}')
    
    if papers_with_target_words:
        print(f'\n=== SUCCESS! FOUND CANDIDATE PAPERS ===')
        print(f'Found {len(papers_with_target_words)} papers containing target axis label words')
        print('Next step: Download and analyze these papers to find usage describing "type of society"')
    else:
        print(f'\n=== NO TARGET WORDS FOUND IN ABSTRACTS ===')
        print('Target words may appear in full paper content rather than titles/abstracts')
        print('Next step: Download and analyze full paper content for target words')
        
else:
    print('No papers found in the expanded date range')
    print('May need to expand further or try different search strategies')

print('\n*** EXPANDED ARXIV SEARCH COMPLETE ***')
```

## Created Time
2025-08-11 01:53:42
