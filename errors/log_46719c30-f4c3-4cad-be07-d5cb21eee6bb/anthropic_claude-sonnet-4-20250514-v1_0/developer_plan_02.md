# Developer Plan 02

## Plan
Search for Pietro Murano's first published paper to identify the title of his earliest academic publication. Based on the previous research showing Pietro Murano had 21 prior publications before 2015 spanning from 2001-2014, focus on finding his very first paper from around 2001 or the earliest available publication. Search academic databases and publication records to identify the chronologically first paper authored by Pietro Murano, extracting the complete title of this inaugural publication.

## Description
This is the necessary next step because: (1) The previous research successfully identified that Pietro Murano was the author from the 2015 'Pie Menus or Linear Menus, Which Is Better?' paper who had prior publications (21 papers from 2001-2014), while Iram N. Khan had no clear prior publications, (2) The TASK specifically asks for the title of the first paper authored by the one that had authored prior papers, which is Pietro Murano, (3) Expected outcome is to identify the exact title of Pietro Murano's chronologically first academic publication, (4) This will complete the TASK by providing the specific title requested

## Episodic Examples
### Development Step 1: Determine Year David Sklar First Published Innovation Reports in Academic Medicine

**Description**: Search for information about David Sklar and Innovation Reports in Academic Medicine journal. Focus on finding the specific year when David Sklar first introduced or published Innovation Reports in this medical education publication. Use multiple search approaches: (1) Academic database searches for 'David Sklar Innovation Reports Academic Medicine', (2) PubMed searches combining these terms, (3) Google Scholar searches for relevant publications, (4) Direct searches of Academic Medicine journal archives. Extract publication dates, article titles, and verify the connection between David Sklar and the Innovation Reports concept.

**Use Cases**:
- Academic historian mapping the origin of “Innovation Reports” by David Sklar in Academic Medicine to contextualize a literature review on medical education advancements
- Medical librarian automating the extraction of publication dates and author metadata for David Sklar’s Innovation Reports to build a searchable institutional repository
- Curriculum developer analyzing the inception year of Innovation Reports for integrating historical innovation milestones into a medical education program syllabus
- Grant proposal writer validating the first appearance of Innovation Reports by David Sklar as evidence for funding a retrospective study on innovation diffusion in healthcare
- Bibliometric analyst systematically harvesting and verifying David Sklar’s publication timeline in Academic Medicine to conduct trend analysis on educational innovation research
- Science journalist investigating the debut of Innovation Reports in Academic Medicine to write a feature story on pioneers of medical education innovation
- Healthcare quality assessor auditing the historical publication record of Innovation Reports to ensure compliance with accreditation standards for innovation coursework

```
import os
import re
import requests
import json
from datetime import datetime

# Search for David Sklar and Innovation Reports in Academic Medicine journal
# Starting with a comprehensive search to find the first publication

query = 'David Sklar "Innovation Reports" "Academic Medicine" journal'
max_results = 20
type = "search"

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
    exit(1)

print(f"Searching for: {query}")
print(f"Max results: {max_results}")
print("=" * 60)

# Prepare API request parameters
params = {
    "q": query,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": max_results,
    "type": type
}

# Make API request to SerpAPI
response = requests.get("https://serpapi.com/search.json", params=params)

if response.status_code == 200:
    results = response.json()
    print("Search completed successfully!")
    print(f"Status: {response.status_code}")
    
    # Save raw results for analysis
    with open('workspace/david_sklar_innovation_reports_search_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\nRaw search results saved to: workspace/david_sklar_innovation_reports_search_results.json")
    
    # Process organic results
    if results.get("organic_results"):
        print(f"\nFound {len(results['organic_results'])} organic results:")
        print("=" * 60)
        
        for i, result in enumerate(results['organic_results'], 1):
            print(f"\nResult {i}:")
            print(f"Title: {result.get('title', 'N/A')}")
            print(f"Link: {result.get('link', 'N/A')}")
            print(f"Snippet: {result.get('snippet', 'N/A')}")
            print("-" * 40)
    
    # Extract and save relevant information
    relevant_results = []
    if results.get("organic_results"):
        for result in results['organic_results']:
            title_snippet = result.get('title', '').lower() + ' ' + result.get('snippet', '').lower()
            
            # Check for key terms
            if any(keyword in title_snippet for keyword in ['david sklar', 'innovation reports', 'academic medicine']):
                
                # Extract potential years from the result
                year_pattern = r'\b(19|20)\d{2}\b'
                years_found = re.findall(year_pattern, result.get('title', '') + ' ' + result.get('snippet', ''))
                
                # Calculate relevance score
                relevance_score = sum(1 for keyword in ['david sklar', 'innovation reports', 'academic medicine'] 
                                     if keyword in title_snippet)
                
                relevant_results.append({
                    'title': result.get('title', ''),
                    'link': result.get('link', ''),
                    'snippet': result.get('snippet', ''),
                    'years_found': years_found,
                    'relevance_score': relevance_score
                })
    
    # Sort by relevance
    relevant_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"\nFiltered {len(relevant_results)} relevant results:")
    print("=" * 60)
    
    for i, result in enumerate(relevant_results, 1):
        print(f"\nRelevant Result {i} (Relevance Score: {result['relevance_score']}):")
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Snippet: {result['snippet']}")
        if result['years_found']:
            print(f"Years found: {', '.join(result['years_found'])}")
        print("-" * 40)
    
    # Save filtered results
    with open('workspace/david_sklar_innovation_reports_relevant_results.json', 'w', encoding='utf-8') as f:
        json.dump(relevant_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nFiltered results saved to: workspace/david_sklar_innovation_reports_relevant_results.json")
    
else:
    print(f"Error: API request failed with status {response.status_code}: {response.text}")

print("\n" + "=" * 60)
print("SEARCH PHASE 1 COMPLETE")
print("=" * 60)
print("Next steps:")
print("1. Analyze the search results for specific publication dates")
print("2. Conduct additional targeted searches if needed")
print("3. Search Academic Medicine journal archives directly")
print("4. Look for PubMed citations")
```

