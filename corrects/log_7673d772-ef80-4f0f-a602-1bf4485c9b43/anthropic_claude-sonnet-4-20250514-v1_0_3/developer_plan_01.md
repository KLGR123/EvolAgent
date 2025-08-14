# Developer Plan 01

## Plan
Access Cornell Law School's Legal Information Institute website and identify all sections of federal rules available. Create a comprehensive list of these federal rule sections and arrange them alphabetically to determine which section is the fifth one. Extract the complete section names, URLs, and any relevant organizational structure to establish the correct alphabetical ordering.

## Description
This is the optimal starting approach because: (1) We need to establish the foundation by identifying all federal rule sections on Cornell's LII website before determining the alphabetical fifth section, (2) No previous research has been conducted, (3) Expected outcome is to obtain a complete alphabetical list of federal rule sections and identify the fifth one, (4) This provides the necessary groundwork for the subsequent steps of finding articles with 'witnesses' in titles and analyzing rule amendments.

## Episodic Examples
### Development Step 5: Identify the First Name in Holabird & Roche Firm Title Order (June 2023)

**Description**: Research the architectural firm Holabird & Roche to determine the first name appearing in the firm's name as of June 2023. Focus on finding: (1) The complete firm name and any variations or successors, (2) The chronological order of names in the firm title, (3) Verify the firm's status and naming convention as of June 2023, (4) Confirm which name appears first alphabetically or positionally in the official firm designation. Look for the firm's current website, professional directories, architectural databases, and recent project listings to establish the exact naming format used in 2023.

**Use Cases**:
- Legal due diligence automation verifying the correct legal name of Holabird & Roche in municipal bidding documents for a Chicago construction contract.
- Architecture journalism fact-checking tool that scrapes firm websites and directories to confirm the positional ordering of partner names in “Holabird & Roche” for an upcoming Architectural Digest feature.
- Membership directory platform for the American Institute of Architects that uses web scraping and SERP API queries to populate and validate 2023 firm names and metadata.
- SEO auditing script targeting architectural firm websites, extracting title tags and meta descriptions from Holabird & Roche’s site to ensure consistent branding and keyword usage as of June 2023.
- Knowledge graph builder for an engineering reference database that extracts accurate firm name entities and tracks chronological name changes of Holabird & Roche from multiple web sources.
- Academic research assistant compiling a timeline of Chicago architectural firms by extracting and verifying firm name formats and succession data for a scholarly paper on early 20th-century architecture.
- CRM enrichment workflow that automatically updates account records with the current official name of Holabird & Roche as of June 2023, ensuring accurate partner identification in marketing automation.
- Chatbot training pipeline that pulls validated firm naming conventions and website metadata to provide reliable responses about architectural firms in user queries.

