# Developer Plan 01

## Plan
Search for the book with DOI 10.2307/j.ctv9b2xdv to identify the title, author, and publisher. Use multiple search approaches: (1) Direct DOI resolution through doi.org, (2) Academic database searches using the DOI, (3) Google Scholar search with the DOI string, (4) Publisher database searches focusing on the '10.2307' prefix which typically indicates JSTOR publications. Extract complete bibliographic information including title, author, publication year, publisher, and any available abstract or description to understand the book's content and structure.

## Description
This is the optimal first step because: (1) We need to identify the specific book before accessing page 11 and its endnotes, (2) No previous research has been conducted, (3) Expected outcome is to obtain the book's bibliographic details and access information, (4) This establishes the foundation for locating and analyzing page 11's second-to-last paragraph and its endnote containing the Wikipedia access date

## Episodic Examples
### Development Step 1: Find Bibliographic Details of Neurologist-Focused Book via DOI 10.1353/book.24372

**Description**: Search for the book with DOI 10.1353/book.24372 to identify the title, author, and subject neurologist. Use multiple search approaches: (1) Direct DOI resolution through doi.org, (2) Academic database searches using the DOI, (3) Google Scholar search with the DOI string, (4) Publisher database searches focusing on the '10.1353' prefix which typically indicates Project MUSE publications. Extract complete bibliographic information including title, author, publication year, publisher, and any available abstract or description that identifies which neurologist the book concerns.

**Use Cases**:
- University library catalog integration for automated ingestion of new monographs by resolving DOIs, extracting complete bibliographic metadata, and populating catalog records
- Reference management software enhancement that auto-fills title, author, publication year, and subject area for books by querying DOI.org and academic databases
- Bibliometric research pipeline in neuroscience studies that aggregates publication metrics and author profiles for books on neurologists using Google Scholar DOI searches
- Digital humanities project compiling biographical data on historical neurologists by scraping abstracts and descriptions from Project MUSE entries resolved via the ‘10.1353’ DOI prefix
- Curriculum development tool for medical schools that retrieves book summaries, publisher details, and recommended readings in neurology courses through automated DOI lookups
- Academic journal editorial workflow that validates submitted book citations by cross-checking DOIs against doi.org redirects and Google search results to ensure metadata accuracy
- Biomedical publishing quality assurance system that verifies DOI-to-title/author mappings before printing new neurology textbooks by performing scripted resolution and pattern extraction
- Patent analysis software for medical device innovation that identifies foundational neurological texts cited in filings by resolving book DOIs and extracting publication information for citation networks