### Development Step 4: Locate 1851 Atheistic Naturalism Phrenology Mesmerism Book and 2009 Reissuing Publisher

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- University research library digitization team using the multi-engine search script to locate and verify obscure 1851 scientific texts for digital archive inclusion and confirm 2009 reissue details.
- Historical society librarian employing automated Google Scholar, Bing, JSTOR, and archive.org queries to compile a complete bibliography of co-authored controversial phrenology and mesmerism treatises for a museum exhibition.
- Digital humanities scholar mapping the spread of atheistic naturalism by systematically harvesting primary sources and modern reprint information from multiple search engines for network analysis.
- Rare bookseller validating a potential 1851 first edition’s provenance by cross-referencing academic databases and general web searches to confirm authorship, publication history, and a 2009 specialty press reissue.
- PhD candidate in history of science leveraging the Python multi-method search to uncover mid-19th century philosophical works on phrenology and mesmerism across library catalogs and online archives for dissertation research.
- Independent publisher’s research team discovering forgotten public domain texts for annotated reissues by scanning academic sites and search engines to identify obscure co-authored volumes and track modern rights holders.
- Data journalist investigating the revival of fringe-science publications by extracting publication metadata and reissue patterns from search logs to illustrate how 19th-century controversial works reappear in contemporary niche markets.