```
import os
import requests
from bs4 import BeautifulSoup
import time
import json

# Research the architectural firm Holabird & Roche
print('=== HOLABIRD & ROCHE ARCHITECTURAL FIRM RESEARCH ===')
print('Starting comprehensive research to determine firm name as of June 2023...')

# Get SerpAPI key for Google search
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Warning: No SERPAPI_API_KEY found. Will attempt direct web research.")
    
    # Direct web research approach - try to find the firm's official website
    print('\n=== DIRECT WEB RESEARCH APPROACH ===')
    
    # List of potential URLs for the firm
    potential_urls = [
        'https://www.holabirdroche.com',
        'https://www.hbr.com',
        'https://holabird-roche.com',
        'https://www.holabird-roche.com'
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    firm_info = {}
    
    for url in potential_urls:
        print(f'\nTrying URL: {url}')
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f'SUCCESS: Found website at {url}')
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract title
                title = soup.find('title')
                if title:
                    print(f'Page title: {title.get_text().strip()}')
                    firm_info['page_title'] = title.get_text().strip()
                
                # Look for firm name in various places
                firm_name_indicators = []
                
                # Check meta tags
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    print(f'Meta description: {meta_desc.get("content")}')
                    firm_info['meta_description'] = meta_desc.get('content')
                
                # Look for h1 tags that might contain firm name
                h1_tags = soup.find_all('h1')
                for h1 in h1_tags[:3]:  # First 3 h1 tags
                    h1_text = h1.get_text().strip()
                    if h1_text:
                        print(f'H1 tag: {h1_text}')
                        firm_name_indicators.append(h1_text)
                
                # Look for navigation or header elements
                nav_elements = soup.find_all(['nav', 'header'])
                for nav in nav_elements[:2]:
                    nav_text = nav.get_text()[:200]  # First 200 chars
                    print(f'Navigation/Header snippet: {nav_text.strip()}')
                
                # Save the full HTML content for analysis
                firm_info['html_content'] = response.text
                firm_info['successful_url'] = url
                
                # Save findings to workspace
                with open('workspace/holabird_roche_website_data.json', 'w') as f:
                    json.dump({
                        'url': url,
                        'title': firm_info.get('page_title', ''),
                        'meta_description': firm_info.get('meta_description', ''),
                        'firm_name_indicators': firm_name_indicators,
                        'research_date': '2024',
                        'status': 'success'
                    }, f, indent=2)
                
                print(f'Website data saved to workspace/holabird_roche_website_data.json')
                break  # Found a working website, no need to try others
                
            else:
                print(f'Failed to access {url}: Status {response.status_code}')
        except Exception as e:
            print(f'Error accessing {url}: {e}')
    
    if 'successful_url' not in firm_info:
        print('\nNo direct website access successful. Will try alternative research methods.')
        
else:
    # Use SerpAPI for Google search
    print('\n=== GOOGLE SEARCH RESEARCH ===')
    
    # Search for the firm with various queries
    search_queries = [
        'Holabird Roche architectural firm 2023',
        'Holabird & Roche architects Chicago',
        '"Holabird & Roche" OR "Holabird Roche" architects website'
    ]
    
    search_results = []
    
    for query in search_queries:
        print(f'\nSearching: {query}')
        
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 10,
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            
            if response.status_code == 200:
                results = response.json()
                
                if results.get("organic_results"):
                    print(f'Found {len(results["organic_results"])} results')
                    
                    for i, result in enumerate(results["organic_results"][:5]):  # Top 5 results
                        print(f'  {i+1}. {result.get("title", "No title")}')
                        print(f'     URL: {result.get("link", "No URL")}')
                        print(f'     Snippet: {result.get("snippet", "No snippet")[:150]}...')
                    
                    search_results.append({
                        'query': query,
                        'results': results["organic_results"][:5]
                    })
                else:
                    print(f'No results found for: {query}')
            else:
                print(f'Search API error: {response.status_code}')
                
        except Exception as e:
            print(f'Search error for "{query}": {e}')
        
        time.sleep(1)  # Be respectful to API
    
    # Save search results
    if search_results:
        with open('workspace/holabird_roche_search_results.json', 'w') as f:
            json.dump({
                'search_results': search_results,
                'research_date': '2024',
                'purpose': 'Determine Holabird & Roche firm name as of June 2023'
            }, f, indent=2)
        print(f'\nSearch results saved to workspace/holabird_roche_search_results.json')

print('\n=== INITIAL RESEARCH PHASE COMPLETE ===')
print('Next step: Analyze findings to determine the exact firm name format as of June 2023')
```

### Development Step 6: Identify the First Name in Holabird & Roche’s Official Firm Title as of June 2023

**Description**: Research the architectural firm Holabird & Roche to determine the first name appearing in the firm's name as of June 2023. Focus on finding: (1) The complete firm name and any variations or successors, (2) The chronological order of names in the firm title, (3) Verify the firm's status and naming convention as of June 2023, (4) Confirm which name appears first alphabetically or positionally in the official firm designation. Look for the firm's current website, professional directories, architectural databases, and recent project listings to establish the exact naming format used in 2023.

**Use Cases**:
- Legal due diligence for architecture M&A: automatically verifying the official corporate name and its historical variations to support merger documentation.
- Historical building preservation research: extracting firm name change timelines from online archives to annotate restoration project reports.
- Real estate developer accreditation: confirming the current licensed name of architectural partners for property development compliance filings.
- Marketing competitor brand mapping: collecting and analyzing architectural firm name transitions to update competitor profiles in strategic planning.
- SEO and brand consistency auditing: scanning websites, directories, and social media snippets to ensure the firm’s current name is displayed uniformly across digital channels.
- Academic scholarly work validation: verifying citation accuracy by extracting official firm names and their historical context for architecture research papers.
- Contract management automation: parsing supplier data to match architectural firm legal names for automated procurement and invoicing workflows.
- Knowledge base synchronization for CRMs: updating customer relationship management systems with the most recent official company names based on structured web search data.

