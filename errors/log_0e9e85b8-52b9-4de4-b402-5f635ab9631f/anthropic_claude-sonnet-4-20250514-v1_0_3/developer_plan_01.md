# Developer Plan 01

## Plan
Access Carl Nebel's Wikipedia page and retrieve the latest version as it appeared in August 2023. Locate the first citation reference link in the article, follow that link to the referenced webpage, and examine any images on that webpage to identify chronological year dates written within the images. Extract the latest (most recent) year date found in the image content.

## Description
This is the optimal starting approach because: (1) We need to first locate Carl Nebel's Wikipedia page and access its August 2023 version to ensure we're working with the correct timeframe, (2) No previous research has been conducted on this specific task, (3) Expected outcome is to identify the first citation reference link and access the target webpage containing images with chronological dates, (4) This establishes the foundation for systematically following the citation chain and analyzing image content to find the latest year date as requested in the TASK.

## Episodic Examples
### Development Step 7: **Title:**  
Extract Wikipedia Access Date from Endnote on Page 11 of 'The Responsibility of Intellectuals' (2019)

**Description**: Access and download the full text of 'The Responsibility of Intellectuals' (DOI 10.2307/j.ctv9b2xdv) from JSTOR or UCL Press. Since this is a 2019 UCL Press publication available through JSTOR, retrieve the complete book content and save it to the workspace. Focus on locating page 11, identifying the second-to-last paragraph on that page, and extracting the specific endnote referenced in that paragraph. The endnote should contain a Wikipedia article citation with a November access date - extract the exact day of the month when the Wikipedia article was accessed.

**Use Cases**:
- Academic integrity auditing by university librarians to verify citation accuracy and access dates in open-access scholarly books
- Automated literature review tools for researchers needing to extract and cross-reference Wikipedia citations and their access dates across large PDF collections
- Digital humanities projects analyzing citation patterns and sources in contemporary intellectual history publications
- Legal compliance checks for publishers ensuring all Wikipedia references in academic works include proper access dates as per citation standards
- Bibliometric analysis for research impact studies, tracking the prevalence and recency of Wikipedia citations in academic monographs
- Content verification workflows for fact-checkers reviewing the reliability and timeliness of Wikipedia-sourced references in published books
- Automated metadata enrichment for digital repositories, extracting and structuring citation details (including access dates) from full-text PDFs
- Quality assurance processes in academic publishing, detecting missing or outdated access dates in Wikipedia citations before final release

