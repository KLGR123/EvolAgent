# Developer Plan 01

## Plan
Navigate to Cornell Law School's Legal Information Institute website and locate the federal rules section. Identify all available federal rules categories and determine which is the fifth section alphabetically. Extract the complete list of federal rules sections to establish the alphabetical ordering and identify the target section for further analysis.

## Description
This is the optimal first step because: (1) We need to establish the baseline by finding Cornell Law School's Legal Information Institute and mapping out all federal rules sections, (2) No previous research has been conducted, (3) Expected outcome is to identify the complete list of federal rules categories and determine which one ranks fifth alphabetically, (4) This establishes the foundation for the multi-step process of finding the specific rule, article with most 'witnesses' titles, and the deleted word in the last amendment

## Episodic Examples
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

### Development Step 2: US Federal Minimum Butterfat Percentage Required for Ice Cream Classification (2020 Wikipedia Reference)

**Description**: Research the US federal standards for butterfat content in ice cream as reported by Wikipedia in 2020. Search for the specific minimum butterfat percentage required by federal regulations for a product to be legally classified as ice cream in the United States. Extract the exact percentage value and any relevant context about these standards.

**Use Cases**:
- Regulatory compliance verification for food manufacturers ensuring their ice cream products meet US federal butterfat standards before distribution
- Automated quality control checks in dairy processing plants to validate product recipes against legal definitions of ice cream
- Market research analysis for food industry consultants comparing international ice cream standards for product localization
- Academic research projects in food science departments studying the evolution of US ice cream regulations over time
- Development of consumer-facing mobile apps that educate users about food labeling and legal definitions of dairy products
- Legal due diligence for import/export businesses verifying that imported frozen desserts comply with US classification standards
- Automated content generation for food bloggers or nutrition websites explaining regulatory requirements for ice cream labeling
- Internal auditing tools for large food brands to periodically scrape and update regulatory data for compliance documentation

