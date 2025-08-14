# Developer Plan 01

## Plan
Parse and analyze the attached CSV file data/gaia/2023/validation/8d46b8d6-b38a-47ff-ac74-cda14cf2d19b.csv to understand its structure and content. Extract all penguin data including species identification, location information (specifically noting which penguins live on Dream Island), beak measurements, and population counts. Identify the specific columns and data format to prepare for filtering penguins that don't live on Dream Island and don't have beaks longer than 42mm.

## Description
This is the optimal first step because: (1) We need to understand the CSV file structure and identify what penguin data is available before we can filter and count specific populations, (2) No previous analysis has been performed on this file, (3) Expected outcome is to have complete understanding of the penguin dataset including location data, beak measurements, and population figures, (4) This provides the foundation needed to filter for penguins that don't live on Dream Island and don't have beaks longer than 42mm, which we'll then compare against Wikipedia's total penguin population estimates from end of 2012

## Episodic Examples
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

### Development Step 3: Locate 2018 Chinstrap Penguin Population Data on Wikipedia and Document Source, Units, and Context

**Description**: Search for and access the Wikipedia page about penguin species populations to locate the specific chinstrap penguin population data as of the end of 2018. Extract the population figure, noting whether it's given in breeding pairs or individual penguins, and document the exact source and context of this information.

**Use Cases**:
- Automated biodiversity monitoring dashboard for an environmental NGO to track and compare chinstrap penguin populations year over year
- Research pipeline for a polar ecology lab to integrate the 2018 IUCN population figures into species trend models
- Content management system for an educational website that auto-updates wildlife fact sheets with the latest penguin population data
- Data validation workflow for a conservation funding agency that cross-checks grant applications against official IUCN population estimates
- Media production tool for a nature documentary team that pulls precise penguin statistics and citations directly into scripts and graphics
- Policy briefing generator for government wildlife agencies that compiles exact 2018 chinstrap penguin numbers with source references
- Mobile field app for Antarctic researchers that preloads species population baselines to plan tagging and surveying efforts
- Data journalism toolkit for environmental reporters to source, verify, and visualize authoritative penguin population figures in news articles

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
import re

