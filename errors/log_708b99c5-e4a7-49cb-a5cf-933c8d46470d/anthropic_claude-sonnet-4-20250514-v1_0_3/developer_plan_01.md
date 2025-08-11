# Developer Plan 01

## Plan
Search for the DeepFruits fruit detection paper from 2016 and locate its Connected Papers visualization graph. Examine the graph to identify the largest bubble and determine what feature or metric determines bubble sizes in Connected Papers visualizations. Extract information about what specific characteristic caused the largest bubble to be that particular size.

## Description
This is the optimal first step because: (1) We need to locate the specific DeepFruits fruit detection paper from 2016 and access its Connected Papers graph visualization, (2) No previous research has been conducted on this topic, (3) Expected outcome is to find the Connected Papers graph and understand the bubble sizing methodology to identify what feature determines the largest bubble's size, (4) This directly addresses the TASK requirement to determine what feature caused the largest bubble to be the size it is on the Connected Papers graph

## Episodic Examples
### Development Step 5: 2016 Uganda SPFMV & SPCSV Diagnostics: Chemical Reagents and EC Numbers

**Description**: Search for a 2016 research paper about SPFMV (Sweet Potato Feathery Mottle Virus) and SPCSV (Sweet Potato Chlorotic Stunt Virus) from Uganda (Pearl of Africa). Focus on finding academic publications that discuss virus testing methods and identify the specific chemicals used for viral detection. Look for papers that mention EC numbers for chemicals used in diagnostic procedures, laboratory protocols, or testing methodologies for these sweet potato viruses.

**Use Cases**:
- Crop disease diagnostic protocol aggregation from research JSON for plant pathology labs in Uganda to rapidly identify chemicals (EC numbers) used in SPFMV/SPCSV testing
- Automated literature screening for EC numbers associated with antimicrobial enzymes in clinical microbiology research workflows
- Pharmaceutical R&D chemical assay identification by parsing JSON search results from PubMed and Wiley to flag target enzyme inhibitors via EC numbers
- Environmental enzyme tracking by extracting EC numbers for pollutant-degrading catalysts from open-access databases for bioremediation studies
- Agricultural extension content curation by collecting region-specific virus testing methods and reagents from academic papers to support field diagnostics
- Laboratory compliance auditing by scanning SOP and protocol JSON exports for mandatory EC-numbered reagents to ensure regulatory standards
- Academic library indexing enhancement by auto-tagging publications with detected EC numbers and domain keywords for improved discoverability
- Patent landscape analysis by mining chemical EC identifiers from patent search results to map innovation in enzyme-based diagnostic assays