```
import os
import requests
import json
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

print('=== ALTERNATIVE SEARCH STRATEGY FOR 1851 ATHEISTIC NATURALISM BOOK ===')
print('Previous attempts failed due to API rate limits (SERPAPI) and HTTP 202 responses (DuckDuckGo)')
print('Implementing multi-pronged approach with different search engines and methods\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Initialize comprehensive results storage
search_results = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'objective': 'Find 1851 co-authored book on atheistic naturalism with phrenology/mesmerism, reissued 2009',
    'search_methods': [],
    'all_findings': [],
    'book_candidates': [],
    'analysis_summary': {}
}

print('TARGET BOOK CHARACTERISTICS:')
print('• Published: 1851')
print('• Co-authored (multiple authors)')
print('• Topic: Atheistic naturalism')
print('• Contains: Phrenology and mesmerism content')
print('• Controversial for these topics')
print('• Reissued by a publisher in 2009')
print()

# Method 1: Try Google Scholar search using requests
print('=== METHOD 1: GOOGLE SCHOLAR DIRECT SEARCH ===')
print('=' * 60)

scholar_queries = [
    '"atheistic naturalism" 1851 phrenology mesmerism',
    '1851 controversial book phrenology mesmerism authors',
    'phrenology mesmerism 1851 naturalism philosophy'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

for i, query in enumerate(scholar_queries, 1):
    print(f'\nGoogle Scholar Search {i}: {query}')
    try:
        scholar_url = f'https://scholar.google.com/scholar?q={quote_plus(query)}'
        print(f'URL: {scholar_url}')
        
        response = requests.get(scholar_url, headers=headers, timeout=20)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML
            filename = f'google_scholar_search_{i}.html'
            filepath = os.path.join('workspace', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f'Saved: {filepath}')
            
            # Quick parse for academic results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result titles in Google Scholar
            result_titles = soup.find_all(['h3', 'a'], class_=lambda x: x and 'gs_rt' in str(x))
            if not result_titles:
                result_titles = soup.find_all('h3')
            
            print(f'Found {len(result_titles)} potential results')
            
            for j, title_elem in enumerate(result_titles[:5], 1):
                title_text = title_elem.get_text().strip()
                if len(title_text) > 10:
                    print(f'  {j}. {title_text[:100]}...')
                    
                    # Check for key terms
                    text_lower = title_text.lower()
                    relevance_indicators = []
                    if '1851' in text_lower: relevance_indicators.append('1851')
                    if 'phrenology' in text_lower: relevance_indicators.append('phrenology')
                    if 'mesmerism' in text_lower: relevance_indicators.append('mesmerism')
                    if 'naturalism' in text_lower: relevance_indicators.append('naturalism')
                    
                    if relevance_indicators:
                        print(f'     ⭐ Relevant terms: {', '.join(relevance_indicators)}')
                        search_results['all_findings'].append({
                            'source': 'Google Scholar',
                            'query': query,
                            'title': title_text,
                            'relevance_terms': relevance_indicators,
                            'method': 'scholar_direct'
                        })
            
            search_results['search_methods'].append(f'Google Scholar: {query} - Status {response.status_code}')
        else:
            print(f'Failed with status {response.status_code}')
            
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)  # Rate limiting

# Method 2: Try Bing search
print('\n=== METHOD 2: BING SEARCH ===')
print('=' * 40)

bing_queries = [
    '"1851" "atheistic naturalism" phrenology mesmerism book',
    '1851 controversial phrenology mesmerism co-authored book',
    'phrenology mesmerism 1851 naturalism reissued 2009'
]

for i, query in enumerate(bing_queries, 1):
    print(f'\nBing Search {i}: {query}')
    try:
        bing_url = f'https://www.bing.com/search?q={quote_plus(query)}'
        print(f'URL: {bing_url}')
        
        response = requests.get(bing_url, headers=headers, timeout=20)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML
            filename = f'bing_search_{i}.html'
            filepath = os.path.join('workspace', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f'Saved: {filepath}')
            
            # Parse for results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for Bing result titles
            result_links = soup.find_all('a', href=True)
            relevant_results = []
            
            for link in result_links:
                link_text = link.get_text().strip()
                href = link.get('href')
                
                if len(link_text) > 15 and href:
                    text_lower = link_text.lower()
                    relevance_score = 0
                    matched_terms = []
                    
                    key_terms = {'1851': 3, 'phrenology': 2, 'mesmerism': 2, 'naturalism': 2, 'atheistic': 2, 'book': 1}
                    
                    for term, weight in key_terms.items():
                        if term in text_lower:
                            relevance_score += weight
                            matched_terms.append(term)
                    
                    if relevance_score >= 3:
                        relevant_results.append({
                            'text': link_text[:150],
                            'href': href,
                            'score': relevance_score,
                            'terms': matched_terms
                        })
            
            print(f'Found {len(relevant_results)} relevant results')
            for j, result in enumerate(relevant_results[:3], 1):
                print(f'  {j}. Score {result["score"]}: {result["text"]}...')
                print(f'     Terms: {', '.join(result["terms"])}')
                
                search_results['all_findings'].append({
                    'source': 'Bing',
                    'query': query,
                    'title': result['text'],
                    'link': result['href'],
                    'relevance_score': result['score'],
                    'relevance_terms': result['terms'],
                    'method': 'bing_direct'
                })
            
            search_results['search_methods'].append(f'Bing: {query} - Status {response.status_code}')
        else:
            print(f'Failed with status {response.status_code}')
            
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)  # Rate limiting

# Method 3: Try specific academic database searches
print('\n=== METHOD 3: ACADEMIC DATABASE SEARCHES ===')
print('=' * 50)

# Try JSTOR, Project MUSE, and other academic sources
academic_sites = [
    'site:jstor.org',
    'site:muse.jhu.edu', 
    'site:archive.org',
    'site:hathitrust.org'
]

base_query = '1851 atheistic naturalism phrenology mesmerism'

for i, site in enumerate(academic_sites, 1):
    query = f'{site} {base_query}'
    print(f'\nAcademic Search {i}: {query}')
    
    try:
        # Use Google to search specific academic sites
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        print(f'URL: {google_url}')
        
        response = requests.get(google_url, headers=headers, timeout=20)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            filename = f'academic_search_{i}_{site.replace("site:", "").replace(".", "_")}.html'
            filepath = os.path.join('workspace', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f'Saved: {filepath}')
            
            # Quick analysis
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for Google result snippets
            snippets = soup.find_all(['span', 'div'], class_=lambda x: x and 'st' in str(x).lower())
            
            relevant_snippets = []
            for snippet in snippets:
                snippet_text = snippet.get_text().strip()
                if len(snippet_text) > 20:
                    text_lower = snippet_text.lower()
                    if any(term in text_lower for term in ['1851', 'phrenology', 'mesmerism', 'naturalism']):
                        relevant_snippets.append(snippet_text[:200])
            
            print(f'Found {len(relevant_snippets)} relevant snippets')
            for j, snippet in enumerate(relevant_snippets[:2], 1):
                print(f'  {j}. {snippet}...')
                
                search_results['all_findings'].append({
                    'source': f'Academic - {site}',
                    'query': query,
                    'snippet': snippet,
                    'method': 'academic_site_search'
                })
            
            search_results['search_methods'].append(f'Academic {site}: Status {response.status_code}')
        else:
            print(f'Failed with status {response.status_code}')
            
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(4)  # Longer delay for Google

# Method 4: Try alternative search engines
print('\n=== METHOD 4: ALTERNATIVE SEARCH ENGINES ===')
print('=' * 50)

# Try Startpage (uses Google results but with privacy)
startpage_query = '"1851" phrenology mesmerism atheistic naturalism book'
print(f'\nStartpage Search: {startpage_query}')

try:
    startpage_url = f'https://www.startpage.com/sp/search?query={quote_plus(startpage_query)}'
    print(f'URL: {startpage_url}')
    
    response = requests.get(startpage_url, headers=headers, timeout=20)
    print(f'Status: {response.status_code}')
    
    if response.status_code == 200:
        filename = 'startpage_search.html'
        filepath = os.path.join('workspace', filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f'Saved: {filepath}')
        
        search_results['search_methods'].append(f'Startpage: Status {response.status_code}')
    else:
        print(f'Failed with status {response.status_code}')
        
except Exception as e:
    print(f'Error: {str(e)}')

# Analyze all findings
print('\n' + '=' * 80)
print('COMPREHENSIVE ANALYSIS OF ALL SEARCH METHODS')
print('=' * 80)

total_findings = len(search_results['all_findings'])
print(f'Total findings collected: {total_findings}')
print(f'Search methods attempted: {len(search_results["search_methods"])}')

if search_results['all_findings']:
    print('\n🔍 ALL FINDINGS ANALYSIS:')
    print('-' * 40)
    
    # Group by source
    by_source = {}
    for finding in search_results['all_findings']:
        source = finding['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(finding)
    
    for source, findings in by_source.items():
        print(f'\n{source} ({len(findings)} findings):')
        for i, finding in enumerate(findings, 1):
            title = finding.get('title', finding.get('snippet', 'No title'))[:100]
            terms = finding.get('relevance_terms', [])
            score = finding.get('relevance_score', 'N/A')
            print(f'  {i}. {title}... (Score: {score}, Terms: {", ".join(terms)})')
    
    # Identify potential book candidates
    book_indicators = ['book', 'work', 'treatise', 'publication', 'volume']
    year_indicators = ['1851']
    topic_indicators = ['phrenology', 'mesmerism', 'naturalism', 'atheistic']
    
    for finding in search_results['all_findings']:
        text_content = (finding.get('title', '') + ' ' + finding.get('snippet', '')).lower()
        
        has_book = any(indicator in text_content for indicator in book_indicators)
        has_year = any(indicator in text_content for indicator in year_indicators)
        has_topic = any(indicator in text_content for indicator in topic_indicators)
        
        if has_book and has_year and has_topic:
            search_results['book_candidates'].append(finding)
    
    print(f'\n📚 POTENTIAL BOOK CANDIDATES: {len(search_results["book_candidates"])}')
    for i, candidate in enumerate(search_results['book_candidates'], 1):
        print(f'\n{i}. Source: {candidate["source"]}')
        print(f'   Title/Snippet: {candidate.get("title", candidate.get("snippet", "No content"))[:150]}...')
        print(f'   Terms: {candidate.get("relevance_terms", [])}')
        print(f'   Score: {candidate.get("relevance_score", "N/A")}')

else:
    print('\n❌ No findings collected from any search method')
    print('This suggests the book may be:')
    print('1. Very obscure or not well-digitized')
    print('2. Known by a different title or description')
    print('3. Not matching our exact search terms')

# Save comprehensive results
results_file = os.path.join('workspace', 'comprehensive_1851_book_search.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE SEARCH RESULTS SAVED TO: {results_file}')

# Summary statistics
search_results['analysis_summary'] = {
    'total_findings': total_findings,
    'book_candidates': len(search_results['book_candidates']),
    'search_methods_attempted': len(search_results['search_methods']),
    'successful_searches': len([m for m in search_results['search_methods'] if '200' in m]),
    'sources_used': list(set([f['source'] for f in search_results['all_findings']])) if search_results['all_findings'] else []
}

print(f'\n📊 FINAL SEARCH STATISTICS:')
print(f'   • Total findings: {search_results["analysis_summary"]["total_findings"]}')
print(f'   • Book candidates: {search_results["analysis_summary"]["book_candidates"]}')
print(f'   • Methods attempted: {search_results["analysis_summary"]["search_methods_attempted"]}')
print(f'   • Successful searches: {search_results["analysis_summary"]["successful_searches"]}')
print(f'   • Sources accessed: {search_results["analysis_summary"]["sources_used"]}')

print('\n🎯 RECOMMENDED NEXT STEPS:')
if search_results['book_candidates']:
    print('1. ✅ Investigate specific book candidates found')
    print('2. ✅ Follow up on promising links and sources')
    print('3. ✅ Search for 2009 reissue information')
else:
    print('1. 🔄 Try more specific author name searches')
    print('2. 🔄 Search for "controversial 1851 books" generally')
    print('3. 🔄 Look into 19th century philosophy/science book catalogs')
    print('4. 🔄 Search academic databases for phrenology/mesmerism history')

print('5. 📋 Review all saved HTML files for additional context')
print('6. 🔍 Consider library catalog searches (WorldCat, etc.)')

print('\n=== COMPREHENSIVE MULTI-METHOD SEARCH COMPLETE ===')
```

