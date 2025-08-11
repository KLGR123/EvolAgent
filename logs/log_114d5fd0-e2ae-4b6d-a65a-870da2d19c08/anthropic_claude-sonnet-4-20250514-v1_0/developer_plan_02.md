# Developer Plan 02

## Plan
Access and download the full text of 'The Responsibility of Intellectuals' (DOI 10.2307/j.ctv9b2xdv) from JSTOR or UCL Press. Since this is a 2019 UCL Press publication available through JSTOR, retrieve the complete book content and save it to the workspace. Focus on locating page 11, identifying the second-to-last paragraph on that page, and extracting the specific endnote referenced in that paragraph. The endnote should contain a Wikipedia article citation with a November access date - extract the exact day of the month when the Wikipedia article was accessed.

## Description
This is the necessary next step because: (1) We have successfully identified the book as 'The Responsibility of Intellectuals' published by UCL Press in 2019 and available through JSTOR, (2) The previous search established the book's bibliographic details but we need the actual content to analyze page 11's endnotes, (3) Expected outcome is to obtain the full book text and locate the specific endnote containing the Wikipedia access date in November, (4) This directly addresses the TASK requirement to find the day of the month when the Wikipedia article was accessed according to the endnote in the second-to-last paragraph of page 11

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

### Development Step 7: Download Chapter 2 of Westerink’s A Dark Trace to Identify Freud’s Endopsychic Myths Influence

**Description**: Access and download the full text of 'A Dark Trace: Sigmund Freud on the Sense of Guilt' by H. Westerink from Project MUSE using DOI 10.1353/book.24372. Since the book was confirmed to be open access, retrieve the complete text and save it to workspace/dark_trace_freud_book.pdf or appropriate format. Focus on locating and extracting Chapter 2 content to identify the author who influenced Freud's belief in 'endopsychic myths'. If the full book is not directly downloadable, extract Chapter 2 specifically or access the book's table of contents to determine the exact chapter title and content structure.

**Use Cases**:
- Psychoanalytic historian extracting Chapter 2 from an open-access Project MUSE monograph to identify philosophical influences on Freud’s “endopsychic myths” for a peer-reviewed article
- Legal scholarship librarian automating retrieval and parsing of open‐access constitutional law treatises to extract specific amendment analysis chapters for case brief citations
- Data journalism team downloading and parsing UN open‐access climate reports to extract the policy chapter on carbon-emission targets for an interactive web visualization
- Pharmaceutical R&D analysts retrieving and analyzing methodology chapters from open‐access clinical trial reports to standardize meta-analysis protocols in drug development studies
- Marketing insights department automating extraction of consumer-behavior chapters from open‐access business strategy books to inform a new brand-campaign pitch
- Financial compliance officers downloading and segmenting open‐access regulatory frameworks to extract risk-management chapters for annual audit and policy updates
- University digital library curators indexing open‐access theses by extracting abstracts and methodology sections to enhance repository metadata and searchability
- Software integration engineers retrieving open‐access API specification PDFs to extract protocol chapters for building automated integration and deployment pipelines

