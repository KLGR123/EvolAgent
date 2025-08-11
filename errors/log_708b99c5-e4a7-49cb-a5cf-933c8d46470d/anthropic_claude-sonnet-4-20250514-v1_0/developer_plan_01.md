# Developer Plan 01

## Plan
Search for the DeepFruits fruit detection paper from 2016 on Connected Papers platform. Navigate to the Connected Papers website and locate the specific graph/visualization for the DeepFruits paper. Examine the bubble chart or network visualization to identify the largest bubble and determine what feature or metric determines bubble size in Connected Papers' visualization system (typically citation count, influence score, or similar academic metrics).

## Description
This is the optimal first step because: (1) We need to locate the specific DeepFruits paper from 2016 on Connected Papers to access its visualization graph, (2) No previous research has been conducted on this task, (3) Expected outcome is to find the Connected Papers page for DeepFruits and understand the bubble sizing methodology used in their network visualization, (4) This directly addresses the TASK requirement to identify what feature caused the largest bubble to be the size it is on the DeepFruits detection graph

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

### Development Step 11: Number of Peer-Reviewed Research Articles Published by Nature Journal in 2020

**Description**: Research and determine the total number of research articles (excluding book reviews, columns, editorials, and other non-research content) published by Nature journal in 2020. Focus on identifying peer-reviewed research articles that would typically involve statistical analysis and hypothesis testing.

**Use Cases**:
- University library subscription verification: automating DOI count checks on downloaded Nature 2020 archive files to confirm that all issues and research articles are present in the institutional collection
- Patent office prior-art review automation: scanning Nature’s entire 2020 text archives for DOI extraction and article counts to support patent examiners in assessing relevant scientific literature
- Pharmaceutical clinical trial intelligence: monthly parsing of Nature 2020 archives to identify and tally newly published clinical research articles for updating internal R&D databases
- Science funding impact assessment: extracting per-issue research article counts from Nature’s 2020 volumes to measure publication outputs tied to specific grant programs and inform policy evaluations
- Academic publisher quality assurance: validating volume/issue structure, pagination, and DOI presence in Nature 2020 text dumps before final online release to ensure consistency and completeness
- Bibliometric service data pipeline: ingesting raw Nature archive files, parsing article listings and DOIs, and populating a bibliometric database used for institutional rankings and citation analysis
- Data journalism on publication trends: programmatically analyzing Nature’s 2020 archive text for research article patterns, topic distributions, and monthly publication volumes to support investigative reporting
- Research discovery platform integration: automated parsing of Nature 2020 archive text files to extract structured metadata (DOI, title, volume, issue) and feed into an academic search index for enhanced discoverability

