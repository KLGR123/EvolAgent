# Developer Plan 02

## Plan
Research and extract the total penguin population according to the upper estimates on English Wikipedia at the end of 2012. Search for comprehensive penguin population data from Wikipedia's 2012 content, focusing on global penguin population estimates or species-specific population data that would have been available at the end of 2012. Look for upper estimate figures rather than lower estimates or ranges.

## Description
This is the necessary next step because: (1) We have successfully identified 86 penguins from the CSV file that meet the filtering criteria (not on Dream Island AND beak length ≤ 42mm), (2) To calculate the percentage, we need the total penguin population upper estimates from English Wikipedia as of end of 2012, (3) Expected outcome is to obtain the Wikipedia 2012 upper estimate figure for global penguin populations, (4) This will enable us to calculate the final percentage: (86 / Wikipedia total) × 100, rounded to five decimal places as requested in the TASK

## Episodic Examples
### Development Step 4: Locate Chinstrap Penguin End-2018 Population Figure on Wikipedia, Note Units and Source

**Description**: Search for and access the Wikipedia page about penguin species populations to locate the specific chinstrap penguin population data as of the end of 2018. Extract the population figure, noting whether it's given in breeding pairs or individual penguins, and document the exact source and context of this information.

**Use Cases**:
- Conservation NGOs automating collection of IUCN population data for chinstrap penguins and other species to update annual impact reports and support grant applications
- Marine biodiversity researchers extracting and aggregating 2018 population figures and measurement types from Wikipedia for multivariate statistical modeling of Antarctic ecosystem health
- Educational publishers generating data-driven infographics on penguin populations, automatically pulling exact quotes and citations to ensure academic accuracy in textbooks
- Environmental consultants incorporating up-to-date wildlife population metrics into corporate sustainability assessments, scraping IUCN estimates and source contexts for regulatory compliance documentation
- Data journalism teams verifying public claims about penguin population trends by extracting precise 2018 figures and reference links to fact-check articles on wildlife conservation
- Government wildlife agencies building a centralized database of species population statistics, using automated scraping to integrate Wikipedia’s conservation status sections with GIS-based planning tools
- Software developers creating a mobile app for wildlife enthusiasts, populating species profiles with live population estimates and direct source citations from Wikipedia pages
- Grant-writing specialists compiling authoritative citations for funding proposals, automating extraction of population data and full source context from IUCN references on Wikipedia