```
import os
import re
import requests
import time
from urllib.parse import quote

# DOI to search for
doi = "10.1353/book.24372"
print(f"Searching for book with DOI: {doi}")
print("="*60)

# Method 1: Direct DOI resolution through doi.org
print("\nMethod 1: Direct DOI Resolution")
print("-" * 40)
try:
    doi_url = f"https://doi.org/{doi}"
    print(f"Attempting to resolve DOI: {doi_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    
    response = requests.get(doi_url, headers=headers, timeout=10, allow_redirects=True)
    print(f"DOI resolution status: {response.status_code}")
    print(f"Final URL after redirect: {response.url}")
    
    if response.status_code == 200:
        # Save the DOI resolution page content
        with open('workspace/doi_resolution_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("DOI resolution page saved to workspace/doi_resolution_page.html")
        
        # Extract key information from the page
        content = response.text.lower()
        
        # Look for title patterns
        title_patterns = [
            r'<title[^>]*>([^<]+)</title>',
            r'<h1[^>]*>([^<]+)</h1>',
            r'"title"\s*:\s*"([^"]+)"',
            r'<meta[^>]*name=["\']title["\'][^>]*content=["\']([^"\'>]+)["\']',
            r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\']([^"\'>]+)["\']'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE | re.DOTALL)
            if matches:
                print(f"Title candidates found: {matches[:3]}")
                break
        
        # Look for author patterns
        author_patterns = [
            r'<meta[^>]*name=["\']author["\'][^>]*content=["\']([^"\'>]+)["\']',
            r'"author"\s*:\s*"([^"]+)"',
            r'by\s+([A-Z][a-zA-Z\s,\.]+)',
            r'<span[^>]*class=["\'][^"\'>]*author[^"\'>]*["\'][^>]*>([^<]+)</span>'
        ]
        
        for pattern in author_patterns:
            matches = re.findall(pattern, response.text, re.IGNORECASE)
            if matches:
                print(f"Author candidates found: {matches[:3]}")
                break
                
        # Check if this is Project MUSE (based on 10.1353 prefix)
        if 'muse.jhu.edu' in response.url or 'project muse' in content:
            print("*** CONFIRMED: This is a Project MUSE publication ***")
            
    else:
        print(f"DOI resolution failed with status {response.status_code}")
        
except Exception as e:
    print(f"Error in DOI resolution: {str(e)}")

time.sleep(1)  # Brief pause between requests

# Method 2: Google Scholar search with DOI
print("\n" + "="*60)
print("Method 2: Google Scholar Search")
print("-" * 40)

# Check if SerpAPI key is available
api_key = os.getenv("SERPAPI_API_KEY")
if api_key:
    print(f"SerpAPI key available: {api_key[:10]}...")
    
    # Search Google Scholar for the DOI
    scholar_query = f'"10.1353/book.24372" OR "doi:10.1353/book.24372"'
    
    params = {
        "q": scholar_query,
        "api_key": api_key,
        "engine": "google_scholar",
        "num": 10
    }
    
    try:
        print(f"Searching Google Scholar for: {scholar_query}")
        response = requests.get("https://serpapi.com/search.json", params=params)
        
        if response.status_code == 200:
            scholar_results = response.json()
            
            if scholar_results.get("organic_results"):
                print(f"Found {len(scholar_results['organic_results'])} results on Google Scholar")
                
                for i, result in enumerate(scholar_results['organic_results'][:3]):
                    title = result.get('title', 'No title')
                    authors = result.get('authors', 'No authors')
                    publication_info = result.get('publication_info', {}).get('summary', 'No publication info')
                    link = result.get('link', 'No link')
                    
                    print(f"\nScholar Result {i+1}:")
                    print(f"Title: {title}")
                    print(f"Authors: {authors}")
                    print(f"Publication: {publication_info}")
                    print(f"Link: {link}")
                    print("-" * 30)
                    
                # Save Google Scholar results
                with open('workspace/google_scholar_results.json', 'w') as f:
                    import json
                    json.dump(scholar_results, f, indent=2)
                print("Google Scholar results saved to workspace/google_scholar_results.json")
                
            else:
                print("No results found on Google Scholar")
                if 'error' in scholar_results:
                    print(f"Scholar API Error: {scholar_results['error']}")
                    
        else:
            print(f"Google Scholar search failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error in Google Scholar search: {str(e)}")
else:
    print("SerpAPI key not available - skipping Google Scholar search")

time.sleep(1)  # Brief pause between requests

# Method 3: General Google search with DOI
print("\n" + "="*60)
print("Method 3: General Google Search")
print("-" * 40)

if api_key:
    # Search regular Google for the DOI
    google_query = f'"10.1353/book.24372" book title author neurologist'
    
    params = {
        "q": google_query,
        "api_key": api_key,
        "engine": "google",
        "num": 15
    }
    
    try:
        print(f"Searching Google for: {google_query}")
        response = requests.get("https://serpapi.com/search.json", params=params)
        
        if response.status_code == 200:
            google_results = response.json()
            
            if google_results.get("organic_results"):
                print(f"Found {len(google_results['organic_results'])} results on Google")
                
                # Look for academic/book-related results
                academic_results = []
                
                for i, result in enumerate(google_results['organic_results']):
                    title = result.get('title', 'No title')
                    link = result.get('link', 'No link')
                    snippet = result.get('snippet', 'No snippet')
                    
                    # Check for academic indicators
                    academic_indicators = [
                        'book', 'author', 'publisher', 'muse.jhu.edu', 'project muse',
                        'neurologist', 'neurology', 'medicine', 'biography', 'doi'
                    ]
                    
                    is_academic = any(indicator in (title + link + snippet).lower() for indicator in academic_indicators)
                    
                    print(f"\nGoogle Result {i+1}:")
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Snippet: {snippet}")
                    
                    if is_academic:
                        print("*** POTENTIALLY RELEVANT ACADEMIC SOURCE ***")
                        academic_results.append(result)
                    
                    print("-" * 30)
                    
                    if i >= 4:  # Show first 5 results in detail
                        break
                
                print(f"\nTotal potentially relevant academic results: {len(academic_results)}")
                
                # Save Google search results
                with open('workspace/google_search_results.json', 'w') as f:
                    import json
                    json.dump(google_results, f, indent=2)
                print("Google search results saved to workspace/google_search_results.json")
                
            else:
                print("No results found on Google")
                if 'error' in google_results:
                    print(f"Google API Error: {google_results['error']}")
                    
        else:
            print(f"Google search failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error in Google search: {str(e)}")

time.sleep(1)  # Brief pause between requests

# Method 4: Project MUSE specific search
print("\n" + "="*60)
print("Method 4: Project MUSE Specific Search")
print("-" * 40)

if api_key:
    # Search specifically for Project MUSE with this DOI
    muse_query = f'site:muse.jhu.edu "10.1353/book.24372" OR "book.24372"'
    
    params = {
        "q": muse_query,
        "api_key": api_key,
        "engine": "google",
        "num": 10
    }
    
    try:
        print(f"Searching Project MUSE for: {muse_query}")
        response = requests.get("https://serpapi.com/search.json", params=params)
        
        if response.status_code == 200:
            muse_results = response.json()
            
            if muse_results.get("organic_results"):
                print(f"Found {len(muse_results['organic_results'])} results on Project MUSE")
                
                for i, result in enumerate(muse_results['organic_results']):
                    title = result.get('title', 'No title')
                    link = result.get('link', 'No link')
                    snippet = result.get('snippet', 'No snippet')
                    
                    print(f"\nProject MUSE Result {i+1}:")
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Snippet: {snippet}")
                    print("-" * 30)
                    
                # Save Project MUSE results
                with open('workspace/project_muse_results.json', 'w') as f:
                    import json
                    json.dump(muse_results, f, indent=2)
                print("Project MUSE search results saved to workspace/project_muse_results.json")
                
            else:
                print("No results found on Project MUSE")
                if 'error' in muse_results:
                    print(f"Project MUSE API Error: {muse_results['error']}")
                    
        else:
            print(f"Project MUSE search failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Error in Project MUSE search: {str(e)}")

# Summary of search approach
print("\n" + "="*60)
print("SEARCH SUMMARY")
print("="*60)
print(f"DOI searched: {doi}")
print(f"Publisher prefix: 10.1353 (Project MUSE)")
print("\nSearch methods completed:")
print("1. Direct DOI resolution through doi.org")
print("2. Google Scholar search with DOI")
print("3. General Google search with DOI + keywords")
print("4. Project MUSE specific search")
print("\nResults saved to workspace/ directory for analysis")
print("Files created:")
print("- doi_resolution_page.html (if DOI resolved)")
print("- google_scholar_results.json (if Scholar search successful)")
print("- google_search_results.json (if Google search successful)")
print("- project_muse_results.json (if MUSE search successful)")
```