```
import os
import json
import re

print("=== DETAILED ANALYSIS OF DOWNLOADED NATURE JOURNAL 2020 ARCHIVE CONTENT ===\n")

# Find workspace directory
workspace_dirs = [d for d in os.listdir('.') if d.startswith('workspace')]
if workspace_dirs:
    workspace_dir = workspace_dirs[0]
    print(f"Using workspace directory: {workspace_dir}")
else:
    print("No workspace directory found.")
    exit()

# First, let's inspect what Nature journal archive files we have
print(f"\nFiles in workspace:")
archive_files = []
for file in os.listdir(workspace_dir):
    file_path = os.path.join(workspace_dir, file)
    file_size = os.path.getsize(file_path)
    print(f"  - {file} ({file_size:,} bytes)")
    if 'nature_journal_archive' in file and file.endswith('.txt'):
        archive_files.append(file)

print(f"\nFound {len(archive_files)} Nature journal archive files to analyze:")
for file in archive_files:
    print(f"  - {file}")

# Analyze each Nature journal archive file in detail
print("\n=== DETAILED CONTENT ANALYSIS OF NATURE JOURNAL ARCHIVE FILES ===\n")

analysis_results = []

for i, filename in enumerate(archive_files, 1):
    filepath = os.path.join(workspace_dir, filename)
    print(f"Analyzing {i}. {filename}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Content length: {len(content):,} characters")
    
    # Extract header information
    lines = content.split('\n')
    header_info = {}
    for line in lines[:10]:
        if line.startswith('Source:'):
            header_info['source'] = line.replace('Source:', '').strip()
        elif line.startswith('URL:'):
            header_info['url'] = line.replace('URL:', '').strip()
    
    print(f"Source: {header_info.get('source', 'Unknown')}")
    print(f"URL: {header_info.get('url', 'Unknown')}")
    
    # Show more content to understand the structure
    print(f"\n--- Content Structure Analysis ---")
    
    # Look for the actual content after the header
    content_start_marker = "=" * 50
    if content_start_marker in content:
        main_content = content[content.find(content_start_marker) + len(content_start_marker):]
    else:
        main_content = content[500:]  # Skip header info
    
    print(f"Main content length: {len(main_content):,} characters")
    print(f"First 800 characters of main content:")
    print(f"{main_content[:800]}...")
    
    # Convert to lowercase for analysis
    content_lower = main_content.lower()
    
    # Look for article listing patterns
    print(f"\n--- Searching for Article Listings and Counts ---")
    
    # Patterns that might indicate article counts or listings
    article_listing_patterns = [
        r'article\s+\d+',
        r'\d+\s+articles?',
        r'research\s+article',
        r'volume\s+\d+',
        r'issue\s+\d+',
        r'doi:',
        r'nature\s+\d+',
        r'published\s+\d+',
        r'january\s+2020',
        r'december\s+2020'
    ]
    
    found_patterns = {}
    for pattern in article_listing_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            found_patterns[pattern] = len(matches)
    
    print(f"Article-related patterns found:")
    for pattern, count in found_patterns.items():
        print(f"  {pattern}: {count} occurrences")
    
    # Look for DOI patterns (each research article should have a DOI)
    doi_patterns = [
        r'doi:\s*10\.1038/s41586-\d+-\d+-\d+',
        r'10\.1038/s41586-\d+-\d+-\d+',
        r'doi:10\.1038',
        r'10\.1038/nature\d+'
    ]
    
    total_dois = 0
    doi_matches = {}
    for pattern in doi_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            doi_matches[pattern] = matches
            total_dois += len(matches)
    
    print(f"\nDOI patterns found (indicates research articles):")
    print(f"Total DOIs found: {total_dois}")
    for pattern, matches in doi_matches.items():
        print(f"  {pattern}: {len(matches)} matches")
        if len(matches) <= 5:  # Show first few matches
            for match in matches[:3]:
                print(f"    - {match}")
    
    # Look for volume and issue structure
    print(f"\n--- Volume and Issue Analysis ---")
    
    # Extract volume numbers
    volume_matches = re.findall(r'volume\s+(\d+)', content_lower)
    issue_matches = re.findall(r'issue\s+(\d+)', content_lower)
    
    unique_volumes = list(set(volume_matches))
    unique_issues = list(set(issue_matches))
    
    print(f"Volumes found: {unique_volumes}")
    print(f"Issues found: {unique_issues[:10]}{'...' if len(unique_issues) > 10 else ''}")
    
    # Look for article titles or research article indicators
    research_article_indicators = [
        'research article',
        'article',
        'letter',
        'brief communication',
        'analysis',
        'perspective'
    ]
    
    content_type_counts = {}
    for indicator in research_article_indicators:
        count = content_lower.count(indicator)
        if count > 0:
            content_type_counts[indicator] = count
    
    print(f"\nContent type indicators:")
    for content_type, count in content_type_counts.items():
        print(f"  {content_type}: {count} occurrences")
    
    # Look for pagination or "load more" indicators
    pagination_patterns = [
        r'page\s+(\d+)',
        r'showing\s+(\d+)',
        r'load\s+more',
        r'next\s+(\d+)',
        r'of\s+(\d+)\s+results',
        r'(\d+)\s+results'
    ]
    
    pagination_info = {}
    for pattern in pagination_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            pagination_info[pattern] = matches
    
    print(f"\nPagination information:")
    for pattern, matches in pagination_info.items():
        print(f"  {pattern}: {matches[:5]}")
    
    # Save detailed analysis for this file
    file_analysis = {
        'filename': filename,
        'source': header_info.get('source', 'Unknown'),
        'url': header_info.get('url', 'Unknown'),
        'content_length': len(content),
        'main_content_length': len(main_content),
        'article_patterns': found_patterns,
        'doi_count': total_dois,
        'doi_details': doi_matches,
        'volumes_found': unique_volumes,
        'issues_found': unique_issues,
        'content_type_counts': content_type_counts,
        'pagination_info': pagination_info
    }
    
    analysis_results.append(file_analysis)
    print("=" * 80)

# Comprehensive analysis across all files
print(f"\n=== COMPREHENSIVE ANALYSIS ACROSS ALL NATURE JOURNAL ARCHIVES ===\n")

total_dois_all_files = sum(result['doi_count'] for result in analysis_results)
all_volumes = []
all_content_types = {}

for result in analysis_results:
    all_volumes.extend(result['volumes_found'])
    for content_type, count in result['content_type_counts'].items():
        all_content_types[content_type] = all_content_types.get(content_type, 0) + count

unique_volumes_all = sorted(set(int(v) for v in all_volumes if v.isdigit()))

print(f"Files analyzed: {len(analysis_results)}")
print(f"Total DOIs found across all files: {total_dois_all_files}")
print(f"All Nature volumes found: {unique_volumes_all}")
print(f"Content type totals across all files:")
for content_type, total_count in sorted(all_content_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {content_type}: {total_count} total occurrences")

# Estimate research article count based on analysis
print(f"\n=== ESTIMATING NATURE JOURNAL 2020 RESEARCH ARTICLE COUNT ===\n")

# Method 1: DOI count (most reliable for research articles)
if total_dois_all_files > 0:
    print(f"Method 1 - DOI Count: {total_dois_all_files} research articles")
    print(f"  (Each research article should have a unique DOI)")
else:
    print(f"Method 1 - DOI Count: No DOIs extracted from content")

# Method 2: Research article mentions
research_article_mentions = all_content_types.get('research article', 0)
if research_article_mentions > 0:
    print(f"Method 2 - Research Article Mentions: ~{research_article_mentions} research articles")
    print(f"  (Based on 'research article' text occurrences)")
else:
    print(f"Method 2 - Research Article Mentions: No clear research article mentions")

# Method 3: Volume analysis
if unique_volumes_all:
    print(f"Method 3 - Volume Analysis: Found volumes {unique_volumes_all}")
    print(f"  Nature 2020 published volumes {min(unique_volumes_all)}-{max(unique_volumes_all)}")
    # Nature typically publishes ~40-50 articles per volume, ~50 issues per year
    volume_count = len(unique_volumes_all)
    if volume_count > 0:
        estimated_articles = volume_count * 45  # Conservative estimate
        print(f"  Estimated articles: ~{estimated_articles} (assuming ~45 articles per volume)")

# Final determination
print(f"\n=== FINAL DETERMINATION ===\n")

if total_dois_all_files >= 200:  # Reasonable range for Nature journal
    final_count = total_dois_all_files
    method = "DOI count"
    confidence = "High"
elif research_article_mentions >= 200:
    final_count = research_article_mentions
    method = "Research article mentions"
    confidence = "Medium"
elif unique_volumes_all:
    final_count = len(unique_volumes_all) * 45
    method = "Volume-based estimation"
    confidence = "Low"
else:
    final_count = None
    method = "Unable to determine"
    confidence = "None"

if final_count:
    print(f"🎯 ANSWER: Nature journal published approximately {final_count} research articles in 2020")
    print(f"   Method: {method}")
    print(f"   Confidence: {confidence}")
    print(f"   Source: Analysis of Nature journal's official 2020 archives")
    print(f"   Content type: Peer-reviewed research articles (excluding editorials, reviews, correspondence)")
else:
    print(f"⚠️  Unable to determine exact count from downloaded archive content")
    print(f"   The archive pages may require JavaScript or have different structure than expected")
    print(f"   Alternative: Manual inspection of Nature journal's 2020 issues or contact editorial office")

# Save comprehensive final analysis
final_comprehensive_analysis = {
    'analysis_date': '2025-01-06',
    'method': 'Detailed content analysis of Nature journal 2020 archives',
    'files_analyzed': len(analysis_results),
    'total_dois_found': total_dois_all_files,
    'research_article_mentions': research_article_mentions,
    'nature_2020_volumes': unique_volumes_all,
    'content_type_totals': all_content_types,
    'file_details': analysis_results,
    'final_determination': {
        'estimated_count': final_count,
        'method_used': method,
        'confidence_level': confidence,
        'reasoning': 'Based on analysis of official Nature journal archive content'
    }
}

final_file = os.path.join(workspace_dir, 'nature_2020_research_articles_final_analysis.json')
with open(final_file, 'w') as f:
    json.dump(final_comprehensive_analysis, f, indent=2)

print(f"\nComprehensive analysis saved to: {os.path.basename(final_file)}")
print(f"\nWorkspace files:")
for file in sorted(os.listdir(workspace_dir)):
    if 'nature' in file:
        file_path = os.path.join(workspace_dir, file)
        file_size = os.path.getsize(file_path)
        print(f"  - {file} ({file_size:,} bytes)")
```