```
import os
import json
from datetime import datetime

# Simple, focused analysis of Uganda SPFMV/SPCSV search results
# Avoiding generator expressions and complex variable scoping

print("=" * 80)
print("SIMPLE ANALYSIS OF UGANDA SWEET POTATO VIRUS SEARCH RESULTS")
print("=" * 80)

# Find the search results file
workspace_files = []
if os.path.exists('workspace'):
    for file in os.listdir('workspace'):
        if file.startswith('uganda_spfmv_spcsv_2016_search_results_') and file.endswith('.json'):
            workspace_files.append(file)
            print(f"Found search results file: {file}")

if not workspace_files:
    print("No search results files found in workspace.")
else:
    # Use the most recent file
    latest_file = sorted(workspace_files)[-1]
    results_file = f'workspace/{latest_file}'
    
    print(f"\nAnalyzing file: {results_file}")
    
    # Load the search results
    with open(results_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\nFile structure inspection:")
    print(f"Top-level keys: {list(data.keys())}")
    
    if 'search_results' in data:
        print(f"Number of search queries: {len(data['search_results'])}")
        if len(data['search_results']) > 0:
            sample_query = data['search_results'][0]
            print(f"Sample query keys: {list(sample_query.keys())}")
            if 'results' in sample_query and len(sample_query['results']) > 0:
                sample_result = sample_query['results'][0]
                print(f"Sample result keys: {list(sample_result.keys())}")
    
    print("\n" + "=" * 80)
    print("EXTRACTING KEY FINDINGS - SIMPLE APPROACH")
    print("=" * 80)
    
    # Simple analysis without complex variable scoping
    total_results = 0
    wiley_papers = []
    ec_number_mentions = []
    uganda_papers = []
    both_virus_papers = []
    academic_sources = []
    
    # Process each search query
    for query_idx, query_data in enumerate(data.get('search_results', []), 1):
        query_text = query_data.get('query', '')
        results_list = query_data.get('results', [])
        total_results += len(results_list)
        
        print(f"\nQuery {query_idx}: {query_text}")
        print(f"Results: {len(results_list)}")
        print("-" * 60)
        
        # Process each result in this query
        for result_idx, single_result in enumerate(results_list, 1):
            # Extract basic information
            result_title = single_result.get('title', '')
            result_link = single_result.get('link', '')
            result_snippet = single_result.get('snippet', '')
            
            # Create a simple result object
            result_obj = {
                'query': query_text,
                'title': result_title,
                'link': result_link,
                'snippet': result_snippet
            }
            
            # Check for Wiley paper (specific target)
            if 'wiley.com' in result_link and 'jph.12451' in result_link:
                wiley_papers.append(result_obj)
                print(f"  🎯 WILEY TARGET PAPER: {result_title}")
                print(f"     URL: {result_link}")
            
            # Check for EC numbers in snippet
            if '1.11.1.7' in result_snippet or '3.1.3.1' in result_snippet:
                ec_number_mentions.append(result_obj)
                print(f"  🧪 EC NUMBERS FOUND: {result_title}")
                print(f"     Snippet: {result_snippet[:200]}...")
            
            # Check for Uganda mentions
            if 'uganda' in result_title.lower() or 'uganda' in result_snippet.lower():
                uganda_papers.append(result_obj)
            
            # Check for both viruses
            title_lower = result_title.lower()
            snippet_lower = result_snippet.lower()
            if ('spfmv' in title_lower or 'spfmv' in snippet_lower) and ('spcsv' in title_lower or 'spcsv' in snippet_lower):
                both_virus_papers.append(result_obj)
                print(f"  🦠 BOTH VIRUSES: {result_title[:60]}...")
            
            # Check for academic sources
            academic_domains = ['researchgate', 'pubmed', 'ncbi', 'sciencedirect', 'springer', 'wiley', '.edu', 'doi.org', 'core.ac.uk']
            is_academic = False
            for domain in academic_domains:
                if domain in result_link:
                    is_academic = True
                    break
            
            if is_academic:
                academic_sources.append(result_obj)
    
    print("\n" + "=" * 80)
    print("FINAL ANALYSIS SUMMARY")
    print("=" * 80)
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"Total search results processed: {total_results}")
    print(f"Wiley target papers found: {len(wiley_papers)}")
    print(f"EC number mentions found: {len(ec_number_mentions)}")
    print(f"Uganda-related papers: {len(uganda_papers)}")
    print(f"Both viruses mentioned: {len(both_virus_papers)}")
    print(f"Academic sources: {len(academic_sources)}")
    
    # Display key findings
    if wiley_papers:
        print(f"\n✅ TARGET WILEY PAPER IDENTIFIED:")
        for paper in wiley_papers:
            print(f"  Title: {paper['title']}")
            print(f"  URL: {paper['link']}")
            print(f"  Snippet: {paper['snippet'][:300]}...")
    
    if ec_number_mentions:
        print(f"\n✅ EC NUMBERS FOUND:")
        for ec_result in ec_number_mentions:
            print(f"  Source: {ec_result['title']}")
            print(f"  URL: {ec_result['link']}")
            print(f"  Content: {ec_result['snippet']}")
    
    # Look specifically for the EC numbers 1.11.1.7 and 3.1.3.1
    specific_ec_found = []
    for query_data in data.get('search_results', []):
        for result in query_data.get('results', []):
            snippet_text = result.get('snippet', '')
            if '1.11.1.7' in snippet_text and '3.1.3.1' in snippet_text:
                specific_ec_found.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': snippet_text
                })
    
    if specific_ec_found:
        print(f"\n🔬 SPECIFIC EC NUMBERS (1.11.1.7 & 3.1.3.1) LOCATED:")
        for ec_item in specific_ec_found:
            print(f"  Title: {ec_item['title']}")
            print(f"  URL: {ec_item['link']}")
            print(f"  Content: {ec_item['snippet']}")
    
    # Create final assessment
    mission_success = len(wiley_papers) > 0 and len(specific_ec_found) > 0
    
    print(f"\n🎯 MISSION STATUS:")
    if mission_success:
        print("✅ SUCCESS: Target research paper and EC numbers successfully identified")
        print("\n📋 ANSWER TO ORIGINAL QUESTION:")
        print("The EC numbers of the two most commonly used chemicals for virus")
        print("testing in the 2016 Uganda SPFMV/SPCSV research paper are:")
        print("• 1.11.1.7")
        print("• 3.1.3.1")
        print("\nSource: Identified through comprehensive search of academic databases")
        print("Target paper: Effects of Sweet Potato Feathery Mottle Virus (Wiley publication)")
    else:
        print("⚠️ PARTIAL SUCCESS: Some targets identified, further analysis may be needed")
    
    # Save simple analysis results
    simple_analysis_file = f'workspace/uganda_virus_simple_analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    simple_analysis_data = {
        'analysis_timestamp': datetime.now().isoformat(),
        'total_results_processed': total_results,
        'mission_success': mission_success,
        'key_findings': {
            'wiley_papers': wiley_papers,
            'ec_number_mentions': ec_number_mentions,
            'specific_ec_numbers_found': specific_ec_found,
            'uganda_papers_count': len(uganda_papers),
            'both_virus_papers_count': len(both_virus_papers),
            'academic_sources_count': len(academic_sources)
        },
        'answer': {
            'ec_numbers': ['1.11.1.7', '3.1.3.1'] if specific_ec_found else [],
            'research_paper_identified': len(wiley_papers) > 0,
            'chemicals_for_virus_testing': 'Two chemicals with EC numbers 1.11.1.7 and 3.1.3.1 for SPFMV/SPCSV testing in Uganda 2016 research'
        }
    }
    
    with open(simple_analysis_file, 'w', encoding='utf-8') as f:
        json.dump(simple_analysis_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSimple analysis results saved to: {simple_analysis_file}")
    print("\n✅ Analysis completed successfully with simplified approach.")
```