### Development Step 2: Identify Year David Sklar Introduced Innovation Reports Section in Academic Medicine Journal

**Description**: Search for information about David Sklar and Innovation Reports in Academic Medicine journal. Use multiple search approaches: (1) Direct search for 'David Sklar Innovation Reports Academic Medicine journal', (2) Search Academic Medicine journal archives or database for articles by David Sklar, (3) Search for 'Innovation Reports Academic Medicine introduction year', (4) Look for historical information about when Innovation Reports section was established in Academic Medicine. Focus on identifying the specific year when David Sklar introduced or established the Innovation Reports feature in this medical journal.

**Use Cases**:
- Competitive intelligence for product teams: parse search engine results and press release archives to pinpoint the exact year a rival company introduced a flagship feature, enabling data-driven roadmap planning.
- Academic editorial research: mine online journal archives and search metadata to determine when a specific section (e.g., “Case Studies”) was first established and credit the founding editor with publication details.
- Legal compliance tracking: analyze government websites and legal databases to extract the enactment year of a new regulation by detecting keywords like “enacted” or “established” in legal snippets.
- Patent analytics for R&D: aggregate patent office search results and automatically extract filing and grant years for key inventions in a target technology domain, ranking them by relevance.
- Marketing campaign monitoring: search news aggregators and corporate blogs to identify the introduction date of a major brand slogan or sustainability initiative, capturing launch year and source URLs.
- Public policy timeline building: scrape WHO, CDC, and other public health agency archives to confirm the publication year of critical guidelines, filtering for “published” or “launched” mentions in the text.
- Technical standards research: gather search results from ISO, IEEE, and industry consortium websites to establish when a new communication protocol or best practice standard was first released.
- Corporate heritage documentation: compile internal communications, annual reports, and press coverage to verify the inception year of a company’s flagship community outreach program, extracting evidence and timestamps.

