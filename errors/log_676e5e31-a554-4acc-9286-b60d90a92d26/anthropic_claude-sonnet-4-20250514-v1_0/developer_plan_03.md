# Developer Plan 03

## Plan
Research alternative access methods to obtain the complete content of the verified July 2, 1959 USDA standards document. Try accessing the document through USDA Agricultural Marketing Service archives, National Archives (NARA), HathiTrust Digital Library, or university agricultural library collections. Focus on finding a version that allows full text extraction of the 'dried and dehydrated section' and 'Frozen/Chilled section' to identify the specific standards that meet the TASK criteria.

## Description
This is the necessary next step because: (1) The developer successfully located and verified the 1959 USDA document through Google Books but encountered access restrictions preventing content extraction, (2) We need the actual content from both sections to identify qualifying standards before researching their supersession status, (3) Expected outcome is to access the complete document through alternative government or academic archives that provide full text access, (4) This will enable us to extract the baseline list of standards needed to calculate the supersession percentage as of August 2023

## Episodic Examples
### Development Step 3: Confirm 2011 Extractive Metallurgy of Ni, Co, PGM Includes Lithium Calcination and Two-Stage Bioleaching

**Description**: Verify the identified 2011 Elsevier publication 'Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals' by conducting a targeted search to confirm it specifically covers both the calcination process with lithium salts for recovering metals from spent automotive catalysts AND the two-stage bioleaching method using Acidithiobacillus thiooxidans for low-grade cobalt ores. Search for the book's table of contents, chapter summaries, or detailed reviews that explicitly mention these two specific processes. Cross-reference with academic databases, publisher catalogs, and technical literature citations to ensure this publication contains both required methodologies described in the TASK.

**Use Cases**:
- Patent due diligence for materials science: verifying that a 2022 WO patent application covers both reinforced polymer composites and flame-retardant additive processing steps by targeted SerpAPI queries to patent office and scholarly sources
- Pharmaceutical guideline confirmation: ensuring the 2020 WHO monograph explicitly includes renal dosage adjustment protocols and adverse reaction monitoring procedures by searching chapter summaries and section titles
- Automotive supplier audit: confirming an ISO/TS 16949 supplier manual online covers both heat-treatment procedures for chassis parts and corrosion-resistance testing protocols using focused Google searches
- Open-source software compliance check: verifying that a cryptography library’s documentation details both RSA key generation methods and AES-GCM encryption usage via structured search queries on GitHub Pages and developer blogs
- Market intelligence white-paper analysis: ensuring a competitor’s 2021 market study contains consumer behavior segmentation for North America and side-by-side feature comparisons with key rivals by scanning executive summaries and table of contents
- Academic textbook syllabus alignment: confirming a 2023 engineering thermodynamics textbook includes both entropy analysis chapters and exergy efficiency case studies as mandated by a university course outline
- GDPR compliance verification: checking that the EU’s official GDPR guidelines PDF addresses both data subject access rights and data breach notification requirements by targeted searches of section headings and legal commentary
- Environmental impact report validation: verifying that a 2019 EPA assessment document covers both greenhouse gas emission quantification methods and carbon capture technology evaluations through focused online catalog and summary searches

