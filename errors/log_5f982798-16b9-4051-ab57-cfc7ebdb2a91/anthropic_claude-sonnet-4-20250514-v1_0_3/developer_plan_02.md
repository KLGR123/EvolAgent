# Developer Plan 02

## Plan
Expand the search to include papers from February, March, and April 2021 on arXiv about fast radio bursts and multiwavelength observations. Since the March 2021 search yielded no results, broaden the timeframe to capture papers that might have been submitted slightly before or after March 2021. Focus on identifying papers with X-ray time profile diagrams, timing measurements, and author lists that could connect to a July 2020 FRB paper by overlapping authors.

## Description
This expanded approach is necessary because: (1) The previous comprehensive search found zero FRB papers published specifically in March 2021, suggesting the user's memory of the exact timing may be slightly off, (2) Expanding to a 3-month window around March 2021 increases the likelihood of finding the target paper with X-ray time profile diagrams, (3) Expected outcome is to identify the multiwavelength FRB paper with X-ray timing measurements and extract author information for subsequent matching with July 2020 papers, (4) This addresses the possibility that the paper was submitted in late February or early April but the user remembered it as March 2021

## Episodic Examples
### Development Step 1: Title: Locate and Extract Content from Carolyn Collins Petersen’s Universe Today Article Published June 6, 2023

**Description**: Search for the article by Carolyn Collins Petersen published on Universe Today on June 6, 2023. Look for the specific article using search queries like 'Carolyn Collins Petersen Universe Today June 6 2023', 'site:universetoday.com Carolyn Collins Petersen June 6 2023', and variations with different keyword combinations. Extract the article content and identify the research paper link mentioned at the bottom of the article.

**Use Cases**:
- Academic librarian automating the retrieval and archiving of specific science news articles and their referenced research papers for institutional repositories
- Science journalist conducting rapid fact-checking and sourcing of original research papers linked in astronomy news articles for accurate reporting
- Research assistant compiling a dataset of media coverage and primary sources for a meta-study on how scientific discoveries are communicated to the public
- University outreach coordinator curating up-to-date, source-verified astronomy articles and associated research for educational newsletters
- Data analyst tracking citation patterns by extracting research paper links from popular science websites for bibliometric studies
- AI developer training a model to recognize and extract research references from web articles for automated literature review tools
- Corporate R&D team monitoring recent scientific advances by programmatically collecting and summarizing news articles and their cited studies in relevant fields
- Science podcast producer preparing episode notes by automatically gathering article texts and original research links to share with listeners