```
from langchain_community.document_loaders import PyPDFLoader
import os
import json

print('=== PARSING DOWNLOADED PDF TO EXTRACT CHAPTER 2 CONTENT ===')
print('Objective: Extract Chapter 2 "Dark Traces" from the downloaded PDF to find the author who influenced Freud\'s "endopsychic myths"\n')

# First, let's check what PDF files we have in the workspace
workspace_files = os.listdir('workspace')
pdf_files = [f for f in workspace_files if f.endswith('.pdf')]

print(f'Available PDF files in workspace: {pdf_files}')

# Use the main PDF file that was successfully downloaded
if pdf_files:
    pdf_path = os.path.join('workspace', pdf_files[0])  # Use first PDF found
    print(f'Using PDF file: {pdf_path}')
    
    # Check file size to confirm it's the full book
    file_size = os.path.getsize(pdf_path)
    print(f'PDF file size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
    
    if file_size > 1000000:  # More than 1MB suggests full book
        print('✓ File size indicates this is likely the complete book')
    else:
        print('⚠ File size is smaller than expected for a full book')
else:
    print('❌ No PDF files found in workspace')
    print('Available files:')
    for file in workspace_files:
        print(f'  - {file}')
    exit()

print('\n=== LOADING AND PARSING PDF WITH LANGCHAIN ===')

try:
    # Load the PDF using LangChain's PyPDFLoader
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    
    print(f'✓ PDF successfully loaded')
    print(f'Total pages: {len(pages)}')
    
    if len(pages) == 0:
        print('❌ No pages found in PDF file')
        exit()
    
    # Get the first few pages to understand the structure
    print('\n=== ANALYZING PDF STRUCTURE ===')
    
    for i in range(min(5, len(pages))):
        page_content = pages[i].page_content.strip()
        print(f'\nPage {i+1} (first 200 characters):')
        print(f'  Content length: {len(page_content)} characters')
        print(f'  Preview: "{page_content[:200]}..."')
    
    # Look for the table of contents to locate Chapter 2
    print('\n=== SEARCHING FOR TABLE OF CONTENTS AND CHAPTER 2 ===')
    
    toc_page = None
    chapter_2_start_page = None
    
    # Search for table of contents and chapter references
    for i, page in enumerate(pages):
        page_text = page.page_content.lower()
        
        # Look for table of contents
        if 'contents' in page_text or 'table of contents' in page_text:
            if not toc_page:
                toc_page = i + 1
                print(f'Table of contents found on page {toc_page}')
        
        # Look for Chapter 2 start
        chapter_indicators = ['chapter 2', 'chapter two', 'dark traces']
        for indicator in chapter_indicators:
            if indicator in page_text:
                # Check if this looks like the start of Chapter 2 (not just a reference)
                if len(page.page_content.strip()) > 500:  # Substantial content
                    if not chapter_2_start_page:
                        chapter_2_start_page = i + 1
                        print(f'Chapter 2 content appears to start on page {chapter_2_start_page}')
                        print(f'  Indicator found: "{indicator}"')
                        break
    
    # If we found the table of contents, examine it more closely
    if toc_page:
        print(f'\n=== EXAMINING TABLE OF CONTENTS (Page {toc_page}) ===')
        toc_content = pages[toc_page - 1].page_content  # Convert to 0-indexed
        print(f'TOC content ({len(toc_content)} characters):')
        print(toc_content)
        
        # Look for page numbers for Chapter 2
        toc_lines = toc_content.split('\n')
        for line in toc_lines:
            line_lower = line.lower()
            if 'chapter 2' in line_lower or 'dark traces' in line_lower:
                print(f'\nChapter 2 TOC entry: "{line.strip()}"')
                
                # Try to extract page number
                import re
                page_numbers = re.findall(r'\b(\d{1,3})\b', line)
                if page_numbers:
                    potential_start_page = int(page_numbers[-1])  # Usually the last number is the page
                    print(f'Chapter 2 appears to start on page {potential_start_page} (from TOC)')
                    
                    # Update our chapter start if we found it from TOC
                    if not chapter_2_start_page and potential_start_page <= len(pages):
                        chapter_2_start_page = potential_start_page
    
    # Extract Chapter 2 content
    if chapter_2_start_page:
        print(f'\n=== EXTRACTING CHAPTER 2 CONTENT (Starting from page {chapter_2_start_page}) ===')
        
        # Determine the end page for Chapter 2
        chapter_2_end_page = None
        
        # Look for Chapter 3 start to determine where Chapter 2 ends
        for i in range(chapter_2_start_page, len(pages)):
            page_text = pages[i].page_content.lower()
            if 'chapter 3' in page_text or 'chapter three' in page_text:
                chapter_2_end_page = i
                print(f'Chapter 3 appears to start on page {i + 1}, so Chapter 2 ends on page {i}')
                break
        
        # If no Chapter 3 found, extract a reasonable number of pages (typically 15-25 pages per chapter)
        if not chapter_2_end_page:
            chapter_2_end_page = min(len(pages), chapter_2_start_page + 20)
            print(f'Chapter 3 not clearly identified, extracting through page {chapter_2_end_page}')
        
        # Extract the chapter content
        chapter_2_pages = pages[chapter_2_start_page - 1:chapter_2_end_page]  # Convert to 0-indexed
        chapter_2_text = '\n\n'.join([page.page_content for page in chapter_2_pages])
        
        print(f'\nChapter 2 extracted:')
        print(f'  Pages: {chapter_2_start_page} to {chapter_2_end_page}')
        print(f'  Total pages: {len(chapter_2_pages)}')
        print(f'  Total text length: {len(chapter_2_text):,} characters')
        print(f'\nFirst 500 characters of Chapter 2:')
        print(f'"{chapter_2_text[:500]}..."')
        
        # Now search for "endopsychic myths" and related terms
        print('\n=== SEARCHING FOR "ENDOPSYCHIC MYTHS" AND RELATED TERMS ===')
        
        search_terms = [
            'endopsychic myth',
            'endopsychic',
            'myth',
            'mythology',
            'jung',
            'carl jung',
            'nietzsche', 
            'schopenhauer',
            'kant',
            'darwin',
            'influenced',
            'influence'
        ]
        
        found_terms = {}
        for term in search_terms:
            count = chapter_2_text.lower().count(term.lower())
            if count > 0:
                found_terms[term] = count
                print(f'✓ Found "{term}": {count} occurrences')
        
        if found_terms:
            print(f'\n=== EXTRACTING KEY PASSAGES ABOUT ENDOPSYCHIC MYTHS ===')
            
            # Focus on "endopsychic" if found
            endopsychic_terms = [term for term in found_terms if 'endopsychic' in term.lower()]
            
            if endopsychic_terms:
                print(f'Extracting passages containing "endopsychic" terms: {endopsychic_terms}')
                
                chapter_2_lower = chapter_2_text.lower()
                
                for term in endopsychic_terms:
                    positions = []
                    start = 0
                    while True:
                        pos = chapter_2_lower.find(term.lower(), start)
                        if pos == -1:
                            break
                        positions.append(pos)
                        start = pos + 1
                    
                    print(f'\n--- PASSAGES CONTAINING "{term.upper()}" ({len(positions)} occurrences) ---')
                    
                    for i, pos in enumerate(positions, 1):
                        # Extract substantial context around the term
                        context_start = max(0, pos - 600)
                        context_end = min(len(chapter_2_text), pos + 800)
                        context = chapter_2_text[context_start:context_end]
                        
                        print(f'\nPassage {i} (position {pos}):')
                        print('=' * 100)
                        print(context)
                        print('=' * 100)
                        
                        # Look for author names in this passage
                        context_lower = context.lower()
                        potential_authors = ['jung', 'carl jung', 'nietzsche', 'schopenhauer', 'kant', 'darwin', 'hegel']
                        
                        mentioned_authors = []
                        for author in potential_authors:
                            if author in context_lower:
                                mentioned_authors.append(author)
                        
                        if mentioned_authors:
                            print(f'\n*** POTENTIAL INFLUENCES FOUND IN THIS PASSAGE: {[author.upper() for author in mentioned_authors]} ***')
                        
                        print(f'\n{"="*100}\n')
            
            else:
                print('No direct "endopsychic" references found. Searching for influence/mythology references...')
                
                # Look for other relevant terms that might indicate the influence
                influence_terms = [term for term in found_terms if term in ['influenced', 'influence', 'mythology', 'myth']]
                
                for term in influence_terms[:2]:  # Look at first 2 relevant terms
                    print(f'\n--- PASSAGES CONTAINING "{term.upper()}" ---')
                    
                    chapter_2_lower = chapter_2_text.lower()
                    positions = []
                    start = 0
                    while True:
                        pos = chapter_2_lower.find(term.lower(), start)
                        if pos == -1:
                            break
                        positions.append(pos)
                        start = pos + 1
                    
                    # Show first 3 occurrences
                    for i, pos in enumerate(positions[:3], 1):
                        context_start = max(0, pos - 400)
                        context_end = min(len(chapter_2_text), pos + 500)
                        context = chapter_2_text[context_start:context_end]
                        
                        print(f'\nPassage {i}:')
                        print('-' * 80)
                        print(context)
                        print('-' * 80)
        
        else:
            print('\n⚠ No key terms found in Chapter 2 content')
            print('This may indicate the chapter extraction did not capture the relevant content')
            print('\nFull Chapter 2 content preview (first 2000 characters):')
            print(chapter_2_text[:2000] + '...')
        
        # Save the extracted Chapter 2 content
        chapter_data = {
            'source_pdf': pdf_path,
            'chapter_title': 'Chapter 2: Dark Traces',
            'start_page': chapter_2_start_page,
            'end_page': chapter_2_end_page,
            'total_pages': len(chapter_2_pages),
            'content_length': len(chapter_2_text),
            'full_text': chapter_2_text,
            'search_terms_found': found_terms,
            'extraction_timestamp': '2025-01-21 12:00:00'
        }
        
        chapter_file = 'workspace/chapter_2_dark_traces_extracted.json'
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, indent=2, ensure_ascii=False)
        
        print(f'\n*** CHAPTER 2 EXTRACTION COMPLETE ***')
        print(f'✓ Extracted from pages {chapter_2_start_page} to {chapter_2_end_page}')
        print(f'✓ Content length: {len(chapter_2_text):,} characters')
        print(f'✓ Search terms found: {len(found_terms)}')
        print(f'✓ Chapter content saved to: {chapter_file}')
        
        if 'endopsychic' in ''.join(found_terms.keys()):
            print(f'\n🎯 SUCCESS: Found "endopsychic" references in Chapter 2!')
            print('The passages above should reveal the author who influenced Freud\'s belief in "endopsychic myths"')
        else:
            print(f'\n⚠ "Endopsychic" not found - may need to search broader or check extraction accuracy')
    
    else:
        print('\n❌ Could not locate Chapter 2 start page')
        print('Searching entire document for "endopsychic" references...')
        
        # Search the entire document as fallback
        full_text = '\n\n'.join([page.page_content for page in pages])
        
        endopsychic_count = full_text.lower().count('endopsychic')
        if endopsychic_count > 0:
            print(f'Found {endopsychic_count} "endopsychic" references in the full document')
            
            # Extract passages
            full_text_lower = full_text.lower()
            positions = []
            start = 0
            while True:
                pos = full_text_lower.find('endopsychic', start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + 1
            
            print(f'\n=== ALL "ENDOPSYCHIC" REFERENCES IN DOCUMENT ===')
            for i, pos in enumerate(positions, 1):
                context_start = max(0, pos - 500)
                context_end = min(len(full_text), pos + 600)
                context = full_text[context_start:context_end]
                
                print(f'\nReference {i} (position {pos}):')
                print('=' * 80)
                print(context)
                print('=' * 80)
        else:
            print('No "endopsychic" references found in the entire document')
            print('The term may be spelled differently or the concept may be described without using this exact word')

except Exception as e:
    print(f'❌ Error parsing PDF: {str(e)}')
    print('This may be due to PDF format issues or file corruption')

print('\n=== PDF PARSING COMPLETE ===')
print('Objective: Find the author who influenced Freud\'s belief in "endopsychic myths"')
print('Status: Chapter 2 content extracted and analyzed for target information')
```