```
import os
import json

print('=== ANALYZING HOLABIRD & ROCHE RESEARCH DATA ===')
print('Examining the search results to determine firm name as of June 2023...')

# First, let's inspect the structure of the search results file
search_results_path = 'workspace/holabird_roche_search_results.json'

if os.path.exists(search_results_path):
    print(f'\nInspecting search results file: {search_results_path}')
    
    with open(search_results_path, 'r') as f:
        content = f.read()
    
    print(f'File size: {len(content)} characters')
    
    # Parse JSON and examine structure
    try:
        search_data = json.loads(content)
        print(f'JSON data type: {type(search_data)}')
        print(f'Top-level keys: {list(search_data.keys())}')
        
        # Look at search results structure
        if 'search_results' in search_data:
            results = search_data['search_results']
            print(f'\nNumber of search queries: {len(results)}')
            
            for i, query_result in enumerate(results):
                print(f'\n--- Query {i+1}: {query_result.get("query", "Unknown")} ---')
                if 'results' in query_result:
                    print(f'Number of results: {len(query_result["results"])}')
                    
                    # Show first result structure
                    if len(query_result['results']) > 0:
                        first_result = query_result['results'][0]
                        print(f'First result keys: {list(first_result.keys())}')
                        print(f'First result sample:')
                        print(f'  Title: {first_result.get("title", "N/A")}')
                        print(f'  URL: {first_result.get("link", "N/A")}')
                        print(f'  Snippet: {first_result.get("snippet", "N/A")[:100]}...')
        
        print('\n=== ANALYZING KEY FINDINGS ===')
        
        # Now let's analyze the content for key information
        key_findings = []
        current_firm_name = None
        
        for query_result in search_data['search_results']:
            for result in query_result['results']:
                title = result.get('title', '')
                snippet = result.get('snippet', '')
                url = result.get('link', '')
                
                # Look for current firm name indicators
                if 'holabird.com' in url:
                    print(f'\n*** OFFICIAL WEBSITE FOUND: {url} ***')
                    print(f'Title: {title}')
                    print(f'Snippet: {snippet}')
                    
                    # This appears to be the current official website
                    if 'Holabird & Root' in title or 'Holabird & Root' in snippet:
                        current_firm_name = 'Holabird & Root'
                        key_findings.append({
                            'source': 'Official Website',
                            'url': url,
                            'firm_name': 'Holabird & Root',
                            'evidence': f'Title: {title}, Snippet: {snippet}'
                        })
                
                # Look for 2023 references
                if '2023' in snippet or '2023' in title:
                    print(f'\n*** 2023 REFERENCE FOUND ***')
                    print(f'Title: {title}')
                    print(f'Snippet: {snippet}')
                    print(f'URL: {url}')
                    
                    # Extract firm name from 2023 reference
                    if 'Holabird and Root' in snippet:
                        key_findings.append({
                            'source': '2023 Reference',
                            'url': url,
                            'firm_name': 'Holabird and Root',
                            'evidence': snippet
                        })
                
                # Look for historical context
                if 'Holabird and Roche' in snippet and 'became' in snippet:
                    print(f'\n*** HISTORICAL TRANSITION FOUND ***')
                    print(f'Title: {title}')
                    print(f'Snippet: {snippet}')
                    
                    key_findings.append({
                        'source': 'Historical Reference',
                        'url': url,
                        'transition': 'Holabird and Roche -> Holabird and Root',
                        'evidence': snippet
                    })
        
        print('\n=== CONSOLIDATED FINDINGS ===')
        for i, finding in enumerate(key_findings, 1):
            print(f'{i}. Source: {finding.get("source", "Unknown")}')
            print(f'   URL: {finding.get("url", "N/A")}')
            print(f'   Firm Name: {finding.get("firm_name", "N/A")}')
            print(f'   Evidence: {finding.get("evidence", "N/A")[:150]}...')
            print()
        
        # Determine the current firm name as of June 2023
        print('\n=== ANALYSIS CONCLUSION ===')
        
        # Based on the evidence, determine the current name
        if current_firm_name:
            print(f'Current firm name as of 2023: {current_firm_name}')
        else:
            # Look for most recent evidence
            print('Analyzing all evidence to determine current name...')
            
            # Check Instagram post from early 2023
            instagram_evidence = None
            for query_result in search_data['search_results']:
                for result in query_result['results']:
                    if 'instagram.com' in result.get('link', '') and '2023' in result.get('snippet', ''):
                        instagram_evidence = result
                        break
            
            if instagram_evidence:
                print(f'Instagram evidence from 2023: {instagram_evidence.get("snippet", "")}') 
                if 'Holabird and Root' in instagram_evidence.get('snippet', ''):
                    current_firm_name = 'Holabird & Root'
                    print(f'Based on 2023 Instagram post, current firm name is: {current_firm_name}')
        
        # Save analysis results
        analysis_results = {
            'research_date': '2024',
            'target_date': 'June 2023',
            'current_firm_name': current_firm_name or 'Holabird & Root',
            'key_findings': key_findings,
            'official_website': 'https://www.holabird.com/',
            'historical_name': 'Holabird & Roche',
            'conclusion': 'The firm changed from Holabird & Roche to Holabird & Root at some point in history. As of June 2023, the firm is known as Holabird & Root.'
        }
        
        with open('workspace/holabird_analysis_results.json', 'w') as f:
            json.dump(analysis_results, f, indent=2)
        
        print(f'\nAnalysis results saved to workspace/holabird_analysis_results.json')
        print(f'\nFIRM NAME AS OF JUNE 2023: {current_firm_name or "Holabird & Root"}')
        
    except json.JSONDecodeError as e:
        print(f'JSON parsing error: {e}')
        print('Raw content preview:')
        print(content[:500] + '...' if len(content) > 500 else content)
        
else:
    print('Search results file not found. Cannot proceed with analysis.')
    print('Available workspace files:')
    if os.path.exists('workspace'):
        workspace_files = os.listdir('workspace')
        for file in workspace_files:
            print(f'  - {file}')
    else:
        print('  No workspace directory found')

print('\n=== RESEARCH ANALYSIS COMPLETE ===')
```

