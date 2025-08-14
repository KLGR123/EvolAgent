# Developer Plan #1 - anthropic.claude-sonnet-4-20250514-v1:0

**Task ID:** webshaper_37  
**Model:** anthropic.claude-sonnet-4-20250514-v1:0  
**Plan Index:** 1  
**Timestamp:** 2025-08-09 14:17:45

## Plan Content
```
Conduct a comprehensive web search to identify a historical book series that includes both: (1) analysis of the political transition between the Bourbon Restoration and the July Monarchy in France, and (2) analysis of Gaul's history under Celtic, Roman, and Frankish rule. Focus on finding series that feature volumes authored by Frantz Funck-Brentano, a French historian. Search using keywords including 'Frantz Funck-Brentano historical series', 'Bourbon Restoration July Monarchy transition', 'Gaul Celtic Roman Frankish history series', and 'French historical book series political transition'. Identify the specific series name and locate the volume dealing with the Bourbon Restoration to July Monarchy transition to determine its publication year.
```

## Plan Description
```
This is the optimal starting approach because: (1) We need to identify a specific historical book series with very particular characteristics involving French political transitions and ancient Gaul history, (2) No previous research has been conducted, (3) Expected outcome is to find the series name and the specific volume's publication year, (4) This directly targets the unique combination of historical periods, author involvement, and publication information needed to answer the TASK
```

## Retrieved Episodic Memory Examples
### Development Step 9: Identify 1851 Co-Authored Atheistic Naturalism Book on Phrenology and Mesmerism Reissued in 2009

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- Rare book dealers verifying the provenance and reprint history of a mid-19th-century scientific treatise to accurately price and catalog high-value auction listings
- University library digitization teams automating the extraction of publication metadata and 2009 reissue details for public domain texts in their digital collections
- Academic researchers mapping the dissemination of pseudoscientific ideas (phrenology and mesmerism) in 1851 publications for a peer-reviewed history of science journal article
- Legal research departments cross-checking original publication dates and subsequent reprints to build evidence for copyright and public domain status in intellectual property cases
- Archivists in cultural heritage institutions compiling correspondence-based works and publisher reissue records to prioritize preservation efforts and secure conservation funding
- Educational publishers creating annotated critical editions of Victorian naturalism texts by programmatically validating author attributions, controversial topics, and modern reissue publishers
- Genealogical historians tracing ancestral contributions to social science debates by systematically identifying co-authored 19th-century publications and their 2009 republications

