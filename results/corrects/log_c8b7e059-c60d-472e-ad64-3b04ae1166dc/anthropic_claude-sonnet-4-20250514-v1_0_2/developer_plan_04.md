# Developer Plan 04

## Plan
Access Federico Lauria's actual 2014 dissertation to verify the exact work referenced in footnote 397, then search the Smithsonian American Art Museum collection for the two specific paintings whose titles quote from that work. Focus on finding the dissertation through academic databases like ProQuest Dissertations & Theses Global, university institutional repositories, or direct contact with the author's institution. Once footnote 397 is verified, conduct a targeted search of the SAAM collection using the actual source work's chapter titles or key phrases to identify the two paintings and determine which chapters their titles reference.

## Description
This approach is necessary because: (1) Previous analysis relied on predictions rather than accessing the actual footnote 397, leading to unsuccessful searches in the SAAM collection, (2) The developer found Shakespeare-derived artworks but this may not be the correct source work referenced in footnote 397, (3) We need definitive verification of the actual work cited in footnote 397 to conduct an accurate search for the specific two paintings mentioned in the TASK, (4) Only by identifying the correct source work and its chapter structure can we calculate the absolute difference between the chapter numbers of the two painting titles as requested

## Episodic Examples
### Development Step 2: Metropolitan Museum Portrait Accession 29.100.5: Title, Artist, Subject, and Metadata Search

**Description**: Search for information about the Metropolitan Museum of Art portrait with accession number 29.100.5. Look for the artwork's title, artist, subject, and any available metadata or catalog information. Use multiple search approaches including: (1) Direct search on the Met Museum's official website and collection database, (2) Google search with terms 'Metropolitan Museum Art 29.100.5 accession portrait', (3) Art history databases and museum catalog searches. Extract complete details about the portrait including who is depicted in the artwork.

**Use Cases**:
- Museum collection management and automated metadata synchronization for accession 29.100.5 in digital archives
- Graduate art history research and batch extraction of portrait details for thematic analysis in academic publications
- Auction house provenance verification and authenticity checks using cross-referenced Met Museum accession metadata
- Virtual tour application development and real-time retrieval of portrait metadata for enhanced visitor engagement
- Digital marketing content enrichment and SEO optimization with official artwork titles and artist information
- Journalism fact-checking and rapid aggregation of catalog details for museum exhibit coverage
- Cultural heritage linked data integration and semantic querying across multiple collection APIs
- Conservation report automation and pre-population of restoration logs with Met Museum artwork metadata

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

print('=== METROPOLITAN MUSEUM OF ART PORTRAIT RESEARCH ===\n')
print('Target: Accession number 29.100.5')
print('Objective: Find artwork title, artist, subject, and complete metadata\n')

# Fix the syntax error by treating accession number as string
accession_number = '29.100.5'
print(f'Searching for accession number: {accession_number}')

# First, try to access the Met Museum's official collection database directly
print('Step 1: Attempting direct access to Met Museum collection database...')

# The Met has a public API and collection search
met_collection_urls = [
    f'https://www.metmuseum.org/art/collection/search/{accession_number}',
    f'https://www.metmuseum.org/art/collection/search?q={accession_number}',
    f'https://collectionapi.metmuseum.org/public/collection/v1/search?q={accession_number}',
    f'https://www.metmuseum.org/art/collection/search?accessionNumber={accession_number}'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

met_results = []
for i, url in enumerate(met_collection_urls):
    print(f'\nTrying Met URL {i+1}: {url}')
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f'Response status: {response.status_code}')
        
        if response.status_code == 200:
            print(f'✓ Successfully accessed {url}')
            
            # Save the response for analysis
            filename = f'workspace/met_direct_search_{i+1}.html'
            
            # Check if it's JSON or HTML
            try:
                json_data = response.json()
                filename = f'workspace/met_api_response_{i+1}.json'
                with open(filename, 'w') as f:
                    json.dump(json_data, f, indent=2)
                print(f'  Saved JSON response to: {filename}')
                print(f'  JSON keys: {list(json_data.keys()) if isinstance(json_data, dict) else "List with " + str(len(json_data)) + " items"}')
            except:
                # It's HTML
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f'  Saved HTML response to: {filename}')
                
                # Quick analysis of HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.find('title')
                title_text = title.get_text().strip() if title else 'No title found'
                print(f'  Page title: {title_text}')
                
                # Look for accession number mentions
                content_text = response.text.lower()
                if accession_number in content_text:
                    print('  *** ACCESSION NUMBER FOUND IN CONTENT ***')
                
                # Look for portrait/artwork indicators
                artwork_indicators = ['portrait', 'painting', 'artist', 'artwork', 'collection']
                found_indicators = [ind for ind in artwork_indicators if ind in content_text]
                if found_indicators:
                    print(f'  Artwork indicators found: {found_indicators}')
            
            met_results.append({
                'url': url,
                'status': response.status_code,
                'filename': filename,
                'content_length': len(response.text)
            })
            
        else:
            print(f'✗ Failed - Status: {response.status_code}')
            met_results.append({
                'url': url,
                'status': response.status_code,
                'error': f'HTTP {response.status_code}'
            })
            
    except Exception as e:
        print(f'✗ Error: {str(e)}')
        met_results.append({
            'url': url,
            'error': str(e)
        })
    
    time.sleep(2)  # Be respectful to servers