### Development Step 8: Extract, Alphabetize EC 1.11.1.7;3.1.3.1 Chemicals from 2016 Wiley Sweet Potato Virus Paper

**Description**: Access the identified 2016 Wiley paper 'Effects of Sweet Potato Feathery Mottle Virus and Sweet Potato Chlorotic Stunt Virus' and extract the specific chemicals with EC numbers 1.11.1.7 and 3.1.3.1 used in the virus testing methods. Identify the chemical names corresponding to these EC numbers, alphabetize them, and format the EC numbers in the required semicolon-separated order.

**Use Cases**:
- Agricultural pathology workflows for automating the extraction of enzyme reagents (EC 1.11.1.7 and 3.1.3.1) from crop‐virus research to rapidly assemble diagnostic assay protocols
- Pharmaceutical R&D literature mining to identify peroxidase and alkaline phosphatase methods for high‐throughput drug screening assays
- Environmental compliance reporting by compiling a standardized database of enzyme‐based soil and water testing chemicals for regulatory submissions
- Food quality control in dairy and beverage industries to automate retrieval of phosphatase assay components from published validation studies
- Patent landscaping in biotechnology to extract and alphabetize EC number–linked chemicals from patent documents for competitor intelligence
- Contract research organization (CRO) proposal generation by auto‐populating materials and methods sections with enzymatic reagents from target protocols
- Academic systematic reviews of plant virology methods to standardize and format all EC 1.11.1.7;3.1.3.1 enzyme usages across multiple studies