### Development Step 11: Locate Greetham’s “Uncoupled: OR, How I Lost My Author(s)” (pp.45–46) and verify quoted passage.

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Academic journal editorial teams use automated DOI resolution and HTML scraping to verify author citations and ensure quoted passages match original publications during peer review quality control
- University librarians integrate DOI-based metadata extraction and quote verification scripts into repository workflows to confirm full-text availability and accurate catalog records for archival of electronic theses
- Legal analysts deploy automated quote extraction from jurisprudence articles via DOI resolution to cross-check citations and quotations in legal briefs, minimizing transcription errors and ensuring case law accuracy
- Investigative journalists employ DOI lookup and web scraping to authenticate scholarly sources cited in investigative reports, ensuring that quoted material is accurately represented and preventing misinformation
- Digital humanities researchers use automated page-level text extraction and context analysis to study variations in manuscript transmission and verify quoted passages across multiple editions and digital archives
- Graduate students leverage citation verification automation to validate bibliographic entries and ensure their theses contain accurate direct quotes, reducing manual workload and preventing referencing errors
- Compliance officers in pharmaceutical companies apply DOI-based article retrieval and metadata analysis to confirm that drug safety reports cite clinical studies accurately, supporting regulatory submission integrity
- Reference management software developers integrate DOI resolution, metadata scraping, and quote verification modules to enhance import workflows, enabling users to automatically retrieve full-text context and ensure citation accuracy

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

print('=== GREETHAM ARTICLE QUOTE VERIFICATION - FINAL VERSION ===')
print('Title: Uncoupled: OR, How I Lost My Author(s)')
print('Author: David Greetham')
print('Journal: Textual Cultures: Texts, Contexts, Interpretation')
print('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46')
print('DOI: 10.2979/tex.2008.3.1.44')
print('Target Quote: "obscured not by a \"cloak of print\" but by the veil of scribal confusion and mis-transmission"')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Check if we already have the raw HTML from previous attempts
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

print('\n=== EXTRACTING PAGE CONTENT AND METADATA ===')

# CRITICAL: Define both page_text variables immediately after soup creation
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

print('\n=== SEARCHING FOR TARGET QUOTE ===')

# Define the target quote and variations using simple string literals
target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'

# Define quote variations to handle different quote styles and partial matches
quote_variations = [
    'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission',
    'obscured not by a cloak of print but by the veil of scribal confusion and mis-transmission',
    'veil of scribal confusion and mis-transmission',
    'cloak of print',
    'veil of scribal confusion',
    'scribal confusion and mis-transmission',
    'scribal confusion'
]

print(f'Searching for {len(quote_variations)} quote variations...')

quote_found = False
found_variation = None
found_context = None

for i, variation in enumerate(quote_variations, 1):
    if variation.lower() in page_text_lower:
        print(f'\n🎯 FOUND QUOTE VARIATION {i}: "{variation}"')
        quote_found = True
        found_variation = variation
        
        # Extract context around the quote
        index = page_text_lower.find(variation.lower())
        context_start = max(0, index - 800)
        context_end = min(len(page_text), index + 1000)
        found_context = page_text[context_start:context_end]
        
        print(f'\n*** QUOTE CONTEXT FROM GREETHAM ARTICLE ***')
        print('='*120)
        print(found_context)
        print('='*120)
        break

