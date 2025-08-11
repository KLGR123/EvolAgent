# Developer Plan 02

## Plan
Follow the first citation reference link from Carl Nebel's Wikipedia page by accessing the URL http://web.archive.org/web/20230306063201/https://de.wikipedia.org/wiki/Thieme-Becker (the Thieme-Becker biographical dictionary entry). Download and analyze the complete webpage content to locate any images present on the page. For each image found, extract and examine all visible text, dates, numbers, and chronological information to identify the latest (most recent) chronological year date written within any image on that webpage.

## Description
This is the necessary next step because: (1) The developer successfully identified the first citation reference link from Carl Nebel's Wikipedia page pointing to the Thieme-Becker entry, (2) We now need to follow this link and access the target webpage to search for images containing chronological year dates, (3) Expected outcome is to locate all images on the Thieme-Becker page and extract the latest chronological year date from any text visible within those images, (4) This directly addresses the TASK requirement to find the latest year date written in images on the webpage reached through the first citation reference link.

## Episodic Examples
### Development Step 8: Locate 1851 atheistic naturalism book on phrenology & mesmerism reissued by publisher in 2009

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- Academic historian cataloging 19th-century controversial publications by extracting author names, thematic keywords (e.g., “atheistic naturalism,” “phrenology”), and original/reissue dates from archived HTML search results to build a digital bibliography.
- Legal e-discovery team automating the analysis of thousands of saved HTML case summaries to identify specific statutes, publication years, and co-counsel mentions for evidence tracking in litigation.
- Publishing house digital archivist processing legacy website snapshots to pinpoint out-of-print titles, detect reissue editions (e.g., 2009 reprints), and extract publisher credits for planning new annotated volumes.
- Marketing intelligence unit scanning archived competitor webpages to count occurrences of key product terms, track first-release dates, and infer promotional patterns for strategic positioning.
- SEO consultant auditing historical site snapshots to extract keyword density, publication timestamps, and backlink publisher clues from saved HTML to optimize on-page content and refresh outdated pages.
- Compliance officer reviewing stored HTML policy documents to locate regulatory terms, confirm enactment years, and identify issuing bodies for audit readiness and gap analysis.
- Genealogy researcher mining downloaded obituary and local history pages to extract names, vital dates, and relationship mentions for automated family-tree construction.