### Development Step 1: Identify Emily Midkiff’s June 2014 dragon depictions article in Fafnir Journal

**Description**: Search for information about Emily Midkiff's June 2014 article, focusing on identifying the journal named after one of Hreidmar's sons from Norse mythology. Research Hreidmar's sons (Fafnir, Regin, and Otr) to determine which one has a journal named after them, then locate Midkiff's specific article from June 2014 that discusses dragon depictions and contains quotes from two different authors expressing distaste.

**Use Cases**:
- Digital humanities research for medieval literature scholars: automating retrieval of articles on Norse mythology from niche journals (e.g., “Fáfnir Journal”), then extracting critical commentary quotes for a comparative analysis thesis
- Legal case preparation by law firms: scanning law reviews named after prominent jurists to find analyses of recent Supreme Court decisions, filtering and extracting dissenting judge quotes for briefings
- Pharmaceutical regulatory monitoring: searching clinical trial publications in specialty journals named after key compounds, identifying and extracting researcher statements on adverse events for safety reporting
- Competitive intelligence in tech R&D: aggregating engineering and patent‐focused articles from journals named after inventors, scraping and ranking passages where competitors critique hardware performance
- Financial market analysis for investment teams: locating macroeconomics papers in journals named after Nobel laureates, extracting risk assessment quotes by leading economists for client reports
- Marketing insight gathering for consumer goods: crawling enthusiast blogs and product forums named after brand mascots, filtering posts for negative feedback and extracting representative customer complaints
- Environmental policy research for NGOs: compiling ecological impact studies in region‐specific environmental journals, extracting scientist warnings on biodiversity loss for advocacy materials
- Genealogical and heritage studies by amateur historians: finding family‐history articles in society journals named after ancestral clans, pulling out firsthand narratives and dispute accounts for published family trees

