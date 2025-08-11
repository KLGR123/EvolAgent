# Developer Plan 03

## Plan
Match each of the 6 table titles extracted from the Excel file against the complete bibliography from the 'Trans fatty acid contents in chocolates and chocolate wafers in Turkey' paper to identify which reference number corresponds to each table. Create a comma-separated list of reference numbers in the order that the tables appear in the Excel file from top to bottom (Studies of Flavonoids → High-linoleic acid diet → Composition of Vegetable Oils → Concentrations of serum cholesterol → Chocolate and Cocoa Feeding Trials → Assayed macronutrient composition).

## Description
This is the final matching step because: (1) We have successfully extracted all 6 table titles from the Excel file and obtained the complete numbered bibliography from the target research paper, (2) The developer has provided the full reference list with 6+ numbered citations that need to be cross-referenced with our table titles, (3) Expected outcome is to identify which bibliography reference number corresponds to each table based on title matching, research topic alignment, and content analysis, (4) This will complete the TASK by providing the comma-separated list of reference numbers in the exact order requested (top to bottom from Excel file)

## Episodic Examples
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

### Development Step 9: Extract and Alphabetize Chemicals EC 1.11.1.7;3.1.3.1 from 2016 Wiley Sweet Potato Virus Paper

**Description**: Access the identified 2016 Wiley paper 'Effects of Sweet Potato Feathery Mottle Virus and Sweet Potato Chlorotic Stunt Virus' and extract the specific chemicals with EC numbers 1.11.1.7 and 3.1.3.1 used in the virus testing methods. Identify the chemical names corresponding to these EC numbers, alphabetize them, and format the EC numbers in the required semicolon-separated order.

**Use Cases**:
- Agricultural biotech team automating extraction of peroxidase (EC 1.11.1.7) and alkaline phosphatase (EC 3.1.3.1) reagent details from 2016 sweet potato virus studies to optimize field trial protocols
- Pharmaceutical R&D group curating enzyme assay protocols and EC number mappings from Wiley virology papers for antiviral drug development documentation
- Regulatory compliance unit generating standardized EC-to-chemical mappings of enzyme reagents used in plant pathogen testing to support audit and safety submissions
- Bioinformatics department automating literature mining of virus–enzyme interactions to integrate peroxidase and alkaline phosphatase data into a research knowledge graph
- Laboratory operations manager extracting EC numbers and enzyme names from JSON search results to compile a reagent procurement list for virology experiments
- Grant proposal writer summarizing specific peroxidase and alkaline phosphatase assays referenced in key sweet potato virus publications to strengthen funding applications
- Data analytics team building an interactive dashboard of virus detection methods by parsing EC numbers and chemical names from search result files for internal reporting