### Development Step 61: Locate and Extract Fish Bag Volume (m³) from dragon_diet_fish_bag.pdf

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Fisheries logistics automation for a seafood export company to extract fish bag volumes from shipping PDFs and optimize container load planning
- Marine biology research pipeline to batch-process field study reports and compile fish bag volume data for population density modeling
- Aquarium retail inventory system integration that parses vendor PDF catalogs for fish bag dimensions and updates product listings automatically
- Quality control compliance tool for food safety auditors to verify reported packing volumes in seafood transport documents against regulatory limits
- E-commerce platform enhancement to auto-extract packaging volume details from supplier spec sheets in PDF form and drive dynamic shipping cost calculations
- Supply chain analytics dashboard for cold-chain managers to aggregate cubic meter capacities from multiple carrier PDF manifests and balance temperature-controlled loads
- Veterinary supply management software module that reads equipment and containment unit volumes from manufacturer PDFs to reconcile against hospital storage capacity requirements

```
import os
import re
from PyPDF2 import PdfReader

print("=== FISH BAG VOLUME EXTRACTION (VARIABLE NAME FIX) ===")

# Step 1: Locate the workspace directory (robust to random suffixes)
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    print("Error: No directory starting with 'workspace' found in current working directory.")
    exit(1)
workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Step 2: Locate the PDF file
files = os.listdir(workspace_dir)
print(f"Files in '{workspace_dir}': {files}\n")
pdf_name = None
for fname in files:
    if fname.lower().endswith('.pdf') and 'dragon_diet_fish_bag' in fname.lower():
        pdf_name = fname
        break
if not pdf_name:
    print("Error: 'dragon_diet_fish_bag.pdf' not found in workspace directory.")
    exit(1)
pdf_path = os.path.join(workspace_dir, pdf_name)
print(f"Found PDF: {pdf_path}\n")

# Step 3: Read PDF and search for volume references
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Total pages in PDF: {num_pages}\n")

# Improved regex to capture number + cubic meter units
volume_pattern = re.compile(r"(\d+(?:[.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)
keyword_terms = ['volume', 'm3', 'm³', 'cubic meter']

findings = []
for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    lower_text = text.lower()  # renamed to avoid NameError

    # Print a short preview for debugging
    print(f"--- Page {i} Preview ---")
    preview = text[:200].replace('\n', ' ')
    print(preview + ('...' if len(text) > 200 else ''))

    # Check for any volume-related keyword
    if any(term in lower_text for term in keyword_terms):
        print(f"Page {i} contains volume-related term(s). Searching regex matches...")
        for match in volume_pattern.finditer(text):
            full_match = match.group(0)
            vol_str = match.group(1)
            unit_str = full_match[len(vol_str):].strip()
            start, end = match.start(), match.end()
            context = text[max(0, start-50):min(len(text), end+50)].replace('\n', ' ')

            print(f"Match on page {i}: '{full_match}' -> value: {vol_str} unit: {unit_str}")
            print(f"Context: ...{context.strip()}...")

            findings.append({
                'page': i,
                'value': vol_str,
                'unit': unit_str,
                'context': context.strip()
            })

# Step 4: Report or save
if not findings:
    print("\nNo volume number found matching the pattern.")
else:
    first = findings[0]
    volume_value = first['value']
    unit = first['unit']
    page_no = first['page']
    print(f"\n>>> Extracted fish bag volume: {volume_value} {unit} (from page {page_no})")

    out_path = os.path.join(workspace_dir, 'fish_bag_volume.txt')
    with open(out_path, 'w') as f:
        f.write(f"{volume_value} {unit}\n")
    print(f"Volume saved to: {out_path}")
```

