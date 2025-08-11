# Developer Plan 04

## Plan
Extract and analyze footnote 397 specifically from the downloaded Federico Lauria 2014 publication 'The Logic of the Liver: A Deontic View of the Intentionality of Desire' (workspace/lauria_2014_complete.pdf). Locate the exact text of footnote 397, identify what literary work it references, then search the Smithsonian American Art Museum's collection for paintings whose titles are quotations from that same referenced work. Once the paintings are identified, determine which chapters their titles quote from and calculate the absolute difference between those chapter numbers.

## Description
This is the critical next step because: (1) The previous research successfully located and downloaded Lauria's complete 2014 publication containing footnote 397, with 2,343 footnote patterns identified including the target footnote, (2) We now have direct access to the specific footnote content that will reveal the literary work referenced, (3) Expected outcome is to extract the exact reference from footnote 397, identify the corresponding Smithsonian paintings with chapter-based titles from that work, and calculate the absolute difference between their chapter numbers, (4) This will complete the TASK by connecting the dissertation footnote to the specific paintings and providing the final numerical answer requested

## Episodic Examples
### Development Step 4: Extract Pages 45–46 from Greetham’s “Uncoupled: OR, How I Lost My Author(s)” to Verify Quotation

**Description**: Search for the academic article 'Uncoupled: OR, How I Lost My Author(s)' by David Greetham published in Textual Cultures: Texts, Contexts, Interpretation, vol. 3 no. 1, 2008, pages 45-46. Use the provided DOI 10.2979/tex.2008.3.1.44 to locate the article on Project MUSE or through DOI resolution. Extract the complete text from pages 45-46 to verify if the quoted passage 'obscured not by a "cloak of print" but by the veil of scribal confusion and mis-transmission' appears exactly as cited in the bibliography.

**Use Cases**:
- Academic publisher’s editorial team automating DOI resolution and web scraping to verify exact quoted passages in manuscript submissions, catching miscitations before print
- Digital humanities research lab batch-processing Project MUSE articles via DOI and BeautifulSoup to build a corpus on scribal transmission themes for thematic analysis
- University library IT department harvesting metadata and PDF links from Project MUSE through DOI-based retrieval to enrich the institutional catalog automatically
- Graduate students using a scriptable tool to fetch and confirm precise quotes from literary theory articles during thesis writing, ensuring citation accuracy and completeness
- Reference management software developers integrating DOI resolution and HTML parsing to auto-populate article metadata and flag mismatched quotes for Zotero or EndNote users
- Legal scholars conducting intertextuality studies by scraping academic journal pages via DOI to collect full-text evidence of cited scholarly passages in case filings
- Data scientists constructing an NLP dataset of scholarly quotations on publication practices by programmatically extracting text from DOI-resolved journal articles

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING GREETHAM ARTICLE VIA DOI - SYNTAX CORRECTED ===') 
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

### Development Step 29: Extract Emily Midkiff’s June 2014 Fafnir article and identify shared critical word in dragon quotes

**Description**: Access Emily Midkiff's June 2014 article in the Fafnir journal to extract the full text and identify the specific word that was quoted from two different authors expressing distaste for the nature of dragon depictions. Parse the article content systematically to locate quotes from multiple authors that contain the same critical word about dragon portrayals.

**Use Cases**:
- Comparative mythology research and motif extraction from scholarly dragon folklore texts
- Academic literature analysis and recurring keyword identification for graduate thesis writing
- Digital humanities workshops and hands-on text mining of dragon portrayal critiques
- Fantasy blog content creation and scholarly quote curation for marketing campaigns
- Library archival systems and metadata enrichment using thematic keyword extraction from journals
- Educational resource development and automated compilation of critical dragon imagery quotes
- Conference abstract support and cross-author sentiment summarization on dragon representations

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time
import re