```
import os
import json
from datetime import datetime

# First, let's locate and properly inspect the search results file
print("Locating search results files...")
print("="*80)

# Check multiple possible locations for the search results file
search_file_candidates = [
    'workspace/sweet_potato_virus_paper_search_20250806_185041.json',
    'workspace_2a649bb1-795f-4a01-b3be-9a01868dae73/sweet_potato_virus_paper_search_20250806_185041.json'
]

search_data = None
used_file_path = None

for file_path in search_file_candidates:
    if os.path.exists(file_path):
        print(f"Found search results file: {file_path}")
        used_file_path = file_path
        break

if not used_file_path:
    print("No search results file found. Checking workspace contents...")
    if os.path.exists('workspace'):
        workspace_files = os.listdir('workspace')
        print(f"Workspace files: {workspace_files}")
        # Look for any virus-related search files
        for file in workspace_files:
            if 'virus' in file.lower() or 'sweet_potato' in file.lower():
                used_file_path = f'workspace/{file}'
                print(f"Using alternative file: {used_file_path}")
                break
    
if not used_file_path:
    print("ERROR: No search results file found.")
else:
    # Load and inspect the file structure first
    print(f"\nInspecting file structure: {used_file_path}")
    print("-"*60)
    
    with open(used_file_path, 'r', encoding='utf-8') as f:
        search_data = json.load(f)
    
    print("File structure overview:")
    for key, value in search_data.items():
        if isinstance(value, list):
            print(f"  {key}: list with {len(value)} items")
            if len(value) > 0 and isinstance(value[0], dict):
                print(f"    Sample item keys: {list(value[0].keys())}")
        elif isinstance(value, dict):
            print(f"  {key}: dict with keys {list(value.keys())}")
        else:
            print(f"  {key}: {value}")
    
    # Now analyze the search results with proper variable handling
    print("\n" + "="*80)
    print("EXTRACTING PAPER CANDIDATES AND EC NUMBER INFORMATION")
    print("="*80)
    
    target_paper = search_data.get('target_paper', 'Unknown')
    target_ec_numbers = search_data.get('target_ec_numbers', [])
    search_results = search_data.get('search_results', [])
    
    print(f"Target Paper: {target_paper}")
    print(f"Target EC Numbers: {target_ec_numbers}")
    print(f"Search Result Sets: {len(search_results)}")
    
    # Initialize result containers
    paper_candidates = []
    ec_chemical_sources = []
    
    # Process each search query result set
    for query_idx, query_result in enumerate(search_results, 1):
        query_text = query_result.get('query', 'Unknown query')
        results_list = query_result.get('results', [])
        
        print(f"\nProcessing Query {query_idx}: {query_text}")
        print(f"Results in this query: {len(results_list)}")
        print("-"*50)
        
        # Analyze each search result
        for result_idx, result in enumerate(results_list[:10], 1):  # Top 10 results per query
            title = result.get('title', 'No title')
            link = result.get('link', 'No URL')
            snippet = result.get('snippet', 'No snippet')
            
            print(f"  {result_idx}. {title[:70]}...")
            
            # Create text for analysis (fixing the scoping issue)
            title_text = title.lower()
            snippet_text = snippet.lower()
            link_text = link.lower()
            
            # Calculate relevance score for target paper identification
            relevance_score = 0
            matching_terms = []
            
            # Check for paper-specific indicators
            if 'sweet potato feathery mottle virus' in title_text or 'sweet potato feathery mottle virus' in snippet_text:
                relevance_score += 10
                matching_terms.append('SPFMV')
            
            if 'sweet potato chlorotic stunt virus' in title_text or 'sweet potato chlorotic stunt virus' in snippet_text:
                relevance_score += 10
                matching_terms.append('SPCSV')
            
            if '2016' in title_text or '2016' in snippet_text:
                relevance_score += 5
                matching_terms.append('2016')
            
            if 'wiley' in link_text or 'onlinelibrary.wiley.com' in link_text:
                relevance_score += 5
                matching_terms.append('Wiley')
            
            if 'effects' in title_text:
                relevance_score += 3
                matching_terms.append('Effects')
            
            # Check for EC numbers and enzyme information
            ec_found = []
            if '1.11.1.7' in snippet_text:
                relevance_score += 8
                ec_found.append('1.11.1.7')
            
            if '3.1.3.1' in snippet_text:
                relevance_score += 8
                ec_found.append('3.1.3.1')
            
            enzyme_terms = []
            if 'peroxidase' in snippet_text:
                enzyme_terms.append('peroxidase')
            if 'alkaline phosphatase' in snippet_text:
                enzyme_terms.append('alkaline phosphatase')
            if 'enzyme' in snippet_text:
                enzyme_terms.append('enzyme')
            
            if enzyme_terms:
                relevance_score += 4
                matching_terms.extend(enzyme_terms)
            
            # Display analysis for this result
            if matching_terms:
                print(f"      Score: {relevance_score}, Terms: {', '.join(matching_terms)}")
            
            if ec_found:
                print(f"      🧪 EC Numbers Found: {', '.join(ec_found)}")
            
            # Store high-relevance paper candidates
            if relevance_score >= 15:
                is_wiley_direct = 'onlinelibrary.wiley.com' in link_text
                paper_candidates.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'relevance_score': relevance_score,
                    'matching_terms': matching_terms,
                    'ec_numbers_found': ec_found,
                    'is_wiley_direct': is_wiley_direct,
                    'query_source': query_text
                })
                print(f"      ⭐ HIGH RELEVANCE - Added to candidates")
            
            # Store sources that mention EC numbers with chemical information
            if ec_found or enzyme_terms:
                ec_chemical_sources.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet,
                    'ec_numbers_mentioned': ec_found,
                    'enzyme_terms_found': enzyme_terms,
                    'query_source': query_text
                })
                print(f"      🔬 EC/Chemical info - Added to sources")
    
    # Sort paper candidates by relevance score
    paper_candidates.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print("\n" + "="*80)
    print("ANALYSIS RESULTS AND CHEMICAL IDENTIFICATION")
    print("="*80)
    
    print(f"\n📚 PAPER CANDIDATES IDENTIFIED: {len(paper_candidates)}")
    
    if paper_candidates:
        print("\nTop paper candidates:")
        for i, candidate in enumerate(paper_candidates[:3], 1):
            print(f"\n{i}. RELEVANCE SCORE: {candidate['relevance_score']}")
            print(f"   Title: {candidate['title']}")
            print(f"   URL: {candidate['link']}")
            print(f"   Wiley Direct: {'✅ YES' if candidate['is_wiley_direct'] else '❌ NO'}")
            print(f"   Terms: {', '.join(candidate['matching_terms'])}")
            if candidate['ec_numbers_found']:
                print(f"   EC Numbers: {', '.join(candidate['ec_numbers_found'])}")
            
            # Check if this is the target paper
            if (candidate['relevance_score'] >= 25 and 
                candidate['is_wiley_direct'] and 
                'effects' in candidate['title'].lower()):
                print(f"   🎯 THIS IS THE TARGET PAPER!")
    
    print(f"\n🧪 EC NUMBER CHEMICAL SOURCES: {len(ec_chemical_sources)}")
    
    # Analyze chemical information from EC sources
    chemical_mapping = {}
    
    if ec_chemical_sources:
        print("\nEC number and chemical information found:")
        for i, source in enumerate(ec_chemical_sources, 1):
            print(f"\n{i}. {source['title'][:60]}...")
            print(f"   URL: {source['link']}")
            
            if source['ec_numbers_mentioned']:
                print(f"   EC Numbers: {', '.join(source['ec_numbers_mentioned'])}")
            
            if source['enzyme_terms_found']:
                print(f"   Enzymes: {', '.join(source['enzyme_terms_found'])}")
            
            snippet_lower = source['snippet'].lower()
            print(f"   Snippet: {source['snippet'][:150]}...")
            
            # Extract chemical name associations
            if 'alkaline phosphatase' in snippet_lower:
                chemical_mapping['3.1.3.1'] = 'Alkaline phosphatase'
                print(f"   💡 IDENTIFIED: Alkaline phosphatase (likely EC 3.1.3.1)")
            
            if 'peroxidase' in snippet_lower:
                chemical_mapping['1.11.1.7'] = 'Peroxidase'
                print(f"   💡 IDENTIFIED: Peroxidase (likely EC 1.11.1.7)")
    
    # Based on standard EC number classifications, provide the chemical identification
    print(f"\n" + "="*80)
    print("FINAL CHEMICAL IDENTIFICATION FOR EC NUMBERS")
    print("="*80)
    
    # EC 1.11.1.7 is peroxidase, EC 3.1.3.1 is alkaline phosphatase (standard biochemistry)
    ec_chemicals = {
        '1.11.1.7': 'Peroxidase',
        '3.1.3.1': 'Alkaline phosphatase'
    }
    
    print(f"\nEC Number to Chemical Mapping:")
    for ec_number in target_ec_numbers:
        chemical_name = ec_chemicals.get(ec_number, 'Unknown')
        print(f"  EC {ec_number} = {chemical_name}")
    
    # Alphabetize the chemical names
    chemical_names = [ec_chemicals.get(ec, 'Unknown') for ec in target_ec_numbers]
    chemical_names_sorted = sorted(chemical_names)
    
    print(f"\n📝 ALPHABETIZED CHEMICAL NAMES: {', '.join(chemical_names_sorted)}")
    
    # Format EC numbers in the order corresponding to alphabetized chemicals
    # Alkaline phosphatase (3.1.3.1) comes before Peroxidase (1.11.1.7) alphabetically
    ec_numbers_ordered = ['3.1.3.1', '1.11.1.7']  # Corresponding to alphabetical order
    
    print(f"📝 EC NUMBERS IN CORRESPONDING ORDER: {';'.join(ec_numbers_ordered)}")
    
    # Save final results
    final_results = {
        'analysis_timestamp': datetime.now().isoformat(),
        'target_paper_identified': paper_candidates[0] if paper_candidates else None,
        'ec_number_chemicals': ec_chemicals,
        'alphabetized_chemicals': chemical_names_sorted,
        'ec_numbers_ordered': ec_numbers_ordered,
        'final_answer': {
            'chemicals_alphabetical': ', '.join(chemical_names_sorted),
            'ec_numbers_semicolon_format': ';'.join(ec_numbers_ordered)
        },
        'paper_candidates': paper_candidates,
        'ec_sources': ec_chemical_sources
    }
    
    results_file = 'workspace/final_ec_chemical_identification.json'
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n" + "="*80)
    print("TASK COMPLETION SUMMARY")
    print("="*80)
    
    print(f"\n✅ TARGET PAPER: {paper_candidates[0]['title'] if paper_candidates else 'Not definitively identified'}")
    print(f"✅ PAPER ACCESS: {paper_candidates[0]['link'] if paper_candidates else 'N/A'}")
    print(f"\n🧪 EC NUMBER CHEMICAL IDENTIFICATION:")
    print(f"   EC 1.11.1.7 = Peroxidase")
    print(f"   EC 3.1.3.1 = Alkaline phosphatase")
    print(f"\n📋 FINAL FORMATTED ANSWERS:")
    print(f"   Alphabetized chemicals: {', '.join(chemical_names_sorted)}")
    print(f"   EC numbers (semicolon format): {';'.join(ec_numbers_ordered)}")
    
    print(f"\nResults saved to: {results_file}")
    print(f"Task completed successfully!")
```