### Development Step 66: Extract Fish Bag Volume (cubic meters) from Dragon Diet PDF

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Fisheries logistics automation and inventory forecasting for seafood distributors
- Aquaculture research data extraction and feed ratio calculation in marine biology labs
- Environmental compliance auditing and carbon footprint estimation for marine transport NGOs
- Food safety regulatory verification and container specification validation for health inspectors
- E-commerce product catalog enrichment and metadata population for online seafood retailers
- Aquarium operations scheduling and water quality management for public aquariums and zoos
- Academic publication support and experimental methodology documentation for marine science researchers
- ERP integration and packaging data synchronization for seafood manufacturing plants

```
import os
import re
from PyPDF2 import PdfReader

print("=== FISH BAG VOLUME EXTRACTION (FILTER BY 'bag' CONTEXT) ===")

# Step 1: Locate the workspace directory (handles random suffixes)
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    print("Error: No directory starting with 'workspace' found in current working directory.")
    exit(1)
workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Step 2: Locate the PDF file in workspace
files = os.listdir(workspace_dir)
print(f"Files in '{workspace_dir}': {files}\n")
pdf_name = None
for fname in files:
    if fname.lower().endswith('.pdf') and 'dragon_diet_fish_bag' in fname.lower():
        pdf_name = fname
        break
if not pdf_name:
    print("Error: 'dragon_diet_fish_bag.pdf' not found in workspace directory.")
    exit(1)
pdf_path = os.path.join(workspace_dir, pdf_name)
print(f"Found PDF: {pdf_path}\n")

# Step 3: Read PDF and scan pages for volume patterns
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Total pages in PDF: {num_pages}\n")

# Regex to capture numbers + cubic meter units (e.g., '0.1777 m3', '0.1777 m³', '5 cubic meters')
volume_pattern = re.compile(r"(\d+(?:[.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)

# We'll look for the term 'bag' in the regex match context to pick the fish-bag volume
found_volume = None
found_unit = None
found_page = None

for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    # Print a short preview for debugging
    print(f"--- Page {i} Preview ---")
    preview = text.replace('\n', ' ')[:200]
    print(preview + ('...' if len(text) > 200 else ''))

    # Search for all volume matches on this page
    for match in volume_pattern.finditer(text):
        vol_str = match.group(1)
        full_match = match.group(0)
        unit_str = full_match[len(vol_str):].strip()
        start, end = match.start(), match.end()
        context = text[max(0, start-50):min(len(text), end+50)].replace('\n', ' ')

        # Debug each match
        print(f"Match on page {i}: '{full_match}' -> value: {vol_str}, unit: {unit_str}")
        print(f"Context snippet: ...{context.strip()}...\n")

        # Filter for the fish bag capacity by checking 'bag' in the context
        if 'bag' in context.lower():
            found_volume = vol_str
            found_unit = unit_str
            found_page = i
            print(f"--> Selected as fish-bag volume (contains 'bag'): {vol_str} {unit_str} (page {i})\n")
            break
    # If we found it, no need to scan further pages
    if found_volume:
        break

# Step 4: Report result and save to file
if not found_volume:
    print("\nNo fish-bag volume found in any page.")
else:
    result_line = f"{found_volume} {found_unit}"
    print(f"\n>>> Extracted fish bag volume: {result_line} (from page {found_page})")
    out_path = os.path.join(workspace_dir, 'fish_bag_volume.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(result_line + "\n")
    print(f"Volume saved to: {out_path}")
```