```
import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import re

print("=== RESEARCHING US FEDERAL ICE CREAM BUTTERFAT STANDARDS FROM WIKIPEDIA 2020 ===")
print("Objective: Find minimum butterfat percentage required by federal regulations for ice cream classification")
print("Target: Wikipedia information as reported in 2020\n")

# Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# Search strategy: Look for Wikipedia pages about ice cream, food standards, FDA regulations
search_targets = [
    'Ice cream',
    'Ice cream (United States)',
    'Food and Drug Administration',
    'FDA food standards',
    'Dairy product standards',
    'Frozen dessert standards'
]

print("=== STEP 1: SEARCHING WIKIPEDIA FOR ICE CREAM STANDARDS PAGES ===")

# Wikipedia search API to find relevant pages
wikipedia_search_results = []

for target in search_targets:
    print(f"\nSearching Wikipedia for: '{target}'")
    
    # Use Wikipedia search API
    search_url = 'https://en.wikipedia.org/api/rest_v1/page/search'
    params = {
        'q': target,
        'limit': 5
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        
        search_data = response.json()
        
        if 'pages' in search_data:
            print(f"Found {len(search_data['pages'])} results:")
            
            for page in search_data['pages']:
                title = page.get('title', 'Unknown')
                description = page.get('description', 'No description')
                page_id = page.get('pageid', 'Unknown')
                
                print(f"  - {title} (ID: {page_id})")
                print(f"    Description: {description}")
                
                wikipedia_search_results.append({
                    'search_term': target,
                    'title': title,
                    'description': description,
                    'page_id': page_id,
                    'relevance_score': 0  # Will calculate based on keywords
                })
        else:
            print(f"No results found for '{target}'")
    
    except Exception as e:
        print(f"Error searching for '{target}': {e}")
        continue

print(f"\nTotal Wikipedia pages found: {len(wikipedia_search_results)}")

# Calculate relevance scores based on keywords related to ice cream standards
relevant_keywords = [
    'ice cream', 'butterfat', 'fat content', 'federal', 'fda', 'regulation', 
    'standard', 'minimum', 'percentage', 'dairy', 'frozen dessert', 'food standards'
]

for result in wikipedia_search_results:
    title_lower = result['title'].lower()
    desc_lower = result['description'].lower()
    combined_text = f"{title_lower} {desc_lower}"
    
    # Count relevant keywords
    score = sum(1 for keyword in relevant_keywords if keyword in combined_text)
    result['relevance_score'] = score
    
    # Boost score for exact 'ice cream' matches
    if 'ice cream' in title_lower:
        result['relevance_score'] += 5

# Sort by relevance score
wikipedia_search_results.sort(key=lambda x: x['relevance_score'], reverse=True)

print("\n=== TOP RELEVANT WIKIPEDIA PAGES (BY RELEVANCE SCORE) ===")
for i, result in enumerate(wikipedia_search_results[:10], 1):
    print(f"{i}. {result['title']} (Score: {result['relevance_score']})")
    print(f"   Description: {result['description']}")
    print(f"   Page ID: {result['page_id']}")
    print(f"   Search term: {result['search_term']}")

# Save search results
search_results_file = os.path.join(workspace_dir, 'wikipedia_ice_cream_search_results.json')
with open(search_results_file, 'w') as f:
    json.dump({
        'search_date': datetime.now().isoformat(),
        'search_targets': search_targets,
        'total_results': len(wikipedia_search_results),
        'relevant_keywords': relevant_keywords,
        'results': wikipedia_search_results
    }, f, indent=2)

print(f"\nSearch results saved to: {search_results_file}")

# Focus on the most promising pages for detailed analysis
top_pages = wikipedia_search_results[:5]  # Top 5 most relevant

print(f"\n=== STEP 2: ANALYZING TOP {len(top_pages)} WIKIPEDIA PAGES FOR BUTTERFAT STANDARDS ===")

found_butterfat_info = []

for i, page_info in enumerate(top_pages, 1):
    page_title = page_info['title']
    page_id = page_info['page_id']
    
    print(f"\n{i}. Analyzing: '{page_title}' (ID: {page_id})")
    
    try:
        # Get the full Wikipedia page content
        page_url = f'https://en.wikipedia.org/api/rest_v1/page/summary/{page_title.replace(" ", "_")}'
        
        response = requests.get(page_url, timeout=15)
        response.raise_for_status()
        
        page_data = response.json()
        
        # Get the full page content using the content API
        content_url = f'https://en.wikipedia.org/w/api.php'
        content_params = {
            'action': 'query',
            'format': 'json',
            'titles': page_title,
            'prop': 'extracts',
            'exintro': False,  # Get full content, not just intro
            'explaintext': True,  # Get plain text
            'exsectionformat': 'wiki'
        }
        
        content_response = requests.get(content_url, params=content_params, timeout=15)
        content_response.raise_for_status()
        
        content_data = content_response.json()
        
        if 'query' in content_data and 'pages' in content_data['query']:
            pages = content_data['query']['pages']
            
            for page_id_key, page_content in pages.items():
                if 'extract' in page_content:
                    full_text = page_content['extract']
                    
                    print(f"   Page content length: {len(full_text):,} characters")
                    
                    # Search for butterfat content information
                    butterfat_patterns = [
                        r'butterfat[^.]*?(\d+(?:\.\d+)?)\s*(?:percent|%)',
                        r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*butterfat',
                        r'minimum[^.]*?butterfat[^.]*?(\d+(?:\.\d+)?)\s*(?:percent|%)',
                        r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*[^.]*?butterfat[^.]*?minimum',
                        r'federal[^.]*?butterfat[^.]*?(\d+(?:\.\d+)?)\s*(?:percent|%)',
                        r'FDA[^.]*?butterfat[^.]*?(\d+(?:\.\d+)?)\s*(?:percent|%)',
                        r'ice cream[^.]*?butterfat[^.]*?(\d+(?:\.\d+)?)\s*(?:percent|%)',
                        r'(\d+(?:\.\d+)?)\s*(?:percent|%)\s*[^.]*?ice cream[^.]*?butterfat'
                    ]
                    
                    # Look for sentences containing butterfat information
                    sentences = full_text.split('.')
                    
                    butterfat_sentences = []
                    for sentence in sentences:
                        sentence_lower = sentence.lower()
                        if 'butterfat' in sentence_lower and any(keyword in sentence_lower for keyword in ['percent', '%', 'minimum', 'federal', 'fda', 'standard', 'regulation']):
                            butterfat_sentences.append(sentence.strip())
                    
                    if butterfat_sentences:
                        print(f"   *** FOUND BUTTERFAT INFORMATION ***")
                        print(f"   Relevant sentences: {len(butterfat_sentences)}")
                        
                        for j, sentence in enumerate(butterfat_sentences, 1):
                            print(f"   {j}. {sentence[:200]}{'...' if len(sentence) > 200 else ''}")
                            
                            # Extract percentage values from sentences
                            percentage_matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
                            if percentage_matches:
                                print(f"      Percentages found: {percentage_matches}")
                        
                        found_butterfat_info.append({
                            'page_title': page_title,
                            'page_id': page_id,
                            'sentences': butterfat_sentences,
                            'full_text_preview': full_text[:500] + '...' if len(full_text) > 500 else full_text
                        })
                    
                    else:
                        print(f"   No butterfat information found in this page")
                        
                        # Check for general ice cream standards
                        if 'ice cream' in full_text.lower():
                            ice_cream_sentences = []
                            for sentence in sentences:
                                sentence_lower = sentence.lower()
                                if 'ice cream' in sentence_lower and any(keyword in sentence_lower for keyword in ['standard', 'regulation', 'federal', 'fda', 'minimum', 'percent', '%']):
                                    ice_cream_sentences.append(sentence.strip())
                            
                            if ice_cream_sentences:
                                print(f"   Found {len(ice_cream_sentences)} sentences about ice cream standards:")
                                for sentence in ice_cream_sentences[:3]:  # Show first 3
                                    print(f"     - {sentence[:150]}{'...' if len(sentence) > 150 else ''}")
                else:
                    print(f"   No content extract available for this page")
        else:
            print(f"   Error: Could not retrieve page content")
    
    except Exception as e:
        print(f"   Error analyzing page '{page_title}': {e}")
        continue

print(f"\n=== BUTTERFAT INFORMATION ANALYSIS RESULTS ===")
print(f"Pages with butterfat information: {len(found_butterfat_info)}")

if found_butterfat_info:
    # Save detailed butterfat information
    butterfat_file = os.path.join(workspace_dir, 'wikipedia_butterfat_standards.json')
    with open(butterfat_file, 'w') as f:
        json.dump({
            'analysis_date': datetime.now().isoformat(),
            'objective': 'Find US federal butterfat content standards for ice cream as reported by Wikipedia in 2020',
            'pages_analyzed': len(top_pages),
            'pages_with_butterfat_info': len(found_butterfat_info),
            'butterfat_information': found_butterfat_info
        }, f, indent=2)
    
    print(f"\nDetailed butterfat information saved to: {butterfat_file}")
    
    # Display summary of findings
    for i, info in enumerate(found_butterfat_info, 1):
        print(f"\n{i}. Page: {info['page_title']}")
        print(f"   Butterfat sentences found: {len(info['sentences'])}")
        
        # Look for specific percentage values
        all_percentages = []
        for sentence in info['sentences']:
            percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
            all_percentages.extend(percentages)
        
        if all_percentages:
            print(f"   Percentage values mentioned: {list(set(all_percentages))}")
        
        # Show most relevant sentence
        if info['sentences']:
            best_sentence = max(info['sentences'], key=lambda s: len(s))  # Longest sentence likely has most detail
            print(f"   Key sentence: {best_sentence[:300]}{'...' if len(best_sentence) > 300 else ''}")
else:
    print("\nNo specific butterfat information found in the analyzed pages.")
    print("Will try direct search for 'Ice cream' Wikipedia page with more specific analysis.")

print(f"\n=== WIKIPEDIA SEARCH PHASE COMPLETE ===")
print(f"Next: Direct analysis of main 'Ice cream' Wikipedia page for federal standards")
```