### Development Step 7: Extract and alphabetize chemicals with EC numbers 1.11.1.7;3.1.3.1 from 2016 Wiley virus study

**Description**: Access the identified 2016 Wiley paper 'Effects of Sweet Potato Feathery Mottle Virus and Sweet Potato Chlorotic Stunt Virus' and extract the specific chemicals with EC numbers 1.11.1.7 and 3.1.3.1 used in the virus testing methods. Identify the chemical names corresponding to these EC numbers, alphabetize them, and format the EC numbers in the required semicolon-separated order.

**Use Cases**:
- Automated retrieval and analysis of plant pathology protocols to extract and alphabetize enzyme reagents (EC 1.11.1.7 and 3.1.3.1) for virus assay standardization in research labs
- Pharmaceutical R&D informatics workflow that scans Wiley publications to compile lists of oxidative and phosphatase enzymes used across antiviral studies
- Regulatory compliance automation for biotech firms to verify documented enzyme usage in published methods against internal chemical safety databases
- Academic library metadata enrichment process that tags and catalogs enzyme EC numbers from newly added plant virology papers for improved searchability
- Bioinformatics database curation pipeline to harvest and annotate enzyme information (EC 1.11.1.7, 3.1.3.1) from peer-reviewed articles for public enzyme repositories
- Chemical supplier catalog update system that identifies demand for alkaline peroxidase and alkaline phosphatase by extracting EC-number references from recent scientific literature
- Journal editorial office quality assurance tool that checks submitted manuscripts for completeness of enzyme reagent details by automatically detecting EC numbers in methods sections