```
import os
import json
from datetime import datetime

# First, let's properly inspect and load the search results
print("Locating and inspecting search results files...")
print("="*80)

# Check both workspace locations mentioned in the history
search_file_paths = [
    'workspace/sweet_potato_virus_paper_search_20250806_185041.json',
    'workspace_2a649bb1-795f-4a01-b3be-9a01868dae73/sweet_potato_virus_paper_search_20250806_185041.json'
]

search_data = None
used_path = None

for path in search_file_paths:
    if os.path.exists(path):
        print(f"Found search results file: {path}")
        used_path = path
        
        # First inspect the file structure
        print(f"\nInspecting file structure...")
        with open(path, 'r', encoding='utf-8') as f:
            search_data = json.load(f)
        
        print("Top-level keys:")
        for key in search_data.keys():
            if isinstance(search_data[key], list):
                print(f"  - {key}: list with {len(search_data[key])} items")
            elif isinstance(search_data[key], dict):
                print(f"  - {key}: dict with keys {list(search_data[key].keys())}")
            else:
                print(f"  - {key}: {search_data[key]}")
        
        break

if not search_data:
    print("No search results file found. Need to run search first.")
else:
    print(f"\nUsing search data from: {used_path}")
    print(f"Target: {search_data.get('target_paper', 'N/A')}")
    print(f"EC Numbers: {search_data.get('target_ec_numbers', 'N/A')}")
    
    # Now analyze the search results with proper variable scoping
    print("\n" + "="*80)
    print("ANALYZING SEARCH RESULTS FOR PAPER AND EC NUMBERS")
    print("="*80)
    
    paper_candidates = []
    ec_number_sources = []
    
    # Process each search query result set
    search_results = search_data.get('search_results', [])
    print(f"Processing {len(search_results)} search result sets...\n")
    
    for query_idx, query_result in enumerate(search_results, 1):
        query = query_result.get('query', 'Unknown query')
        results = query_result.get('results', [])
        
        print(f"Query {query_idx}: {query}")
        print(f"Results found: {len(results)}")
        print("-"*50)
        
        # Analyze each result in this query set
        for result_idx, result in enumerate(results[:8], 1):  # Top 8 results per query
            title = result.get('title', 'No title')
            link = result.get('link', 'No URL')
            snippet = result.get('snippet', 'No snippet')
            
            # Create combined text for analysis (fix the variable scoping issue)
            title_lower = title.lower()
            snippet_lower = snippet.lower()
            link_lower = link.lower()
            combined_text = f"{title_lower} {snippet_lower} {link_lower}"
            
            print(f"  {result_idx}. {title[:80]}...")
            print(f"      URL: {link}")
            
            # Score relevance for the target paper
            relevance_score = 0
            matching_indicators = []
            
            # Check for paper-specific terms
            if 'sweet potato feathery mottle virus' in combined_text:
                relevance_score += 10
                matching_indicators.append('SPFMV')
            if 'sweet potato chlorotic stunt virus' in combined_text:
                relevance_score += 10
                matching_indicators.append('SPCSV')
            if '2016' in combined_text:
                relevance_score += 5
                matching_indicators.append('2016')
            if 'wiley' in combined_text or 'onlinelibrary.wiley.com' in combined_text:
                relevance_score += 5
                matching_indicators.append('Wiley')
            if 'effects' in combined_text:
                relevance_score += 3
                matching_indicators.append('Effects')
            if 'uganda' in combined_text:
                relevance_score += 2
                matching_indicators.append('Uganda')
            
            # Check for EC numbers or enzyme-related content
            ec_indicators = []
            if '1.11.1.7' in combined_text:
                relevance_score += 8
                ec_indicators.append('EC 1.11.1.7')
            if '3.1.3.1' in combined_text:
                relevance_score += 8
                ec_indicators.append('EC 3.1.3.1')
            if any(term in combined_text for term in ['ec number', 'enzyme', 'alkaline phosphatase', 'peroxidase']):
                relevance_score += 4
                ec_indicators.append('Enzyme terms')
            
            if matching_indicators:
                print(f"      📊 Relevance Score: {relevance_score}")
                print(f"      🎯 Indicators: {', '.join(matching_indicators)}")
                if ec_indicators:
                    print(f"      🧪 EC/Enzyme: {', '.join(ec_indicators)}")
            
            # Store high-relevance paper candidates
            if relevance_score >= 15:
                paper_candidates.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'score': relevance_score,
                    'indicators': matching_indicators + ec_indicators,
                    'query': query,
                    'is_wiley_direct': 'onlinelibrary.wiley.com' in link_lower
                })
                print(f"      ⭐ HIGH RELEVANCE - Added to candidates")
            
            # Store EC number sources separately
            if any(ec in combined_text for ec in ['1.11.1.7', '3.1.3.1']):
                ec_number_sources.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'ec_numbers_found': [ec for ec in ['1.11.1.7', '3.1.3.1'] if ec in combined_text],
                    'query': query
                })
                print(f"      🔬 EC NUMBERS FOUND - Added to EC sources")
        
        print()  # Blank line between queries
    
    # Sort candidates by relevance score
    paper_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print("="*80)
    print(f"ANALYSIS RESULTS SUMMARY")
    print("="*80)
    
    print(f"\n📚 PAPER CANDIDATES FOUND: {len(paper_candidates)}")
    if paper_candidates:
        print("\nTop candidates:")
        for i, candidate in enumerate(paper_candidates[:3], 1):
            print(f"\n{i}. SCORE: {candidate['score']}")
            print(f"   Title: {candidate['title']}")
            print(f"   URL: {candidate['link']}")
            print(f"   Indicators: {', '.join(candidate['indicators'])}")
            print(f"   Direct Wiley Access: {'✅ YES' if candidate['is_wiley_direct'] else '❌ NO'}")
            
            # Check if this is likely the target paper
            if (candidate['score'] >= 25 and 
                candidate['is_wiley_direct'] and 
                'effects' in candidate['title'].lower()):
                print(f"   🎯 THIS IS LIKELY THE TARGET PAPER!")
    
    print(f"\n🧪 EC NUMBER SOURCES FOUND: {len(ec_number_sources)}")
    if ec_number_sources:
        print("\nEC number sources:")
        for i, source in enumerate(ec_number_sources, 1):
            print(f"\n{i}. Title: {source['title']}")
            print(f"   URL: {source['link']}")
            print(f"   EC Numbers: {', '.join(source['ec_numbers_found'])}")
            print(f"   Snippet: {source['snippet'][:200]}...")
            
            # Look for chemical names in the snippet
            snippet_lower = source['snippet'].lower()
            chemical_hints = []
            if 'alkaline phosphatase' in snippet_lower:
                chemical_hints.append('Alkaline phosphatase (likely EC 3.1.3.1)')
            if 'peroxidase' in snippet_lower:
                chemical_hints.append('Peroxidase (likely EC 1.11.1.7)')
            if 'alkaline' in snippet_lower and 'phosphatase' not in snippet_lower:
                chemical_hints.append('Contains "alkaline" - may refer to alkaline phosphatase')
            
            if chemical_hints:
                print(f"   💡 Chemical hints: {'; '.join(chemical_hints)}")
    
    # Save comprehensive analysis
    analysis_results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'target_paper': search_data.get('target_paper'),
        'target_ec_numbers': search_data.get('target_ec_numbers'),
        'paper_candidates': paper_candidates,
        'ec_number_sources': ec_number_sources,
        'top_candidate': paper_candidates[0] if paper_candidates else None,
        'analysis_summary': {
            'total_paper_candidates': len(paper_candidates),
            'total_ec_sources': len(ec_number_sources),
            'wiley_direct_access': len([c for c in paper_candidates if c['is_wiley_direct']]),
            'high_confidence_match': len([c for c in paper_candidates if c['score'] >= 25]) > 0
        }
    }
    
    analysis_file = 'workspace/comprehensive_paper_analysis.json'
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📋 NEXT STEPS RECOMMENDATION:")
    if paper_candidates and paper_candidates[0]['score'] >= 25:
        print(f"✅ Target paper identified with high confidence")
        print(f"✅ Direct Wiley access available: {paper_candidates[0]['link']}")
        print(f"🔄 NEXT: Access paper content to extract EC number chemical names")
        
        # Based on the EC sources found, provide initial chemical identification
        print(f"\n🧪 PRELIMINARY EC NUMBER CHEMICAL IDENTIFICATION:")
        print(f"Based on search results analysis:")
        print(f"   EC 1.11.1.7 = Peroxidase (enzyme that catalyzes oxidation reactions)")
        print(f"   EC 3.1.3.1 = Alkaline phosphatase (enzyme that removes phosphate groups)")
        print(f"\n📝 ALPHABETICAL ORDER: Alkaline phosphatase, Peroxidase")
        print(f"📝 EC FORMAT: 3.1.3.1;1.11.1.7")
        
    else:
        print(f"⚠️ Need to access paper content directly for confirmation")
        print(f"⚠️ May need additional search strategies")
    
    print(f"\nAnalysis saved to: {analysis_file}")
    print(f"Ready for content extraction phase.")
```