```
import json
import re
from datetime import datetime

# Load the search results data
with open('workspace/david_sklar_innovation_reports_search_results.json', 'r') as f:
    search_data = json.load(f)

print("=" * 80)
print("ANALYZING SEARCH RESULTS FOR DAVID SKLAR INNOVATION REPORTS IN ACADEMIC MEDICINE")
print("=" * 80)

# Initialize our findings
key_findings = []
year_mentions = []
publication_details = {}

# Helper function to extract years from text
def extract_years(text):
    years = re.findall(r'\b(20\d{2})\b', text)
    return [int(year) for year in years]

# Helper function to check for Innovation Reports mentions
def contains_innovation_reports(text):
    return 'innovation reports' in text.lower()

# Helper function to check for David Sklar mentions
def contains_david_sklar(text):
    return 'david sklar' in text.lower() or 'david p. sklar' in text.lower() or 'david p sklar' in text.lower()

# Analyze each search category for key information
for category, data in search_data.items():
    print(f"\n{'='*20} ANALYZING {category.upper()} {'='*20}")
    
    if 'organic_results' in data:
        results = data['organic_results']
        
        for i, result in enumerate(results):
            title = result.get('title', '')
            snippet = result.get('snippet', '')
            url = result.get('link', '')
            
            combined_text = f"{title} {snippet}"
            
            # Check if this result mentions Innovation Reports AND David Sklar
            has_innovation_reports = contains_innovation_reports(combined_text)
            has_david_sklar = contains_david_sklar(combined_text)
            years_found = extract_years(combined_text)
            
            # Special attention to results that mention both key terms
            if has_innovation_reports and has_david_sklar:
                finding = {
                    'category': category,
                    'title': title,
                    'url': url,
                    'snippet': snippet,
                    'years_mentioned': years_found,
                    'relevance_score': 10  # Highest relevance
                }
                key_findings.append(finding)
                
                print(f"\n*** HIGH RELEVANCE RESULT {i+1} ***")
                print(f"Title: {title}")
                print(f"URL: {url}")
                print(f"Years mentioned: {years_found}")
                print(f"Snippet: {snippet}")
                
                # Extract specific year information from snippet
                if '2013' in snippet and 'introduced' in snippet.lower():
                    year_mentions.append({
                        'year': 2013,
                        'source': category,
                        'evidence': snippet,
                        'url': url
                    })
            
            # Also check for results with Innovation Reports or David Sklar (but not necessarily both)
            elif has_innovation_reports or has_david_sklar:
                if years_found:  # Only include if years are mentioned
                    finding = {
                        'category': category,
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'years_mentioned': years_found,
                        'relevance_score': 5  # Medium relevance
                    }
                    key_findings.append(finding)

# Now let's identify the specific year and evidence
print("\n" + "=" * 80)
print("KEY FINDINGS ANALYSIS: WHEN DID DAVID SKLAR INTRODUCE INNOVATION REPORTS?")
print("=" * 80)

# Look for specific evidence about the introduction year
introduction_evidence = []

for finding in key_findings:
    snippet = finding['snippet'].lower()
    
    # Look for specific phrases that indicate introduction/establishment
    if any(phrase in snippet for phrase in ['introduced', 'established', 'began', 'started', 'launched']):
        if 'innovation reports' in snippet and 'david sklar' in snippet:
            introduction_evidence.append({
                'year_mentioned': finding['years_mentioned'],
                'evidence': finding['snippet'],
                'source_category': finding['category'],
                'url': finding['url'],
                'title': finding['title']
            })

# Analyze the most definitive evidence
print("\nDEFINITIVE EVIDENCE FOR INTRODUCTION YEAR:")
print("-" * 60)

confirmed_year = None
best_evidence = None

for evidence in introduction_evidence:
    print(f"\nEvidence from {evidence['source_category']}:")
    print(f"Years mentioned: {evidence['year_mentioned']}")
    print(f"Title: {evidence['title']}")
    print(f"Evidence text: {evidence['evidence']}")
    print(f"Source URL: {evidence['url']}")
    
    # Check for the most specific evidence
    if '2013' in str(evidence['year_mentioned']) and 'introduced' in evidence['evidence'].lower():
        if 'innovation reports were introduced in academic medicine in 2013 by david sklar' in evidence['evidence'].lower():
            confirmed_year = 2013
            best_evidence = evidence
            print("*** THIS IS THE DEFINITIVE ANSWER ***")

# Additional analysis from year mentions
if year_mentions:
    print("\n" + "-" * 60)
    print("YEAR MENTIONS SUMMARY:")
    print("-" * 60)
    
    for mention in year_mentions:
        print(f"Year: {mention['year']}")
        print(f"Source: {mention['source']}")
        print(f"Evidence: {mention['evidence']}")
        print(f"URL: {mention['url']}")
        print()

# Final conclusion
print("\n" + "=" * 80)
print("FINAL ANSWER: WHEN DID DAVID SKLAR INTRODUCE INNOVATION REPORTS?")
print("=" * 80)

if confirmed_year:
    print(f"\n*** CONFIRMED ANSWER: {confirmed_year} ***")
    print("\nEvidence:")
    print(f"- Title: {best_evidence['title']}")
    print(f"- Source: Academic Medicine journal website")
    print(f"- Specific quote: '{best_evidence['evidence']}'")
    print(f"- URL: {best_evidence['url']}")
else:
    # Analyze patterns in the findings
    all_years = []
    for finding in key_findings:
        all_years.extend(finding['years_mentioned'])
    
    if all_years:
        from collections import Counter
        year_counts = Counter(all_years)
        most_common_year = year_counts.most_common(1)[0] if year_counts else None
        
        print(f"\nBased on search result analysis:")
        print(f"Most frequently mentioned year: {most_common_year[0] if most_common_year else 'Not found'}")
        print(f"Frequency: {most_common_year[1] if most_common_year else 0} mentions")
        print(f"All years mentioned: {sorted(set(all_years))}")

# Save comprehensive analysis results
analysis_results = {
    'analysis_date': datetime.now().isoformat(),
    'confirmed_year': confirmed_year,
    'best_evidence': best_evidence,
    'total_key_findings': len(key_findings),
    'introduction_evidence_count': len(introduction_evidence),
    'year_mentions': year_mentions,
    'search_categories_analyzed': list(search_data.keys()),
    'conclusion': f"David Sklar introduced Innovation Reports in Academic Medicine in {confirmed_year}" if confirmed_year else "Year not definitively confirmed from search results"
}

with open('workspace/david_sklar_innovation_reports_analysis.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)

print(f"\n{'-'*60}")
print(f"ANALYSIS COMPLETE")
print(f"Total key findings analyzed: {len(key_findings)}")
print(f"Analysis results saved to: workspace/david_sklar_innovation_reports_analysis.json")
print(f"Analysis completed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if confirmed_year:
    print(f"\n🎯 MISSION ACCOMPLISHED: David Sklar introduced Innovation Reports in Academic Medicine in {confirmed_year}")
else:
    print(f"\n⚠️  Additional research may be needed to confirm the exact year")
```

### Development Step 1: Identify Year David Sklar Introduced Innovation Reports Section in Academic Medicine Journal

**Description**: Search for information about David Sklar and Innovation Reports in Academic Medicine journal. Use multiple search approaches: (1) Direct search for 'David Sklar Innovation Reports Academic Medicine journal', (2) Search Academic Medicine journal archives or database for articles by David Sklar, (3) Search for 'Innovation Reports Academic Medicine introduction year', (4) Look for historical information about when Innovation Reports section was established in Academic Medicine. Focus on identifying the specific year when David Sklar introduced or established the Innovation Reports feature in this medical journal.

**Use Cases**:
- Medical historian tracing the exact year David Sklar launched the Innovation Reports section in Academic Medicine for a publication on editorial evolution
- Journal editor benchmarking competitor features by extracting launch dates and context of Innovation Reports in peer medical journals
- Research assistant automating the collection of archival metadata to build a timeline of new section introductions across Academic Medicine issues
- Medical educator preparing a lecture module on how and when key innovation-focused sections were added to leading medical education journals
- Academic librarian verifying feature histories in journal collection development, ensuring accurate catalog records of new editorial sections
- Publishing strategist analyzing past journal feature rollouts, using scraped search results to inform the launch plan for a new innovation column
- Data analyst conducting a meta-research project on trends in academic journal innovations, automating multi-step web searches for reliable timelines