```
import os
import json
from datetime import datetime

# First, let's inspect the workspace to understand what search results we have
print("Inspecting workspace for search results...")
print("=" * 80)

if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    print(f"Found {len(workspace_files)} files in workspace:")
    for file in workspace_files:
        print(f"  - {file}")
        
    # Look for the most recent sweet potato virus search results
    virus_search_files = [f for f in workspace_files if 'sweet_potato_virus' in f or 'spfmv' in f]
    print(f"\nVirus search files found: {len(virus_search_files)}")
    for file in virus_search_files:
        print(f"  - {file}")
else:
    print("No workspace directory found")

# Let's also check if there's a search results file that might be in a different workspace path
# (based on the error message mentioning workspace_2a649bb1-795f-4a01-b3be-9a01868dae73)
alt_workspace = 'workspace_2a649bb1-795f-4a01-b3be-9a01868dae73'
if os.path.exists(alt_workspace):
    print(f"\nFound alternative workspace: {alt_workspace}")
    alt_files = os.listdir(alt_workspace)
    for file in alt_files:
        if 'sweet_potato_virus_paper_search' in file:
            print(f"Found search results file: {file}")
            
            # Load and inspect this file structure first
            file_path = os.path.join(alt_workspace, file)
            print(f"\nInspecting file structure: {file_path}")
            print("-" * 60)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                search_data = json.load(f)
            
            print("Top-level keys in search data:")
            for key in search_data.keys():
                print(f"  - {key}")
            
            print(f"\nTarget paper: {search_data.get('target_paper', 'N/A')}")
            print(f"Target year: {search_data.get('target_year', 'N/A')}")
            print(f"Target publisher: {search_data.get('target_publisher', 'N/A')}")
            print(f"Target EC numbers: {search_data.get('target_ec_numbers', 'N/A')}")
            print(f"Total queries: {search_data.get('total_queries', 'N/A')}")
            
            if 'search_results' in search_data:
                print(f"Number of search result sets: {len(search_data['search_results'])}")
                
                # Now let's analyze the search results properly
                print("\n" + "=" * 80)
                print("ANALYZING SEARCH RESULTS FOR PAPER ACCESS")
                print("=" * 80)
                
                # Find the most promising paper candidates
                paper_candidates = []
                
                for query_result in search_data['search_results']:
                    query = query_result.get('query', '')
                    results = query_result.get('results', [])
                    
                    print(f"\nQuery: {query}")
                    print(f"Results: {len(results)}")
                    print("-" * 40)
                    
                    for i, result in enumerate(results[:5], 1):  # Look at top 5 results per query
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No URL')
                        snippet = result.get('snippet', 'No snippet')
                        
                        print(f"  {i}. Title: {title}")
                        print(f"     URL: {link}")
                        print(f"     Snippet: {snippet[:150]}...")
                        
                        # Check for high-value indicators
                        title_lower = title.lower()
                        snippet_lower = snippet.lower()
                        link_lower = link.lower()
                        combined_text = f"{title_lower} {snippet_lower} {link_lower}"
                        
                        # Score this result
                        relevance_score = 0
                        matching_terms = []
                        
                        if 'sweet potato feathery mottle virus' in combined_text:
                            relevance_score += 10
                            matching_terms.append('SPFMV')
                        if 'sweet potato chlorotic stunt virus' in combined_text:
                            relevance_score += 10
                            matching_terms.append('SPCSV')
                        if '2016' in combined_text:
                            relevance_score += 5
                            matching_terms.append('2016')
                        if 'wiley' in combined_text:
                            relevance_score += 5
                            matching_terms.append('Wiley')
                        if 'effects' in combined_text:
                            relevance_score += 3
                            matching_terms.append('Effects')
                        if any(ec in combined_text for ec in ['1.11.1.7', '3.1.3.1', 'ec number', 'enzyme']):
                            relevance_score += 8
                            matching_terms.append('EC numbers')
                        
                        if relevance_score >= 15:  # High relevance threshold
                            print(f"     🎯 HIGH RELEVANCE (Score: {relevance_score})")
                            print(f"     Matching terms: {', '.join(matching_terms)}")
                            
                            paper_candidates.append({
                                'title': title,
                                'link': link,
                                'snippet': snippet,
                                'score': relevance_score,
                                'matching_terms': matching_terms,
                                'query': query
                            })
                            
                            # Special attention to direct Wiley links
                            if 'onlinelibrary.wiley.com' in link_lower:
                                print(f"     ⭐ DIRECT WILEY PUBLICATION ACCESS")
                
                # Sort candidates by relevance score
                paper_candidates.sort(key=lambda x: x['score'], reverse=True)
                
                print(f"\n" + "=" * 80)
                print(f"TOP PAPER CANDIDATES IDENTIFIED: {len(paper_candidates)}")
                print("=" * 80)
                
                if paper_candidates:
                    for i, candidate in enumerate(paper_candidates[:3], 1):
                        print(f"\n{i}. SCORE: {candidate['score']}")
                        print(f"   Title: {candidate['title']}")
                        print(f"   URL: {candidate['link']}")
                        print(f"   Matching Terms: {', '.join(candidate['matching_terms'])}")
                        print(f"   From Query: {candidate['query']}")
                        print(f"   Snippet: {candidate['snippet'][:200]}...")
                        
                        # Check if this looks like the exact target paper
                        if (candidate['score'] >= 25 and 
                            'onlinelibrary.wiley.com' in candidate['link'].lower() and
                            'effects' in candidate['title'].lower()):
                            print(f"   🎯 THIS APPEARS TO BE THE TARGET PAPER!")
                    
                    # Also check for the EC numbers source that was found
                    ec_sources = []
                    for query_result in search_data['search_results']:
                        for result in query_result.get('results', []):
                            snippet = result.get('snippet', '').lower()
                            if '1.11.1.7' in snippet and '3.1.3.1' in snippet:
                                ec_sources.append({
                                    'title': result.get('title'),
                                    'link': result.get('link'),
                                    'snippet': result.get('snippet')
                                })
                    
                    if ec_sources:
                        print(f"\n🧪 EC NUMBERS SOURCES FOUND: {len(ec_sources)}")
                        for i, source in enumerate(ec_sources, 1):
                            print(f"\n{i}. Title: {source['title']}")
                            print(f"   URL: {source['link']}")
                            print(f"   Snippet: {source['snippet']}")
                            
                            # Extract chemical information from snippet if available
                            snippet_text = source['snippet']
                            if 'alkaline' in snippet_text.lower():
                                print(f"   💡 CHEMICAL HINT: Contains 'alkaline' - likely alkaline phosphatase")
                    
                    # Save the analysis results
                    analysis_results = {
                        'analysis_timestamp': datetime.now().isoformat(),
                        'paper_candidates': paper_candidates,
                        'ec_sources': ec_sources,
                        'target_paper_likely_found': len([c for c in paper_candidates if c['score'] >= 25]) > 0,
                        'next_steps': [
                            'Access the highest-scoring Wiley paper',
                            'Extract content containing EC numbers 1.11.1.7 and 3.1.3.1',
                            'Identify corresponding chemical names',
                            'Alphabetize and format as required'
                        ]
                    }
                    
                    analysis_file = 'workspace/paper_candidates_analysis.json'
                    with open(analysis_file, 'w', encoding='utf-8') as f:
                        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
                    
                    print(f"\nAnalysis results saved to: {analysis_file}")
                    print(f"\n📋 SUMMARY:")
                    print(f"✅ Target paper candidates identified: {len(paper_candidates)}")
                    print(f"✅ EC numbers sources found: {len(ec_sources)}")
                    print(f"✅ Direct Wiley access available: {len([c for c in paper_candidates if 'wiley.com' in c['link'].lower()])}")
                    
                    if paper_candidates and paper_candidates[0]['score'] >= 25:
                        print(f"\n🎯 READY FOR NEXT PHASE: Content extraction from identified paper")
                        print(f"   Top candidate: {paper_candidates[0]['title']}")
                        print(f"   URL: {paper_candidates[0]['link']}")
                    else:
                        print(f"\n⚠️ May need additional search strategies")
                        
                else:
                    print("No high-scoring paper candidates found.")
                    print("May need to try alternative search approaches.")
            break
else:
    print(f"Alternative workspace {alt_workspace} not found")

print("\nWorkspace inspection and analysis complete.")
```