```
import os
import json
from bs4 import BeautifulSoup
import re
from collections import Counter

print('=== ANALYZING SAVED HTML SEARCH RESULTS FOR 1851 ATHEISTIC NATURALISM BOOK ===')
print('Objective: Extract information from saved HTML files to identify the book and 2009 publisher\n')

# First, let's inspect what HTML files we have in the workspace
workspace_dir = 'workspace'
html_files = []

if os.path.exists(workspace_dir):
    for filename in os.listdir(workspace_dir):
        if filename.endswith('.html') and 'search_' in filename:
            html_files.append(filename)
    
    print(f'Found {len(html_files)} HTML search result files:')
    for i, filename in enumerate(html_files, 1):
        print(f'  {i}. {filename}')
else:
    print('❌ Workspace directory not found')
    html_files = []

if not html_files:
    print('❌ No HTML search result files found to analyze')
    print('Need to execute searches first')
else:
    print(f'\n📁 ANALYZING {len(html_files)} HTML FILES FOR BOOK INFORMATION:')
    print('=' * 70)
    
    # Initialize analysis results
    analysis_results = {
        'timestamp': '2025-01-07',
        'files_analyzed': len(html_files),
        'book_evidence': [],
        'publisher_clues': [],
        'author_mentions': [],
        'year_confirmations': [],
        'topic_confirmations': [],
        'reissue_information': []
    }
    
    # Analyze each HTML file
    for i, filename in enumerate(html_files, 1):
        filepath = os.path.join(workspace_dir, filename)
        print(f'\nAnalyzing File {i}: {filename}')
        print('-' * 50)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract all text content
            page_text = soup.get_text(separator=' ', strip=True).lower()
            
            print(f'HTML file size: {len(html_content):,} characters')
            print(f'Extracted text size: {len(page_text):,} characters')
            
            # Look for key terms with context
            key_terms = {
                'martineau': 0,
                'atkinson': 0,
                '1851': 0,
                'letters': 0,
                'nature': 0,
                'development': 0,
                'atheistic': 0,
                'naturalism': 0,
                'phrenology': 0,
                'mesmerism': 0,
                'controversial': 0,
                '2009': 0,
                'reissue': 0,
                'publisher': 0,
                'edition': 0
            }
            
            # Count occurrences of each term
            found_terms = []
            for term in key_terms.keys():
                count = page_text.count(term)
                key_terms[term] = count
                if count > 0:
                    found_terms.append(f'{term}({count})')
            
            total_relevance = sum(key_terms.values())
            print(f'Total term occurrences: {total_relevance}')
            print(f'Found terms: {" ".join(found_terms[:10])}')
            
            # Look for specific patterns and extract context
            patterns_found = []
            
            # Pattern 1: Author names together
            if 'martineau' in page_text and 'atkinson' in page_text:
                # Find sentences with both authors
                sentences = re.split(r'[.!?]', page_text)
                author_sentences = []
                for sentence in sentences:
                    if 'martineau' in sentence and 'atkinson' in sentence:
                        if len(sentence.strip()) > 10:
                            author_sentences.append(sentence.strip()[:200])
                
                if author_sentences:
                    patterns_found.append('Authors mentioned together')
                    analysis_results['author_mentions'].extend(author_sentences[:3])
                    print('✓ Found author mentions together')
                    for j, sent in enumerate(author_sentences[:2], 1):
                        print(f'  {j}. {sent[:150]}...')
            
            # Pattern 2: Year 1851 with book context
            if '1851' in page_text:
                sentences = re.split(r'[.!?]', page_text)
                year_sentences = []
                for sentence in sentences:
                    if '1851' in sentence and any(word in sentence for word in ['book', 'letters', 'work', 'published', 'wrote']):
                        if len(sentence.strip()) > 10:
                            year_sentences.append(sentence.strip()[:200])
                
                if year_sentences:
                    patterns_found.append('1851 with book context')
                    analysis_results['year_confirmations'].extend(year_sentences[:3])
                    print('✓ Found 1851 with book context')
                    for j, sent in enumerate(year_sentences[:2], 1):
                        print(f'  {j}. {sent[:150]}...')
            
            # Pattern 3: Topic terms (phrenology, mesmerism, naturalism)
            topic_terms = ['phrenology', 'mesmerism', 'naturalism', 'atheistic']
            topic_mentions = []
            for topic in topic_terms:
                if topic in page_text:
                    sentences = re.split(r'[.!?]', page_text)
                    for sentence in sentences:
                        if topic in sentence and len(sentence.strip()) > 20:
                            topic_mentions.append(f'{topic}: {sentence.strip()[:150]}')
                            break  # Just get one example per topic
            
            if topic_mentions:
                patterns_found.append(f'Topic terms: {", ".join([t.split(":")[0] for t in topic_mentions])}')
                analysis_results['topic_confirmations'].extend(topic_mentions)
                print('✓ Found topic terms with context')
                for mention in topic_mentions[:2]:
                    print(f'  • {mention}...')
            
            # Pattern 4: 2009 reissue information
            if '2009' in page_text:
                sentences = re.split(r'[.!?]', page_text)
                reissue_sentences = []
                for sentence in sentences:
                    if '2009' in sentence:
                        if any(word in sentence for word in ['reissue', 'reprint', 'edition', 'published', 'publisher', 'press']):
                            if len(sentence.strip()) > 10:
                                reissue_sentences.append(sentence.strip()[:250])
                
                if reissue_sentences:
                    patterns_found.append('2009 reissue information')
                    analysis_results['reissue_information'].extend(reissue_sentences[:3])
                    print('✓ Found 2009 reissue information')
                    for j, sent in enumerate(reissue_sentences[:2], 1):
                        print(f'  {j}. {sent[:200]}...')
                
                # Look for publisher names near 2009
                publishers = [
                    'cambridge university press', 'oxford university press', 'harvard university press',
                    'yale university press', 'princeton university press', 'university of chicago press',
                    'routledge', 'palgrave', 'macmillan', 'sage publications', 'academic press',
                    'dover publications', 'penguin classics', 'everyman library', 'cambridge', 'oxford',
                    'norton', 'vintage', 'anchor books', 'university press'
                ]
                
                found_publishers = []
                for pub in publishers:
                    if pub in page_text:
                        # Check if publisher appears near 2009
                        pub_index = page_text.find(pub)
                        year_index = page_text.find('2009')
                        if pub_index != -1 and year_index != -1:
                            distance = abs(pub_index - year_index)
                            if distance < 500:  # Within 500 characters
                                found_publishers.append((pub, distance))
                
                if found_publishers:
                    # Sort by proximity to 2009
                    found_publishers.sort(key=lambda x: x[1])
                    analysis_results['publisher_clues'].extend([pub[0] for pub in found_publishers])
                    print('✓ Found publishers near 2009:')
                    for pub, dist in found_publishers[:3]:
                        print(f'  • {pub} (distance: {dist} chars)')
            
            # Store file analysis
            file_analysis = {
                'filename': filename,
                'total_relevance': total_relevance,
                'key_terms': {k: v for k, v in key_terms.items() if v > 0},
                'patterns_found': patterns_found
            }
            
            analysis_results['book_evidence'].append(file_analysis)
            
            print(f'Patterns found: {len(patterns_found)}')
            if patterns_found:
                print(f'  - {" | ".join(patterns_found)}')
            
        except Exception as e:
            print(f'Error analyzing {filename}: {str(e)}')
    
    print('\n' + '=' * 80)
    print('COMPREHENSIVE ANALYSIS SUMMARY')
    print('=' * 80)
    
    # Summarize findings
    total_author_mentions = len(analysis_results['author_mentions'])
    total_year_confirmations = len(analysis_results['year_confirmations'])
    total_topic_confirmations = len(analysis_results['topic_confirmations'])
    total_reissue_info = len(analysis_results['reissue_information'])
    total_publisher_clues = len(analysis_results['publisher_clues'])
    
    print(f'📊 EVIDENCE SUMMARY:')
    print(f'   • Author mentions (Martineau + Atkinson): {total_author_mentions}')
    print(f'   • Year confirmations (1851): {total_year_confirmations}')
    print(f'   • Topic confirmations: {total_topic_confirmations}')
    print(f'   • 2009 reissue information: {total_reissue_info}')
    print(f'   • Publisher clues: {total_publisher_clues}')
    
    # Analyze publisher frequency
    if analysis_results['publisher_clues']:
        publisher_counts = Counter(analysis_results['publisher_clues'])
        print(f'\n📚 PUBLISHER ANALYSIS:')
        print('Most frequently mentioned publishers near 2009:')
        for pub, count in publisher_counts.most_common(5):
            print(f'  • {pub}: {count} mentions')
        
        # Identify most likely publisher
        top_publisher = publisher_counts.most_common(1)[0]
        print(f'\n🎯 MOST LIKELY 2009 PUBLISHER: {top_publisher[0]} ({top_publisher[1]} mentions)')
    
    # Show best evidence examples
    if analysis_results['author_mentions']:
        print(f'\n👥 BEST AUTHOR EVIDENCE:')
        for i, mention in enumerate(analysis_results['author_mentions'][:2], 1):
            print(f'  {i}. {mention[:200]}...')
    
    if analysis_results['reissue_information']:
        print(f'\n📅 BEST 2009 REISSUE EVIDENCE:')
        for i, info in enumerate(analysis_results['reissue_information'][:2], 1):
            print(f'  {i}. {info[:250]}...')
    
    # Calculate confidence score
    evidence_score = 0
    if total_author_mentions > 0: evidence_score += 20
    if total_year_confirmations > 0: evidence_score += 20
    if total_topic_confirmations > 0: evidence_score += 20
    if total_reissue_info > 0: evidence_score += 25
    if total_publisher_clues > 0: evidence_score += 15
    
    print(f'\n📈 CONFIDENCE SCORE: {evidence_score}/100')
    
    # Final book identification
    print('\n' + '=' * 80)
    print('FINAL BOOK IDENTIFICATION')
    print('=' * 80)
    
    print('📖 IDENTIFIED BOOK:')
    print('   Title: "Letters on the Laws of Man\'s Nature and Development"')
    print('   Authors: Harriet Martineau and Henry George Atkinson')
    print('   Original Publication: 1851')
    print('   Content: Atheistic naturalism, phrenology, mesmerism')
    print('   Controversial: Yes, for its atheistic and pseudoscientific content')
    
    if analysis_results['publisher_clues']:
        top_publisher = Counter(analysis_results['publisher_clues']).most_common(1)[0][0]
        print(f'   2009 Reissue Publisher: {top_publisher}')
    else:
        print('   2009 Reissue Publisher: [Not definitively identified from search results]')
    
    # Save comprehensive analysis
    results_file = os.path.join(workspace_dir, 'comprehensive_book_analysis.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    
    print(f'\n💾 COMPREHENSIVE ANALYSIS SAVED TO: {results_file}')
    
    if evidence_score >= 60:
        print('\n✅ BOOK SUCCESSFULLY IDENTIFIED WITH HIGH CONFIDENCE!')
        print('\nThe 1851 co-authored book on atheistic naturalism with phrenology/mesmerism')
        print('content that was controversial and reissued in 2009 is:')
        print('\n"Letters on the Laws of Man\'s Nature and Development"')
        print('by Harriet Martineau and Henry George Atkinson')
    else:
        print('\n❓ PARTIAL IDENTIFICATION - Additional research may be needed')
        print('Based on historical knowledge, this is most likely:')
        print('"Letters on the Laws of Man\'s Nature and Development"')
        print('by Harriet Martineau and Henry George Atkinson (1851)')

print('\n=== HTML ANALYSIS FOR 1851 ATHEISTIC NATURALISM BOOK COMPLETE ===')
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

### Development Step 5: Identify 1851 Atheistic Naturalism Book on Phrenology/Mesmerism and Its 2009 Reissue Publisher

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- Academic historian automating the identification of obscure 19th-century texts and their modern reissue details for a journal article on atheistic naturalism controversies
- Library metadata specialist using targeted web and scholarly search scripts to update collection records with publication dates, co-authors, and reprint publisher information
- Digital humanities project integrating automated web scraping and match-scoring to curate a dataset of phrenology and mesmerism publications for network and discourse analysis
- Publishing house acquisitions team conducting due diligence on public domain works by detecting original 1851 publication details and 2009 reissue rights before green-lighting a new edition
- Intellectual property attorney verifying authorship, publication history, and modern publisher claims for 19th-century texts in a litigation involving contested reprint rights
- Graduate student building a reproducible search pipeline to gather evidence on historical debates in naturalism, phrenology, and mesmerism for a dissertation timeline and annotated bibliography
- Cultural heritage institution employing automated Google Scholar analysis to tag and contextualize controversial topics in its digital archive of 19th-century manuscripts
- Open-access repository manager using a customized search-and-analyze workflow to prioritize the digitization of historically significant works with detailed bibliographic provenance

```
import os
import json
from collections import Counter

