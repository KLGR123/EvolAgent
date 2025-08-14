# Developer Plan 02

## Plan
Contact the University of Geneva library system or Federico Lauria directly to request access to the complete institutional version of his 2014 dissertation 'The Logic of the Liver: A Deontic View of the Intentionality of Desire' that contains footnote 397. Since the publicly available PDF version definitively lacks this footnote, we need the full institutional repository version or author's original document. Once obtained, extract the work referenced in footnote 397, then search the Smithsonian American Art Museum's collection (as of August 2023) for paintings whose titles derive from the same source work, identify the specific chapters quoted in the painting titles, and calculate the absolute difference between their chapter numbers.

## Description
This approach is necessary because: (1) The developer's comprehensive analysis confirmed that footnote 397 does not exist in the publicly available 422-page PDF version of Lauria's dissertation, (2) Multiple search strategies across 11 different academic databases and repositories have been exhausted, (3) The task requires institutional access to the complete dissertation version that may contain additional footnotes not present in the public PDF, (4) This represents the only viable path forward to identify the source work that connects to the Smithsonian painting titles and complete the chapter number calculation as requested in the original TASK.

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

### Development Step 2: Download ‘A Dark Trace’ Open Access Book, Extract Chapter 2 to Find ‘Endopsychic Myths’ Influencer

**Description**: Access and download the full text of 'A Dark Trace: Sigmund Freud on the Sense of Guilt' by H. Westerink from Project MUSE using DOI 10.1353/book.24372. Since the book was confirmed to be open access, retrieve the complete text and save it to workspace/dark_trace_freud_book.pdf or appropriate format. Focus on locating and extracting Chapter 2 content to identify the author who influenced Freud's belief in 'endopsychic myths'. If the full book is not directly downloadable, extract Chapter 2 specifically or access the book's table of contents to determine the exact chapter title and content structure.

**Use Cases**:
- Digital humanities research project mapping Freud’s intellectual lineage by automatically retrieving “A Dark Trace: Sigmund Freud on the Sense of Guilt” via DOI and extracting Chapter 2 to identify Wilhelm Fliess’s influence on endopsychic myths.
- University library metadata automation system that scrapes Project MUSE via DOI to validate open access status, download the full-text PDF, extract the table of contents, and index Chapter 2 under psychoanalysis subject headings.
- Graduate student workflow for thesis preparation that uses a Python script to download the complete book from Project MUSE and isolate Chapter 2 content for direct quoting, annotation, and citation management in a dissertation on Freud’s sense of guilt.
- AI training data pipeline for natural language processing that harvests Chapter 2 passages from open access psychoanalytic texts to build a specialized corpus for modeling references to early psychological myth constructs.
- Institutional repository ingestion process where archivists automate DOI-based harvesting of open access monographs, save full PDFs, parse chapter structures, and tag Chapter 2 content for long-term preservation and public access.
- Publisher open access compliance checker that programmatically follows DOIs on Project MUSE, confirms Creative Commons licensing, validates PDF download links, and flags any access or licensing anomalies for titles like “A Dark Trace: Sigmund Freud on the Sense of Guilt.”
- Research information system generating a knowledge graph of psychoanalysis by retrieving monograph text, parsing the table of contents, extracting author references in Chapter 2, and creating entities and relationships representing Freud’s intellectual influences.
- E-learning content automation where an educational platform downloads open access chapters from Project MUSE, extracts illustrative examples from Chapter 2, and generates interactive quiz questions about scholars who shaped Freud’s theory of guilt.

