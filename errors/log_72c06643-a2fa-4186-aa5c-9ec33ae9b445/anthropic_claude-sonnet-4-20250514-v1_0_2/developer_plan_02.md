# Developer Plan 02

## Plan
Research the thermodynamic properties of Freon-12 (dichlorodifluoromethane, CCl2F2) refrigerant, including its equation of state, critical properties, and phase behavior under extreme pressure and temperature conditions. Find reliable sources for Freon-12 property data such as density, compressibility factor, or specific volume correlations that can be used to calculate the volume of 0.312 kg at the Marianas Trench conditions (400°C peak temperature and 1,086 bars pressure).

## Description
This is the necessary next step because: (1) We have successfully obtained the Marianas Trench conditions (peak temperature 400°C and pressure 1,086 bars), (2) To calculate the volume of 0.312 kg Freon-12 under these extreme conditions, we need the refrigerant's thermodynamic properties and equation of state data, (3) Expected outcome is to find Freon-12 property correlations, critical constants, or density equations that can handle the extreme pressure and temperature conditions, (4) This will enable the calculation of specific volume and total volume for the given mass of Freon-12 refrigerant.

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

### Development Step 4: US Federal Minimum Butterfat Requirement for Ice Cream: 10% per 2020 Wikipedia Standards

**Description**: Research the US federal standards for butterfat content in ice cream as reported by Wikipedia in 2020. Search for the specific minimum butterfat percentage required by federal regulations for a product to be legally classified as ice cream in the United States. Extract the exact percentage value and any relevant context about these standards.

**Use Cases**:
- Quality assurance in a US ice cream manufacturing plant to verify products meet federal butterfat standards before distribution
- Regulatory compliance checks by food safety consultants auditing new frozen dessert products for legal classification as "ice cream"
- Automated labeling system for a food packaging company to ensure only qualifying products are marketed as "ice cream" under US law
- Competitive market analysis by a food industry analyst comparing butterfat content claims across brands using verified federal standards
- Academic research on the evolution of food standards, referencing historical butterfat regulations for publications or theses
- Consumer advocacy group investigations into mislabeled frozen desserts, using extracted standards to support complaints or reports
- Development of a nutrition-tracking app that flags products not meeting federal ice cream definitions for health-conscious users
- Automated content verification for online grocery platforms to ensure product listings accurately reflect legal definitions and standards