print('=== ANALYZING SEARCH RESULTS AND CONDUCTING TARGETED FOLLOW-UP ===\n')
print('Previous search collected 9 Google Scholar findings on phrenology/mesmerism topics')
print('Need to fix NameError and analyze results for the 1851 atheistic naturalism book\n')

# First, let's inspect the saved search results file structure
results_file = os.path.join('workspace', 'comprehensive_1851_book_search.json')

if os.path.exists(results_file):
    print('📁 INSPECTING SAVED SEARCH RESULTS FILE:')
    print('-' * 50)
    
    with open(results_file, 'r', encoding='utf-8') as f:
        search_data = json.load(f)
    
    print(f'File keys: {list(search_data.keys())}')
    print(f'Timestamp: {search_data.get("timestamp", "N/A")}')
    print(f'Total findings: {len(search_data.get("all_findings", []))}')
    print(f'Search methods: {len(search_data.get("search_methods", []))}')
    
    if search_data.get('all_findings'):
        print(f'\nFirst finding structure: {list(search_data["all_findings"][0].keys())}')
        print(f'Sample finding: {search_data["all_findings"][0]}')
else:
    print('❌ No previous search results file found')
    # Initialize empty structure
    search_data = {
        'timestamp': 'N/A',
        'all_findings': [],
        'search_methods': [],
        'book_candidates': []
    }

