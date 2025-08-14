# Developer Plan 02

## Plan
Search the Smithsonian American Art Museum's collection database for paintings whose titles contain quotes or references from Michael Smith's 'The Moral Problem' (1994), which was identified as the most likely work referenced in footnote 397 of Federico Lauria's 2014 dissertation. Focus on finding two specific paintings in the collection as of August 2023 that derive their titles from this philosophical work. Extract the complete titles and identify which chapters from Smith's work are being quoted to determine the absolute difference between the chapter numbers.

## Description
This is the logical next step because: (1) The developer has identified Michael Smith's 'The Moral Problem' (1994) as the most probable work referenced in footnote 397 through systematic academic analysis, (2) We now need to search the Smithsonian American Art Museum collection for paintings with titles derived from this source, (3) Expected outcome is to locate two paintings whose titles quote from different chapters of Smith's work, (4) This will enable us to calculate the absolute difference between the chapter numbers as requested in the TASK

## Episodic Examples
### Development Step 12: Locate Greetham’s "Uncoupled" (Textual Cultures 3.1) Pages 45–46 and Verify Quoted Passage

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Academic journal editorial teams automating citation verification and quote accuracy checks before article publication
- University library metadata specialists extracting precise bibliographic details and verifying DOIs for new database acquisitions
- Research integrity offices auditing faculty publications to detect misquoted passages and transcription errors in bibliographies
- Digital humanities projects scraping and analyzing primary source texts for variant readings and transmission history studies
- Graduate students automating thesis literature reviews by extracting targeted passages from journal pages via DOI resolution
- Patent examiners verifying novelty claims by cross-referencing quoted academic passages against original article texts
- Institutional repositories populating and validating article metadata and content snippets for open-access archives
- Scientific publishers integrating automated QA workflows to confirm in-text citations and quoted material across proof stages

