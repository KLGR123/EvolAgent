# Developer Plan #3 - anthropic.claude-sonnet-4-20250514-v1:0

**Task ID:** webshaper_42  
**Model:** anthropic.claude-sonnet-4-20250514-v1:0  
**Plan Index:** 3  
**Timestamp:** 2025-08-10 14:38:28

## Plan Content
```
Based on the comprehensive research results from the HISTORY, analyze the publication years identified for Eric Van Young's Mexican rural history articles to determine which specific year answers the TASK question. The developer found multiple publications spanning 1983, 1993, 2006, and 2020, with his seminal work 'Mexican rural history since Chevalier: The historiography of the colonial hacienda' published in 1983 in Latin American Research Review being the most directly relevant article about Mexican rural history.
```

## Plan Description
```
This analysis step is needed because: (1) The previous search successfully identified Eric Van Young as the editor of the 1992 Center for U.S.-Mexican Studies publication and found multiple years when he published on Mexican rural history, (2) We have concrete publication years (1983, 1993, 2006, 2020) but need to determine which represents the primary article on Mexican rural history referenced in the TASK, (3) Expected outcome is to identify 1983 as the answer, given that 'Mexican rural history since Chevalier' appears to be his foundational work specifically focused on Mexican rural history, (4) This will provide the definitive year answer required by the TASK
```

## Retrieved Episodic Memory Examples
### Development Step 11: Identify 2009 Reissue Publisher of Martineau and Atkinson’s “Letters on the Laws of Man’s Nature”

**Description**: Verify the specific publisher that reissued 'Letters on the Laws of Man's Nature and Development' by Harriet Martineau and Henry George Atkinson in 2009. The previous search confirmed this is the correct 1851 co-authored book on atheistic naturalism, phrenology, and mesmerism, but we need to identify the exact 2009 reissue publisher. Search for '2009 reissue Letters on the Laws of Man's Nature and Development publisher', 'Martineau Atkinson 2009 republication', and check academic publishers, university presses, or specialty reprint publishers that may have reissued this historical work in 2009.

**Use Cases**:
- Academic historians verifying the 2009 reissue publisher of Martineau and Atkinson’s 1851 work to ensure accurate citations in a peer-reviewed journal article on Victorian-era naturalist philosophies
- University library metadata teams automating batch extraction of edition and publisher details for rare-book catalog updates in their digital archives
- Rare-book dealers cross-referencing multiple online sources to authenticate and price a 2009 reprint of a public-domain 19th-century title before listing it on their e-commerce platform
- Legal publishing departments conducting due-diligence on reproduction rights by identifying the exact 2009 reprint publisher to secure permissions for a digital facsimile release
- Digital humanities researchers mapping academic press networks by extracting publisher information across historical reissues to study the spread of 19th-century scientific ideas
- University presses planning a new annotated edition and using automated web-scraping to avoid overlaps with the 2009 reprint publisher’s rights and market positioning
- Bibliographic data specialists enhancing WorldCat and OCLC records by programmatically detecting and updating publisher fields for the 2009 republication of “Letters on the Laws of Man’s Nature and Development”

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import quote_plus, urljoin

print('=== SEARCHING FOR 2009 REISSUE PUBLISHER OF MARTINEAU-ATKINSON LETTERS ===')
print('Title: Letters on the Laws of Man\'s Nature and Development')
print('Authors: Harriet Martineau and Henry George Atkinson')
print('Original: 1851')
print('Target: 2009 reissue publisher identification')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Headers for web requests
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

# Define comprehensive search queries for 2009 reissue
search_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 2009 publisher',
    'Martineau Atkinson "Letters Laws" 2009 reissue',
    'Harriet Martineau Henry Atkinson 2009 republication',
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reprint',
    'Martineau Atkinson 2009 edition publisher',
    '"Laws of Man\'s Nature and Development" 2009 reissue',
    'Harriet Martineau 2009 Letters Laws publisher',
    'Henry George Atkinson 2009 reprint publisher',
    '"Letters on the Laws" Martineau Atkinson 2009',
    'Martineau Atkinson correspondence 2009 publisher'
]

print('=== STEP 1: CONDUCTING TARGETED PUBLISHER SEARCHES ===')
print(f'Total search queries: {len(search_queries)}')
print('\nSearch queries:')
for i, query in enumerate(search_queries, 1):
    print(f'  {i:2d}. {query}')

search_results = {}
search_base_url = 'https://html.duckduckgo.com/html/'

# Function to perform search and analyze results
def perform_search(query, search_index):
    print(f'\n--- SEARCH {search_index}: {query} ---')
    try:
        params = {'q': query}
        response = requests.get(search_base_url, params=params, headers=headers, timeout=30)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML for analysis
            filename = f'search_{search_index:02d}_{query.replace(" ", "_").replace("\'", "").replace('"', "")[:40]}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Saved: {filepath}')
            
            # Parse for relevant results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result links with publisher information
            result_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                
                # Filter for highly relevant results
                if href and text and len(text) > 15:
                    text_lower = text.lower()
                    relevance_score = 0
                    
                    # High-value terms for 2009 reissue identification
                    high_value_terms = [
                        ('2009', 3),
                        ('martineau', 2),
                        ('atkinson', 2),
                        ('letters', 1),
                        ('laws', 1),
                        ('nature', 1),
                        ('development', 1),
                        ('publisher', 2),
                        ('reissue', 2),
                        ('reprint', 2),
                        ('edition', 1),
                        ('republication', 2)
                    ]
                    
                    # Publisher-specific terms
                    publisher_terms = [
                        ('cambridge university press', 4),
                        ('oxford university press', 4),
                        ('harvard university press', 4),
                        ('yale university press', 4),
                        ('princeton university press', 4),
                        ('university of chicago press', 4),
                        ('routledge', 3),
                        ('palgrave', 3),
                        ('macmillan', 3),
                        ('springer', 3),
                        ('brill', 3),
                        ('ashgate', 3),
                        ('continuum', 3),
                        ('thoemmes', 3),
                        ('pickering', 3),
                        ('nabu press', 2),
                        ('kessinger', 2),
                        ('forgotten books', 2),
                        ('bibliolife', 2),
                        ('gale ecco', 2),
                        ('making of modern law', 2)
                    ]
                    
                    # Calculate relevance score
                    for term, score in high_value_terms + publisher_terms:
                        if term in text_lower:
                            relevance_score += score
                    
                    # Additional scoring for URL domains
                    if href:
                        href_lower = href.lower()
                        if any(domain in href_lower for domain in ['cambridge.org', 'oup.com', 'harvard.edu', 'yale.edu', 'routledge.com', 'palgrave.com']):
                            relevance_score += 3
                        elif any(domain in href_lower for domain in ['amazon.com', 'worldcat.org', 'goodreads.com', 'abebooks.com']):
                            relevance_score += 2
                    
                    if relevance_score >= 3:  # Only include highly relevant results
                        result_links.append({
                            'url': href,
                            'text': text[:300],  # Longer text for better analysis
                            'relevance_score': relevance_score
                        })
            
            # Sort by relevance score
            result_links.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            search_results[query] = {
                'html_file': filepath,
                'status_code': response.status_code,
                'relevant_links': result_links[:15],  # Top 15 most relevant
                'total_links_found': len(result_links)
            }
            
            print(f'Found {len(result_links)} highly relevant links')
            if result_links:
                print('Top results:')
                for i, link in enumerate(result_links[:5], 1):
                    print(f'  {i}. Score {link["relevance_score"]}: {link["text"][:120]}...')
                    print(f'     URL: {link["url"]}')
            
            time.sleep(2)  # Rate limiting
            return True
        else:
            print(f'Failed: HTTP {response.status_code}')
            return False
            
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

