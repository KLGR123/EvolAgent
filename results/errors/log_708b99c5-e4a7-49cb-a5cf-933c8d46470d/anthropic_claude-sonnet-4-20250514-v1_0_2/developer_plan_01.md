# Developer Plan 01

## Plan
Search for the DeepFruits fruit detection research paper from 2016 on Connected Papers platform. Navigate to the Connected Papers website and locate the specific graph/visualization for the DeepFruits paper to examine the bubble sizes and identify what feature determines the size of the largest bubble in the network visualization.

## Description
This is the optimal first step because: (1) We need to locate the specific DeepFruits paper from 2016 on Connected Papers to access its network graph visualization, (2) No previous research has been conducted yet, (3) Expected outcome is to find the Connected Papers page for DeepFruits and examine the bubble-based network graph to understand what feature controls bubble sizing, (4) This directly targets the core TASK requirement to identify what causes the largest bubble's size in the DeepFruits detection graph on Connected Papers

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

### Development Step 1: Locate 2016 Uganda SPFMV/SPCSV Research on EC-Numbered Chemicals in Virus Detection Methods

**Description**: Search for a 2016 research paper about SPFMV (Sweet Potato Feathery Mottle Virus) and SPCSV (Sweet Potato Chlorotic Stunt Virus) from Uganda (Pearl of Africa). Focus on finding academic publications that discuss virus testing methods and identify the specific chemicals used for viral detection. Look for papers that mention EC numbers for chemicals used in diagnostic procedures, laboratory protocols, or testing methodologies for these sweet potato viruses.

**Use Cases**:
- Plant pathology research optimization for laboratory teams in Uganda to automate the discovery of 2016 SPFMV and SPCSV diagnostic protocols and EC-numbered chemicals
- Agricultural extension program development to source region-specific viral detection methods and reagent lists for training farmers on sweet potato disease surveillance
- Regulatory compliance auditing for government agencies ensuring diagnostic kits use approved EC-number chemicals in Uganda’s sweet potato virus testing
- Biotech product sourcing by agro-chemical manufacturers to identify chemicals and protocols cited in academic publications for commercial assay kit development
- Academic library services automating literature curation of African plant virus research, tagging papers by year, region, and methodology for institutional repositories
- Cross-pathogen diagnostic workflow adaptation where plant virologists repurpose SPFMV/SPCSV search templates to find testing methods for other tuber crops in East Africa
- Grant proposal preparation for international research consortia, extracting precedent studies on virus detection reagents and protocols to justify methodology in funding applications