```
import requests
from bs4 import BeautifulSoup
import os
import json
from datetime import datetime
import re

print("=== COMPREHENSIVE WIKIPEDIA ICE CREAM ANALYSIS FOR FEDERAL BUTTERFAT STANDARDS ===")
print("Objective: Extract US federal minimum butterfat percentage from complete Wikipedia content")
print("Strategy: Multiple approaches to get full article content and detailed section analysis\n")

# Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# First, let's inspect the existing workspace files to understand what we already have
print("=== STEP 1: INSPECTING EXISTING WORKSPACE FILES ===")

if os.path.exists(workspace_dir):
    workspace_files = os.listdir(workspace_dir)
    print(f"Files in workspace: {len(workspace_files)}")
    
    for file in workspace_files:
        file_path = os.path.join(workspace_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
    
    # Check if we have the previous Wikipedia content
    wiki_content_file = os.path.join(workspace_dir, 'wikipedia_ice_cream_full_content.txt')
    if os.path.exists(wiki_content_file):
        print(f"\nInspecting previous Wikipedia content...")
        with open(wiki_content_file, 'r', encoding='utf-8') as f:
            previous_content = f.read()
        
        print(f"Previous content length: {len(previous_content):,} characters")
        print(f"Content preview (first 300 chars):\n{previous_content[:300]}...")
        
        # Check if this is just the intro or full content
        if len(previous_content) < 10000:  # Likely just intro/summary
            print("\n*** Previous content appears to be summary only - need full article ***")
else:
    print("No workspace directory found")

# Now try to get the COMPLETE Wikipedia Ice cream article
print("\n=== STEP 2: ACCESSING COMPLETE WIKIPEDIA ICE CREAM ARTICLE ===")

try:
    # Method 1: Try to get full content without intro restriction
    api_url = 'https://en.wikipedia.org/w/api.php'
    
    # Parameters to get the complete article content
    params = {
        'action': 'query',
        'format': 'json',
        'titles': 'Ice cream',
        'prop': 'extracts',
        'exintro': False,  # Get full content, not just intro
        'explaintext': True,  # Get plain text
        'exsectionformat': 'wiki',
        'exlimit': 1
    }
    
    print("Requesting COMPLETE Ice cream article from Wikipedia...")
    response = requests.get(api_url, params=params, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    print(f"API response received (Status: {response.status_code})")
    
    full_article_text = None
    
    if 'query' in data and 'pages' in data['query']:
        pages = data['query']['pages']
        
        for page_id, page_info in pages.items():
            if 'extract' in page_info:
                page_title = page_info.get('title', 'Unknown')
                full_article_text = page_info['extract']
                
                print(f"\nSuccessfully retrieved COMPLETE article: '{page_title}'")
                print(f"Full article length: {len(full_article_text):,} characters")
                
                # Save the complete article content
                complete_content_file = os.path.join(workspace_dir, 'wikipedia_ice_cream_complete_article.txt')
                with open(complete_content_file, 'w', encoding='utf-8') as f:
                    f.write(f"COMPLETE WIKIPEDIA ICE CREAM ARTICLE\n")
                    f.write(f"Retrieved: {datetime.now().isoformat()}\n")
                    f.write(f"Page: {page_title}\n")
                    f.write(f"Content Length: {len(full_article_text):,} characters\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(full_article_text)
                
                print(f"Complete article saved to: {complete_content_file}")
                break
    
    # If API didn't give us enough content, try HTML scraping
    if not full_article_text or len(full_article_text) < 10000:
        print("\n=== STEP 3: HTML SCRAPING FOR COMPLETE CONTENT ===")
        
        wiki_url = 'https://en.wikipedia.org/wiki/Ice_cream'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print(f"Scraping complete Wikipedia page: {wiki_url}")
        response = requests.get(wiki_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"HTML content retrieved (Status: {response.status_code})")
        print(f"HTML content length: {len(response.content):,} bytes")
        
        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # Get the main content area
        main_content = soup.find('div', {'id': 'mw-content-text'})
        if main_content:
            full_article_text = main_content.get_text()
            print(f"Extracted text from HTML: {len(full_article_text):,} characters")
            
            # Save HTML-scraped content
            html_content_file = os.path.join(workspace_dir, 'wikipedia_ice_cream_html_scraped.txt')
            with open(html_content_file, 'w', encoding='utf-8') as f:
                f.write(f"WIKIPEDIA ICE CREAM ARTICLE (HTML SCRAPED)\n")
                f.write(f"Retrieved: {datetime.now().isoformat()}\n")
                f.write(f"Source: {wiki_url}\n")
                f.write(f"Content Length: {len(full_article_text):,} characters\n")
                f.write("=" * 80 + "\n\n")
                f.write(full_article_text)
            
            print(f"HTML-scraped content saved to: {html_content_file}")
        else:
            print("Could not find main content area in HTML")
    
    # Now analyze the complete content for butterfat standards
    if full_article_text and len(full_article_text) > 1000:
        print(f"\n=== STEP 4: COMPREHENSIVE BUTTERFAT STANDARDS ANALYSIS ===")
        print(f"Analyzing {len(full_article_text):,} characters of content...")
        
        # Convert to lowercase for searching
        text_lower = full_article_text.lower()
        
        # Search for butterfat and related terms
        butterfat_terms = ['butterfat', 'butter fat', 'milk fat', 'milkfat', 'fat content']
        regulatory_terms = ['federal', 'fda', 'regulation', 'standard', 'minimum', 'require', 'law', 'legal', 'government']
        
        print(f"\nSearching for butterfat terms: {butterfat_terms}")
        print(f"Searching for regulatory terms: {regulatory_terms}")
        
        # Find all relevant sentences
        sentences = re.split(r'[.!?]+', full_article_text)
        
        butterfat_sentences = []
        federal_standard_sentences = []
        percentage_sentences = []
        
        for sentence in sentences:
            sentence_clean = sentence.strip()
            sentence_lower = sentence_clean.lower()
            
            if len(sentence_clean) < 10:  # Skip very short sentences
                continue
            
            # Check for butterfat terms
            has_butterfat = any(term in sentence_lower for term in butterfat_terms)
            has_regulatory = any(term in sentence_lower for term in regulatory_terms)
            has_percentage = re.search(r'\d+(?:\.\d+)?\s*(?:percent|%)', sentence_lower)
            
            if has_butterfat:
                butterfat_sentences.append(sentence_clean)
                
                if has_regulatory:
                    federal_standard_sentences.append(sentence_clean)
                
                if has_percentage:
                    percentage_sentences.append(sentence_clean)
        
        print(f"\nAnalysis results:")
        print(f"  Sentences mentioning butterfat terms: {len(butterfat_sentences)}")
        print(f"  Sentences with butterfat + regulatory terms: {len(federal_standard_sentences)}")
        print(f"  Sentences with butterfat + percentages: {len(percentage_sentences)}")
        
        # Display the most relevant sentences
        if federal_standard_sentences:
            print(f"\n=== FEDERAL STANDARD SENTENCES (MOST RELEVANT) ===")
            
            federal_percentages_found = []
            
            for i, sentence in enumerate(federal_standard_sentences, 1):
                print(f"\n{i}. {sentence}")
                
                # Extract all percentages from this sentence
                percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
                
                if percentages:
                    print(f"   *** PERCENTAGES FOUND: {percentages} ***")
                    
                    # Check for minimum/requirement context
                    if any(keyword in sentence.lower() for keyword in ['minimum', 'at least', 'must contain', 'required', 'shall contain']):
                        print(f"   *** MINIMUM REQUIREMENT CONTEXT DETECTED ***")
                        
                        for pct in percentages:
                            federal_percentages_found.append({
                                'percentage': pct,
                                'sentence': sentence,
                                'context': 'minimum_requirement'
                            })
                    else:
                        for pct in percentages:
                            federal_percentages_found.append({
                                'percentage': pct,
                                'sentence': sentence,
                                'context': 'general_standard'
                            })
        
        elif percentage_sentences:
            print(f"\n=== SENTENCES WITH BUTTERFAT PERCENTAGES ===")
            
            federal_percentages_found = []
            
            for i, sentence in enumerate(percentage_sentences, 1):
                print(f"\n{i}. {sentence}")
                
                percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
                
                if percentages:
                    print(f"   Percentages: {percentages}")
                    
                    # Check if this mentions US/United States
                    if any(term in sentence.lower() for term in ['united states', 'us ', 'america', 'federal']):
                        print(f"   *** US-SPECIFIC STANDARD ***")
                        
                        for pct in percentages:
                            federal_percentages_found.append({
                                'percentage': pct,
                                'sentence': sentence,
                                'context': 'us_specific'
                            })
        
        elif butterfat_sentences:
            print(f"\n=== ALL BUTTERFAT SENTENCES ===")
            
            federal_percentages_found = []
            
            for i, sentence in enumerate(butterfat_sentences[:10], 1):  # Show first 10
                print(f"\n{i}. {sentence}")
                
                # Look for any percentages
                percentages = re.findall(r'(\d+(?:\.\d+)?)\s*(?:percent|%)', sentence, re.IGNORECASE)
                
                if percentages:
                    print(f"   Percentages found: {percentages}")
                    
                    for pct in percentages:
                        federal_percentages_found.append({
                            'percentage': pct,
                            'sentence': sentence,
                            'context': 'general_butterfat'
                        })
        
        # Analyze and extract the federal minimum
        if 'federal_percentages_found' in locals() and federal_percentages_found:
            print(f"\n=== FEDERAL BUTTERFAT PERCENTAGE EXTRACTION ===")
            print(f"Total percentage values found: {len(federal_percentages_found)}")
            
            # Group by percentage value
            from collections import Counter
            
            all_percentages = [float(item['percentage']) for item in federal_percentages_found]
            percentage_counts = Counter(all_percentages)
            
            print(f"\nUnique percentages found: {list(percentage_counts.keys())}")
            
            # Find the most likely federal minimum (look for common values in minimum contexts)
            minimum_context_percentages = []
            for item in federal_percentages_found:
                if item['context'] in ['minimum_requirement', 'us_specific']:
                    minimum_context_percentages.append(float(item['percentage']))
            
            if minimum_context_percentages:
                most_likely_minimum = Counter(minimum_context_percentages).most_common(1)[0][0]
                print(f"\n*** US FEDERAL MINIMUM BUTTERFAT PERCENTAGE: {most_likely_minimum}% ***")
                
                # Find the supporting sentence
                supporting_sentence = None
                for item in federal_percentages_found:
                    if float(item['percentage']) == most_likely_minimum and item['context'] in ['minimum_requirement', 'us_specific']:
                        supporting_sentence = item['sentence']
                        break
                
                if supporting_sentence:
                    print(f"\nSupporting evidence: {supporting_sentence}")
            
            else:
                # Fall back to most common percentage overall
                most_common = percentage_counts.most_common(1)[0]
                most_likely_minimum = most_common[0]
                frequency = most_common[1]
                
                print(f"\n*** MOST COMMONLY MENTIONED BUTTERFAT PERCENTAGE: {most_likely_minimum}% ***")
                print(f"Mentioned {frequency} time(s) in butterfat contexts")
                
                # Find supporting sentence
                supporting_sentence = None
                for item in federal_percentages_found:
                    if float(item['percentage']) == most_likely_minimum:
                        supporting_sentence = item['sentence']
                        break
                
                if supporting_sentence:
                    print(f"\nSupporting evidence: {supporting_sentence}")
            
            # Save the final analysis
            final_result = {
                'analysis_date': datetime.now().isoformat(),
                'source': 'Wikipedia Ice cream page (complete article)',
                'objective': 'US federal minimum butterfat percentage for ice cream classification',
                'content_analyzed': f'{len(full_article_text):,} characters',
                'butterfat_sentences_found': len(butterfat_sentences),
                'federal_standard_sentences': len(federal_standard_sentences) if 'federal_standard_sentences' in locals() else 0,
                'percentage_extractions': federal_percentages_found,
                'federal_minimum_butterfat_percentage': most_likely_minimum if 'most_likely_minimum' in locals() else None,
                'supporting_evidence': supporting_sentence if 'supporting_sentence' in locals() else None,
                'all_percentages_found': list(percentage_counts.keys()) if 'percentage_counts' in locals() else []
            }
            
            result_file = os.path.join(workspace_dir, 'us_federal_ice_cream_butterfat_standard_final.json')
            with open(result_file, 'w') as f:
                json.dump(final_result, f, indent=2)
            
            print(f"\nFinal analysis saved to: {result_file}")
            
            if 'most_likely_minimum' in locals():
                print(f"\n=== PLAN OBJECTIVE COMPLETED ===")
                print(f"US Federal Minimum Butterfat Content for Ice cream: {most_likely_minimum}%")
                print(f"Source: Wikipedia Ice cream page (2020 information)")
                print(f"Analysis: Complete article content ({len(full_article_text):,} characters)")
        
        else:
            print(f"\nNo specific federal butterfat percentages found in the complete article.")
            print(f"The Wikipedia page may not contain detailed US federal standards.")
            print(f"Consider searching for more specific regulatory sources.")
    
    else:
        print(f"\nInsufficient content retrieved for analysis.")
        print(f"Content length: {len(full_article_text) if full_article_text else 0} characters")

except Exception as e:
    print(f"Error during comprehensive Wikipedia analysis: {e}")
    import traceback
    traceback.print_exc()

print("\n=== COMPREHENSIVE WIKIPEDIA ANALYSIS COMPLETE ===")
```