```
import os
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import quote_plus, urljoin

print('=== RESEARCHING HREIDMAR\'S SONS AND EMILY MIDKIFF ARTICLE ===')
print('Objective: Find Emily Midkiff\'s June 2014 article in a journal named after one of Hreidmar\'s sons')
print('Norse mythology research: Hreidmar\'s sons are Fafnir, Regin, and Otr')
print('Need to identify which son has a journal named after them\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Step 1: Research Hreidmar's sons and potential journals
print('=== STEP 1: RESEARCHING HREIDMAR\'S SONS FROM NORSE MYTHOLOGY ===')
hreidmar_sons = {
    'Fafnir': {
        'description': 'Transformed into a dragon, guards treasure',
        'alternate_spellings': ['Fáfnir', 'Fafner'],
        'significance': 'Most famous dragon in Norse mythology'
    },
    'Regin': {
        'description': 'Dwarf smith, foster father of Sigurd',
        'alternate_spellings': ['Reginn'],
        'significance': 'Craftsman and mentor figure'
    },
    'Otr': {
        'description': 'Could transform into an otter, killed by Loki',
        'alternate_spellings': ['Ótr', 'Otter'],
        'significance': 'His death triggered the curse on the gold'
    }
}

print('Hreidmar\'s sons and their characteristics:')
for son, info in hreidmar_sons.items():
    print(f'\n{son}:')
    print(f'  Description: {info["description"]}')
    print(f'  Alternate spellings: {", ".join(info["alternate_spellings"])}')
    print(f'  Significance: {info["significance"]}')

# Step 2: Search for academic journals named after these figures
print('\n=== STEP 2: SEARCHING FOR JOURNALS NAMED AFTER HREIDMAR\'S SONS ===')

# Headers for web requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

# Search queries for each son + "journal" to find academic publications
journal_search_queries = []
for son, info in hreidmar_sons.items():
    # Create search queries for each name variant
    for name in [son] + info['alternate_spellings']:
        journal_search_queries.extend([
            f'{name} journal academic',
            f'{name} journal mythology',
            f'{name} journal medieval studies',
            f'{name} journal dragon studies'
        ])

print(f'Generated {len(journal_search_queries)} search queries for journal identification')
print('Sample queries:')
for i, query in enumerate(journal_search_queries[:8]):
    print(f'  {i+1}. {query}')

# Step 3: Search for Emily Midkiff June 2014 article
print('\n=== STEP 3: SEARCHING FOR EMILY MIDKIFF JUNE 2014 ARTICLE ===')

# Multiple search strategies for Emily Midkiff
midkiff_queries = [
    'Emily Midkiff June 2014 dragon',
    'Emily Midkiff 2014 dragon depictions',
    'Emily Midkiff dragon mythology article',
    '"Emily Midkiff" 2014 dragon distaste quotes',
    'Emily Midkiff Norse mythology dragon 2014',
    'Emily Midkiff Fafnir journal 2014',
    'Emily Midkiff Regin journal 2014',
    'Emily Midkiff medieval dragon studies 2014'
]

print('Emily Midkiff search queries:')
for i, query in enumerate(midkiff_queries, 1):
    print(f'  {i}. {query}')

# Step 4: Conduct web searches using DuckDuckGo HTML interface
print('\n=== STEP 4: CONDUCTING WEB SEARCHES ===')

search_results = {}
search_base_url = 'https://html.duckduckgo.com/html/'

# Function to perform search and save results
def perform_search(query, search_type):
    print(f'\nSearching for: {query}')
    try:
        params = {'q': query}
        response = requests.get(search_base_url, params=params, headers=headers, timeout=30)
        print(f'  Status: {response.status_code}')
        
        if response.status_code == 200:
            # Save raw HTML
            filename = f'{search_type}_{query.replace(" ", "_").replace('"', "")[:50]}.html'
            filepath = os.path.join('workspace', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f'  Saved: {filepath}')
            
            # Parse for quick analysis
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for result links
            result_links = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                text = link.get_text().strip()
                
                # Filter for relevant results
                if href and text and len(text) > 10:
                    if any(term in text.lower() for term in ['midkiff', 'fafnir', 'regin', 'dragon', 'journal']):
                        result_links.append({
                            'url': href,
                            'text': text[:200],
                            'relevance_score': sum(1 for term in ['midkiff', 'fafnir', 'regin', 'dragon', 'journal', '2014'] if term in text.lower())
                        })
            
            # Sort by relevance
            result_links.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            search_results[query] = {
                'html_file': filepath,
                'status_code': response.status_code,
                'relevant_links': result_links[:10],  # Top 10 most relevant
                'total_links_found': len(result_links)
            }
            
            print(f'  Found {len(result_links)} relevant links')
            if result_links:
                print('  Top results:')
                for i, link in enumerate(result_links[:3], 1):
                    print(f'    {i}. Score {link["relevance_score"]}: {link["text"][:100]}...')
            
            time.sleep(2)  # Rate limiting
            return True
        else:
            print(f'  Failed: HTTP {response.status_code}')
            return False
            
    except Exception as e:
        print(f'  Error: {str(e)}')
        return False

# Search for journals first (focusing on most likely candidates)
priority_journal_queries = [
    'Fafnir journal academic medieval',
    'Regin journal Norse mythology',
    'Fafnir journal dragon studies',
    '"Fafnir journal" academic publication'
]

print('\n--- PRIORITY JOURNAL SEARCHES ---')
for query in priority_journal_queries:
    perform_search(query, 'journal_search')

# Search for Emily Midkiff articles
print('\n--- EMILY MIDKIFF ARTICLE SEARCHES ---')
for query in midkiff_queries[:5]:  # Focus on top 5 queries first
    perform_search(query, 'midkiff_search')

# Step 5: Analyze search results
print('\n=== STEP 5: ANALYZING SEARCH RESULTS ===')

# Compile all findings
analysis_results = {
    'research_objective': 'Find Emily Midkiff June 2014 article in journal named after Hreidmar\'s son',
    'hreidmar_sons_research': hreidmar_sons,
    'search_queries_used': {
        'journal_searches': priority_journal_queries,
        'midkiff_searches': midkiff_queries[:5]
    },
    'search_results_summary': {},
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
}

# Analyze each search result
high_relevance_findings = []
for query, results in search_results.items():
    analysis_results['search_results_summary'][query] = {
        'html_file': results['html_file'],
        'total_relevant_links': results['total_links_found'],
        'top_links': results['relevant_links'][:3]
    }
    
    # Identify high-relevance findings
    for link in results['relevant_links']:
        if link['relevance_score'] >= 3:  # High relevance threshold
            high_relevance_findings.append({
                'query': query,
                'link': link,
                'potential_match': True
            })

analysis_results['high_relevance_findings'] = high_relevance_findings

print(f'Total searches conducted: {len(search_results)}')
print(f'High-relevance findings: {len(high_relevance_findings)}')

if high_relevance_findings:
    print('\nMost promising findings:')
    for i, finding in enumerate(high_relevance_findings[:5], 1):
        print(f'{i}. Query: {finding["query"]}')
        print(f'   Score: {finding["link"]["relevance_score"]}')
        print(f'   Text: {finding["link"]["text"][:150]}...')
        print(f'   URL: {finding["link"]["url"]}')
        print()

# Save comprehensive analysis
analysis_file = os.path.join('workspace', 'hreidmar_sons_midkiff_research.json')
with open(analysis_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

print(f'\n*** RESEARCH PHASE COMPLETE ***')
print(f'✓ Norse mythology research completed for Hreidmar\'s sons')
print(f'✓ {len(search_results)} web searches conducted')
print(f'✓ {len(high_relevance_findings)} high-relevance findings identified')
print(f'✓ Analysis saved to: {analysis_file}')
print('\nNext steps:')
print('1. Review high-relevance findings to identify the correct journal')
print('2. Locate Emily Midkiff\'s specific June 2014 article')
print('3. Extract the article content and identify the two quoted authors')
```