```
import os
import json
import requests
from bs4 import BeautifulSoup
import time
import re

print('=== COMPREHENSIVE SEARCH FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES ===')
print('DOI: 10.2307/j.ctv9b2xdv')
print('Objective: Search entire book for Wikipedia citations with November access dates')
print('Status: Page 11 second-to-last paragraph had no endnote references')
print('\n' + '='*100 + '\n')

# First, let's check if we have the full book PDF downloaded
pdf_path = None
workspace_files = os.listdir('workspace')
for file in workspace_files:
    if file.endswith('.pdf') and 'responsibility' in file.lower():
        pdf_path = os.path.join('workspace', file)
        break

if not pdf_path:
    print('❌ Full book PDF not found in workspace')
    print('Available files:')
    for file in workspace_files:
        print(f'  - {file}')
    exit()

print(f'Found PDF: {pdf_path}')
file_size = os.path.getsize(pdf_path)
print(f'PDF size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')

print('\n=== EXTRACTING FULL BOOK TEXT FOR COMPREHENSIVE SEARCH ===')

try:
    from langchain_community.document_loaders import PyPDFLoader
    
    print('Loading complete PDF...')
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    
    print(f'✓ PDF loaded with {len(pages)} pages')
    
    # Combine all pages into full text
    full_book_text = '\n\n'.join([page.page_content for page in pages])
    print(f'Total book text: {len(full_book_text):,} characters')
    
    # Save full text for reference
    with open('workspace/full_book_text.txt', 'w', encoding='utf-8') as f:
        f.write('THE RESPONSIBILITY OF INTELLECTUALS - FULL BOOK TEXT\n')
        f.write('Source: UCL Press Open Access PDF\n')
        f.write('='*80 + '\n\n')
        f.write(full_book_text)
    
    print('✓ Full book text saved to workspace/full_book_text.txt')
    
    print('\n=== SEARCHING FOR ALL WIKIPEDIA REFERENCES ===')
    
    # First, let's find all Wikipedia references regardless of date
    wikipedia_general_patterns = [
        r'wikipedia[^\n]{0,300}',
        r'en\.wikipedia\.org[^\n]{0,300}',
        r'\bwikipedia\b[^\n]{0,300}'
    ]
    
    all_wikipedia_refs = []
    for pattern in wikipedia_general_patterns:
        matches = re.finditer(pattern, full_book_text, re.IGNORECASE)
        for match in matches:
            ref_text = match.group(0)
            all_wikipedia_refs.append({
                'text': ref_text,
                'position': match.start(),
                'pattern_used': pattern
            })
    
    # Remove duplicates based on position
    unique_wiki_refs = []
    seen_positions = set()
    for ref in all_wikipedia_refs:
        if ref['position'] not in seen_positions:
            seen_positions.add(ref['position'])
            unique_wiki_refs.append(ref)
    
    print(f'Found {len(unique_wiki_refs)} total Wikipedia references in the book')
    
    if unique_wiki_refs:
        print('\nFirst 10 Wikipedia references:')
        for i, ref in enumerate(unique_wiki_refs[:10], 1):
            print(f'{i}. Position {ref["position"]:,}: {ref["text"][:100]}...')
    
    print('\n=== SEARCHING FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES ===')
    
    # Comprehensive patterns for Wikipedia citations with November dates
    november_wikipedia_patterns = [
        # Wikipedia followed by November and day
        r'wikipedia[^\n]{0,400}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        r'en\.wikipedia\.org[^\n]{0,400}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        
        # November and day followed by Wikipedia
        r'november[^\n]{0,100}\d{1,2}[^\n]{0,200}wikipedia[^\n]{0,300}',
        r'\d{1,2}[^\n]{0,50}november[^\n]{0,200}wikipedia[^\n]{0,300}',
        
        # Accessed patterns
        r'accessed[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,200}wikipedia[^\n]{0,200}',
        r'wikipedia[^\n]{0,400}accessed[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        
        # More flexible patterns
        r'\bwikipedia\b[^\n]{0,500}\bnovember\b[^\n]{0,150}\b\d{1,2}\b[^\n]{0,150}',
        r'\bnovember\b[^\n]{0,150}\b\d{1,2}\b[^\n]{0,300}\bwikipedia\b[^\n]{0,300}',
        
        # URL patterns with dates
        r'https?://[^\s]*wikipedia[^\s]*[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,100}',
        r'november[^\n]{0,100}\d{1,2}[^\n]{0,200}https?://[^\s]*wikipedia[^\s]*[^\n]{0,100}'
    ]
    
    november_citations = []
    for pattern in november_wikipedia_patterns:
        matches = re.finditer(pattern, full_book_text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            citation_text = match.group(0)
            
            # Extract the day from November date using multiple patterns
            day_patterns = [
                r'november\s+(\d{1,2})',
                r'(\d{1,2})\s+november',
                r'november\s+(\d{1,2})(?:st|nd|rd|th)?',
                r'(\d{1,2})(?:st|nd|rd|th)?\s+november',
                r'november\s*,?\s*(\d{1,2})',
                r'(\d{1,2})\s*,?\s*november',
                r'november\s+(\d{1,2})\s*,?\s*\d{4}',
                r'(\d{1,2})\s+november\s+\d{4}'
            ]
            
            day_found = None
            for day_pattern in day_patterns:
                day_match = re.search(day_pattern, citation_text, re.IGNORECASE)
                if day_match:
                    day_found = day_match.group(1)
                    break
            
            if day_found and 1 <= int(day_found) <= 31:  # Valid day
                # Get broader context around the citation
                context_start = max(0, match.start() - 1000)
                context_end = min(len(full_book_text), match.end() + 1000)
                citation_context = full_book_text[context_start:context_end]
                
                # Determine which page this citation appears on
                char_count = 0
                page_number = 0
                for page_idx, page in enumerate(pages):
                    if char_count + len(page.page_content) >= match.start():
                        page_number = page_idx + 1
                        break
                    char_count += len(page.page_content) + 2  # +2 for \n\n separator
                
                november_citations.append({
                    'citation': citation_text,
                    'november_day': day_found,
                    'position': match.start(),
                    'context': citation_context,
                    'page_number': page_number,
                    'pattern_used': pattern
                })
    
    # Remove duplicates based on citation text and day
    unique_november_citations = []
    seen_citations = set()
    for citation in november_citations:
        citation_key = (citation['citation'].strip().lower(), citation['november_day'])
        if citation_key not in seen_citations:
            seen_citations.add(citation_key)
            unique_november_citations.append(citation)
    
    if unique_november_citations:
        print(f'\n🎯 FOUND {len(unique_november_citations)} UNIQUE WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES:')
        
        for i, citation in enumerate(unique_november_citations, 1):
            print(f'\nCitation {i}:')
            print(f'November day: {citation["november_day"]}')
            print(f'Page number: {citation["page_number"]}')
            print(f'Position in book: {citation["position"]:,}')
            print(f'Pattern used: {citation["pattern_used"]}')
            print('Citation text:')
            print('='*80)
            print(citation['citation'])
            print('='*80)
            
            # Show relevant context
            context_preview = citation['context'][:500] + '...' if len(citation['context']) > 500 else citation['context']
            print(f'Context: {context_preview}')
            print('-'*80)
        
        # Save the complete analysis
        final_analysis = {
            'source_pdf': pdf_path,
            'book_title': 'The Responsibility of Intellectuals',
            'publisher': 'UCL Press',
            'year': 2019,
            'total_pages': len(pages),
            'total_wikipedia_references': len(unique_wiki_refs),
            'wikipedia_citations_with_november_dates': unique_november_citations,
            'search_patterns_used': november_wikipedia_patterns,
            'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open('workspace/comprehensive_wikipedia_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(final_analysis, f, indent=2, ensure_ascii=False)
        
        print('\n✓ Complete analysis saved to workspace/comprehensive_wikipedia_analysis.json')
        
        # Determine the final answer
        if len(unique_november_citations) == 1:
            answer_day = unique_november_citations[0]['november_day']
            page_num = unique_november_citations[0]['page_number']
            print(f'\n*** FINAL ANSWER: The Wikipedia article was accessed on November {answer_day} ***')
            print(f'(Found on page {page_num} of the book)')
        elif len(unique_november_citations) > 1:
            print(f'\n*** MULTIPLE WIKIPEDIA CITATIONS WITH NOVEMBER DATES FOUND ***')
            print('All November access dates found:')
            for i, citation in enumerate(unique_november_citations, 1):
                print(f'{i}. November {citation["november_day"]} (page {citation["page_number"]})')
            
            # Look for the one closest to page 11 or in endnotes section
            closest_to_page_11 = None
            min_distance = float('inf')
            
            for citation in unique_november_citations:
                distance = abs(citation['page_number'] - 11)
                if distance < min_distance:
                    min_distance = distance
                    closest_to_page_11 = citation
            
            if closest_to_page_11:
                answer_day = closest_to_page_11['november_day']
                page_num = closest_to_page_11['page_number']
                print(f'\n*** MOST LIKELY ANSWER (closest to page 11): November {answer_day} ***')
                print(f'(Found on page {page_num}, distance from page 11: {min_distance} pages)')
            else:
                # Default to first citation
                answer_day = unique_november_citations[0]['november_day']
                print(f'\nDefaulting to first citation: November {answer_day}')
    
    else:
        print('\n⚠ No Wikipedia citations with November access dates found')
        
        # Let's search for any date patterns with Wikipedia
        print('\nSearching for Wikipedia citations with any date patterns...')
        
        date_patterns = [
            r'wikipedia[^\n]{0,300}\d{1,2}[^\n]{0,100}\d{4}[^\n]{0,100}',  # Any date
            r'wikipedia[^\n]{0,300}accessed[^\n]{0,200}\d{4}[^\n]{0,100}',  # Accessed with year
            r'accessed[^\n]{0,200}wikipedia[^\n]{0,300}\d{4}[^\n]{0,100}',  # Accessed before wikipedia
        ]
        
        any_date_citations = []
        for pattern in date_patterns:
            matches = re.finditer(pattern, full_book_text, re.IGNORECASE)
            for match in matches:
                citation_text = match.group(0)
                any_date_citations.append(citation_text)
        
        if any_date_citations:
            print(f'Found {len(any_date_citations)} Wikipedia citations with any date patterns:')
            for i, citation in enumerate(any_date_citations[:5], 1):
                print(f'{i}. {citation[:150]}...')
        else:
            print('No Wikipedia citations with any date patterns found')
        
        # Final fallback: search for month names with Wikipedia
        print('\nSearching for Wikipedia citations with any month names...')
        
        month_patterns = [
            r'wikipedia[^\n]{0,300}(?:january|february|march|april|may|june|july|august|september|october|november|december)[^\n]{0,100}\d{1,2}[^\n]{0,100}',
            r'(?:january|february|march|april|may|june|july|august|september|october|november|december)[^\n]{0,100}\d{1,2}[^\n]{0,200}wikipedia[^\n]{0,300}'
        ]
        
        month_citations = []
        for pattern in month_patterns:
            matches = re.finditer(pattern, full_book_text, re.IGNORECASE)
            for match in matches:
                citation_text = match.group(0)
                month_citations.append(citation_text)
        
        if month_citations:
            print(f'Found {len(month_citations)} Wikipedia citations with month names:')
            for i, citation in enumerate(month_citations[:5], 1):
                print(f'{i}. {citation[:150]}...')
        else:
            print('No Wikipedia citations with month names found')

except ImportError:
    print('❌ PyPDFLoader not available - cannot extract text from PDF')
except Exception as e:
    print(f'❌ Error during comprehensive search: {str(e)}')

print('\n' + '='*100)
print('COMPREHENSIVE WIKIPEDIA SEARCH COMPLETE')
print('='*100)
print('Objective: Find Wikipedia citation with November access date from entire book')
print('Status: Searched all pages since page 11 paragraph had no endnote references')
print('\nFiles created:')
if os.path.exists('workspace'):
    for file in sorted(os.listdir('workspace')):
        if file.endswith(('.txt', '.json')):
            file_path = os.path.join('workspace', file)
            file_size = os.path.getsize(file_path)
            print(f'- {file} ({file_size:,} bytes)')
```

### Development Step 4: **Title:**  
Extract Wikipedia Access Date from Endnote on Page 11 of 'The Responsibility of Intellectuals' (2019)

**Description**: Access and download the full text of 'The Responsibility of Intellectuals' (DOI 10.2307/j.ctv9b2xdv) from JSTOR or UCL Press. Since this is a 2019 UCL Press publication available through JSTOR, retrieve the complete book content and save it to the workspace. Focus on locating page 11, identifying the second-to-last paragraph on that page, and extracting the specific endnote referenced in that paragraph. The endnote should contain a Wikipedia article citation with a November access date - extract the exact day of the month when the Wikipedia article was accessed.

**Use Cases**:
- Academic integrity auditing by university librarians to verify the accuracy and recency of Wikipedia citations in scholarly books and ensure proper referencing standards are met
- Automated extraction of citation metadata for digital humanities researchers analyzing how Wikipedia is referenced in modern academic monographs
- Legal compliance checks by publishers to confirm that open-access book content and endnotes are correctly attributed and accessible, especially for digital distribution
- Research reproducibility validation for peer reviewers who need to trace and confirm the exact sources and access dates of online references cited in academic texts
- Large-scale content ingestion and knowledge graph enrichment for AI systems that require granular bibliographic data, including access dates of web-based sources
- Workflow automation for academic editors who need to extract, review, and cross-check endnote details (such as Wikipedia access dates) across multiple chapters of a book
- Historical citation trend analysis by information scientists studying the evolution of Wikipedia usage in scholarly literature over time
- Quality assurance for digital archives ensuring that digitized books from platforms like JSTOR/UCL Press have complete, accurate, and machine-readable endnote information for future reference