### Development Step 8: Download Open Access ’A Dark Trace’ and Extract Chapter 2 to Identify Freud’s Influencer

**Description**: Access and download the full text of 'A Dark Trace: Sigmund Freud on the Sense of Guilt' by H. Westerink from Project MUSE using DOI 10.1353/book.24372. Since the book was confirmed to be open access, retrieve the complete text and save it to workspace/dark_trace_freud_book.pdf or appropriate format. Focus on locating and extracting Chapter 2 content to identify the author who influenced Freud's belief in 'endopsychic myths'. If the full book is not directly downloadable, extract Chapter 2 specifically or access the book's table of contents to determine the exact chapter title and content structure.

**Use Cases**:
- Automated academic literature review and chapter-specific author influence mapping for graduate thesis research
- Legal contract clause extraction and keyword-based compliance verification for law firm due diligence
- Historical archive digitization and thematic content extraction for museum exhibit curation
- Pharmaceutical clinical trial protocol parsing and adverse-event term indexing for regulatory submissions
- Corporate compliance audit document processing and policy reference tracking for financial services
- Intelligence report ingestion and threat-related keyword highlighting for defense analysis teams
- E-learning textbook chapter summarization and concept linkage generation for online course development
- Patent portfolio screening and inventor-influence network mapping for intellectual property management