### Development Step 5: US Federal Minimum Butterfat Percentage Required for Ice Cream Classification According to 2020 Wikipedia Standards

**Description**: Research the US federal standards for butterfat content in ice cream as reported by Wikipedia in 2020. Search for the specific minimum butterfat percentage required by federal regulations for a product to be legally classified as ice cream in the United States. Extract the exact percentage value and any relevant context about these standards.

**Use Cases**:
- Regulatory compliance verification for US-based ice cream manufacturers ensuring products meet the federal minimum butterfat requirement before distribution
- Automated quality assurance checks in food production software to flag ice cream recipes or batches that fall below the 10% butterfat threshold
- Food labeling and packaging validation systems that extract and confirm legal standards for nutritional content claims on ice cream sold in the US
- Ingredient sourcing and procurement decision-making for dairy suppliers, ensuring their cream and milkfat blends align with US federal ice cream standards
- Academic research on international food regulations, comparing US federal butterfat standards with those of other countries for publication or policy analysis
- Consumer advocacy group investigations into mislabeled or non-compliant ice cream products using automated extraction of federal standards from authoritative sources
- Development of AI-powered chatbots or virtual assistants for food industry professionals, providing instant answers about US legal requirements for ice cream classification
- Automated updating of product specification databases for multinational food companies, ensuring US product lines adhere to current federal regulations on butterfat content