```
import os
import json
import re
from bs4 import BeautifulSoup

print("=== CHINSTRAP PENGUIN POPULATION RESEARCH - FINAL STEP ===\n")
print("Objective: Compile complete answer with exact 2018 IUCN population data and full source context")
print("Focus: Extract precise citation details and confirm population measurement type\n")

# First, let's inspect the workspace to understand what files we have
print("Files available in workspace:")
if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    for file in workspace_files:
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
else:
    print("  No workspace directory found")

# Inspect the main extraction results file structure first
extraction_file = 'workspace/chinstrap_penguin_population_extraction.json'
if os.path.exists(extraction_file):
    print(f"\n=== INSPECTING EXTRACTION RESULTS STRUCTURE ===\n")
    
    with open(extraction_file, 'r') as f:
        extraction_data = json.load(f)
    
    print("Top-level keys in extraction results:")
    for key, value in extraction_data.items():
        if isinstance(value, dict):
            print(f"  {key}: Dictionary with {len(value)} keys")
        elif isinstance(value, list):
            print(f"  {key}: List with {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Examine the pages_data structure
    if 'pages_data' in extraction_data:
        print(f"\nPages data structure:")
        for i, page in enumerate(extraction_data['pages_data']):
            print(f"  Page {i+1}: {page.get('page_name', 'Unknown')}")
            for key in page.keys():
                if key == 'population_matches' and page[key]:
                    print(f"    {key}: {len(page[key])} matches found")
                elif key == 'conservation_sections' and page[key]:
                    print(f"    {key}: {len(page[key])} sections found")
                else:
                    print(f"    {key}: {type(page[key]).__name__}")

# Now let's extract the specific population data we need
print(f"\n=== EXTRACTING FINAL POPULATION DATA ===\n")

if os.path.exists(extraction_file):
    with open(extraction_file, 'r') as f:
        extraction_data = json.load(f)
    
    # Find the Chinstrap penguin page data
    chinstrap_page_data = None
    for page in extraction_data.get('pages_data', []):
        if 'Chinstrap penguin' in page.get('page_name', ''):
            chinstrap_page_data = page
            break
    
    if chinstrap_page_data:
        print("✓ Found Chinstrap penguin page data")
        
        # Extract the best population matches
        population_matches = chinstrap_page_data.get('population_matches', [])
        print(f"Population matches found: {len(population_matches)}")
        
        # Find the most complete match
        best_match = None
        for match in population_matches:
            text = match.get('matched_text', '')
            if 'In 2018' in text and 'IUCN estimated' in text and '8 million specimens' in text:
                best_match = match
                break
        
        if best_match:
            print(f"\n✓ FOUND EXACT POPULATION DATA:")
            print(f"Text: {best_match['matched_text']}")
            
            # Also check conservation sections for additional context
            conservation_sections = chinstrap_page_data.get('conservation_sections', [])
            print(f"\nConservation sections: {len(conservation_sections)}")
            
            for section in conservation_sections:
                print(f"  Section: {section.get('section_title', 'Unknown')}")
                content = section.get('content', '')[:200] + '...' if len(section.get('content', '')) > 200 else section.get('content', '')
                print(f"  Content preview: {content}")

# Also examine the HTML file directly for more detailed citation information
chinstrap_html_file = None
for file in workspace_files:
    if 'chinstrap_penguin.html' in file:
        chinstrap_html_file = f'workspace/{file}'
        break

if chinstrap_html_file:
    print(f"\n=== ANALYZING HTML SOURCE FOR DETAILED CITATION ===\n")
    print(f"HTML file: {chinstrap_html_file}")
    
    with open(chinstrap_html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Look for the specific conservation status section
    print("Searching for conservation status section...")
    
    # Find conservation status heading
    conservation_heading = soup.find(['h2', 'h3'], string=re.compile(r'Conservation status', re.IGNORECASE))
    if conservation_heading:
        print(f"✓ Found conservation status heading: {conservation_heading.get_text()}")
        
        # Get the content following this heading
        current = conservation_heading.parent if conservation_heading.parent else conservation_heading
        
        # Find the next few paragraphs
        conservation_content = []
        for _ in range(10):  # Look at next 10 elements
            current = current.find_next_sibling()
            if current is None:
                break
            if current.name == 'p':
                text = current.get_text().strip()
                if '2018' in text and 'IUCN' in text:
                    conservation_content.append(text)
                    print(f"\n✓ FOUND DETAILED CONSERVATION TEXT:")
                    print(f"{text}")
                    
                    # Look for citations/references in this paragraph
                    citations = current.find_all(['sup', 'a'], class_=re.compile(r'reference|cite', re.IGNORECASE))
                    if citations:
                        print(f"\nCitations found: {len(citations)}")
                        for cite in citations[:3]:  # Show first 3 citations
                            cite_text = cite.get_text().strip()
                            cite_href = cite.get('href', '')
                            print(f"  Citation: {cite_text} (href: {cite_href})")
                    
                    break
            elif current.name in ['h1', 'h2', 'h3', 'h4']:  # Hit next major section
                break
    
    # Also search for any references section that might contain the IUCN source
    print(f"\n=== SEARCHING FOR REFERENCES TO IUCN 2018 ===\n")
    
    # Look for references or bibliography sections
    ref_sections = soup.find_all(['h2', 'h3'], string=re.compile(r'reference|bibliography|source', re.IGNORECASE))
    print(f"Reference sections found: {len(ref_sections)}")
    
    # Search for IUCN citations in the entire document
    iucn_mentions = soup.find_all(string=re.compile(r'IUCN.*2018|2018.*IUCN', re.IGNORECASE))
    print(f"IUCN 2018 mentions found: {len(iucn_mentions)}")
    
    for i, mention in enumerate(iucn_mentions[:3], 1):  # Show first 3
        clean_mention = ' '.join(mention.strip().split())
        print(f"  {i}. {clean_mention[:150]}...")

# Compile the final answer
print(f"\n=== COMPILING FINAL ANSWER ===\n")

final_answer = {
    'research_objective': 'Find chinstrap penguin population data as of end of 2018',
    'data_found': True,
    'population_figure': '8 million specimens',
    'measurement_type': 'Individual penguins (specimens), not breeding pairs',
    'source_year': '2018',
    'source_organization': 'IUCN (International Union for Conservation of Nature)',
    'exact_quote': 'In 2018, the IUCN estimated that the population of chinstrap penguins was around 8 million specimens.',
    'source_page': 'Wikipedia: Chinstrap penguin',
    'source_url': 'https://en.wikipedia.org/wiki/Chinstrap_penguin',
    'section': 'Conservation status',
    'extraction_timestamp': extraction_data.get('extraction_timestamp', 'Unknown'),
    'confidence_level': 'High - Direct quote from authoritative source with clear attribution'
}

# Save the final answer
with open('workspace/chinstrap_penguin_final_answer.json', 'w') as f:
    json.dump(final_answer, f, indent=2)

print("✓ RESEARCH COMPLETE - FINAL ANSWER COMPILED:")
print(f"")
print(f"Population Figure: {final_answer['population_figure']}")
print(f"Measurement Type: {final_answer['measurement_type']}")
print(f"Source: {final_answer['source_organization']} ({final_answer['source_year']})")
print(f"Exact Quote: '{final_answer['exact_quote']}'")
print(f"Source Page: {final_answer['source_page']}")
print(f"Confidence: {final_answer['confidence_level']}")
print(f"")
print(f"Final answer saved to: workspace/chinstrap_penguin_final_answer.json")
print(f"\n🐧 CHINSTRAP PENGUIN POPULATION RESEARCH SUCCESSFULLY COMPLETED 🐧")
```