```
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

print('=== ALTERNATIVE ACCESS APPROACH: TRYING SPECIFIC CHAPTER PDF LINKS ===')
print('DOI: 10.2307/j.ctv9b2xdv')
print('Objective: Access individual chapter PDFs to locate page 11 and Wikipedia endnote')
print('\n' + '='*100 + '\n')

# First, inspect the final bibliographic record to get chapter URLs
final_record_path = 'workspace/final_bibliographic_record.json'
if os.path.exists(final_record_path):
    print('=== INSPECTING BIBLIOGRAPHIC RECORD FOR CHAPTER URLS ===')
    with open(final_record_path, 'r', encoding='utf-8') as f:
        biblio_data = json.load(f)
    
    print('Checking chapters_sections structure...')
    if 'chapters_sections' in biblio_data:
        chapters = biblio_data['chapters_sections']
        print(f'Found {len(chapters)} chapters/sections')
        
        # Extract PDF links specifically
        pdf_links = []
        for i, chapter in enumerate(chapters, 1):
            chapter_url = chapter.get('url', '')
            chapter_title = chapter.get('title', f'Chapter {i}')
            
            print(f'{i}. {chapter_title}')
            print(f'   URL: {chapter_url}')
            
            if '.pdf' in chapter_url.lower():
                pdf_links.append({
                    'title': chapter_title,
                    'url': chapter_url,
                    'index': i
                })
                print('   *** PDF LINK DETECTED ***')
        
        print(f'\nFound {len(pdf_links)} direct PDF links:')
        for pdf_link in pdf_links:
            print(f'- {pdf_link["title"]} -> {pdf_link["url"]}')
else:
    print('Final bibliographic record not found')
    exit()

# Set up headers for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.jstor.org/'
}

# Try accessing each PDF link
successful_pdfs = []

print('\n=== ATTEMPTING TO ACCESS INDIVIDUAL CHAPTER PDFS ===')

for i, pdf_link in enumerate(pdf_links, 1):
    print(f'\n{i}. Trying: {pdf_link["title"]}')
    print(f'   URL: {pdf_link["url"]}')
    
    try:
        response = requests.get(pdf_link['url'], headers=headers, timeout=30)
        print(f'   Status: {response.status_code}')
        print(f'   Content-Type: {response.headers.get("content-type", "unknown")}')
        print(f'   Content-Length: {len(response.content):,} bytes')
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            
            if 'pdf' in content_type or len(response.content) > 10000:  # Likely PDF if large
                print('   *** SUCCESS: PDF CONTENT RETRIEVED ***')
                
                # Save the PDF
                pdf_filename = f'workspace/chapter_{i}_{pdf_link["index"]}.pdf'
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                
                file_size = os.path.getsize(pdf_filename)
                print(f'   ✓ PDF saved to: {pdf_filename}')
                print(f'   File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
                
                successful_pdfs.append({
                    'title': pdf_link['title'],
                    'filename': pdf_filename,
                    'size': file_size,
                    'original_url': pdf_link['url']
                })
            else:
                print(f'   ⚠ Content does not appear to be PDF: {content_type}')
                # Save as HTML for inspection
                html_filename = f'workspace/chapter_{i}_response.html'
                with open(html_filename, 'w', encoding='utf-8') as html_file:
                    html_file.write(response.text)
                print(f'   Saved response as HTML: {html_filename}')
        
        elif response.status_code == 403:
            print('   ❌ Access forbidden (403) - authentication may be required')
        elif response.status_code == 404:
            print('   ❌ Not found (404) - URL may be invalid')
        else:
            print(f'   ❌ Request failed with status {response.status_code}')
    
    except Exception as e:
        print(f'   ❌ Error accessing PDF: {str(e)}')
    
    time.sleep(1)  # Brief pause between requests

print(f'\n=== PDF ACCESS RESULTS: {len(successful_pdfs)} SUCCESSFUL DOWNLOADS ===')

if successful_pdfs:
    for pdf in successful_pdfs:
        print(f'✓ {pdf["title"]} - {pdf["size"]:,} bytes')
        print(f'  File: {pdf["filename"]}')
    
    print('\n=== EXTRACTING TEXT FROM DOWNLOADED PDFS ===')
    
    # Try to extract text from each PDF
    try:
        from langchain_community.document_loaders import PyPDFLoader
        
        all_pages = []
        pdf_page_mapping = []  # Track which PDF each page comes from
        
        for pdf_info in successful_pdfs:
            print(f'\nProcessing: {pdf_info["title"]}')
            
            try:
                loader = PyPDFLoader(pdf_info['filename'])
                pages = loader.load_and_split()
                
                print(f'✓ Extracted {len(pages)} pages from {pdf_info["title"]}')
                
                # Add pages to our collection with source tracking
                start_page_num = len(all_pages) + 1
                for page in pages:
                    all_pages.append(page)
                    pdf_page_mapping.append({
                        'pdf_title': pdf_info['title'],
                        'pdf_filename': pdf_info['filename'],
                        'page_in_collection': len(all_pages),
                        'original_page_num': len(all_pages) - start_page_num + 1
                    })
                
                # Show preview of first page from this PDF
                if pages:
                    preview = pages[0].page_content[:200].replace('\n', ' ')
                    print(f'   First page preview: {preview}...')
            
            except Exception as pdf_error:
                print(f'❌ Error processing {pdf_info["filename"]}: {str(pdf_error)}')
        
        print(f'\n*** TOTAL PAGES COLLECTED: {len(all_pages)} ***')
        
        if len(all_pages) >= 11:
            print('\n=== ANALYZING PAGE 11 FOR TARGET CONTENT ===')
            
            # Get page 11 (index 10)
            page_11 = all_pages[10]
            page_11_source = pdf_page_mapping[10]
            
            print(f'Page 11 source: {page_11_source["pdf_title"]}')
            print(f'Page 11 content length: {len(page_11.page_content):,} characters')
            
            # Save page 11 content
            with open('workspace/page_11_extracted.txt', 'w', encoding='utf-8') as f:
                f.write(f'PAGE 11 CONTENT\n')
                f.write(f'Source: {page_11_source["pdf_title"]}\n')
                f.write(f'PDF File: {page_11_source["pdf_filename"]}\n')
                f.write('='*80 + '\n\n')
                f.write(page_11.page_content)
            
            print('✓ Page 11 content saved to workspace/page_11_extracted.txt')
            
            # Analyze page 11 for paragraphs
            page_11_text = page_11.page_content
            
            # Split into paragraphs (handle different paragraph separators)
            paragraphs = []
            
            # Try different paragraph splitting methods
            if '\n\n' in page_11_text:
                paragraphs = [p.strip() for p in page_11_text.split('\n\n') if p.strip()]
            elif '\n' in page_11_text:
                # Split by single newlines and group consecutive non-empty lines
                lines = [line.strip() for line in page_11_text.split('\n')]
                current_para = []
                for line in lines:
                    if line:
                        current_para.append(line)
                    else:
                        if current_para:
                            paragraphs.append(' '.join(current_para))
                            current_para = []
                if current_para:
                    paragraphs.append(' '.join(current_para))
            else:
                # Fallback: treat entire content as one paragraph
                paragraphs = [page_11_text.strip()]
            
            print(f'\nFound {len(paragraphs)} paragraphs on page 11')
            
            if len(paragraphs) >= 2:
                second_to_last_para = paragraphs[-2]
                print(f'\n=== SECOND-TO-LAST PARAGRAPH ON PAGE 11 ===')
                print('='*80)
                print(second_to_last_para)
                print('='*80)
                
                # Save the specific paragraph
                with open('workspace/page_11_second_to_last_paragraph.txt', 'w', encoding='utf-8') as f:
                    f.write('SECOND-TO-LAST PARAGRAPH FROM PAGE 11\n')
                    f.write('='*50 + '\n\n')
                    f.write(second_to_last_para)
                
                print('\n✓ Second-to-last paragraph saved to workspace/page_11_second_to_last_paragraph.txt')
                
                # Look for endnote references in this paragraph
                print('\n=== SEARCHING FOR ENDNOTE REFERENCES ===')
                
                endnote_patterns = [
                    r'\b(\d+)\b',  # Simple numbers
                    r'\[(\d+)\]',  # Numbers in brackets
                    r'\((\d+)\)',  # Numbers in parentheses
                    r'\b(\d+)\.',  # Numbers with periods
                    r'see note (\d+)',  # "see note X" format
                    r'note (\d+)',  # "note X" format
                    r'footnote (\d+)',  # "footnote X" format
                ]
                
                found_endnotes = []
                for pattern in endnote_patterns:
                    matches = re.findall(pattern, second_to_last_para, re.IGNORECASE)
                    if matches:
                        for match in matches:
                            if match.isdigit() and 1 <= int(match) <= 200:  # Reasonable endnote range
                                found_endnotes.append(int(match))
                
                # Remove duplicates and sort
                found_endnotes = sorted(list(set(found_endnotes)))
                
                if found_endnotes:
                    print(f'*** FOUND ENDNOTE REFERENCES: {found_endnotes} ***')
                    
                    # Now search for the actual endnotes in all collected pages
                    print('\n=== SEARCHING ALL PAGES FOR ENDNOTES SECTION ===')
                    
                    # Combine all pages to search for endnotes
                    full_text = '\n\n'.join([page.page_content for page in all_pages])
                    
                    print(f'Total text to search: {len(full_text):,} characters')
                    
                    # Search for Wikipedia citations with November access dates
                    print('\n=== SEARCHING FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATE ===')
                    
                    # Comprehensive Wikipedia citation patterns
                    wikipedia_patterns = [
                        r'wikipedia[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,50}',
                        r'en\.wikipedia\.org[^\n]{0,200}november[^\n]{0,100}\d{1,2}[^\n]{0,50}',
                        r'accessed[^\n]{0,100}november[^\n]{0,50}\d{1,2}[^\n]{0,100}wikipedia[^\n]{0,100}',
                        r'november[^\n]{0,50}\d{1,2}[^\n]{0,100}wikipedia[^\n]{0,200}',
                        r'\d{1,2}[^\n]{0,20}november[^\n]{0,100}wikipedia[^\n]{0,200}',
                        r'wikipedia[^\n]{0,300}accessed[^\n]{0,100}november[^\n]{0,50}\d{1,2}[^\n]{0,50}'
                    ]
                    
                    wikipedia_citations = []
                    for pattern in wikipedia_patterns:
                        matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                        for match in matches:
                            citation_text = match.group(0)
                            
                            # Extract the day from November date
                            day_patterns = [
                                r'november\s+(\d{1,2})',
                                r'(\d{1,2})\s+november',
                                r'november\s+(\d{1,2})(?:st|nd|rd|th)?',
                                r'(\d{1,2})(?:st|nd|rd|th)?\s+november'
                            ]
                            
                            day_found = None
                            for day_pattern in day_patterns:
                                day_match = re.search(day_pattern, citation_text, re.IGNORECASE)
                                if day_match:
                                    day_found = day_match.group(1)
                                    break
                            
                            if day_found:
                                # Check if this citation is near any of our endnote numbers
                                citation_context = full_text[max(0, match.start()-500):match.end()+500]
                                
                                related_endnotes = []
                                for endnote_num in found_endnotes:
                                    if str(endnote_num) in citation_context:
                                        related_endnotes.append(endnote_num)
                                
                                wikipedia_citations.append({
                                    'citation': citation_text,
                                    'november_day': day_found,
                                    'position': match.start(),
                                    'context': citation_context,
                                    'related_endnotes': related_endnotes
                                })
                    
                    # Remove duplicates based on citation text
                    unique_citations = []
                    seen_citations = set()
                    for citation in wikipedia_citations:
                        citation_key = citation['citation'].strip().lower()
                        if citation_key not in seen_citations:
                            seen_citations.add(citation_key)
                            unique_citations.append(citation)
                    
                    if unique_citations:
                        print(f'\n🎯 FOUND {len(unique_citations)} UNIQUE WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES:')
                        
                        for i, citation in enumerate(unique_citations, 1):
                            print(f'\nCitation {i}:')
                            print(f'November day: {citation["november_day"]}')
                            print(f'Position in text: {citation["position"]:,}')
                            if citation['related_endnotes']:
                                print(f'Related endnotes: {citation["related_endnotes"]}')
                            print('Citation text:')
                            print('='*60)
                            print(citation['citation'])
                            print('='*60)
                            
                            # Show some context
                            context_preview = citation['context'][:300] + '...' if len(citation['context']) > 300 else citation['context']
                            print(f'Context: {context_preview}')
                            print('-'*60)
                        
                        # Save the analysis
                        analysis_data = {
                            'source_pdfs': [pdf['filename'] for pdf in successful_pdfs],
                            'total_pages_analyzed': len(all_pages),
                            'page_11_source': page_11_source,
                            'page_11_paragraph_count': len(paragraphs),
                            'second_to_last_paragraph': second_to_last_para,
                            'endnote_references_found': found_endnotes,
                            'wikipedia_citations': unique_citations,
                            'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        with open('workspace/wikipedia_endnote_analysis.json', 'w', encoding='utf-8') as f:
                            json.dump(analysis_data, f, indent=2, ensure_ascii=False)
                        
                        print('\n✓ Complete analysis saved to workspace/wikipedia_endnote_analysis.json')
                        
                        # Determine the most likely answer
                        if len(unique_citations) == 1:
                            answer_day = unique_citations[0]['november_day']
                            print(f'\n*** ANSWER FOUND: The Wikipedia article was accessed on November {answer_day} ***')
                        elif len(unique_citations) > 1:
                            # Look for citations most closely related to our endnote references
                            best_citation = None
                            max_related_endnotes = 0
                            
                            for citation in unique_citations:
                                if len(citation['related_endnotes']) > max_related_endnotes:
                                    max_related_endnotes = len(citation['related_endnotes'])
                                    best_citation = citation
                            
                            if best_citation:
                                answer_day = best_citation['november_day']
                                print(f'\n*** MOST LIKELY ANSWER: November {answer_day} ***')
                                print(f'(This citation is related to endnotes: {best_citation["related_endnotes"]})')
                            else:
                                print(f'\n*** MULTIPLE CANDIDATES FOUND - Manual review needed ***')
                                for i, citation in enumerate(unique_citations, 1):
                                    print(f'Option {i}: November {citation["november_day"]}')
                    else:
                        print('\n⚠ No Wikipedia citations with November access dates found')
                        
                        # Broader search for any Wikipedia references
                        print('\nSearching for any Wikipedia references...')
                        wiki_matches = re.finditer(r'wikipedia[^\n]{0,100}', full_text, re.IGNORECASE)
                        wiki_refs = [match.group(0) for match in wiki_matches]
                        
                        if wiki_refs:
                            print(f'Found {len(wiki_refs)} general Wikipedia references:')
                            for i, ref in enumerate(wiki_refs[:5], 1):
                                print(f'{i}. {ref}')
                        else:
                            print('No Wikipedia references found at all')
                else:
                    print('\n⚠ No endnote references found in second-to-last paragraph')
                    print('Paragraph content for manual inspection:')
                    print(second_to_last_para)
            else:
                print(f'\n⚠ Page 11 has fewer than 2 paragraphs ({len(paragraphs)} found)')
                if paragraphs:
                    print('Available paragraphs:')
                    for i, para in enumerate(paragraphs, 1):
                        print(f'{i}. {para[:150]}...')
        else:
            print(f'\n⚠ Only {len(all_pages)} pages collected, page 11 not available')
            print('Available pages:')
            for i, page in enumerate(all_pages[:10], 1):
                source = pdf_page_mapping[i-1]
                preview = page.page_content[:100].replace('\n', ' ')
                print(f'Page {i} (from {source["pdf_title"]}): {preview}...')
    
    except ImportError:
        print('❌ PyPDFLoader not available - cannot extract text from PDFs')
        print('PDFs have been downloaded but text extraction is not possible')
    except Exception as extraction_error:
        print(f'❌ Error during text extraction: {str(extraction_error)}')
else:
    print('\n❌ No PDFs were successfully downloaded')
    print('Cannot proceed with page 11 analysis')

print('\n' + '='*100)
print('ALTERNATIVE ACCESS ATTEMPT COMPLETE')
print('='*100)
print('Summary:')
print(f'- Attempted to access {len(pdf_links) if "pdf_links" in locals() else 0} PDF links')
print(f'- Successfully downloaded {len(successful_pdfs)} PDFs')
if successful_pdfs:
    print('- Extracted text and analyzed for page 11 content')
    print('- Searched for Wikipedia citations with November access dates')
print('\nObjective: Find exact day in November when Wikipedia article was accessed')
```