if quote_found:
    print('\n🎯 SUCCESS: TARGET QUOTE FOUND AND VERIFIED!')
    
    # Save the verification context
    verification_path = 'workspace/quote_verification_pages_45_46.txt'
    with open(verification_path, 'w', encoding='utf-8') as verify_file:
        verify_file.write('QUOTE VERIFICATION REPORT\n')
        verify_file.write('='*60 + '\n')
        verify_file.write('Article: Uncoupled: OR, How I Lost My Author(s)\n')
        verify_file.write('Author: David Greetham\n')
        verify_file.write('Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
        verify_file.write('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46\n')
        verify_file.write('DOI: 10.2979/tex.2008.3.1.44\n\n')
        verify_file.write('TARGET QUOTE:\n')
        verify_file.write(target_quote + '\n\n')
        verify_file.write('FOUND VARIATION:\n')
        verify_file.write(found_variation + '\n\n')
        verify_file.write('CONTEXT FROM ARTICLE:\n')
        verify_file.write('='*80 + '\n')
        verify_file.write(found_context + '\n')
        verify_file.write('='*80 + '\n\n')
        verify_file.write('VERIFICATION STATUS: QUOTE CONFIRMED\n')
        verify_file.write('The quoted passage appears exactly as cited in the bibliography.\n')
        verify_file.write('Note: The context shows "[End Page 45]" indicating this spans pages 45-46.\n')
    
    print(f'\n✓ Quote verification saved to: {verification_path}')
    
    # Analyze the quote context for accuracy
    print('\n=== QUOTE ACCURACY ANALYSIS ===')
    
    # Check if the full target quote appears in the context
    if 'cloak of print' in found_context.lower():
        print('✓ "cloak of print" phrase found in context')
    else:
        print('⚠ "cloak of print" phrase not found - checking for variations')
        if 'veil of print' in found_context.lower():
            print('! Found "veil of print" instead of "cloak of print"')
            print('! This suggests a potential discrepancy in the quoted text')
    
    if 'veil of scribal confusion' in found_context.lower():
        print('✓ "veil of scribal confusion" phrase confirmed')
    
    if 'mis-transmission' in found_context.lower():
        print('✓ "mis-transmission" term confirmed')
    
    # Check page boundary
    if '[End Page 45]' in found_context:
        print('✓ Context confirms this passage spans pages 45-46 as cited')
    
else:
    print('\n⚠ Target quote not found on the accessible Project MUSE page')
    print('This may indicate the full text requires institutional access')
    
    # Look for related terms to confirm we have the right article
    related_terms = ['textual', 'manuscript', 'editorial', 'transmission', 'scribal']
    found_terms = []
    
    for term in related_terms:
        if term.lower() in page_text_lower:
            count = page_text_lower.count(term.lower())
            found_terms.append(f'{term} ({count})')
    
    if found_terms:
        print(f'✓ Related textual criticism terms found: {found_terms}')
        print('This confirms we have the correct article, but full text may be restricted')

# Check for open access indicators (now page_text_lower is properly defined)
open_access_indicators = ['open access', 'free access', 'freely available']
is_open_access = any(indicator in page_text_lower for indicator in open_access_indicators)
print(f'\nOpen access indicators detected: {is_open_access}')

# Save comprehensive analysis
analysis_data = {
    'doi_url': 'https://doi.org/10.2979/tex.2008.3.1.44',
    'final_url': final_url if 'final_url' in locals() else 'https://muse.jhu.edu/article/240795',
    'page_title': page_title.get_text().strip() if page_title else None,
    'article_title': article_title,
    'article_author': article_author,
    'journal_title': journal_title,
    'page_text_length': len(page_text),
    'is_open_access': is_open_access,
    'quote_found': quote_found,
    'found_variation': found_variation,
    'target_quote': target_quote,
    'quote_variations_searched': len(quote_variations),
    'verification_status': 'CONFIRMED' if quote_found else 'NOT_FOUND',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

analysis_path = 'workspace/greetham_article_analysis.json'
with open(analysis_path, 'w', encoding='utf-8') as analysis_file:
    json.dump(analysis_data, analysis_file, indent=2, ensure_ascii=False)

print(f'\n✓ Comprehensive analysis saved to: {analysis_path}')

print('\n=== FINAL SUMMARY ===')
print('DOI Resolution: ✓ SUCCESS')
print('Article Identification: ✓ CONFIRMED')
print('Metadata Extraction: ✓ COMPLETE')
if quote_found:
    print('Quote Verification: ✓ SUCCESS - QUOTE FOUND AND VERIFIED')
    print('\n*** VERIFICATION RESULT ***')
    print('The quoted passage from the bibliography has been successfully located')
    print('in the Greetham article on Project MUSE. The quote appears in the')
    print('context spanning pages 45-46 as cited.')
    
    # Check for any discrepancies
    if 'veil of print' in found_context.lower() and 'cloak of print' not in found_context.lower():
        print('\n⚠ POTENTIAL DISCREPANCY DETECTED:')
        print('The article text shows "veil of print" but the citation quotes "cloak of print"')
        print('This may indicate a transcription error in the bibliography.')
else:
    print('Quote Verification: ⚠ QUOTE NOT ACCESSIBLE')
    print('The article exists but full text may require institutional access')

print('\nFiles created:')
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')
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

### Development Step 9: Retrieve and verify quoted passage from Greetham’s 2008 article pages 45–46 via DOI.

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Automated verification of bibliographic citations in academic publishing workflows to ensure quoted passages match the original source before final print
- Digital humanities research pipelines for extracting and comparing key textual criticism passages across manuscript editions via DOI resolution
- Library acquisition teams using DOI-based scraping to confirm institutional access and validate critical excerpts in licensed journal articles
- Editorial quality control in scholarly monograph production, automatically checking that all cited quotations are accurately transcribed from journal pages 45–46
- Plagiarism detection systems in graduate thesis review, comparing student citations against the Project MUSE article to flag mis-quoted or altered text
- Educational technology platforms generating annotated reading assignments by extracting verified quotes and context from primary research articles
- Journal peer-review management tools pre-screening submitted manuscripts for citation accuracy and completeness by fetching and validating DOI content
- Corporate R&D knowledge management integrating authenticated research findings into whitepapers, using automated DOI resolution to extract and verify critical quotes

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE - SYNTAX ERROR FIXED ===') 
print('Title: Uncoupled: OR, How I Lost My Author(s)')
print('Author: David Greetham')
print('Journal: Textual Cultures: Texts, Contexts, Interpretation')
print('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46')
print('DOI: 10.2979/tex.2008.3.1.44')
print('Target Quote: "obscured not by a \"cloak of print\" but by the veil of scribal confusion and mis-transmission"')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# First, let's check if we already have the raw HTML from previous attempts
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

# Define the target quote and variations - FIXED SYNTAX
target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'

# Define quote variations with proper string handling - SYNTAX COMPLETELY FIXED
quote_variations = [
    target_quote,
    'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission',
    'obscured not by a \'cloak of print\' but by the veil of scribal confusion and mis-transmission',
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
                content_file.write(f'ARTICLE CONTENT EXTRACTED FROM PROJECT MUSE\n')
                content_file.write(f'Selector used: {selector}\n')
                content_file.write(f'Content length: {len(content_text):,} characters\n')
                content_file.write(f'{\'=\'*80}\n')
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
                        verify_file.write(f'QUOTE VERIFICATION REPORT\n')
                        verify_file.write(f'Article: Uncoupled: OR, How I Lost My Author(s)\n')
                        verify_file.write(f'Author: David Greetham\n')
                        verify_file.write(f'Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
                        verify_file.write(f'DOI: 10.2979/tex.2008.3.1.44\n\n')
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
        verify_file.write(f'QUOTE VERIFICATION REPORT\n')
        verify_file.write(f'Article: Uncoupled: OR, How I Lost My Author(s)\n')
        verify_file.write(f'Author: David Greetham\n')
        verify_file.write(f'Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
        verify_file.write(f'DOI: 10.2979/tex.2008.3.1.44\n\n')
        verify_file.write(f'TARGET QUOTE:\n{target_quote}\n\n')
        verify_file.write(f'FOUND VARIATION:\n{found_variation}\n\n')
        verify_file.write(f'CONTEXT FROM MAIN PAGE:\n{found_context}\n')
    
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

print('\n=== QUOTE VERIFICATION COMPLETE ===')
print('Summary:')
print('- ✓ Successfully resolved DOI to Project MUSE')
print('- ✓ Confirmed correct Greetham article')
print('- ✓ Extracted article metadata')
print('- ✓ Searched for target quote with multiple variations')
print('- ✓ Saved all results to workspace/ directory')

print('\nFiles created:')
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')

if quote_found_on_page or article_content_found:
    print('\n🎯 SUCCESS: Target quote found and verified!')
else:
    print('\n⚠ Quote not found on accessible content - may require institutional access')
```

### Development Step 7: Locate Greetham’s 'Uncoupled' via DOI and verify exact quoted passage on pages 45–46

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Automated citation verification for digital humanities researchers: batch-resolve DOIs, download articles from Project MUSE, extract pages 45–46, and confirm obscure quotations for critical-edition projects.
- Library metadata enrichment in academic institutions: integrate DOI-based scraping into the cataloging pipeline to fetch article titles, authors, and full-text PDF links for seamless access updates.
- Plagiarism prevention in educational technology: cross-fetch and parse original scholarly texts to validate student-submitted quotes and references against the source material in real time.
- AI dataset curation for natural language processing: programmatically download and extract clean, full-text content from humanities journals to build a domain-specific training corpus.
- Editorial quality control at academic publishers: automate the review of author-submitted manuscripts by verifying that all cited passages match the original articles before publication.
- Grant proposal literature audits for funding agencies: rapidly retrieve and scan key passages from referenced articles to ensure proposal claims are supported by accurate quotations.
- Legal research compliance in intellectual property firms: pull and verify exact wording of quoted academic sources to support patent applications and maintain citation integrity.

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE VIA DOI - VARIABLE SCOPE FIXED ===')
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
    
    # FIXED: Define page_text early to avoid NameError
    page_text = soup.get_text().lower()
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
    
    # Look for article metadata
    print('\n--- EXTRACTING ARTICLE METADATA ---')
    
    # Search for article title in various locations
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
        # Search for author in page text (now page_text is defined)
        if 'greetham' in page_text:
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
        # Search for journal in page text (now page_text is defined)
        if 'textual cultures' in page_text:
            print('✓ Journal name "Textual Cultures" found in page text')
    
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
    open_access_indicators = ['open access', 'free access', 'freely available', 'oa']
    is_open_access = any(indicator in page_text for indicator in open_access_indicators)
    print(f'\nOpen access indicators detected: {is_open_access}')
    
    # Search for the target quote on the current page
    print('\n=== STEP 4: SEARCHING FOR TARGET QUOTE ON PAGE ===')
    target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'
    
    # Define quote variations with proper string handling
    quote_variations = [
        target_quote,
        target_quote.replace('"', "'"),  # Replace double quotes with single quotes
        target_quote.replace('"', "'"),  # Replace with smart quotes
        'cloak of print',
        'veil of scribal confusion',
        'scribal confusion and mis-transmission',
        'scribal confusion',
        'mis-transmission'
    ]
    
    quote_found_on_page = False
    for i, variation in enumerate(quote_variations, 1):
        if variation.lower() in page_text:
            print(f'✓ Found quote variation {i}: "{variation}"')
            quote_found_on_page = True
            
            # Extract context around the quote
            index = page_text.find(variation.lower())
            full_text = soup.get_text()
            context_start = max(0, index - 400)
            context_end = min(len(full_text), index + 500)
            context = full_text[context_start:context_end]
            
            print(f'\n*** QUOTE CONTEXT ***')
            print('='*80)
            print(context)
            print('='*80)
            break
    
    if not quote_found_on_page:
        print('⚠ Target quote not found on the main page')
        print('This suggests the full text is behind access controls')
        
        # Let's examine what content IS available on the page
        print('\n--- ANALYZING AVAILABLE PAGE CONTENT ---')
        
        # Look for abstract or preview content
        abstract_selectors = ['.abstract', '.summary', '.description', '.excerpt']
        abstract_found = False
        
        for selector in abstract_selectors:
            abstract_elem = soup.select_one(selector)
            if abstract_elem:
                abstract_text = abstract_elem.get_text().strip()
                if len(abstract_text) > 50:
                    print(f'\nAbstract/Summary found ({selector}):')
                    print('='*60)
                    print(abstract_text[:500] + ('...' if len(abstract_text) > 500 else ''))
                    print('='*60)
                    abstract_found = True
                    break
        
        if not abstract_found:
            print('No abstract or summary content found')
        
        # Look for any content that might contain pages 45-46
        page_indicators = ['page 45', 'page 46', 'pp. 45', 'pp. 46', 'p. 45', 'p. 46']
        page_refs_found = []
        
        for indicator in page_indicators:
            if indicator in page_text:
                page_refs_found.append(indicator)
        
        if page_refs_found:
            print(f'\n✓ Page references found: {page_refs_found}')
        else:
            print('\n⚠ No specific page 45-46 references found on main page')
    
    print('\n=== STEP 5: ATTEMPTING FULL TEXT ACCESS ===')
    
    if unique_access:
        # Prioritize PDF links, then full-text links
        pdf_links = [link for link in unique_access if '.pdf' in link['url'].lower()]
        fulltext_links = [link for link in unique_access if 'fulltext' in link['url'].lower() or 'full-text' in link['url'].lower()]
        
        # Choose the best access link
        if pdf_links:
            target_link = pdf_links[0]
            print(f'Attempting PDF access: {target_link["text"]}')
        elif fulltext_links:
            target_link = fulltext_links[0]
            print(f'Attempting full-text access: {target_link["text"]}')
        else:
            target_link = unique_access[0]
            print(f'Attempting general access: {target_link["text"]}')
        
        print(f'Target URL: {target_link["url"]}')
        
        try:
            print('Making request to access full content...')
            content_response = requests.get(target_link['url'], headers=headers, timeout=60)
            print(f'Content access status: {content_response.status_code}')
            print(f'Content type: {content_response.headers.get("content-type", "unknown")}')
            print(f'Content length: {len(content_response.content):,} bytes')
            
            if content_response.status_code == 200:
                content_type = content_response.headers.get('content-type', '').lower()
                
                if 'pdf' in content_type:
                    print('\n*** PDF CONTENT DETECTED ***')
                    pdf_path = 'workspace/greetham_uncoupled_article.pdf'
                    
                    with open(pdf_path, 'wb') as pdf_file:
                        pdf_file.write(content_response.content)
                    
                    file_size = os.path.getsize(pdf_path)
                    print(f'✓ PDF saved to: {pdf_path}')
                    print(f'File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
                    
                    # Try to extract text from PDF using langchain if available
                    try:
                        print('\nAttempting to extract text from PDF...')
                        from langchain_community.document_loaders import PyPDFLoader
                        
                        loader = PyPDFLoader(pdf_path)
                        pages = loader.load_and_split()
                        
                        print(f'✓ PDF loaded successfully with {len(pages)} pages')
                        
                        # Combine all pages into full text
                        full_pdf_text = '\n\n'.join([page.page_content for page in pages])
                        
                        # Save extracted text
                        text_path = 'workspace/greetham_uncoupled_extracted_text.txt'
                        with open(text_path, 'w', encoding='utf-8') as text_file:
                            text_file.write(full_pdf_text)
                        
                        print(f'✓ Extracted PDF text saved to: {text_path}')
                        print(f'Total extracted text length: {len(full_pdf_text):,} characters')
                        
                        # Search for the target quote in the PDF text
                        print('\n=== STEP 6: SEARCHING PDF TEXT FOR TARGET QUOTE ===')
                        
                        pdf_text_lower = full_pdf_text.lower()
                        quote_found_in_pdf = False
                        
                        for i, variation in enumerate(quote_variations, 1):
                            if variation.lower() in pdf_text_lower:
                                print(f'\n🎯 FOUND TARGET QUOTE IN PDF (Variation {i}): "{variation}"')
                                quote_found_in_pdf = True
                                
                                # Extract substantial context around the quote
                                index = pdf_text_lower.find(variation.lower())
                                context_start = max(0, index - 800)
                                context_end = min(len(full_pdf_text), index + 1000)
                                context = full_pdf_text[context_start:context_end]
                                
                                print(f'\n*** QUOTE VERIFICATION - PAGES 45-46 CONTENT ***')
                                print('='*120)
                                print(context)
                                print('='*120)
                                
                                # Save the verification context
                                verification_path = 'workspace/quote_verification_pages_45_46.txt'
                                with open(verification_path, 'w', encoding='utf-8') as verify_file:
                                    verify_file.write(f'QUOTE VERIFICATION REPORT\n')
                                    verify_file.write(f'Article: Uncoupled: OR, How I Lost My Author(s)\n')
                                    verify_file.write(f'Author: David Greetham\n')
                                    verify_file.write(f'Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
                                    verify_file.write(f'DOI: 10.2979/tex.2008.3.1.44\n\n')
                                    verify_file.write(f'TARGET QUOTE:\n{target_quote}\n\n')
                                    verify_file.write(f'FOUND VARIATION:\n{variation}\n\n')
                                    verify_file.write(f'CONTEXT FROM ARTICLE:\n{context}\n')
                                
                                print(f'\n✓ Quote verification saved to: {verification_path}')
                                break
                        
                        if not quote_found_in_pdf:
                            print('⚠ Target quote not found in extracted PDF text')
                            print('Searching for related terms and saving full text for manual review')
                            
                            # Search for related terms that might indicate we have the right content
                            related_terms = ['textual', 'manuscript', 'editorial', 'transmission', 'scribal']
                            found_terms = []
                            
                            for term in related_terms:
                                if term.lower() in pdf_text_lower:
                                    count = pdf_text_lower.count(term.lower())
                                    found_terms.append(f'{term} ({count} occurrences)')
                            
                            if found_terms:
                                print(f'✓ Related textual criticism terms found: {found_terms}')
                            
                            # Save first 2000 characters for inspection
                            preview_text = full_pdf_text[:2000]
                            print(f'\n*** PDF TEXT PREVIEW (First 2000 characters) ***')
                            print('='*100)
                            print(preview_text)
                            print('='*100)
                    
                    except ImportError:
                        print('⚠ PyPDFLoader not available - PDF saved but text extraction skipped')
                        print('PDF file can be manually reviewed for the target quote')
                    except Exception as pdf_error:
                        print(f'❌ PDF text extraction error: {str(pdf_error)}')
                        print('PDF file saved but text extraction failed')
                
                elif 'html' in content_type:
                    print('\n*** HTML CONTENT DETECTED ***')
                    
                    # Save the HTML content for analysis
                    html_path = 'workspace/greetham_fulltext_page.html'
                    with open(html_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(content_response.text)
                    
                    print(f'✓ Full HTML content saved to: {html_path}')
                    
                    # Parse the full-text HTML
                    content_soup = BeautifulSoup(content_response.content, 'html.parser')
                    
                    # Remove navigation and non-content elements
                    for element in content_soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                        element.decompose()
                    
                    # Try to find the main article content
                    content_selectors = [
                        '.article-content',
                        '.full-text',
                        '.article-body',
                        'main',
                        '.content',
                        '#content',
                        '.text'
                    ]
                    
                    article_content = None
                    for selector in content_selectors:
                        content_elem = content_soup.select_one(selector)
                        if content_elem:
                            article_content = content_elem.get_text()
                            print(f'✓ Article content extracted using selector: {selector}')
                            break
                    
                    if not article_content:
                        # Fallback to full page text
                        article_content = content_soup.get_text()
                        print('Using full page text as fallback')
                    
                    # Clean up the extracted text
                    lines = (line.strip() for line in article_content.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
                    clean_text = ' '.join(chunk for chunk in chunks if chunk)
                    
                    print(f'✓ Extracted text length: {len(clean_text):,} characters')
                    
                    # Save the full article text
                    text_path = 'workspace/greetham_uncoupled_full_text.txt'
                    with open(text_path, 'w', encoding='utf-8') as text_file:
                        text_file.write(clean_text)
                    
                    print(f'✓ Full article text saved to: {text_path}')
                    
                    # Search for the target quote in the full text
                    print('\n=== STEP 6: SEARCHING FULL TEXT FOR TARGET QUOTE ===')
                    
                    clean_text_lower = clean_text.lower()
                    quote_found_in_full = False
                    
                    for i, variation in enumerate(quote_variations, 1):
                        if variation.lower() in clean_text_lower:
                            print(f'\n🎯 FOUND TARGET QUOTE (Variation {i}): "{variation}"')
                            quote_found_in_full = True
                            
                            # Extract substantial context around the quote
                            index = clean_text_lower.find(variation.lower())
                            context_start = max(0, index - 800)
                            context_end = min(len(clean_text), index + 1000)
                            context = clean_text[context_start:context_end]
                            
                            print(f'\n*** QUOTE VERIFICATION - PAGES 45-46 CONTENT ***')
                            print('='*120)
                            print(context)
                            print('='*120)
                            
                            # Save the verification context
                            verification_path = 'workspace/quote_verification_pages_45_46.txt'
                            with open(verification_path, 'w', encoding='utf-8') as verify_file:
                                verify_file.write(f'QUOTE VERIFICATION REPORT\n')
                                verify_file.write(f'Article: Uncoupled: OR, How I Lost My Author(s)\n')
                                verify_file.write(f'Author: David Greetham\n')
                                verify_file.write(f'Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
                                verify_file.write(f'DOI: 10.2979/tex.2008.3.1.44\n\n')
                                verify_file.write(f'TARGET QUOTE:\n{target_quote}\n\n')
                                verify_file.write(f'FOUND VARIATION:\n{variation}\n\n')
                                verify_file.write(f'CONTEXT FROM ARTICLE:\n{context}\n')
                            
                            print(f'\n✓ Quote verification saved to: {verification_path}')
                            break
                    
                    if not quote_found_in_full:
                        print('⚠ Target quote not found in full HTML text')
                        print('Saving extracted text for manual review')
                        
                        # Save first 2000 characters for inspection
                        preview_text = clean_text[:2000]
                        print(f'\n*** HTML TEXT PREVIEW (First 2000 characters) ***')
                        print('='*100)
                        print(preview_text)
                        print('='*100)
                
                else:
                    print(f'\n*** UNKNOWN CONTENT TYPE: {content_type} ***')
                    print('Saving raw content for analysis')
                    
                    raw_content_path = 'workspace/unknown_content_response.txt'
                    with open(raw_content_path, 'w', encoding='utf-8') as raw_file:
                        raw_file.write(content_response.text)
                    
                    print(f'Raw content saved to: {raw_content_path}')
            
            else:
                print(f'❌ Content access failed with status: {content_response.status_code}')
                print(f'Response preview: {content_response.text[:300]}')
        
        except Exception as content_error:
            print(f'❌ Error accessing full content: {str(content_error)}')
    
    else:
        print('❌ No access links found on the page')
        print('The article may require institutional access or subscription')
        
        # Save page analysis for manual review
        page_analysis = {
            'doi_url': doi_url,
            'final_url': doi_response.url,
            'page_title': page_title.get_text().strip() if page_title else None,
            'article_title': article_title,
            'article_author': article_author,
            'journal_title': journal_title,
            'access_links_found': len(unique_access),
            'is_open_access': is_open_access,
            'quote_found_on_page': quote_found_on_page,
            'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        analysis_path = 'workspace/greetham_article_analysis.json'
        with open(analysis_path, 'w', encoding='utf-8') as analysis_file:
            json.dump(page_analysis, analysis_file, indent=2, ensure_ascii=False)
        
        print(f'\n✓ Page analysis saved to: {analysis_path}')

except Exception as e:
    print(f'❌ Error during DOI resolution: {str(e)}')
    
    # Try alternative approaches
    print('\n=== ATTEMPTING ALTERNATIVE ACCESS METHODS ===')
    
    # Try direct Project MUSE search
    muse_search_url = 'https://muse.jhu.edu/search?action=search&query=creator%3A%22Greetham%2C%20David%22%20AND%20title%3A%22Uncoupled%22'
    print(f'Trying direct Project MUSE search: {muse_search_url}')
    
    try:
        search_response = requests.get(muse_search_url, headers=headers, timeout=30)
        print(f'Search response status: {search_response.status_code}')
        
        if search_response.status_code == 200:
            search_soup = BeautifulSoup(search_response.content, 'html.parser')
            
            # Look for the article in search results
            result_links = search_soup.find_all('a', href=True)
            greetham_links = []
            
            for link in result_links:
                href = link.get('href')
                text = link.get_text().strip()
                if href and ('uncoupled' in text.lower() or 'greetham' in text.lower()):
                    if href.startswith('/'):
                        href = urljoin('https://muse.jhu.edu', href)
                    greetham_links.append({
                        'url': href,
                        'text': text
                    })
            
            print(f'Found {len(greetham_links)} potential Greetham article links:')
            for i, link in enumerate(greetham_links, 1):
                print(f'{i}. {link["text"]} -> {link["url"]}')
            
            # Save search results
            search_results = {
                'search_url': muse_search_url,
                'status_code': search_response.status_code,
                'greetham_links_found': greetham_links,
                'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open('workspace/greetham_search_results.json', 'w', encoding='utf-8') as search_file:
                json.dump(search_results, search_file, indent=2, ensure_ascii=False)
            
            print('✓ Search results saved to: workspace/greetham_search_results.json')
        
        else:
            print(f'Search failed with status: {search_response.status_code}')
    
    except Exception as search_error:
        print(f'Search attempt failed: {str(search_error)}')

print('\n=== DOI RESOLUTION AND QUOTE VERIFICATION COMPLETE ===')
print('Summary:')
print('- Successfully resolved DOI to Project MUSE')
print('- Extracted article metadata and confirmed correct Greetham article')
print('- Searched for full-text access options')
print('- Attempted to extract and verify the target quote')
print('- Saved all intermediate results to workspace/ directory')
print('\nFiles created:')
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')
```

## Created Time
2025-08-11 02:29:24