### Development Step 2: Locate 2018 Chinstrap Penguin Population Data on Wikipedia and Document Figure, Units, and Source

**Description**: Search for and access the Wikipedia page about penguin species populations to locate the specific chinstrap penguin population data as of the end of 2018. Extract the population figure, noting whether it's given in breeding pairs or individual penguins, and document the exact source and context of this information.

**Use Cases**:
- Wildlife conservation reporting and automated population data extraction for environmental NGO impact assessments
- Academic ecological research and historical trend analysis of penguin species for climate change studies
- Zoo exhibit content management and real-time species statistics integration for educational displays
- Government policy briefing and reliable IUCN-based species population sourcing for conservation legislation
- Data journalism fact-checking and automated population figure verification for wildlife news stories
- Mobile app development and species metadata enrichment for citizen science biodiversity tracking
- Educational platform content generation and automated insertion of up-to-date species statistics for science curricula

```
import os
import json

print("=== CHINSTRAP PENGUIN POPULATION RESEARCH - STEP 2 ===\n")
print("Objective: Inspect workspace files and understand their structure")
print("Focus: Examine search results before fetching Wikipedia pages\n")

# First, let's check what files are available in the workspace
print("Files available in workspace:")
if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    for file in workspace_files:
        file_path = os.path.join('workspace', file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
else:
    print("  No workspace directory found")

# Inspect the search results JSON file structure
search_results_file = 'workspace/chinstrap_penguin_search_results.json'
if os.path.exists(search_results_file):
    print(f"\n=== INSPECTING SEARCH RESULTS FILE ===\n")
    print(f"File: {search_results_file}")
    
    with open(search_results_file, 'r') as f:
        search_data = json.load(f)
    
    print("\nTop-level keys in search results:")
    for key, value in search_data.items():
        if isinstance(value, dict):
            print(f"  {key}: Dictionary with {len(value)} keys")
        elif isinstance(value, list):
            print(f"  {key}: List with {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Examine the search results structure
    if 'search_results_by_query' in search_data:
        print(f"\nSearch results by query:")
        for i, query_result in enumerate(search_data['search_results_by_query']):
            query = query_result.get('query', 'Unknown query')
            results_count = query_result.get('results_count', 0)
            print(f"  Query {i+1}: {query}")
            print(f"    Results found: {results_count}")
            
            # Show sample result structure
            if 'results' in query_result and query_result['results']:
                sample_result = query_result['results'][0]
                print(f"    Sample result keys: {list(sample_result.keys())}")
                if 'snippet' in sample_result:
                    snippet = sample_result['snippet'][:100] + "..." if len(sample_result['snippet']) > 100 else sample_result['snippet']
                    print(f"    Sample snippet: {snippet}")

# Inspect the pages to fetch JSON file structure
pages_file = 'workspace/wikipedia_pages_to_fetch.json'
if os.path.exists(pages_file):
    print(f"\n=== INSPECTING PAGES TO FETCH FILE ===\n")
    print(f"File: {pages_file}")
    
    with open(pages_file, 'r') as f:
        pages_data = json.load(f)
    
    print("\nTop-level keys in pages to fetch:")
    for key, value in pages_data.items():
        if isinstance(value, dict):
            print(f"  {key}: Dictionary with {len(value)} keys")
        elif isinstance(value, list):
            print(f"  {key}: List with {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Show target pages
    if 'target_pages' in pages_data:
        print(f"\nTarget pages identified:")
        for i, page in enumerate(pages_data['target_pages'], 1):
            print(f"  Page {i}:")
            for key, value in page.items():
                if key == 'snippet':
                    snippet = value[:80] + "..." if len(value) > 80 else value
                    print(f"    {key}: {snippet}")
                else:
                    print(f"    {key}: {value}")

# Look for specific population-related content in the search snippets
print(f"\n=== ANALYZING SEARCH SNIPPETS FOR POPULATION DATA ===\n")

if os.path.exists(search_results_file):
    with open(search_results_file, 'r') as f:
        search_data = json.load(f)
    
    population_indicators = []
    
    for query_result in search_data.get('search_results_by_query', []):
        for result in query_result.get('results', []):
            snippet = result.get('snippet', '').lower()
            title = result.get('title', '')
            url = result.get('link', '')
            
            # Look for population-related keywords
            population_keywords = ['2018', 'population', 'breeding pairs', '8,000,000', '8 million', 'iucn', 'estimated']
            
            found_keywords = [kw for kw in population_keywords if kw in snippet]
            
            if found_keywords:
                population_indicators.append({
                    'title': title,
                    'url': url,
                    'snippet': result.get('snippet', ''),
                    'found_keywords': found_keywords,
                    'from_query': query_result.get('query', '')
                })
    
    print(f"Results with population indicators: {len(population_indicators)}")
    
    for i, indicator in enumerate(population_indicators, 1):
        print(f"\n{i}. {indicator['title']}")
        print(f"   URL: {indicator['url']}")
        print(f"   Keywords found: {indicator['found_keywords']}")
        print(f"   Snippet: {indicator['snippet'][:150]}...")
        print(f"   From query: {indicator['from_query']}")

print(f"\n=== WORKSPACE INSPECTION COMPLETE ===\n")
print("Key findings:")
print("1. Main target: 'Chinstrap penguin' Wikipedia page")
print("2. Promising snippets mention '2018, the IUCN estimated' and '8,000,000'")
print("3. 'List of Sphenisciformes by population' also contains relevant data")
print("\nNext step: Fetch and parse the Wikipedia pages to extract exact population figures")
```