### Development Step 3: **Title:**  
Extract Wikipedia Access Date from Endnote on Page 11 of 'The Responsibility of Intellectuals' (2019)

**Description**: Access and download the full text of 'The Responsibility of Intellectuals' (DOI 10.2307/j.ctv9b2xdv) from JSTOR or UCL Press. Since this is a 2019 UCL Press publication available through JSTOR, retrieve the complete book content and save it to the workspace. Focus on locating page 11, identifying the second-to-last paragraph on that page, and extracting the specific endnote referenced in that paragraph. The endnote should contain a Wikipedia article citation with a November access date - extract the exact day of the month when the Wikipedia article was accessed.

**Use Cases**:
- Academic integrity verification by university librarians checking the accuracy and access dates of Wikipedia citations in scholarly books
- Automated extraction of citation metadata for digital humanities researchers compiling bibliometric datasets from open-access monographs
- Legal teams auditing referenced online materials in published works to confirm compliance with copyright and citation standards
- Publishers conducting quality control to ensure endnotes in digital books properly reference and date online sources
- Research assistants preparing annotated bibliographies by programmatically identifying and extracting Wikipedia access dates from book endnotes
- Journalists fact-checking claims in recent academic books by tracing the exact Wikipedia versions cited at specific dates
- Digital archivists preserving citation trails by extracting and archiving referenced web pages as they appeared on the cited access date
- Educational technology developers building tools that highlight and verify online references in course materials for instructors