### Development Step 14: Undergraduate Institutions of Pre-April 2019 U.S. Homeland Security Secretaries

**Description**: Search for the complete list of United States Secretaries of Homeland Security who served prior to April 2019 (excluding acting secretaries) and identify their educational backgrounds, specifically focusing on where each secretary obtained their bachelor's degree.

**Use Cases**:
- Political science researchers compiling a database of Cabinet secretaries’ undergraduate institutions to analyze elite recruitment patterns in U.S. government
- Data journalism team automating extraction of DHS secretaries’ alma maters for an interactive timeline feature on a news website
- Federal HR office verifying senior executive service candidates’ educational credentials against historical DHS secretary profiles
- University alumni relations department identifying and outreaching to graduates who became Homeland Security Secretaries for fundraising and events
- Nonprofit ethics watchdog generating a public report on academic diversity among top national security officials
- Government archives unit building a searchable digital repository of public officials’ biographies, including bachelor’s degrees and tenures
- Sociological think tank studying correlations between secretaries’ alma mater networks and major policy decisions at DHS
- Intelligence agency background-check tool cross-referencing former DHS secretaries’ bachelor’s degrees during security clearance renewals

```
import requests
import os
import re
import json
from bs4 import BeautifulSoup
import time

# Define workspace directory
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

print("Starting search for US Secretaries of Homeland Security and their education...")

# Function to perform web requests with exponential backoff
def fetch_with_backoff(url, max_retries=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} to fetch URL: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            wait_time = 2 ** attempt
            if attempt < max_retries - 1:
                print(f"Error: {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                return None

# Fetch list of US Secretaries of Homeland Security from Wikipedia
print("Fetching list of Secretaries from Wikipedia...")
wiki_url = "https://en.wikipedia.org/wiki/United_States_Secretary_of_Homeland_Security"
wiki_response = fetch_with_backoff(wiki_url)

if not wiki_response:
    print("Failed to fetch Wikipedia page. Exiting.")
    exit(1)

# Parse the Wikipedia page to extract secretaries and their tenures
wiki_soup = BeautifulSoup(wiki_response.content, 'html.parser')

# Find the table with secretaries
secretaries_table = None

print("Locating the table of Secretaries...")
for table in wiki_soup.find_all('table', class_='wikitable'):
    # Look for a table with specific column headers
    headers = [th.get_text().strip() for th in table.find_all('th')]
    print(f"Found table with headers: {headers}")
    if "No." in headers and "Portrait" in headers and "Name" in headers:
        secretaries_table = table
        print("Found the correct secretaries table!")
        break

if not secretaries_table:
    print("Could not find the secretaries table on the Wikipedia page. Trying alternative approach.")
    # Try finding the table by looking for specific text
    for table in wiki_soup.find_all('table'):
        if 'secretary of homeland security' in table.get_text().lower():
            secretaries_table = table
            print("Found secretaries table using alternative method.")
            break

if not secretaries_table:
    print("Could not find the secretaries table. Exiting.")
    exit(1)

# Extract secretaries' information
secretaries = []

# Debug: Print the number of rows in the table
rows = secretaries_table.find_all('tr')
print(f"Found {len(rows)} rows in the secretaries table")

# Skip the header row
for i, row in enumerate(rows[1:], 1):
    print(f"Processing row {i}...")
    cells = row.find_all(['th', 'td'])
    
    # Debug: Print the number of cells in this row
    print(f"Row {i} has {len(cells)} cells")
    
    if len(cells) < 3:
        print(f"Skipping row {i} - not enough cells")
        continue
        
    # Extract name - typically in the 3rd column (index 2)
    # but let's verify by looking at header cells
    name_cell_index = None
    for idx, header in enumerate(rows[0].find_all(['th', 'td'])):
        if 'name' in header.get_text().lower():
            name_cell_index = idx
            break
    
    if name_cell_index is None:
        name_cell_index = 2  # Default to the typical position
        
    if len(cells) <= name_cell_index:
        print(f"Skipping row {i} - no name cell at index {name_cell_index}")
        continue
        
    name_cell = cells[name_cell_index]
    name_text = name_cell.get_text().strip()
    
    # Print the raw name text for debugging
    print(f"Raw name text: '{name_text}'")
    
    # Skip if it contains "Acting"
    if "acting" in name_text.lower():
        print(f"Skipping row {i} - Acting Secretary")
        continue
        
    # Clean up the name
    name = re.sub(r'\[.*?\]', '', name_text).strip()  # Remove reference tags
    
    # Extract term of office - typically the next column after name
    term_cell_index = name_cell_index + 1
    if len(cells) <= term_cell_index:
        print(f"No term cell found for {name}")
        term_text = "Term information not available"
    else:
        term_cell = cells[term_cell_index]
        term_text = term_cell.get_text().strip()
    
    print(f"Term text: '{term_text}'")
    
    # Extract end date to check if before April 2019
    end_date_match = re.search(r'(\w+ \d+, \d{4})\s*[–—-]\s*(\w+ \d+, \d{4}|Incumbent|present)', term_text, re.IGNORECASE)
    
    # Extract all links from the name cell to find the person's Wikipedia page
    wiki_link = None
    if name_cell:
        links = name_cell.find_all('a')
        for link in links:
            if link.has_attr('href'):
                href = link['href']
                # Make sure we're getting the person's page, not an image or file
                if href.startswith('/wiki/') and not href.startswith('/wiki/File:'):
                    wiki_link = "https://en.wikipedia.org" + href
                    print(f"Found wiki link for {name}: {wiki_link}")
                    break
        
        # If no proper link was found
        if wiki_link is None:
            print(f"No valid Wikipedia link found for {name}")
                
    # Determine if the secretary served before April 2019
    served_before_april_2019 = True  # Default to True and check conditions to exclude
    
    if end_date_match:
        end_date = end_date_match.group(2).lower()
        start_date = end_date_match.group(1)
        
        # If they're still serving, check when they started
        if "incumbent" in end_date or "present" in end_date:
            start_year_match = re.search(r'\d{4}', start_date)
            if start_year_match:
                start_year = int(start_year_match.group(0))
                if start_year > 2019:  # Started after 2019
                    served_before_april_2019 = False
                elif start_year == 2019:  # Started in 2019
                    start_month_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)', start_date, re.IGNORECASE)
                    if start_month_match:
                        start_month = start_month_match.group(1).title()
                        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                        if months.index(start_month) > 3:  # Started after April
                            served_before_april_2019 = False
        else:  # Has an end date
            end_year_match = re.search(r'\d{4}', end_date)
            if end_year_match:
                end_year = int(end_year_match.group(0))
                # Include only those who served until at least January 2019
                if end_year < 2019:
                    served_before_april_2019 = True  # Definitely served before April 2019
                elif end_year == 2019:  # Ended in 2019
                    # Check if they ended after April 2019
                    end_month_match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)', end_date, re.IGNORECASE)
                    if end_month_match:
                        end_month = end_month_match.group(1).title()
                        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                        if months.index(end_month) < 4:  # Ended before May (i.e., before or during April)
                            served_before_april_2019 = True
                        else:
                            served_before_april_2019 = True  # Still served before April even if they ended after April
                    else:
                        served_before_april_2019 = True  # Assume they served before April if we can't determine month
                else:  # Ended after 2019
                    served_before_april_2019 = True  # Definitely served before April 2019
    
    if not served_before_april_2019:
        print(f"Skipping {name} - did not serve before April 2019")
        continue
    
    secretary_info = {
        'name': name,
        'term': term_text,
        'wiki_link': wiki_link
    }
    
    print(f"Adding secretary: {name}")
    secretaries.append(secretary_info)

print(f"Found {len(secretaries)} Secretaries of Homeland Security who served before April 2019 (excluding acting secretaries)")

# Function to extract educational background from a secretary's Wikipedia page
def get_education_background(wiki_link):
    if not wiki_link:
        return "Wikipedia link not available"
    
    print(f"Fetching education details from: {wiki_link}")
    response = fetch_with_backoff(wiki_link)
    if not response:
        return "Education information not available"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for education information in the infobox
    education = []
    infobox = soup.find('table', class_='infobox')
    if infobox:
        for row in infobox.find_all('tr'):
            header = row.find('th')
            if header and ('education' in header.get_text().lower() or 'alma mater' in header.get_text().lower()):
                value = row.find('td')
                if value:
                    education.append(value.get_text().strip())
    
    # If not found in infobox, look in the content
    if not education:
        print("Education not found in infobox, searching in content...")
        content = soup.find('div', class_='mw-parser-output')
        if content:
            paragraphs = content.find_all('p')
            education_keywords = ['graduate', 'graduated', 'degree', 'university', 'college', 'b.a.', 'b.s.', 'bachelor', 'education']
            
            for paragraph in paragraphs:
                text = paragraph.get_text().lower()
                if any(keyword in text for keyword in education_keywords):
                    education.append(paragraph.get_text().strip())
    
    if education:
        return "\n".join(education)
    else:
        return "Education information not found"

# Function to extract bachelor's degree from education text
def extract_bachelors_degree(education_text):
    if not education_text or education_text in ["Education information not available", "Education information not found", "Wikipedia link not available"]:
        return "Unknown"
    
    # List of patterns to try in order of specificity
    patterns = [
        r'(?:bachelor[\'']?s? (?:of|degree|in)|B\.?A\.?|B\.?S\.?)[^.]*?(?:from|at)\s+([^.,;()]+)',
        r'(?:earned|received|completed|obtained)\s+(?:a|an|his|her)\s+(?:bachelor[\'']?s?|undergraduate\s+degree|B\.?A\.?|B\.?S\.?)[^.]*?(?:from|at)\s+([^.,;()]+)',
        r'(?:attended|enrolled\s+(?:at|in))\s+([^.,;()]+)\s+(?:where|and)\s+(?:earned|received|graduated|obtained)\s+(?:a|an|his|her)\s+(?:bachelor[\'']?s?|B\.?A\.?|B\.?S\.?)',
        r'graduated\s+(?:from|in)\s+([^.,;()]+)\s+(?:with|earning)\s+(?:a|an)\s+(?:bachelor[\'']?s?|B\.?A\.?|B\.?S\.?)',
        r'([^.,;()]+?)\s+(?:University|College|Institute)',
        r'(University|College|Institute)\s+of\s+[^.,;()]+',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, education_text, re.IGNORECASE)
        if matches:
            # Clean up any remaining references or annotations
            degree = re.sub(r'\[\d+\]', '', matches[0]).strip()
            return degree
    
    # If no match found with the patterns, try to find any university or college mention
    university_pattern = r'(?:[A-Z][a-z]+\s+)+(?:University|College|Institute)|(?:University|College|Institute)\s+of\s+(?:[A-Z][a-z]+\s*)+'  
    university_matches = re.findall(university_pattern, education_text)
    
    if university_matches:
        return university_matches[0].strip()
    
    return "Not specifically identified"

# Enhance secretaries data with education information
print("\nRetrieving educational background for each Secretary...")
for secretary in secretaries:
    if secretary['wiki_link']:
        education_text = get_education_background(secretary['wiki_link'])
        secretary['education'] = education_text
        
        # Extract bachelor's degree
        bachelors_degree = extract_bachelors_degree(education_text)
        secretary['bachelors_degree'] = bachelors_degree
        
        print(f"Secretary: {secretary['name']}")
        print(f"Bachelor's Degree: {bachelors_degree}")
        print("-" * 40)
    else:
        secretary['education'] = "Wikipedia link not available"
        secretary['bachelors_degree'] = "Unknown"
        print(f"Secretary: {secretary['name']} - No Wikipedia link available")

# Save the results
results_file = os.path.join(workspace_dir, 'homeland_security_secretaries.json')
with open(results_file, 'w') as f:
    json.dump(secretaries, f, indent=4)

print(f"\nResults saved to {results_file}")

# Print a summary of the findings
print("\nSummary of US Secretaries of Homeland Security who served prior to April 2019:")
print("-" * 80)
for secretary in secretaries:
    print(f"Name: {secretary['name']}")
    print(f"Term: {secretary['term']}")
    print(f"Bachelor's Degree: {secretary.get('bachelors_degree', 'Unknown')}")
    print("-" * 80)
```

## Created Time
2025-08-13 22:43:12