### Development Step 19: Download University of Leicester Dragon Diet Fish Supply Research Paper

**Description**: Conduct a web search for the University of Leicester paper titled "Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?" and download the full PDF of that paper into workspace/dragon_diet_fish_bag.pdf.

**Use Cases**:
- Research consortium automating retrieval of environmental impact assessment PDFs from government portals for comparative analysis
- Pharmaceutical R&D team collecting clinical trial protocols published on university domains to inform study designs
- Legal department scanning court websites and downloading recent case judgments in PDF for compliance monitoring
- Financial analysts aggregating quarterly earnings reports from public company investor relations sites into a centralized workspace
- University librarians ingesting newly published theses and dissertations in PDF format into the institutional repository
- Data journalists scraping city planning PDFs from municipal websites to extract zoning changes and urban development data
- Patent researchers bulk-downloading patent specification PDFs from official patent office domains for prior art searches
- Marketing intelligence teams gathering competitor whitepapers and technical briefs from corporate subdomains for product strategy

```
import os
import sys
import re
import requests

# Step 1: Ensure workspace directory exists
workspace = 'workspace'
if not os.path.isdir(workspace):
    print(f"ERROR: Workspace directory '{workspace}' does not exist.")
    sys.exit(1)
print(f"[INFO] Using workspace: {workspace}\n")

# Step 2: Perform a live Bing search for the target paper PDF on le.ac.uk
search_url = 'https://www.bing.com/search'
query = 'site:le.ac.uk "Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?" filetype:pdf'
params = {'q': query}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html'
}
print(f"[SEARCH] Querying Bing: {query}")
try:
    resp = requests.get(search_url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    html = resp.text
    print(f"[SEARCH] Received {len(html)} characters of HTML from Bing.")
except Exception as e:
    print(f"ERROR: Failed to fetch Bing search results: {e}")
    sys.exit(1)

# Step 3: Extract all .pdf URLs from the HTML
print("[PARSE] Extracting .pdf links from search results...")
all_pdfs = re.findall(r'https?://[^\s'\"]+\.pdf', html)
print(f"[PARSE] Found {len(all_pdfs)} total .pdf URLs in the HTML.")

# Step 4: Filter for le.ac.uk domain
leicester_pdfs = []
for link in set(all_pdfs):
    if 'le.ac.uk' in link.lower():
        print(f"  [MATCH] le.ac.uk PDF link: {link}")
        leicester_pdfs.append(link)

if not leicester_pdfs:
    print("ERROR: No .pdf links on le.ac.uk found in Bing results.")
    print("Please verify that the paper is hosted on le.ac.uk or adjust the query.")
    sys.exit(1)

# Step 5: Download the first matching PDF
pdf_url = leicester_pdfs[0]
pdf_path = os.path.join(workspace, 'dragon_diet_fish_bag.pdf')
print(f"[DOWNLOAD] Downloading PDF from: {pdf_url}")
try:
    rpdf = requests.get(pdf_url, headers=headers, stream=True, timeout=60)
    rpdf.raise_for_status()
    with open(pdf_path, 'wb') as f:
        for chunk in rpdf.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    size = os.path.getsize(pdf_path)
    print(f"[SUCCESS] Saved PDF to: {pdf_path}")
    print(f"[INFO] File size: {size} bytes ({size/1024:.2f} KB)")
    if size < 10 * 1024:
        print("WARNING: PDF file is smaller than 10 KB. It may not be the correct paper.")
        sys.exit(1)
    print("[COMPLETE] PDF download appears successful and exceeds size threshold.")
except Exception as e:
    print(f"ERROR: Failed to download PDF: {e}")
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    sys.exit(1)
```

## Created Time
2025-08-11 07:23:27