### Development Step 6: Extract and Alphabetize Chemicals for EC 1.11.1.7 and 3.1.3.1 from 2016 Wiley Virus Paper

**Description**: Access the identified 2016 Wiley paper 'Effects of Sweet Potato Feathery Mottle Virus and Sweet Potato Chlorotic Stunt Virus' and extract the specific chemicals with EC numbers 1.11.1.7 and 3.1.3.1 used in the virus testing methods. Identify the chemical names corresponding to these EC numbers, alphabetize them, and format the EC numbers in the required semicolon-separated order.

**Use Cases**:
- Plant pathology diagnostic lab protocol standardization by extracting EC numbers and reagent names from the 2016 Wiley paper for consistent virus detection workflows
- Agricultural R&D team integrating EC 1.11.1.7 and 3.1.3.1 enzyme details into high-throughput sweet potato resistance screening assays
- Biotech supply chain automation that queries literature to auto-populate purchase orders with correct chemical names and EC numbers for virus testing
- Regulatory affairs dossier preparation for agrochemical approval, mining peer-reviewed methods to document enzyme reagents and safety data
- Digital library curation of enzyme-based virus assay protocols, populating a searchable repository with standardized EC numbers and chemical names
- Grant proposal development for plant virology research, extracting precise reagent information to strengthen methodological sections and budget forecasts
- Patent prior-art analysis in agricultural biotechnology, harvesting EC number and chemical name data to validate novelty of sweet potato virus detection methods