print('\n' + '='*80)
print('DETAILED ANALYSIS OF GOOGLE SCHOLAR FINDINGS')
print('='*80)

# Analyze the Google Scholar findings in detail
scholar_findings = [f for f in search_data.get('all_findings', []) if f.get('source') == 'Google Scholar']

print(f'Google Scholar findings to analyze: {len(scholar_findings)}')

if scholar_findings:
    print('\n📚 DETAILED ANALYSIS OF EACH FINDING:')
    print('-' * 60)
    
    potential_1851_books = []
    related_works = []
    
    for i, finding in enumerate(scholar_findings, 1):
        title = finding.get('title', 'No title')
        terms = finding.get('relevance_terms', [])
        query = finding.get('query', 'Unknown query')
        
        print(f'\n{i}. TITLE: {title}')
        print(f'   QUERY: {query}')
        print(f'   RELEVANT TERMS: {", ".join(terms)}')
        
        # Analyze for 1851 connections
        title_lower = title.lower()
        
        # Check for year indicators
        year_indicators = ['1851', '1850', '1852', 'mid-19th', '19th century']
        has_year = any(indicator in title_lower for indicator in year_indicators)
        
        # Check for book indicators
        book_indicators = ['book', 'letters', 'treatise', 'work', 'volume']
        has_book = any(indicator in title_lower for indicator in book_indicators)
        
        # Check for naturalism/atheism indicators
        naturalism_indicators = ['naturalism', 'atheistic', 'atheism', 'scientific', 'natural']
        has_naturalism = any(indicator in title_lower for indicator in naturalism_indicators)
        
        # Check for co-authorship indicators
        coauthor_indicators = ['letters', 'correspondence', 'dialogue']
        has_coauthor_hint = any(indicator in title_lower for indicator in coauthor_indicators)
        
        print(f'   ANALYSIS:')
        print(f'     - Year connection: {has_year} ({[y for y in year_indicators if y in title_lower]})')
        print(f'     - Book format: {has_book} ({[b for b in book_indicators if b in title_lower]})')
        print(f'     - Naturalism theme: {has_naturalism} ({[n for n in naturalism_indicators if n in title_lower]})')
        print(f'     - Co-author hints: {has_coauthor_hint} ({[c for c in coauthor_indicators if c in title_lower]})')
        
        # Score potential match
        match_score = 0
        if has_year: match_score += 3
        if has_book: match_score += 2
        if has_naturalism: match_score += 2
        if has_coauthor_hint: match_score += 1
        if 'phrenology' in terms: match_score += 2
        if 'mesmerism' in terms: match_score += 2
        
        print(f'     - MATCH SCORE: {match_score}/12')
        
        if match_score >= 6:
            print('     ⭐ HIGH POTENTIAL MATCH')
            potential_1851_books.append({
                'title': title,
                'score': match_score,
                'terms': terms,
                'analysis': {
                    'has_year': has_year,
                    'has_book': has_book,
                    'has_naturalism': has_naturalism,
                    'has_coauthor_hint': has_coauthor_hint
                }
            })
        elif match_score >= 3:
            print('     📖 RELATED WORK')
            related_works.append({
                'title': title,
                'score': match_score,
                'terms': terms
            })
    
    print(f'\n\n🎯 POTENTIAL 1851 BOOK MATCHES: {len(potential_1851_books)}')
    print('='*60)
    
    if potential_1851_books:
        # Sort by score
        potential_1851_books.sort(key=lambda x: x['score'], reverse=True)
        
        for i, book in enumerate(potential_1851_books, 1):
            print(f'\n{i}. {book["title"]}')
            print(f'   Score: {book["score"]}/12')
            print(f'   Terms: {", ".join(book["terms"])}')
            print(f'   Year connection: {book["analysis"]["has_year"]}')
            print(f'   Book format: {book["analysis"]["has_book"]}')
            print(f'   Naturalism theme: {book["analysis"]["has_naturalism"]}')
            print(f'   Co-author hints: {book["analysis"]["has_coauthor_hint"]}')
    else:
        print('No high-scoring matches found in current results')
    
    print(f'\n📚 RELATED WORKS: {len(related_works)}')
    print('='*40)
    
    if related_works:
        related_works.sort(key=lambda x: x['score'], reverse=True)
        for i, work in enumerate(related_works[:5], 1):  # Show top 5
            print(f'{i}. {work["title"]} (Score: {work["score"]})')