```
import os
import requests
import json
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from collections import Counter
import re

print('=== COMPREHENSIVE SEARCH FOR 1851 CO-AUTHORED ATHEISTIC NATURALISM BOOK ===')
print('Objective: Find co-authored 1851 book advocating atheistic naturalism with phrenology/mesmerism, reissued 2009\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Based on historical knowledge and previous analysis, the target book is:
# "Letters on the Laws of Man's Nature and Development" by Harriet Martineau and Henry George Atkinson (1851)
print('TARGET BOOK CHARACTERISTICS:')
print('• Published: 1851')
print('• Co-authored by multiple authors')
print('• Topic: Atheistic naturalism')
print('• Contains: Phrenology and mesmerism content')
print('• Controversial for these topics')
print('• Reissued by a publisher in 2009')
print()

# Initialize comprehensive search results
search_results = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'objective': 'Find 1851 co-authored book on atheistic naturalism with phrenology/mesmerism, reissued 2009',
    'target_identification': {
        'title': 'Letters on the Laws of Man\'s Nature and Development',
        'authors': ['Harriet Martineau', 'Henry George Atkinson'],
        'year': 1851,
        'topics': ['atheistic naturalism', 'phrenology', 'mesmerism'],
        'controversial': True
    },
    'search_methods': [],
    'findings': [],
    'publisher_analysis': {},
    'final_conclusion': {}
}

# Headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive'
}

print('=== PHASE 1: TARGETED SEARCHES FOR BOOK IDENTIFICATION ===') 
print('=' * 70)

# Comprehensive search queries targeting the specific book
targeted_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" Martineau Atkinson 1851',
    'Harriet Martineau Henry Atkinson Letters 1851 atheistic naturalism controversial',
    '"Laws of Man\'s Nature Development" phrenology mesmerism 1851 co-authored',
    'Martineau Atkinson 1851 Letters atheism naturalism phrenology mesmerism',
    '"Letters Laws Man Nature Development" 2009 reissue publisher edition reprint'
]

print(f'Executing {len(targeted_queries)} comprehensive searches:')
for i, query in enumerate(targeted_queries, 1):
    print(f'  {i}. {query}')

# Execute searches and collect results
for i, query in enumerate(targeted_queries, 1):
    print(f'\nSearch {i}/{len(targeted_queries)}: {query}')
    print('-' * 60)
    
    try:
        # Google search
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        print(f'URL: {google_url}')
        
        response = requests.get(google_url, headers=headers, timeout=20)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save HTML
            filename = f'comprehensive_search_{i}_{query[:40].replace(" ", "_").replace("\'", "").replace('"', "")}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Saved: {filepath}')
            
            # Parse and analyze content
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text(separator=' ', strip=True).lower()
            
            # Define key terms with weights for relevance scoring
            key_terms = {
                'martineau': 5,
                'atkinson': 5, 
                '1851': 6,
                'letters': 4,
                'nature': 2,
                'development': 3,
                'atheistic': 5,
                'naturalism': 5,
                'phrenology': 5,
                'mesmerism': 5,
                'controversial': 4,
                '2009': 6,
                'reissue': 5,
                'reprint': 4,
                'publisher': 4,
                'edition': 3
            }
            
            # Calculate relevance and find terms
            found_terms = []
            relevance_score = 0
            term_counts = {}
            
            for term, weight in key_terms.items():
                count = page_text.count(term)
                if count > 0:
                    found_terms.append(f'{term}({count})')
                    relevance_score += weight * count
                    term_counts[term] = count
            
            print(f'Relevance score: {relevance_score}')
            print(f'Found terms: {" ".join(found_terms[:10])}')
            
            # Extract meaningful text snippets
            meaningful_snippets = []
            
            # Look for sentences containing key combinations
            sentences = re.split(r'[.!?]', page_text)
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20 and len(sentence) < 300:
                    # Check for author combinations
                    if 'martineau' in sentence and 'atkinson' in sentence:
                        meaningful_snippets.append(('authors', sentence))
                    # Check for year + book context
                    elif '1851' in sentence and any(word in sentence for word in ['letters', 'book', 'work', 'published']):
                        meaningful_snippets.append(('year_book', sentence))
                    # Check for topic combinations
                    elif any(topic in sentence for topic in ['phrenology', 'mesmerism', 'naturalism']) and any(word in sentence for word in ['controversial', 'atheistic', 'scientific']):
                        meaningful_snippets.append(('topics', sentence))
                    # Check for 2009 reissue info
                    elif '2009' in sentence and any(word in sentence for word in ['reissue', 'reprint', 'edition', 'publisher']):
                        meaningful_snippets.append(('reissue', sentence))
            
            # Look for publisher information specifically
            publishers_found = []
            if '2009' in page_text:
                print('✓ Found 2009 - scanning for publishers...')
                
                # Academic and commercial publishers
                publisher_list = [
                    'cambridge university press', 'oxford university press', 'harvard university press',
                    'yale university press', 'princeton university press', 'university of chicago press',
                    'routledge', 'palgrave macmillan', 'sage publications', 'academic press',
                    'dover publications', 'penguin classics', 'everyman library', 'vintage books',
                    'anchor books', 'norton', 'university press', 'scholarly press',
                    'cambridge', 'oxford', 'harvard', 'yale', 'princeton'
                ]
                
                for pub in publisher_list:
                    if pub in page_text:
                        # Check proximity to 2009
                        pub_positions = [m.start() for m in re.finditer(pub, page_text)]
                        year_positions = [m.start() for m in re.finditer('2009', page_text)]
                        
                        for pub_pos in pub_positions:
                            for year_pos in year_positions:
                                distance = abs(pub_pos - year_pos)
                                if distance < 1000:  # Within 1000 characters
                                    publishers_found.append((pub, distance))
                                    print(f'  • {pub} (distance from 2009: {distance} chars)')
                                    break
            
            # Store comprehensive finding
            finding = {
                'query': query,
                'relevance_score': relevance_score,
                'term_counts': term_counts,
                'found_terms': found_terms,
                'meaningful_snippets': meaningful_snippets[:5],  # Top 5 snippets
                'publishers_near_2009': publishers_found,
                'html_file': filepath,
                'has_2009': '2009' in page_text,
                'has_authors': 'martineau' in page_text and 'atkinson' in page_text,
                'has_year': '1851' in page_text,
                'has_topics': any(topic in page_text for topic in ['phrenology', 'mesmerism', 'naturalism'])
            }
            
            search_results['findings'].append(finding)
            search_results['search_methods'].append(f'Google search: {query} - Status {response.status_code}')
            
            # Display key findings
            if relevance_score >= 20:
                print('🎯 HIGH RELEVANCE RESULT')
                if meaningful_snippets:
                    print('Key snippets found:')
                    for snippet_type, snippet in meaningful_snippets[:3]:
                        print(f'  [{snippet_type}] {snippet[:150]}...')
            
        else:
            print(f'Failed with status {response.status_code}')
            
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)  # Rate limiting

# PHASE 2: Specific 2009 reissue publisher search
print('\n=== PHASE 2: FOCUSED 2009 REISSUE PUBLISHER SEARCH ===')
print('=' * 60)

reissue_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reprint publisher',
    'Martineau Atkinson Letters 1851 2009 edition reissued publisher',
    '"Laws of Man\'s Nature Development" 2009 reprint edition publisher',
    'atheistic naturalism 1851 book 2009 reissue Martineau Atkinson publisher'
]

for i, query in enumerate(reissue_queries, 1):
    print(f'\nReissue Search {i}: {query}')
    
    try:
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        response = requests.get(google_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            filename = f'reissue_search_{i}_{query[:35].replace(" ", "_").replace("\'", "").replace('"', "")}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Status: {response.status_code} | Saved: {filename}')
            
            # Quick analysis for publisher + 2009 combinations
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            if '2009' in page_text:
                # Extract sentences containing 2009
                sentences_2009 = []
                for sentence in re.split(r'[.!?]', page_text):
                    if '2009' in sentence and len(sentence.strip()) > 15:
                        sentences_2009.append(sentence.strip()[:200])
                
                if sentences_2009:
                    print(f'  ✓ Found {len(sentences_2009)} sentences with 2009')
                    for j, sent in enumerate(sentences_2009[:2], 1):
                        print(f'    {j}. {sent[:120]}...')
                    
                    # Store reissue information
                    search_results['findings'].append({
                        'query': query,
                        'type': 'reissue_focused',
                        'sentences_2009': sentences_2009[:5],
                        'html_file': filepath
                    })
        
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)

# PHASE 3: Comprehensive analysis of all findings
print('\n' + '=' * 80)
print('COMPREHENSIVE ANALYSIS OF ALL SEARCH RESULTS')
print('=' * 80)

total_findings = len(search_results['findings'])
print(f'Total search results collected: {total_findings}')

if search_results['findings']:
    # Analyze by relevance
    high_relevance = [f for f in search_results['findings'] if f.get('relevance_score', 0) >= 20]
    moderate_relevance = [f for f in search_results['findings'] if 5 <= f.get('relevance_score', 0) < 20]
    reissue_focused = [f for f in search_results['findings'] if f.get('type') == 'reissue_focused']
    
    print(f'\n📊 FINDINGS BREAKDOWN:')
    print(f'   • High relevance (20+ score): {len(high_relevance)}')
    print(f'   • Moderate relevance (5-19 score): {len(moderate_relevance)}')
    print(f'   • Reissue-focused results: {len(reissue_focused)}')
    
    # Compile all publisher information
    all_publishers = []
    for finding in search_results['findings']:
        if finding.get('publishers_near_2009'):
            for pub, distance in finding['publishers_near_2009']:
                all_publishers.append(pub)
    
    # Analyze publisher frequency
    if all_publishers:
        publisher_counts = Counter(all_publishers)
        search_results['publisher_analysis'] = {
            'total_mentions': len(all_publishers),
            'unique_publishers': len(set(all_publishers)),
            'frequency_ranking': dict(publisher_counts.most_common())
        }
        
        print(f'\n📚 PUBLISHER ANALYSIS:')
        print(f'   • Total publisher mentions near 2009: {len(all_publishers)}')
        print(f'   • Unique publishers found: {len(set(all_publishers))}')
        
        if publisher_counts:
            print('   • Top publishers by frequency:')
            for pub, count in publisher_counts.most_common(5):
                print(f'     - {pub}: {count} mentions')
            
            top_publisher = publisher_counts.most_common(1)[0]
            search_results['publisher_analysis']['most_likely_2009_publisher'] = top_publisher[0]
            print(f'\n🎯 MOST LIKELY 2009 PUBLISHER: {top_publisher[0]} ({top_publisher[1]} mentions)')
    
    # Evidence compilation
    evidence_summary = {
        'book_title_evidence': sum(1 for f in search_results['findings'] if 'letters' in str(f.get('term_counts', {})).lower()),
        'authors_evidence': sum(1 for f in search_results['findings'] if f.get('has_authors', False)),
        'year_evidence': sum(1 for f in search_results['findings'] if f.get('has_year', False)),
        'topics_evidence': sum(1 for f in search_results['findings'] if f.get('has_topics', False)),
        'reissue_evidence': sum(1 for f in search_results['findings'] if f.get('has_2009', False))
    }
    
    print(f'\n🔍 EVIDENCE SUMMARY:')
    for evidence_type, count in evidence_summary.items():
        status = '✅' if count > 0 else '❌'
        print(f'   {status} {evidence_type.replace("_", " ").title()}: {count} findings')
    
    search_results['final_conclusion']['evidence_summary'] = evidence_summary
    
    # Calculate overall confidence
    total_evidence = sum(evidence_summary.values())
    max_possible = len(evidence_summary) * total_findings
    confidence_percentage = (total_evidence / max_possible * 100) if max_possible > 0 else 0
    
    print(f'\n📈 OVERALL CONFIDENCE: {confidence_percentage:.1f}%')
    search_results['final_conclusion']['confidence_percentage'] = confidence_percentage

# Final book identification and conclusion
print('\n' + '=' * 80)
print('FINAL BOOK IDENTIFICATION AND CONCLUSION')
print('=' * 80)

print('📖 IDENTIFIED BOOK:')
print('   Title: "Letters on the Laws of Man\'s Nature and Development"')
print('   Authors: Harriet Martineau and Henry George Atkinson')
print('   Original Publication: 1851')
print('   Content: Advocated atheistic naturalism, systematically explored phrenology and mesmerism')
print('   Controversial: Yes, for its atheistic views and pseudoscientific content')
print('   Co-authored: Yes, correspondence between Martineau and Atkinson')

if search_results.get('publisher_analysis', {}).get('most_likely_2009_publisher'):
    publisher = search_results['publisher_analysis']['most_likely_2009_publisher']
    print(f'   2009 Reissue Publisher: {publisher}')
else:
    print('   2009 Reissue Publisher: [To be determined from search results analysis]')

# Save comprehensive results
results_file = os.path.join('workspace', 'comprehensive_1851_atheistic_naturalism_book_search.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE SEARCH RESULTS SAVED TO: {results_file}')

# Final summary
print('\n📊 SEARCH COMPLETION SUMMARY:')
print(f'   • Total queries executed: {len(search_results["search_methods"])}')
print(f'   • HTML files saved: {len([f for f in search_results["findings"] if f.get("html_file")])}')
print(f'   • High-relevance findings: {len([f for f in search_results["findings"] if f.get("relevance_score", 0) >= 20])}')
print(f'   • Publisher clues collected: {len(all_publishers) if "all_publishers" in locals() else 0}')

if search_results.get('final_conclusion', {}).get('confidence_percentage', 0) >= 50:
    print('\n✅ BOOK SUCCESSFULLY IDENTIFIED WITH HIGH CONFIDENCE!')
    print('\n🎯 FINAL ANSWER:')
    print('The 1851 co-authored book that advocated atheistic naturalism,')
    print('systematically explored phrenology and mesmerism, was controversial')
    print('for these topics, and was reissued in 2009 is:')
    print('\n"Letters on the Laws of Man\'s Nature and Development"')
    print('by Harriet Martineau and Henry George Atkinson')
else:
    print('\n📋 BOOK IDENTIFIED BASED ON HISTORICAL KNOWLEDGE:')
    print('"Letters on the Laws of Man\'s Nature and Development"')
    print('by Harriet Martineau and Henry George Atkinson (1851)')
    print('\n[2009 publisher information may require additional verification]')

print('\n=== COMPREHENSIVE SEARCH FOR 1851 ATHEISTIC NATURALISM BOOK COMPLETE ===')
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

### Development Step 6: Identify 1851 Co-Authored Atheistic Naturalism Phrenology Mesmerism Book and 2009 Reissue Publisher

**Description**: Conduct a comprehensive web search to identify a co-authored book from 1851 that advocated for atheistic naturalism, systematically explored phrenology and mesmerism, was controversial for these topics, and was reissued by a publisher in 2009. Search using keywords including '1851 book atheistic naturalism phrenology mesmerism co-authored', '1851 controversial book phrenology mesmerism reissued 2009', 'atheistic naturalism 1851 publication', and 'phrenology mesmerism 1851 authors'. Focus on identifying both the original 1851 publication details and the specific publisher who reissued it in 2009.

**Use Cases**:
- Historical bibliography verification and metadata extraction for librarians cataloging rare 19th-century publications
- Academic literature discovery and relevance scoring for researchers compiling annotated bibliographies on atheism and pseudoscience
- Publisher reissue tracking and competitive analysis for publishing houses evaluating potential 2009 reprint opportunities
- Intellectual property prior-art identification and automated search for patent attorneys verifying historical references in phrenology and mesmerism
- Content monitoring and automated discovery of controversial publications for human rights NGOs tracking censorship trends
- Market intelligence gathering and trend analysis of historical book reissues for online book retailers optimizing inventory and promotions
- Educational resource curation and syllabus development for university professors selecting primary sources on Victorian naturalism
- Digital humanities research automation integrating web scraping and text analysis of 19th-century works for cultural studies projects

```
import os
import requests
import json
import time
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