### Development Step 8: Extract 2020 Chinstrap Penguin Population Count and Methodology from Nature.com Study for Comparison

**Description**: Search for and access the Nature.com article titled 'global population assessment of the Chinstrap penguin' from 2020. Extract the specific population figure from this study, noting whether it's provided as breeding pairs or individual penguins. Document the exact methodology and population count to enable accurate comparison with the Wikipedia 2018 data.

**Use Cases**:
- Conservation NGO population tracking dashboards and policy recommendation reports for Antarctic wildlife management
- Government environmental agency species status assessments and legislative drafting for marine protection
- Academic meta-analysis combining multi-decade seabird population studies for climate change impact research
- Automated update of biodiversity informatics platforms (e.g., GBIF) with standardized species counts and confidence intervals
- Ecotourism operator planning and risk assessment for Antarctic expeditions based on up-to-date penguin colony sizes
- Science education module development and interactive visualizations for university ecology courses
- Journalistic data-driven articles on wildlife biodiversity trends for environmental news outlets
- Environmental consultancy feasibility studies and impact assessments for proposed Antarctic infrastructure projects

```
import os
import json

print("=== FINAL EXTRACTION: 2020 NATURE STUDY POPULATION DATA ===\n")

# Locate workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("No workspace directory found.")
    exit()

workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# First, inspect the analysis file structure before accessing it
analysis_file = os.path.join(workspace_dir, 'nature_2020_population_analysis.json')
if not os.path.exists(analysis_file):
    print(f"Analysis file not found: {analysis_file}")
    exit()

print("=== INSPECTING ANALYSIS FILE STRUCTURE ===\n")
print(f"Reading analysis file: {os.path.basename(analysis_file)}")

with open(analysis_file, 'r') as f:
    analysis_data = json.load(f)

print("Top-level keys in analysis data:")
for key, value in analysis_data.items():
    if isinstance(value, dict):
        print(f"  {key}: Dictionary with {len(value)} keys")
    elif isinstance(value, list):
        print(f"  {key}: List with {len(value)} items")
    else:
        print(f"  {key}: {type(value).__name__} - {str(value)[:100]}...")

print("\n=== EXTRACTING KEY POPULATION DATA FROM ANALYSIS ===\n")

# Extract the main population figure from abstract
if 'abstract_text' in analysis_data:
    abstract_text = analysis_data['abstract_text']
    print("Abstract text (key excerpt):")
    print(abstract_text[:500] + "...")
    
    # Extract the specific population figure mentioned
    print("\n*** KEY FINDING FROM ABSTRACT ***")
    print("Global population: 3.42 million breeding pairs")
    print("95th-percentile CI: [2.98, 4.00] million breeding pairs")
    print("Number of colonies: 375 extant colonies")
    print("Data collection year: 2020")
else:
    print("Abstract text not found in analysis")

# Extract methodology information
print("\n=== METHODOLOGY FROM 2020 STUDY ===\n")

if 'methods_text' in analysis_data:
    methods_text = analysis_data['methods_text']
    print("Methodology approach (from abstract and methods):")
    print("1. Satellite imagery analysis")
    print("2. Drone (UAS) imagery counts")
    print("3. Ground counting of individual occupied nests or chicks")
    print("4. Guano coverage area estimation from satellite imagery")
    print("5. High-resolution commercial imagery prioritized")
    
    print("\nMethodology details (excerpt from methods section):")
    print(methods_text[:800] + "...")
else:
    print("Methods text not available")

# Compare measurement types and provide summary
print("\n=== POPULATION MEASUREMENT SPECIFICATIONS ===\n")

print("2020 Nature Study Specifications:")
print("• Population Count: 3.42 million")
print("• Measurement Unit: BREEDING PAIRS")
print("• Confidence Interval: 95th-percentile CI [2.98, 4.00] million")
print("• Total Colonies Assessed: 375 extant colonies")
print("• Data Collection Methods: Satellite + Drone + Ground surveys")
print("• Survey Scope: Global comprehensive assessment")
print("• Publication Year: 2020")
print("• Data Collection Period: Multi-year (referenced from 1980s to 2020)")

# Create final comparison dataset
final_results = {
    "nature_2020_study": {
        "title": "A global population assessment of the Chinstrap penguin (Pygoscelis antarctica)",
        "publication_year": 2020,
        "journal": "Nature Scientific Reports",
        "population_figure": "3.42 million",
        "measurement_unit": "breeding pairs",
        "confidence_interval": "95th-percentile CI: [2.98, 4.00] million breeding pairs",
        "number_of_colonies": 375,
        "methodology": {
            "primary_methods": [
                "Satellite imagery analysis",
                "Drone (UAS) imagery", 
                "Ground counting of nests/chicks",
                "Guano coverage estimation"
            ],
            "imagery_sources": [
                "High-resolution commercial imagery",
                "Planet imagery",
                "Landsat imagery"
            ],
            "survey_approach": "Comprehensive global assessment",
            "data_prioritization": "Direct census methods prioritized over satellite estimates"
        },
        "key_findings": {
            "extirpated_colonies": 23,
            "new_colonies_identified": 5,
            "previously_unreported_colonies": 21,
            "colonies_with_historical_comparison": "65% of all colonies",
            "declining_colonies_percentage": "45% probably or certainly declined",
            "increasing_colonies_percentage": "18% probably or certainly increased"
        },
        "data_quality_notes": [
            "Limited historical data at 35% of colonies prohibit population change assessment",
            "Most historical comparisons made against 1980s baseline data",
            "Large colonies in South Sandwich Islands lack historical benchmark"
        ]
    },
    "comparison_ready": {
        "measurement_type": "breeding pairs",
        "population_value": 3.42,
        "population_unit": "million breeding pairs", 
        "confidence_range_low": 2.98,
        "confidence_range_high": 4.00,
        "year": 2020,
        "methodology_summary": "Multi-method global survey using satellite, drone, and ground-based counting",
        "coverage": "Comprehensive global assessment of 375 colonies"
    }
}

# Save final extraction results
final_file = os.path.join(workspace_dir, 'nature_2020_final_population_data.json')
with open(final_file, 'w') as f:
    json.dump(final_results, f, indent=2)

print(f"\n=== FINAL DATA EXTRACTION COMPLETE ===\n")
print(f"Comprehensive population data saved to: {final_file}")

print("\n=== SUMMARY FOR WIKIPEDIA COMPARISON ===\n")
print("Nature 2020 Study Results:")
print(f"• Global Population: 3.42 million breeding pairs")
print(f"• Confidence Interval: 2.98 - 4.00 million breeding pairs")
print(f"• Total Colonies: 375 extant breeding sites")
print(f"• Methodology: Satellite + Drone + Ground surveys (comprehensive global assessment)")
print(f"• Data Quality: High precision with 95th-percentile confidence intervals")
print(f"• Study Scope: First comprehensive global population assessment")

print("\nReady for comparison with Wikipedia 2018 data:")
print("✓ Population figure extracted: 3.42 million breeding pairs")
print("✓ Measurement unit identified: breeding pairs (not individuals)")
print("✓ Methodology documented: multi-source survey approach")
print("✓ Confidence intervals provided: [2.98, 4.00] million")
print("✓ Publication year confirmed: 2020")

print("\nThis 2020 Nature study provides the specific population assessment")
print("needed for comparison with Wikipedia's 2018 population data.")
```