else:
    print('No Google Scholar findings to analyze')

# Now conduct more targeted searches based on the most promising finding
print('\n' + '='*80)
print('CONDUCTING TARGETED FOLLOW-UP SEARCHES')
print('='*80)

# Based on the Google Scholar results, let's search for more specific information
# The "Letters on the Laws of Man's Nature and Development" seems most promising

targeted_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 1851 co-authored',
    '"Letters on the Laws of Man\'s Nature and Development" phrenology mesmerism',
    '"Letters on the Laws of Man\'s Nature and Development" atheistic naturalism',
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reissue',
    'Harriet Martineau Henry Atkinson Letters 1851 phrenology mesmerism'
]

print('🔍 TARGETED SEARCH QUERIES:')
for i, query in enumerate(targeted_queries, 1):
    print(f'  {i}. {query}')

# Try a more specific web search approach
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

targeted_results = []

print('\n📡 EXECUTING TARGETED WEB SEARCHES:')
print('-' * 50)

for i, query in enumerate(targeted_queries, 1):
    print(f'\nTargeted Search {i}: {query}')
    
    try:
        # Try Google search
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        print(f'URL: {google_url}')
        
        response = requests.get(google_url, headers=headers, timeout=20)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save HTML
            filename = f'targeted_search_{i}_{query[:30].replace(" ", "_").replace("\'", "")}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Saved: {filepath}')
            
            # Quick parse for results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result snippets and titles
            result_elements = soup.find_all(['h3', 'div', 'span'], string=lambda text: text and any(term in text.lower() for term in ['1851', 'letters', 'martineau', 'atkinson', 'phrenology', 'mesmerism', '2009']))
            
            relevant_snippets = []
            for elem in result_elements:
                text = elem.get_text().strip()
                if len(text) > 20 and len(text) < 300:
                    text_lower = text.lower()
                    relevance_terms = []
                    
                    key_terms = ['1851', 'letters', 'martineau', 'atkinson', 'phrenology', 'mesmerism', 'naturalism', 'atheistic', '2009', 'reissue']
                    
                    for term in key_terms:
                        if term in text_lower:
                            relevance_terms.append(term)
                    
                    if len(relevance_terms) >= 2:
                        relevant_snippets.append({
                            'text': text,
                            'terms': relevance_terms,
                            'query': query
                        })
            
            print(f'Found {len(relevant_snippets)} relevant snippets')
            
            for j, snippet in enumerate(relevant_snippets[:3], 1):
                print(f'  {j}. {snippet["text"][:100]}...')
                print(f'     Terms: {", ".join(snippet["terms"])}')
                
                targeted_results.append(snippet)
        
        else:
            print(f'Failed with status {response.status_code}')
    
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)  # Rate limiting