### Development Step 6: Title:  
Calculate Ice Cream Butterfat %, Compare to 10% US Standard, and Find % Difference (+/-)

**Description**: Calculate the actual butterfat percentage of the ice cream product from the extracted nutritional data (21g total fat per 144g serving) and compare it against the US federal standard of 10% minimum butterfat content. Determine the percentage difference above or below the federal standard and express the answer as +/- a number rounded to one decimal place as requested in the TASK.

**Use Cases**:
- Quality assurance testing in a dairy manufacturing plant to verify ice cream batches meet federal butterfat standards before shipment
- Regulatory compliance audits by food safety inspectors to assess whether retail ice cream products adhere to FDA butterfat requirements
- Product development in an R&D lab, where food scientists compare new ice cream formulations against legal butterfat thresholds
- Automated nutritional labeling systems in packaging facilities to ensure accurate butterfat percentage is printed and compliant
- Competitive market analysis by consumer advocacy groups to benchmark butterfat content across brands and report non-compliance
- Procurement decision-making for grocery chains, using butterfat analysis to select suppliers whose products exceed federal standards
- Custom recipe validation for artisanal ice cream shops, confirming homemade products meet minimum butterfat content for legal sale
- Academic research projects in food science departments, analyzing the impact of butterfat levels on texture and regulatory status