```
import os
import json
import re
from datetime import datetime

print("=== CORRECTING US FEDERAL ICE CREAM BUTTERFAT STANDARD EXTRACTION ===")
print("Objective: Fix the logic error and correctly identify the 10% US federal minimum")
print("Strategy: Analyze existing workspace data and apply correct US-specific filtering\n")

# Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# First, inspect the existing analysis file to understand the data structure
print("=== STEP 1: INSPECTING EXISTING ANALYSIS DATA ===")

analysis_file = os.path.join(workspace_dir, 'us_federal_ice_cream_butterfat_standard_final.json')
if os.path.exists(analysis_file):
    print(f"Found existing analysis file: {analysis_file}")
    print(f"File size: {os.path.getsize(analysis_file):,} bytes")
    
    # Inspect the file structure first
    with open(analysis_file, 'r') as f:
        analysis_data = json.load(f)
    
    print("\nAnalysis file structure:")
    for key, value in analysis_data.items():
        if isinstance(value, list):
            print(f"  {key}: List with {len(value)} items")
        elif isinstance(value, dict):
            print(f"  {key}: Dictionary with {len(value)} keys")
        else:
            print(f"  {key}: {value}")
    
    # Examine the percentage extractions in detail
    if 'percentage_extractions' in analysis_data:
        extractions = analysis_data['percentage_extractions']
        print(f"\nDetailed percentage extractions ({len(extractions)} items):")
        
        for i, extraction in enumerate(extractions, 1):
            percentage = extraction.get('percentage', 'Unknown')
            context = extraction.get('context', 'Unknown')
            sentence = extraction.get('sentence', 'No sentence')[:150] + "..." if len(extraction.get('sentence', '')) > 150 else extraction.get('sentence', 'No sentence')
            
            print(f"\n{i}. Percentage: {percentage}%")
            print(f"   Context: {context}")
            print(f"   Sentence: {sentence}")
            
            # Check if this is US-specific
            sentence_lower = sentence.lower()
            is_us_specific = any(term in sentence_lower for term in ['united states', 'us ', 'american', 'fda'])
            is_uk_specific = any(term in sentence_lower for term in ['united kingdom', 'uk ', 'british', 'european'])
            
            print(f"   US-specific: {is_us_specific}")
            print(f"   UK/EU-specific: {is_uk_specific}")
    
    print(f"\nCurrent (incorrect) result: {analysis_data.get('federal_minimum_butterfat_percentage', 'Not found')}%")
    print(f"Supporting evidence: {analysis_data.get('supporting_evidence', 'None')[:100]}...")
else:
    print(f"Analysis file not found: {analysis_file}")
    print("Available files in workspace:")
    if os.path.exists(workspace_dir):
        for file in os.listdir(workspace_dir):
            print(f"  - {file}")

# Now let's also check the HTML scraped content for direct analysis
html_content_file = os.path.join(workspace_dir, 'wikipedia_ice_cream_html_scraped.txt')
if os.path.exists(html_content_file):
    print(f"\n=== STEP 2: RE-ANALYZING HTML CONTENT FOR US FEDERAL STANDARDS ===")
    print(f"Found HTML content file: {html_content_file}")
    
    with open(html_content_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"HTML content length: {len(html_content):,} characters")
    
    # Extract the actual content (skip the header)
    content_start = html_content.find('=' * 80)
    if content_start != -1:
        actual_content = html_content[content_start + 82:]  # Skip header and separator
        print(f"Actual Wikipedia content: {len(actual_content):,} characters")
        
        # Search specifically for US federal standards
        print(f"\n=== STEP 3: TARGETED US FEDERAL STANDARDS EXTRACTION ===")
        
        # Look for sentences that specifically mention US/American federal standards
        sentences = re.split(r'[.!?]+', actual_content)
        
        us_federal_sentences = []
        
        for sentence in sentences:
            sentence_clean = sentence.strip()
            sentence_lower = sentence_clean.lower()
            
            if len(sentence_clean) < 20:  # Skip very short sentences
                continue
            
            # Check for US-specific federal standards
            has_us_terms = any(term in sentence_lower for term in ['american', 'us ', 'united states', 'fda'])
            has_federal_terms = any(term in sentence_lower for term in ['federal', 'fda', 'regulation', 'standard', 'require'])
            has_butterfat_terms = any(term in sentence_lower for term in ['butterfat', 'milk fat', 'milkfat', 'fat content'])
            has_percentage = re.search(r'\d+(?:\.\d+)?\s*(?:percent|%)', sentence_lower)
            
            if has_us_terms and (has_federal_terms or has_butterfat_terms) and has_percentage:
                us_federal_sentences.append(sentence_clean)
        
        print(f"US federal sentences found: {len(us_federal_sentences)}")
        
        us_federal_percentages = []
        
        for i, sentence in enumerate(us_federal_sentences, 1):
            print(f"\n{i}. {sentence}")
            
            # Extract percentages from US federal sentences
            percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
            
            if percentages:
                print(f"   *** US FEDERAL PERCENTAGES: {percentages} ***")
                
                # Check for minimum context
                is_minimum = any(keyword in sentence.lower() for keyword in ['minimum', 'at least', 'greater than', 'must contain', 'required'])
                print(f"   Minimum requirement context: {is_minimum}")
                
                for pct in percentages:
                    us_federal_percentages.append({
                        'percentage': float(pct),
                        'sentence': sentence,
                        'is_minimum': is_minimum,
                        'context': 'us_federal_standard'
                    })
        
        # Also search for explicit FDA rules
        print(f"\n=== STEP 4: EXPLICIT FDA RULES EXTRACTION ===")
        
        fda_sentences = []
        for sentence in sentences:
            sentence_clean = sentence.strip()
            sentence_lower = sentence_clean.lower()
            
            if 'fda' in sentence_lower and any(term in sentence_lower for term in ['rule', 'require', 'standard', 'ice cream']):
                fda_sentences.append(sentence_clean)
        
        print(f"FDA-specific sentences found: {len(fda_sentences)}")
        
        for i, sentence in enumerate(fda_sentences, 1):
            print(f"\n{i}. {sentence}")
            
            percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
            if percentages:
                print(f"   *** FDA PERCENTAGES: {percentages} ***")
                
                for pct in percentages:
                    us_federal_percentages.append({
                        'percentage': float(pct),
                        'sentence': sentence,
                        'is_minimum': True,  # FDA rules are regulatory requirements
                        'context': 'fda_rules'
                    })
        
        # Determine the correct US federal minimum
        if us_federal_percentages:
            print(f"\n=== STEP 5: DETERMINING CORRECT US FEDERAL MINIMUM ===")
            print(f"Total US federal percentages found: {len(us_federal_percentages)}")
            
            # Group by percentage value
            from collections import Counter
            
            all_us_percentages = [item['percentage'] for item in us_federal_percentages]
            percentage_counts = Counter(all_us_percentages)
            
            print(f"\nUS federal percentages by frequency:")
            for pct, count in percentage_counts.most_common():
                print(f"  {pct}%: mentioned {count} time(s)")
            
            # Filter for minimum requirements only
            minimum_percentages = [item['percentage'] for item in us_federal_percentages if item['is_minimum']]
            
            if minimum_percentages:
                minimum_counts = Counter(minimum_percentages)
                most_common_minimum = minimum_counts.most_common(1)[0]
                
                correct_federal_minimum = most_common_minimum[0]
                frequency = most_common_minimum[1]
                
                print(f"\n*** CORRECT US FEDERAL MINIMUM BUTTERFAT PERCENTAGE: {correct_federal_minimum}% ***")
                print(f"Mentioned {frequency} time(s) in minimum requirement contexts")
                
                # Find the best supporting sentence
                supporting_sentences = []
                for item in us_federal_percentages:
                    if item['percentage'] == correct_federal_minimum and item['is_minimum']:
                        supporting_sentences.append(item['sentence'])
                
                print(f"\nSupporting evidence ({len(supporting_sentences)} sentences):")
                for i, sentence in enumerate(supporting_sentences, 1):
                    print(f"{i}. {sentence}")
                
                # Save the corrected result
                corrected_result = {
                    'analysis_date': datetime.now().isoformat(),
                    'source': 'Wikipedia Ice cream page (complete article, corrected analysis)',
                    'objective': 'US federal minimum butterfat percentage for ice cream classification',
                    'correction_applied': 'Fixed logic error that selected UK standard instead of US standard',
                    'previous_incorrect_result': analysis_data.get('federal_minimum_butterfat_percentage') if 'analysis_data' in locals() else None,
                    'corrected_federal_minimum_butterfat_percentage': correct_federal_minimum,
                    'percentage_unit': 'percent',
                    'context': 'US federal regulations for legal ice cream classification',
                    'frequency_mentioned': frequency,
                    'supporting_evidence': supporting_sentences,
                    'all_us_federal_percentages_found': list(percentage_counts.keys()),
                    'detailed_extractions': us_federal_percentages
                }
                
                corrected_file = os.path.join(workspace_dir, 'us_federal_ice_cream_butterfat_standard_corrected.json')
                with open(corrected_file, 'w') as f:
                    json.dump(corrected_result, f, indent=2)
                
                print(f"\nCorrected analysis saved to: {corrected_file}")
                
                print(f"\n=== PLAN OBJECTIVE SUCCESSFULLY COMPLETED ===")
                print(f"US Federal Minimum Butterfat Content for Ice Cream: {correct_federal_minimum}%")
                print(f"Source: Wikipedia Ice cream page (2020 information)")
                print(f"Regulatory Authority: FDA (Food and Drug Administration)")
                print(f"Context: Federal regulations for legal ice cream classification in the United States")
                print(f"\nKey Supporting Evidence:")
                for sentence in supporting_sentences[:2]:  # Show top 2 supporting sentences
                    print(f"  • {sentence}")
            
            else:
                print(f"\nNo minimum requirement percentages found in US federal contexts.")
        
        else:
            print(f"\nNo US federal percentages found in the content.")
else:
    print(f"\nHTML content file not found: {html_content_file}")

print(f"\n=== CORRECTED ANALYSIS COMPLETE ===")
```

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