# Perform all searches
print('\n=== EXECUTING SEARCHES ===')
successful_searches = 0

for i, query in enumerate(search_queries, 1):
    if perform_search(query, i):
        successful_searches += 1
    
    # Brief pause between searches
    if i < len(search_queries):
        time.sleep(1)

print(f'\n=== STEP 2: ANALYZING SEARCH RESULTS ===')
print(f'Successful searches: {successful_searches}/{len(search_queries)}')

# Compile and analyze all findings
high_priority_findings = []
all_publishers_mentioned = set()
publisher_frequency = {}

# Known academic and reprint publishers to watch for
known_publishers = [
    'Cambridge University Press', 'Oxford University Press', 'Harvard University Press',
    'Yale University Press', 'Princeton University Press', 'University of Chicago Press',
    'Routledge', 'Palgrave Macmillan', 'Springer', 'Brill', 'Ashgate', 'Continuum',
    'Thoemmes Press', 'Pickering & Chatto', 'Nabu Press', 'Kessinger Publishing',
    'Forgotten Books', 'BiblioLife', 'Gale ECCO', 'Making of Modern Law',
    'Elibron Classics', 'Palala Press', 'Wentworth Press', 'Franklin Classics'
]

print('\n--- ANALYZING ALL SEARCH RESULTS FOR PUBLISHER PATTERNS ---')

for query, results in search_results.items():
    print(f'\nQuery: "{query}"')
    print(f'  Relevant links: {results["total_links_found"]}')
    
    for link in results['relevant_links']:
        # Check for 2009 and publisher combinations
        text_lower = link['text'].lower()
        
        if '2009' in text_lower and any(pub.lower() in text_lower for pub in known_publishers):
            # This is a high-priority finding
            matching_publishers = [pub for pub in known_publishers if pub.lower() in text_lower]
            
            high_priority_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'score': link['relevance_score'],
                'publishers_mentioned': matching_publishers,
                'priority': 'HIGH - Contains 2009 + Publisher'
            })
            
            # Track publisher frequency
            for pub in matching_publishers:
                publisher_frequency[pub] = publisher_frequency.get(pub, 0) + 1
                all_publishers_mentioned.add(pub)
            
            print(f'  🎯 HIGH PRIORITY: {matching_publishers} mentioned with 2009')
        
        elif '2009' in text_lower:
            # Contains 2009 but may have publisher info we need to extract
            high_priority_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'score': link['relevance_score'],
                'publishers_mentioned': [],
                'priority': 'MEDIUM - Contains 2009'
            })
            
            print(f'  📍 MEDIUM: Contains 2009, checking for publisher info')
        
        # Track any publisher mentions regardless of year
        for pub in known_publishers:
            if pub.lower() in text_lower:
                all_publishers_mentioned.add(pub)
                publisher_frequency[pub] = publisher_frequency.get(pub, 0) + 1

print(f'\n=== STEP 3: PUBLISHER FREQUENCY ANALYSIS ===')
print(f'Total unique publishers mentioned: {len(all_publishers_mentioned)}')
print(f'High-priority findings (2009 + publisher): {len([f for f in high_priority_findings if f["priority"].startswith("HIGH")])}')

if publisher_frequency:
    print('\nPublisher mention frequency:')
    sorted_publishers = sorted(publisher_frequency.items(), key=lambda x: x[1], reverse=True)
    for pub, count in sorted_publishers:
        print(f'  {pub}: {count} mentions')
else:
    print('\nNo specific publishers identified in search results')

print(f'\n=== STEP 4: DETAILED ANALYSIS OF HIGH-PRIORITY FINDINGS ===')

if high_priority_findings:
    # Sort by priority and score
    high_priority_findings.sort(key=lambda x: (x['priority'] == 'HIGH - Contains 2009 + Publisher', x['score']), reverse=True)
    
    print(f'\nAnalyzing {len(high_priority_findings)} high-priority findings:')
    
    for i, finding in enumerate(high_priority_findings[:10], 1):  # Top 10 findings
        print(f'\n🔍 FINDING {i} - {finding["priority"]} (Score: {finding["score"]})')
        print(f'Query: {finding["query"]}')
        print(f'Publishers: {finding["publishers_mentioned"] if finding["publishers_mentioned"] else "None explicitly identified"}')
        print(f'URL: {finding["url"]}')
        print(f'Text: {finding["text"][:400]}...')
        print('-' * 120)
        
        # If this is a high-priority finding with a specific URL, we should investigate further
        if finding['priority'].startswith('HIGH') and finding['url']:
            print(f'  ⭐ RECOMMENDED FOR DETAILED INVESTIGATION: {finding["url"]}')
else:
    print('\n⚠ No high-priority findings identified')
    print('This suggests the 2009 reissue may be from a smaller or specialized publisher')

# Check for specific reprint/specialty publishers
print(f'\n=== STEP 5: CHECKING FOR SPECIALTY REPRINT PUBLISHERS ===')

specialty_publishers = [
    'Nabu Press', 'Kessinger Publishing', 'Forgotten Books', 'BiblioLife',
    'Palala Press', 'Wentworth Press', 'Franklin Classics', 'Elibron Classics',
    'Gale ECCO', 'Making of Modern Law', 'Thoemmes Press', 'Pickering & Chatto'
]

specialty_findings = []
for query, results in search_results.items():
    for link in results['relevant_links']:
        text_lower = link['text'].lower()
        
        for specialty_pub in specialty_publishers:
            if specialty_pub.lower() in text_lower:
                specialty_findings.append({
                    'publisher': specialty_pub,
                    'query': query,
                    'text': link['text'],
                    'url': link['url'],
                    'has_2009': '2009' in text_lower
                })

if specialty_findings:
    print(f'Found {len(specialty_findings)} specialty publisher mentions:')
    
    # Group by publisher
    by_publisher = {}
    for finding in specialty_findings:
        pub = finding['publisher']
        if pub not in by_publisher:
            by_publisher[pub] = []
        by_publisher[pub].append(finding)
    
    for pub, findings in by_publisher.items():
        print(f'\n{pub}: {len(findings)} mentions')
        for finding in findings[:2]:  # Show top 2 per publisher
            status = '✓ WITH 2009' if finding['has_2009'] else '- without 2009'
            print(f'  {status}: {finding["text"][:150]}...')
            print(f'    URL: {finding["url"]}')