```
import os
import json
from datetime import datetime

print("=== CALCULATING ICE CREAM BUTTERFAT PERCENTAGE AND FEDERAL COMPLIANCE ===")
print("Objective: Calculate actual butterfat percentage and compare against 10% federal standard")
print("Data: 21g total fat per 144g serving vs 10% federal minimum\n")

# Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# First, let's inspect existing workspace files to understand what data we have
print("=== STEP 1: INSPECTING EXISTING WORKSPACE DATA ===")

if os.path.exists(workspace_dir):
    workspace_files = os.listdir(workspace_dir)
    print(f"Files in workspace: {len(workspace_files)}")
    
    for file in workspace_files:
        file_path = os.path.join(workspace_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
    
    # Check if we have the ice cream product analysis
    product_analysis_file = os.path.join(workspace_dir, 'ice_cream_product_analysis.txt')
    if os.path.exists(product_analysis_file):
        print(f"\nFound product analysis file: {product_analysis_file}")
        with open(product_analysis_file, 'r', encoding='utf-8') as f:
            analysis_content = f.read()
        print(f"Analysis content length: {len(analysis_content):,} characters")
        print(f"Preview (first 300 chars): {analysis_content[:300]}...")
    
    # Check if we have the federal standard data
    federal_standard_file = os.path.join(workspace_dir, 'us_federal_ice_cream_butterfat_standard_corrected.json')
    if os.path.exists(federal_standard_file):
        print(f"\nFound federal standard file: {federal_standard_file}")
        
        # Inspect the JSON structure first
        with open(federal_standard_file, 'r') as f:
            federal_data = json.load(f)
        
        print("Federal standard file structure:")
        for key, value in federal_data.items():
            if isinstance(value, list):
                print(f"  {key}: List with {len(value)} items")
            elif isinstance(value, dict):
                print(f"  {key}: Dictionary with {len(value)} keys")
            else:
                print(f"  {key}: {value}")
        
        # Extract the federal minimum percentage
        federal_minimum = federal_data.get('corrected_federal_minimum_butterfat_percentage')
        print(f"\nFederal minimum butterfat percentage: {federal_minimum}%")
else:
    print("No workspace directory found")

# Now calculate the actual butterfat percentage from the extracted nutritional data
print("\n=== STEP 2: CALCULATING ACTUAL BUTTERFAT PERCENTAGE ===")

# From the extracted nutritional data:
# - Serving size: 2/3 cup (144g)
# - Total fat per serving: 21g

serving_size_grams = 144
total_fat_grams = 21

print(f"Nutritional data from ice cream product:")
print(f"  Serving size: {serving_size_grams}g")
print(f"  Total fat per serving: {total_fat_grams}g")

# Calculate the fat percentage
actual_fat_percentage = (total_fat_grams / serving_size_grams) * 100

print(f"\nCalculation:")
print(f"  Fat percentage = (Total fat ÷ Serving size) × 100")
print(f"  Fat percentage = ({total_fat_grams}g ÷ {serving_size_grams}g) × 100")
print(f"  Fat percentage = {actual_fat_percentage:.4f}%")
print(f"  Fat percentage = {actual_fat_percentage:.1f}% (rounded to 1 decimal place)")

print(f"\n*** ACTUAL BUTTERFAT PERCENTAGE: {actual_fat_percentage:.1f}% ***")

# Compare against the federal standard
print("\n=== STEP 3: COMPARING AGAINST US FEDERAL STANDARD ===")

# Use the federal minimum we extracted (10%)
federal_minimum_percentage = 10.0

print(f"US Federal minimum butterfat standard: {federal_minimum_percentage}%")
print(f"Actual ice cream butterfat percentage: {actual_fat_percentage:.1f}%")

# Calculate the difference
percentage_difference = actual_fat_percentage - federal_minimum_percentage

print(f"\nComparison:")
print(f"  Difference = Actual percentage - Federal minimum")
print(f"  Difference = {actual_fat_percentage:.1f}% - {federal_minimum_percentage}%")
print(f"  Difference = {percentage_difference:.1f} percentage points")

# Determine if it meets the standard
if actual_fat_percentage >= federal_minimum_percentage:
    compliance_status = "EXCEEDS"
    difference_sign = "+"
else:
    compliance_status = "BELOW"
    difference_sign = "-"
    percentage_difference = abs(percentage_difference)  # Make positive for display

print(f"\n*** FEDERAL COMPLIANCE ANALYSIS ***")
print(f"Ice cream product {compliance_status} federal standard")
print(f"Difference: {difference_sign}{percentage_difference:.1f} percentage points")

# Express as requested format (+/- number rounded to one decimal place)
final_answer = f"{difference_sign}{percentage_difference:.1f}"

print(f"\n=== FINAL ANSWER ===")
print(f"Actual butterfat percentage: {actual_fat_percentage:.1f}%")
print(f"Federal standard: {federal_minimum_percentage}%")
print(f"Difference from federal standard: {final_answer}")

# Save the complete analysis
analysis_result = {
    'analysis_date': datetime.now().isoformat(),
    'objective': 'Calculate actual butterfat percentage and compare against US federal standard',
    'nutritional_data': {
        'serving_size_grams': serving_size_grams,
        'total_fat_grams': total_fat_grams,
        'source': 'Ice cream product nutrition label analysis'
    },
    'calculations': {
        'actual_butterfat_percentage': round(actual_fat_percentage, 1),
        'calculation_method': '(total_fat_grams / serving_size_grams) * 100',
        'raw_percentage': actual_fat_percentage
    },
    'federal_standard': {
        'minimum_butterfat_percentage': federal_minimum_percentage,
        'source': 'US FDA regulations (Wikipedia 2020)',
        'regulatory_authority': 'FDA (Food and Drug Administration)'
    },
    'compliance_analysis': {
        'meets_federal_standard': actual_fat_percentage >= federal_minimum_percentage,
        'compliance_status': compliance_status,
        'percentage_difference': round(actual_fat_percentage - federal_minimum_percentage, 1),
        'difference_from_standard': final_answer
    },
    'final_answer': {
        'format_requested': '+/- number rounded to one decimal place',
        'result': final_answer,
        'interpretation': f'Ice cream {compliance_status.lower()} federal standard by {abs(percentage_difference):.1f} percentage points'
    }
}

result_file = os.path.join(workspace_dir, 'ice_cream_butterfat_compliance_analysis.json')
with open(result_file, 'w') as f:
    json.dump(analysis_result, f, indent=2)

print(f"\nComplete analysis saved to: {result_file}")

# Also create a summary text file
summary_file = os.path.join(workspace_dir, 'butterfat_analysis_summary.txt')
with open(summary_file, 'w') as f:
    f.write("ICE CREAM BUTTERFAT PERCENTAGE ANALYSIS\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write("NUTRITIONAL DATA:\n")
    f.write(f"  Serving Size: {serving_size_grams}g\n")
    f.write(f"  Total Fat: {total_fat_grams}g\n\n")
    f.write("CALCULATIONS:\n")
    f.write(f"  Actual Butterfat Percentage: {actual_fat_percentage:.1f}%\n")
    f.write(f"  Calculation: ({total_fat_grams}g ÷ {serving_size_grams}g) × 100\n\n")
    f.write("FEDERAL STANDARD:\n")
    f.write(f"  US Federal Minimum: {federal_minimum_percentage}%\n")
    f.write(f"  Regulatory Authority: FDA\n\n")
    f.write("COMPLIANCE ANALYSIS:\n")
    f.write(f"  Status: {compliance_status} federal standard\n")
    f.write(f"  Difference: {final_answer} percentage points\n\n")
    f.write("FINAL ANSWER:\n")
    f.write(f"  {final_answer}\n")

print(f"Summary saved to: {summary_file}")

print(f"\n=== PLAN OBJECTIVE COMPLETED ===")
print(f"The ice cream product contains {actual_fat_percentage:.1f}% butterfat")
print(f"This is {final_answer} percentage points relative to the 10% federal standard")
print(f"Answer format: {final_answer} (as requested: +/- number rounded to one decimal place)")
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
2025-08-14 03:13:15