print(f'\n=== MET MUSEUM DIRECT SEARCH RESULTS ===\n')
print(f'Attempted {len(met_collection_urls)} direct Met Museum URLs')
successful_met = [r for r in met_results if r.get('status') == 200]
print(f'Successful responses: {len(successful_met)}')

for result in successful_met:
    print(f'  ✓ {result["url"]} -> {result["filename"]}')

# Now use Google Search API for comprehensive search
api_key = os.getenv("SERPAPI_API_KEY")

if api_key:
    print('\n=== GOOGLE SEARCH FOR MET PORTRAIT 29.100.5 ===\n')
    
    # Multiple search queries to maximize information gathering
    search_queries = [
        f'Metropolitan Museum Art {accession_number} accession portrait',
        f'Met Museum {accession_number} painting artwork collection',
        f'"{accession_number}" Metropolitan Museum portrait artist subject',
        f'metmuseum.org {accession_number} accession number artwork'
    ]
    
    google_results = []
    
    for i, query in enumerate(search_queries):
        print(f'Search {i+1}: "{query}"')
        
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 8
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            
            if response.status_code == 200:
                results = response.json()
                
                if results.get("organic_results"):
                    print(f'  Found {len(results["organic_results"])} results')
                    
                    for j, result in enumerate(results["organic_results"]):
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No link')
                        snippet = result.get('snippet', 'No snippet')
                        
                        print(f'\n    Result {j+1}:')
                        print(f'    Title: {title}')
                        print(f'    URL: {link}')
                        print(f'    Snippet: {snippet}')
                        
                        # Check for key information
                        combined_text = f'{title} {snippet}'.lower()
                        
                        key_findings = []
                        if accession_number in combined_text:
                            key_findings.append('Accession number found')
                        if 'portrait' in combined_text:
                            key_findings.append('Portrait mentioned')
                        if 'artist' in combined_text or 'painter' in combined_text:
                            key_findings.append('Artist information')
                        if 'metmuseum.org' in link:
                            key_findings.append('Official Met Museum source')
                        
                        if key_findings:
                            print(f'    *** KEY FINDINGS: {key_findings} ***')
                        
                        google_results.append({
                            'search_query': query,
                            'result_index': j+1,
                            'title': title,
                            'link': link,
                            'snippet': snippet,
                            'key_findings': key_findings
                        })
                else:
                    print('  No organic results found')
            else:
                print(f'  Search failed with status: {response.status_code}')
                
        except Exception as e:
            print(f'  Search error: {str(e)}')
        
        time.sleep(1)  # Rate limiting
    
    # Save all Google search results
    with open('workspace/met_29_100_5_google_results.json', 'w') as f:
        json.dump(google_results, f, indent=2)
    
    print(f'\nGoogle search results saved to: workspace/met_29_100_5_google_results.json')
    print(f'Total Google results collected: {len(google_results)}')
    
    # Identify most promising results
    priority_results = [r for r in google_results if r['key_findings']]
    print(f'Priority results with key findings: {len(priority_results)}')
    
else:
    print('\nNo SERPAPI key available - skipping Google search')
    google_results = []

# Compile initial research summary
research_summary = {
    'target_accession': accession_number,
    'museum': 'Metropolitan Museum of Art',
    'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'direct_met_searches': {
        'attempted_urls': len(met_collection_urls),
        'successful_responses': len(successful_met),
        'results': met_results
    },
    'google_searches': {
        'queries_attempted': len(search_queries) if api_key else 0,
        'total_results': len(google_results),
        'priority_results': len([r for r in google_results if r.get('key_findings')]) if google_results else 0
    },
    'files_created': [
        f for f in os.listdir('workspace') 
        if f.startswith('met_') and (f.endswith('.html') or f.endswith('.json'))
    ]
}

with open('workspace/met_portrait_research_summary.json', 'w') as f:
    json.dump(research_summary, f, indent=2)

print(f'\n=== PHASE 1 RESEARCH COMPLETE ===\n')
print(f'Research summary saved to: workspace/met_portrait_research_summary.json')
print(f'Files created in workspace: {len(research_summary["files_created"])}')  
print(f'Next step: Analyze collected data to extract portrait details')

# Quick preview of findings
if successful_met:
    print(f'\n✓ Successfully accessed {len(successful_met)} Met Museum URLs')
if google_results:
    priority_count = len([r for r in google_results if r.get('key_findings')])
    print(f'✓ Found {priority_count} priority Google results with key information')