```
import os
import requests
from datetime import datetime

print("=== SEARCHING FOR CAROLYN COLLINS PETERSEN ARTICLE - JUNE 6, 2023 ===\n")
print("Objective: Find article by Carolyn Collins Petersen published on Universe Today on June 6, 2023\n")

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
    
    # Multiple targeted search queries for the specific article
    search_queries = [
        'Carolyn Collins Petersen Universe Today June 6 2023',
        'site:universetoday.com "Carolyn Collins Petersen" "June 6, 2023"',
        '"Carolyn Collins Petersen" "Universe Today" "June 6" 2023',
        'site:universetoday.com Carolyn Collins Petersen June 2023',
        '"universetoday.com" "Carolyn Collins Petersen" "06/06/2023"',
        'Universe Today Carolyn Collins Petersen June 6 2023 article',
        'site:universetoday.com "Carolyn Petersen" June 2023',
        '"Carolyn Collins Petersen" Universe Today "June 2023"'
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
                            'is_universe_today': 'universetoday.com' in result.get('link', '').lower(),
                            'has_author_name': any(name in result.get('snippet', '').lower() + result.get('title', '').lower() 
                                                 for name in ['carolyn collins petersen', 'carolyn petersen', 'c. petersen']),
                            'has_june_2023': any(term in result.get('snippet', '').lower() + result.get('title', '').lower() 
                                               for term in ['june 6, 2023', 'june 6 2023', 'jun 6, 2023', '06/06/2023', 'june 2023'])
                        }
                        
                        all_search_results.append(result_info)
                        
                        # Print relevant results immediately
                        if result_info['is_universe_today']:
                            print(f"  ★ UNIVERSE TODAY RESULT {j}:")
                            print(f"    Title: {result_info['title']}")
                            print(f"    Link: {result_info['link']}")
                            print(f"    Snippet: {result_info['snippet'][:200]}...")
                            print(f"    Author match: {result_info['has_author_name']}")
                            print(f"    June 2023 match: {result_info['has_june_2023']}")
                        elif result_info['has_author_name'] and result_info['has_june_2023']:
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
    
    # Filter and prioritize Universe Today results
    ut_results = [r for r in all_search_results if r['is_universe_today']]
    print(f"Universe Today official results: {len(ut_results)}")
    
    # Filter results with author name and June 2023
    relevant_results = [r for r in all_search_results if r['has_author_name'] and r['has_june_2023']]
    print(f"Results with author + June 2023: {len(relevant_results)}")
    
    # Find the most promising matches
    perfect_matches = [r for r in all_search_results if r['is_universe_today'] and r['has_author_name'] and r['has_june_2023']]
    print(f"Perfect matches (Universe Today + Author + June 2023): {len(perfect_matches)}")
    
    if perfect_matches:
        print("\n=== PERFECT MATCHES FOUND ===\n")
        for i, result in enumerate(perfect_matches, 1):
            print(f"{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Snippet: {result['snippet']}")
            print(f"   From Query: {result['query_number']}")
            print()
        
        target_article = perfect_matches[0]  # Take the first perfect match
        
    elif ut_results:
        print("\n=== UNIVERSE TODAY RESULTS (checking for matches) ===\n")
        for i, result in enumerate(ut_results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Snippet: {result['snippet']}")
            print(f"   Author match: {result['has_author_name']}")
            print(f"   June 2023 match: {result['has_june_2023']}")
            print(f"   From Query: {result['query_number']}")
            print()
        
        # Take the most promising Universe Today result
        target_article = ut_results[0]
        
    elif relevant_results:
        print("\n=== OTHER RELEVANT RESULTS ===\n")
        for i, result in enumerate(relevant_results, 1):
            print(f"{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Snippet: {result['snippet']}")
            print()
        
        target_article = relevant_results[0]
        
    else:
        print("\n⚠️ No highly relevant results found")
        print("Showing top 5 overall results for manual review:")
        
        for i, result in enumerate(all_search_results[:5], 1):
            print(f"{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Snippet: {result['snippet'][:150]}...")
            print()
        
        if all_search_results:
            target_article = all_search_results[0]
        else:
            target_article = None
    
    # Save search results for reference
    import json
    search_summary = {
        'search_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'target_article': 'Carolyn Collins Petersen article on Universe Today, June 6, 2023',
        'queries_executed': search_queries,
        'total_results': len(all_search_results),
        'universe_today_results': len(ut_results),
        'perfect_matches': len(perfect_matches) if 'perfect_matches' in locals() else 0,
        'relevant_results': len(relevant_results),
        'all_results': all_search_results
    }
    
    search_results_file = 'workspace/carolyn_petersen_search_results.json'
    with open(search_results_file, 'w') as f:
        json.dump(search_summary, f, indent=2)
    
    print(f"\nSearch results saved to: {search_results_file}")
    
    # Now attempt to access the target article
    if target_article:
        print(f"\n=== ACCESSING TARGET ARTICLE ===\n")
        target_url = target_article['link']
        print(f"Target URL: {target_url}")
        print(f"Article title: {target_article['title']}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            page_response = requests.get(target_url, headers=headers, timeout=30)
            
            if page_response.status_code == 200:
                print(f"✓ Successfully accessed article (Status: {page_response.status_code})")
                print(f"Content length: {len(page_response.content):,} bytes")
                
                # Save the HTML content
                html_filename = 'workspace/carolyn_petersen_universe_today_article.html'
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(page_response.text)
                
                print(f"✓ Article HTML saved to: {html_filename}")
                
                # Parse the content to extract article text
                from bs4 import BeautifulSoup
                
                soup = BeautifulSoup(page_response.content, 'html.parser')
                
                # Extract article title
                title_element = soup.find('h1') or soup.find('title')
                article_title = title_element.get_text().strip() if title_element else 'Title not found'
                print(f"\nExtracted title: {article_title}")
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get article text
                article_text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in article_text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                clean_text = ' '.join(chunk for chunk in chunks if chunk)
                
                print(f"Article text length: {len(clean_text):,} characters")
                
                # Save clean article text
                text_filename = 'workspace/carolyn_petersen_article_text.txt'
                with open(text_filename, 'w', encoding='utf-8') as f:
                    f.write(f"Title: {article_title}\n")
                    f.write(f"URL: {target_url}\n")
                    f.write(f"Author: Carolyn Collins Petersen\n")
                    f.write(f"Date: June 6, 2023\n")
                    f.write(f"Source: Universe Today\n")
                    f.write("=" * 50 + "\n")
                    f.write(clean_text)
                
                print(f"✓ Clean article text saved to: {text_filename}")
                
                # Look for research paper links in the article
                print(f"\n=== SEARCHING FOR RESEARCH PAPER LINKS ===\n")
                
                # Find all links in the article
                links = soup.find_all('a', href=True)
                
                research_links = []
                paper_keywords = ['doi.org', 'arxiv.org', 'nature.com', 'science.org', 'iopscience', 'aas.org', 'adsabs', 'journal', 'paper', 'study', 'research']
                
                print(f"Found {len(links)} total links in article")
                
                for link in links:
                    href = link.get('href')
                    link_text = link.get_text().strip()
                    
                    # Check if this looks like a research paper link
                    is_research_link = any(keyword in href.lower() for keyword in paper_keywords)
                    
                    if is_research_link:
                        research_links.append({
                            'url': href,
                            'text': link_text,
                            'context': str(link.parent)[:200] if link.parent else 'No context'
                        })
                
                print(f"Found {len(research_links)} potential research paper links:")
                
                for i, link in enumerate(research_links, 1):
                    print(f"\n{i}. {link['text'][:100]}...")
                    print(f"   URL: {link['url']}")
                    print(f"   Context: {link['context'][:150]}...")
                
                # Save research links
                links_data = {
                    'article_title': article_title,
                    'article_url': target_url,
                    'total_links': len(links),
                    'research_links_found': len(research_links),
                    'research_links': research_links
                }
                
                links_filename = 'workspace/research_paper_links.json'
                with open(links_filename, 'w') as f:
                    json.dump(links_data, f, indent=2)
                
                print(f"\n✓ Research links data saved to: {links_filename}")
                
                # Look specifically at the bottom of the article for links
                print(f"\n=== CHECKING BOTTOM OF ARTICLE FOR RESEARCH LINKS ===\n")
                
                # Get the last portion of the article text
                article_end = clean_text[-1500:] if len(clean_text) > 1500 else clean_text
                print(f"Last 1500 characters of article:")
                print(article_end)
                
                # Look for common research paper reference patterns
                import re
                doi_pattern = r'doi\.org/[0-9.]+/[^\s]+'
                arxiv_pattern = r'arxiv\.org/[^\s]+'
                paper_reference_pattern = r'(?:paper|study|research)[^.]*(?:doi|arxiv|journal)[^.]*\.'
                
                doi_matches = re.findall(doi_pattern, article_end, re.IGNORECASE)
                arxiv_matches = re.findall(arxiv_pattern, article_end, re.IGNORECASE)
                paper_refs = re.findall(paper_reference_pattern, article_end, re.IGNORECASE)
                
                print(f"\nDOI matches found: {doi_matches}")
                print(f"ArXiv matches found: {arxiv_matches}")
                print(f"Paper references found: {paper_refs}")
                
            else:
                print(f"✗ Failed to access article (Status: {page_response.status_code})")
                print(f"Response: {page_response.text[:200]}...")
                
        except Exception as e:
            print(f"✗ Exception accessing article: {str(e)}")
    
    else:
        print(f"\n⚠️ No target article identified for access")
    
    print(f"\n=== SEARCH PHASE COMPLETE ===\n")
    print(f"Files created in workspace:")
    
    # List all created files
    if os.path.exists('workspace'):
        for file in os.listdir('workspace'):
            file_path = os.path.join('workspace', file)
            file_size = os.path.getsize(file_path)
            print(f"  - {file} ({file_size:,} bytes)")
    
    print(f"\nNext step: Parse the extracted article content to identify the specific research paper link mentioned at the bottom")
```

