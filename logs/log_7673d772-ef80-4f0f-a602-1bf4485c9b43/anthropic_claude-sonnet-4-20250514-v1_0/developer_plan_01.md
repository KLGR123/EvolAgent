# Developer Plan 01

## Plan
Navigate to Cornell Law School's Legal Information Institute website and locate the federal rules section. Identify all available federal rules categories, arrange them alphabetically, and determine which category represents the fifth section. Extract the complete list of federal rules categories to establish the alphabetical ordering and identify the target section for further analysis.

## Description
This is the optimal starting approach because: (1) We need to establish the structure of Cornell Law School's Legal Information Institute and identify all federal rules sections, (2) No previous research has been conducted, (3) Expected outcome is to locate the federal rules categories and determine which one is fifth alphabetically, (4) This establishes the foundation for subsequently finding the article with the most 'witnesses' titles and analyzing the first rule's amendments

## Episodic Examples
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
2025-08-13 22:13:46