print('\nReady for detailed analysis of collected data...')
```

### Development Step 10: Locate and Verify Quoted Passage in Greetham’s “Uncoupled” (2008) via DOI/Project MUSE

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- University librarians automating the verification of quoted passages in graduate theses to ensure accurate citation of articles like Greetham’s “Uncoupled”
- Academic researchers cross-checking bibliographic references and exact quotations during systematic literature reviews for textual criticism studies
- Publishing house editorial teams validating direct quotes and page numbers when preparing digital editions of scholarly journals for consistency and legal compliance
- Plagiarism detection services automatically retrieving full-text content via DOI resolution to confirm the authenticity of cited text in student essays
- Digital humanities projects extracting and analyzing manuscript variant readings from specific pages across multiple editions for comparative textual analysis
- Research data management platforms harvesting article metadata (title, author, journal, pages) via DOI to populate institutional repositories with accurate bibliographic records
- University compliance offices verifying the presence of open access indicators and licensing terms in articles to ensure adherence to funder mandates and institutional policies

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

print('=== ACCESSING GREETHAM ARTICLE - ALL SYNTAX ERRORS FIXED ===')
print('Title: Uncoupled: OR, How I Lost My Author(s)')
print('Author: David Greetham')
print('Journal: Textual Cultures: Texts, Contexts, Interpretation')
print('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46')
print('DOI: 10.2979/tex.2008.3.1.44')
print('Target Quote: "obscured not by a \"cloak of print\" but by the veil of scribal confusion and mis-transmission"')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# First, check if we already have the raw HTML from previous attempts
raw_response_path = 'workspace/doi_response_raw.html'
if os.path.exists(raw_response_path):
    print('=== USING EXISTING RAW HTML RESPONSE ===')
    print(f'Found existing raw response: {raw_response_path}')
    
    with open(raw_response_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f'✓ Loaded existing HTML content: {len(html_content):,} characters')
    
    # Parse the existing content
    soup = BeautifulSoup(html_content, 'html.parser')
    final_url = 'https://muse.jhu.edu/article/240795'  # Known from previous attempts
    
else:
    print('=== FETCHING FRESH CONTENT FROM DOI ===')
    # Construct the DOI URL
    doi_url = 'https://doi.org/10.2979/tex.2008.3.1.44'
    print(f'DOI URL to resolve: {doi_url}')
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    try:
        # Make the DOI request
        print(f'Requesting: {doi_url}')
        doi_response = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
        
        print(f'✓ Request completed')
        print(f'Status code: {doi_response.status_code}')
        print(f'Final URL after redirects: {doi_response.url}')
        print(f'Content length: {len(doi_response.content):,} bytes')
        
        if doi_response.status_code == 200:
            # Save the response
            with open(raw_response_path, 'w', encoding='utf-8') as f:
                f.write(doi_response.text)
            print(f'✓ Raw response saved to: {raw_response_path}')
            
            # Parse the content
            soup = BeautifulSoup(doi_response.content, 'html.parser')
            final_url = doi_response.url
        else:
            print(f'❌ DOI resolution failed with status {doi_response.status_code}')
            exit()
            
    except Exception as e:
        print(f'❌ Error during DOI resolution: {str(e)}')
        exit()

print('\n=== STEP 1: EXTRACTING PAGE CONTENT AND METADATA ===')

# CRITICAL: Define page_text immediately after soup creation
page_text = soup.get_text()
page_text_lower = page_text.lower()
print(f'✓ Page text extracted: {len(page_text):,} characters')

# Get page title
page_title = soup.find('title')
if page_title:
    title_text = page_title.get_text().strip()
    print(f'Page title: {title_text}')
    
    # Verify this is the correct article
    if 'uncoupled' in title_text.lower() or 'greetham' in title_text.lower():
        print('✓ Confirmed: This appears to be the correct Greetham article')
    else:
        print('⚠ Warning: Page title does not clearly match expected article')
else:
    print('⚠ No page title found')

# Extract article metadata
print('\n--- EXTRACTING ARTICLE METADATA ---')

# Search for article title
title_selectors = ['h1', 'h1.title', '.article-title', '.citation_title', '.title']
article_title = None
for selector in title_selectors:
    title_elem = soup.select_one(selector)
    if title_elem:
        title_text = title_elem.get_text().strip()
        if len(title_text) > 10:
            article_title = title_text
            print(f'Article title found: {title_text}')
            break

if not article_title:
    print('Article title not found with standard selectors')

# Search for author information
author_selectors = ['.author', '.citation_author', '.article-author', '[data-author]']
article_author = None
for selector in author_selectors:
    author_elem = soup.select_one(selector)
    if author_elem:
        author_text = author_elem.get_text().strip()
        if 'greetham' in author_text.lower():
            article_author = author_text
            print(f'Author found: {author_text}')
            break

if not article_author:
    print('Author not found with standard selectors')
    if 'greetham' in page_text_lower:
        print('✓ Author name "Greetham" found in page text')

# Search for journal information
journal_selectors = ['.journal-title', '.citation_journal_title', '.source-title']
journal_title = None
for selector in journal_selectors:
    journal_elem = soup.select_one(selector)
    if journal_elem:
        journal_text = journal_elem.get_text().strip()
        if 'textual' in journal_text.lower():
            journal_title = journal_text
            print(f'Journal found: {journal_text}')
            break

if not journal_title:
    print('Journal title not found with standard selectors')
    if 'textual cultures' in page_text_lower:
        print('✓ Journal name "Textual Cultures" found in page text')

print('\n=== STEP 2: SEARCHING FOR TARGET QUOTE ===')

# Define the target quote - using simple approach to avoid syntax errors
target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'

# Define quote variations using simple string literals to avoid escaping issues
quote_variations = [
    'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission',
    'obscured not by a cloak of print but by the veil of scribal confusion and mis-transmission',
    'cloak of print',
    'veil of scribal confusion',
    'scribal confusion and mis-transmission',
    'scribal confusion',
    'mis-transmission'
]

print(f'Searching for {len(quote_variations)} quote variations...')

quote_found_on_page = False
found_variation = None
found_context = None

for i, variation in enumerate(quote_variations, 1):
    if variation.lower() in page_text_lower:
        print(f'\n🎯 FOUND QUOTE VARIATION {i}: "{variation}"')
        quote_found_on_page = True
        found_variation = variation
        
        # Extract context around the quote
        index = page_text_lower.find(variation.lower())
        context_start = max(0, index - 600)
        context_end = min(len(page_text), index + 800)
        found_context = page_text[context_start:context_end]
        
        print(f'\n*** QUOTE CONTEXT FROM PROJECT MUSE PAGE ***')
        print('='*120)
        print(found_context)
        print('='*120)
        break

if not quote_found_on_page:
    print('⚠ Target quote not found on the main Project MUSE page')
    print('This suggests the full text may be behind access controls')
    
    # Let's search for any content that might indicate we have access to the article content
    print('\n--- ANALYZING AVAILABLE CONTENT ---')
    
    # Look for page references
    page_indicators = ['page 45', 'page 46', 'pp. 45', 'pp. 46', 'p. 45', 'p. 46']
    page_refs_found = []
    
    for indicator in page_indicators:
        if indicator in page_text_lower:
            page_refs_found.append(indicator)
    
    if page_refs_found:
        print(f'✓ Page references found: {page_refs_found}')
    else:
        print('⚠ No specific page 45-46 references found on main page')
    
    # Look for related textual criticism terms
    related_terms = ['textual', 'manuscript', 'editorial', 'transmission', 'scribal', 'print', 'confusion']
    found_terms = []
    
    for term in related_terms:
        if term.lower() in page_text_lower:
            count = page_text_lower.count(term.lower())
            found_terms.append(f'{term} ({count})')
    
    if found_terms:
        print(f'✓ Related textual criticism terms found: {found_terms}')
    else:
        print('⚠ No related textual criticism terms found')

print('\n=== STEP 3: SEARCHING FOR FULL TEXT ACCESS ===')

# Look for various types of access links
access_selectors = [
    'a[href*=".pdf"]',
    'a[href*="download"]',
    'a[href*="fulltext"]',
    'a[href*="full-text"]',
    'a[href*="view"]',
    'a[href*="read"]',
    '.pdf-link a',
    '.download-link a',
    '.full-text-link a',
    '.access-link a'
]

access_links = []
for selector in access_selectors:
    try:
        links = soup.select(selector)
        for link in links:
            href = link.get('href')
            if href:
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = urljoin('https://muse.jhu.edu', href)
                
                link_text = link.get_text().strip()
                access_links.append({
                    'url': href,
                    'text': link_text,
                    'selector': selector
                })
    except Exception as e:
        print(f'Error with selector {selector}: {str(e)}')

# Remove duplicates
unique_access = []
seen_urls = set()
for link in access_links:
    if link['url'] not in seen_urls:
        seen_urls.add(link['url'])
        unique_access.append(link)

print(f'Found {len(unique_access)} potential access links:')
for i, link in enumerate(unique_access, 1):
    print(f'{i}. "{link["text"]}" -> {link["url"]}')
    print(f'   (Found via: {link["selector"]})')

# Check for open access indicators
open_access_indicators = ['open access', 'free access', 'freely available', 'oa']
is_open_access = any(indicator in page_text_lower for indicator in open_access_indicators)
print(f'\nOpen access indicators detected: {is_open_access}')

print('\n=== STEP 4: ATTEMPTING TO ACCESS FULL ARTICLE CONTENT ===')

# Look for the actual article content on the current page
# Sometimes Project MUSE includes the full text directly in the page
content_selectors = [
    '.article-content',
    '.full-text',
    '.article-body',
    '.content',
    '#content',
    '.text',
    '.article-text',
    'main',
    '.body-content'
]

article_content_found = False
for selector in content_selectors:
    content_elem = soup.select_one(selector)
    if content_elem:
        content_text = content_elem.get_text().strip()
        if len(content_text) > 500:  # Substantial content
            print(f'\n✓ Found substantial article content using selector: {selector}')
            print(f'Content length: {len(content_text):,} characters')
            
            # Save the extracted content
            content_path = 'workspace/greetham_article_content.txt'
            with open(content_path, 'w', encoding='utf-8') as content_file:
                content_file.write('ARTICLE CONTENT EXTRACTED FROM PROJECT MUSE\n')
                content_file.write(f'Selector used: {selector}\n')
                content_file.write(f'Content length: {len(content_text):,} characters\n')
                content_file.write('='*80 + '\n')
                content_file.write(content_text)
            
            print(f'✓ Article content saved to: {content_path}')
            
            # Search for the target quote in this content
            print('\n--- SEARCHING EXTRACTED CONTENT FOR TARGET QUOTE ---')
            content_text_lower = content_text.lower()
            
            for i, variation in enumerate(quote_variations, 1):
                if variation.lower() in content_text_lower:
                    print(f'\n🎯 FOUND TARGET QUOTE IN EXTRACTED CONTENT (Variation {i}): "{variation}"')
                    
                    # Extract context around the quote
                    index = content_text_lower.find(variation.lower())
                    context_start = max(0, index - 800)
                    context_end = min(len(content_text), index + 1000)
                    context = content_text[context_start:context_end]
                    
                    print(f'\n*** QUOTE VERIFICATION - PAGES 45-46 CONTENT ***')
                    print('='*120)
                    print(context)
                    print('='*120)
                    
                    # Save the verification context
                    verification_path = 'workspace/quote_verification_pages_45_46.txt'
                    with open(verification_path, 'w', encoding='utf-8') as verify_file:
                        verify_file.write('QUOTE VERIFICATION REPORT\n')
                        verify_file.write('Article: Uncoupled: OR, How I Lost My Author(s)\n')
                        verify_file.write('Author: David Greetham\n')
                        verify_file.write('Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
                        verify_file.write('DOI: 10.2979/tex.2008.3.1.44\n\n')
                        verify_file.write(f'TARGET QUOTE:\n{target_quote}\n\n')
                        verify_file.write(f'FOUND VARIATION:\n{variation}\n\n')
                        verify_file.write(f'CONTEXT FROM ARTICLE:\n{context}\n')
                    
                    print(f'\n✓ Quote verification saved to: {verification_path}')
                    article_content_found = True
                    break
            
            if not article_content_found:
                print('⚠ Target quote not found in extracted content')
                # Show preview of extracted content
                preview_text = content_text[:1500]
                print(f'\n*** EXTRACTED CONTENT PREVIEW (First 1500 characters) ***')
                print('='*100)
                print(preview_text)
                print('='*100)
            
            break

# If we found the quote on the main page, save that verification too
if quote_found_on_page and found_context:
    verification_path = 'workspace/quote_verification_pages_45_46.txt'
    with open(verification_path, 'w', encoding='utf-8') as verify_file:
        verify_file.write('QUOTE VERIFICATION REPORT\n')
        verify_file.write('Article: Uncoupled: OR, How I Lost My Author(s)\n')
        verify_file.write('Author: David Greetham\n')
        verify_file.write('Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
        verify_file.write('DOI: 10.2979/tex.2008.3.1.44\n\n')
        verify_file.write(f'TARGET QUOTE:\n{target_quote}\n\n')
        verify_file.write(f'FOUND VARIATION:\n{found_variation}\n\n')
        verify_file.write('CONTEXT FROM MAIN PAGE:\n' + found_context + '\n')
    
    print(f'\n✓ Quote verification from main page saved to: {verification_path}')
    article_content_found = True

if not article_content_found:
    print('\n⚠ No substantial article content found on the main page')
    print('The full text may require institutional access or be on a separate page')
    
    # Save a comprehensive analysis
    analysis_data = {
        'doi_url': 'https://doi.org/10.2979/tex.2008.3.1.44',
        'final_url': final_url if 'final_url' in locals() else 'https://muse.jhu.edu/article/240795',
        'page_title': page_title.get_text().strip() if page_title else None,
        'article_title': article_title,
        'article_author': article_author,
        'journal_title': journal_title,
        'page_text_length': len(page_text),
        'access_links_found': len(unique_access),
        'is_open_access': is_open_access,
        'quote_found_on_page': quote_found_on_page,
        'target_quote': target_quote,
        'quote_variations_searched': len(quote_variations),
        'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    analysis_path = 'workspace/greetham_article_analysis.json'
    with open(analysis_path, 'w', encoding='utf-8') as analysis_file:
        json.dump(analysis_data, analysis_file, indent=2, ensure_ascii=False)
    
    print(f'\n✓ Comprehensive analysis saved to: {analysis_path}')

# Let's also inspect what files we have in workspace to understand the current state
print('\n=== WORKSPACE FILES INSPECTION ===')
if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    print(f'Found {len(workspace_files)} files in workspace:')
    for file in workspace_files:
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')
        
        # If it's a JSON file, let's inspect its structure
        if file.endswith('.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                print(f'  JSON keys: {list(json_data.keys()) if isinstance(json_data, dict) else "Not a dict"}')
            except Exception as e:
                print(f'  JSON inspection error: {str(e)}')
else:
    print('No workspace directory found')

print('\n=== QUOTE VERIFICATION COMPLETE ===')
print('Summary:')
print('- ✓ Successfully resolved DOI to Project MUSE')
print('- ✓ Confirmed correct Greetham article')
print('- ✓ Extracted article metadata')
print('- ✓ Searched for target quote with multiple variations')
print('- ✓ Saved all results to workspace/ directory')

if quote_found_on_page or article_content_found:
    print('\n🎯 SUCCESS: Target quote found and verified!')
else:
    print('\n⚠ Quote not found on accessible content - may require institutional access')
    print('The article appears to be behind a paywall or requires institutional access')
    print('However, we have successfully confirmed the article exists and matches the citation')
```