else:
    print('No specialty reprint publishers clearly identified')

# Save comprehensive analysis
analysis_results = {
    'search_objective': 'Identify 2009 reissue publisher for Martineau-Atkinson Letters',
    'book_details': {
        'title': 'Letters on the Laws of Man\'s Nature and Development',
        'authors': ['Harriet Martineau', 'Henry George Atkinson'],
        'original_year': 1851,
        'target_reissue_year': 2009
    },
    'search_summary': {
        'total_queries': len(search_queries),
        'successful_searches': successful_searches,
        'total_relevant_links': sum(len(r['relevant_links']) for r in search_results.values())
    },
    'publisher_analysis': {
        'publishers_mentioned': list(all_publishers_mentioned),
        'publisher_frequency': publisher_frequency,
        'high_priority_findings_count': len([f for f in high_priority_findings if f['priority'].startswith('HIGH')]),
        'specialty_publisher_findings': len(specialty_findings)
    },
    'high_priority_findings': high_priority_findings[:10],  # Top 10 findings
    'specialty_findings': specialty_findings,
    'search_queries_used': search_queries,
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

analysis_file = 'workspace/martineau_atkinson_2009_publisher_analysis.json'
with open(analysis_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

print(f'\n*** PUBLISHER SEARCH ANALYSIS COMPLETE ***')
print(f'✓ Conducted {successful_searches} successful searches')
print(f'✓ Analyzed {sum(len(r["relevant_links"]) for r in search_results.values())} relevant results')
print(f'✓ Identified {len(all_publishers_mentioned)} unique publishers mentioned')
print(f'✓ Found {len(high_priority_findings)} high-priority findings')
print(f'✓ Comprehensive analysis saved to: {analysis_file}')

# Summary of most promising leads
if high_priority_findings:
    top_finding = high_priority_findings[0]
    print(f'\n🎯 MOST PROMISING LEAD:')
    print(f'Priority: {top_finding["priority"]}')
    print(f'Publishers mentioned: {top_finding["publishers_mentioned"]}')
    print(f'Score: {top_finding["score"]}')
    print(f'URL: {top_finding["url"]}')
else:
    print(f'\n⚠ No definitive 2009 publisher identified in initial search')
    print('Recommend manual investigation of saved search results')

print('\nFiles created in workspace:')
for file in sorted(os.listdir('workspace')):
    file_path = os.path.join('workspace', file)
    file_size = os.path.getsize(file_path)
    print(f'- {file} ({file_size:,} bytes)')

print('\n=== NEXT STEPS ===')
print('1. Review high-priority findings for definitive publisher identification')
print('2. Investigate URLs from top-scoring results')
print('3. Check specialty reprint publishers for 2009 editions')
print('4. Cross-reference with library catalogs (WorldCat, etc.)')
```

### Development Step 13: 2009 Reissue Publisher of “Letters on the Laws of Man’s Nature and Development”

**Description**: Verify the specific publisher that reissued 'Letters on the Laws of Man's Nature and Development' by Harriet Martineau and Henry George Atkinson in 2009. The previous search confirmed this is the correct 1851 co-authored book on atheistic naturalism, phrenology, and mesmerism, but we need to identify the exact 2009 reissue publisher. Search for '2009 reissue Letters on the Laws of Man's Nature and Development publisher', 'Martineau Atkinson 2009 republication', and check academic publishers, university presses, or specialty reprint publishers that may have reissued this historical work in 2009.

**Use Cases**:
- Library catalog metadata enhancement: automating the identification of the 2009 reissue publisher for historical titles like Martineau & Atkinson’s Letters to update and standardize library records.
- Antiquarian book dealership due diligence: verifying the authenticity and exact publisher of a 2009 reprint of a rare 1851 naturalism/phrenology work before listing it for sale.
- Academic bibliography validation: enabling researchers to confirm the correct publisher and edition year when citing the 2009 reissue of a 19th-century correspondence volume.
- Digital humanities project metadata curation: scraping and analyzing online sources to fill missing publisher fields for digitized archives of classical texts reissued in 2009.
- Online book retailer inventory verification: automatically cross-checking product listings to ensure the 2009 edition of Martineau & Atkinson’s work is attributed to the correct reprint publisher.
- Publishing market intelligence gathering: detecting specialty reprint publishers and tracking their 2009 release patterns for competitive analysis in the academic book market.
- Library acquisition workflow automation: integrating web-scraping scripts to auto-populate publisher details for newly acquired historical reprints in the year 2009.
- Reference management tool integration: building a plugin that fetches edition and publisher information for specified historical works (e.g., 2009 reissues) directly into citation software.

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import quote_plus, urljoin

print('=== FULLY FIXED: SEARCHING FOR 2009 REISSUE PUBLISHER OF MARTINEAU-ATKINSON LETTERS ===')
print('Title: Letters on the Laws of Man\'s Nature and Development')
print('Authors: Harriet Martineau and Henry George Atkinson')
print('Original: 1851')
print('Target: 2009 reissue publisher identification')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Define comprehensive search queries for 2009 reissue
search_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 2009 publisher',
    'Martineau Atkinson "Letters Laws" 2009 reissue',
    'Harriet Martineau Henry Atkinson 2009 republication',
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reprint',
    'Martineau Atkinson 2009 edition publisher',
    '"Laws of Man\'s Nature and Development" 2009 reissue',
    'Harriet Martineau 2009 Letters Laws publisher',
    'Henry George Atkinson 2009 reprint publisher',
    '"Letters on the Laws" Martineau Atkinson 2009',
    'Martineau Atkinson correspondence 2009 publisher'
]

print('=== STEP 1: CONDUCTING TARGETED PUBLISHER SEARCHES ===')
print(f'Total search queries: {len(search_queries)}')
print('\nSearch queries:')
for i, query in enumerate(search_queries, 1):
    print(f'  {i:2d}. {query}')

search_results = {}

# Function to perform search and analyze results - FIXED ALL VARIABLE SCOPE ISSUES
def perform_search(query, search_index):
    # Define ALL required variables inside function to fix scope issues
    search_base_url = 'https://html.duckduckgo.com/html/'
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
    
    print(f'\n--- SEARCH {search_index}: {query} ---')
    try:
        params = {'q': query}
        response = requests.get(search_base_url, params=params, headers=headers, timeout=30)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML for analysis
            filename = f'search_{search_index:02d}_{query.replace(" ", "_").replace("\'", "").replace('"', "")[:40]}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Saved: {filepath}')
            
            # Parse for relevant results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result links with publisher information
            result_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                
                # Filter for highly relevant results
                if href and text and len(text) > 15:
                    text_lower = text.lower()
                    relevance_score = 0
                    
                    # High-value terms for 2009 reissue identification
                    high_value_terms = [
                        ('2009', 3),
                        ('martineau', 2),
                        ('atkinson', 2),
                        ('letters', 1),
                        ('laws', 1),
                        ('nature', 1),
                        ('development', 1),
                        ('publisher', 2),
                        ('reissue', 2),
                        ('reprint', 2),
                        ('edition', 1),
                        ('republication', 2)
                    ]
                    
                    # Publisher-specific terms
                    publisher_terms = [
                        ('cambridge university press', 4),
                        ('oxford university press', 4),
                        ('harvard university press', 4),
                        ('yale university press', 4),
                        ('princeton university press', 4),
                        ('university of chicago press', 4),
                        ('routledge', 3),
                        ('palgrave', 3),
                        ('macmillan', 3),
                        ('springer', 3),
                        ('brill', 3),
                        ('ashgate', 3),
                        ('continuum', 3),
                        ('thoemmes', 3),
                        ('pickering', 3),
                        ('nabu press', 2),
                        ('kessinger', 2),
                        ('forgotten books', 2),
                        ('bibliolife', 2),
                        ('gale ecco', 2),
                        ('making of modern law', 2)
                    ]
                    
                    # Calculate relevance score
                    for term, score in high_value_terms + publisher_terms:
                        if term in text_lower:
                            relevance_score += score
                    
                    # Additional scoring for URL domains
                    if href:
                        href_lower = href.lower()
                        if any(domain in href_lower for domain in ['cambridge.org', 'oup.com', 'harvard.edu', 'yale.edu', 'routledge.com', 'palgrave.com']):
                            relevance_score += 3
                        elif any(domain in href_lower for domain in ['amazon.com', 'worldcat.org', 'goodreads.com', 'abebooks.com']):
                            relevance_score += 2
                    
                    if relevance_score >= 3:  # Only include highly relevant results
                        result_links.append({
                            'url': href,
                            'text': text[:300],  # Longer text for better analysis
                            'relevance_score': relevance_score
                        })
            
            # Sort by relevance score
            result_links.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            search_results[query] = {
                'html_file': filepath,
                'status_code': response.status_code,
                'relevant_links': result_links[:15],  # Top 15 most relevant
                'total_links_found': len(result_links)
            }
            
            print(f'Found {len(result_links)} highly relevant links')
            if result_links:
                print('Top results:')
                for i, link in enumerate(result_links[:5], 1):
                    print(f'  {i}. Score {link["relevance_score"]}: {link["text"][:120]}...')
                    print(f'     URL: {link["url"]}')
            
            time.sleep(2)  # Rate limiting
            return True
        else:
            print(f'Failed: HTTP {response.status_code}')
            return False
            
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

# Perform all searches
print('\n=== EXECUTING SEARCHES ===')
successful_searches = 0

for i, query in enumerate(search_queries, 1):
    if perform_search(query, i):
        successful_searches += 1
    
    # Brief pause between searches
    if i < len(search_queries):
        time.sleep(1)

print(f'\n=== STEP 2: ANALYZING SEARCH RESULTS ===')
print(f'Successful searches: {successful_searches}/{len(search_queries)}')

# Compile and analyze all findings
high_priority_findings = []
all_publishers_mentioned = set()
publisher_frequency = {}

# Known academic and reprint publishers to watch for
known_publishers = [
    'Cambridge University Press', 'Oxford University Press', 'Harvard University Press',
    'Yale University Press', 'Princeton University Press', 'University of Chicago Press',
    'Routledge', 'Palgrave Macmillan', 'Springer', 'Brill', 'Ashgate', 'Continuum',
    'Thoemmes Press', 'Pickering & Chatto', 'Nabu Press', 'Kessinger Publishing',
    'Forgotten Books', 'BiblioLife', 'Gale ECCO', 'Making of Modern Law',
    'Elibron Classics', 'Palala Press', 'Wentworth Press', 'Franklin Classics'
]

print('\n--- ANALYZING ALL SEARCH RESULTS FOR PUBLISHER PATTERNS ---')

for query, results in search_results.items():
    print(f'\nQuery: "{query}"')
    print(f'  Relevant links: {results["total_links_found"]}')
    
    for link in results['relevant_links']:
        # Check for 2009 and publisher combinations
        text_lower = link['text'].lower()
        
        if '2009' in text_lower and any(pub.lower() in text_lower for pub in known_publishers):
            # This is a high-priority finding
            matching_publishers = [pub for pub in known_publishers if pub.lower() in text_lower]
            
            high_priority_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'score': link['relevance_score'],
                'publishers_mentioned': matching_publishers,
                'priority': 'HIGH - Contains 2009 + Publisher'
            })
            
            # Track publisher frequency
            for pub in matching_publishers:
                publisher_frequency[pub] = publisher_frequency.get(pub, 0) + 1
                all_publishers_mentioned.add(pub)
            
            print(f'  🎯 HIGH PRIORITY: {matching_publishers} mentioned with 2009')
        
        elif '2009' in text_lower:
            # Contains 2009 but may have publisher info we need to extract
            high_priority_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'score': link['relevance_score'],
                'publishers_mentioned': [],
                'priority': 'MEDIUM - Contains 2009'
            })
            
            print(f'  📍 MEDIUM: Contains 2009, checking for publisher info')
        
        # Track any publisher mentions regardless of year
        for pub in known_publishers:
            if pub.lower() in text_lower:
                all_publishers_mentioned.add(pub)
                publisher_frequency[pub] = publisher_frequency.get(pub, 0) + 1

print(f'\n=== STEP 3: PUBLISHER FREQUENCY ANALYSIS ===')
print(f'Total unique publishers mentioned: {len(all_publishers_mentioned)}')
print(f'High-priority findings (2009 + publisher): {len([f for f in high_priority_findings if f["priority"].startswith("HIGH")])}')

if publisher_frequency:
    print('\nPublisher mention frequency:')
    sorted_publishers = sorted(publisher_frequency.items(), key=lambda x: x[1], reverse=True)
    for pub, count in sorted_publishers:
        print(f'  {pub}: {count} mentions')
else:
    print('\nNo specific publishers identified in search results')

print(f'\n=== STEP 4: DETAILED ANALYSIS OF HIGH-PRIORITY FINDINGS ===')

if high_priority_findings:
    # Sort by priority and score
    high_priority_findings.sort(key=lambda x: (x['priority'] == 'HIGH - Contains 2009 + Publisher', x['score']), reverse=True)
    
    print(f'\nAnalyzing {len(high_priority_findings)} high-priority findings:')
    
    for i, finding in enumerate(high_priority_findings[:10], 1):  # Top 10 findings
        print(f'\n🔍 FINDING {i} - {finding["priority"]} (Score: {finding["score"]})')
        print(f'Query: {finding["query"]}')
        print(f'Publishers: {finding["publishers_mentioned"] if finding["publishers_mentioned"] else "None explicitly identified"}')
        print(f'URL: {finding["url"]}')
        print(f'Text: {finding["text"][:400]}...')
        print('-' * 120)
        
        # If this is a high-priority finding with a specific URL, we should investigate further
        if finding['priority'].startswith('HIGH') and finding['url']:
            print(f'  ⭐ RECOMMENDED FOR DETAILED INVESTIGATION: {finding["url"]}')
else:
    print('\n⚠ No high-priority findings identified')
    print('This suggests the 2009 reissue may be from a smaller or specialized publisher')

# Check for specific reprint/specialty publishers
print(f'\n=== STEP 5: CHECKING FOR SPECIALTY REPRINT PUBLISHERS ===')

specialty_publishers = [
    'Nabu Press', 'Kessinger Publishing', 'Forgotten Books', 'BiblioLife',
    'Palala Press', 'Wentworth Press', 'Franklin Classics', 'Elibron Classics',
    'Gale ECCO', 'Making of Modern Law', 'Thoemmes Press', 'Pickering & Chatto'
]

specialty_findings = []
for query, results in search_results.items():
    for link in results['relevant_links']:
        text_lower = link['text'].lower()
        
        for specialty_pub in specialty_publishers:
            if specialty_pub.lower() in text_lower:
                specialty_findings.append({
                    'publisher': specialty_pub,
                    'query': query,
                    'text': link['text'],
                    'url': link['url'],
                    'has_2009': '2009' in text_lower
                })

if specialty_findings:
    print(f'Found {len(specialty_findings)} specialty publisher mentions:')
    
    # Group by publisher
    by_publisher = {}
    for finding in specialty_findings:
        pub = finding['publisher']
        if pub not in by_publisher:
            by_publisher[pub] = []
        by_publisher[pub].append(finding)
    
    for pub, findings in by_publisher.items():
        print(f'\n{pub}: {len(findings)} mentions')
        for finding in findings[:2]:  # Show top 2 per publisher
            status = '✓ WITH 2009' if finding['has_2009'] else '- without 2009'
            print(f'  {status}: {finding["text"][:150]}...')
            print(f'    URL: {finding["url"]}')
else:
    print('No specialty reprint publishers clearly identified')

# Additional search for specific reprint publisher patterns
print(f'\n=== STEP 6: ANALYZING FOR REPRINT PUBLISHER PATTERNS ===')

# Look for common reprint publisher indicators in all search results
reprint_indicators = [
    'reprint', 'reprinted', 'reproduction', 'facsimile', 'digitally printed',
    'print on demand', 'pod', 'classic reprint', 'historical reproduction',
    'nabu', 'kessinger', 'forgotten books', 'bibliolife', 'palala',
    'wentworth', 'franklin classics', 'elibron', 'gale ecco'
]

reprint_pattern_findings = []
for query, results in search_results.items():
    for link in results['relevant_links']:
        text_lower = link['text'].lower()
        
        # Check for reprint indicators
        found_indicators = []
        for indicator in reprint_indicators:
            if indicator in text_lower:
                found_indicators.append(indicator)
        
        if found_indicators and '2009' in text_lower:
            reprint_pattern_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'indicators': found_indicators,
                'score': link['relevance_score']
            })

if reprint_pattern_findings:
    print(f'Found {len(reprint_pattern_findings)} results with 2009 + reprint indicators:')
    
    # Sort by number of indicators and score
    reprint_pattern_findings.sort(key=lambda x: (len(x['indicators']), x['score']), reverse=True)
    
    for i, finding in enumerate(reprint_pattern_findings[:5], 1):
        print(f'\n🎯 REPRINT PATTERN {i}:')
        print(f'Indicators: {finding["indicators"]}')
        print(f'Score: {finding["score"]}')
        print(f'URL: {finding["url"]}')
        print(f'Text: {finding["text"][:200]}...')
        print('-' * 80)
else:
    print('No clear reprint patterns with 2009 found')

# Save comprehensive analysis
analysis_results = {
    'search_objective': 'Identify 2009 reissue publisher for Martineau-Atkinson Letters',
    'book_details': {
        'title': 'Letters on the Laws of Man\'s Nature and Development',
        'authors': ['Harriet Martineau', 'Henry George Atkinson'],
        'original_year': 1851,
        'target_reissue_year': 2009
    },
    'search_summary': {
        'total_queries': len(search_queries),
        'successful_searches': successful_searches,
        'total_relevant_links': sum(len(r['relevant_links']) for r in search_results.values())
    },
    'publisher_analysis': {
        'publishers_mentioned': list(all_publishers_mentioned),
        'publisher_frequency': publisher_frequency,
        'high_priority_findings_count': len([f for f in high_priority_findings if f['priority'].startswith('HIGH')]),
        'specialty_publisher_findings': len(specialty_findings),
        'reprint_pattern_findings': len(reprint_pattern_findings)
    },
    'high_priority_findings': high_priority_findings[:10],  # Top 10 findings
    'specialty_findings': specialty_findings,
    'reprint_pattern_findings': reprint_pattern_findings[:5],  # Top 5 reprint patterns
    'search_queries_used': search_queries,
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

analysis_file = 'workspace/martineau_atkinson_2009_publisher_search_complete.json'
with open(analysis_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

print(f'\n*** PUBLISHER SEARCH ANALYSIS COMPLETE ***')
print(f'✓ Conducted {successful_searches} successful searches')
print(f'✓ Analyzed {sum(len(r["relevant_links"]) for r in search_results.values())} relevant results')
print(f'✓ Identified {len(all_publishers_mentioned)} unique publishers mentioned')
print(f'✓ Found {len(high_priority_findings)} high-priority findings')
print(f'✓ Found {len(reprint_pattern_findings)} reprint pattern matches')
print(f'✓ Comprehensive analysis saved to: {analysis_file}')

# Summary of most promising leads
if high_priority_findings:
    top_finding = high_priority_findings[0]
    print(f'\n🎯 MOST PROMISING LEAD:')
    print(f'Priority: {top_finding["priority"]}')
    print(f'Publishers mentioned: {top_finding["publishers_mentioned"]}')
    print(f'Score: {top_finding["score"]}')
    print(f'URL: {top_finding["url"]}')
elif reprint_pattern_findings:
    top_reprint = reprint_pattern_findings[0]
    print(f'\n🎯 MOST PROMISING REPRINT LEAD:')
    print(f'Reprint indicators: {top_reprint["indicators"]}')
    print(f'Score: {top_reprint["score"]}')
    print(f'URL: {top_reprint["url"]}')
else:
    print(f'\n⚠ No definitive 2009 publisher identified in initial search')
    print('Recommend manual investigation of saved search results')

# Check existing search files for additional clues
print(f'\n=== STEP 7: CHECKING EXISTING SEARCH FILES FOR 2009 REFERENCES ===')

workspace_files = [f for f in os.listdir('workspace') if f.endswith('.html')]
print(f'Found {len(workspace_files)} existing HTML search files to analyze')

# Look for 2009 references in existing files
files_with_2009 = []
for filename in workspace_files[:20]:  # Check first 20 files to avoid overwhelming output
    filepath = os.path.join('workspace', filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            if '2009' in content and ('martineau' in content or 'atkinson' in content):
                # Count occurrences
                count_2009 = content.count('2009')
                count_martineau = content.count('martineau')
                count_atkinson = content.count('atkinson')
                
                files_with_2009.append({
                    'filename': filename,
                    'count_2009': count_2009,
                    'count_martineau': count_martineau,
                    'count_atkinson': count_atkinson,
                    'total_relevance': count_2009 + count_martineau + count_atkinson
                })
    except Exception as e:
        print(f'Error reading {filename}: {str(e)}')

if files_with_2009:
    print(f'\nFound {len(files_with_2009)} existing files with 2009 + author references:')
    
    # Sort by relevance
    files_with_2009.sort(key=lambda x: x['total_relevance'], reverse=True)
    
    for i, file_info in enumerate(files_with_2009[:5], 1):
        print(f'{i}. {file_info["filename"]}')
        print(f'   2009: {file_info["count_2009"]}, Martineau: {file_info["count_martineau"]}, Atkinson: {file_info["count_atkinson"]}')
        
        # Try to extract specific publisher information from this file
        filepath = os.path.join('workspace', file_info['filename'])
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')
                
                # Look for text containing both 2009 and publisher names
                text_content = soup.get_text().lower()
                
                # Find sentences/phrases containing 2009
                sentences_with_2009 = []
                lines = text_content.split('\n')
                for line in lines:
                    if '2009' in line and ('martineau' in line or 'atkinson' in line):
                        # Check if any known publishers are mentioned
                        for pub in known_publishers:
                            if pub.lower() in line:
                                sentences_with_2009.append({
                                    'text': line.strip()[:200],
                                    'publisher': pub
                                })
                                break
                        else:
                            # Check for specialty publishers
                            for specialty_pub in specialty_publishers:
                                if specialty_pub.lower() in line:
                                    sentences_with_2009.append({
                                        'text': line.strip()[:200],
                                        'publisher': specialty_pub
                                    })
                                    break
                
                if sentences_with_2009:
                    print(f'   🎯 PUBLISHER CLUES FOUND:')
                    for j, clue in enumerate(sentences_with_2009[:3], 1):
                        print(f'     {j}. {clue["publisher"]}: {clue["text"]}...')
                        
        except Exception as e:
            print(f'   Error analyzing {file_info["filename"]}: {str(e)}')
else:
    print('\nNo existing files found with 2009 + author references')

print('\n=== SEARCH COMPLETION SUMMARY ===')
print('✓ Executed comprehensive web searches for 2009 reissue publisher')
print('✓ Analyzed both new search results and existing workspace files')
print('✓ Applied advanced relevance scoring and pattern detection')
print('✓ Checked for both academic and specialty reprint publishers')
print('\nRecommendations for manual follow-up:')
print('1. Review high-priority findings URLs for definitive publisher identification')
print('2. Cross-reference findings with WorldCat or library catalogs')
print('3. Check Amazon or Google Books for 2009 edition details')
print('4. Contact academic libraries for specialized reprint publisher information')
```

### Development Step 12: 2009 Reissue Publisher of Martineau & Atkinson's Letters on Laws of Man's Nature and Development

**Description**: Verify the specific publisher that reissued 'Letters on the Laws of Man's Nature and Development' by Harriet Martineau and Henry George Atkinson in 2009. The previous search confirmed this is the correct 1851 co-authored book on atheistic naturalism, phrenology, and mesmerism, but we need to identify the exact 2009 reissue publisher. Search for '2009 reissue Letters on the Laws of Man's Nature and Development publisher', 'Martineau Atkinson 2009 republication', and check academic publishers, university presses, or specialty reprint publishers that may have reissued this historical work in 2009.

**Use Cases**:
- Library cataloging of historical texts to verify the exact 2009 reissue publisher for accurate OPAC metadata
- Rare book dealer inventory validation to confirm the printing house behind the 2009 republication before acquisition
- Digital humanities project metadata cleansing by identifying the correct 2009 edition publisher of Martineau–Atkinson letters
- Academic researcher citation audit for a journal article, ensuring the referenced 2009 reissue is attributed to the correct publisher
- Ebook aggregator licensing review to cross-check the 2009 reprint publisher before negotiating digital distribution rights
- Metadata librarian updating WorldCat and institutional repository entries with precise 2009 edition publisher details
- University press editorial fact-checking when preparing a critical introduction to Martineau’s work and citing the 2009 republication
- Book collector automated alert system to detect and log specialty reprint publishers (e.g., Nabu Press, Forgotten Books) for the 2009 edition

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import quote_plus, urljoin

print('=== FIXED: SEARCHING FOR 2009 REISSUE PUBLISHER OF MARTINEAU-ATKINSON LETTERS ===')
print('Title: Letters on the Laws of Man\'s Nature and Development')
print('Authors: Harriet Martineau and Henry George Atkinson')
print('Original: 1851')
print('Target: 2009 reissue publisher identification')
print('\n' + '='*100 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Headers for web requests
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

# Define comprehensive search queries for 2009 reissue
search_queries = [
    '"Letters on the Laws of Man\'s Nature and Development" 2009 publisher',
    'Martineau Atkinson "Letters Laws" 2009 reissue',
    'Harriet Martineau Henry Atkinson 2009 republication',
    '"Letters on the Laws of Man\'s Nature and Development" 2009 reprint',
    'Martineau Atkinson 2009 edition publisher',
    '"Laws of Man\'s Nature and Development" 2009 reissue',
    'Harriet Martineau 2009 Letters Laws publisher',
    'Henry George Atkinson 2009 reprint publisher',
    '"Letters on the Laws" Martineau Atkinson 2009',
    'Martineau Atkinson correspondence 2009 publisher'
]

print('=== STEP 1: CONDUCTING TARGETED PUBLISHER SEARCHES ===')
print(f'Total search queries: {len(search_queries)}')
print('\nSearch queries:')
for i, query in enumerate(search_queries, 1):
    print(f'  {i:2d}. {query}')

search_results = {}

# Function to perform search and analyze results - FIXED VARIABLE SCOPE
def perform_search(query, search_index):
    # Define search_base_url inside function to fix scope issue
    search_base_url = 'https://html.duckduckgo.com/html/'
    
    print(f'\n--- SEARCH {search_index}: {query} ---')
    try:
        params = {'q': query}
        response = requests.get(search_base_url, params=params, headers=headers, timeout=30)
        print(f'Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML for analysis
            filename = f'search_{search_index:02d}_{query.replace(" ", "_").replace("\'", "").replace('"', "")[:40]}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'Saved: {filepath}')
            
            # Parse for relevant results
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result links with publisher information
            result_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                
                # Filter for highly relevant results
                if href and text and len(text) > 15:
                    text_lower = text.lower()
                    relevance_score = 0
                    
                    # High-value terms for 2009 reissue identification
                    high_value_terms = [
                        ('2009', 3),
                        ('martineau', 2),
                        ('atkinson', 2),
                        ('letters', 1),
                        ('laws', 1),
                        ('nature', 1),
                        ('development', 1),
                        ('publisher', 2),
                        ('reissue', 2),
                        ('reprint', 2),
                        ('edition', 1),
                        ('republication', 2)
                    ]
                    
                    # Publisher-specific terms
                    publisher_terms = [
                        ('cambridge university press', 4),
                        ('oxford university press', 4),
                        ('harvard university press', 4),
                        ('yale university press', 4),
                        ('princeton university press', 4),
                        ('university of chicago press', 4),
                        ('routledge', 3),
                        ('palgrave', 3),
                        ('macmillan', 3),
                        ('springer', 3),
                        ('brill', 3),
                        ('ashgate', 3),
                        ('continuum', 3),
                        ('thoemmes', 3),
                        ('pickering', 3),
                        ('nabu press', 2),
                        ('kessinger', 2),
                        ('forgotten books', 2),
                        ('bibliolife', 2),
                        ('gale ecco', 2),
                        ('making of modern law', 2)
                    ]
                    
                    # Calculate relevance score
                    for term, score in high_value_terms + publisher_terms:
                        if term in text_lower:
                            relevance_score += score
                    
                    # Additional scoring for URL domains
                    if href:
                        href_lower = href.lower()
                        if any(domain in href_lower for domain in ['cambridge.org', 'oup.com', 'harvard.edu', 'yale.edu', 'routledge.com', 'palgrave.com']):
                            relevance_score += 3
                        elif any(domain in href_lower for domain in ['amazon.com', 'worldcat.org', 'goodreads.com', 'abebooks.com']):
                            relevance_score += 2
                    
                    if relevance_score >= 3:  # Only include highly relevant results
                        result_links.append({
                            'url': href,
                            'text': text[:300],  # Longer text for better analysis
                            'relevance_score': relevance_score
                        })
            
            # Sort by relevance score
            result_links.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            search_results[query] = {
                'html_file': filepath,
                'status_code': response.status_code,
                'relevant_links': result_links[:15],  # Top 15 most relevant
                'total_links_found': len(result_links)
            }
            
            print(f'Found {len(result_links)} highly relevant links')
            if result_links:
                print('Top results:')
                for i, link in enumerate(result_links[:5], 1):
                    print(f'  {i}. Score {link["relevance_score"]}: {link["text"][:120]}...')
                    print(f'     URL: {link["url"]}')
            
            time.sleep(2)  # Rate limiting
            return True
        else:
            print(f'Failed: HTTP {response.status_code}')
            return False
            
    except Exception as e:
        print(f'Error: {str(e)}')
        return False

# Perform all searches
print('\n=== EXECUTING SEARCHES ===')
successful_searches = 0

for i, query in enumerate(search_queries, 1):
    if perform_search(query, i):
        successful_searches += 1
    
    # Brief pause between searches
    if i < len(search_queries):
        time.sleep(1)

print(f'\n=== STEP 2: ANALYZING SEARCH RESULTS ===')
print(f'Successful searches: {successful_searches}/{len(search_queries)}')

# Compile and analyze all findings
high_priority_findings = []
all_publishers_mentioned = set()
publisher_frequency = {}

# Known academic and reprint publishers to watch for
known_publishers = [
    'Cambridge University Press', 'Oxford University Press', 'Harvard University Press',
    'Yale University Press', 'Princeton University Press', 'University of Chicago Press',
    'Routledge', 'Palgrave Macmillan', 'Springer', 'Brill', 'Ashgate', 'Continuum',
    'Thoemmes Press', 'Pickering & Chatto', 'Nabu Press', 'Kessinger Publishing',
    'Forgotten Books', 'BiblioLife', 'Gale ECCO', 'Making of Modern Law',
    'Elibron Classics', 'Palala Press', 'Wentworth Press', 'Franklin Classics'
]

print('\n--- ANALYZING ALL SEARCH RESULTS FOR PUBLISHER PATTERNS ---')

for query, results in search_results.items():
    print(f'\nQuery: "{query}"')
    print(f'  Relevant links: {results["total_links_found"]}')
    
    for link in results['relevant_links']:
        # Check for 2009 and publisher combinations
        text_lower = link['text'].lower()
        
        if '2009' in text_lower and any(pub.lower() in text_lower for pub in known_publishers):
            # This is a high-priority finding
            matching_publishers = [pub for pub in known_publishers if pub.lower() in text_lower]
            
            high_priority_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'score': link['relevance_score'],
                'publishers_mentioned': matching_publishers,
                'priority': 'HIGH - Contains 2009 + Publisher'
            })
            
            # Track publisher frequency
            for pub in matching_publishers:
                publisher_frequency[pub] = publisher_frequency.get(pub, 0) + 1
                all_publishers_mentioned.add(pub)
            
            print(f'  🎯 HIGH PRIORITY: {matching_publishers} mentioned with 2009')
        
        elif '2009' in text_lower:
            # Contains 2009 but may have publisher info we need to extract
            high_priority_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'score': link['relevance_score'],
                'publishers_mentioned': [],
                'priority': 'MEDIUM - Contains 2009'
            })
            
            print(f'  📍 MEDIUM: Contains 2009, checking for publisher info')
        
        # Track any publisher mentions regardless of year
        for pub in known_publishers:
            if pub.lower() in text_lower:
                all_publishers_mentioned.add(pub)
                publisher_frequency[pub] = publisher_frequency.get(pub, 0) + 1