```
import os
import requests
import json
from time import sleep

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
    exit()

# Initialize results storage
all_search_results = {}

# Search approach 1: Direct search for 'David Sklar Innovation Reports Academic Medicine journal'
print("=" * 80)
print("SEARCH 1: Direct search for David Sklar Innovation Reports Academic Medicine journal")
print("=" * 80)

query1 = "David Sklar Innovation Reports Academic Medicine journal"
params1 = {
    "q": query1,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": 15,
    "type": "search"
}

response1 = requests.get("https://serpapi.com/search.json", params=params1)

if response1.status_code == 200:
    results1 = response1.json()
    all_search_results['direct_search'] = results1
    
    if results1.get("organic_results"):
        print(f"Found {len(results1['organic_results'])} results for direct search:")
        for i, result in enumerate(results1['organic_results'][:10]):
            print(f"\n{i+1}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No URL')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')}")
    else:
        print("No organic results found for direct search")
else:
    print(f"Error in direct search: {response1.status_code} - {response1.text}")

# Small delay between requests
sleep(1)

# Search approach 2: Academic Medicine journal archives for David Sklar articles
print("\n" + "=" * 80)
print("SEARCH 2: Academic Medicine journal David Sklar articles")
print("=" * 80)

query2 = "Academic Medicine journal David Sklar articles archives"
params2 = {
    "q": query2,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": 15,
    "type": "search"
}

response2 = requests.get("https://serpapi.com/search.json", params=params2)

if response2.status_code == 200:
    results2 = response2.json()
    all_search_results['academic_medicine_search'] = results2
    
    if results2.get("organic_results"):
        print(f"Found {len(results2['organic_results'])} results for Academic Medicine search:")
        for i, result in enumerate(results2['organic_results'][:10]):
            print(f"\n{i+1}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No URL')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')}")
    else:
        print("No organic results found for Academic Medicine search")
else:
    print(f"Error in Academic Medicine search: {response2.status_code} - {response2.text}")

# Small delay between requests
sleep(1)

# Search approach 3: Innovation Reports Academic Medicine introduction year
print("\n" + "=" * 80)
print("SEARCH 3: Innovation Reports Academic Medicine introduction year")
print("=" * 80)

query3 = "Innovation Reports Academic Medicine introduction year established when started"
params3 = {
    "q": query3,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": 15,
    "type": "search"
}

response3 = requests.get("https://serpapi.com/search.json", params=params3)

if response3.status_code == 200:
    results3 = response3.json()
    all_search_results['innovation_reports_year_search'] = results3
    
    if results3.get("organic_results"):
        print(f"Found {len(results3['organic_results'])} results for Innovation Reports year search:")
        for i, result in enumerate(results3['organic_results'][:10]):
            print(f"\n{i+1}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No URL')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')}")
    else:
        print("No organic results found for Innovation Reports year search")
else:
    print(f"Error in Innovation Reports year search: {response3.status_code} - {response3.text}")

# Small delay between requests
sleep(1)

# Search approach 4: Historical information about Innovation Reports section establishment
print("\n" + "=" * 80)
print("SEARCH 4: Academic Medicine Innovation Reports section history establishment")
print("=" * 80)

query4 = "Academic Medicine journal Innovation Reports section history David Sklar editor"
params4 = {
    "q": query4,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": 15,
    "type": "search"
}

response4 = requests.get("https://serpapi.com/search.json", params=params4)

if response4.status_code == 200:
    results4 = response4.json()
    all_search_results['innovation_reports_history_search'] = results4
    
    if results4.get("organic_results"):
        print(f"Found {len(results4['organic_results'])} results for Innovation Reports history search:")
        for i, result in enumerate(results4['organic_results']):
            print(f"\n{i+1}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No URL')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')}")
    else:
        print("No organic results found for Innovation Reports history search")
else:
    print(f"Error in Innovation Reports history search: {response4.status_code} - {response4.text}")

# Small delay between requests
sleep(1)

# Search approach 5: More specific search with site restriction for Academic Medicine journal
print("\n" + "=" * 80)
print("SEARCH 5: Site-specific search on Academic Medicine journal website")
print("=" * 80)

query5 = "site:journals.lww.com David Sklar Innovation Reports Academic Medicine"
params5 = {
    "q": query5,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": 15,
    "type": "search"
}

response5 = requests.get("https://serpapi.com/search.json", params=params5)

if response5.status_code == 200:
    results5 = response5.json()
    all_search_results['site_specific_search'] = results5
    
    if results5.get("organic_results"):
        print(f"Found {len(results5['organic_results'])} results for site-specific search:")
        for i, result in enumerate(results5['organic_results']):
            print(f"\n{i+1}. {result.get('title', 'No title')}")
            print(f"   URL: {result.get('link', 'No URL')}")
            print(f"   Snippet: {result.get('snippet', 'No snippet')}")
    else:
        print("No organic results found for site-specific search")
else:
    print(f"Error in site-specific search: {response5.status_code} - {response5.text}")

# Save all search results to workspace for further analysis
with open('workspace/david_sklar_innovation_reports_search_results.json', 'w') as f:
    json.dump(all_search_results, f, indent=2)

print("\n" + "=" * 80)
print("SEARCH SUMMARY")
print("=" * 80)
print(f"Completed 5 different search approaches:")
print(f"1. Direct search: {'✓' if 'direct_search' in all_search_results else '✗'}")
print(f"2. Academic Medicine journal: {'✓' if 'academic_medicine_search' in all_search_results else '✗'}")
print(f"3. Innovation Reports year: {'✓' if 'innovation_reports_year_search' in all_search_results else '✗'}")
print(f"4. Innovation Reports history: {'✓' if 'innovation_reports_history_search' in all_search_results else '✗'}")
print(f"5. Site-specific search: {'✓' if 'site_specific_search' in all_search_results else '✗'}")
print(f"\nAll search results saved to: workspace/david_sklar_innovation_reports_search_results.json")
print(f"Next step: Analyze results to identify the specific year when David Sklar introduced Innovation Reports in Academic Medicine journal")
```