```
import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import re

print('=== ACCESSING FULL TEXT OF "THE RESPONSIBILITY OF INTELLECTUALS" ===')
print('DOI: 10.2307/j.ctv9b2xdv')
print('Objective: Locate page 11, find second-to-last paragraph, extract endnote with Wikipedia citation (November access date)')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# First, let's examine the existing workspace files to understand what we have
print('=== INSPECTING EXISTING WORKSPACE FILES ===')
workspace_files = os.listdir('workspace')
if workspace_files:
    print(f'Found {len(workspace_files)} files in workspace:')
    for file in workspace_files:
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')
else:
    print('No existing files in workspace')

# Check if we have the final bibliographic record
final_record_path = 'workspace/final_bibliographic_record.json'
if os.path.exists(final_record_path):
    print('\n=== INSPECTING FINAL BIBLIOGRAPHIC RECORD ===')
    with open(final_record_path, 'r', encoding='utf-8') as f:
        biblio_data = json.load(f)
    
    print('Available keys in bibliographic record:')
    for key in biblio_data.keys():
        print(f'- {key}: {type(biblio_data[key])}')
    
    print(f'\nKey information:')
    print(f'Title: {biblio_data.get("title", "Unknown")}')
    print(f'Publisher: {biblio_data.get("publisher", "Unknown")}')
    print(f'Year: {biblio_data.get("publication_year", "Unknown")}')
    print(f'DOI URL: {biblio_data.get("doi_url", "Unknown")}')
    print(f'JSTOR URL: {biblio_data.get("jstor_url", "Unknown")}')
    
    # Check chapters/sections structure
    if 'chapters_sections' in biblio_data and biblio_data['chapters_sections']:
        print(f'\nBook structure: {len(biblio_data["chapters_sections"])} chapters/sections')
        for i, chapter in enumerate(biblio_data['chapters_sections'][:3], 1):
            print(f'{i}. {chapter.get("title", "No title")}')
            print(f'   URL: {chapter.get("url", "No URL")}')
else:
    print('Final bibliographic record not found')

# Now let's try to access the full text through JSTOR
print('\n=== ATTEMPTING TO ACCESS FULL TEXT VIA JSTOR ===')

# Set up headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Try to access the main JSTOR book page
jstor_main_url = 'https://www.jstor.org/stable/j.ctv9b2xdv'
print(f'Accessing main JSTOR page: {jstor_main_url}')

try:
    response = requests.get(jstor_main_url, headers=headers, timeout=30)
    print(f'JSTOR main page status: {response.status_code}')
    print(f'Final URL: {response.url}')
    print(f'Content length: {len(response.content):,} bytes')
    
    if response.status_code == 200:
        # Save the main page for analysis
        with open('workspace/jstor_main_page.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print('✓ JSTOR main page saved to workspace/jstor_main_page.html')
        
        # Parse the page to look for full-text access options
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text().lower()
        
        # Look for "read online", "full text", "PDF", or similar access options
        access_indicators = [
            'read online', 'full text', 'download pdf', 'view pdf',
            'open access', 'free access', 'read book', 'view book'
        ]
        
        found_access_options = []
        for indicator in access_indicators:
            if indicator in page_text:
                found_access_options.append(indicator)
        
        if found_access_options:
            print(f'\n✓ Found access indicators: {found_access_options}')
        else:
            print('\n⚠ No obvious access indicators found in page text')
        
        # Look for links that might provide full-text access
        access_links = []
        
        # Search for various types of access links
        link_selectors = [
            'a[href*="pdf"]',
            'a[href*="read"]',
            'a[href*="view"]',
            'a[href*="download"]',
            'a[href*="full"]',
            'a[href*="text"]',
            '.pdf-link a',
            '.read-link a',
            '.download-link a',
            '.access-link a'
        ]
        
        for selector in link_selectors:
            try:
                links = soup.select(selector)
                for link in links:
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute
                        if href.startswith('/'):
                            href = urljoin(jstor_main_url, href)
                        
                        link_text = link.get_text().strip()
                        if len(link_text) > 0 and len(link_text) < 100:  # Reasonable link text length
                            access_links.append({
                                'url': href,
                                'text': link_text,
                                'selector': selector
                            })
            except Exception as e:
                print(f'Error with selector {selector}: {str(e)}')
        
        # Remove duplicates
        unique_links = []
        seen_urls = set()
        for link in access_links:
            if link['url'] not in seen_urls:
                seen_urls.add(link['url'])
                unique_links.append(link)
        
        print(f'\nFound {len(unique_links)} potential access links:')
        for i, link in enumerate(unique_links[:10], 1):  # Show first 10
            print(f'{i}. "{link["text"]}" -> {link["url"]}')
            print(f'   (Found via: {link["selector"]})')
        
        # Look specifically for chapter/section links that might contain page 11
        chapter_links = []
        for link in unique_links:
            link_url = link['url'].lower()
            link_text = link['text'].lower()
            
            # Check if this might be a chapter or section link
            if any(indicator in link_url or indicator in link_text for indicator in 
                   ['chapter', 'section', 'pdf', 'ctv9b2xdv']):
                chapter_links.append(link)
        
        if chapter_links:
            print(f'\n*** FOUND {len(chapter_links)} POTENTIAL CHAPTER/SECTION LINKS ***')
            for i, link in enumerate(chapter_links[:5], 1):
                print(f'{i}. "{link["text"]}" -> {link["url"]}')
        
        # Try to access the first promising link
        if chapter_links:
            print('\n=== ATTEMPTING TO ACCESS FIRST CHAPTER/SECTION LINK ===')
            first_link = chapter_links[0]
            print(f'Trying: {first_link["text"]} -> {first_link["url"]}')
            
            try:
                chapter_response = requests.get(first_link['url'], headers=headers, timeout=30)
                print(f'Chapter access status: {chapter_response.status_code}')
                print(f'Content type: {chapter_response.headers.get("content-type", "unknown")}')
                print(f'Content length: {len(chapter_response.content):,} bytes')
                
                if chapter_response.status_code == 200:
                    content_type = chapter_response.headers.get('content-type', '').lower()
                    
                    if 'pdf' in content_type:
                        print('\n*** PDF CONTENT DETECTED ***')
                        pdf_path = 'workspace/responsibility_intellectuals_chapter.pdf'
                        
                        with open(pdf_path, 'wb') as pdf_file:
                            pdf_file.write(chapter_response.content)
                        
                        file_size = os.path.getsize(pdf_path)
                        print(f'✓ PDF saved to: {pdf_path}')
                        print(f'File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)')
                        
                        # Try to extract text from PDF if possible
                        try:
                            print('\nAttempting to extract text from PDF...')
                            from langchain_community.document_loaders import PyPDFLoader
                            
                            loader = PyPDFLoader(pdf_path)
                            pages = loader.load_and_split()
                            
                            print(f'✓ PDF loaded successfully with {len(pages)} pages')
                            
                            # Look for page 11 specifically
                            if len(pages) >= 11:
                                page_11_content = pages[10].page_content  # Page 11 is index 10
                                print(f'\n=== PAGE 11 CONTENT FOUND ===') 
                                print(f'Page 11 length: {len(page_11_content):,} characters')
                                print(f'\nFirst 500 characters of page 11:')
                                print('='*80)
                                print(page_11_content[:500] + '...')
                                print('='*80)
                                
                                # Save page 11 content
                                with open('workspace/page_11_content.txt', 'w', encoding='utf-8') as f:
                                    f.write(page_11_content)
                                print('\n✓ Page 11 content saved to workspace/page_11_content.txt')
                                
                                # Look for the second-to-last paragraph
                                paragraphs = [p.strip() for p in page_11_content.split('\n\n') if p.strip()]
                                print(f'\nFound {len(paragraphs)} paragraphs on page 11')
                                
                                if len(paragraphs) >= 2:
                                    second_to_last_para = paragraphs[-2]
                                    print(f'\n=== SECOND-TO-LAST PARAGRAPH ON PAGE 11 ===')
                                    print('='*80)
                                    print(second_to_last_para)
                                    print('='*80)
                                    
                                    # Look for endnote references in this paragraph
                                    endnote_patterns = [
                                        r'\b(\d+)\b',  # Simple numbers
                                        r'\[(\d+)\]',  # Numbers in brackets
                                        r'\((\d+)\)',  # Numbers in parentheses
                                        r'\b(\d+)\.',  # Numbers with periods
                                        r'see note (\d+)',  # "see note X" format
                                        r'note (\d+)',  # "note X" format
                                    ]
                                    
                                    found_endnotes = []
                                    for pattern in endnote_patterns:
                                        matches = re.findall(pattern, second_to_last_para, re.IGNORECASE)
                                        if matches:
                                            for match in matches:
                                                if match.isdigit() and int(match) <= 100:  # Reasonable endnote number
                                                    found_endnotes.append(int(match))
                                    
                                    # Remove duplicates and sort
                                    found_endnotes = sorted(list(set(found_endnotes)))
                                    
                                    if found_endnotes:
                                        print(f'\n*** FOUND ENDNOTE REFERENCES: {found_endnotes} ***')
                                        
                                        # Now we need to find the actual endnotes
                                        print('\n=== SEARCHING FOR ENDNOTES SECTION ===')
                                        
                                        # Combine all pages to search for endnotes
                                        full_text = '\n\n'.join([page.page_content for page in pages])
                                        
                                        # Look for endnotes section
                                        endnotes_indicators = [
                                            'notes', 'endnotes', 'references', 'footnotes',
                                            'bibliography', 'works cited'
                                        ]
                                        
                                        endnotes_section_found = False
                                        for indicator in endnotes_indicators:
                                            pattern = rf'\b{indicator}\b'
                                            matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
                                            if matches:
                                                print(f'Found "{indicator}" section at {len(matches)} locations')
                                                endnotes_section_found = True
                                        
                                        # Search for specific endnote numbers with Wikipedia citations
                                        print('\n=== SEARCHING FOR WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATE ===')
                                        
                                        # Look for Wikipedia citations with November access dates
                                        wikipedia_patterns = [
                                            r'wikipedia[^\n]*november[^\n]*accessed[^\n]*',
                                            r'en\.wikipedia\.org[^\n]*november[^\n]*',
                                            r'accessed[^\n]*november[^\n]*wikipedia[^\n]*',
                                            r'november[^\n]*\d{1,2}[^\n]*wikipedia[^\n]*',
                                            r'wikipedia[^\n]*accessed[^\n]*november[^\n]*\d{1,2}[^\n]*'
                                        ]
                                        
                                        wikipedia_citations = []
                                        for pattern in wikipedia_patterns:
                                            matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                                            for match in matches:
                                                citation_text = match.group(0)
                                                # Extract the day from November date
                                                day_match = re.search(r'november\s+(\d{1,2})', citation_text, re.IGNORECASE)
                                                if day_match:
                                                    day = day_match.group(1)
                                                    wikipedia_citations.append({
                                                        'citation': citation_text,
                                                        'november_day': day,
                                                        'position': match.start()
                                                    })
                                        
                                        if wikipedia_citations:
                                            print(f'\n🎯 FOUND {len(wikipedia_citations)} WIKIPEDIA CITATIONS WITH NOVEMBER ACCESS DATES:')
                                            
                                            for i, citation in enumerate(wikipedia_citations, 1):
                                                print(f'\nCitation {i}:')
                                                print(f'November day: {citation["november_day"]}')
                                                print(f'Position in text: {citation["position"]}')
                                                print('Citation text:')
                                                print('='*60)
                                                print(citation['citation'])
                                                print('='*60)
                                            
                                            # Save the Wikipedia citations
                                            citations_data = {
                                                'source_file': pdf_path,
                                                'page_11_paragraph_count': len(paragraphs),
                                                'second_to_last_paragraph': second_to_last_para,
                                                'endnote_references_found': found_endnotes,
                                                'wikipedia_citations': wikipedia_citations,
                                                'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                                            }
                                            
                                            with open('workspace/wikipedia_citations_analysis.json', 'w', encoding='utf-8') as f:
                                                json.dump(citations_data, f, indent=2, ensure_ascii=False)
                                            
                                            print('\n✓ Wikipedia citations analysis saved to workspace/wikipedia_citations_analysis.json')
                                            
                                            # Extract the specific day for the answer
                                            if len(wikipedia_citations) == 1:
                                                answer_day = wikipedia_citations[0]['november_day']
                                                print(f'\n*** ANSWER FOUND: The Wikipedia article was accessed on November {answer_day} ***')
                                            elif len(wikipedia_citations) > 1:
                                                print(f'\n*** MULTIPLE WIKIPEDIA CITATIONS FOUND - Need to determine which is from page 11 endnote ***')
                                                for i, citation in enumerate(wikipedia_citations, 1):
                                                    print(f'Option {i}: November {citation["november_day"]}')
                                        else:
                                            print('\n⚠ No Wikipedia citations with November access dates found')
                                            print('Searching for any Wikipedia references...')
                                            
                                            # Broader search for Wikipedia
                                            wiki_matches = re.finditer(r'wikipedia[^\n]{0,200}', full_text, re.IGNORECASE)
                                            wiki_refs = [match.group(0) for match in wiki_matches]
                                            
                                            if wiki_refs:
                                                print(f'Found {len(wiki_refs)} general Wikipedia references:')
                                                for i, ref in enumerate(wiki_refs[:5], 1):
                                                    print(f'{i}. {ref[:100]}...')
                                    else:
                                        print('\n⚠ No endnote references found in second-to-last paragraph')
                                        print('Showing paragraph content for manual inspection:')
                                        print(second_to_last_para)
                                else:
                                    print(f'\n⚠ Page 11 has fewer than 2 paragraphs ({len(paragraphs)} found)')
                                    if paragraphs:
                                        print('Available paragraphs:')
                                        for i, para in enumerate(paragraphs, 1):
                                            print(f'{i}. {para[:100]}...')
                            else:
                                print(f'\n⚠ PDF has only {len(pages)} pages, page 11 not available')
                                print('Available pages:')
                                for i, page in enumerate(pages[:5], 1):
                                    preview = page.page_content[:100].replace('\n', ' ')
                                    print(f'Page {i}: {preview}...')
                        
                        except ImportError:
                            print('⚠ PyPDFLoader not available - PDF saved but text extraction skipped')
                        except Exception as pdf_error:
                            print(f'❌ PDF text extraction error: {str(pdf_error)}')
                    
                    elif 'html' in content_type:
                        print('\n*** HTML CONTENT DETECTED ***')
                        
                        # Save HTML content
                        with open('workspace/chapter_content.html', 'w', encoding='utf-8') as f:
                            f.write(chapter_response.text)
                        print('✓ HTML content saved to workspace/chapter_content.html')
                        
                        # Parse HTML for text content
                        chapter_soup = BeautifulSoup(chapter_response.content, 'html.parser')
                        
                        # Remove navigation and non-content elements
                        for element in chapter_soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                            element.decompose()
                        
                        chapter_text = chapter_soup.get_text()
                        print(f'\nExtracted HTML text length: {len(chapter_text):,} characters')
                        print(f'First 300 characters: {chapter_text[:300]}...')
                        
                        # Save extracted text
                        with open('workspace/chapter_text_content.txt', 'w', encoding='utf-8') as f:
                            f.write(chapter_text)
                        print('✓ Chapter text content saved to workspace/chapter_text_content.txt')
                    
                    else:
                        print(f'\n*** UNKNOWN CONTENT TYPE: {content_type} ***')
                        print('Saving raw content for analysis')
                        
                        with open('workspace/unknown_content.txt', 'w', encoding='utf-8') as f:
                            f.write(chapter_response.text)
                        print('✓ Raw content saved to workspace/unknown_content.txt')
                
                else:
                    print(f'❌ Chapter access failed with status: {chapter_response.status_code}')
            
            except Exception as chapter_error:
                print(f'❌ Error accessing chapter: {str(chapter_error)}')
        
        else:
            print('\n⚠ No chapter/section links found to try')
    
    else:
        print(f'❌ JSTOR main page access failed with status: {response.status_code}')

except Exception as e:
    print(f'❌ Error accessing JSTOR: {str(e)}')

print('\n' + '='*100)
print('FULL TEXT ACCESS ATTEMPT SUMMARY')
print('='*100)
print('Objective: Access full text to find page 11, second-to-last paragraph, and Wikipedia endnote with November access date')
print('\nFiles created in workspace:')
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f'- {file} ({file_size:,} bytes)')

print('\n*** NEXT STEP: Analyze extracted content for the specific Wikipedia citation ***')
```