print(f'\n=== STEP 3: PUBLISHER FREQUENCY ANALYSIS ===')
print(f'Total unique publishers mentioned: {len(all_publishers_mentioned)}')
print(f'High-priority findings (2009 + publisher): {len([f for f in high_priority_findings if f["priority"].startswith("HIGH")])}')

if publisher_frequency:
    print('\nPublisher mention frequency:')
    sorted_publishers = sorted(publisher_frequency.items(), key=lambda x: x[1], reverse=True)
    for pub, count in sorted_publishers:
        print(f'  {pub}: {count} mentions')
else:
    print('\nNo specific publishers identified in search results')

print(f'\n=== STEP 4: DETAILED ANALYSIS OF HIGH-PRIORITY FINDINGS ===')

if high_priority_findings:
    # Sort by priority and score
    high_priority_findings.sort(key=lambda x: (x['priority'] == 'HIGH - Contains 2009 + Publisher', x['score']), reverse=True)
    
    print(f'\nAnalyzing {len(high_priority_findings)} high-priority findings:')
    
    for i, finding in enumerate(high_priority_findings[:10], 1):  # Top 10 findings
        print(f'\n🔍 FINDING {i} - {finding["priority"]} (Score: {finding["score"]})')
        print(f'Query: {finding["query"]}')
        print(f'Publishers: {finding["publishers_mentioned"] if finding["publishers_mentioned"] else "None explicitly identified"}')
        print(f'URL: {finding["url"]}')
        print(f'Text: {finding["text"][:400]}...')
        print('-' * 120)
        
        # If this is a high-priority finding with a specific URL, we should investigate further
        if finding['priority'].startswith('HIGH') and finding['url']:
            print(f'  ⭐ RECOMMENDED FOR DETAILED INVESTIGATION: {finding["url"]}')