### Development Step 3: Identify 1851 Co-Authored Atheistic Naturalism Book on Phrenology and Mesmerism Reissued in 2009

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- Historical research for a university scholar investigating 19th-century atheist naturalism and pseudoscientific literature: use targeted web scraping queries to locate obscure co-authored works and their modern reprints.
- Digital humanities project mapping the evolution of pseudoscience: automate extraction of publication details on phrenology and mesmerism works from library catalogs and 2009 reissue records.
- Publisher rights-clearance team verifying public-domain status and reissue history for a niche 1851 philosophical text before negotiating a new edition.
- Rare-bookseller inventory enrichment by scraping auction sites and institutional repositories to confirm provenance, edition details, and modern reprints of a controversial treatise.
- Museum exhibit curator compiling metadata on fringe scientific movements: extract original publication data and modern publisher information for exhibit catalogs and digital displays.
- Intellectual property lawyer assembling evidence on historical publication dates and reissue claims to advise on copyright expiration and public-domain eligibility for atheistic naturalism texts.
- Open-knowledge platform contributor populating a bibliographic database with accurate 1851 publication and 2009 reissue details of co-authored works on phrenology and mesmerism.
- Genealogist tracing co-authors’ biographies by retrieving original 1851 publication records and 2009 publisher information to enrich family-history profiles.

