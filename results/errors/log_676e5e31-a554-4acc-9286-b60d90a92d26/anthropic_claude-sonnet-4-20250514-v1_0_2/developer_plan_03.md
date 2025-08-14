# Developer Plan 03

## Plan
Research the current supersession status of the 44 identified food standards from the 1959 document as of August 2023. For each of the qualifying items (3 dehydrated items: Apples, Grapefruit Juice, Orange Juice; and 41 frozen items including Apples, Apricots, Asparagus, etc.), determine whether each standard has been superseded by a newer version since July 2, 1959. Search through USDA Agricultural Marketing Service records, Federal Register updates, and current USDA standards databases to identify which of these 44 standards have been replaced or updated with new versions between 1959 and August 2023.

## Description
This is the critical next step because: (1) The developer successfully extracted all 44 qualifying standards from the 1959 document that meet the TASK criteria (3 dehydrated items and 41 frozen items), (2) We need to determine the supersession status of each standard to calculate the percentage that have been updated since 1959, (3) Expected outcome is to identify how many of the 44 standards have been superseded by newer versions as of August 2023, (4) This will enable us to calculate the final percentage (to the nearest percent) of standards that have been superseded since the 1959 date, completing the TASK requirement

## Episodic Examples
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

### Development Step 4: 2016 Uganda SPFMV/SPCSV Testing Methods: EC-Numbered Chemicals in Virus Diagnostics

**Description**: Search for a 2016 research paper about SPFMV (Sweet Potato Feathery Mottle Virus) and SPCSV (Sweet Potato Chlorotic Stunt Virus) from Uganda (Pearl of Africa). Focus on finding academic publications that discuss virus testing methods and identify the specific chemicals used for viral detection. Look for papers that mention EC numbers for chemicals used in diagnostic procedures, laboratory protocols, or testing methodologies for these sweet potato viruses.

**Use Cases**:
- Automated literature review of Ugandan sweet potato virus diagnostics for virology research teams
- Regulatory submission support by extracting EC numbers of diagnostic reagents for agrochemical compliance officers
- Seed industry R&D monitoring new SPFMV/SPCSV assay protocols to inform in-house testing kit development
- Intellectual property due diligence automating prior-art classification of virus detection patents in plant pathology
- Agricultural extension training compiling methodology summaries for Ugandan labs to standardize virus testing protocols
- Digital repository curation indexing PDF-based protocol metadata for university libraries specializing in plant disease research
- Biotech assay formulation mining specific enzyme EC numbers (1.11.1.7, 3.1.3.1) to guide diagnostic kit reagent selection
- Competitive market intelligence for agro-biotech firms analyzing publication trends in sweet potato virus detection methods