```
import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import time

print('=== ACCESSING PROJECT MUSE BOOK VIA DOI ===')
print('Title: A Dark Trace: Sigmund Freud on the Sense of Guilt')
print('Author: H. Westerink')
print('DOI: 10.1353/book.24372')
print('Source: Project MUSE\n')

# Construct the DOI URL
doi_url = 'https://doi.org/10.1353/book.24372'
print(f'DOI URL: {doi_url}')

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

print('\n=== FOLLOWING DOI REDIRECT ===')

try:
    # Follow the DOI redirect to get the actual Project MUSE URL
    print('Making initial request to DOI...')
    doi_response = requests.get(doi_url, headers=headers, timeout=30, allow_redirects=True)
    print(f'Final URL after redirects: {doi_response.url}')
    print(f'Status code: {doi_response.status_code}')
    print(f'Content length: {len(doi_response.content):,} bytes')
    print(f'Content type: {doi_response.headers.get("Content-Type", "unknown")}')
    
    if doi_response.status_code == 200:
        # Parse the page to understand its structure
        soup = BeautifulSoup(doi_response.content, 'html.parser')
        
        # Get page title
        page_title = soup.find('title')
        if page_title:
            print(f'\nPage title: {page_title.get_text().strip()}')
        
        # Look for the book title on the page
        book_title_selectors = [
            'h1.title',
            'h1',
            '.book-title',
            '[data-title]',
            '.citation_title'
        ]
        
        book_title_found = None
        for selector in book_title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title_text = title_elem.get_text().strip()
                if 'dark trace' in title_text.lower() or 'freud' in title_text.lower():
                    book_title_found = title_text
                    print(f'Book title found: {title_text}')
                    break
        
        if not book_title_found:
            print('Book title not immediately found, checking page content...')
        
        # Look for download links (PDF, full text access)
        download_links = []
        
        # Common selectors for download links on academic sites
        download_selectors = [
            'a[href*=".pdf"]',
            'a[href*="download"]',
            'a[href*="fulltext"]',
            '.pdf-link',
            '.download-link',
            '.full-text-link',
            '[data-download]',
            'a:contains("PDF")',
            'a:contains("Download")',
            'a:contains("Full Text")'
        ]
        
        for selector in download_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                link_text = link.get_text().strip()
                if href:
                    # Convert relative URLs to absolute
                    if href.startswith('/'):
                        href = urljoin(doi_response.url, href)
                    download_links.append({
                        'url': href,
                        'text': link_text,
                        'selector': selector
                    })
        
        # Remove duplicates
        unique_downloads = []
        seen_urls = set()
        for link in download_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_downloads.append(link)
        
        print(f'\n=== DOWNLOAD LINKS ANALYSIS ===')
        print(f'Found {len(unique_downloads)} potential download links:')
        
        for i, link in enumerate(unique_downloads, 1):
            print(f'{i}. {link["text"]} -> {link["url"]}')
            print(f'   Selector: {link["selector"]}')
        
        # Look for table of contents or chapter information
        print(f'\n=== SEARCHING FOR TABLE OF CONTENTS ===')
        
        toc_selectors = [
            '.table-of-contents',
            '.toc',
            '.chapter-list',
            '.contents',
            '[id*="toc"]',
            '[class*="chapter"]'
        ]
        
        toc_found = False
        for selector in toc_selectors:
            toc_elem = soup.select_one(selector)
            if toc_elem:
                print(f'Table of contents found with selector: {selector}')
                toc_text = toc_elem.get_text().strip()
                print(f'TOC preview: {toc_text[:500]}...' if len(toc_text) > 500 else f'TOC: {toc_text}')
                toc_found = True
                break
        
        if not toc_found:
            # Search for chapter references in the text
            page_text = soup.get_text().lower()
            chapter_indicators = ['chapter 2', 'chapter two', 'ch. 2', 'ch 2']
            
            for indicator in chapter_indicators:
                if indicator in page_text:
                    print(f'Found reference to Chapter 2: "{indicator}"')
                    # Extract context around the chapter reference
                    index = page_text.find(indicator)
                    context_start = max(0, index - 100)
                    context_end = min(len(page_text), index + 200)
                    context = page_text[context_start:context_end]
                    print(f'Context: ...{context}...')
                    break
        
        # Check if this is an open access work
        open_access_indicators = ['open access', 'free access', 'freely available', 'cc license']
        is_open_access = any(indicator in soup.get_text().lower() for indicator in open_access_indicators)
        print(f'\nOpen access indicators found: {is_open_access}')
        
        # Try the most promising download link if available
        if unique_downloads:
            # Prioritize PDF links
            pdf_links = [link for link in unique_downloads if '.pdf' in link['url'].lower()]
            
            if pdf_links:
                target_link = pdf_links[0]
                print(f'\n=== ATTEMPTING PDF DOWNLOAD ===')
                print(f'Target: {target_link["text"]}')
                print(f'URL: {target_link["url"]}')
                
                try:
                    print('Downloading PDF...')
                    pdf_response = requests.get(target_link['url'], headers=headers, timeout=60)
                    
                    if pdf_response.status_code == 200:
                        content_type = pdf_response.headers.get('content-type', '').lower()
                        print(f'Content-Type: {content_type}')
                        print(f'Content-Length: {len(pdf_response.content):,} bytes')
                        
                        if 'pdf' in content_type or len(pdf_response.content) > 50000:
                            # Save the PDF
                            pdf_path = 'workspace/dark_trace_freud_book.pdf'
                            os.makedirs('workspace', exist_ok=True)
                            
                            with open(pdf_path, 'wb') as pdf_file:
                                pdf_file.write(pdf_response.content)
                            
                            file_size = os.path.getsize(pdf_path)
                            print(f'\n*** PDF SUCCESSFULLY DOWNLOADED ***')
                            print(f'Saved to: {pdf_path}')
                            print(f'File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
                            
                        else:
                            print('Downloaded content does not appear to be a PDF')
                            print(f'Content preview: {pdf_response.text[:300]}...')
                    
                    else:
                        print(f'PDF download failed with status code: {pdf_response.status_code}')
                        print(f'Response: {pdf_response.text[:300]}...')
                
                except Exception as e:
                    print(f'Error downloading PDF: {str(e)}')
            
            else:
                # Try the first general download link
                target_link = unique_downloads[0]
                print(f'\n=== ATTEMPTING GENERAL DOWNLOAD ===')
                print(f'Target: {target_link["text"]}')
                print(f'URL: {target_link["url"]}')
                
                try:
                    download_response = requests.get(target_link['url'], headers=headers, timeout=60)
                    print(f'Download response status: {download_response.status_code}')
                    print(f'Content type: {download_response.headers.get("content-type", "unknown")}')
                    
                    if download_response.status_code == 200:
                        # Save the response for analysis
                        content_path = 'workspace/book_content_response.html'
                        with open(content_path, 'w', encoding='utf-8') as f:
                            f.write(download_response.text)
                        print(f'Content saved to: {content_path}')
                    
                except Exception as e:
                    print(f'Error with general download: {str(e)}')
        
        # Save page analysis results
        page_analysis = {
            'doi_url': doi_url,
            'final_url': doi_response.url,
            'page_title': page_title.get_text().strip() if page_title else None,
            'book_title_found': book_title_found,
            'download_links': unique_downloads,
            'is_open_access': is_open_access,
            'toc_found': toc_found,
            'content_length': len(doi_response.content),
            'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        analysis_file = 'workspace/project_muse_page_analysis.json'
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(page_analysis, f, indent=2, ensure_ascii=False)
        
        print(f'\n=== ANALYSIS COMPLETE ===')
        print(f'✓ Page analysis saved to: {analysis_file}')
        print(f'✓ Found {len(unique_downloads)} download links')
        print(f'✓ Open access status: {is_open_access}')
        print(f'✓ Book title identified: {book_title_found is not None}')
        
    else:
        print(f'Failed to access DOI page: {doi_response.status_code}')
        print(f'Response: {doi_response.text[:500]}...')

except Exception as e:
    print(f'Error accessing DOI: {str(e)}')
    
    # Try alternative approaches
    print('\n=== TRYING DIRECT PROJECT MUSE SEARCH ===')
    
    # Try searching Project MUSE directly
    muse_search_url = 'https://muse.jhu.edu/search?action=search&query=creator%3A%22Westerink%2C%20H%22%20AND%20title%3A%22Dark%20Trace%22'
    print(f'Direct search URL: {muse_search_url}')
    
    try:
        search_response = requests.get(muse_search_url, headers=headers, timeout=30)
        print(f'Search response status: {search_response.status_code}')
        
        if search_response.status_code == 200:
            search_soup = BeautifulSoup(search_response.content, 'html.parser')
            
            # Look for the book in search results
            result_links = search_soup.find_all('a', href=True)
            book_links = []
            
            for link in result_links:
                href = link.get('href')
                text = link.get_text().strip()
                if href and ('dark' in text.lower() or 'freud' in text.lower() or 'westerink' in text.lower()):
                    if href.startswith('/'):
                        href = urljoin('https://muse.jhu.edu', href)
                    book_links.append({
                        'url': href,
                        'text': text
                    })
            
            print(f'Found {len(book_links)} potential book links:')
            for i, link in enumerate(book_links, 1):
                print(f'{i}. {link["text"]} -> {link["url"]}')
            
            # Save search results
            search_results = {
                'search_url': muse_search_url,
                'status_code': search_response.status_code,
                'book_links_found': book_links,
                'search_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open('workspace/project_muse_search_results.json', 'w', encoding='utf-8') as f:
                json.dump(search_results, f, indent=2, ensure_ascii=False)
            
            print('Search results saved to: workspace/project_muse_search_results.json')
    
    except Exception as search_error:
        print(f'Search attempt also failed: {str(search_error)}')

print('\n=== INITIAL ACCESS ATTEMPT COMPLETE ===')
print('Next steps: Analyze results and attempt targeted content extraction')
```

## Created Time
2025-08-14 01:58:52