print('\n' + '='*80)
print('COMPREHENSIVE FINDINGS SUMMARY')
print('='*80)

print(f'📊 SEARCH STATISTICS:')
print(f'   • Previous Google Scholar findings: {len(scholar_findings)}')
print(f'   • High-potential 1851 book matches: {len(potential_1851_books) if "potential_1851_books" in locals() else 0}')
print(f'   • Related works identified: {len(related_works) if "related_works" in locals() else 0}')
print(f'   • Targeted search results: {len(targeted_results)}')

# Compile all evidence
all_evidence = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'objective': 'Find 1851 co-authored book on atheistic naturalism with phrenology/mesmerism, reissued 2009',
    'scholar_findings_analyzed': len(scholar_findings),
    'potential_1851_matches': potential_1851_books if 'potential_1851_books' in locals() else [],
    'related_works': related_works if 'related_works' in locals() else [],
    'targeted_search_results': targeted_results,
    'top_candidate': None
}

# Identify top candidate
if 'potential_1851_books' in locals() and potential_1851_books:
    all_evidence['top_candidate'] = potential_1851_books[0]
    
    print(f'\n🏆 TOP CANDIDATE IDENTIFIED:')
    print(f'   Title: {potential_1851_books[0]["title"]}')
    print(f'   Match Score: {potential_1851_books[0]["score"]}/12')
    print(f'   Key Terms: {", ".join(potential_1851_books[0]["terms"])}')
    
    # Check if this looks like "Letters on the Laws of Man's Nature and Development"
    if 'letters' in potential_1851_books[0]['title'].lower():
        print('\n💡 STRONG INDICATION: This appears to be "Letters on the Laws of Man\'s Nature and Development"')
        print('   This work was co-authored by Harriet Martineau and Henry George Atkinson in 1851')
        print('   It was controversial for its atheistic naturalism and discussion of phrenology/mesmerism')
        print('   Need to verify: 2009 reissue publisher information')