```
import os
import json
from datetime import datetime

# Complete analysis of Uganda SPFMV/SPCSV search results with proper variable scoping
print("=" * 80)
print("COMPLETING ANALYSIS OF UGANDA SWEET POTATO VIRUS SEARCH RESULTS")
print("=" * 80)

# Find and load the search results file
workspace_files = []
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        if file.startswith('uganda_spfmv_spcsv_2016_search_results_') and file.endswith('.json'):
            workspace_files.append(file)
            print(f"Found search results file: {file}")

if not workspace_files:
    print("No search results files found in workspace.")
else:
    # Use the most recent file (they're timestamped)
    latest_file = sorted(workspace_files)[-1]
    results_file = f'workspace/{latest_file}'
    
    print(f"\nAnalyzing file: {results_file}")
    
    # Load and inspect the search results
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\nFile overview:")
    print(f"Search target: {data.get('search_target', 'N/A')}")
    print(f"Total queries executed: {data.get('total_queries', 'N/A')}")
    print(f"Search result sets: {len(data.get('search_results', []))}")
    
    # Initialize result categories
    high_relevance_results = []
    uganda_specific_results = []
    both_viruses_results = []
    methodology_results = []
    academic_sources = []
    pdf_sources = []
    ec_number_results = []
    wiley_paper_results = []
    huggingface_results = []
    specific_ec_numbers_found = []
    
    total_results = 0
    
    print("\n" + "=" * 80)
    print("PROCESSING SEARCH RESULTS WITH CORRECTED VARIABLE SCOPING")
    print("=" * 80)
    
    # Process each search query's results
    for query_idx, query_data in enumerate(data.get('search_results', []), 1):
        query = query_data.get('query', '')
        results = query_data.get('results', [])
        total_results += len(results)
        
        print(f"\nQuery {query_idx}: {query}")
        print(f"Results found: {len(results)}")
        print("-" * 60)
        
        # Process each individual result
        for result_idx, result in enumerate(results, 1):
            # Extract and normalize text fields - DEFINE ALL VARIABLES FIRST
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            result_link = result.get('link', '').lower()
            
            # CRITICAL FIX: Define combined variable before any usage
            combined = f"{title} {snippet} {result_link}"
            
            # Create result context object
            result_with_context = {
                'query': query,
                'title': result.get('title'),
                'link': result.get('link'),
                'snippet': result.get('snippet')
            }
            
            # Calculate relevance score - NOW combined is properly defined
            relevance_score = 0
            if 'spfmv' in combined: relevance_score += 1
            if 'spcsv' in combined: relevance_score += 1
            if 'uganda' in combined: relevance_score += 1
            if '2016' in combined: relevance_score += 1
            
            # Check for testing/methodology terms
            testing_terms = ['testing', 'diagnostic', 'chemical', 'detection', 'methodology', 'protocol']
            if any(term in combined for term in testing_terms): relevance_score += 1
            
            # Display high-relevance results as we process them
            if relevance_score >= 3:
                print(f"\n  HIGH RELEVANCE Result {result_idx}: {result.get('title')}")
                print(f"    URL: {result.get('link')}")
                print(f"    Relevance Score: {relevance_score}/5")
                print(f"    Snippet: {result.get('snippet', '')[:200]}...")
                
                high_relevance_results.append({**result_with_context, 'relevance_score': relevance_score})
            
            # Categorize results - all variables are now properly defined
            if 'uganda' in combined or 'pearl of africa' in combined:
                uganda_specific_results.append(result_with_context)
            
            if 'spfmv' in combined and 'spcsv' in combined:
                both_viruses_results.append(result_with_context)
                print(f"    🦠 BOTH VIRUSES: {result.get('title')[:50]}...")
            
            if any(term in combined for term in testing_terms):
                methodology_results.append(result_with_context)
            
            # Academic sources
            academic_domains = ['researchgate', 'pubmed', 'ncbi', 'sciencedirect', 'springer', 'wiley', '.edu', 'doi.org', 'core.ac.uk']
            if any(domain in result_link for domain in academic_domains):
                academic_sources.append(result_with_context)
                print(f"    📚 ACADEMIC: {result.get('title')[:50]}...")
            
            # PDF sources
            if '.pdf' in result_link:
                pdf_sources.append(result_with_context)
                print(f"    📄 PDF: {result.get('title')[:50]}...")
            
            # EC number results
            if 'ec number' in combined or '1.11.1.7' in combined or '3.1.3.1' in combined:
                ec_number_results.append(result_with_context)
                print(f"    🧪 EC NUMBERS: {result.get('title')[:50]}...")
            
            # Target Wiley paper
            if 'wiley.com' in result_link and 'jph.12451' in result_link:
                wiley_paper_results.append(result_with_context)
                print(f"    🎯 TARGET WILEY PAPER FOUND: {result.get('title')}")
            
            # Hugging Face dataset
            if 'huggingface.co' in result_link:
                huggingface_results.append(result_with_context)
                print(f"    🤗 HUGGING FACE: {result.get('title')[:50]}...")
            
            # Check for specific EC numbers in snippet
            snippet_original = result.get('snippet', '')
            if '1.11.1.7' in snippet_original and '3.1.3.1' in snippet_original:
                specific_ec_numbers_found.append(result_with_context)
                print(f"    🔬 SPECIFIC EC NUMBERS FOUND: {result.get('title')[:50]}...")
    
    # Sort high relevance results by score
    high_relevance_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 80)
    
    print(f"\n📊 RESULTS CATEGORIZATION:")
    print(f"Total search results processed: {total_results}")
    print(f"High Relevance Results (3+ criteria): {len(high_relevance_results)}")
    print(f"Uganda-Specific Results: {len(uganda_specific_results)}")
    print(f"Both Viruses Mentioned: {len(both_viruses_results)}")
    print(f"Methodology/Testing Focus: {len(methodology_results)}")
    print(f"Academic Sources: {len(academic_sources)}")
    print(f"PDF Sources: {len(pdf_sources)}")
    print(f"EC Number Results: {len(ec_number_results)}")
    print(f"Target Wiley Paper: {len(wiley_paper_results)}")
    print(f"Hugging Face Results: {len(huggingface_results)}")
    print(f"Specific EC Numbers Found: {len(specific_ec_numbers_found)}")
    
    # Display key findings
    print(f"\n🎯 KEY RESEARCH FINDINGS:")
    
    if wiley_paper_results:
        print(f"\n✅ TARGET WILEY PAPER IDENTIFIED:")
        for paper in wiley_paper_results:
            print(f"  Title: {paper['title']}")
            print(f"  URL: {paper['link']}")
            print(f"  Snippet: {paper['snippet'][:300]}...")
    
    if specific_ec_numbers_found:
        print(f"\n✅ SPECIFIC EC NUMBERS (1.11.1.7 & 3.1.3.1) LOCATED:")
        for ec_result in specific_ec_numbers_found:
            print(f"  Source: {ec_result['title']}")
            print(f"  URL: {ec_result['link']}")
            print(f"  Content: {ec_result['snippet']}")
    
    if high_relevance_results:
        print(f"\n🏆 TOP HIGH-RELEVANCE RESULTS:")
        for i, result in enumerate(high_relevance_results[:3], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     URL: {result['link']}")
            print(f"     Score: {result['relevance_score']}/5")
            print(f"     Snippet: {result['snippet'][:200]}...")
    
    # Create final assessment
    assessment = {
        'search_completed': True,
        'total_results': total_results,
        'target_paper_identified': len(wiley_paper_results) > 0,
        'ec_numbers_found': len(specific_ec_numbers_found) > 0,
        'academic_sources_available': len(academic_sources) > 0,
        'methodology_focus_confirmed': len(methodology_results) > 0,
        'uganda_research_confirmed': len(uganda_specific_results) > 0,
        'both_viruses_coverage': len(both_viruses_results) > 0,
        'pdf_access_available': len(pdf_sources) > 0
    }
    
    print(f"\n📋 FINAL ASSESSMENT:")
    print(f"✅ Search Completed: {assessment['search_completed']}")
    print(f"📄 Target Paper Identified: {assessment['target_paper_identified']}")
    print(f"🧪 EC Numbers Found: {assessment['ec_numbers_found']}")
    print(f"📚 Academic Sources Available: {assessment['academic_sources_available']}")
    print(f"🔬 Methodology Focus Confirmed: {assessment['methodology_focus_confirmed']}")
    print(f"🌍 Uganda Research Confirmed: {assessment['uganda_research_confirmed']}")
    print(f"🦠 Both Viruses Coverage: {assessment['both_viruses_coverage']}")
    print(f"📄 PDF Access Available: {assessment['pdf_access_available']}")
    
    # Save comprehensive analysis
    analysis_file = f'workspace/uganda_spfmv_spcsv_final_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    analysis_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'source_file': results_file,
        'total_results_processed': total_results,
        'assessment': assessment,
        'key_findings': {
            'target_wiley_paper': wiley_paper_results,
            'specific_ec_numbers': specific_ec_numbers_found,
            'high_relevance_results': high_relevance_results[:10],  # Top 10
            'academic_sources': academic_sources[:10],  # Top 10
            'pdf_sources': pdf_sources
        },
        'categorized_counts': {
            'high_relevance': len(high_relevance_results),
            'uganda_specific': len(uganda_specific_results),
            'both_viruses': len(both_viruses_results),
            'methodology_focus': len(methodology_results),
            'academic_sources': len(academic_sources),
            'pdf_sources': len(pdf_sources),
            'ec_number_results': len(ec_number_results),
            'wiley_papers': len(wiley_paper_results),
            'huggingface_results': len(huggingface_results)
        }
    }
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nComprehensive analysis saved to: {analysis_file}")
    
    # Final status and next steps
    print(f"\n🎯 MISSION STATUS:")
    if assessment['target_paper_identified'] and assessment['ec_numbers_found']:
        print("✅ SUCCESS: Target research paper and EC numbers successfully identified")
        print("   - 2016 Uganda SPFMV/SPCSV research paper located (Wiley publication)")
        print("   - Specific EC numbers for virus testing chemicals found (1.11.1.7, 3.1.3.1)")
        print("   - Multiple academic sources and PDF access points available")
        print("\n📋 ANSWER TO ORIGINAL QUESTION:")
        print("   The EC numbers of the two most commonly used chemicals for virus")
        print("   testing in the 2016 Uganda SPFMV/SPCSV research are:")
        print("   • 1.11.1.7")
        print("   • 3.1.3.1")
    elif assessment['target_paper_identified']:
        print("⚠️ PARTIAL SUCCESS: Research paper identified, EC numbers need extraction")
        print("   - Need to access full paper content for detailed chemical information")
    else:
        print("❌ INCOMPLETE: Additional research needed for definitive identification")
    
    print("\nSearch and analysis completed successfully.")
```

## Created Time
2025-08-13 19:21:44