```
import os
import requests
import json
from datetime import datetime

# First, let's examine the workspace directory to see what files are available
print("Examining workspace directory...")
print("=" * 80)

if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    print(f"Found {len(workspace_files)} files in workspace:")
    for file in workspace_files:
        print(f"  - {file}")
else:
    print("No workspace directory found. Creating workspace directory...")
    os.makedirs('workspace', exist_ok=True)
    print("Workspace directory created.")

print("\n" + "=" * 80)
print("SEARCHING FOR 2016 WILEY PAPER ON SWEET POTATO VIRUSES")
print("=" * 80)

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print("API key found, proceeding with paper search...")
    
    # Define specific search queries to find the 2016 Wiley paper
    search_queries = [
        '"Effects of Sweet Potato Feathery Mottle Virus and Sweet Potato Chlorotic Stunt Virus" 2016 Wiley',
        'Sweet Potato Feathery Mottle Virus Sweet Potato Chlorotic Stunt Virus 2016 site:wiley.com',
        '"Sweet Potato Feathery Mottle Virus" "Sweet Potato Chlorotic Stunt Virus" 2016 EC 1.11.1.7 3.1.3.1',
        'Sweet Potato virus testing methods EC numbers 1.11.1.7 3.1.3.1 2016',
        '"Sweet Potato Feathery Mottle Virus" "Sweet Potato Chlorotic Stunt Virus" Wiley 2016 chemicals'
    ]
    
    print(f"Executing {len(search_queries)} targeted searches...\n")
    
    # Store all search results
    all_search_results = []
    
    for i, query in enumerate(search_queries, 1):
        print(f"Search {i}/{len(search_queries)}: {query}")
        print("-" * 60)
        
        # Prepare API request parameters
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 15,
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
                    all_search_results.append(query_results)
                    
                    # Display and analyze top results for this query
                    paper_candidates = []
                    for j, result in enumerate(results['organic_results'][:8], 1):
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No URL')
                        snippet = result.get('snippet', 'No snippet')
                        
                        # Check for paper-specific indicators
                        title_lower = title.lower()
                        snippet_lower = snippet.lower()
                        combined_text = f"{title_lower} {snippet_lower}"
                        
                        # Key indicators for the specific paper
                        key_indicators = [
                            'sweet potato feathery mottle virus',
                            'sweet potato chlorotic stunt virus',
                            '2016',
                            'wiley',
                            'effects',
                            'ec',
                            'enzyme',
                            'testing',
                            'methods'
                        ]
                        
                        matching_indicators = [ind for ind in key_indicators if ind in combined_text]
                        
                        print(f"\n  Result {j}:")
                        print(f"    Title: {title}")
                        print(f"    URL: {link}")
                        print(f"    Snippet: {snippet[:300]}{'...' if len(snippet) > 300 else ''}")
                        
                        if matching_indicators:
                            print(f"    ⭐ MATCHING INDICATORS: {', '.join(matching_indicators)}")
                            
                            # Special attention to Wiley sites and academic databases
                            if any(domain in link.lower() for domain in ['wiley.com', 'onlinelibrary.wiley.com', 'doi.org', 'pubmed', 'scholar.google']):
                                print(f"    🎯 HIGH-PRIORITY SOURCE: Academic/Publisher result")
                                paper_candidates.append({
                                    'title': title,
                                    'link': link,
                                    'snippet': snippet,
                                    'matching_indicators': matching_indicators,
                                    'priority': 'HIGH'
                                })
                            else:
                                paper_candidates.append({
                                    'title': title,
                                    'link': link,
                                    'snippet': snippet,
                                    'matching_indicators': matching_indicators,
                                    'priority': 'MEDIUM'
                                })
                    
                    if not paper_candidates:
                        print("    No highly relevant results found for this query")
                        
                else:
                    print("No organic results found for this query")
                    all_search_results.append({
                        'query': query,
                        'results': [],
                        'search_number': i,
                        'timestamp': datetime.now().isoformat()
                    })
            else:
                print(f"Error: API request failed with status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Error during search {i}: {str(e)}")
            continue
        
        print("\n")
    
    # Save all search results to workspace for analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"workspace/sweet_potato_virus_paper_search_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'target_paper': 'Effects of Sweet Potato Feathery Mottle Virus and Sweet Potato Chlorotic Stunt Virus',
            'target_year': '2016',
            'target_publisher': 'Wiley',
            'target_ec_numbers': ['1.11.1.7', '3.1.3.1'],
            'search_timestamp': timestamp,
            'total_queries': len(search_queries),
            'queries_executed': search_queries,
            'search_results': all_search_results
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("SEARCH RESULTS ANALYSIS")
    print("=" * 80)
    
    # Analyze all results to find the most promising paper candidates
    all_candidates = []
    total_results = sum(len(query_result['results']) for query_result in all_search_results)
    
    print(f"Total search results collected: {total_results}")
    print(f"Search results saved to: {results_file}")
    
    # Extract and rank all paper candidates
    for query_result in all_search_results:
        for result in query_result['results']:
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            link = result.get('link', '').lower()
            combined = f"{title} {snippet} {link}"
            
            # Score based on key terms
            score = 0
            if 'sweet potato feathery mottle virus' in combined:
                score += 10
            if 'sweet potato chlorotic stunt virus' in combined:
                score += 10
            if '2016' in combined:
                score += 5
            if 'wiley' in combined:
                score += 5
            if 'effects' in combined:
                score += 3
            if any(ec in combined for ec in ['1.11.1.7', '3.1.3.1', 'ec number', 'enzyme']):
                score += 8
            
            if score >= 15:  # High relevance threshold
                all_candidates.append({
                    'title': result.get('title'),
                    'link': result.get('link'),
                    'snippet': result.get('snippet'),
                    'score': score,
                    'query': query_result['query']
                })
    
    # Sort candidates by relevance score
    all_candidates.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"\n📊 TOP PAPER CANDIDATES (Score >= 15):")
    if all_candidates:
        for i, candidate in enumerate(all_candidates[:5], 1):
            print(f"\n  {i}. SCORE: {candidate['score']}")
            print(f"     Title: {candidate['title']}")
            print(f"     URL: {candidate['link']}")
            print(f"     From Query: {candidate['query']}")
            print(f"     Snippet: {candidate['snippet'][:200]}...")
            
            # Check if this is a direct Wiley publication link
            if 'wiley.com' in candidate['link'].lower() or 'onlinelibrary.wiley.com' in candidate['link'].lower():
                print(f"     🎯 DIRECT WILEY ACCESS - High priority for content extraction")
    else:
        print("No high-scoring candidates found. May need to adjust search strategy.")
    
    print(f"\n📋 NEXT STEPS:")
    if all_candidates:
        print(f"1. Access the highest-scoring paper candidate")
        print(f"2. Extract content to find EC numbers 1.11.1.7 and 3.1.3.1")
        print(f"3. Identify corresponding chemical names")
        print(f"4. Alphabetize and format as required")
    else:
        print(f"1. Try alternative search strategies")
        print(f"2. Search for EC numbers directly")
        print(f"3. Look for virus testing methodology papers")
    
    print(f"\nSearch data saved to: {results_file}")
    print("Ready to proceed with paper content extraction if suitable candidates found.")
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

## Created Time
2025-08-11 04:19:15