```
from langchain_community.document_loaders import PyPDFLoader
import os
import json

print('=== CORRECTING CHAPTER 2 EXTRACTION - EXTRACTING ACTUAL PAGES 37-56 ===')
print('Objective: Fix extraction error and get the real Chapter 2 content to find the author who influenced Freud\'s "endopsychic myths"\n')

# First, let's inspect the saved extraction file to understand what went wrong
extraction_file = 'workspace/chapter_2_dark_traces_extracted.json'

if os.path.exists(extraction_file):
    print('=== INSPECTING PREVIOUS EXTRACTION FILE ===')
    with open(extraction_file, 'r', encoding='utf-8') as f:
        previous_data = json.load(f)
    
    print(f'Previous extraction keys: {list(previous_data.keys())}')
    print(f'Previous start_page: {previous_data.get("start_page", "Unknown")}')
    print(f'Previous end_page: {previous_data.get("end_page", "Unknown")}')
    print(f'Previous content length: {previous_data.get("content_length", 0):,} characters')
    
    # Show first part of previous content to confirm it was TOC
    prev_content = previous_data.get('full_text', '')
    print(f'\nFirst 300 chars of previous extraction: "{prev_content[:300]}..."')
    
    if 'Contents' in prev_content[:500]:
        print('\n*** CONFIRMED: Previous extraction got Table of Contents, not Chapter 2 ***')
    
else:
    print(f'Previous extraction file not found: {extraction_file}')

# Load the PDF again with correct page extraction
workspace_files = os.listdir('workspace')
pdf_files = [f for f in workspace_files if f.endswith('.pdf')]

if pdf_files:
    pdf_path = os.path.join('workspace', pdf_files[0])
    print(f'\nReloading PDF file: {pdf_path}')
    
    try:
        # Load the PDF using LangChain's PyPDFLoader
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()
        
        print(f'✓ PDF reloaded successfully')
        print(f'Total pages: {len(pages)}')
        
        # Extract the CORRECT Chapter 2 pages (37-56 based on TOC)
        chapter_2_start = 37
        chapter_2_end = 56  # From TOC analysis, Chapter 2 goes from page 37 to before Chapter 3 at page 57
        
        print(f'\n=== EXTRACTING CORRECT CHAPTER 2 PAGES ({chapter_2_start}-{chapter_2_end}) ===')
        
        # Convert to 0-based indexing for page access
        start_idx = chapter_2_start - 1  # Page 37 = index 36
        end_idx = chapter_2_end  # Page 56 = index 55, but end_idx is exclusive so we use 56
        
        print(f'Extracting pages {chapter_2_start} to {chapter_2_end} (indices {start_idx} to {end_idx-1})')
        
        if end_idx <= len(pages):
            chapter_2_pages = pages[start_idx:end_idx]
            chapter_2_text = '\n\n'.join([page.page_content for page in chapter_2_pages])
            
            print(f'\nChapter 2 correctly extracted:')
            print(f'  Pages: {chapter_2_start} to {chapter_2_end}')
            print(f'  Total pages: {len(chapter_2_pages)}')
            print(f'  Total text length: {len(chapter_2_text):,} characters')
            print(f'\nFirst 500 characters of ACTUAL Chapter 2:')
            print(f'"{chapter_2_text[:500]}..."')
            
            # Verify this looks like chapter content, not TOC
            if 'Dark traces' in chapter_2_text[:1000] and 'Contents' not in chapter_2_text[:1000]:
                print('\n✓ This appears to be actual Chapter 2 content (contains "Dark traces", no "Contents")')
            else:
                print('\n⚠ Content verification: May still have extraction issues')
            
            # Now search for "endopsychic myths" and related terms in the CORRECT content
            print('\n=== SEARCHING FOR "ENDOPSYCHIC MYTHS" IN CORRECT CHAPTER 2 CONTENT ===')
            
            search_terms = [
                'endopsychic myth',
                'endopsychic', 
                'myth',
                'mythology',
                'jung',
                'carl jung',
                'nietzsche',
                'schopenhauer', 
                'kant',
                'darwin',
                'hegel',
                'influenced',
                'influence'
            ]
            
            found_terms = {}
            for term in search_terms:
                count = chapter_2_text.lower().count(term.lower())
                if count > 0:
                    found_terms[term] = count
                    print(f'✓ Found "{term}": {count} occurrences')
            
            if found_terms:
                print(f'\n=== EXTRACTING KEY PASSAGES FOR ENDOPSYCHIC MYTHS ===')
                
                # Prioritize searching for "endopsychic" terms first
                endopsychic_terms = [term for term in found_terms if 'endopsychic' in term.lower()]
                
                if endopsychic_terms:
                    print(f'\n🎯 SUCCESS: Found "endopsychic" terms: {endopsychic_terms}')
                    
                    chapter_2_lower = chapter_2_text.lower()
                    
                    for term in endopsychic_terms:
                        positions = []
                        start = 0
                        while True:
                            pos = chapter_2_lower.find(term.lower(), start)
                            if pos == -1:
                                break
                            positions.append(pos)
                            start = pos + 1
                        
                        print(f'\n--- EXTRACTING ALL "{term.upper()}" PASSAGES ({len(positions)} found) ---')
                        
                        for i, pos in enumerate(positions, 1):
                            # Extract substantial context around the term
                            context_start = max(0, pos - 800)
                            context_end = min(len(chapter_2_text), pos + 1000)
                            context = chapter_2_text[context_start:context_end]
                            
                            print(f'\nPASSAGE {i} - Position {pos}:')
                            print('=' * 120)
                            print(context)
                            print('=' * 120)
                            
                            # Analyze this passage for author names
                            context_lower = context.lower()
                            potential_authors = [
                                'jung', 'carl jung', 'c.g. jung', 'c. g. jung',
                                'nietzsche', 'friedrich nietzsche', 
                                'schopenhauer', 'arthur schopenhauer',
                                'kant', 'immanuel kant',
                                'darwin', 'charles darwin',
                                'hegel', 'georg hegel'
                            ]
                            
                            mentioned_authors = []
                            for author in potential_authors:
                                if author in context_lower:
                                    mentioned_authors.append(author)
                            
                            if mentioned_authors:
                                print(f'\n*** AUTHOR INFLUENCES IDENTIFIED IN THIS PASSAGE ***')
                                print(f'Authors mentioned: {[author.title() for author in mentioned_authors]}')
                                
                                # Look for specific influence language
                                influence_phrases = [
                                    'influenced by', 'influence of', 'influenced freud',
                                    'borrowed from', 'adopted from', 'derived from',
                                    'took from', 'learned from', 'inspired by'
                                ]
                                
                                influence_indicators = []
                                for phrase in influence_phrases:
                                    if phrase in context_lower:
                                        influence_indicators.append(phrase)
                                
                                if influence_indicators:
                                    print(f'Influence language found: {influence_indicators}')
                                    print('\n🔍 THIS PASSAGE LIKELY CONTAINS THE ANSWER! 🔍')
                            
                            print(f'\n{"-"*120}\n')
                
                else:
                    print('\n⚠ No direct "endopsychic" references found in correct Chapter 2 content')
                    print('Searching for "myth" and "influence" terms that might describe the concept differently...')
                    
                    # Look for other relevant terms
                    relevant_terms = []
                    for term in ['myth', 'mythology', 'influenced', 'influence']:
                        if term in found_terms:
                            relevant_terms.append(term)
                    
                    for term in relevant_terms[:2]:  # Focus on most promising terms
                        print(f'\n--- PASSAGES CONTAINING "{term.upper()}" ---')
                        
                        chapter_2_lower = chapter_2_text.lower()
                        positions = []
                        start = 0
                        while True:
                            pos = chapter_2_lower.find(term.lower(), start)
                            if pos == -1:
                                break
                            positions.append(pos)
                            start = pos + 1
                        
                        # Show first few occurrences with substantial context
                        for i, pos in enumerate(positions[:3], 1):
                            context_start = max(0, pos - 600)
                            context_end = min(len(chapter_2_text), pos + 700)
                            context = chapter_2_text[context_start:context_end]
                            
                            print(f'\nPassage {i}:')
                            print('=' * 90)
                            print(context)
                            print('=' * 90)
                            
                            # Check for author names in this context
                            context_lower = context.lower()
                            mentioned_authors = []
                            for author in ['jung', 'nietzsche', 'schopenhauer', 'kant', 'darwin']:
                                if author in context_lower:
                                    mentioned_authors.append(author)
                            
                            if mentioned_authors:
                                print(f'\nAuthors mentioned: {[a.title() for a in mentioned_authors]}')
                            
                            print(f'\n{"-"*90}\n')
            
            else:
                print('\n⚠ No search terms found in the corrected Chapter 2 content')
                print('This suggests either:')
                print('1. The term "endopsychic myths" may not appear in Chapter 2')
                print('2. The term is referenced differently than expected')
                print('3. There may still be page extraction issues')
                
                print('\nShowing sample of corrected Chapter 2 content for manual inspection:')
                print('\n' + '='*100)
                print(chapter_2_text[:2000] + '...')
                print('='*100)
            
            # Save the CORRECTED Chapter 2 content
            corrected_chapter_data = {
                'source_pdf': pdf_path,
                'chapter_title': 'Chapter 2: Dark Traces',
                'start_page': chapter_2_start,
                'end_page': chapter_2_end,
                'total_pages': len(chapter_2_pages),
                'content_length': len(chapter_2_text),
                'full_text': chapter_2_text,
                'search_terms_found': found_terms,
                'extraction_method': 'Corrected - extracted actual pages 37-56',
                'extraction_timestamp': '2025-01-21 12:30:00'
            }
            
            corrected_file = 'workspace/chapter_2_dark_traces_CORRECTED.json'
            with open(corrected_file, 'w', encoding='utf-8') as f:
                json.dump(corrected_chapter_data, f, indent=2, ensure_ascii=False)
            
            print(f'\n*** CORRECTED CHAPTER 2 EXTRACTION COMPLETE ***')
            print(f'✓ Correctly extracted from pages {chapter_2_start} to {chapter_2_end}')
            print(f'✓ Content length: {len(chapter_2_text):,} characters')
            print(f'✓ Search terms found: {len(found_terms)}')
            print(f'✓ Corrected chapter content saved to: {corrected_file}')
            
            if any('endopsychic' in term.lower() for term in found_terms.keys()):
                print(f'\n🎯 SUCCESS: Found "endopsychic" references in the CORRECT Chapter 2!')
                print('The extracted passages above should reveal the author who influenced Freud\'s "endopsychic myths"')
            elif any(term in found_terms for term in ['myth', 'influence', 'influenced']):
                print(f'\n✓ Found relevant terms that may lead to the answer')
                print('Review the extracted passages for context about mythological influences')
            else:
                print(f'\n⚠ Target terms still not found - may need broader search or different approach')
        
        else:
            print(f'❌ Chapter 2 end page ({chapter_2_end}) exceeds PDF length ({len(pages)} pages)')
    
    except Exception as e:
        print(f'❌ Error during corrected extraction: {str(e)}')

else:
    print('❌ No PDF files found in workspace')

print('\n=== CORRECTED EXTRACTION COMPLETE ===')
print('Objective: Find the author who influenced Freud\'s belief in "endopsychic myths"')
print('Status: Extracted actual Chapter 2 content (pages 37-56) and analyzed for target information')
```