```
import os
import requests
import json
from datetime import datetime

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print("API key found, proceeding with targeted verification search...")
    print("=" * 80)
    print("VERIFYING 2011 ELSEVIER PUBLICATION: 'Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals'")
    print("=" * 80)
    
    # Define highly specific search queries to verify the publication contains both required processes
    verification_queries = [
        '"Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals" 2011 Elsevier calcination lithium salts automotive catalysts',
        '"Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals" 2011 bioleaching Acidithiobacillus thiooxidans cobalt',
        '"Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals" table of contents chapters',
        '"Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals" 2011 Elsevier review summary',
        'Elsevier 2011 "calcination process lithium salts" "spent automotive catalysts" nickel cobalt platinum',
        'Elsevier 2011 "two-stage bioleaching" "Acidithiobacillus thiooxidans" "low-grade cobalt ores"',
        '"Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals" publisher catalog description',
        'ScienceDirect "Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals" 2011 chapters'
    ]
    
    print(f"Executing {len(verification_queries)} targeted verification searches...\n")
    
    # Store all verification results
    verification_results = []
    
    for i, query in enumerate(verification_queries, 1):
        print(f"Verification Search {i}/{len(verification_queries)}: {query}")
        print("-" * 60)
        
        # Prepare API request parameters
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 15,  # Increased number for better coverage
            "type": "search"
        }
        
        try:
            # Make API request to SerpAPI
            response = requests.get("https://serpapi.com/search.json", params=params, timeout=30)
            
            if response.status_code == 200:
                results = response.json()
                
                if results.get("organic_results"):
                    print(f"Found {len(results['organic_results'])} results")
                    
                    # Store results with query context
                    query_results = {
                        'query': query,
                        'results': results['organic_results'],
                        'search_number': i,
                        'timestamp': datetime.now().isoformat()
                    }
                    verification_results.append(query_results)
                    
                    # Display and analyze top results for this query
                    relevant_found = False
                    for j, result in enumerate(results['organic_results'][:8], 1):
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No URL')
                        snippet = result.get('snippet', 'No snippet')
                        
                        # Check for highly relevant indicators
                        title_lower = title.lower()
                        snippet_lower = snippet.lower()
                        combined_text = f"{title_lower} {snippet_lower}"
                        
                        # Key indicators for the specific publication
                        key_indicators = [
                            'extractive metallurgy of nickel, cobalt and platinum-group metals',
                            'calcination process',
                            'lithium salts',
                            'automotive catalysts',
                            'bioleaching',
                            'acidithiobacillus thiooxidans',
                            'cobalt ores',
                            'elsevier',
                            '2011'
                        ]
                        
                        matching_indicators = [ind for ind in key_indicators if ind in combined_text]
                        
                        print(f"\n  Result {j}:")
                        print(f"    Title: {title}")
                        print(f"    URL: {link}")
                        print(f"    Snippet: {snippet[:300]}{'...' if len(snippet) > 300 else ''}")
                        
                        if matching_indicators:
                            print(f"    ⭐ MATCHING INDICATORS: {', '.join(matching_indicators)}")
                            relevant_found = True
                            
                            # Special attention to publisher sites, academic databases, and book catalogs
                            if any(domain in link.lower() for domain in ['elsevier', 'sciencedirect', 'springer', 'wiley', 'worldcat', 'amazon', 'google.com/books']):
                                print(f"    🎯 HIGH-PRIORITY SOURCE: Publisher/Academic database result")
                    
                    if not relevant_found:
                        print("    No highly relevant results found for this query")
                        
                else:
                    print("No organic results found for this query")
                    verification_results.append({
                        'query': query,
                        'results': [],
                        'search_number': i,
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                print(f"Error: API request failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Error during verification search {i}: {str(e)}")
            continue
        
        print("\n")
    
    print("\n" + "=" * 80)
    print("VERIFICATION ANALYSIS SUMMARY")
    print("=" * 80)
    
    # Save all verification results to workspace for detailed analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"workspace/elsevier_2011_verification_results_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'publication_title': 'Extractive Metallurgy of Nickel, Cobalt and Platinum-Group Metals',
            'publication_year': '2011',
            'publisher': 'Elsevier',
            'verification_timestamp': timestamp,
            'total_queries': len(verification_queries),
            'queries_executed': verification_queries,
            'verification_results': verification_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Verification results saved to: {results_file}")
    
    # Analyze findings
    total_results = sum(len(query_result['results']) for query_result in verification_results)
    print(f"Total verification results collected: {total_results}")
    
    # Look for direct publication matches
    direct_matches = []
    calcination_mentions = []
    bioleaching_mentions = []
    elsevier_2011_matches = []
    
    for query_result in verification_results:
        for result in query_result['results']:
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            link = result.get('link', '').lower()
            combined = f"{title} {snippet} {link}"
            
            # Direct publication title matches
            if 'extractive metallurgy of nickel, cobalt and platinum-group metals' in combined:
                direct_matches.append({
                    'query': query_result['query'],
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })
            
            # Calcination process mentions
            if 'calcination' in combined and ('lithium' in combined or 'automotive' in combined or 'catalyst' in combined):
                calcination_mentions.append({
                    'query': query_result['query'],
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })
            
            # Bioleaching mentions
            if 'bioleaching' in combined and ('acidithiobacillus' in combined or 'thiooxidans' in combined or 'cobalt' in combined):
                bioleaching_mentions.append({
                    'query': query_result['query'],
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })
            
            # Elsevier 2011 matches
            if 'elsevier' in combined and '2011' in combined:
                elsevier_2011_matches.append({
                    'query': query_result['query'],
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet')
                })
    
    print(f"\n📊 VERIFICATION FINDINGS:")
    print(f"Direct publication title matches: {len(direct_matches)}")
    print(f"Calcination process mentions: {len(calcination_mentions)}")
    print(f"Bioleaching process mentions: {len(bioleaching_mentions)}")
    print(f"Elsevier 2011 matches: {len(elsevier_2011_matches)}")
    
    if direct_matches:
        print(f"\n🎯 DIRECT PUBLICATION MATCHES FOUND:")
        for i, match in enumerate(direct_matches[:5], 1):
            print(f"  {i}. {match['title']}")
            print(f"     URL: {match['link']}")
            print(f"     Query: {match['query']}")
            print(f"     Snippet: {match['snippet'][:200]}...")
            print()
    
    if calcination_mentions:
        print(f"\n⚗️ CALCINATION PROCESS MENTIONS:")
        for i, mention in enumerate(calcination_mentions[:3], 1):
            print(f"  {i}. {mention['title']}")
            print(f"     Snippet: {mention['snippet'][:150]}...")
            print()
    
    if bioleaching_mentions:
        print(f"\n🦠 BIOLEACHING PROCESS MENTIONS:")
        for i, mention in enumerate(bioleaching_mentions[:3], 1):
            print(f"  {i}. {mention['title']}")
            print(f"     Snippet: {mention['snippet'][:150]}...")
            print()
    
    print(f"\n📋 VERIFICATION STATUS:")
    if direct_matches and (calcination_mentions or bioleaching_mentions):
        print("✅ PUBLICATION IDENTIFIED with some process mentions")
        print("   - Direct publication matches found")
        print("   - Some relevant process mentions detected")
        print("   - Requires deeper analysis of specific chapters/content")
    elif direct_matches:
        print("⚠️ PUBLICATION IDENTIFIED but limited process verification")
        print("   - Direct publication matches found")
        print("   - Limited specific process mentions")
        print("   - May require access to full publication content")
    else:
        print("❌ LIMITED VERIFICATION RESULTS")
        print("   - No direct publication title matches")
        print("   - May need alternative search strategies")
        print("   - Publication may not be widely indexed or accessible")
    
    print(f"\nDetailed verification data saved to: {results_file}")
    print("Ready for next phase: detailed content analysis if publication is confirmed.")
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

### Development Step 3: 2016 Uganda SPFMV/SPCSV Testing Methods: Reagents and EC Numbers

**Description**: Search for a 2016 research paper about SPFMV (Sweet Potato Feathery Mottle Virus) and SPCSV (Sweet Potato Chlorotic Stunt Virus) from Uganda (Pearl of Africa). Focus on finding academic publications that discuss virus testing methods and identify the specific chemicals used for viral detection. Look for papers that mention EC numbers for chemicals used in diagnostic procedures, laboratory protocols, or testing methodologies for these sweet potato viruses.

**Use Cases**:
- Agricultural extension services automating literature scanning to update diagnostic protocols for sweet potato virus testing in East African labs
- Pharmaceutical R&D teams extracting EC number references from global research databases to streamline enzyme assay development for antiviral compounds
- Government agriculture ministries compiling academic sources and chemical methodologies to standardize national surveillance of SPFMV and SPCSV in staple crops
- Biotechnology startups conducting automated patent and article analysis to identify emerging viral detection reagents and EC-classified enzymes for new diagnostic kits
- University virology courses using JSON-based search result parsing to teach students hands-on research workflows and data categorization techniques
- Data science consultancies performing bulk processing of literature search outputs to build a searchable database of virus diagnostic protocols and chemical identifiers
- Nonprofit agricultural research organizations monitoring Uganda-specific SPFMV/SPCSV publications to inform funding decisions and field trial designs
- Environmental monitoring agencies integrating automated search analysis into accreditation pipelines to flag novel virus testing methods and EC numbers for laboratory compliance standards

```
import os
import json
from datetime import datetime