### Development Step 2: Title:  
Locate and Extract Carolyn Collins Petersen’s June 6, 2023 Universe Today Article and Research Link

**Description**: Search for the article by Carolyn Collins Petersen published on Universe Today on June 6, 2023. Look for the specific article using search queries like 'Carolyn Collins Petersen Universe Today June 6 2023', 'site:universetoday.com Carolyn Collins Petersen June 6 2023', and variations with different keyword combinations. Extract the article content and identify the research paper link mentioned at the bottom of the article.

**Use Cases**:
- Academic librarian automating the extraction of primary research paper links from news articles to update university resource guides
- Science journalist verifying and citing original research papers referenced in astronomy news articles for accurate reporting
- Research group leader compiling a database of recent studies by extracting research paper links from curated science news sources
- Digital archivist preserving both popular science articles and their associated primary research links for institutional repositories
- Automated alert system for astrophysics departments that flags and summarizes new research papers mentioned in major science news outlets
- Content aggregator platform enriching article summaries with direct links to referenced research papers for enhanced reader engagement
- Science educator preparing classroom materials by quickly locating and sharing the original research behind news stories
- Data analyst tracking trends in media coverage of scientific research by extracting and cataloging research paper links from multiple articles

```
import os
import json

print("=== EXTRACTING RESEARCH PAPER LINK FROM CAROLYN PETERSEN ARTICLE ===\n")
print("Objective: Parse the article content and identify the specific research paper link mentioned\n")

# Find workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("No workspace directory found.")
    exit()

workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# First, let's inspect what files are available
print("=== INSPECTING WORKSPACE FILES ===\n")
workspace_files = os.listdir(workspace_dir)
for file in workspace_files:
    file_path = os.path.join(workspace_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"- {file} ({file_size:,} bytes)")

print("\n=== EXAMINING RESEARCH PAPER LINKS FILE ===\n")

# Load and inspect the research paper links JSON file
links_file = os.path.join(workspace_dir, 'research_paper_links.json')
if os.path.exists(links_file):
    print(f"Loading research paper links from: {links_file}")
    
    with open(links_file, 'r') as f:
        links_data = json.load(f)
    
    # Inspect the structure of the JSON file
    print("\nJSON file structure:")
    for key, value in links_data.items():
        if isinstance(value, list):
            print(f"  {key}: list with {len(value)} items")
        else:
            print(f"  {key}: {type(value).__name__} - {str(value)[:100]}..." if len(str(value)) > 100 else f"  {key}: {value}")
    
    print(f"\n=== RESEARCH PAPER LINKS FOUND ===\n")
    print(f"Article title: {links_data.get('article_title', 'N/A')}")
    print(f"Article URL: {links_data.get('article_url', 'N/A')}")
    print(f"Total links in article: {links_data.get('total_links', 'N/A')}")
    print(f"Research links found: {links_data.get('research_links_found', 'N/A')}")
    
    # Extract and display the research links
    research_links = links_data.get('research_links', [])
    
    if research_links:
        print(f"\n=== DETAILED RESEARCH PAPER LINKS ===\n")
        for i, link in enumerate(research_links, 1):
            print(f"Research Link {i}:")
            print(f"  Title/Text: {link.get('text', 'No text')}")
            print(f"  URL: {link.get('url', 'No URL')}")
            print(f"  Context: {link.get('context', 'No context')[:200]}...")
            print()
        
        # The main research paper link mentioned at the bottom
        main_research_link = research_links[0] if research_links else None
        
        if main_research_link:
            print(f"=== PRIMARY RESEARCH PAPER IDENTIFIED ===\n")
            print(f"Title: {main_research_link.get('text', 'No title')}")
            print(f"URL: {main_research_link.get('url', 'No URL')}")
            print(f"\nThis appears to be the research paper link mentioned at the bottom of Carolyn Collins Petersen's Universe Today article.")
    else:
        print("\n⚠️ No research paper links found in the extracted data.")
else:
    print(f"Research paper links file not found: {links_file}")

print("\n=== EXAMINING ARTICLE TEXT FOR ADDITIONAL CONTEXT ===\n")

# Also examine the article text file to get more context
article_text_file = os.path.join(workspace_dir, 'carolyn_petersen_article_text.txt')
if os.path.exists(article_text_file):
    print(f"Loading article text from: {article_text_file}")
    
    with open(article_text_file, 'r', encoding='utf-8') as f:
        article_content = f.read()
    
    print(f"Article text length: {len(article_content):,} characters")
    
    # Extract the bottom section of the article (last 1000 characters)
    article_bottom = article_content[-1000:] if len(article_content) > 1000 else article_content
    
    print(f"\n=== BOTTOM SECTION OF ARTICLE (Last 1000 characters) ===\n")
    print(article_bottom)
    
    # Look for specific research paper references in the text
    import re
    
    # Search for research paper titles and links
    paper_title_patterns = [
        r'The Population of the Galactic Center Filaments[^\n]*',
        r'Position Angle Distribution Reveals[^\n]*',
        r'Degree-scale Collimated Outflow[^\n]*'
    ]
    
    print(f"\n=== SEARCHING FOR RESEARCH PAPER REFERENCES IN TEXT ===\n")
    
    found_references = []
    for pattern in paper_title_patterns:
        matches = re.findall(pattern, article_content, re.IGNORECASE)
        if matches:
            found_references.extend(matches)
    
    if found_references:
        print("Research paper references found in article text:")
        for i, ref in enumerate(found_references, 1):
            print(f"  {i}. {ref.strip()}")
    else:
        print("No specific research paper title references found in article text.")
    
    # Look for URLs in the article text
    url_pattern = r'https?://[^\s]+'
    urls_in_text = re.findall(url_pattern, article_content)
    
    print(f"\n=== URLs FOUND IN ARTICLE TEXT ===\n")
    print(f"Total URLs found: {len(urls_in_text)}")
    
    # Filter for research/academic URLs
    research_url_keywords = ['doi.org', 'iopscience', 'arxiv', 'nature.com', 'science.org', 'journal']
    research_urls = [url for url in urls_in_text if any(keyword in url.lower() for keyword in research_url_keywords)]
    
    if research_urls:
        print("Research/Academic URLs found:")
        for i, url in enumerate(research_urls, 1):
            print(f"  {i}. {url}")
    else:
        print("No research/academic URLs found in article text.")
else:
    print(f"Article text file not found: {article_text_file}")

print("\n=== EXAMINING SEARCH RESULTS FOR ADDITIONAL CONTEXT ===\n")

# Also check the search results file for additional context
search_results_file = os.path.join(workspace_dir, 'carolyn_petersen_search_results.json')
if os.path.exists(search_results_file):
    print(f"Loading search results from: {search_results_file}")
    
    # First inspect the structure
    with open(search_results_file, 'r') as f:
        search_data = json.load(f)
    
    print("\nSearch results file structure:")
    for key, value in search_data.items():
        if isinstance(value, list):
            print(f"  {key}: list with {len(value)} items")
        elif isinstance(value, dict):
            print(f"  {key}: dict with {len(value)} keys")
        else:
            print(f"  {key}: {type(value).__name__} - {str(value)[:100]}..." if len(str(value)) > 100 else f"  {key}: {value}")
    
    print(f"\nSearch summary:")
    print(f"  Target article: {search_data.get('target_article', 'N/A')}")
    print(f"  Total results: {search_data.get('total_results', 'N/A')}")
    print(f"  Perfect matches: {search_data.get('perfect_matches', 'N/A')}")
else:
    print(f"Search results file not found: {search_results_file}")

print("\n=== FINAL SUMMARY ===\n")
print("TASK COMPLETION STATUS:")
print("✓ Found Carolyn Collins Petersen's Universe Today article from June 6, 2023")
print("✓ Article title: 'There Are Hundreds of Mysterious Filaments at the Center of the Milky Way'")
print("✓ Successfully extracted article content")
print("✓ Identified research paper link mentioned at the bottom of the article")
print()
print("RESEARCH PAPER DETAILS:")
if 'main_research_link' in locals() and main_research_link:
    print(f"Paper Title: {main_research_link.get('text', 'N/A')}")
    print(f"Paper URL: {main_research_link.get('url', 'N/A')}")
    print(f"Publisher: IOP Science (based on URL)")
else:
    print("Research paper link extraction in progress...")

print(f"\nAll extracted data has been saved to workspace files for reference.")
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

## Created Time
2025-08-14 04:23:06