### Development Step 4: Download ‘A Dark Trace’ Open Access PDF, Extract Chapter 2 to Identify Endopsychic Myths Author

**Description**: Access and download the full text of 'A Dark Trace: Sigmund Freud on the Sense of Guilt' by H. Westerink from Project MUSE using DOI 10.1353/book.24372. Since the book was confirmed to be open access, retrieve the complete text and save it to workspace/dark_trace_freud_book.pdf or appropriate format. Focus on locating and extracting Chapter 2 content to identify the author who influenced Freud's belief in 'endopsychic myths'. If the full book is not directly downloadable, extract Chapter 2 specifically or access the book's table of contents to determine the exact chapter title and content structure.

**Use Cases**:
- Academic psychoanalytic researchers automating extraction of Chapter 2 from “A Dark Trace” to systematically review Freud’s conceptualization of endopsychic myths across primary sources
- Digital humanities scholars building a searchable corpus of philosophical influences on Freudian guilt by scraping open-access chapters via DOI-based access scripts
- University librarians ingesting open-access book PDFs and parsing Chapter 2 metadata to streamline cataloging and improve digital library discoverability
- NLP engineers curating a domain-specific text dataset by extracting passages on Freud’s influences from Chapter 2 for machine-learning models analyzing psychoanalytic discourse
- Graduate students generating annotated excerpts of Jungian and Nietzschean references in Chapter 2 to support literature reviews in their theses on psychoanalytic genealogy
- E-learning content developers embedding targeted psychoanalytic chapter content into online course modules by automating retrieval of specific chapters from Project MUSE
- Open-access compliance officers validating and archiving Chapter 2 downloads to ensure licensing adherence and long-term preservation in institutional repositories
- Legal historians retrieving and analyzing Chapter 2 discussions of guilt theories to trace historical legal concepts in interdisciplinary law research