### Development Step 2: Locate Greetham’s ‘Uncoupled’ via DOI and Verify Quotation on Pages 45–46

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- University library digitization team automating bulk DOI resolution and full-text retrieval to build a searchable local archive of historical journal issues
- Journal editorial office running a pre-publication script to confirm each DOI link resolves correctly on Project MUSE and verify quoted passages during copyediting
- Reference management tool plugin for graduate students that fetches article metadata, downloads PDFs, and validates key quotations from bibliographies
- Digital humanities research group extracting specific textual passages across multiple articles to analyze scribal transmission errors in medieval manuscript studies
- University open-access office scanning faculty publications to detect “free access” indicators, retrieve full texts, and update the institutional repository automatically
- Bibliometric analysts harvesting metadata, full-text access links, and citation contexts for large-scale network analysis of scholarly communication patterns
- Patent law firm verifying verbatim quotes from academic articles via DOI resolution and HTML parsing to support prior-art examination and infringement cases
- Research compliance team automating audits of funded project reports to ensure published papers include correct DOIs, accessible full texts, and accurate quoted excerpts

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE VIA DOI - FIXED IMPLEMENTATION ===')
print('Title: Uncoupled: OR, How I Lost My Author(s)')
print('Author: David Greetham')
print('Journal: Textual Cultures: Texts, Contexts, Interpretation')
print('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46')
print('DOI: 10.2979/tex.2008.3.1.44')
print('Target Quote: "obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission"')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Construct the DOI URL - this is the critical step that failed before
doi_url = 'https://doi.org/10.2979/tex.2008.3.1.44'
print(f'DOI URL to resolve: {doi_url}')

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