```
import os
import requests
import json
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

print('=== CORRECTED DIRECT WEB SEARCH FOR 1851 ATHEISTIC NATURALISM BOOK ===')
print('Fixing syntax errors from previous attempt and executing comprehensive search\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Define targeted search queries focusing on the most specific combinations
search_queries = [
    '"atheistic naturalism" 1851 phrenology mesmerism book',
    '1851 controversial book phrenology mesmerism co-authored',
    'phrenology mesmerism 1851 naturalism philosophy book',
    '1851 atheism phrenology mesmerism publication authors',
    'controversial 1851 book naturalism phrenology reissued 2009'
]

print(f'Executing {len(search_queries)} targeted searches using direct web scraping:')
for i, query in enumerate(search_queries, 1):
    print(f'  {i}. {query}')

# Headers for web requests to avoid blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Initialize results storage
all_results = {
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'method': 'Direct web scraping (DuckDuckGo)',
    'objective': 'Find 1851 co-authored book on atheistic naturalism with phrenology/mesmerism, reissued 2009',
    'queries': search_queries,
    'results': [],
    'potential_books': [],
    'analysis': {}
}

print('\n=== EXECUTING DUCKDUCKGO SEARCHES ===')
print('=' * 60)

# Function to extract and analyze search results
def analyze_search_content(html_content, query):
    """Extract and analyze search results from HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find result containers (DuckDuckGo specific)
    results = []
    
    # Look for various result container patterns
    result_containers = soup.find_all(['div', 'article'], class_=lambda x: x and any(term in str(x).lower() for term in ['result', 'web-result', 'links_main']))
    
    if not result_containers:
        # Fallback: look for any links that might be results
        result_containers = soup.find_all('a', href=True)
    
    for container in result_containers[:15]:  # Limit to first 15 results
        try:
            # Extract title
            title_elem = container.find(['h2', 'h3', 'a']) or container
            title = title_elem.get_text().strip() if title_elem else 'No title'
            
            # Extract link
            link_elem = container.find('a', href=True) or (container if container.name == 'a' else None)
            link = link_elem.get('href') if link_elem else 'No link'
            
            # Extract snippet/description
            snippet_elem = container.find(['p', 'span', 'div'], class_=lambda x: x and 'snippet' in str(x).lower()) or container.find('p')
            snippet = snippet_elem.get_text().strip() if snippet_elem else 'No snippet'
            
            # Skip if no meaningful content
            if len(title) < 5 or title == 'No title':
                continue
                
            # Calculate relevance score
            combined_text = f'{title} {snippet} {link}'.lower()
            
            relevance_score = 0
            matched_terms = []
            
            key_terms = {
                '1851': 5,
                'atheistic': 3,
                'naturalism': 3,
                'phrenology': 3,
                'mesmerism': 3,
                'co-authored': 2,
                'controversial': 2,
                '2009': 2,
                'reissued': 2,
                'book': 1,
                'publication': 1,
                'philosophy': 1,
                'atheism': 2
            }
            
            for term, weight in key_terms.items():
                if term in combined_text:
                    relevance_score += weight
                    matched_terms.append(term)
            
            if relevance_score > 0:  # Only include results with some relevance
                results.append({
                    'title': title[:200],
                    'link': link,
                    'snippet': snippet[:300],
                    'relevance_score': relevance_score,
                    'matched_terms': matched_terms,
                    'query': query
                })
                
        except Exception as e:
            continue  # Skip problematic results
    
    return results

# Execute DuckDuckGo searches
for i, query in enumerate(search_queries, 1):
    print(f'\nDuckDuckGo Search {i}/{len(search_queries)}: {query}')
    print('-' * 50)
    
    try:
        # Construct DuckDuckGo search URL
        search_url = f'https://html.duckduckgo.com/html/?q={quote_plus(query)}'
        
        print(f'Requesting: {search_url}')
        response = requests.get(search_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print(f'✅ Successfully retrieved search results (Status: {response.status_code})')
            
            # Save raw HTML for reference
            html_filename = f'duckduckgo_search_{i}_{query.replace(" ", "_")[:30]}.html'
            html_filepath = os.path.join('workspace', html_filename)
            
            with open(html_filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Raw HTML saved to: {html_filepath}')
            
            # Analyze search results
            search_results = analyze_search_content(response.text, query)
            
            print(f'Extracted {len(search_results)} relevant results')
            
            # Display high-relevance results
            high_relevance = [r for r in search_results if r['relevance_score'] >= 5]
            moderate_relevance = [r for r in search_results if 3 <= r['relevance_score'] < 5]
            
            if high_relevance:
                print(f'\n🎯 HIGH RELEVANCE RESULTS ({len(high_relevance)}):')
                for j, result in enumerate(high_relevance, 1):
                    print(f'  {j}. Score: {result["relevance_score"]} | {result["title"]}')
                    print(f'     Terms: {", ".join(result["matched_terms"])}')
                    print(f'     Link: {result["link"]}')
                    print(f'     Snippet: {result["snippet"][:150]}...')
                    print()
            
            if moderate_relevance:
                print(f'\n⭐ MODERATE RELEVANCE RESULTS ({len(moderate_relevance)}):')
                for j, result in enumerate(moderate_relevance[:3], 1):  # Show top 3
                    print(f'  {j}. Score: {result["relevance_score"]} | {result["title"][:80]}...')
                    print(f'     Terms: {", ".join(result["matched_terms"])}')
            
            # Store results
            all_results['results'].extend(search_results)
            
            # Identify potential book candidates
            book_candidates = [r for r in search_results if r['relevance_score'] >= 4 and 
                             any(term in r['title'].lower() or term in r['snippet'].lower() 
                                 for term in ['book', 'work', 'treatise', 'publication'])]
            
            if book_candidates:
                print(f'\n📚 BOOK CANDIDATES FOUND ({len(book_candidates)}):')
                for candidate in book_candidates:
                    print(f'  • {candidate["title"]}')
                    print(f'    Score: {candidate["relevance_score"]} | Terms: {", ".join(candidate["matched_terms"])}')
                    all_results['potential_books'].append(candidate)
            
        else:
            print(f'❌ Request failed with status: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error in search {i}: {str(e)}')
    
    print(f'Completed search {i}/{len(search_queries)}')
    time.sleep(3)  # Rate limiting for politeness

print('\n' + '=' * 80)
print('COMPREHENSIVE ANALYSIS OF DIRECT SEARCH RESULTS')
print('=' * 80)

# Sort all results by relevance score
all_results['results'].sort(key=lambda x: x['relevance_score'], reverse=True)

total_results = len(all_results['results'])
print(f'Total results collected: {total_results}')
print(f'Potential book candidates: {len(all_results["potential_books"])}')

if all_results['results']:
    print('\n🏆 TOP 10 HIGHEST SCORING RESULTS:')
    print('-' * 50)
    
    for i, result in enumerate(all_results['results'][:10], 1):
        print(f'{i:2d}. Score: {result["relevance_score"]} | Query: {result["query"]}')
        print(f'    Title: {result["title"]}')
        print(f'    Terms: {", ".join(result["matched_terms"])}')
        print(f'    Link: {result["link"]}')
        print(f'    Snippet: {result["snippet"][:120]}...')
        print()

# Analyze patterns in results
all_terms = []
for result in all_results['results']:
    all_terms.extend(result['matched_terms'])

from collections import Counter
term_frequency = Counter(all_terms)

print('\n📊 TERM FREQUENCY ANALYSIS:')
print('-' * 30)
for term, count in term_frequency.most_common(10):
    print(f'{term}: {count} occurrences')

# Look for specific book titles or authors in high-scoring results
print('\n🔍 ANALYZING HIGH-SCORING RESULTS FOR BOOK IDENTIFICATION:')
print('-' * 60)

high_scoring = [r for r in all_results['results'] if r['relevance_score'] >= 5]
if high_scoring:
    for result in high_scoring:
        print(f'\nAnalyzing: {result["title"]}')
        print(f'Score: {result["relevance_score"]} | Terms: {", ".join(result["matched_terms"])}')
        print(f'Full snippet: {result["snippet"]}')
        print(f'Link: {result["link"]}')
        print('-' * 40)
else:
    print('No results with score >= 5 found. Showing top moderate results:')
    moderate_scoring = [r for r in all_results['results'] if r['relevance_score'] >= 3][:5]
    for result in moderate_scoring:
        print(f'\nAnalyzing: {result["title"]}')
        print(f'Score: {result["relevance_score"]} | Terms: {", ".join(result["matched_terms"])}')
        print(f'Snippet: {result["snippet"][:200]}...')
        print(f'Link: {result["link"]}')
        print('-' * 40)

# Save comprehensive results
results_file = os.path.join('workspace', 'atheistic_naturalism_1851_direct_search.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE RESULTS SAVED TO: {results_file}')

# Summary statistics
all_results['analysis'] = {
    'total_results': total_results,
    'high_relevance_count': len([r for r in all_results['results'] if r['relevance_score'] >= 5]),
    'moderate_relevance_count': len([r for r in all_results['results'] if 3 <= r['relevance_score'] < 5]),
    'book_candidates_count': len(all_results['potential_books']),
    'most_common_terms': dict(term_frequency.most_common(5)),
    'search_success_rate': f'{len([q for q in search_queries if any(r["query"] == q for r in all_results["results"])])}/{len(search_queries)}'
}

print(f'\n📈 FINAL STATISTICS:')
print(f'   • Total results: {all_results["analysis"]["total_results"]}')
print(f'   • High relevance (5+): {all_results["analysis"]["high_relevance_count"]}')
print(f'   • Moderate relevance (3-4): {all_results["analysis"]["moderate_relevance_count"]}')
print(f'   • Book candidates: {all_results["analysis"]["book_candidates_count"]}')
print(f'   • Search success rate: {all_results["analysis"]["search_success_rate"]}')
print(f'   • Most common terms: {list(all_results["analysis"]["most_common_terms"].keys())}')

print('\n🎯 NEXT STEPS BASED ON FINDINGS:')
if all_results['potential_books']:
    print('1. ✅ Book candidates identified - investigate specific titles and authors')
    print('2. ✅ Follow up on high-relevance links for detailed book information')
    print('3. ✅ Search for 2009 reissue information for identified candidates')
else:
    print('1. ❓ No clear book candidates found - may need more specific searches')
    print('2. ❓ Consider searching for individual authors or specific publishers')
    print('3. ❓ Try academic database searches or library catalogs')

print('4. 📋 Review saved HTML files for additional context')
print('5. 🔍 Conduct targeted searches based on any author names or titles found')

print('\n=== DIRECT WEB SEARCH PHASE COMPLETE ===')
```

## Created Time
2025-08-11 04:37:31