### Development Step 64: Locate and extract the fish bag volume (in cubic meters) from dragon_diet_fish_bag.pdf.

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Aquaculture feed optimization by extracting fish bag volume from culture protocol PDFs to calculate precise feed ratios
- Fisheries logistics planning by parsing transport container volumes in shipping manuals for route capacity management
- Aquarium retail compliance auditing by automating extraction of fish bag capacities from product specification sheets to ensure accurate labeling
- Ichthyology laboratory experimental standardization by gathering water volume data from multiple research PDFs to normalize test conditions
- Marine conservation impact assessments by extracting habitat simulation volume parameters from environmental report PDFs
- Pet supply catalog automation by reading digital product fact sheets to update e-commerce listings with accurate fish bag volume specifications
- Regulatory documentation verification for animal welfare by scanning facility guideline PDFs for container volume metrics to maintain compliance
- Custom fish transport app development by dynamically retrieving bag volume data from vendor PDFs to optimize water and oxygen requirements

```
import os
import re
from PyPDF2 import PdfReader

print("=== FISH BAG VOLUME EXTRACTION (CONSISTENT VARIABLE NAMES) ===")

# Step 1: Locate the workspace directory (handles random suffixes)
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    print("Error: No directory starting with 'workspace' found in current working directory.")
    exit(1)
workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Step 2: Locate the dragon_diet_fish_bag PDF file
dir_files = os.listdir(workspace_dir)
print(f"Files in '{workspace_dir}': {dir_files}\n")
pdf_name = None
for fname in dir_files:
    if fname.lower().endswith('.pdf') and 'dragon_diet_fish_bag' in fname.lower():
        pdf_name = fname
        break
if not pdf_name:
    print("Error: 'dragon_diet_fish_bag.pdf' not found in workspace directory.")
    exit(1)
pdf_path = os.path.join(workspace_dir, pdf_name)
print(f"Found PDF: {pdf_path}\n")

# Step 3: Read PDF and search for fish bag volume
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Total pages in PDF: {num_pages}\n")

# Compile regex for numbers + cubic meter units
volume_pattern = re.compile(r"(\d+(?:[.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)
keyword_terms = ['volume', 'm3', 'm³', 'cubic meter']
findings = []

for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    lower_text = text.lower()  # define lowercase copy before use

    # Print a short preview for debugging
    print(f"--- Page {i} Preview ---")
    preview = text.replace('\n', ' ')[:200]
    print(preview + ('...' if len(text) > 200 else ''))

    # Check for any volume-related keyword in lowercase text
    if any(term in lower_text for term in keyword_terms):
        print(f"Page {i} contains volume-related term(s). Searching regex matches...")
        for match in volume_pattern.finditer(text):
            full_match = match.group(0)
            vol_str = match.group(1)
            unit_str = full_match[len(vol_str):].strip()
            start, end = match.start(), match.end()
            context = text[max(0, start-50):min(len(text), end+50)].replace('\n', ' ')

            print(f"Match on page {i}: '{full_match}' -> value: {vol_str}, unit: {unit_str}")
            print(f"Context: ...{context.strip()}...")

            findings.append({
                'page': i,
                'value': vol_str,
                'unit': unit_str,
                'context': context.strip()
            })

# Step 4: Report or save the first finding
if not findings:
    print("\nNo volume number found matching the pattern.")
else:
    first = findings[0]
    volume_value = first['value']
    unit = first['unit']
    page_no = first['page']
    print(f"\n>>> Extracted fish bag volume: {volume_value} {unit} (from page {page_no})")

    out_path = os.path.join(workspace_dir, 'fish_bag_volume.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"{volume_value} {unit}\n")
    print(f"Volume saved to: {out_path}")
```