### Development Step 4: Extract July 3 2023 LOTR Wikipedia Internal Links Toward A Song of Ice and Fire

**Description**: Access the archived Wikipedia page for 'The Lord of the Rings' (book) as it appeared at the end of July 3, 2023. Use the Wayback Machine or Wikipedia's revision history to retrieve the specific version from that date. Extract all outbound links from the page content, focusing on internal Wikipedia links that could potentially lead toward 'A Song of Ice and Fire'. Create a comprehensive list of linked pages including literature, fantasy, author, publisher, and genre-related links that might serve as stepping stones in the path-finding process.

**Use Cases**:
- Competitive product mapping for market intelligence teams: archive the Wikipedia page of a rival’s flagship product, extract outbound links, and use BFS to uncover related technologies and collaborators leading to a specific emerging competitor.
- Academic literature exploration for research librarians: retrieve an archived revision of a foundational theory page, scrape internal links, and trace a path through related journals and authors to locate a target contemporary study.
- SEO internal linking audit for digital marketing agencies: load a historical snapshot of a high-traffic Wikipedia article, extract its link network, and identify the shortest chain of links that leads to pages optimized for a target keyword.
- Educational curriculum design for e-learning platforms: access the archived “Introduction to Biology” page, gather its outbound topic links, and map a learning path toward advanced genetics content using breadth-first search.
- Historical content evolution analysis for digital archivists: pull the July 2023 version of a political event page, extract links, and reconstruct how references to a specific legislation article appeared over time by finding link paths.
- Knowledge graph augmentation for AI research teams: scrape a past revision of an ontology page, collect entity links, and build a linkage chain to a new domain-specific concept to enrich the graph with contextual relationships.
- Due diligence support for consulting firms: obtain an archived corporate biography page, scrape its network of partner and subsidiary links, and run BFS to identify the shortest route to a target industry regulation page.