```
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

print('=== INVESTIGATING PROJECT MUSE BOOK ACCESS FOR CHAPTER 2 ===')
print('Objective: Access Chapter 2 "Dark Traces" (pages 37-56) to find author who influenced Freud\'s "endopsychic myths"\n')

# First, inspect the saved Project MUSE book page analysis
book_analysis_file = 'workspace/project_muse_book_page.json'

if os.path.exists(book_analysis_file):
    print('=== INSPECTING PROJECT MUSE BOOK PAGE ANALYSIS ===')
    with open(book_analysis_file, 'r', encoding='utf-8') as f:
        book_data = json.load(f)
    
    print(f'Book analysis keys: {list(book_data.keys())}')
    
    for key, value in book_data.items():
        if isinstance(value, (str, bool, int)):
            print(f'{key}: {value}')
        elif isinstance(value, list):
            print(f'{key}: List with {len(value)} items')
            if len(value) > 0:
                print(f'  Sample: {value[0]}')
        elif isinstance(value, dict):
            print(f'{key}: Dictionary with keys {list(value.keys())}')
    
    print(f'\nKey findings:')
    print(f'Book URL: {book_data.get("url", "Unknown")}')
    print(f'Title: {book_data.get("title", "Unknown")}')
    print(f'Book title: {book_data.get("book_title", "Unknown")}')
    print(f'Chapter 2 found: {book_data.get("chapter_2_found", False)}')
    print(f'Open access: {book_data.get("is_open_access", False)}')
    print(f'Access links: {len(book_data.get("access_links", []))}')
    print(f'Preview links: {len(book_data.get("preview_links", []))}')
else:
    print(f'Book analysis file not found: {book_analysis_file}')

print('\n=== TRYING CHAPTER-SPECIFIC ACCESS METHODS ===')

# Since we know it's Chapter 2 on pages 37-56, try different URL patterns
base_url = 'https://muse.jhu.edu/book/24372'
book_id = '24372'

# Possible chapter access URLs
chapter_urls = [
    f'https://muse.jhu.edu/book/{book_id}/chapter/2',
    f'https://muse.jhu.edu/chapter/{book_id}/2',
    f'https://muse.jhu.edu/book/{book_id}/ch/2',
    f'https://muse.jhu.edu/book/{book_id}/read/chapter/2',
    f'https://muse.jhu.edu/book/{book_id}/view/chapter/2',
    f'{base_url}/chapter/2',
    f'{base_url}/ch/2',
    f'{base_url}/read/2',
    f'{base_url}/view/2'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': base_url
}

successful_chapter_urls = []

print('Trying chapter-specific URL patterns:')
for i, chapter_url in enumerate(chapter_urls, 1):
    print(f'\n{i}. Testing: {chapter_url}')
    try:
        response = requests.get(chapter_url, headers=headers, timeout=20)
        print(f'   Status: {response.status_code}')
        
        if response.status_code == 200:
            print(f'   *** SUCCESS - Chapter URL accessible ***')
            print(f'   Final URL: {response.url}')
            print(f'   Content length: {len(response.content):,} bytes')
            
            successful_chapter_urls.append({
                'original_url': chapter_url,
                'final_url': response.url,
                'content_length': len(response.content),
                'response': response
            })
        elif response.status_code == 302 or response.status_code == 301:
            print(f'   Redirect to: {response.headers.get("Location", "Unknown")}')
    except Exception as e:
        print(f'   Error: {str(e)}')

if successful_chapter_urls:
    print(f'\n=== ANALYZING SUCCESSFUL CHAPTER ACCESS ===')
    
    # Use the first successful URL
    chapter_access = successful_chapter_urls[0]
    chapter_response = chapter_access['response']
    
    print(f'Analyzing content from: {chapter_access["final_url"]}')
    
    soup = BeautifulSoup(chapter_response.content, 'html.parser')
    
    # Get page title
    page_title = soup.find('title')
    if page_title:
        print(f'Page title: {page_title.get_text().strip()}')
    
    # Look for chapter content
    chapter_content_selectors = [
        'div.chapter-content',
        'div.content',
        'div.main-content',
        'div.text-content',
        'article',
        'main',
        'div[id*="chapter"]',
        'div[class*="chapter"]'
    ]
    
    chapter_content = None
    for selector in chapter_content_selectors:
        content_elem = soup.select_one(selector)
        if content_elem:
            chapter_content = content_elem
            print(f'Chapter content found with selector: {selector}')
            break
    
    if not chapter_content:
        # Fall back to main content area
        chapter_content = soup.find('body')
        print('Using full body content as fallback')
    
    if chapter_content:
        # Extract text content
        chapter_text = chapter_content.get_text()
        
        print(f'\nChapter content length: {len(chapter_text):,} characters')
        print(f'First 500 characters: {chapter_text[:500]}...')
        
        # Search for key terms related to "endopsychic myths"
        search_terms = [
            'endopsychic myth',
            'endopsychic',
            'myth',
            'mythology',
            'carl jung',
            'jung',
            'nietzsche',
            'schopenhauer',
            'kant',
            'philosophy',
            'influence',
            'influenced'
        ]
        
        print(f'\n=== SEARCHING FOR ENDOPSYCHIC MYTHS REFERENCES ===')
        
        found_terms = {}
        for term in search_terms:
            count = chapter_text.lower().count(term.lower())
            if count > 0:
                found_terms[term] = count
                print(f'Found "{term}": {count} occurrences')
        
        if found_terms:
            print(f'\n=== EXTRACTING RELEVANT PASSAGES ===')
            
            # Focus on "endopsychic" if found
            if any('endopsychic' in term.lower() for term in found_terms.keys()):
                print('Extracting passages about "endopsychic":')  
                
                text_lower = chapter_text.lower()
                endopsychic_positions = []
                start = 0
                while True:
                    pos = text_lower.find('endopsychic', start)
                    if pos == -1:
                        break
                    endopsychic_positions.append(pos)
                    start = pos + 1
                
                for i, pos in enumerate(endopsychic_positions, 1):
                    context_start = max(0, pos - 300)
                    context_end = min(len(chapter_text), pos + 400)
                    context = chapter_text[context_start:context_end]
                    
                    print(f'\nEndopsychic passage {i}:')
                    print(f'Position: {pos}')
                    print(f'Context: ...{context}...')
                    print('-' * 80)
            
            # Also look for author names that might be the influence
            author_names = ['jung', 'nietzsche', 'schopenhauer', 'kant', 'hegel', 'darwin']
            for author in author_names:
                if author in found_terms:
                    print(f'\nExtracting passages mentioning "{author}":')
                    
                    text_lower = chapter_text.lower()
                    author_positions = []
                    start = 0
                    while True:
                        pos = text_lower.find(author, start)
                        if pos == -1:
                            break
                        author_positions.append(pos)
                        start = pos + 1
                    
                    # Show first few occurrences
                    for i, pos in enumerate(author_positions[:3], 1):
                        context_start = max(0, pos - 200)
                        context_end = min(len(chapter_text), pos + 300)
                        context = chapter_text[context_start:context_end]
                        
                        print(f'\n{author.title()} mention {i}:')
                        print(f'Context: ...{context}...')
                        print('-' * 60)
        
        # Save the chapter content for further analysis
        chapter_data = {
            'source_url': chapter_access['final_url'],
            'chapter_title': 'Chapter 2: Dark Traces',
            'content_length': len(chapter_text),
            'full_text': chapter_text,
            'search_terms_found': found_terms,
            'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        chapter_file = 'workspace/chapter_2_dark_traces_content.json'
        with open(chapter_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_data, f, indent=2, ensure_ascii=False)
        
        print(f'\n*** CHAPTER 2 CONTENT SUCCESSFULLY EXTRACTED ***')
        print(f'Saved to: {chapter_file}')
        print(f'Content length: {len(chapter_text):,} characters')
        print(f'Search terms found: {len(found_terms)} out of {len(search_terms)}')

else:
    print('\n=== NO DIRECT CHAPTER ACCESS FOUND ===')
    print('Trying alternative access methods...')
    
    # Try accessing the main book page again and look for reading interfaces
    print('\n=== RE-EXAMINING MAIN BOOK PAGE FOR READING OPTIONS ===')
    
    try:
        main_response = requests.get(base_url, headers=headers, timeout=30)
        if main_response.status_code == 200:
            main_soup = BeautifulSoup(main_response.content, 'html.parser')
            
            # Look for "Read Online", "View", or similar buttons
            read_selectors = [
                'a:contains("Read")',
                'a:contains("View")',
                'a:contains("Online")',
                'button:contains("Read")',
                '.read-button',
                '.view-button',
                '.online-access',
                '[data-action="read"]'
            ]
            
            read_links = []
            for selector in read_selectors:
                try:
                    elements = main_soup.select(selector)
                    for elem in elements:
                        href = elem.get('href') or elem.get('data-href')
                        if href:
                            if href.startswith('/'):
                                href = urljoin(base_url, href)
                            read_links.append({
                                'url': href,
                                'text': elem.get_text().strip(),
                                'selector': selector
                            })
                except:
                    pass
            
            print(f'Found {len(read_links)} potential reading links:')
            for i, link in enumerate(read_links, 1):
                print(f'{i}. {link["text"]} -> {link["url"]}')
            
            if read_links:
                print('\nTrying first reading link...')
                try:
                    read_response = requests.get(read_links[0]['url'], headers=headers, timeout=30)
                    print(f'Reading interface status: {read_response.status_code}')
                    print(f'Final URL: {read_response.url}')
                except Exception as read_error:
                    print(f'Error accessing reading interface: {str(read_error)}')
    
    except Exception as main_error:
        print(f'Error re-examining main page: {str(main_error)}')

print('\n=== CHAPTER 2 ACCESS ATTEMPT COMPLETE ===')
print('Summary:')
print('- Tested multiple chapter-specific URL patterns')
print('- Attempted to extract Chapter 2 "Dark Traces" content')
print('- Searched for "endopsychic myths" references and author influences')
print('- Saved any accessible content for analysis')
print('\nObjective: Identify the author who influenced Freud\'s belief in "endopsychic myths"')
print('Status: Analysis of extracted content should reveal the answer')
```

## Created Time
2025-08-11 02:16:23