### Development Step 63: Extract Fish Bag Volume (m³) from Dragon Diet Fish Bag PDF

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Automated capacity verification for aquaculture supply chains, extracting fish bag volumes from PDF spec sheets to optimize inventory ordering
- Regulatory compliance checks for fish transport, parsing PDF documentation to confirm bag volume meets legal requirements for animal welfare
- Quality assurance reporting in hatcheries, auto-extracting bag volumes from technical manuals to populate daily inspection logs
- Competitive product benchmarking in aquarium retail, mining competitor PDFs for fish bag volume data to compare storage offerings
- Marine biology research data aggregation, scraping fish bag volume figures from published PDFs to standardize dataset for statistical modeling
- Logistics route planning for live fish transport, reading fish bag capacity from vendor PDFs to calculate truck loading and weight distribution
- ERP system integration for farm management, batch-processing PDF equipment catalogs to auto-fill fish bag volume fields in the company database

```
import os
import re
from PyPDF2 import PdfReader

print("=== FISH BAG VOLUME EXTRACTION (FINAL FIX) ===")

# Step 1: Find the workspace directory (handles random suffixes)
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    print("Error: No directory starting with 'workspace' found in current working directory.")
    exit(1)
workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Step 2: Locate the PDF file in workspace
dir_files = os.listdir(workspace_dir)
print(f"Files in '{workspace_dir}': {dir_files}\n")
pdf_name = None
for fname in dir_files:
    if fname.lower().endswith('.pdf') and 'dragon_diet_fish_bag' in fname.lower():
        pdf_name = fname
        break
if not pdf_name:
    print("Error: 'dragon_diet_fish_bag.pdf' not found in workspace directory.")
    exit(1)
pdf_path = os.path.join(workspace_dir, pdf_name)
print(f"Found PDF: {pdf_path}\n")

# Step 3: Read PDF and search for fish bag volume
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Total pages in PDF: {num_pages}\n")

# Compile regex for numbers + cubic meter units
volume_pattern = re.compile(r"(\d+(?:[.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)
keyword_terms = ['volume', 'm3', 'm³', 'cubic meter']
findings = []

for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    lower_text = text.lower()  # define lowercase copy before use

    # Print a short preview for debugging
    print(f"--- Page {i} Preview ---")
    preview = text.replace('\n', ' ')[:200]
    print(preview + ('...' if len(text) > 200 else ''))

    # Check for any volume-related keyword in lowercase text
    if any(term in lower_text for term in keyword_terms):
        print(f"Page {i} contains volume-related term(s). Searching regex matches...")
        for match in volume_pattern.finditer(text):
            full_match = match.group(0)
            vol_str = match.group(1)
            unit_str = full_match[len(vol_str):].strip()
            start, end = match.start(), match.end()
            context = text[max(0, start-50):min(len(text), end+50)].replace('\n', ' ')

            print(f"Match on page {i}: '{full_match}' -> value: {vol_str}, unit: {unit_str}")
            print(f"Context: ...{context.strip()}...")

            findings.append({
                'page': i,
                'value': vol_str,
                'unit': unit_str,
                'context': context.strip()
            })

# Step 4: Report or save the first finding
if not findings:
    print("\nNo volume number found matching the pattern.")
else:
    first = findings[0]
    volume_value = first['value']
    unit = first['unit']
    page_no = first['page']
    print(f"\n>>> Extracted fish bag volume: {volume_value} {unit} (from page {page_no})")

    out_path = os.path.join(workspace_dir, 'fish_bag_volume.txt')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f"{volume_value} {unit}\n")
    print(f"Volume saved to: {out_path}")
```

## Created Time
2025-08-11 07:39:51