print('=== COMPREHENSIVE SEARCH FOR 1851 ATHEISTIC NATURALISM BOOK ===')
print('Objective: Find co-authored 1851 book on atheistic naturalism with phrenology/mesmerism, reissued 2009\n')

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

# Headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

# Method 1: Targeted searches for the most likely candidate
print('=== METHOD 1: TARGETED SEARCHES FOR "LETTERS ON THE LAWS OF MAN\'S NATURE" ===')
print('=' * 80)

# Based on historical knowledge, this is likely "Letters on the Laws of Man's Nature and Development"
# by Harriet Martineau and Henry George Atkinson (1851)
targeted_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 1851 Martineau Atkinson',
    'Harriet Martineau Henry Atkinson 1851 atheistic naturalism controversial',
    '"Letters on the Laws of Man\'s Nature and Development" phrenology mesmerism',
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reissue publisher',
    'Martineau Atkinson 1851 Letters atheism phrenology mesmerism controversial'
]

print(f'Executing {len(targeted_queries)} targeted searches:')
for i, query in enumerate(targeted_queries, 1):
    print(f'  {i}. {query}')

for i, query in enumerate(targeted_queries, 1):
    print(f'\nTargeted Search {i}/{len(targeted_queries)}: {query}')
    print('-' * 60)
    
    try:
        # Try Google search
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        print(f'URL: {google_url}')
        
        response = requests.get(google_url, headers=headers, timeout=20)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML
            filename = f'targeted_search_{i}_{query[:40].replace(" ", "_").replace("\'", "").replace('"', "")}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Saved: {filepath}')
            
            # Parse for results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result titles and snippets
            results_found = []
            
            # Find result containers
            result_containers = soup.find_all(['div', 'h3'], class_=lambda x: x and any(term in str(x).lower() for term in ['result', 'g-', 'rc']))
            
            if not result_containers:
                # Fallback: look for any text containing our key terms
                all_text = soup.get_text()
                if any(term in all_text.lower() for term in ['martineau', 'atkinson', '1851', 'letters']):
                    print('  ✓ Found relevant content in page text')
                    results_found.append({
                        'type': 'page_content',
                        'content': 'Relevant terms found in page',
                        'relevance_score': 1
                    })
            
            # Extract meaningful results
            for container in result_containers[:10]:
                try:
                    # Get text content
                    text_content = container.get_text().strip()
                    
                    if len(text_content) > 20:
                        text_lower = text_content.lower()
                        
                        # Calculate relevance score
                        relevance_score = 0
                        matched_terms = []
                        
                        key_terms = {
                            'martineau': 3,
                            'atkinson': 3,
                            '1851': 4,
                            'letters': 2,
                            'nature': 1,
                            'development': 2,
                            'atheistic': 3,
                            'naturalism': 3,
                            'phrenology': 3,
                            'mesmerism': 3,
                            'controversial': 2,
                            '2009': 3,
                            'reissue': 3,
                            'publisher': 2
                        }
                        
                        for term, weight in key_terms.items():
                            if term in text_lower:
                                relevance_score += weight
                                matched_terms.append(term)
                        
                        if relevance_score >= 3:
                            results_found.append({
                                'text': text_content[:300],
                                'relevance_score': relevance_score,
                                'matched_terms': matched_terms,
                                'query': query
                            })
                            
                except Exception as e:
                    continue
            
            print(f'Found {len(results_found)} relevant results')
            
            # Display high-relevance results
            high_relevance = [r for r in results_found if r['relevance_score'] >= 8]
            moderate_relevance = [r for r in results_found if 4 <= r['relevance_score'] < 8]
            
            if high_relevance:
                print(f'\n🎯 HIGH RELEVANCE RESULTS ({len(high_relevance)}):')
                for j, result in enumerate(high_relevance, 1):
                    print(f'  {j}. Score: {result["relevance_score"]} | Terms: {", ".join(result["matched_terms"][:5])}')
                    print(f'     Text: {result["text"][:150]}...')
                    print()
            
            if moderate_relevance:
                print(f'\n⭐ MODERATE RELEVANCE RESULTS ({len(moderate_relevance)}):')
                for j, result in enumerate(moderate_relevance[:3], 1):
                    print(f'  {j}. Score: {result["relevance_score"]} | Terms: {", ".join(result["matched_terms"][:3])}')
                    print(f'     Text: {result["text"][:100]}...')
            
            # Store all results
            search_results['all_findings'].extend(results_found)
            search_results['search_methods'].append(f'Google targeted: {query} - Status {response.status_code}')
            
        else:
            print(f'Failed with status {response.status_code}')
            
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)  # Rate limiting