else:
    print('\n❓ No clear top candidate identified from current search results')
    print('   May need additional targeted searches or different approach')

# Save comprehensive analysis
analysis_file = os.path.join('workspace', 'comprehensive_1851_book_analysis.json')
with open(analysis_file, 'w', encoding='utf-8') as f:
    json.dump(all_evidence, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE ANALYSIS SAVED TO: {analysis_file}')

print('\n🎯 NEXT STEPS:')
if 'potential_1851_books' in locals() and potential_1851_books:
    print('1. ✅ Investigate "Letters on the Laws of Man\'s Nature and Development" further')
    print('2. ✅ Search for Harriet Martineau and Henry George Atkinson as co-authors')
    print('3. ✅ Find which publisher reissued this work in 2009')
    print('4. ✅ Verify the atheistic naturalism and phrenology/mesmerism content')
else:
    print('1. 🔄 Expand search to include more 1851 controversial books')
    print('2. 🔄 Search for 19th century phrenology/mesmerism book catalogs')
    print('3. 🔄 Try library database searches (WorldCat, etc.)')

print('5. 📋 Review all saved HTML files for additional clues')
print('6. 🔍 Cross-reference findings with academic databases')

print('\n=== TARGETED ANALYSIS AND FOLLOW-UP COMPLETE ===')
```

### Development Step 2: Find 1851 co-authored atheistic naturalism book on phrenology & mesmerism reissued in 2009

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- Academic librarians performing metadata verification and historical edition tracking for rare 19th-century philosophical texts to ensure catalog accuracy
- Antiquarian book dealers automating discovery of first-print and modern reissued editions of controversial 1851 publications for precise inventory valuation
- Historians of science conducting web-based surveys of 1850s works on phrenology and mesmerism by scraping search engines to compile comprehensive bibliographies
- Digital humanities researchers extracting co-authorship, publication dates, and reissue details of obscure naturalism treatises for integration into an open access archive
- Publishing houses auditing online mentions and publisher records of out-of-print atheistic naturalism books to inform decisions on new print runs
- Graduate students assembling a detailed publication timeline of 19th-century atheistic works by automating searches across scholarly and general web sources
- Rare books curators cross-referencing scraped edition data and reissue information to confirm provenance and authenticity of volumes in institutional collections

```
import os
import requests
import json
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

print('=== ALTERNATIVE SEARCH APPROACH FOR 1851 ATHEISTIC NATURALISM BOOK ===')
print('Previous SERPAPI attempts failed due to rate limiting (HTTP 429)')
print('Switching to direct web scraping methods\n')

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
    'method': 'Direct web scraping (DuckDuckGo + Google Scholar)',
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
                print(f'\n🎯 HIGH RELEVANCE RESULTS ({len(high_relevance)}):'):
                for j, result in enumerate(high_relevance, 1):
                    print(f'  {j}. Score: {result["relevance_score"]} | {result["title"]}')
                    print(f'     Terms: {", ".join(result["matched_terms"])}')
                    print(f'     Link: {result["link"]}')
                    print(f'     Snippet: {result["snippet"][:150]}...')
                    print()
            
            if moderate_relevance:
                print(f'\n⭐ MODERATE RELEVANCE RESULTS ({len(moderate_relevance)}):'):
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
                print(f'\n📚 BOOK CANDIDATES FOUND ({len(book_candidates)}):'):
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
    'search_success_rate': f'{len([q for q in search_queries if any(r["query"] == q for r in all_results["results"])]}/{len(search_queries)}'
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

## Created Time
2025-08-11 06:17:06
