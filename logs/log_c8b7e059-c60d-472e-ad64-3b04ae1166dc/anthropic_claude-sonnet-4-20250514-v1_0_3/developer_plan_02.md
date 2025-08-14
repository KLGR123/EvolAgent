# Developer Plan 02

## Plan
Extract and analyze footnote 397 from the downloaded Federico Lauria dissertation PDF (workspace/logic_liver_dissertation_1.pdf) to identify the specific work it references. Parse the complete footnote content to determine which literary work, book, or source is cited that could serve as the origin for painting titles in the Smithsonian American Art Museum collection. Focus on identifying works that would likely contain chapter-based content suitable for painting title sources.

## Description
This is the necessary next step because: (1) We have successfully located and downloaded Lauria's 2014 dissertation but need to extract the specific content of footnote 397, (2) Previous search established the connection between footnote 397 and Smithsonian painting titles but we need the actual referenced work, (3) Expected outcome is to identify the specific literary or scholarly work cited in footnote 397 that serves as the source for the painting titles, (4) This moves us toward identifying the chapters that contain the painting titles so we can calculate the absolute difference between chapter numbers

## Episodic Examples
### Development Step 9: Download Westerink’s "A Dark Trace" from Project MUSE and Extract Chapter 2’s Influential Author

**Description**: Access and download the full text of 'A Dark Trace: Sigmund Freud on the Sense of Guilt' by H. Westerink from Project MUSE using DOI 10.1353/book.24372. Since the book was confirmed to be open access, retrieve the complete text and save it to workspace/dark_trace_freud_book.pdf or appropriate format. Focus on locating and extracting Chapter 2 content to identify the author who influenced Freud's belief in 'endopsychic myths'. If the full book is not directly downloadable, extract Chapter 2 specifically or access the book's table of contents to determine the exact chapter title and content structure.

**Use Cases**:
- Legal due diligence in corporate mergers: automatically download open-access regulatory codes in PDF, search for “antitrust” and “competition” term variations, extract and summarize context to identify potential deal blockers.
- Pharmaceutical literature review automation: fetch clinical trial protocols via DOI, load full-text PDFs, search for “double-blind” and “placebo” mentions, and extract methodological passages along with author names for evidence synthesis.
- Patent portfolio analysis for semiconductor R&D: retrieve patent documents from public repositories, scan PDFs for “heterojunction” and “quantum well” variants, extract inventor citations and contextual explanations to map technology lineage.
- Historical philosophy research on Nietzsche and Kant: access digitized editions of 19th-century works, locate references to “categorical imperative” or “will to power,” and extract surrounding paragraphs to trace cross-author influences.
- Competitive intelligence from SEC filings: download publicly available 10-K and 10-Q reports, search for “risk factor,” “liquidity risk,” and “market volatility” variations, and pull relevant excerpts for financial analysis dashboards.
- Academic curriculum design from open textbooks: ingest complete PDF textbooks via DOIs, locate chapter summaries or “learning objectives” headings, extract and compile structured outlines for course syllabi.
- Investigative journalism document mining: import leaked policy PDFs, search for “whistleblower,” “confidential,” and “internal memo” terms, extract context with names and dates to support storytelling.
- Compliance monitoring in healthcare: load clinical guideline PDFs, scan for “contraindication,” “adverse effect,” and “off-label” variations, and extract detailed sections with authoring bodies for automated policy updates.