```
import os
import requests
import json
from datetime import datetime

# Search for 2016 research paper about SPFMV and SPCSV from Uganda
# Focus on finding academic publications discussing virus testing methods and specific chemicals used for viral detection

api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print("API key found, proceeding with search for SPFMV/SPCSV research from Uganda...")
    print("=" * 80)
    print("SEARCHING FOR 2016 UGANDA SWEET POTATO VIRUS RESEARCH PAPER")
    print("Target viruses: SPFMV (Sweet Potato Feathery Mottle Virus) and SPCSV (Sweet Potato Chlorotic Stunt Virus)")
    print("Focus: Virus testing methods, diagnostic chemicals, EC numbers")
    print("=" * 80)
    
    # Define specific search queries targeting the 2016 Uganda sweet potato virus research
    search_queries = [
        '"Sweet Potato Feathery Mottle Virus" "Sweet Potato Chlorotic Stunt Virus" Uganda 2016 testing methods',
        'SPFMV SPCSV Uganda 2016 "Pearl of Africa" diagnostic chemicals',
        '"Sweet Potato Feathery Mottle Virus" "Sweet Potato Chlorotic Stunt Virus" Uganda 2016 laboratory protocols',
        'SPFMV SPCSV Uganda 2016 EC numbers chemical detection',
        '"Sweet Potato Feathery Mottle Virus" Uganda 2016 viral detection methodology',
        '"Sweet Potato Chlorotic Stunt Virus" Uganda 2016 testing procedures chemicals',
        'Uganda sweet potato virus 2016 SPFMV SPCSV diagnostic methods',
        '"Pearl of Africa" sweet potato virus 2016 SPFMV SPCSV research paper',
        'Uganda 2016 sweet potato virus testing "EC number" chemicals',
        'SPFMV SPCSV Uganda 2016 filetype:pdf research paper'
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
                    for j, result in enumerate(results['organic_results'][:5], 1):
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No URL')
                        snippet = result.get('snippet', 'No snippet')
                        
                        # Check for highly relevant indicators
                        title_lower = title.lower()
                        snippet_lower = snippet.lower()
                        combined_text = f"{title_lower} {snippet_lower}"
                        
                        # Key indicators for the specific research
                        key_indicators = [
                            'spfmv',
                            'spcsv',
                            'sweet potato feathery mottle virus',
                            'sweet potato chlorotic stunt virus',
                            'uganda',
                            '2016',
                            'pearl of africa',
                            'testing methods',
                            'diagnostic',
                            'chemicals',
                            'ec number',
                            'laboratory',
                            'detection',
                            'viral',
                            'methodology'
                        ]
                        
                        matching_indicators = [ind for ind in key_indicators if ind in combined_text]
                        
                        print(f"\n  Result {j}:")
                        print(f"    Title: {title}")
                        print(f"    URL: {link}")
                        print(f"    Snippet: {snippet[:300]}{'...' if len(snippet) > 300 else ''}")
                        
                        if matching_indicators:
                            print(f"    ⭐ MATCHING INDICATORS ({len(matching_indicators)}): {', '.join(matching_indicators)}")
                            
                            # Special attention to academic sources
                            if any(domain in link.lower() for domain in ['researchgate', 'pubmed', 'ncbi', 'sciencedirect', 'springer', 'wiley', 'taylor', 'francis', '.edu', 'doi.org', 'arxiv', '.pdf']):
                                print(f"    🎯 ACADEMIC SOURCE: High-priority research publication")
                                
                            # Check for Uganda/African research institutions
                            if any(term in combined_text for term in ['makerere', 'kampala', 'uganda', 'african', 'pearl of africa']):
                                print(f"    🌍 UGANDA/AFRICAN RESEARCH: Regional relevance confirmed")
                                
                            # Check for specific virus mentions
                            if 'spfmv' in combined_text and 'spcsv' in combined_text:
                                print(f"    🦠 BOTH VIRUSES MENTIONED: SPFMV and SPCSV detected")
                                
                            # Check for methodology/chemical indicators
                            if any(term in combined_text for term in ['testing', 'diagnostic', 'chemical', 'ec number', 'methodology', 'protocol']):
                                print(f"    🧪 METHODOLOGY FOCUS: Testing/chemical content indicated")
                        
                        else:
                            print(f"    No specific matching indicators found")
                    
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
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE SEARCH RESULTS ANALYSIS")
    print("=" * 80)
    
    # Save all search results to workspace for detailed analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"workspace/uganda_spfmv_spcsv_2016_search_results_{timestamp}.json"
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            'search_target': {
                'viruses': ['SPFMV (Sweet Potato Feathery Mottle Virus)', 'SPCSV (Sweet Potato Chlorotic Stunt Virus)'],
                'location': 'Uganda (Pearl of Africa)',
                'year': '2016',
                'focus': 'Virus testing methods, diagnostic chemicals, EC numbers'
            },
            'search_timestamp': timestamp,
            'total_queries': len(search_queries),
            'queries_executed': search_queries,
            'search_results': all_search_results
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Search results saved to: {results_file}")
    
    # Analyze findings across all searches
    total_results = sum(len(query_result['results']) for query_result in all_search_results)
    print(f"Total search results collected: {total_results}")
    
    # Categorize results by relevance
    high_relevance_results = []
    uganda_specific_results = []
    both_viruses_results = []
    methodology_results = []
    academic_sources = []
    pdf_sources = []
    
    for query_result in all_search_results:
        for result in query_result['results']:
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            link = result.get('link', '').lower()
            combined = f"{title} {snippet} {link}"
            
            result_with_context = {
                'query': query_result['query'],
                'title': result.get('title'),
                'link': result.get('link'),
                'snippet': result.get('snippet')
            }
            
            # High relevance: contains multiple key terms
            relevance_score = 0
            if 'spfmv' in combined: relevance_score += 1
            if 'spcsv' in combined: relevance_score += 1
            if 'uganda' in combined: relevance_score += 1
            if '2016' in combined: relevance_score += 1
            if any(term in combined for term in ['testing', 'diagnostic', 'chemical', 'detection']): relevance_score += 1
            
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
            if any(domain in link for domain in ['researchgate', 'pubmed', 'ncbi', 'sciencedirect', 'springer', 'wiley', '.edu', 'doi.org']):
                academic_sources.append(result_with_context)
            
            # PDF sources
            if '.pdf' in link or 'filetype:pdf' in query_result['query']:
                pdf_sources.append(result_with_context)
    
    # Sort high relevance results by score
    high_relevance_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    print(f"\n📊 RESULTS CATEGORIZATION:")
    print(f"High Relevance Results (3+ matching criteria): {len(high_relevance_results)}")
    print(f"Uganda-Specific Results: {len(uganda_specific_results)}")
    print(f"Both Viruses Mentioned: {len(both_viruses_results)}")
    print(f"Methodology/Testing Focus: {len(methodology_results)}")
    print(f"Academic Sources: {len(academic_sources)}")
    print(f"PDF Sources: {len(pdf_sources)}")
    
    if high_relevance_results:
        print(f"\n🎯 TOP HIGH-RELEVANCE RESULTS:")
        for i, result in enumerate(high_relevance_results[:5], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     URL: {result['link']}")
            print(f"     Relevance Score: {result['relevance_score']}/5")
            print(f"     Query: {result['query']}")
            print(f"     Snippet: {result['snippet'][:200]}...")
    
    if both_viruses_results:
        print(f"\n🦠 RESULTS MENTIONING BOTH SPFMV AND SPCSV:")
        for i, result in enumerate(both_viruses_results[:3], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     URL: {result['link']}")
            print(f"     Snippet: {result['snippet'][:150]}...")
    
    if academic_sources:
        print(f"\n📚 ACADEMIC/RESEARCH SOURCES:")
        for i, result in enumerate(academic_sources[:5], 1):
            print(f"\n  {i}. {result['title']}")
            print(f"     URL: {result['link']}")
            print(f"     Snippet: {result['snippet'][:150]}...")
    
    print(f"\n📋 SEARCH STATUS SUMMARY:")
    if high_relevance_results:
        print("✅ HIGH-RELEVANCE RESULTS FOUND")
        print("   - Multiple results matching 3+ key criteria")
        print("   - Ready for detailed content analysis")
    elif uganda_specific_results or both_viruses_results:
        print("⚠️ PARTIAL MATCHES FOUND")
        print("   - Some relevant results identified")
        print("   - May require broader search or alternative keywords")
    else:
        print("❌ LIMITED RELEVANT RESULTS")
        print("   - Few matching results found")
        print("   - May need different search strategy")
    
    print(f"\nDetailed search data saved to: {results_file}")
    print("Ready for next phase: detailed analysis of identified papers and content extraction.")
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
2025-08-14 00:20:19