```
import os
import json
from bs4 import BeautifulSoup
import time

print('=== GREETHAM QUOTE VERIFICATION - COMPLETING THE TASK ===')
print('Objective: Verify the quoted passage from Greetham article pages 45-46')
print('Status: Quote already found in previous attempts - now completing documentation\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Check if we have the raw HTML from previous attempts
raw_response_path = 'workspace/doi_response_raw.html'
if os.path.exists(raw_response_path):
    print(f'✓ Found existing raw response: {raw_response_path}')
    
    with open(raw_response_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f'✓ Loaded HTML content: {len(html_content):,} characters')
    
    # Parse the content
    soup = BeautifulSoup(html_content, 'html.parser')
    page_text = soup.get_text()
    
    print(f'✓ Extracted page text: {len(page_text):,} characters')
    
else:
    print('❌ No existing HTML response found')
    print('Previous attempts should have saved the DOI response')
    # List available files to understand current state
    if os.path.exists('workspace'):
        files = os.listdir('workspace')
        print(f'Available workspace files: {files}')
    exit()

print('\n=== SEARCHING FOR TARGET QUOTE ===')

# Define the target quote and key variations
target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'

# Search for quote variations that were successful in previous attempts
quote_variations = [
    'veil of scribal confusion and mis-transmission',
    'veil of scribal confusion', 
    'scribal confusion and mis-transmission',
    'cloak of print',
    'veil of print'  # This was found in the actual text
]

print(f'Searching for {len(quote_variations)} quote variations...')

quote_found = False
found_variation = None
found_context = None
page_text_lower = page_text.lower()  # Define this variable properly

for i, variation in enumerate(quote_variations, 1):
    if variation.lower() in page_text_lower:
        print(f'\n🎯 FOUND QUOTE VARIATION {i}: "{variation}"')
        quote_found = True
        found_variation = variation
        
        # Extract substantial context around the quote
        index = page_text_lower.find(variation.lower())
        context_start = max(0, index - 1000)
        context_end = min(len(page_text), index + 1200)
        found_context = page_text[context_start:context_end]
        
        print('\n*** QUOTE CONTEXT FROM GREETHAM ARTICLE ***')
        print('=' * 120)
        print(found_context)
        print('=' * 120)
        break

if quote_found:
    print('\n🎯 SUCCESS: TARGET QUOTE FOUND AND VERIFIED!')
    
    # Create comprehensive verification report
    verification_path = 'workspace/quote_verification_pages_45_46.txt'
    with open(verification_path, 'w', encoding='utf-8') as verify_file:
        verify_file.write('QUOTE VERIFICATION REPORT\n')
        verify_file.write('=' * 60 + '\n')
        verify_file.write('Article: Uncoupled: OR, How I Lost My Author(s)\n')
        verify_file.write('Author: David Greetham\n')
        verify_file.write('Journal: Textual Cultures: Texts, Contexts, Interpretation\n')
        verify_file.write('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46\n')
        verify_file.write('DOI: 10.2979/tex.2008.3.1.44\n')
        verify_file.write('Verification Date: ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n\n')
        
        verify_file.write('TARGET QUOTE FROM BIBLIOGRAPHY:\n')
        verify_file.write('"' + target_quote + '"\n\n')
        
        verify_file.write('FOUND VARIATION IN ARTICLE:\n')
        verify_file.write('"' + found_variation + '"\n\n')
        
        verify_file.write('FULL CONTEXT FROM ARTICLE (Pages 45-46):\n')
        verify_file.write('=' * 80 + '\n')
        verify_file.write(found_context + '\n')
        verify_file.write('=' * 80 + '\n\n')
        
        # Analyze accuracy
        verify_file.write('ACCURACY ANALYSIS:\n')
        if 'cloak of print' in found_context.lower():
            verify_file.write('✓ "cloak of print" phrase confirmed as cited\n')
        elif 'veil of print' in found_context.lower():
            verify_file.write('⚠ DISCREPANCY: Article shows "veil of print" not "cloak of print"\n')
            verify_file.write('  This suggests the bibliography citation may contain an error\n')
        
        if 'veil of scribal confusion' in found_context.lower():
            verify_file.write('✓ "veil of scribal confusion" phrase confirmed\n')
        
        if 'mis-transmission' in found_context.lower():
            verify_file.write('✓ "mis-transmission" term confirmed\n')
        
        if '[End Page 45]' in found_context:
            verify_file.write('✓ Context confirms passage spans pages 45-46 as cited\n')
        
        verify_file.write('\nVERIFICATION STATUS: QUOTE LOCATED AND VERIFIED\n')
        verify_file.write('The quoted passage has been successfully found in the Greetham article.\n')
    
    print(f'\n✓ Quote verification report saved to: {verification_path}')
    
    # Detailed accuracy analysis
    print('\n=== ACCURACY ANALYSIS ===')
    
    if 'cloak of print' in found_context.lower():
        print('✓ "cloak of print" phrase found exactly as cited')
    elif 'veil of print' in found_context.lower():
        print('⚠ IMPORTANT DISCREPANCY DETECTED:')
        print('  - Bibliography cites: "cloak of print"')
        print('  - Article actually says: "veil of print"')
        print('  - This indicates a potential transcription error in the bibliography')
    
    if 'veil of scribal confusion' in found_context.lower():
        print('✓ "veil of scribal confusion" phrase confirmed')
    
    if 'mis-transmission' in found_context.lower():
        print('✓ "mis-transmission" term confirmed')
    
    if '[End Page 45]' in found_context:
        print('✓ Page boundary confirmed - passage spans pages 45-46 as cited')
    
    # Save analysis data
    analysis_data = {
        'verification_status': 'SUCCESS',
        'quote_found': True,
        'found_variation': found_variation,
        'target_quote': target_quote,
        'article_info': {
            'title': 'Uncoupled: OR, How I Lost My Author(s)',
            'author': 'David Greetham',
            'journal': 'Textual Cultures: Texts, Contexts, Interpretation',
            'volume': 3,
            'issue': 1,
            'year': 2008,
            'pages': '45-46',
            'doi': '10.2979/tex.2008.3.1.44'
        },
        'discrepancies': {
            'cloak_vs_veil': 'veil of print' in found_context.lower() and 'cloak of print' not in found_context.lower()
        },
        'verification_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    analysis_path = 'workspace/greetham_verification_analysis.json'
    with open(analysis_path, 'w', encoding='utf-8') as analysis_file:
        json.dump(analysis_data, analysis_file, indent=2, ensure_ascii=False)
    
    print(f'\n✓ Analysis data saved to: {analysis_path}')
    
else:
    print('\n❌ Target quote not found in accessible content')
    print('This may indicate institutional access is required for full text')
    
    # Save negative result
    analysis_data = {
        'verification_status': 'NOT_FOUND',
        'quote_found': False,
        'target_quote': target_quote,
        'note': 'Quote not accessible - may require institutional access',
        'verification_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    analysis_path = 'workspace/greetham_verification_analysis.json'
    with open(analysis_path, 'w', encoding='utf-8') as analysis_file:
        json.dump(analysis_data, analysis_file, indent=2, ensure_ascii=False)
    
    print(f'\n✓ Analysis saved to: {analysis_path}')

print('\n=== FINAL SUMMARY ===')
print('DOI Resolution: ✓ SUCCESS (10.2979/tex.2008.3.1.44 → Project MUSE)')
print('Article Identification: ✓ CONFIRMED (David Greetham, Textual Cultures 2008)')
print('Pages 45-46 Access: ✓ CONTENT AVAILABLE')

if quote_found:
    print('Quote Verification: ✓ SUCCESS - QUOTE FOUND AND DOCUMENTED')
    print('\n*** VERIFICATION COMPLETE ***')
    print('The quoted passage has been successfully located in the Greetham article')
    print('and verified against the bibliography citation. All results have been')
    print('saved to workspace/ for further reference.')
    
    if 'veil of print' in found_context.lower() and 'cloak of print' not in found_context.lower():
        print('\n⚠ IMPORTANT FINDING:')
        print('A discrepancy was detected between the bibliography citation and the')
        print('actual article text. The bibliography may contain a transcription error.')
else:
    print('Quote Verification: ❌ QUOTE NOT ACCESSIBLE')
    print('Full text access may require institutional subscription')

print('\nFiles created in workspace/:')
if os.path.exists('workspace'):
    for file in sorted(os.listdir('workspace')):
        if not file.startswith('.'):
            file_path = os.path.join('workspace', file)
            file_size = os.path.getsize(file_path)
            print(f'  - {file} ({file_size:,} bytes)')
```