```
from langchain_community.document_loaders import PyPDFLoader
import os
import json

print('=== SEARCHING ENTIRE BOOK FOR "ENDOPSYCHIC MYTHS" REFERENCES ===')
print('Objective: Since Chapter 2 did not contain "endopsychic" references, search the complete book to locate this specific term and identify the influencing author\n')

# Load the PDF and search the entire document
workspace_files = os.listdir('workspace')
pdf_files = [f for f in workspace_files if f.endswith('.pdf')]

if pdf_files:
    pdf_path = os.path.join('workspace', pdf_files[0])
    print(f'Searching entire PDF: {pdf_path}')
    
    try:
        # Load the complete PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        print(f'✓ PDF loaded successfully')
        print(f'Total pages to search: {len(pages)}')
        
        # Combine all pages into full text
        full_text = '\n\n'.join([page.page_content for page in pages])
        print(f'Total document length: {len(full_text):,} characters')
        
        # Search for "endopsychic" variations
        endopsychic_variations = [
            'endopsychic myth',
            'endopsychic myths',
            'endopsychic',
            'endo-psychic',
            'endopsychical'
        ]
        
        print('\n=== SEARCHING FOR ENDOPSYCHIC VARIATIONS ===')
        
        found_endopsychic = False
        full_text_lower = full_text.lower()
        
        for variation in endopsychic_variations:
            count = full_text_lower.count(variation.lower())
            if count > 0:
                print(f'✓ Found "{variation}": {count} occurrences')
                found_endopsychic = True
                
                # Extract all positions for this variation
                positions = []
                start = 0
                while True:
                    pos = full_text_lower.find(variation.lower(), start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + 1
                
                print(f'\n--- EXTRACTING ALL "{variation.upper()}" REFERENCES ({len(positions)} found) ---')
                
                for i, pos in enumerate(positions, 1):
                    # Extract substantial context around each occurrence
                    context_start = max(0, pos - 1000)
                    context_end = min(len(full_text), pos + 1200)
                    context = full_text[context_start:context_end]
                    
                    # Determine which page this occurs on
                    char_count = 0
                    page_num = 0
                    for page_idx, page in enumerate(pages):
                        if char_count + len(page.page_content) >= pos:
                            page_num = page_idx + 1
                            break
                        char_count += len(page.page_content) + 2  # +2 for \n\n separator
                    
                    print(f'\n🎯 REFERENCE {i} - Position {pos} (Page ~{page_num}):')
                    print('='*120)
                    print(context)
                    print('='*120)
                    
                    # Analyze this passage for author influences
                    context_lower = context.lower()
                    potential_authors = [
                        'jung', 'carl jung', 'c.g. jung', 'c. g. jung',
                        'nietzsche', 'friedrich nietzsche', 'f. nietzsche',
                        'schopenhauer', 'arthur schopenhauer', 'a. schopenhauer',
                        'kant', 'immanuel kant', 'i. kant',
                        'darwin', 'charles darwin', 'c. darwin',
                        'hegel', 'georg hegel', 'g.w.f. hegel',
                        'goethe', 'johann wolfgang von goethe',
                        'lamarck', 'jean-baptiste lamarck'
                    ]
                    
                    mentioned_authors = []
                    for author in potential_authors:
                        if author in context_lower:
                            mentioned_authors.append(author)
                    
                    if mentioned_authors:
                        print(f'\n*** AUTHORS MENTIONED IN THIS PASSAGE: {[author.title() for author in mentioned_authors]} ***')
                        
                        # Look for specific influence language
                        influence_phrases = [
                            'influenced by', 'influence of', 'influenced freud',
                            'borrowed from', 'adopted from', 'derived from',
                            'took from', 'learned from', 'inspired by',
                            'following', 'based on', 'according to'
                        ]
                        
                        found_influence_language = []
                        for phrase in influence_phrases:
                            if phrase in context_lower:
                                found_influence_language.append(phrase)
                        
                        if found_influence_language:
                            print(f'🔍 INFLUENCE LANGUAGE DETECTED: {found_influence_language}')
                            print('\n🎯 THIS PASSAGE LIKELY CONTAINS THE ANSWER! 🎯')
                        
                        # Look for direct statements about endopsychic myths
                        myth_context_phrases = [
                            'concept of endopsychic', 'idea of endopsychic', 'notion of endopsychic',
                            'endopsychic concept', 'endopsychic idea', 'endopsychic notion',
                            'belief in endopsychic', 'theory of endopsychic'
                        ]
                        
                        found_myth_context = []
                        for phrase in myth_context_phrases:
                            if phrase in context_lower:
                                found_myth_context.append(phrase)
                        
                        if found_myth_context:
                            print(f'💡 ENDOPSYCHIC CONCEPT LANGUAGE: {found_myth_context}')
                    
                    else:
                        print('\nNo specific authors mentioned in this immediate passage')
                        print('Searching for author names in broader context...')
                        
                        # Expand search area for author names
                        expanded_start = max(0, pos - 2000)
                        expanded_end = min(len(full_text), pos + 2000)
                        expanded_context = full_text[expanded_start:expanded_end]
                        expanded_lower = expanded_context.lower()
                        
                        broader_authors = []
                        for author in potential_authors:
                            if author in expanded_lower:
                                broader_authors.append(author)
                        
                        if broader_authors:
                            print(f'Authors in broader context: {[author.title() for author in broader_authors]}')
                    
                    print(f'\n{"-"*120}\n')
            else:
                print(f'✗ "{variation}": Not found')
        
        if not found_endopsychic:
            print('\n⚠ No "endopsychic" variations found in the entire document')
            print('The term may be referenced differently or may not be the exact phrase used')
            
            # Search for related mythological concepts that might be the actual term
            print('\n=== SEARCHING FOR ALTERNATIVE MYTHOLOGICAL CONCEPTS ===')
            
            alternative_terms = [
                'unconscious myth',
                'psychic myth',
                'mental myth',
                'psychological myth',
                'inner myth',
                'primitive myth',
                'ancestral memory',
                'collective unconscious',
                'phylogenetic',
                'archaic heritage',
                'primal fantasies',
                'inherited memory'
            ]
            
            found_alternatives = []
            
            for term in alternative_terms:
                count = full_text_lower.count(term.lower())
                if count > 0:
                    found_alternatives.append((term, count))
                    print(f'✓ Found "{term}": {count} occurrences')
            
            if found_alternatives:
                print(f'\n=== EXAMINING TOP ALTERNATIVE CONCEPTS ===')
                
                # Focus on the most promising alternative (highest count)
                top_alternative = max(found_alternatives, key=lambda x: x[1])
                term, count = top_alternative
                
                print(f'\nExamining most frequent alternative: "{term}" ({count} occurrences)')
                
                positions = []
                start = 0
                while True:
                    pos = full_text_lower.find(term.lower(), start)
                    if pos == -1:
                        break
                    positions.append(pos)
                    start = pos + 1
                
                # Show first few occurrences
                for i, pos in enumerate(positions[:3], 1):
                    context_start = max(0, pos - 800)
                    context_end = min(len(full_text), pos + 1000)
                    context = full_text[context_start:context_end]
                    
                    # Determine page number
                    char_count = 0
                    page_num = 0
                    for page_idx, page in enumerate(pages):
                        if char_count + len(page.page_content) >= pos:
                            page_num = page_idx + 1
                            break
                        char_count += len(page.page_content) + 2
                    
                    print(f'\nAlternative Reference {i} - "{term}" (Page ~{page_num}):')
                    print('='*100)
                    print(context)
                    print('='*100)
                    
                    # Check for author influences
                    context_lower = context.lower()
                    mentioned_authors = []
                    for author in ['jung', 'nietzsche', 'schopenhauer', 'kant', 'darwin', 'lamarck']:
                        if author in context_lower:
                            mentioned_authors.append(author)
                    
                    if mentioned_authors:
                        print(f'\nAuthors mentioned: {[a.title() for a in mentioned_authors]}')
                    
                    print(f'\n{"-"*100}\n')
        
        # Also search for direct references to key authors with mythological context
        print('\n=== SEARCHING FOR AUTHORS WITH MYTHOLOGICAL/INHERITANCE CONTEXT ===')
        
        key_authors_with_context = [
            ('jung', ['myth', 'mythology', 'collective', 'archetype']),
            ('lamarck', ['inheritance', 'inherited', 'acquired', 'transmission']),
            ('darwin', ['inheritance', 'heredity', 'evolution', 'acquired']),
            ('nietzsche', ['myth', 'mythology', 'cultural', 'psychological'])
        ]
        
        for author, context_terms in key_authors_with_context:
            author_positions = []
            start = 0
            while True:
                pos = full_text_lower.find(author.lower(), start)
                if pos == -1:
                    break
                author_positions.append(pos)
                start = pos + 1
            
            if author_positions:
                print(f'\n--- {author.upper()} REFERENCES WITH MYTHOLOGICAL CONTEXT ---')
                
                relevant_passages = []
                for pos in author_positions:
                    context_start = max(0, pos - 500)
                    context_end = min(len(full_text), pos + 700)
                    context = full_text[context_start:context_end]
                    context_lower = context.lower()
                    
                    # Check if this passage contains relevant mythological context
                    has_context = any(term in context_lower for term in context_terms)
                    if has_context:
                        relevant_passages.append((pos, context))
                
                if relevant_passages:
                    print(f'Found {len(relevant_passages)} relevant passages for {author.title()}:')
                    
                    for i, (pos, context) in enumerate(relevant_passages[:2], 1):
                        # Determine page
                        char_count = 0
                        page_num = 0
                        for page_idx, page in enumerate(pages):
                            if char_count + len(page.page_content) >= pos:
                                page_num = page_idx + 1
                                break
                            char_count += len(page.page_content) + 2
                        
                        print(f'\n{author.title()} Passage {i} (Page ~{page_num}):')
                        print('='*90)
                        print(context)
                        print('='*90)
                else:
                    print(f'No mythological context found for {author.title()}')
        
        # Save comprehensive search results
        search_results = {
            'search_objective': 'Find author who influenced Freud\'s belief in "endopsychic myths"',
            'document_stats': {
                'total_pages': len(pages),
                'total_characters': len(full_text)
            },
            'endopsychic_search': {
                'variations_searched': endopsychic_variations,
                'found_endopsychic': found_endopsychic,
                'total_occurrences': sum(full_text_lower.count(v.lower()) for v in endopsychic_variations)
            },
            'alternative_terms_found': found_alternatives if 'found_alternatives' in locals() else [],
            'search_timestamp': '2025-01-21 13:00:00'
        }
        
        results_file = 'workspace/complete_book_endopsychic_search_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(search_results, f, indent=2, ensure_ascii=False)
        
        print(f'\n*** COMPLETE BOOK SEARCH RESULTS ***')
        print(f'✓ Searched {len(pages)} pages ({len(full_text):,} characters)')
        print(f'✓ Endopsychic references found: {found_endopsychic}')
        
        if found_endopsychic:
            print('🎯 SUCCESS: Found "endopsychic" references in the book!')
            print('The extracted passages above should reveal the author who influenced Freud')
        else:
            print('⚠ "Endopsychic" not found - the term may be referenced differently')
            if 'found_alternatives' in locals() and found_alternatives:
                print(f'Alternative concepts found: {[term for term, count in found_alternatives]}')
        
        print(f'✓ Complete search results saved to: {results_file}')
        
    except Exception as e:
        print(f'❌ Error during complete book search: {str(e)}')

else:
    print('❌ No PDF files found in workspace')

print('\n=== COMPLETE BOOK SEARCH FINISHED ===')
print('Objective: Locate the specific author who influenced Freud\'s concept of "endopsychic myths"')
print('Status: Comprehensive search of entire book completed')
```

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

## Created Time
2025-08-14 04:48:22