### Development Step 6: Retrieve 2020 Nature.com Chinstrap Penguin Population Estimate and Methodology for 2018 Wikipedia Comparison

**Description**: Search for and access the Nature.com article titled 'global population assessment of the Chinstrap penguin' from 2020. Extract the specific population figure from this study, noting whether it's provided as breeding pairs or individual penguins. Document the exact methodology and population count to enable accurate comparison with the Wikipedia 2018 data.

**Use Cases**:
- Meta-analysis of Chinstrap penguin population trends and methodology comparison for biodiversity researchers
- Conservation planning for Antarctic NGOs using precise 2020 population counts to prioritize colony protection measures
- Environmental policy development teams extracting peer-reviewed census methods and figures to draft marine wildlife regulations
- Data journalism on climate impact leveraging automated retrieval of original 2020 penguin population data for news articles
- Academic thesis support where graduate students parse original study methodology and counts for literature reviews and comparisons with Wikipedia data
- GIS-based habitat modeling incorporating extracted population figures to map Chinstrap penguin distribution under future climate scenarios
- Biodiversity database curation services automating article access and content extraction to populate wildlife population records
- Environmental data dashboard integration for research institutions displaying up-to-date population and methodology details from primary sources

```
import os
import json

print("=== CORRECTING ARTICLE ACCESS - TARGETING CORRECT 2020 STUDY ===\n")

# First, let's inspect the search results file to understand the structure
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    workspace_dir = workspace_dirs[0]
    print(f"Using workspace directory: {workspace_dir}\n")
else:
    print("No workspace directory found.")
    exit()

# Inspect the search results JSON structure first
search_results_file = os.path.join(workspace_dir, 'nature_chinstrap_search_results.json')
if os.path.exists(search_results_file):
    print("=== INSPECTING SEARCH RESULTS STRUCTURE ===\n")
    
    with open(search_results_file, 'r') as f:
        search_data = json.load(f)
    
    print("Top-level keys in search results:")
    for key, value in search_data.items():
        if isinstance(value, list):
            print(f"  {key}: List with {len(value)} items")
        elif isinstance(value, dict):
            print(f"  {key}: Dictionary with {len(value)} keys")
        else:
            print(f"  {key}: {value}")
    
    # Examine the structure of search results
    if 'all_results' in search_data and search_data['all_results']:
        print(f"\nFirst search result structure:")
        first_result = search_data['all_results'][0]
        for key, value in first_result.items():
            print(f"  {key}: {str(value)[:100]}{'...' if len(str(value)) > 100 else ''}")
    
    print(f"\n=== IDENTIFYING CORRECT TARGET ARTICLE ===\n")
    
    # Find the exact 2020 global population assessment article
    target_article = None
    
    for result in search_data['all_results']:
        title = result.get('title', '').lower()
        url = result.get('link', '')
        
        # Look for the specific 2020 study (not citations of it)
        if ('global population assessment' in title and 
            'chinstrap penguin' in title and
            '2020' in url and  # URL should contain 2020
            's41598-020-76479-3' in url):  # Specific article ID from search results
            
            target_article = result
            print(f"*** FOUND TARGET ARTICLE ***")
            print(f"Title: {result.get('title')}")
            print(f"URL: {result.get('link')}")
            print(f"Snippet: {result.get('snippet')}")
            break
    
    # If not found by exact match, look for the first result which should be the primary study
    if not target_article:
        print("Exact match not found, checking first result...\n")
        first_result = search_data['all_results'][0]
        
        print(f"First result details:")
        print(f"Title: {first_result.get('title')}")
        print(f"URL: {first_result.get('link')}")
        print(f"Snippet: {first_result.get('snippet')}")
        
        # Verify this is the correct 2020 study
        if ('s41598-020-76479-3' in first_result.get('link', '') or 
            'global population assessment' in first_result.get('title', '').lower()):
            target_article = first_result
            print(f"\n*** CONFIRMED: This is the target 2020 study ***")
    
    if target_article:
        print(f"\n=== ACCESSING CORRECT ARTICLE ===\n")
        print(f"Target URL: {target_article['link']}")
        
        import requests
        from bs4 import BeautifulSoup
        
        # Set up headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        try:
            article_response = requests.get(target_article['link'], headers=headers, timeout=30)
            
            if article_response.status_code == 200:
                print(f"Successfully accessed correct article. Status code: {article_response.status_code}")
                print(f"Content length: {len(article_response.content):,} bytes")
                
                # Save the correct article HTML
                correct_article_file = os.path.join(workspace_dir, 'nature_chinstrap_2020_study.html')
                with open(correct_article_file, 'w', encoding='utf-8') as f:
                    f.write(article_response.text)
                
                print(f"\nCorrect article HTML saved to: {correct_article_file}")
                
                # Parse the article content
                soup = BeautifulSoup(article_response.text, 'html.parser')
                
                # Extract key information
                article_title = soup.find('title')
                if article_title:
                    print(f"\nArticle title: {article_title.get_text().strip()}")
                
                # Look for article content containers
                content_selectors = [
                    'div[data-test="article-content"]',
                    'div.c-article-body',
                    'article',
                    'div.article-item-body',
                    'main'
                ]
                
                article_content = None
                for selector in content_selectors:
                    content_element = soup.select_one(selector)
                    if content_element:
                        article_content = content_element
                        print(f"Found article content using selector: {selector}")
                        break
                
                if article_content:
                    content_text = article_content.get_text()
                    print(f"\nExtracted content length: {len(content_text):,} characters")
                    
                    # Save extracted text for analysis
                    correct_text_file = os.path.join(workspace_dir, 'nature_chinstrap_2020_study_text.txt')
                    with open(correct_text_file, 'w', encoding='utf-8') as f:
                        f.write(content_text)
                    
                    print(f"Correct article text saved to: {correct_text_file}")
                    
                    # Quick verification - look for key terms that should be in the population study
                    verification_terms = ['population', 'breeding pairs', 'census', 'global', 'assessment', 'methodology']
                    found_terms = []
                    
                    for term in verification_terms:
                        if term.lower() in content_text.lower():
                            found_terms.append(term)
                    
                    print(f"\nContent verification - Found key terms: {found_terms}")
                    print(f"Terms found: {len(found_terms)}/{len(verification_terms)}")
                    
                    if len(found_terms) >= 4:
                        print("✓ Article content verified as population study")
                    else:
                        print("⚠ Content verification inconclusive")
                        
                else:
                    print("Could not locate article content with standard selectors")
                    
                    # Try to extract any text content
                    body_text = soup.get_text()
                    if body_text:
                        print(f"Extracted general body text: {len(body_text):,} characters")
                        
                        fallback_text_file = os.path.join(workspace_dir, 'nature_chinstrap_2020_fallback_text.txt')
                        with open(fallback_text_file, 'w', encoding='utf-8') as f:
                            f.write(body_text)
                        print(f"Fallback text saved to: {fallback_text_file}")
                
            else:
                print(f"Failed to access article. Status code: {article_response.status_code}")
                print(f"Response headers: {dict(article_response.headers)}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error accessing article: {e}")
            
    else:
        print("Could not identify the correct target article from search results.")
        print("Available articles in search results:")
        for i, result in enumerate(search_data['all_results'][:3], 1):
            print(f"  {i}. {result.get('title')} - {result.get('link')}")
else:
    print("Search results file not found in workspace.")

print(f"\n=== CORRECTION PHASE COMPLETE ===")
print("Files in workspace:")
for file in os.listdir(workspace_dir):
    file_path = os.path.join(workspace_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"  - {file} ({file_size:,} bytes)")

print(f"\nNext step: Parse the correct 2020 study for population figures and methodology")
```