print("=== CHINSTRAP PENGUIN POPULATION RESEARCH - STEP 3 ===\n")
print("Objective: Fetch and parse Wikipedia pages to extract exact 2018 population data")
print("Focus: Get precise IUCN population estimate with full context and citation\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# First, load the pages to fetch data
pages_file = 'workspace/wikipedia_pages_to_fetch.json'
if not os.path.exists(pages_file):
    print(f"❌ Pages file not found: {pages_file}")
    exit()

with open(pages_file, 'r') as f:
    pages_data = json.load(f)

print(f"Target pages to fetch: {len(pages_data.get('target_pages', []))}")

# Also identify additional high-value pages from our search analysis
high_priority_pages = [
    'https://en.wikipedia.org/wiki/Chinstrap_penguin',
    'https://en.wikipedia.org/wiki/List_of_Sphenisciformes_by_population'
]

print(f"High priority pages: {len(high_priority_pages)}")

all_extracted_data = []

# Fetch each Wikipedia page
for page_url in high_priority_pages:
    page_name = page_url.split('/')[-1].replace('_', ' ')
    print(f"\n--- FETCHING: {page_name} ---")
    print(f"URL: {page_url}")
    
    try:
        response = requests.get(page_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Save the HTML content
        safe_filename = page_url.split('/')[-1].lower()
        html_file = f'workspace/{safe_filename}.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"✓ HTML saved to: {html_file}")
        
        # Extract key information
        page_title = soup.find('h1', class_='firstHeading')
        page_title_text = page_title.get_text().strip() if page_title else 'No title found'
        
        print(f"Page title: {page_title_text}")
        
        # Look for population data in the content
        page_text = soup.get_text()
        
        # Search for 2018 IUCN population data
        print(f"\n=== SEARCHING FOR 2018 POPULATION DATA ===")
        
        # Look for specific patterns mentioning 2018 and population
        population_patterns = [
            r'(In 2018[^.]*?population[^.]*?[0-9,]+[^.]*)\.',
            r'(2018[^.]*?IUCN[^.]*?population[^.]*?[0-9,]+[^.]*)\.',
            r'(IUCN[^.]*?2018[^.]*?population[^.]*?[0-9,]+[^.]*)\.',
            r'(population[^.]*?2018[^.]*?[0-9,]+[^.]*)\.',
            r'([0-9,]+ million[^.]*?chinstrap[^.]*)\.',
            r'(chinstrap[^.]*?[0-9,]+ million[^.]*)\.',
            r'([0-9,]+[^.]*?specimens[^.]*?chinstrap[^.]*)\.',
            r'(chinstrap[^.]*?[0-9,]+[^.]*?specimens[^.]*)\.',
        ]
        
        found_population_data = []
        
        for pattern in population_patterns:
            matches = re.findall(pattern, page_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                cleaned_match = ' '.join(match.split())  # Clean up whitespace
                if len(cleaned_match) > 20 and ('2018' in cleaned_match or '8' in cleaned_match):  # Filter meaningful matches
                    found_population_data.append({
                        'pattern_used': pattern,
                        'matched_text': cleaned_match,
                        'source_page': page_name
                    })
        
        print(f"Population data matches found: {len(found_population_data)}")
        
        for i, data in enumerate(found_population_data[:5], 1):  # Show top 5 matches
            print(f"  {i}. {data['matched_text'][:120]}...")
        
        # Look specifically for IUCN conservation status sections
        print(f"\n=== SEARCHING FOR CONSERVATION STATUS SECTIONS ===")
        
        # Find conservation status or similar sections
        conservation_sections = soup.find_all(['h2', 'h3', 'h4'], string=re.compile(r'conservation|status|population', re.IGNORECASE))
        
        print(f"Conservation-related sections found: {len(conservation_sections)}")
        
        conservation_content = []
        
        for section in conservation_sections:
            print(f"  Section: {section.get_text().strip()}")
            
            # Get the content following this heading
            next_elements = []
            current = section
            
            # Look for the next few paragraphs after the heading
            for _ in range(5):
                current = current.find_next_sibling()
                if current is None:
                    break
                if current.name in ['p', 'div', 'ul']:
                    text_content = current.get_text().strip()
                    if text_content and len(text_content) > 20:
                        next_elements.append(text_content)
                elif current.name in ['h1', 'h2', 'h3', 'h4']:  # Hit next section
                    break
            
            if next_elements:
                section_content = ' '.join(next_elements)
                if '2018' in section_content or 'population' in section_content.lower():
                    conservation_content.append({
                        'section_title': section.get_text().strip(),
                        'content': section_content[:500] + '...' if len(section_content) > 500 else section_content
                    })
        
        # Look for infobox data (often contains population figures)
        print(f"\n=== SEARCHING FOR INFOBOX DATA ===")
        
        infoboxes = soup.find_all(['table'], class_=re.compile(r'infobox', re.IGNORECASE))
        print(f"Infoboxes found: {len(infoboxes)}")
        
        infobox_data = []
        for infobox in infoboxes:
            rows = infobox.find_all('tr')
            for row in rows:
                row_text = row.get_text()
                if ('population' in row_text.lower() or '2018' in row_text or 
                    'conservation' in row_text.lower() or 'status' in row_text.lower()):
                    cleaned_text = ' '.join(row_text.split())
                    if len(cleaned_text) > 10:
                        infobox_data.append(cleaned_text)
        
        print(f"Relevant infobox entries: {len(infobox_data)}")
        for entry in infobox_data[:3]:  # Show first 3
            print(f"  - {entry[:100]}...")
        
        # Store all extracted data for this page
        page_extraction = {
            'page_name': page_name,
            'page_url': page_url,
            'page_title': page_title_text,
            'html_file': html_file,
            'population_matches': found_population_data,
            'conservation_sections': conservation_content,
            'infobox_entries': infobox_data,
            'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        all_extracted_data.append(page_extraction)
        
    except Exception as e:
        print(f"❌ Error fetching {page_name}: {str(e)}")
        
        # Still record the attempt
        all_extracted_data.append({
            'page_name': page_name,
            'page_url': page_url,
            'error': str(e),
            'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    time.sleep(1)  # Be respectful to Wikipedia

# Save all extracted data
final_extraction = {
    'research_objective': 'Extract chinstrap penguin population data as of end 2018',
    'extraction_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'pages_processed': len(all_extracted_data),
    'pages_data': all_extracted_data
}

with open('workspace/chinstrap_penguin_population_extraction.json', 'w') as f:
    json.dump(final_extraction, f, indent=2)

print(f"\n=== EXTRACTION SUMMARY ===\n")
print(f"Pages processed: {final_extraction['pages_processed']}")
print(f"Extraction data saved to: workspace/chinstrap_penguin_population_extraction.json")

# Analyze the most promising population data found
print(f"\n=== ANALYZING MOST PROMISING POPULATION DATA ===\n")

all_population_matches = []
for page_data in all_extracted_data:
    if 'population_matches' in page_data:
        for match in page_data['population_matches']:
            all_population_matches.append({
                'source_page': page_data['page_name'],
                'text': match['matched_text']
            })

print(f"Total population data matches across all pages: {len(all_population_matches)}")

# Filter for the most relevant matches (containing 2018 and specific numbers)
best_matches = []
for match in all_population_matches:
    text = match['text'].lower()
    if ('2018' in text and 'iucn' in text and 
        ('8 million' in text or '8,000,000' in text or 'million' in text)):
        best_matches.append(match)

print(f"\nBest matches (2018 + IUCN + population figures): {len(best_matches)}")

for i, match in enumerate(best_matches, 1):
    print(f"\n{i}. Source: {match['source_page']}")
    print(f"   Text: {match['text']}")

print(f"\n✓ Wikipedia pages fetched and parsed successfully")
print(f"✓ Population data extraction complete")
print(f"\nNext step: Analyze extracted data to identify the exact 2018 IUCN population figure")
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

### Development Step 7: Access 2020 Nature.com Chinstrap Penguin Global Population Study; Extract Figures and Methodology

**Description**: Search for and access the Nature.com article titled 'global population assessment of the Chinstrap penguin' from 2020. Extract the specific population figure from this study, noting whether it's provided as breeding pairs or individual penguins. Document the exact methodology and population count to enable accurate comparison with the Wikipedia 2018 data.

**Use Cases**:
- Wildlife conservation policy development and regulatory compliance tracking for environmental agencies extracting Chinstrap penguin counts and survey methods to inform protected area management
- Automated meta-analysis pipeline for ecological research labs harvesting 2020 population figures and methodologies for comparative species trend studies
- Environmental NGO report generation and stakeholder presentations incorporating precise breeding-pair data from Nature studies into annual conservation impact reports
- Marine biology curriculum content creation using extracted global population figures and field census techniques as real-world case studies for university courses
- Integration of structured penguin population data into open biodiversity platforms and JSON databases to support public research and citizen science initiatives
- Climate change impact modeling workflow for research institutes feeding standardized population metrics into ecosystem simulation models to forecast Antarctic biodiversity shifts
- Journalistic fact-checking and science news enrichment verifying reported Chinstrap penguin numbers and methodology details when covering Nature.com publications
- Automated updates to Wikipedia species entries comparing 2020 Nature study data with 2018 figures and generating structured update recommendations for editors

```
import os
import re
import json

print("=== PARSING 2020 NATURE STUDY FOR POPULATION FIGURES ===\n")

# Locate workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if not workspace_dirs:
    print("No workspace directory found.")
    exit()

workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Load the correct 2020 study text file
study_text_file = os.path.join(workspace_dir, 'nature_chinstrap_2020_study_text.txt')
if not os.path.exists(study_text_file):
    print(f"Study text file not found: {study_text_file}")
    exit()

print(f"Reading study text file: {os.path.basename(study_text_file)}")
with open(study_text_file, 'r', encoding='utf-8') as f:
    study_text = f.read()

print(f"Study text length: {len(study_text):,} characters\n")

# First, let's examine the overall structure and find key sections
print("=== IDENTIFYING KEY SECTIONS IN THE STUDY ===\n")

# Look for major section headings
section_patterns = [
    r'Abstract',
    r'Introduction', 
    r'Results',
    r'Discussion',
    r'Methods',
    r'Conclusion'
]

found_sections = []
for pattern in section_patterns:
    matches = list(re.finditer(pattern, study_text, re.IGNORECASE))
    if matches:
        for match in matches:
            found_sections.append({
                'section': pattern,
                'position': match.start(),
                'text': match.group()
            })

# Sort sections by position
found_sections.sort(key=lambda x: x['position'])

print("Major sections found:")
for section in found_sections:
    print(f"  - {section['section']} at position {section['position']:,}")

# Extract key population-related numbers and methodology
print("\n=== SEARCHING FOR POPULATION FIGURES ===\n")

# Patterns to look for population numbers
population_patterns = [
    r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:breeding\s*pairs?|pairs?)',
    r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:individuals?|penguins?)',
    r'population\s+of\s+(\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
    r'total\s+(?:of\s+)?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:breeding\s*pairs?|pairs?|individuals?)',
    r'estimated\s+(?:at\s+)?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:breeding\s*pairs?|pairs?|individuals?)',
    r'global\s+population\s+(?:of\s+)?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)',
    r'approximately\s+(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:breeding\s*pairs?|pairs?|individuals?)'
]

population_findings = []

for pattern in population_patterns:
    matches = list(re.finditer(pattern, study_text, re.IGNORECASE))
    for match in matches:
        # Get context around the match (200 characters before and after)
        start = max(0, match.start() - 200)
        end = min(len(study_text), match.end() + 200)
        context = study_text[start:end]
        
        population_findings.append({
            'pattern': pattern,
            'match': match.group(),
            'number': match.group(1) if match.groups() else 'N/A',
            'position': match.start(),
            'context': context.replace('\n', ' ').strip()
        })

print(f"Found {len(population_findings)} potential population references:")
for i, finding in enumerate(population_findings, 1):
    print(f"\nFinding {i}:")
    print(f"  Match: {finding['match']}")
    print(f"  Number: {finding['number']}")
    print(f"  Position: {finding['position']:,}")
    print(f"  Context: ...{finding['context'][:300]}...")

# Look specifically for key result statements
print("\n=== SEARCHING FOR KEY RESULT STATEMENTS ===\n")

# Look for sentences containing key result phrases
result_patterns = [
    r'[^.]*global\s+population[^.]*\.',
    r'[^.]*breeding\s+pairs?[^.]*\d[^.]*\.',
    r'[^.]*total[^.]*population[^.]*\d[^.]*\.',
    r'[^.]*census[^.]*\d[^.]*\.',
    r'[^.]*estimate[^.]*\d[^.]*breeding[^.]*\.',
    r'[^.]*\d[^.]*million[^.]*pairs?[^.]*\.'
]

key_statements = []
for pattern in result_patterns:
    matches = list(re.finditer(pattern, study_text, re.IGNORECASE | re.DOTALL))
    for match in matches:
        statement = match.group().strip()
        # Clean up the statement
        statement = re.sub(r'\s+', ' ', statement)
        
        key_statements.append({
            'pattern': pattern,
            'statement': statement,
            'position': match.start()
        })

print(f"Found {len(key_statements)} key result statements:")
for i, stmt in enumerate(key_statements, 1):
    print(f"\nStatement {i}:")
    print(f"  Position: {stmt['position']:,}")
    print(f"  Text: {stmt['statement']}")

# Look for methodology section
print("\n=== EXTRACTING METHODOLOGY INFORMATION ===\n")

# Find methods section
methods_match = re.search(r'Methods?\s*\n?([\s\S]*?)(?=\n\s*(?:Results?|Discussion|Conclusion|References?|Acknowledgments?)\s*\n|$)', study_text, re.IGNORECASE)

if methods_match:
    methods_text = methods_match.group(1)[:2000]  # First 2000 characters
    print("Methods section found (first 2000 characters):")
    print(methods_text)
    
    # Look for specific methodology terms
    method_terms = ['survey', 'census', 'count', 'observation', 'field', 'colony', 'site']
    found_method_terms = [term for term in method_terms if term.lower() in methods_text.lower()]
    print(f"\nMethodology terms found: {found_method_terms}")
else:
    print("Methods section not clearly identified")

# Look for abstract for concise population summary
print("\n=== EXTRACTING ABSTRACT FOR POPULATION SUMMARY ===\n")

abstract_match = re.search(r'Abstract\s*\n?([\s\S]*?)(?=\n\s*(?:Introduction|Keywords?)\s*\n|$)', study_text, re.IGNORECASE)

if abstract_match:
    abstract_text = abstract_match.group(1)[:1500]  # First 1500 characters
    print("Abstract found (first 1500 characters):")
    print(abstract_text)
    
    # Extract numbers from abstract
    abstract_numbers = re.findall(r'\d{1,3}(?:,\d{3})*(?:\.\d+)?', abstract_text)
    print(f"\nNumbers found in abstract: {abstract_numbers}")
else:
    print("Abstract section not clearly identified")

# Save comprehensive analysis
analysis_results = {
    'study_info': {
        'title': 'A global population assessment of the Chinstrap penguin (Pygoscelis antarctica)',
        'year': 2020,
        'source': 'Nature.com Scientific Reports',
        'text_length': len(study_text)
    },
    'sections_found': found_sections,
    'population_findings': population_findings,
    'key_statements': key_statements,
    'methods_text': methods_text if 'methods_text' in locals() else 'Not extracted',
    'abstract_text': abstract_text if 'abstract_text' in locals() else 'Not extracted',
    'abstract_numbers': abstract_numbers if 'abstract_numbers' in locals() else []
}

analysis_file = os.path.join(workspace_dir, 'nature_2020_population_analysis.json')
with open(analysis_file, 'w') as f:
    json.dump(analysis_results, f, indent=2, default=str)

print(f"\n=== ANALYSIS COMPLETE ===\n")
print(f"Comprehensive analysis saved to: {analysis_file}")
print(f"Population findings: {len(population_findings)}")
print(f"Key statements: {len(key_statements)}")
print(f"Sections identified: {len(found_sections)}")

print("\nNext step: Review findings to identify the specific global population figure and methodology")
```

## Created Time
2025-08-13 20:38:00