else:
    print('\n⚠ No high-priority findings identified')
    print('This suggests the 2009 reissue may be from a smaller or specialized publisher')

# Check for specific reprint/specialty publishers
print(f'\n=== STEP 5: CHECKING FOR SPECIALTY REPRINT PUBLISHERS ===')

specialty_publishers = [
    'Nabu Press', 'Kessinger Publishing', 'Forgotten Books', 'BiblioLife',
    'Palala Press', 'Wentworth Press', 'Franklin Classics', 'Elibron Classics',
    'Gale ECCO', 'Making of Modern Law', 'Thoemmes Press', 'Pickering & Chatto'
]

specialty_findings = []
for query, results in search_results.items():
    for link in results['relevant_links']:
        text_lower = link['text'].lower()
        
        for specialty_pub in specialty_publishers:
            if specialty_pub.lower() in text_lower:
                specialty_findings.append({
                    'publisher': specialty_pub,
                    'query': query,
                    'text': link['text'],
                    'url': link['url'],
                    'has_2009': '2009' in text_lower
                })

if specialty_findings:
    print(f'Found {len(specialty_findings)} specialty publisher mentions:')
    
    # Group by publisher
    by_publisher = {}
    for finding in specialty_findings:
        pub = finding['publisher']
        if pub not in by_publisher:
            by_publisher[pub] = []
        by_publisher[pub].append(finding)
    
    for pub, findings in by_publisher.items():
        print(f'\n{pub}: {len(findings)} mentions')
        for finding in findings[:2]:  # Show top 2 per publisher
            status = '✓ WITH 2009' if finding['has_2009'] else '- without 2009'
            print(f'  {status}: {finding["text"][:150]}...')
            print(f'    URL: {finding["url"]}')