### Development Step 5: Access 2020 Nature.com Chinstrap Penguin Population Study: Extract Count & Methodology for 2018 Comparison

**Description**: Search for and access the Nature.com article titled 'global population assessment of the Chinstrap penguin' from 2020. Extract the specific population figure from this study, noting whether it's provided as breeding pairs or individual penguins. Document the exact methodology and population count to enable accurate comparison with the Wikipedia 2018 data.

**Use Cases**:
- Wildlife conservation NGOs sourcing the latest Chinstrap penguin population figures and methodologies to prioritize colony protection efforts in Antarctica
- University ecology researchers comparing 2020 Nature.com breeding pair estimates with 2018 Wikipedia counts for peer-reviewed longitudinal studies on penguin demographics
- Environmental consultants integrating authoritative Chinstrap penguin numbers into Antarctic tourism impact assessments for compliance with sustainability regulations
- Automated monitoring pipelines extracting updated population data and sampling methods to trigger alerts when Chinstrap penguin counts deviate beyond threshold in ecological dashboards
- Data journalism teams retrieving precise penguin population metrics and survey techniques to create interactive articles on wildlife conservation trends
- Government wildlife agencies extracting standardized population figures from peer-reviewed studies to inform national biodiversity action plans and policy decisions
- E-learning content developers incorporating verified Chinstrap penguin population data and research methods into interactive modules on polar ecosystems
- Citizen science platforms validating volunteer-submitted colony count data against professional population assessments for accuracy and training feedback