print('=== FIXING VARIABLE ERROR AND EXTRACTING MIDKIFF ARTICLE ===\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Target URL for Fafnir 2/2014 issue
target_issue_url = 'https://journal.finfar.org/journal/archive/fafnir-22014/'
print(f'Target issue: Fafnir 2/2014')
print(f'URL: {target_issue_url}\n')

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

print('=== STEP 1: ACCESSING FAFNIR 2/2014 ISSUE PAGE ===\n')

try:
    print(f'Requesting: {target_issue_url}')
    issue_response = requests.get(target_issue_url, headers=headers, timeout=30)
    print(f'Response status: {issue_response.status_code}')
    print(f'Content length: {len(issue_response.content):,} bytes')
    print(f'Content type: {issue_response.headers.get("Content-Type", "unknown")}\n')
    
    if issue_response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(issue_response.content, 'html.parser')
        
        # Get page title
        page_title = soup.find('title')
        if page_title:
            print(f'Page title: {page_title.get_text().strip()}')
        
        # Extract all text content for analysis
        page_text = soup.get_text()
        print(f'Total page text length: {len(page_text):,} characters\n')
        
        # Confirm this page contains Emily Midkiff
        if 'midkiff' in page_text.lower():
            print('✓ Confirmed: Page contains "Midkiff"')
            
            # Find the exact context where Midkiff appears
            midkiff_indices = []
            text_lower = page_text.lower()
            start = 0
            while True:
                index = text_lower.find('midkiff', start)
                if index == -1:
                    break
                midkiff_indices.append(index)
                start = index + 1
            
            print(f'Found "Midkiff" at {len(midkiff_indices)} positions in the text')
            
            # Show context around each occurrence
            for i, index in enumerate(midkiff_indices, 1):
                context_start = max(0, index - 150)
                context_end = min(len(page_text), index + 150)
                context = page_text[context_start:context_end].replace('\n', ' ').strip()
                print(f'\nOccurrence {i} context:')
                print(f'...{context}...')
        else:
            print('⚠ Warning: "Midkiff" not found in page text')
        
        print('\n=== STEP 2: EXTRACTING ALL ARTICLE LINKS FROM THE ISSUE PAGE ===\n')
        
        # Find all links on the page
        all_links = soup.find_all('a', href=True)
        print(f'Total links found on page: {len(all_links)}')
        
        # Filter links that might be articles - FIXED VARIABLE ERROR
        potential_article_links = []
        
        for link in all_links:
            href = link.get('href')
            text = link.get_text().strip()  # FIXED: was undefined link_text
            
            # Skip empty links or navigation links
            if not href or not text:
                continue
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = urljoin('https://journal.finfar.org', href)
            elif not href.startswith('http'):
                href = urljoin(target_issue_url, href)
            
            # Look for links that might be articles (contain meaningful text)
            if len(text) > 10 and not any(nav_word in text.lower() for nav_word in ['home', 'archive', 'about', 'contact', 'menu', 'navigation', 'search']):
                potential_article_links.append({
                    'text': text,
                    'url': href,
                    'has_midkiff': 'midkiff' in text.lower()
                })
        
        print(f'Potential article links found: {len(potential_article_links)}')
        
        # Show all potential article links
        print('\n--- All Potential Article Links ---')
        for i, link in enumerate(potential_article_links, 1):
            marker = '*** MIDKIFF ***' if link['has_midkiff'] else ''
            print(f'{i:2d}. {marker}')
            print(f'    Text: {link["text"][:100]}...' if len(link['text']) > 100 else f'    Text: {link["text"]}')
            print(f'    URL:  {link["url"]}')
            print()
        
        # Find Emily Midkiff's specific article
        midkiff_links = [link for link in potential_article_links if link['has_midkiff']]
        
        if midkiff_links:
            print(f'=== FOUND {len(midkiff_links)} MIDKIFF ARTICLE LINK(S) ===\n')
            
            # Use the first Midkiff link (should be the main one)
            target_article = midkiff_links[0]
            print(f'Selected article:')
            print(f'Title: {target_article["text"]}')
            print(f'URL: {target_article["url"]}\n')
            
            print('=== STEP 3: ACCESSING EMILY MIDKIFF\'S ARTICLE ===\n')
            
            try:
                print(f'Accessing article: {target_article["url"]}')
                article_response = requests.get(target_article['url'], headers=headers, timeout=30)
                print(f'Article response status: {article_response.status_code}')
                print(f'Article content length: {len(article_response.content):,} bytes\n')
                
                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    
                    # Get article title from the page
                    article_title_elem = article_soup.find('title')
                    if article_title_elem:
                        article_title = article_title_elem.get_text().strip()
                        print(f'Article page title: {article_title}')
                    
                    # Remove scripts, styles, and navigation elements
                    for element in article_soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'menu']):
                        element.decompose()
                    
                    # Try multiple selectors to find the main article content
                    content_selectors = [
                        '.article-content',
                        '.article-body', 
                        '.entry-content',
                        '.post-content',
                        '.content',
                        'main',
                        '#content',
                        '.text',
                        'article'
                    ]
                    
                    article_content = None
                    used_selector = None
                    
                    for selector in content_selectors:
                        content_elem = article_soup.select_one(selector)
                        if content_elem:
                            article_content = content_elem.get_text()
                            used_selector = selector
                            print(f'✓ Article content extracted using selector: {selector}')
                            break
                    
                    if not article_content:
                        # Fallback to full page text
                        article_content = article_soup.get_text()
                        used_selector = 'full_page_fallback'
                        print('Using full page text as fallback')
                    
                    # Clean up the extracted text
                    lines = (line.strip() for line in article_content.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
                    clean_content = ' '.join(chunk for chunk in chunks if chunk)
                    
                    print(f'✓ Cleaned article text: {len(clean_content):,} characters\n')
                    
                    # Save the full article text
                    article_text_file = os.path.join(workspace, 'midkiff_fafnir_article_full_text.txt')
                    with open(article_text_file, 'w', encoding='utf-8') as f:
                        f.write(f'Title: {target_article["text"]}\n')
                        f.write(f'URL: {target_article["url"]}\n')
                        f.write(f'Extraction method: {used_selector}\n')
                        f.write(f'Extracted: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
                        f.write('=' * 80 + '\n\n')
                        f.write(clean_content)
                    
                    print(f'✓ Full article text saved to: {article_text_file}')
                    
                    # Save raw HTML for backup
                    article_html_file = os.path.join(workspace, 'midkiff_fafnir_article_raw.html')
                    with open(article_html_file, 'w', encoding='utf-8') as f:
                        f.write(article_response.text)
                    
                    print(f'✓ Raw article HTML saved to: {article_html_file}\n')
                    
                    print('=== STEP 4: ANALYZING ARTICLE FOR DRAGON CRITICISM QUOTES ===\n')
                    
                    # Look for quoted text using multiple quote patterns
                    quote_patterns = [
                        r'"([^"]{15,400})"',  # Standard double quotes
                        r'"([^"]{15,400})
```

### Development Step 36: Locate Common Negative Term in Two Authors’ Dragon-Depiction Quotes in Midkiff’s June 2014 Fafnir Article

**Description**: Access Emily Midkiff's June 2014 article in the Fafnir journal to extract the full text and identify the specific word that was quoted from two different authors expressing distaste for the nature of dragon depictions. Parse the article content systematically to locate quotes from multiple authors that contain the same critical word about dragon portrayals.

**Use Cases**:
- Academic literary research and systematic extraction of thematic quotes from niche fantasy journals to analyze evolving criticism of dragon portrayals
- Digital humanities archiving and building a searchable database of verbatim passages on mythological creatures for cross‐textual studies
- Editorial quality assurance and automated validation of quote attributions in small press publications to maintain citation accuracy
- Sentiment trend analysis and identification of recurring critical descriptors in cultural criticism articles for media monitoring teams
- Library digitization workflows and conversion of legacy journal issues into clean, searchable text repositories for institutional archives
- Market intelligence gathering and tracking negative audience feedback on fantasy IPs by mining specialist journal commentaries
- Automated citation indexing and metadata extraction for streamlined literature reviews in graduate‐level folklore and mythology research
- Educational content curation and assembly of critical perspectives on dragon tropes to support university seminar discussions

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
import time

print('=== EMILY MIDKIFF ARTICLE EXTRACTION - CLEAN IMPLEMENTATION ===')
print('Objective: Extract full text and identify shared critical word about dragon depictions\n')

# Ensure workspace exists
workspace = 'workspace'
os.makedirs(workspace, exist_ok=True)

# Target URL for Fafnir 2/2014 issue
target_issue_url = 'https://journal.finfar.org/journal/archive/fafnir-22014/'
print(f'Target issue: Fafnir 2/2014')
print(f'URL: {target_issue_url}\n')

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

print('=== STEP 1: ACCESSING FAFNIR 2/2014 ISSUE PAGE ===')

try:
    print(f'Requesting: {target_issue_url}')
    issue_response = requests.get(target_issue_url, headers=headers, timeout=30)
    print(f'Response status: {issue_response.status_code}')
    print(f'Content length: {len(issue_response.content):,} bytes')
    print(f'Content type: {issue_response.headers.get("Content-Type", "unknown")}\n')
    
    if issue_response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(issue_response.content, 'html.parser')
        
        # Get page title
        page_title = soup.find('title')
        if page_title:
            print(f'Page title: {page_title.get_text().strip()}')
        
        # Extract all text content for analysis
        page_text = soup.get_text()
        print(f'Total page text length: {len(page_text):,} characters\n')
        
        # Confirm this page contains Emily Midkiff
        if 'midkiff' in page_text.lower():
            print('✓ Confirmed: Page contains "Midkiff"')
            
            # Find the exact context where Midkiff appears
            midkiff_indices = []
            text_lower = page_text.lower()
            start = 0
            while True:
                index = text_lower.find('midkiff', start)
                if index == -1:
                    break
                midkiff_indices.append(index)
                start = index + 1
            
            print(f'Found "Midkiff" at {len(midkiff_indices)} positions in the text')
            
            # Show context around each occurrence
            for i, index in enumerate(midkiff_indices, 1):
                context_start = max(0, index - 150)
                context_end = min(len(page_text), index + 150)
                context = page_text[context_start:context_end].replace('\n', ' ').strip()
                print(f'\nOccurrence {i} context:')
                print(f'...{context}...')
        else:
            print('⚠ Warning: "Midkiff" not found in page text')
        
        print('\n=== STEP 2: EXTRACTING ALL ARTICLE LINKS FROM THE ISSUE PAGE ===')
        
        # Find all links on the page
        all_links = soup.find_all('a', href=True)
        print(f'Total links found on page: {len(all_links)}')
        
        # Filter links that might be articles - FIXED variable scoping
        potential_article_links = []
        
        for link in all_links:
            link_href = link.get('href')
            link_text = link.get_text().strip()
            
            # Skip empty links or navigation links
            if not link_href or not link_text:
                continue
            
            # Convert relative URLs to absolute
            if link_href.startswith('/'):
                link_href = urljoin('https://journal.finfar.org', link_href)
            elif not link_href.startswith('http'):
                link_href = urljoin(target_issue_url, link_href)
            
            # Look for links that might be articles (contain meaningful text)
            nav_words = ['home', 'archive', 'about', 'contact', 'menu', 'navigation', 'search']
            if len(link_text) > 10 and not any(nav_word in link_text.lower() for nav_word in nav_words):
                potential_article_links.append({
                    'text': link_text,
                    'url': link_href,
                    'has_midkiff': 'midkiff' in link_text.lower()
                })
        
        print(f'Potential article links found: {len(potential_article_links)}')
        
        # Show all potential article links
        print('\n--- All Potential Article Links ---')
        for i, link in enumerate(potential_article_links, 1):
            marker = '*** MIDKIFF ***' if link['has_midkiff'] else ''
            print(f'{i:2d}. {marker}')
            if len(link['text']) > 100:
                print(f'    Text: {link["text"][:100]}...')
            else:
                print(f'    Text: {link["text"]}')
            print(f'    URL:  {link["url"]}')
            print()
        
        # Find Emily Midkiff's specific article
        midkiff_links = [link for link in potential_article_links if link['has_midkiff']]
        
        if midkiff_links:
            print(f'=== FOUND {len(midkiff_links)} MIDKIFF ARTICLE LINK(S) ===')
            
            # Use the first Midkiff link (should be the main one)
            target_article = midkiff_links[0]
            print(f'Selected article:')
            print(f'Title: {target_article["text"]}')
            print(f'URL: {target_article["url"]}\n')
            
            print('=== STEP 3: ACCESSING EMILY MIDKIFF\'S ARTICLE ===')
            
            try:
                print(f'Accessing article: {target_article["url"]}')
                article_response = requests.get(target_article['url'], headers=headers, timeout=30)
                print(f'Article response status: {article_response.status_code}')
                print(f'Article content length: {len(article_response.content):,} bytes\n')
                
                if article_response.status_code == 200:
                    article_soup = BeautifulSoup(article_response.content, 'html.parser')
                    
                    # Get article title from the page
                    article_title_elem = article_soup.find('title')
                    if article_title_elem:
                        article_title = article_title_elem.get_text().strip()
                        print(f'Article page title: {article_title}')
                    
                    # Remove scripts, styles, and navigation elements
                    for element in article_soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'menu']):
                        element.decompose()
                    
                    # Try multiple selectors to find the main article content
                    content_selectors = [
                        '.article-content',
                        '.article-body', 
                        '.entry-content',
                        '.post-content',
                        '.content',
                        'main',
                        '#content',
                        '.text',
                        'article'
                    ]
                    
                    article_content = None
                    used_selector = None
                    
                    for selector in content_selectors:
                        content_elem = article_soup.select_one(selector)
                        if content_elem:
                            article_content = content_elem.get_text()
                            used_selector = selector
                            print(f'✓ Article content extracted using selector: {selector}')
                            break
                    
                    if not article_content:
                        # Fallback to full page text
                        article_content = article_soup.get_text()
                        used_selector = 'full_page_fallback'
                        print('Using full page text as fallback')
                    
                    # Clean up the extracted text
                    lines = (line.strip() for line in article_content.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
                    clean_content = ' '.join(chunk for chunk in chunks if chunk)
                    
                    print(f'✓ Cleaned article text: {len(clean_content):,} characters\n')
                    
                    # Save the full article text
                    article_text_file = os.path.join(workspace, 'midkiff_fafnir_article_full_text.txt')
                    with open(article_text_file, 'w', encoding='utf-8') as f:
                        f.write(f'Title: {target_article["text"]}\n')
                        f.write(f'URL: {target_article["url"]}\n')
                        f.write(f'Extraction method: {used_selector}\n')
                        f.write(f'Extracted: {time.strftime("%Y-%m-%d %H:%M:%S")}\n')
                        f.write('=' * 80 + '\n\n')
                        f.write(clean_content)
                    
                    print(f'✓ Full article text saved to: {article_text_file}')
                    
                    # Save raw HTML for backup
                    article_html_file = os.path.join(workspace, 'midkiff_fafnir_article_raw.html')
                    with open(article_html_file, 'w', encoding='utf-8') as f:
                        f.write(article_response.text)
                    
                    print(f'✓ Raw article HTML saved to: {article_html_file}\n')
                    
                    print('=== STEP 4: ANALYZING ARTICLE FOR DRAGON CRITICISM QUOTES ===')
                    
                    # Simple quote extraction using basic string operations
                    print('Searching for quoted passages in the article...')
                    
                    # Find all text between various quote marks - using simple approach
                    all_quotes = []
                    
                    # Method 1: Split by double quotes and take every other piece
                    double_quote_parts = clean_content.split('"')
                    for i in range(1, len(double_quote_parts), 2):  # Take odd indices (quoted content)
                        quote_text = double_quote_parts[i].strip()
                        if len(quote_text) >= 15:  # Only consider substantial quotes
                            all_quotes.append({
                                'text': quote_text,
                                'method': 'double_quotes'
                            })
                    
                    # Method 2: Look for smart quotes (opening and closing)
                    # Split by opening smart quote
                    smart_open_parts = clean_content.split('
```

## Created Time
2025-08-11 09:36:40