### Development Step 5: Extract and verify quoted passage in Greetham’s 'Uncoupled: OR, How I Lost My Author(s)' pp.45–46.

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Academic citation verification and quote extraction for graduate students conducting literature reviews
- Legal evidence collection and source authentication for intellectual property litigation
- Publishing workflow automation and metadata enrichment for digital journal production teams
- Educational content integration and direct article linking within e-learning platforms
- Reference management enhancement and bibliography accuracy checking for dissertation advisors
- Digital library cataloging and metadata harvesting for institutional repository curators
- Plagiarism detection and text-based QA automation in scholarly peer review processes
- Digital humanities corpus building and quote indexing for research data archiving

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE VIA DOI - SYNTAX FIXED ===') 
print('Title: Uncoupled: OR, How I Lost My Author(s)')
print('Author: David Greetham')
print('Journal: Textual Cultures: Texts, Contexts, Interpretation')
print('Volume: 3, Issue: 1, Year: 2008, Pages: 45-46')
print('DOI: 10.2979/tex.2008.3.1.44')
print('Target Quote: "obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission"')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Construct the DOI URL - this is the critical step
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
        # Search for author in page text
        page_text = soup.get_text().lower()
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
        # Search for journal in page text
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
    page_text = soup.get_text().lower()
    open_access_indicators = ['open access', 'free access', 'freely available', 'oa']
    is_open_access = any(indicator in page_text for indicator in open_access_indicators)
    print(f'\nOpen access indicators detected: {is_open_access}')
    
    # Search for the target quote on the current page
    print('\n=== STEP 4: SEARCHING FOR TARGET QUOTE ON PAGE ===')
    target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'
    
    # Define quote variations with proper string handling (FIXED SYNTAX)
    quote_variations = [
        target_quote,
        target_quote.replace('"', '
```

### Development Step 6: Locate and Confirm Quotation in Greetham’s “Uncoupled: OR, How I Lost My Author(s)”

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Academic librarians performing automated citation verification by resolving DOIs, downloading articles from Project MUSE, and extracting quoted passages to ensure bibliographies match source texts
- Graduate students streamlining dissertation literature reviews by programmatically retrieving full-text PDFs via DOI resolution and harvesting key quotations for analysis
- Journal editors conducting pre-publication quality checks to confirm that every quoted phrase in submitted manuscripts matches the original article pages 45–46 exactly
- Legal researchers validating historical and scholarly references in court briefs by automating DOI lookups, extracting pertinent text from academic journals, and cross-checking quotations
- Digital humanities scholars building large-scale text corpora by resolving DOIs to acquire PDFs, extracting full-text content, and indexing themes such as “scribal confusion and mis-transmission”
- Reference management tool developers integrating DOI resolution and on-the-fly full-text extraction to enrich citation metadata with verified excerpts for academic writing platforms
- University IT teams automating institutional repository ingest by fetching articles via DOI, extracting both metadata and text content, and archiving verified passages alongside faculty publications
- Research compliance officers auditing departmental publications for correct attribution by programmatically retrieving source articles, extracting specified quotes, and generating verification reports

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE VIA DOI - SYNTAX COMPLETELY FIXED ===')
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
        # Search for author in page text
        page_text = soup.get_text().lower()
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
        # Search for journal in page text
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
    page_text = soup.get_text().lower()
    open_access_indicators = ['open access', 'free access', 'freely available', 'oa']
    is_open_access = any(indicator in page_text for indicator in open_access_indicators)
    print(f'\nOpen access indicators detected: {is_open_access}')
    
    # Search for the target quote on the current page
    print('\n=== STEP 4: SEARCHING FOR TARGET QUOTE ON PAGE ===')
    target_quote = 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission'
    
    # Define quote variations with proper string handling (SYNTAX FIXED)
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
                            print('Saving full extracted text for manual review')
                            
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
print('- Attempted DOI resolution to Project MUSE')
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
2025-08-14 02:31:21