# First, let's inspect the search results file to understand its structure before analysis
print("=" * 80)
print("INSPECTING SEARCH RESULTS FILE STRUCTURE")
print("=" * 80)

# Find the most recent search results file
workspace_files = []
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        if file.startswith('uganda_spfmv_spcsv_2016_search_results_') and file.endswith('.json'):
            workspace_files.append(file)
            print(f"Found search results file: {file}")

if not workspace_files:
    print("No search results files found. Let me check what's in the workspace:")
    if os.path.exists('workspace'):
        all_files = os.listdir('workspace')
        print(f"Files in workspace: {all_files}")
    else:
        print("Workspace directory does not exist")
else:
    # Use the most recent file (they're timestamped)
    latest_file = sorted(workspace_files)[-1]
    results_file = f'workspace/{latest_file}'
    
    print(f"\nAnalyzing file: {results_file}")
    
    # First, inspect the file structure
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\nFile structure overview:")
    print(f"Top-level keys: {list(data.keys())}")
    
    if 'search_target' in data:
        print(f"Search target: {data['search_target']}")
    
    if 'search_results' in data:
        print(f"Number of search result sets: {len(data['search_results'])}")
        if len(data['search_results']) > 0:
            sample_result = data['search_results'][0]
            print(f"Sample search result structure: {list(sample_result.keys())}")
            if 'results' in sample_result and len(sample_result['results']) > 0:
                sample_individual_result = sample_result['results'][0]
                print(f"Sample individual result structure: {list(sample_individual_result.keys())}")
    
    print("\n" + "=" * 80)
    print("DETAILED ANALYSIS OF SEARCH RESULTS - CORRECTED VERSION")
    print("=" * 80)
    
    # Now properly analyze the content with corrected variable scoping
    high_relevance_results = []
    uganda_specific_results = []
    both_viruses_results = []
    methodology_results = []
    academic_sources = []
    pdf_sources = []
    ec_number_results = []
    wiley_paper_results = []
    huggingface_results = []
    
    total_results = 0
    
    # Process each search query's results
    for query_data in data['search_results']:
        query = query_data.get('query', '')
        results = query_data.get('results', [])
        total_results += len(results)
        
        print(f"\nProcessing Query: {query}")
        print(f"Results found: {len(results)}")
        print("-" * 60)
        
        for result in results:
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            result_link = result.get('link', '').lower()
            
            # FIXED: Define combined variable properly in this scope
            combined = f"{title} {snippet} {result_link}"
            
            result_with_context = {
                'query': query,
                'title': result.get('title'),
                'link': result.get('link'),
                'snippet': result.get('snippet')
            }
            
            # Calculate relevance score
            relevance_score = 0
            if 'spfmv' in combined: relevance_score += 1
            if 'spcsv' in combined: relevance_score += 1
            if 'uganda' in combined: relevance_score += 1
            if '2016' in combined: relevance_score += 1
            if any(term in combined for term in ['testing', 'diagnostic', 'chemical', 'detection']): relevance_score += 1
            
            # Categorize results
            if relevance_score >= 3:
                high_relevance_results.append({**result_with_context, 'relevance_score': relevance_score})
            
            # Uganda-specific results
            if 'uganda' in combined or 'pearl of africa' in combined:
                uganda_specific_results.append(result_with_context)
            
            # Both viruses mentioned
            if 'spfmv' in combined and 'spcsv' in combined:
                both_viruses_results.append(result_with_context)
            
            # Methodology/testing focus
            if any(term in combined for term in ['testing', 'diagnostic', 'methodology', 'protocol', 'chemical', 'ec number']):
                methodology_results.append(result_with_context)
            
            # Academic sources
            if any(domain in result_link for domain in ['researchgate', 'pubmed', 'ncbi', 'sciencedirect', 'springer', 'wiley', '.edu', 'doi.org', 'core.ac.uk']):
                academic_sources.append(result_with_context)
            
            # PDF sources
            if '.pdf' in result_link:
                pdf_sources.append(result_with_context)
            
            # EC number specific results
            if 'ec number' in combined or any(ec_pattern in combined for ec_pattern in ['1.11.1.7', '3.1.3.1']):
                ec_number_results.append(result_with_context)
            
            # Specific target results
            if 'wiley.com' in result_link and 'jph.12451' in result_link:
                wiley_paper_results.append(result_with_context)
            
            if 'huggingface.co' in result_link and ('1.11.1.7' in combined or '3.1.3.1' in combined):
                huggingface_results.append(result_with_context)
    
    # Sort high relevance results by score
    high_relevance_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"\n📊 COMPREHENSIVE RESULTS CATEGORIZATION:")
    print(f"Total search results processed: {total_results}")
    print(f"High Relevance Results (3+ matching criteria): {len(high_relevance_results)}")
    print(f"Uganda-Specific Results: {len(uganda_specific_results)}")
    print(f"Both Viruses Mentioned: {len(both_viruses_results)}")
    print(f"Methodology/Testing Focus: {len(methodology_results)}")
    print(f"Academic Sources: {len(academic_sources)}")
    print(f"PDF Sources: {len(pdf_sources)}")
    print(f"EC Number Specific Results: {len(ec_number_results)}")
    print(f"Target Wiley Paper Results: {len(wiley_paper_results)}")
    print(f"Hugging Face Dataset Results: {len(huggingface_results)}")
    
    # Display key findings
    if high_relevance_results:
        print(f"\n🎯 TOP HIGH-RELEVANCE RESULTS:")
        for i, result in enumerate(high_relevance_results[:5], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     URL: {result['link']}")
            print(f"     Relevance Score: {result['relevance_score']}/5")
            print(f"     Query: {result['query']}")
            print(f"     Snippet: {result['snippet'][:200]}...")
    
    if wiley_paper_results:
        print(f"\n📄 TARGET WILEY PAPER FOUND:")
        for result in wiley_paper_results:
            print(f"  Title: {result['title']}")
            print(f"  URL: {result['link']}")
            print(f"  Snippet: {result['snippet'][:300]}...")
    
    if huggingface_results:
        print(f"\n🤗 HUGGING FACE DATASET WITH EC NUMBERS:")
        for result in huggingface_results:
            print(f"  Title: {result['title']}")
            print(f"  URL: {result['link']}")
            print(f"  Snippet: {result['snippet'][:300]}...")
    
    if ec_number_results:
        print(f"\n🧪 EC NUMBER SPECIFIC RESULTS:")
        for i, result in enumerate(ec_number_results[:5], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     URL: {result['link']}")
            print(f"     Snippet: {result['snippet'][:200]}...")
    
    # Look for the specific EC numbers mentioned in the tester feedback
    ec_numbers_found = []
    for query_data in data['search_results']:
        for result in query_data['results']:
            snippet = result.get('snippet', '')
            if '1.11.1.7' in snippet and '3.1.3.1' in snippet:
                ec_numbers_found.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': snippet,
                    'query': query_data.get('query')
                })
    
    if ec_numbers_found:
        print(f"\n🔬 SPECIFIC EC NUMBERS (1.11.1.7 & 3.1.3.1) FOUND:")
        for result in ec_numbers_found:
            print(f"  Title: {result['title']}")
            print(f"  URL: {result['link']}")
            print(f"  Snippet: {result['snippet']}")
            print(f"  Source Query: {result['query']}")
    
    print(f"\n" + "=" * 80)
    print("FINAL SEARCH ASSESSMENT")
    print("=" * 80)
    
    # Create comprehensive assessment
    assessment = {
        'search_completed': True,
        'total_results': total_results,
        'high_relevance_count': len(high_relevance_results),
        'target_paper_found': len(wiley_paper_results) > 0,
        'ec_numbers_found': len(ec_numbers_found) > 0,
        'academic_sources_count': len(academic_sources),
        'methodology_results_count': len(methodology_results),
        'specific_ec_numbers': ['1.11.1.7', '3.1.3.1'] if ec_numbers_found else [],
        'key_findings': {
            'wiley_paper_identified': len(wiley_paper_results) > 0,
            'huggingface_dataset_found': len(huggingface_results) > 0,
            'uganda_research_confirmed': len(uganda_specific_results) > 0,
            'both_viruses_mentioned': len(both_viruses_results) > 0,
            'testing_methodology_focus': len(methodology_results) > 0
        }
    }
    
    print(f"✅ Search Status: {'SUCCESSFUL' if assessment['search_completed'] else 'INCOMPLETE'}")
    print(f"📊 Total Results: {assessment['total_results']}")
    print(f"🎯 High Relevance Results: {assessment['high_relevance_count']}")
    print(f"📄 Target Paper Found: {'YES' if assessment['target_paper_found'] else 'NO'}")
    print(f"🧪 EC Numbers Found: {'YES' if assessment['ec_numbers_found'] else 'NO'}")
    print(f"📚 Academic Sources: {assessment['academic_sources_count']}")
    print(f"🔬 Methodology Results: {assessment['methodology_results_count']}")
    
    if assessment['specific_ec_numbers']:
        print(f"🔍 Specific EC Numbers Identified: {', '.join(assessment['specific_ec_numbers'])}")
    
    print(f"\n📋 KEY RESEARCH TARGETS IDENTIFIED:")
    for key, value in assessment['key_findings'].items():
        status = "✅ FOUND" if value else "❌ NOT FOUND"
        print(f"  {key.replace('_', ' ').title()}: {status}")
    
    # Save comprehensive analysis
    analysis_file = f'workspace/uganda_spfmv_spcsv_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    analysis_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'source_file': results_file,
        'assessment': assessment,
        'categorized_results': {
            'high_relevance': high_relevance_results,
            'uganda_specific': uganda_specific_results,
            'both_viruses': both_viruses_results,
            'methodology_focus': methodology_results,
            'academic_sources': academic_sources,
            'pdf_sources': pdf_sources,
            'ec_number_results': ec_number_results,
            'wiley_paper_results': wiley_paper_results,
            'huggingface_results': huggingface_results,
            'specific_ec_numbers_found': ec_numbers_found
        }
    }
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nComprehensive analysis saved to: {analysis_file}")
    print("\n🎯 NEXT STEPS RECOMMENDATION:")
    
    if assessment['target_paper_found'] and assessment['ec_numbers_found']:
        print("✅ SUCCESS: Both target paper and EC numbers identified")
        print("   - Wiley paper about SPFMV/SPCSV effects in Uganda located")
        print("   - Specific EC numbers (1.11.1.7, 3.1.3.1) found in Hugging Face dataset")
        print("   - Ready to extract detailed chemical information from sources")
    elif assessment['target_paper_found']:
        print("⚠️ PARTIAL SUCCESS: Target paper found but EC numbers need verification")
        print("   - Focus on accessing full paper content for chemical details")
    else:
        print("❌ ADDITIONAL SEARCH NEEDED: Target paper not clearly identified")
        print("   - Consider alternative search strategies or direct database access")
    
    print("\nSearch analysis completed successfully with corrected variable scoping.")
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

## Created Time
2025-08-13 18:55:33