# Method 2: Search for 2009 reissue information specifically
print('\n=== METHOD 2: SEARCHING FOR 2009 REISSUE INFORMATION ===')
print('=' * 60)

reissue_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reprint publisher',
    'Martineau Atkinson Letters 2009 edition reissued publisher',
    '"Laws of Man\'s Nature" 1851 2009 reprint edition',
    'atheistic naturalism 1851 book 2009 reissue publisher'
]

for i, query in enumerate(reissue_queries, 1):
    print(f'\nReissue Search {i}: {query}')
    
    try:
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        response = requests.get(google_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            filename = f'reissue_search_{i}_{query[:30].replace(" ", "_").replace("\'", "").replace('"', "")}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Status: {response.status_code} | Saved: {filename}')
            
            # Quick analysis for publisher information
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Look for publisher names and 2009
            publisher_indicators = ['cambridge', 'oxford', 'harvard', 'yale', 'princeton', 'university press', 'academic', 'scholarly', 'press', 'books', 'publishing']
            
            found_publishers = []
            if '2009' in page_text:
                for pub in publisher_indicators:
                    if pub in page_text:
                        found_publishers.append(pub)
            
            if found_publishers:
                print(f'  ✓ Found 2009 + publishers: {", ".join(found_publishers[:3])}')
                
                search_results['all_findings'].append({
                    'type': '2009_reissue_clue',
                    'query': query,
                    'publishers_mentioned': found_publishers,
                    'relevance_score': 5 if '2009' in page_text else 2
                })
            
            search_results['search_methods'].append(f'2009 reissue: {query} - Status {response.status_code}')
        
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(3)

# Method 3: Academic database searches
print('\n=== METHOD 3: ACADEMIC DATABASE SEARCHES ===')
print('=' * 50)

academic_sites = [
    'site:jstor.org',
    'site:muse.jhu.edu', 
    'site:cambridge.org',
    'site:oxfordacademic.com'
]

base_query = 'Martineau Atkinson 1851 Letters atheistic naturalism'

for i, site in enumerate(academic_sites, 1):
    query = f'{site} {base_query}'
    print(f'\nAcademic Search {i}: {query}')
    
    try:
        google_url = f'https://www.google.com/search?q={quote_plus(query)}'
        response = requests.get(google_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            filename = f'academic_search_{i}_{site.replace("site:", "").replace(".", "_")}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Status: {response.status_code} | Saved: {filename}')
            
            # Quick relevance check
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            relevance_terms = ['martineau', 'atkinson', '1851', 'letters', 'atheistic', 'naturalism']
            found_terms = [term for term in relevance_terms if term in page_text]
            
            if len(found_terms) >= 3:
                print(f'  ✓ Found {len(found_terms)} relevant terms: {", ".join(found_terms)}')
                
                search_results['all_findings'].append({
                    'type': 'academic_database',
                    'site': site,
                    'query': query,
                    'relevant_terms': found_terms,
                    'relevance_score': len(found_terms)
                })
            
            search_results['search_methods'].append(f'Academic {site}: Status {response.status_code}')
        
    except Exception as e:
        print(f'Error: {str(e)}')
    
    time.sleep(4)  # Longer delay for academic sites

# Comprehensive Analysis
print('\n' + '=' * 80)
print('COMPREHENSIVE ANALYSIS OF ALL SEARCH RESULTS')
print('=' * 80)

total_findings = len(search_results['all_findings'])
print(f'Total findings collected: {total_findings}')
print(f'Search methods attempted: {len(search_results["search_methods"])}')

if search_results['all_findings']:
    print('\n🔍 ANALYZING ALL FINDINGS:')
    print('-' * 40)
    
    # Categorize findings
    high_relevance = [f for f in search_results['all_findings'] if f.get('relevance_score', 0) >= 8]
    moderate_relevance = [f for f in search_results['all_findings'] if 4 <= f.get('relevance_score', 0) < 8]
    reissue_clues = [f for f in search_results['all_findings'] if f.get('type') == '2009_reissue_clue']
    academic_findings = [f for f in search_results['all_findings'] if f.get('type') == 'academic_database']
    
    print(f'\n📊 FINDINGS BREAKDOWN:')
    print(f'   • High relevance (8+ score): {len(high_relevance)}')
    print(f'   • Moderate relevance (4-7 score): {len(moderate_relevance)}')
    print(f'   • 2009 reissue clues: {len(reissue_clues)}')
    print(f'   • Academic database hits: {len(academic_findings)}')
    
    # Identify book candidates
    book_candidates = []
    
    for finding in search_results['all_findings']:
        if finding.get('relevance_score', 0) >= 6:
            # Check if it contains book-related terms
            text_content = finding.get('text', '') + ' ' + str(finding.get('matched_terms', []))
            text_lower = text_content.lower()
            
            has_book_indicators = any(indicator in text_lower for indicator in ['book', 'letters', 'work', 'treatise', 'publication'])
            has_year = '1851' in text_lower
            has_authors = any(author in text_lower for author in ['martineau', 'atkinson'])
            has_topic = any(topic in text_lower for topic in ['atheistic', 'naturalism', 'phrenology', 'mesmerism'])
            
            if has_book_indicators and has_year and (has_authors or has_topic):
                book_candidates.append(finding)
    
    search_results['book_candidates'] = book_candidates
    
    print(f'\n📚 BOOK CANDIDATES IDENTIFIED: {len(book_candidates)}')
    
    if book_candidates:
        for i, candidate in enumerate(book_candidates, 1):
            print(f'\n{i}. Relevance Score: {candidate.get("relevance_score", "N/A")}')
            print(f'   Query: {candidate.get("query", "N/A")}')
            print(f'   Terms: {", ".join(candidate.get("matched_terms", [])[:5])}')
            print(f'   Text: {candidate.get("text", "No text")[:150]}...')
    
    # Analyze 2009 reissue clues
    if reissue_clues:
        print(f'\n🔍 2009 REISSUE ANALYSIS:')
        all_publishers = []
        for clue in reissue_clues:
            publishers = clue.get('publishers_mentioned', [])
            all_publishers.extend(publishers)
        
        from collections import Counter
        publisher_counts = Counter(all_publishers)
        
        print(f'   Publishers mentioned with 2009: {dict(publisher_counts.most_common(5))}')
        
        if publisher_counts:
            most_likely_publisher = publisher_counts.most_common(1)[0][0]
            print(f'   🎯 Most likely 2009 publisher: {most_likely_publisher}')

else:
    print('\n❌ No findings collected from searches')

# Save comprehensive results
results_file = os.path.join('workspace', 'comprehensive_1851_atheistic_naturalism_search.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(search_results, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE RESULTS SAVED TO: {results_file}')

# Final summary and conclusions
search_results['analysis_summary'] = {
    'total_findings': total_findings,
    'book_candidates': len(search_results.get('book_candidates', [])),
    'search_methods_attempted': len(search_results['search_methods']),
    'likely_book_title': 'Letters on the Laws of Man\'s Nature and Development',
    'likely_authors': 'Harriet Martineau and Henry George Atkinson',
    'publication_year': '1851',
    'controversial_topics': 'atheistic naturalism, phrenology, mesmerism',
    'reissue_year': '2009 (publisher to be confirmed)'
}

print(f'\n📋 FINAL CONCLUSIONS:')
print(f'   • Most likely book: "Letters on the Laws of Man\'s Nature and Development"')
print(f'   • Authors: Harriet Martineau and Henry George Atkinson')
print(f'   • Original publication: 1851')
print(f'   • Controversial topics: Atheistic naturalism, phrenology, mesmerism')
print(f'   • 2009 reissue: Publisher needs verification from search results')

print(f'\n📊 SEARCH STATISTICS:')
print(f'   • Total findings: {search_results["analysis_summary"]["total_findings"]}')
print(f'   • Book candidates: {search_results["analysis_summary"]["book_candidates"]}')
print(f'   • Methods attempted: {search_results["analysis_summary"]["search_methods_attempted"]}')

print(f'\n🎯 NEXT STEPS:')
print('1. ✅ Review saved HTML files for 2009 publisher information')
print('2. ✅ Cross-reference findings to confirm publisher details')
print('3. ✅ Verify the complete bibliographic information')
print('4. 📋 Check academic databases for definitive publication details')

print('\n=== COMPREHENSIVE SEARCH FOR 1851 ATHEISTIC NATURALISM BOOK COMPLETE ===')
```

## Development History
*(This section will be updated as development progresses)*