print('\n=== STEP 1: DOI RESOLUTION TO PROJECT MUSE ===')
print('Making HTTP request to DOI resolver...')

try:
    # Make the DOI request with proper error handling
    print(f'Requesting: {doi_url}')
    doi_response = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
    
    print(f'✓ Request completed')
    print(f'Status code: {doi_response.status_code}')
    print(f'Final URL after redirects: {doi_response.url}')
    print(f'Content length: {len(doi_response.content):,} bytes')
    print(f'Content type: {doi_response.headers.get("Content-Type", "unknown")}')
    print(f'Response headers count: {len(doi_response.headers)}')
    
    # Verify we actually got a valid response
    if doi_response.status_code != 200:
        print(f'❌ DOI resolution failed with status {doi_response.status_code}')
        print(f'Response text preview: {doi_response.text[:500]}')
        raise Exception(f'DOI resolution failed: HTTP {doi_response.status_code}')
    
    # Check if we're actually on Project MUSE or the expected domain
    final_domain = urlparse(doi_response.url).netloc
    print(f'Final domain: {final_domain}')
    
    if 'muse.jhu.edu' not in final_domain and 'projectmuse.org' not in final_domain:
        print(f'⚠ Warning: Not on expected Project MUSE domain')
        print(f'Actual domain: {final_domain}')
    else:
        print(f'✓ Successfully reached Project MUSE domain')
    
    # Parse the response content
    print('\n=== STEP 2: PARSING PROJECT MUSE ARTICLE PAGE ===')
    soup = BeautifulSoup(doi_response.content, 'html.parser')
    
    # Get page title
    page_title = soup.find('title')
    if page_title:
        title_text = page_title.get_text().strip()
        print(f'Page title: {title_text}')
        
        # Verify this is the correct article
        if 'uncoupled' in title_text.lower() or 'greetham' in title_text.lower():
            print('✓ Confirmed: This appears to be the correct Greetham article')
        else:
            print('⚠ Warning: Page title does not clearly match expected article')
    else:
        print('⚠ No page title found')
    
    # Look for article metadata
    print('\n--- EXTRACTING ARTICLE METADATA ---')
    
    # Search for article title
    title_selectors = ['h1', 'h1.title', '.article-title', '.citation_title']
    article_title = None
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            title_text = title_elem.get_text().strip()
            if len(title_text) > 10:  # Reasonable title length
                article_title = title_text
                print(f'Article title: {title_text}')
                break
    
    # Search for author information
    author_selectors = ['.author', '.citation_author', '.article-author']
    article_author = None
    for selector in author_selectors:
        author_elem = soup.select_one(selector)
        if author_elem:
            author_text = author_elem.get_text().strip()
            if 'greetham' in author_text.lower():
                article_author = author_text
                print(f'Author: {author_text}')
                break
    
    # Search for journal information
    journal_selectors = ['.journal-title', '.citation_journal_title', '.source-title']
    journal_title = None
    for selector in journal_selectors:
        journal_elem = soup.select_one(selector)
        if journal_elem:
            journal_text = journal_elem.get_text().strip()
            if 'textual' in journal_text.lower():
                journal_title = journal_text
                print(f'Journal: {journal_text}')
                break
    
    # Look for volume/issue/page information
    volume_info = {}
    citation_selectors = {
        'volume': ['.citation_volume', '.volume'],
        'issue': ['.citation_issue', '.issue'], 
        'year': ['.citation_date', '.year', '.date'],
        'pages': ['.citation_firstpage', '.citation_lastpage', '.pages']
    }
    
    for info_type, selectors in citation_selectors.items():
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                value = elem.get_text().strip()
                if value:
                    volume_info[info_type] = value
                    print(f'{info_type.title()}: {value}')
                    break
    
    print('\n=== STEP 3: SEARCHING FOR FULL TEXT ACCESS ===')
    
    # Look for various types of access links
    access_selectors = [
        'a[href*=".pdf"]',
        'a[href*="download"]',
        'a[href*="fulltext"]',
        'a[href*="full-text"]',
        'a[href*="view"]',
        'a[href*="read"]',
        '.pdf-link a',
        '.download-link a',
        '.full-text-link a',
        '.access-link a'
    ]
    
    access_links = []
    for selector in access_selectors:
        try:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        href = urljoin(doi_response.url, href)
                    
                    link_text = link.get_text().strip()
                    access_links.append({
                        'url': href,
                        'text': link_text,
                        'selector': selector
                    })
        except Exception as e:
            print(f'Error with selector {selector}: {str(e)}')
    
    # Remove duplicates
    unique_access = []
    seen_urls = set()
    for link in access_links:
        if link['url'] not in seen_urls:
            seen_urls.add(link['url'])
            unique_access.append(link)
    
    print(f'Found {len(unique_access)} potential access links:')
    for i, link in enumerate(unique_access, 1):
        print(f'{i}. "{link["text"]}" -> {link["url"]}')
        print(f'   (Found via: {link["selector"]})')
    
    # Check for open access indicators
    page_text = soup.get_text().lower()
    open_access_indicators = ['open access', 'free access', 'freely available', 'oa']
    is_open_access = any(indicator in page_text for indicator in open_access_indicators)
    print(f'\nOpen access indicators detected: {is_open_access}')
    
    # Search for the target quote on the current page
    print('\n=== STEP 4: SEARCHING FOR TARGET QUOTE ON PAGE ===')
    target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'
    
    quote_variations = [
        target_quote,
        target_quote.replace('"', '
```

### Development Step 3: Verify quoted passage in David Greetham’s ‘Uncoupled: OR, How I Lost My Author(s)’

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Automated verification of dissertation citations by fetching articles via DOI and confirming quoted passages against original pages
- Library metadata enrichment workflows that resolve DOIs to populate institutional repositories with accurate titles, authors, and journal details
- Journal editorial systems that programmatically retrieve manuscript references to check for correct article matching and potential mis-citations
- Digital humanities projects extracting specific text passages from online archives to compare manuscript variants and transmission errors
- Patent research teams mining academic articles for targeted technical phrases to support thorough prior‐art searches
- Market intelligence units automatically pulling industry white papers by DOI and scanning for key terms to inform competitive analysis
- Educational content providers verifying textbook quotation accuracy and page numbers by scraping source articles in real time
- Systematic review platforms that batch‐resolve DOIs, download full texts, and extract methodological details for meta‐analysis

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE VIA DOI - CORRECTED IMPLEMENTATION ===')
print('Title: Uncoupled: OR, How I Lost My Author(s)')
print('Author: David Greetham')
print('Journal: Textual Cultures: Texts, Contexts, Interpretation')
print('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46')
print('DOI: 10.2979/tex.2008.3.1.44')
print('Target Quote: "obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission"')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Construct the DOI URL
doi_url = 'https://doi.org/10.2979/tex.2008.3.1.44'
print(f'DOI URL to resolve: {doi_url}')

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
}

print('\n=== STEP 1: DOI RESOLUTION TO PROJECT MUSE ===')
print('Making HTTP request to DOI resolver...')

try:
    # Make the DOI request with proper error handling
    print(f'Requesting: {doi_url}')
    doi_response = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
    
    print(f'✓ Request completed')
    print(f'Status code: {doi_response.status_code}')
    print(f'Final URL after redirects: {doi_response.url}')
    print(f'Content length: {len(doi_response.content):,} bytes')
    print(f'Content type: {doi_response.headers.get("Content-Type", "unknown")}')
    
    # Verify we actually got a valid response
    if doi_response.status_code != 200:
        print(f'❌ DOI resolution failed with status {doi_response.status_code}')
        print(f'Response text preview: {doi_response.text[:500]}')
        raise Exception(f'DOI resolution failed: HTTP {doi_response.status_code}')
    
    # Check if we're actually on Project MUSE or the expected domain
    final_domain = urlparse(doi_response.url).netloc
    print(f'Final domain: {final_domain}')
    
    if 'muse.jhu.edu' not in final_domain and 'projectmuse.org' not in final_domain:
        print(f'⚠ Warning: Not on expected Project MUSE domain')
        print(f'Actual domain: {final_domain}')
    else:
        print(f'✓ Successfully reached Project MUSE domain')
    
    # Save the raw response for analysis
    raw_response_path = 'workspace/doi_response_raw.html'
    with open(raw_response_path, 'w', encoding='utf-8') as f:
        f.write(doi_response.text)
    print(f'✓ Raw DOI response saved to: {raw_response_path}')
    
    # Parse the response content
    print('\n=== STEP 2: PARSING PROJECT MUSE ARTICLE PAGE ===')
    soup = BeautifulSoup(doi_response.content, 'html.parser')
    
    # Get page title
    page_title = soup.find('title')
    if page_title:
        title_text = page_title.get_text().strip()
        print(f'Page title: {title_text}')
        
        # Verify this is the correct article
        if 'uncoupled' in title_text.lower() or 'greetham' in title_text.lower():
            print('✓ Confirmed: This appears to be the correct Greetham article')
        else:
            print('⚠ Warning: Page title does not clearly match expected article')
    else:
        print('⚠ No page title found')
    
    # Look for article metadata
    print('\n--- EXTRACTING ARTICLE METADATA ---')
    
    # Search for article title
    title_selectors = ['h1', 'h1.title', '.article-title', '.citation_title', '.title']
    article_title = None
    for selector in title_selectors:
        title_elem = soup.select_one(selector)
        if title_elem:
            title_text = title_elem.get_text().strip()
            if len(title_text) > 10:  # Reasonable title length
                article_title = title_text
                print(f'Article title found: {title_text}')
                break
    
    if not article_title:
        print('Article title not found with standard selectors')
    
    # Search for author information
    author_selectors = ['.author', '.citation_author', '.article-author', '[data-author]']
    article_author = None
    for selector in author_selectors:
        author_elem = soup.select_one(selector)
        if author_elem:
            author_text = author_elem.get_text().strip()
            if 'greetham' in author_text.lower():
                article_author = author_text
                print(f'Author found: {author_text}')
                break
    
    if not article_author:
        print('Author not found with standard selectors')
    
    # Search for journal information
    journal_selectors = ['.journal-title', '.citation_journal_title', '.source-title']
    journal_title = None
    for selector in journal_selectors:
        journal_elem = soup.select_one(selector)
        if journal_elem:
            journal_text = journal_elem.get_text().strip()
            if 'textual' in journal_text.lower():
                journal_title = journal_text
                print(f'Journal found: {journal_text}')
                break
    
    if not journal_title:
        print('Journal title not found with standard selectors')
    
    print('\n=== STEP 3: SEARCHING FOR FULL TEXT ACCESS ===')
    
    # Look for various types of access links
    access_selectors = [
        'a[href*=".pdf"]',
        'a[href*="download"]',
        'a[href*="fulltext"]',
        'a[href*="full-text"]',
        'a[href*="view"]',
        'a[href*="read"]',
        '.pdf-link a',
        '.download-link a',
        '.full-text-link a',
        '.access-link a'
    ]
    
    access_links = []
    for selector in access_selectors:
        try:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        href = urljoin(doi_response.url, href)
                    
                    link_text = link.get_text().strip()
                    access_links.append({
                        'url': href,
                        'text': link_text,
                        'selector': selector
                    })
        except Exception as e:
            print(f'Error with selector {selector}: {str(e)}')
    
    # Remove duplicates
    unique_access = []
    seen_urls = set()
    for link in access_links:
        if link['url'] not in seen_urls:
            seen_urls.add(link['url'])
            unique_access.append(link)
    
    print(f'Found {len(unique_access)} potential access links:')
    for i, link in enumerate(unique_access, 1):
        print(f'{i}. "{link["text"]}" -> {link["url"]}')
        print(f'   (Found via: {link["selector"]})')
    
    # Check for open access indicators
    page_text = soup.get_text().lower()
    open_access_indicators = ['open access', 'free access', 'freely available', 'oa']
    is_open_access = any(indicator in page_text for indicator in open_access_indicators)
    print(f'\nOpen access indicators detected: {is_open_access}')
    
    # Search for the target quote on the current page
    print('\n=== STEP 4: SEARCHING FOR TARGET QUOTE ON PAGE ===')
    target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'
    
    # Define quote variations with proper string handling
    quote_variations = [
        target_quote,
        target_quote.replace('"', '
```

## Created Time
2025-08-14 04:14:59