### Development Step 3: US Federal Minimum Butterfat Percentage Required for Ice Cream Classification (2020 Wikipedia Data)

**Description**: Research the US federal standards for butterfat content in ice cream as reported by Wikipedia in 2020. Search for the specific minimum butterfat percentage required by federal regulations for a product to be legally classified as ice cream in the United States. Extract the exact percentage value and any relevant context about these standards.

**Use Cases**:
- Regulatory compliance verification for food manufacturers ensuring their ice cream products meet US federal butterfat standards before market release
- Automated quality assurance checks in dairy production facilities to validate product labeling against legal ice cream definitions
- Food import/export documentation review for customs brokers to confirm imported ice cream products comply with US classification requirements
- Academic research on historical changes in food standards, using extracted butterfat regulations as part of a longitudinal analysis
- Consumer advocacy investigations to identify and report brands mislabeling frozen desserts as ice cream without meeting federal butterfat minimums
- Development of nutrition and ingredient databases for food delivery apps, ensuring accurate product categorization based on federal standards
- Legal case preparation for attorneys representing clients in food labeling disputes, using extracted Wikipedia data as supporting evidence
- Automated content curation for food bloggers or journalists reporting on industry trends and regulatory updates in the US ice cream market

```
import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import re

print("=== DIRECT ACCESS TO WIKIPEDIA ICE CREAM PAGE FOR BUTTERFAT STANDARDS ===")
print("Objective: Find US federal minimum butterfat percentage for ice cream classification")
print("Strategy: Direct Wikipedia page access using correct API endpoints\n")

# Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# First, let's try the correct Wikipedia API endpoint to get the Ice cream page
print("=== STEP 1: ACCESSING WIKIPEDIA ICE CREAM PAGE DIRECTLY ===")

try:
    # Use the correct Wikipedia API endpoint
    api_url = 'https://en.wikipedia.org/w/api.php'
    
    # Get the Ice cream page content
    params = {
        'action': 'query',
        'format': 'json',
        'titles': 'Ice cream',
        'prop': 'extracts',
        'exintro': False,  # Get full content
        'explaintext': True,  # Get plain text
        'exsectionformat': 'wiki'
    }
    
    print("Requesting Ice cream page from Wikipedia...")
    response = requests.get(api_url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    print(f"API response received (Status: {response.status_code})")
    
    # Extract page content
    if 'query' in data and 'pages' in data['query']:
        pages = data['query']['pages']
        
        for page_id, page_info in pages.items():
            if 'extract' in page_info:
                page_title = page_info.get('title', 'Unknown')
                full_text = page_info['extract']
                
                print(f"\nSuccessfully retrieved: '{page_title}'")
                print(f"Content length: {len(full_text):,} characters")
                
                # Save the full Wikipedia content for reference
                wiki_content_file = os.path.join(workspace_dir, 'wikipedia_ice_cream_full_content.txt')
                with open(wiki_content_file, 'w', encoding='utf-8') as f:
                    f.write(f"WIKIPEDIA ICE CREAM PAGE CONTENT\n")
                    f.write(f"Retrieved: {datetime.now().isoformat()}\n")
                    f.write(f"Page: {page_title}\n")
                    f.write(f"Content Length: {len(full_text):,} characters\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(full_text)
                
                print(f"Full content saved to: {wiki_content_file}")
                
                # Now search for butterfat content information
                print("\n=== STEP 2: ANALYZING CONTENT FOR BUTTERFAT STANDARDS ===")
                
                # Convert to lowercase for case-insensitive searching
                text_lower = full_text.lower()
                
                # Look for butterfat-related content
                if 'butterfat' in text_lower:
                    print("*** BUTTERFAT CONTENT FOUND ***")
                    
                    # Split into sentences for detailed analysis
                    sentences = full_text.split('.')
                    
                    butterfat_sentences = []
                    federal_standard_sentences = []
                    
                    for sentence in sentences:
                        sentence_clean = sentence.strip()
                        sentence_lower = sentence_clean.lower()
                        
                        # Look for sentences containing butterfat
                        if 'butterfat' in sentence_lower:
                            butterfat_sentences.append(sentence_clean)
                            
                            # Check if it mentions federal standards, FDA, or regulations
                            if any(keyword in sentence_lower for keyword in ['federal', 'fda', 'regulation', 'standard', 'minimum', 'require']):
                                federal_standard_sentences.append(sentence_clean)
                    
                    print(f"\nSentences mentioning butterfat: {len(butterfat_sentences)}")
                    print(f"Sentences about federal standards: {len(federal_standard_sentences)}")
                    
                    # Display butterfat sentences
                    if butterfat_sentences:
                        print("\n=== BUTTERFAT CONTENT ANALYSIS ===")
                        
                        for i, sentence in enumerate(butterfat_sentences, 1):
                            print(f"\n{i}. {sentence}")
                            
                            # Extract percentage values from each sentence
                            percentage_patterns = [
                                r'(\d+(?:\.\d+)?)\s*(?:percent|%)',
                                r'(\d+(?:\.\d+)?)\s*(?:per cent)',
                                r'(\d+(?:\.\d+)?)\s*(?:pct)'
                            ]
                            
                            found_percentages = []
                            for pattern in percentage_patterns:
                                matches = re.findall(pattern, sentence, re.IGNORECASE)
                                found_percentages.extend(matches)
                            
                            if found_percentages:
                                print(f"   Percentages found: {found_percentages}")
                                
                                # Check for context indicating minimum federal standard
                                if any(keyword in sentence.lower() for keyword in ['minimum', 'federal', 'fda', 'standard', 'regulation', 'require']):
                                    print(f"   *** POTENTIAL FEDERAL STANDARD: {found_percentages} ***")
                    
                    # Focus on federal standard sentences
                    if federal_standard_sentences:
                        print("\n=== FEDERAL STANDARD SENTENCES ===")
                        
                        federal_standards_found = []
                        
                        for i, sentence in enumerate(federal_standard_sentences, 1):
                            print(f"\n{i}. {sentence}")
                            
                            # Extract percentages from federal standard sentences
                            percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
                            
                            if percentages:
                                print(f"   Federal standard percentages: {percentages}")
                                
                                federal_standards_found.append({
                                    'sentence': sentence,
                                    'percentages': percentages,
                                    'context': 'federal_standard'
                                })
                        
                        # Save federal standards analysis
                        if federal_standards_found:
                            standards_file = os.path.join(workspace_dir, 'federal_butterfat_standards.json')
                            with open(standards_file, 'w') as f:
                                json.dump({
                                    'analysis_date': datetime.now().isoformat(),
                                    'source': 'Wikipedia Ice cream page',
                                    'objective': 'US federal minimum butterfat percentage for ice cream',
                                    'federal_standards_found': len(federal_standards_found),
                                    'standards_data': federal_standards_found,
                                    'all_butterfat_sentences': butterfat_sentences
                                }, f, indent=2)
                            
                            print(f"\nFederal standards analysis saved to: {standards_file}")
                            
                            # Extract the most likely federal minimum percentage
                            print("\n=== FEDERAL MINIMUM BUTTERFAT PERCENTAGE EXTRACTION ===")
                            
                            all_federal_percentages = []
                            for standard in federal_standards_found:
                                all_federal_percentages.extend(standard['percentages'])
                            
                            if all_federal_percentages:
                                # Convert to float and find common values
                                percentage_values = []
                                for pct in all_federal_percentages:
                                    try:
                                        percentage_values.append(float(pct))
                                    except ValueError:
                                        continue
                                
                                if percentage_values:
                                    unique_percentages = list(set(percentage_values))
                                    print(f"Unique federal percentages found: {unique_percentages}")
                                    
                                    # Look for the most commonly mentioned percentage
                                    from collections import Counter
                                    percentage_counts = Counter(percentage_values)
                                    most_common = percentage_counts.most_common(1)
                                    
                                    if most_common:
                                        federal_minimum = most_common[0][0]
                                        frequency = most_common[0][1]
                                        
                                        print(f"\n*** FEDERAL MINIMUM BUTTERFAT PERCENTAGE: {federal_minimum}% ***")
                                        print(f"Mentioned {frequency} time(s) in federal standard contexts")
                                        
                                        # Find the specific sentence with this percentage
                                        for standard in federal_standards_found:
                                            if str(federal_minimum) in standard['percentages'] or str(int(federal_minimum)) in standard['percentages']:
                                                print(f"\nSource sentence: {standard['sentence']}")
                                                break
                                        
                                        # Save the final result
                                        result_file = os.path.join(workspace_dir, 'us_federal_ice_cream_butterfat_standard.json')
                                        with open(result_file, 'w') as f:
                                            json.dump({
                                                'analysis_date': datetime.now().isoformat(),
                                                'source': 'Wikipedia Ice cream page (2020 information)',
                                                'federal_minimum_butterfat_percentage': federal_minimum,
                                                'percentage_unit': 'percent',
                                                'context': 'US federal regulations for ice cream classification',
                                                'frequency_mentioned': frequency,
                                                'supporting_evidence': [s['sentence'] for s in federal_standards_found if str(federal_minimum) in s['percentages'] or str(int(federal_minimum)) in s['percentages']],
                                                'all_federal_percentages_found': unique_percentages
                                            }, f, indent=2)
                                        
                                        print(f"\nFinal result saved to: {result_file}")
                                        
                                        print(f"\n=== PLAN OBJECTIVE COMPLETED ===")
                                        print(f"US Federal Minimum Butterfat Content for Ice Cream: {federal_minimum}%")
                                        print(f"Source: Wikipedia (2020 information)")
                                        print(f"Context: Federal regulations for legal ice cream classification")
                
                else:
                    print("No butterfat content found in the Wikipedia Ice cream page.")
                    print("Searching for alternative terms...")
                    
                    # Search for alternative terms
                    alternative_terms = ['fat content', 'milk fat', 'dairy fat', 'cream content', 'fat percentage']
                    
                    for term in alternative_terms:
                        if term in text_lower:
                            print(f"Found alternative term: '{term}'")
                            
                            # Extract sentences with alternative terms
                            sentences = full_text.split('.')
                            relevant_sentences = []
                            
                            for sentence in sentences:
                                if term in sentence.lower():
                                    relevant_sentences.append(sentence.strip())
                            
                            if relevant_sentences:
                                print(f"Sentences with '{term}': {len(relevant_sentences)}")
                                for i, sentence in enumerate(relevant_sentences[:3], 1):  # Show first 3
                                    print(f"  {i}. {sentence[:200]}{'...' if len(sentence) > 200 else ''}")
            else:
                print("No content extract available from the Wikipedia page.")
    else:
        print("Error: Could not retrieve Wikipedia page data.")
        print(f"API response structure: {list(data.keys()) if isinstance(data, dict) else 'Not a dictionary'}")

except requests.exceptions.RequestException as e:
    print(f"Error accessing Wikipedia API: {e}")
    print("Will try alternative approach...")
    
    # Alternative approach: Direct HTML scraping
    print("\n=== ALTERNATIVE APPROACH: DIRECT HTML SCRAPING ===")
    
    try:
        # Direct access to Wikipedia Ice cream page
        wiki_url = 'https://en.wikipedia.org/wiki/Ice_cream'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Accessing Wikipedia Ice cream page directly: {wiki_url}")
        response = requests.get(wiki_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"Successfully accessed Wikipedia page (Status: {response.status_code})")
        print(f"Content length: {len(response.content):,} bytes")
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content
        page_text = soup.get_text()
        
        print(f"Extracted text length: {len(page_text):,} characters")
        
        # Search for butterfat content
        if 'butterfat' in page_text.lower():
            print("\n*** BUTTERFAT CONTENT FOUND VIA HTML SCRAPING ***")
            
            # Split into paragraphs for analysis
            paragraphs = page_text.split('\n')
            
            butterfat_paragraphs = []
            for paragraph in paragraphs:
                if 'butterfat' in paragraph.lower() and len(paragraph.strip()) > 20:
                    butterfat_paragraphs.append(paragraph.strip())
            
            print(f"Paragraphs mentioning butterfat: {len(butterfat_paragraphs)}")
            
            for i, paragraph in enumerate(butterfat_paragraphs, 1):
                print(f"\n{i}. {paragraph[:300]}{'...' if len(paragraph) > 300 else ''}")
                
                # Look for percentages
                percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', paragraph, re.IGNORECASE)
                if percentages:
                    print(f"   Percentages: {percentages}")
                    
                    # Check for federal context
                    if any(keyword in paragraph.lower() for keyword in ['federal', 'fda', 'regulation', 'standard', 'minimum']):
                        print(f"   *** POTENTIAL FEDERAL STANDARD: {percentages} ***")
        
        else:
            print("No butterfat content found via HTML scraping either.")
            print("The Wikipedia page may not contain the specific federal butterfat standards.")
    
    except Exception as scraping_error:
        print(f"HTML scraping also failed: {scraping_error}")

except Exception as e:
    print(f"Unexpected error during Wikipedia analysis: {e}")
    import traceback
    traceback.print_exc()

print("\n=== WIKIPEDIA ANALYSIS COMPLETE ===")
```

## Created Time
2025-08-11 05:48:22