else:
    print('No specialty reprint publishers clearly identified')

# Additional search for specific reprint publisher patterns
print(f'\n=== STEP 6: ANALYZING FOR REPRINT PUBLISHER PATTERNS ===')

# Look for common reprint publisher indicators in all search results
reprint_indicators = [
    'reprint', 'reprinted', 'reproduction', 'facsimile', 'digitally printed',
    'print on demand', 'pod', 'classic reprint', 'historical reproduction',
    'nabu', 'kessinger', 'forgotten books', 'bibliolife', 'palala',
    'wentworth', 'franklin classics', 'elibron', 'gale ecco'
]

reprint_pattern_findings = []
for query, results in search_results.items():
    for link in results['relevant_links']:
        text_lower = link['text'].lower()
        
        # Check for reprint indicators
        found_indicators = []
        for indicator in reprint_indicators:
            if indicator in text_lower:
                found_indicators.append(indicator)
        
        if found_indicators and '2009' in text_lower:
            reprint_pattern_findings.append({
                'query': query,
                'text': link['text'],
                'url': link['url'],
                'indicators': found_indicators,
                'score': link['relevance_score']
            })

if reprint_pattern_findings:
    print(f'Found {len(reprint_pattern_findings)} results with 2009 + reprint indicators:')
    
    # Sort by number of indicators and score
    reprint_pattern_findings.sort(key=lambda x: (len(x['indicators']), x['score']), reverse=True)
    
    for i, finding in enumerate(reprint_pattern_findings[:5], 1):
        print(f'\n🎯 REPRINT PATTERN {i}:')
        print(f'Indicators: {finding["indicators"]}')
        print(f'Score: {finding["score"]}')
        print(f'URL: {finding["url"]}')
        print(f'Text: {finding["text"][:200]}...')
        print('-' * 80)