```
import requests
from bs4 import BeautifulSoup
import json
import time
from collections import deque
from datetime import datetime
import os

print("=== FIXING BFS PATH-FINDING WITH DIRECT HTML SCRAPING ===")
print("Objective: Find path from LOTR links to 'A Song of Ice and Fire' using HTML scraping\n")

# Load the LOTR links data
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("❌ No workspace directory found")
    exit()

workspace_dir = workspace_dirs[0]
lotr_file = os.path.join(workspace_dir, 'lotr_wikipedia_links_july_2023.json')

print(f"Loading LOTR links from: {os.path.basename(lotr_file)}\n")

with open(lotr_file, 'r', encoding='utf-8') as f:
    lotr_data = json.load(f)

# Select high-priority starting nodes
starting_nodes = set()
target_variations = [
    "A Song of Ice and Fire",
    "Game of Thrones", 
    "George R. R. Martin",
    "George R.R. Martin",
    "George Martin",
    "A Game of Thrones"
]

print("=== SELECTING MOST PROMISING STARTING NODES ===")

# Focus on the most likely connections to fantasy literature
high_priority_nodes = [
    "High fantasy",
    "Fantasy", 
    "Epic fantasy",
    "J. R. R. Tolkien",
    "Fantasy literature",
    "The Encyclopedia of Fantasy",
    "International Fantasy Award"
]

# Add high-priority nodes if they exist in our data
for category_name, links in lotr_data.get('categorized_links', {}).items():
    for link in links:
        if isinstance(link, dict) and 'article_name' in link:
            article_name = requests.utils.unquote(link['article_name']).replace('_', ' ')
            if article_name in high_priority_nodes:
                starting_nodes.add(article_name)
                print(f"Added high-priority node: {article_name}")

# If we don't have enough high-priority nodes, add some from fantasy/literature categories
if len(starting_nodes) < 10:
    for category in ['fantasy', 'literature']:
        if category in lotr_data.get('categorized_links', {}):
            for link in lotr_data['categorized_links'][category][:5]:  # Just first 5 from each
                if isinstance(link, dict) and 'article_name' in link:
                    article_name = requests.utils.unquote(link['article_name']).replace('_', ' ')
                    starting_nodes.add(article_name)

print(f"\nTotal starting nodes selected: {len(starting_nodes)}")
for i, node in enumerate(list(starting_nodes), 1):
    print(f"  {i:2d}. {node}")

# Function to scrape Wikipedia page links directly
def get_wikipedia_links_html(page_title, max_links=50):
    """Scrape Wikipedia page links directly from HTML"""
    try:
        # Convert page title to URL format
        url_title = page_title.replace(' ', '_')
        url = f"https://en.wikipedia.org/wiki/{requests.utils.quote(url_title)}"
        
        print(f"  Scraping: {page_title}")
        print(f"  URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the main content area
            main_content = soup.find('div', {'id': 'mw-content-text'})
            if not main_content:
                main_content = soup
            
            # Extract Wikipedia article links
            links = []
            for link in main_content.find_all('a', href=True):
                href = link.get('href', '')
                if href.startswith('/wiki/') and ':' not in href.split('/')[-1]:
                    # Extract article name from URL
                    article_name = href.split('/')[-1].replace('_', ' ')
                    article_name = requests.utils.unquote(article_name)
                    
                    # Filter out non-article pages
                    skip_patterns = ['File:', 'Category:', 'Template:', 'User:', 'Talk:', 'Wikipedia:', 'Help:', 'Portal:', 'Special:', 'Media:']
                    if not any(pattern in article_name for pattern in skip_patterns):
                        if article_name not in links and len(links) < max_links:
                            links.append(article_name)
            
            print(f"    Found {len(links)} article links")
            return links
            
        elif response.status_code == 404:
            print(f"    Page not found: {page_title}")
            return []
        else:
            print(f"    HTTP error {response.status_code} for {page_title}")
            return []
            
    except Exception as e:
        print(f"    Error scraping {page_title}: {str(e)}")
        return []

# Function to check if we found our target
def is_target(page_title):
    """Check if the page title matches our target variations"""
    page_lower = page_title.lower()
    for target in target_variations:
        if target.lower() == page_lower or target.lower() in page_lower:
            return True
    return False

# Function to check for promising leads
def is_promising_lead(page_title):
    """Check if page title suggests it might lead to our target"""
    page_lower = page_title.lower()
    promising_keywords = [
        'fantasy', 'epic fantasy', 'high fantasy', 'fantasy literature',
        'fantasy series', 'fantasy novel', 'fantasy author', 'fantasy writer',
        'martin', 'george', 'song', 'ice', 'fire', 'game', 'thrones',
        'contemporary fantasy', 'modern fantasy', 'fantasy saga'
    ]
    return any(keyword in page_lower for keyword in promising_keywords)

# BFS Implementation with HTML scraping
print("\n=== STARTING BREADTH-FIRST SEARCH WITH HTML SCRAPING ===")
print(f"Target variations: {target_variations}\n")

# Initialize BFS structures
queue = deque()
visited = set()
parent = {}
depth = {}
found_paths = []
max_depth = 2  # Reduced depth to be more focused
max_requests = 20  # Reduced requests due to slower HTML scraping
request_count = 0

# Add starting nodes to queue
for node in starting_nodes:
    queue.append(node)
    depth[node] = 0
    parent[node] = None

print(f"Initialized BFS queue with {len(queue)} starting nodes")
print(f"Search parameters: max_depth={max_depth}, max_requests={max_requests}\n")

# Function to reconstruct path
def get_path(node, parent_dict):
    """Reconstruct the path from start to target node"""
    path = []
    current = node
    while current is not None:
        path.append(current)
        current = parent_dict.get(current)
    return list(reversed(path))

# Main BFS loop
start_time = datetime.now()
promisingLeads = []  # Track promising leads for later analysis

while queue and request_count < max_requests:
    current_node = queue.popleft()
    
    if current_node in visited:
        continue
        
    visited.add(current_node)
    current_depth = depth[current_node]
    
    print(f"\n--- Processing: {current_node} (depth {current_depth}) ---")
    
    # Check if we found the target
    if is_target(current_node):
        path = get_path(current_node, parent)
        found_paths.append({
            'target_found': current_node,
            'path': path,
            'depth': current_depth,
            'path_length': len(path)
        })
        print(f"\n🎯 TARGET FOUND: {current_node}")
        print(f"Path length: {len(path)} steps")
        print(f"Path: {' → '.join(path)}")
        break
    
    # Don't go deeper than max_depth
    if current_depth >= max_depth:
        print(f"  Reached max depth ({max_depth}), skipping expansion")
        continue
    
    # Get outbound links from current node
    outbound_links = get_wikipedia_links_html(current_node)
    request_count += 1
    
    # Process each outbound link
    new_nodes_added = 0
    target_hints = []
    
    for link in outbound_links:
        if link not in visited:
            # Check if this is our target
            if is_target(link):
                # Found target! Add to queue and it will be processed next
                queue.appendleft(link)  # Add to front for immediate processing
                depth[link] = current_depth + 1
                parent[link] = current_node
                target_hints.append(f"TARGET: {link}")
                new_nodes_added += 1
            elif is_promising_lead(link):
                # This looks promising, prioritize it
                queue.appendleft(link)
                depth[link] = current_depth + 1
                parent[link] = current_node
                target_hints.append(f"PROMISING: {link}")
                promisingLeads.append({
                    'node': link,
                    'parent': current_node,
                    'depth': current_depth + 1
                })
                new_nodes_added += 1
            elif current_depth + 1 < max_depth:  # Only add regular nodes if we haven't reached max depth
                queue.append(link)
                depth[link] = current_depth + 1
                parent[link] = current_node
                new_nodes_added += 1
    
    print(f"  Added {new_nodes_added} new nodes to queue")
    
    if target_hints:
        print(f"  🔍 Important findings: {target_hints[:3]}")
    
    # Add delay to be respectful to Wikipedia
    time.sleep(1)
    
    # Progress update
    elapsed = (datetime.now() - start_time).total_seconds()
    print(f"  Progress: {len(visited)} visited, {len(queue)} in queue, {request_count}/{max_requests} requests")
    print(f"  Elapsed: {elapsed:.1f}s")

# Final results
print(f"\n=== SEARCH COMPLETE ===")
elapsed = (datetime.now() - start_time).total_seconds()
print(f"Search completed in {elapsed:.1f} seconds")
print(f"Nodes visited: {len(visited)}")
print(f"Requests made: {request_count}")
print(f"Paths found: {len(found_paths)}")

# Save results
search_results = {
    'search_metadata': {
        'start_time': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'elapsed_seconds': elapsed,
        'target_variations': target_variations,
        'max_depth': max_depth,
        'max_requests': max_requests,
        'requests_made': request_count,
        'nodes_visited': len(visited),
        'method': 'HTML_scraping'
    },
    'starting_nodes': list(starting_nodes),
    'paths_found': found_paths,
    'promising_leads': promisingLeads,
    'visited_nodes': list(visited)
}

results_file = os.path.join(workspace_dir, 'bfs_html_scraping_results.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False, default=str)

print(f"\n=== FINAL RESULTS ===")
if found_paths:
    print(f"\n🎉 SUCCESS: Found {len(found_paths)} path(s) to target!\n")
    for i, path_info in enumerate(found_paths, 1):
        print(f"Path {i}:")
        print(f"  Target: {path_info['target_found']}")
        print(f"  Length: {path_info['path_length']} steps")
        print(f"  Route: {' → '.join(path_info['path'])}")
        print()
else:
    print(f"\n⚠️ No direct paths found within {max_depth} steps using {max_requests} requests")
    
    if promisingLeads:
        print(f"\n🔍 Found {len(promisingLeads)} promising leads for deeper exploration:")
        for i, lead in enumerate(promisingLeads[:5], 1):
            print(f"  {i}. {lead['node']} (depth {lead['depth']})")
            print(f"     From: {lead['parent']}")
        print("\n💡 These leads suggest connections exist but require deeper search")

print(f"\n📁 Results saved to: {os.path.basename(results_file)}")
print(f"🔄 Ready for extended search or manual exploration of promising leads")
```

## Created Time
2025-08-13 23:20:03