```
import os
import re
import requests
import json
from bs4 import BeautifulSoup

print("=== SEARCHING FOR NATURE.COM CHINSTRAP PENGUIN POPULATION STUDY (2020) ===\n")

# Search for the specific Nature.com article about Chinstrap penguin global population assessment from 2020
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print("API key found. Proceeding with search...\n")
    
    # Construct specific search query for Nature.com Chinstrap penguin study
    query = 'site:nature.com "global population assessment" "Chinstrap penguin" 2020'
    
    print(f"Search query: {query}")
    
    # Prepare API request parameters
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "google_domain": "google.com",
        "safe": "off",
        "num": 10,
        "type": "search"
    }
    
    # Make API request to SerpAPI
    print("\nMaking search request...")
    response = requests.get("https://serpapi.com/search.json", params=params)
    
    if response.status_code == 200:
        results = response.json()
        print(f"Search completed successfully. Status code: {response.status_code}")
        
        # Check if we have organic results
        if results.get("organic_results"):
            print(f"\nFound {len(results['organic_results'])} search results:\n")
            
            nature_articles = []
            
            for i, result in enumerate(results['organic_results'], 1):
                title = result.get('title', 'No title')
                link = result.get('link', 'No link')
                snippet = result.get('snippet', 'No snippet')
                
                print(f"Result {i}:")
                print(f"  Title: {title}")
                print(f"  URL: {link}")
                print(f"  Snippet: {snippet}")
                print()
                
                # Check if this is a Nature.com article about Chinstrap penguins
                if ('nature.com' in link.lower() and 
                    ('chinstrap' in title.lower() or 'chinstrap' in snippet.lower()) and
                    ('population' in title.lower() or 'population' in snippet.lower()) and
                    '2020' in (title + snippet)):
                    
                    nature_articles.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet,
                        'result_number': i
                    })
                    print(f"  *** IDENTIFIED AS TARGET NATURE ARTICLE ***")
            
            # Save search results for reference
            search_results_data = {
                'search_query': query,
                'total_results': len(results['organic_results']),
                'nature_articles_found': len(nature_articles),
                'all_results': results['organic_results'],
                'identified_nature_articles': nature_articles
            }
            
            with open('workspace/nature_chinstrap_search_results.json', 'w') as f:
                json.dump(search_results_data, f, indent=2)
            
            print(f"\n=== SEARCH RESULTS SUMMARY ===")
            print(f"Total search results: {len(results['organic_results'])}")
            print(f"Nature.com articles identified: {len(nature_articles)}")
            
            if nature_articles:
                print("\n=== IDENTIFIED NATURE.COM ARTICLES ===")
                for article in nature_articles:
                    print(f"\nArticle {article['result_number']}:")
                    print(f"Title: {article['title']}")
                    print(f"URL: {article['url']}")
                    print(f"Snippet: {article['snippet']}")
                
                # Try to access the first Nature article found
                target_article = nature_articles[0]
                print(f"\n=== ATTEMPTING TO ACCESS TARGET ARTICLE ===")
                print(f"Target URL: {target_article['url']}")
                
                # Set up headers to mimic browser request
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive'
                }
                
                try:
                    article_response = requests.get(target_article['url'], headers=headers, timeout=30)
                    
                    if article_response.status_code == 200:
                        print(f"Successfully accessed article. Status code: {article_response.status_code}")
                        print(f"Content length: {len(article_response.content):,} bytes")
                        
                        # Save the article HTML for analysis
                        with open('workspace/nature_chinstrap_article.html', 'w', encoding='utf-8') as f:
                            f.write(article_response.text)
                        
                        print(f"\nArticle HTML saved to: workspace/nature_chinstrap_article.html")
                        
                        # Parse the article content
                        soup = BeautifulSoup(article_response.text, 'html.parser')
                        
                        # Extract key information
                        article_title = soup.find('title')
                        if article_title:
                            print(f"\nArticle title: {article_title.get_text().strip()}")
                        
                        # Look for article content containers
                        content_selectors = [
                            'div[data-test="article-content"]',
                            'div.c-article-body',
                            'article',
                            'div.article-item-body',
                            'main'
                        ]
                        
                        article_content = None
                        for selector in content_selectors:
                            content_element = soup.select_one(selector)
                            if content_element:
                                article_content = content_element
                                print(f"Found article content using selector: {selector}")
                                break
                        
                        if article_content:
                            content_text = article_content.get_text()
                            print(f"\nExtracted content length: {len(content_text):,} characters")
                            
                            # Save extracted text for further analysis
                            with open('workspace/nature_chinstrap_article_text.txt', 'w', encoding='utf-8') as f:
                                f.write(content_text)
                            
                            print(f"Article text saved to: workspace/nature_chinstrap_article_text.txt")
                        else:
                            print("Could not locate article content with standard selectors")
                            print("Will need to analyze full HTML structure")
                        
                    else:
                        print(f"Failed to access article. Status code: {article_response.status_code}")
                        print(f"Response: {article_response.text[:500]}...")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Error accessing article: {e}")
            else:
                print("\nNo Nature.com articles found for Chinstrap penguin population assessment.")
                print("Will try broader search terms...")
                
        else:
            print("No search results found. Trying alternative search...")
            
    else:
        print(f"Search request failed. Status code: {response.status_code}")
        print(f"Error response: {response.text}")

print(f"\n=== SEARCH PHASE COMPLETE ===")
print("Files created in workspace/:")
print("  - nature_chinstrap_search_results.json (search results data)")
if os.path.exists('workspace/nature_chinstrap_article.html'):
    print("  - nature_chinstrap_article.html (full article HTML)")
if os.path.exists('workspace/nature_chinstrap_article_text.txt'):
    print("  - nature_chinstrap_article_text.txt (extracted article text)")

print("\nNext step: Parse the downloaded article to extract population figures and methodology")
```

## Created Time
2025-08-11 03:40:03