else:
    print('No clear reprint patterns with 2009 found')

# Save comprehensive analysis
analysis_results = {
    'search_objective': 'Identify 2009 reissue publisher for Martineau-Atkinson Letters',
    'book_details': {
        'title': 'Letters on the Laws of Man\'s Nature and Development',
        'authors': ['Harriet Martineau', 'Henry George Atkinson'],
        'original_year': 1851,
        'target_reissue_year': 2009
    },
    'search_summary': {
        'total_queries': len(search_queries),
        'successful_searches': successful_searches,
        'total_relevant_links': sum(len(r['relevant_links']) for r in search_results.values())
    },
    'publisher_analysis': {
        'publishers_mentioned': list(all_publishers_mentioned),
        'publisher_frequency': publisher_frequency,
        'high_priority_findings_count': len([f for f in high_priority_findings if f['priority'].startswith('HIGH')]),
        'specialty_publisher_findings': len(specialty_findings),
        'reprint_pattern_findings': len(reprint_pattern_findings)
    },
    'high_priority_findings': high_priority_findings[:10],  # Top 10 findings
    'specialty_findings': specialty_findings,
    'reprint_pattern_findings': reprint_pattern_findings[:5],  # Top 5 reprint patterns
    'search_queries_used': search_queries,
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

analysis_file = 'workspace/martineau_atkinson_2009_publisher_analysis_fixed.json'
with open(analysis_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

print(f'\n*** PUBLISHER SEARCH ANALYSIS COMPLETE ***')
print(f'✓ Conducted {successful_searches} successful searches')
print(f'✓ Analyzed {sum(len(r["relevant_links"]) for r in search_results.values())} relevant results')
print(f'✓ Identified {len(all_publishers_mentioned)} unique publishers mentioned')
print(f'✓ Found {len(high_priority_findings)} high-priority findings')
print(f'✓ Found {len(reprint_pattern_findings)} reprint pattern matches')
print(f'✓ Comprehensive analysis saved to: {analysis_file}')

# Summary of most promising leads
if high_priority_findings:
    top_finding = high_priority_findings[0]
    print(f'\n🎯 MOST PROMISING LEAD:')
    print(f'Priority: {top_finding["priority"]}')
    print(f'Publishers mentioned: {top_finding["publishers_mentioned"]}')
    print(f'Score: {top_finding["score"]}')
    print(f'URL: {top_finding["url"]}')
elif reprint_pattern_findings:
    top_reprint = reprint_pattern_findings[0]
    print(f'\n🎯 MOST PROMISING REPRINT LEAD:')
    print(f'Reprint indicators: {top_reprint["indicators"]}')
    print(f'Score: {top_reprint["score"]}')
    print(f'URL: {top_reprint["url"]}')
else:
    print(f'\n⚠ No definitive 2009 publisher identified in initial search')
    print('Recommend manual investigation of saved search results')

print('\n=== NEXT STEPS ===')
print('1. Review high-priority findings for definitive publisher identification')
print('2. Investigate URLs from top-scoring results')
print('3. Check specialty reprint publishers for 2009 editions')
print('4. Cross-reference with library catalogs (WorldCat, etc.)')
print('5. Examine reprint pattern findings for publisher clues')
```

## Development History
*(This section will be updated as development progresses)*

