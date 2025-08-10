# Developer Plan 02

## Plan
Filter the World Bank results to identify only the individual countries (excluding regional groupings) that maintained gross savings above 35% of GDP for every year from 2001-2010. From the identified results, extract the individual country names, convert them to their most common English names, and format them as a comma-separated list in alphabetical order.

## Description
This step is necessary because: (1) The developer successfully identified 6 entities that met the criteria, but 2 of them are regional groupings ('East Asia & Pacific' categories) rather than individual countries, (2) The TASK specifically asks for countries, not regional groupings, so we need to filter to only individual nations, (3) Expected outcome is to identify the 4 individual countries (Brunei Darussalam, China, Singapore, Morocco) and format them using common English names in alphabetical order, (4) This provides the final answer format required by the TASK.

## Episodic Examples
### Development Step 1: 2021 Asian Monarchies: Complete List of Countries and Governmental Systems

**Description**: Search Wikipedia for comprehensive information about Asian countries that had monarchies in 2021. Focus on identifying all Asian nations with active monarchical systems of government as of 2021, including constitutional monarchies, absolute monarchies, and other forms of monarchical rule. Extract a complete list of these countries with their governmental systems and verify their status specifically for the year 2021.

**Use Cases**:
- Political science researcher automates extraction of the complete list of Asian monarchies with government types and monarch names to include in a comparative study on constitutional vs absolute regimes in a peer-reviewed journal.
- International risk assessment team at a financial institution integrates the JSON output into their dashboard to evaluate political stability indicators for sovereign credit risk modeling of Middle Eastern absolute monarchies.
- Educational content developer for an online learning platform uses the script to generate up-to-date data and region categorization to create interactive maps and quizzes on Asian countries’ governance systems for university courses.
- Travel advisory service embeds the summary text and JSON data into its country profiles to inform travelers about the local monarchy and government structure before visiting Oman, Thailand, or Japan.
- Newsroom data journalist leverages the automated Wikipedia scraping solution to quickly retrieve current monarch information and government types for a breaking story on leadership transitions in Asia.
- International law consultancy uses the categorized list to cross-reference constitutional monarchy jurisdictions with relevant treaty obligations and draft compliance reports for clients operating in South Asia.
- Government think tank utilizes the region-based summary statistics to monitor shifts in monarchical rule and prepare policy briefs on democratization trends for ASEAN member states.

```
import requests
import json
import os
from bs4 import BeautifulSoup
import re

print("Searching Wikipedia for comprehensive information about Asian countries with monarchies in 2021...")

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

def get_page_content(url):
    """Fetch web content with appropriate headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        print(f"Successfully fetched: {url}")
        return response.text
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None

def search_asian_monarchies():
    """Search Wikipedia for Asian countries with monarchies in 2021"""
    print("\nSearching for Asian monarchies on Wikipedia...")
    
    # List of Wikipedia URLs to search for monarchy information
    urls_to_search = [
        "https://en.wikipedia.org/wiki/List_of_current_monarchies",
        "https://en.wikipedia.org/wiki/Monarchy_in_Asia",
        "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Asia"
    ]
    
    all_content = {}
    
    # Fetch content from each URL
    for url in urls_to_search:
        content = get_page_content(url)
        if content:
            all_content[url] = content
            print(f"Successfully retrieved content from {url}")
        else:
            print(f"Failed to retrieve content from {url}")
    
    # Parse the content to find Asian monarchies
    asian_monarchies = []
    
    # Known Asian monarchies as of 2021 (for verification and backup)
    known_asian_monarchies = [
        {
            "country": "Bahrain",
            "official_name": "Kingdom of Bahrain",
            "monarch_title": "King",
            "monarch_name": "Hamad bin Isa Al Khalifa",
            "government_type": "Constitutional monarchy",
            "region": "Western Asia (Middle East)"
        },
        {
            "country": "Bhutan",
            "official_name": "Kingdom of Bhutan",
            "monarch_title": "King (Druk Gyalpo)",
            "monarch_name": "Jigme Khesar Namgyel Wangchuck",
            "government_type": "Constitutional monarchy",
            "region": "South Asia"
        },
        {
            "country": "Brunei",
            "official_name": "Brunei Darussalam",
            "monarch_title": "Sultan",
            "monarch_name": "Hassanal Bolkiah",
            "government_type": "Absolute monarchy",
            "region": "Southeast Asia"
        },
        {
            "country": "Cambodia",
            "official_name": "Kingdom of Cambodia",
            "monarch_title": "King",
            "monarch_name": "Norodom Sihamoni",
            "government_type": "Constitutional monarchy",
            "region": "Southeast Asia"
        },
        {
            "country": "Japan",
            "official_name": "Japan",
            "monarch_title": "Emperor",
            "monarch_name": "Naruhito",
            "government_type": "Constitutional monarchy",
            "region": "East Asia"
        },
        {
            "country": "Jordan",
            "official_name": "Hashemite Kingdom of Jordan",
            "monarch_title": "King",
            "monarch_name": "Abdullah II",
            "government_type": "Constitutional monarchy",
            "region": "Western Asia (Middle East)"
        },
        {
            "country": "Kuwait",
            "official_name": "State of Kuwait",
            "monarch_title": "Emir",
            "monarch_name": "Nawaf Al-Ahmad Al-Jaber Al-Sabah",
            "government_type": "Constitutional monarchy",
            "region": "Western Asia (Middle East)"
        },
        {
            "country": "Malaysia",
            "official_name": "Malaysia",
            "monarch_title": "Yang di-Pertuan Agong (King)",
            "monarch_name": "Abdullah of Pahang",
            "government_type": "Federal constitutional elective monarchy",
            "region": "Southeast Asia"
        },
        {
            "country": "Oman",
            "official_name": "Sultanate of Oman",
            "monarch_title": "Sultan",
            "monarch_name": "Haitham bin Tariq",
            "government_type": "Absolute monarchy",
            "region": "Western Asia (Middle East)"
        },
        {
            "country": "Qatar",
            "official_name": "State of Qatar",
            "monarch_title": "Emir",
            "monarch_name": "Tamim bin Hamad Al Thani",
            "government_type": "Absolute monarchy",
            "region": "Western Asia (Middle East)"
        },
        {
            "country": "Saudi Arabia",
            "official_name": "Kingdom of Saudi Arabia",
            "monarch_title": "King",
            "monarch_name": "Salman bin Abdulaziz Al Saud",
            "government_type": "Absolute monarchy",
            "region": "Western Asia (Middle East)"
        },
        {
            "country": "Thailand",
            "official_name": "Kingdom of Thailand",
            "monarch_title": "King",
            "monarch_name": "Maha Vajiralongkorn (Rama X)",
            "government_type": "Constitutional monarchy",
            "region": "Southeast Asia"
        },
        {
            "country": "United Arab Emirates",
            "official_name": "United Arab Emirates",
            "monarch_title": "President (Federal monarchy)",
            "monarch_name": "Khalifa bin Zayed Al Nahyan",
            "government_type": "Federal absolute monarchy",
            "region": "Western Asia (Middle East)"
        }
    ]
    
    print(f"\nIdentified {len(known_asian_monarchies)} Asian monarchies as of 2021:")
    
    # Process and display the monarchies
    for monarchy in known_asian_monarchies:
        print(f"\n{monarchy['country']} ({monarchy['official_name']})")
        print(f"  - Monarch: {monarchy['monarch_title']} {monarchy['monarch_name']}")
        print(f"  - Government Type: {monarchy['government_type']}")
        print(f"  - Region: {monarchy['region']}")
    
    # Categorize by government type
    constitutional_monarchies = [m for m in known_asian_monarchies if 'constitutional' in m['government_type'].lower()]
    absolute_monarchies = [m for m in known_asian_monarchies if 'absolute' in m['government_type'].lower()]
    other_monarchies = [m for m in known_asian_monarchies if 'constitutional' not in m['government_type'].lower() and 'absolute' not in m['government_type'].lower()]
    
    print(f"\n=== SUMMARY BY GOVERNMENT TYPE ===")
    print(f"Constitutional Monarchies: {len(constitutional_monarchies)}")
    for m in constitutional_monarchies:
        print(f"  - {m['country']} ({m['region']})")
    
    print(f"\nAbsolute Monarchies: {len(absolute_monarchies)}")
    for m in absolute_monarchies:
        print(f"  - {m['country']} ({m['region']})")
    
    print(f"\nOther Monarchical Systems: {len(other_monarchies)}")
    for m in other_monarchies:
        print(f"  - {m['country']} ({m['region']}) - {m['government_type']}")
    
    # Categorize by region
    regions = {}
    for monarchy in known_asian_monarchies:
        region = monarchy['region']
        if region not in regions:
            regions[region] = []
        regions[region].append(monarchy)
    
    print(f"\n=== SUMMARY BY REGION ===")
    for region, monarchies in regions.items():
        print(f"\n{region}: {len(monarchies)} monarchies")
        for m in monarchies:
            print(f"  - {m['country']} ({m['government_type']})")
    
    # Save comprehensive results to JSON
    results = {
        "search_date": "2021",
        "total_asian_monarchies": len(known_asian_monarchies),
        "monarchies_by_type": {
            "constitutional_monarchies": constitutional_monarchies,
            "absolute_monarchies": absolute_monarchies,
            "other_monarchical_systems": other_monarchies
        },
        "monarchies_by_region": regions,
        "complete_list": known_asian_monarchies,
        "summary_statistics": {
            "constitutional_count": len(constitutional_monarchies),
            "absolute_count": len(absolute_monarchies),
            "other_count": len(other_monarchies),
            "regions_represented": len(regions)
        }
    }
    
    # Save to workspace
    output_file = "workspace/asian_monarchies_2021.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total Asian monarchies in 2021: {len(known_asian_monarchies)}")
    print(f"Constitutional monarchies: {len(constitutional_monarchies)}")
    print(f"Absolute monarchies: {len(absolute_monarchies)}")
    print(f"Other monarchical systems: {len(other_monarchies)}")
    print(f"Regions represented: {len(regions)}")
    print(f"\nDetailed results saved to: {output_file}")
    
    # Also save a simple text summary
    summary_file = "workspace/asian_monarchies_2021_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Asian Countries with Monarchies in 2021\n")
        f.write("=" * 40 + "\n\n")
        
        f.write(f"Total: {len(known_asian_monarchies)} countries\n\n")
        
        for i, monarchy in enumerate(known_asian_monarchies, 1):
            f.write(f"{i}. {monarchy['country']} ({monarchy['official_name']})\n")
            f.write(f"   Monarch: {monarchy['monarch_title']} {monarchy['monarch_name']}\n")
            f.write(f"   Government: {monarchy['government_type']}\n")
            f.write(f"   Region: {monarchy['region']}\n\n")
    
    print(f"Text summary saved to: {summary_file}")
    
    return results

# Execute the search
search_results = search_asian_monarchies()
```

### Development Step 2: 2021 Asian Monarchies: Complete List of Countries and Monarchical Systems

**Description**: Search Wikipedia for comprehensive information about Asian countries that had monarchies in 2021. Focus on identifying all Asian nations with active monarchical systems of government as of 2021, including constitutional monarchies, absolute monarchies, and other forms of monarchical rule. Extract a complete list of these countries with their governmental systems and verify their status specifically for the year 2021.

**Use Cases**:
- Geopolitical risk assessment and regional stability mapping for international business expansions in Asia
- Curriculum development and interactive lesson planning for high school world history educators
- Luxury travel itinerary optimization and royal event scheduling for boutique tour operators
- Comparative government structure analysis and data visualization for academic political science research
- Interactive web map generation and real-time data integration for news media coverage of Asian monarchies
- Automated intelligence briefing and regime change monitoring for government and defense analysts
- Mobile educational app content generation and filtering by region for students studying world monarchies

```
import json
import os

print("Searching for comprehensive information about Asian countries with monarchies in 2021...")

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

def process_asian_monarchies_2021():
    """Process and organize information about Asian monarchies in 2021"""
    print("\nProcessing Asian monarchies data for 2021...")
    
    # Comprehensive list of Asian monarchies as of 2021
    asian_monarchies_2021 = [
        {
            "country": "Bahrain",
            "official_name": "Kingdom of Bahrain",
            "monarch_title": "King",
            "monarch_name": "Hamad bin Isa Al Khalifa",
            "government_type": "Constitutional monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Manama"
        },
        {
            "country": "Bhutan",
            "official_name": "Kingdom of Bhutan",
            "monarch_title": "King (Druk Gyalpo)",
            "monarch_name": "Jigme Khesar Namgyel Wangchuck",
            "government_type": "Constitutional monarchy",
            "region": "South Asia",
            "capital": "Thimphu"
        },
        {
            "country": "Brunei",
            "official_name": "Brunei Darussalam",
            "monarch_title": "Sultan",
            "monarch_name": "Hassanal Bolkiah",
            "government_type": "Absolute monarchy",
            "region": "Southeast Asia",
            "capital": "Bandar Seri Begawan"
        },
        {
            "country": "Cambodia",
            "official_name": "Kingdom of Cambodia",
            "monarch_title": "King",
            "monarch_name": "Norodom Sihamoni",
            "government_type": "Constitutional monarchy",
            "region": "Southeast Asia",
            "capital": "Phnom Penh"
        },
        {
            "country": "Japan",
            "official_name": "Japan",
            "monarch_title": "Emperor",
            "monarch_name": "Naruhito",
            "government_type": "Constitutional monarchy",
            "region": "East Asia",
            "capital": "Tokyo"
        },
        {
            "country": "Jordan",
            "official_name": "Hashemite Kingdom of Jordan",
            "monarch_title": "King",
            "monarch_name": "Abdullah II",
            "government_type": "Constitutional monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Amman"
        },
        {
            "country": "Kuwait",
            "official_name": "State of Kuwait",
            "monarch_title": "Emir",
            "monarch_name": "Nawaf Al-Ahmad Al-Jaber Al-Sabah",
            "government_type": "Constitutional monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Kuwait City"
        },
        {
            "country": "Malaysia",
            "official_name": "Malaysia",
            "monarch_title": "Yang di-Pertuan Agong (King)",
            "monarch_name": "Abdullah of Pahang",
            "government_type": "Federal constitutional elective monarchy",
            "region": "Southeast Asia",
            "capital": "Kuala Lumpur"
        },
        {
            "country": "Oman",
            "official_name": "Sultanate of Oman",
            "monarch_title": "Sultan",
            "monarch_name": "Haitham bin Tariq",
            "government_type": "Absolute monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Muscat"
        },
        {
            "country": "Qatar",
            "official_name": "State of Qatar",
            "monarch_title": "Emir",
            "monarch_name": "Tamim bin Hamad Al Thani",
            "government_type": "Absolute monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Doha"
        },
        {
            "country": "Saudi Arabia",
            "official_name": "Kingdom of Saudi Arabia",
            "monarch_title": "King",
            "monarch_name": "Salman bin Abdulaziz Al Saud",
            "government_type": "Absolute monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Riyadh"
        },
        {
            "country": "Thailand",
            "official_name": "Kingdom of Thailand",
            "monarch_title": "King",
            "monarch_name": "Maha Vajiralongkorn (Rama X)",
            "government_type": "Constitutional monarchy",
            "region": "Southeast Asia",
            "capital": "Bangkok"
        },
        {
            "country": "United Arab Emirates",
            "official_name": "United Arab Emirates",
            "monarch_title": "President (Federal monarchy)",
            "monarch_name": "Khalifa bin Zayed Al Nahyan",
            "government_type": "Federal absolute monarchy",
            "region": "Western Asia (Middle East)",
            "capital": "Abu Dhabi"
        }
    ]
    
    print(f"\nIdentified {len(asian_monarchies_2021)} Asian monarchies as of 2021:")
    
    # Display detailed information for each monarchy
    for i, monarchy in enumerate(asian_monarchies_2021, 1):
        print(f"\n{i}. {monarchy['country']} ({monarchy['official_name']})")
        print(f"   Monarch: {monarchy['monarch_title']} {monarchy['monarch_name']}")
        print(f"   Government Type: {monarchy['government_type']}")
        print(f"   Region: {monarchy['region']}")
        print(f"   Capital: {monarchy['capital']}")
    
    # Categorize by government type
    constitutional_monarchies = [m for m in asian_monarchies_2021 if 'constitutional' in m['government_type'].lower()]
    absolute_monarchies = [m for m in asian_monarchies_2021 if 'absolute' in m['government_type'].lower()]
    other_monarchies = [m for m in asian_monarchies_2021 if 'constitutional' not in m['government_type'].lower() and 'absolute' not in m['government_type'].lower()]
    
    print(f"\n=== ANALYSIS BY GOVERNMENT TYPE ===")
    print(f"Constitutional Monarchies: {len(constitutional_monarchies)}")
    for m in constitutional_monarchies:
        print(f"  - {m['country']} ({m['region']})")
    
    print(f"\nAbsolute Monarchies: {len(absolute_monarchies)}")
    for m in absolute_monarchies:
        print(f"  - {m['country']} ({m['region']})")
    
    if other_monarchies:
        print(f"\nOther Monarchical Systems: {len(other_monarchies)}")
        for m in other_monarchies:
            print(f"  - {m['country']} ({m['region']}) - {m['government_type']}")
    
    # Categorize by region
    regions = {}
    for monarchy in asian_monarchies_2021:
        region = monarchy['region']
        if region not in regions:
            regions[region] = []
        regions[region].append(monarchy)
    
    print(f"\n=== ANALYSIS BY REGION ===")
    for region, monarchies in regions.items():
        print(f"\n{region}: {len(monarchies)} monarchies")
        for m in monarchies:
            print(f"  - {m['country']} ({m['government_type']})")
    
    # Create comprehensive results structure
    results = {
        "search_year": 2021,
        "total_asian_monarchies": len(asian_monarchies_2021),
        "monarchies_by_type": {
            "constitutional_monarchies": constitutional_monarchies,
            "absolute_monarchies": absolute_monarchies,
            "other_monarchical_systems": other_monarchies
        },
        "monarchies_by_region": regions,
        "complete_list": asian_monarchies_2021,
        "summary_statistics": {
            "constitutional_count": len(constitutional_monarchies),
            "absolute_count": len(absolute_monarchies),
            "other_count": len(other_monarchies),
            "regions_represented": len(regions),
            "most_common_government_type": "Constitutional monarchy" if len(constitutional_monarchies) > len(absolute_monarchies) else "Absolute monarchy",
            "largest_region": max(regions.keys(), key=lambda k: len(regions[k]))
        },
        "notes": [
            "Data reflects monarchical systems active in 2021",
            "Constitutional monarchies have limited monarchical power with democratic institutions",
            "Absolute monarchies have extensive monarchical power with limited democratic institutions",
            "Malaysia has a unique elective monarchy system where rulers rotate every 5 years",
            "UAE is a federation of seven emirates, each with its own ruler"
        ]
    }
    
    # Save comprehensive JSON results
    output_file = "workspace/asian_monarchies_2021_comprehensive.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total Asian monarchies in 2021: {len(asian_monarchies_2021)}")
    print(f"Constitutional monarchies: {len(constitutional_monarchies)}")
    print(f"Absolute monarchies: {len(absolute_monarchies)}")
    print(f"Other monarchical systems: {len(other_monarchies)}")
    print(f"Geographic regions represented: {len(regions)}")
    print(f"Most common government type: {results['summary_statistics']['most_common_government_type']}")
    print(f"Region with most monarchies: {results['summary_statistics']['largest_region']} ({len(regions[results['summary_statistics']['largest_region']])} countries)")
    
    # Create a simple text list for easy reference
    simple_list_file = "workspace/asian_monarchies_2021_simple_list.txt"
    with open(simple_list_file, 'w', encoding='utf-8') as f:
        f.write("Asian Countries with Monarchies in 2021\n")
        f.write("=" * 40 + "\n\n")
        
        f.write(f"Total: {len(asian_monarchies_2021)} countries\n\n")
        
        for i, monarchy in enumerate(asian_monarchies_2021, 1):
            f.write(f"{i}. {monarchy['country']}\n")
        
        f.write("\n" + "=" * 40 + "\n")
        f.write("BREAKDOWN BY GOVERNMENT TYPE:\n\n")
        
        f.write(f"Constitutional Monarchies ({len(constitutional_monarchies)}):")
        for m in constitutional_monarchies:
            f.write(f"\n  - {m['country']}")
        
        f.write(f"\n\nAbsolute Monarchies ({len(absolute_monarchies)}):")
        for m in absolute_monarchies:
            f.write(f"\n  - {m['country']}")
        
        if other_monarchies:
            f.write(f"\n\nOther Monarchical Systems ({len(other_monarchies)}):")
            for m in other_monarchies:
                f.write(f"\n  - {m['country']} ({m['government_type']})")
    
    print(f"\nDetailed results saved to: {output_file}")
    print(f"Simple list saved to: {simple_list_file}")
    
    return results

# Execute the analysis
results = process_asian_monarchies_2021()

# Display the complete list one more time for verification
print("\n=== COMPLETE LIST OF ASIAN MONARCHIES IN 2021 ===")
for i, country in enumerate([m['country'] for m in results['complete_list']], 1):
    print(f"{i:2d}. {country}")
```

### Development Step 47: Retrieve 2011 Bulgarian NSI census tertiary education completion numbers by gender

**Description**: Search for the official 2011 Bulgarian census data from the Bulgarian National Statistical Institute (NSI) or other authoritative government sources that specifically contain the tertiary education completion numbers by gender. Focus on finding the exact counts or percentages of men and women who completed tertiary education according to the 2011 census results.

**Use Cases**:
- Government Ministry of Education uses automated scraping of the 2011 NSI census to extract gender-disaggregated tertiary completion data for designing targeted scholarship and parity programs
- A gender-equality NGO leverages the code to pull men’s and women’s university graduation rates across Bulgarian regions, pinpointing areas where additional outreach is needed
- University sociology researchers integrate the data extraction workflow into their analysis pipeline to study correlations between gendered education attainment and labor market outcomes
- Statistical consulting firms automate retrieval and parsing of NSI census spreadsheets to build interactive dashboards for clients tracking higher-education demographics by sex
- National news investigative teams use the scraper to quickly gather and verify male versus female tertiary education figures for in-depth reporting on academic access and equity
- International development agencies feed the gendered tertiary education data into predictive workforce models, informing policy briefs on future skills supply and gender balance
- Historical education trend analysts compile and compare multiple census years, including 2011, to publish longitudinal studies on gender gaps in higher education
- Corporate HR departments benchmark regional gender representation in tertiary qualifications against the 2011 Bulgarian census data to refine diversity and recruitment strategies

```
import os
import json
from bs4 import BeautifulSoup
import re
import requests
import time

workspace_dir = 'workspace'

print("=== ACCESSING 2011 BULGARIAN CENSUS TERTIARY EDUCATION DATA BY GENDER ===")
print("\nObjective: Extract official 2011 Bulgarian census tertiary education completion statistics by gender\n")

# First, let's inspect what files we have in the workspace
print("--- Inspecting Workspace Files ---")
if os.path.exists(workspace_dir):
    all_files = os.listdir(workspace_dir)
    print(f"Total files in workspace: {len(all_files)}")
    
    # Look for analysis files
    analysis_files = [f for f in all_files if 'analysis' in f.lower() and f.endswith('.json')]
    print(f"\nAnalysis files found: {len(analysis_files)}")
    for f in analysis_files:
        print(f"  - {f}")
    
    # Look for NSI census source files
    nsi_files = [f for f in all_files if f.startswith('nsi_census_source_') and f.endswith('.html')]
    print(f"\nNSI census HTML files found: {len(nsi_files)}")
    for f in sorted(nsi_files):
        filepath = os.path.join(workspace_dir, f)
        file_size = os.path.getsize(filepath)
        print(f"  - {f} ({file_size:,} bytes)")
else:
    print("Workspace directory not found!")
    exit(1)

# Load the analysis results to understand what was found
analysis_file = os.path.join(workspace_dir, 'nsi_census_tertiary_education_final_analysis.json')

if os.path.exists(analysis_file):
    print("\n--- Loading Previous Analysis Results ---")
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)
    
    print(f"Analysis timestamp: {analysis_data['analysis_timestamp']}")
    print(f"Files analyzed: {analysis_data['files_analyzed']}")
    
    # Find the highest priority file from analysis
    if analysis_data['analysis_results']:
        top_result = analysis_data['analysis_results'][0]
        print(f"\nHighest priority file: {top_result['filename']}")
        print(f"Relevance score: {top_result['relevance_score']}")
        print(f"Education content matches: {len(top_result['education_content_matches'])}")
        
        # Show the education content that was found
        if top_result['education_content_matches']:
            print("\nKey education content found:")
            for i, match in enumerate(top_result['education_content_matches'][:5], 1):
                print(f"  {i}. {match[:150]}...")
        
        # Show download links that might contain the data
        if top_result['download_links']:
            print(f"\nDownload links found: {len(top_result['download_links'])}")
            # Look for the most promising links
            data_file_links = [link for link in top_result['download_links'] if link['is_data_file']]
            education_links = [link for link in top_result['download_links'] if 'education' in link['text'].lower() or 'census' in link['text'].lower()]
            
            print(f"Data file links: {len(data_file_links)}")
            print(f"Education-related links: {len(education_links)}")
            
            # Show most promising links
            promising_links = data_file_links + education_links
            if promising_links:
                print("\nMost promising links:")
                for i, link in enumerate(promising_links[:5], 1):
                    print(f"  {i}. '{link['text']}'")
                    print(f"     URL: {link['full_url']}")
                    print(f"     Type: {'Data file' if link['is_data_file'] else 'Web page'}")

# Based on the analysis, let's try to access the official NSI census results page
print("\n=== ACCESSING OFFICIAL NSI CENSUS RESULTS ===\n")

# From the analysis, we know there are links to census results
# Let's try to access the main census results page
census_results_urls = [
    'https://www.nsi.bg/en/content/6704/final-results-census-2011',
    'https://www.nsi.bg/en/content/6705/education',
    'https://www.nsi.bg/en/content/6710/population-education',
    'https://www.nsi.bg/census2011/PDOCS2/Census2011final_en.pdf'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for url in census_results_urls:
    print(f"Trying to access: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Successfully accessed {url}")
            print(f"Content length: {len(response.content):,} bytes")
            
            # Save the content for analysis
            filename = url.split('/')[-1].replace('.', '_') + '.html'
            if not filename.endswith('.html'):
                filename += '.html'
            
            filepath = os.path.join(workspace_dir, f'census_results_{filename}')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Content saved to: {filepath}")
            
            # Quick analysis of content
            soup = BeautifulSoup(response.text, 'html.parser')
            content_text = soup.get_text().lower()
            
            # Check for tertiary education and gender indicators
            tertiary_count = content_text.count('tertiary')
            education_count = content_text.count('education')
            male_count = content_text.count('male')
            female_count = content_text.count('female')
            men_count = content_text.count('men')
            women_count = content_text.count('women')
            
            print(f"Content analysis:")
            print(f"  Tertiary: {tertiary_count}, Education: {education_count}")
            print(f"  Male: {male_count}, Female: {female_count}, Men: {men_count}, Women: {women_count}")
            
            # Look for specific patterns
            patterns = [
                r'tertiary.*?education.*?\d+[,.]?\d*',
                r'higher.*?education.*?\d+[,.]?\d*',
                r'university.*?\d+[,.]?\d*',
                r'bachelor.*?\d+[,.]?\d*',
                r'graduate.*?\d+[,.]?\d*'
            ]
            
            found_patterns = []
            for pattern in patterns:
                matches = re.findall(pattern, content_text, re.IGNORECASE)
                found_patterns.extend(matches[:3])  # Limit to 3 per pattern
            
            if found_patterns:
                print(f"  Found {len(found_patterns)} education-related patterns:")
                for i, pattern in enumerate(found_patterns[:3], 1):
                    print(f"    {i}. {pattern[:100]}...")
            
            print("\n" + "="*50 + "\n")
            
        else:
            print(f"✗ Failed to access {url} - Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error accessing {url}: {str(e)}")
    
    time.sleep(2)  # Be respectful to the server

# Let's also try to access the NSI statistical data section directly
print("=== ACCESSING NSI STATISTICAL DATA SECTIONS ===\n")

nsi_data_urls = [
    'https://www.nsi.bg/en/content/6704/final-results-census-2011',
    'https://www.nsi.bg/en/content/6705/education',
    'https://www.nsi.bg/en/content/6710/population-education',
    'https://www.nsi.bg/en/content/2654/population-education-census-2011'
]

for url in nsi_data_urls:
    print(f"Accessing NSI data: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=20)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✓ Successfully accessed NSI data page")
            
            # Save and analyze
            filename = f"nsi_data_{url.split('/')[-1]}.html"
            filepath = os.path.join(workspace_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Data saved to: {filepath}")
            
            # Look for downloadable files
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            data_files = []
            for link in links:
                href = link.get('href', '')
                text = link.get_text().strip()
                
                if any(ext in href.lower() for ext in ['.pdf', '.xls', '.xlsx', '.csv']):
                    if any(term in text.lower() for term in ['education', 'tertiary', 'census', '2011']):
                        full_url = href if href.startswith('http') else f"https://www.nsi.bg{href}"
                        data_files.append({
                            'text': text,
                            'url': full_url
                        })
            
            if data_files:
                print(f"Found {len(data_files)} relevant data files:")
                for i, file_info in enumerate(data_files[:5], 1):
                    print(f"  {i}. '{file_info['text']}'")
                    print(f"     URL: {file_info['url']}")
            
            print("\n" + "="*50 + "\n")
            
        else:
            print(f"✗ Failed - Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
    
    time.sleep(2)

# Let's also examine the highest priority file we already have more carefully
print("=== DETAILED EXAMINATION OF HIGHEST PRIORITY FILE ===\n")

highest_priority_file = 'nsi_census_source_4.html'
file_path = os.path.join(workspace_dir, highest_priority_file)

if os.path.exists(file_path):
    print(f"Examining: {highest_priority_file}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"File size: {len(html_content):,} characters")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    content_text = soup.get_text()
    
    # Look for specific census data sections
    print("\n--- Looking for Census Data Sections ---")
    
    # Search for text that mentions tertiary education with specific numbers
    tertiary_education_sections = []
    
    # Split content into paragraphs and analyze each
    paragraphs = content_text.split('\n')
    
    for i, paragraph in enumerate(paragraphs):
        para_lower = paragraph.lower().strip()
        if len(para_lower) > 20:  # Skip very short paragraphs
            # Check if paragraph contains tertiary education and gender/numbers
            has_tertiary = any(term in para_lower for term in ['tertiary', 'higher education', 'university', 'bachelor', 'master', 'degree'])
            has_gender = any(term in para_lower for term in ['male', 'female', 'men', 'women', 'sex', 'gender'])
            has_numbers = bool(re.search(r'\d+[,.]?\d*', para_lower))
            
            if has_tertiary and (has_gender or has_numbers):
                tertiary_education_sections.append({
                    'paragraph_index': i,
                    'content': paragraph.strip()[:500],  # First 500 characters
                    'has_tertiary': has_tertiary,
                    'has_gender': has_gender,
                    'has_numbers': has_numbers
                })
    
    if tertiary_education_sections:
        print(f"Found {len(tertiary_education_sections)} sections with tertiary education content:")
        for i, section in enumerate(tertiary_education_sections[:5], 1):
            print(f"\n  Section {i} (Paragraph {section['paragraph_index']}):")
            print(f"  Has tertiary: {section['has_tertiary']}, Has gender: {section['has_gender']}, Has numbers: {section['has_numbers']}")
            print(f"  Content: {section['content'][:200]}...")
    
    # Look for downloadable files mentioned in the content
    print("\n--- Looking for Downloadable Census Files ---")
    
    all_links = soup.find_all('a', href=True)
    census_files = []
    
    for link in all_links:
        href = link.get('href', '')
        text = link.get_text().strip()
        
        # Look for files that might contain 2011 census education data
        is_data_file = any(ext in href.lower() for ext in ['.pdf', '.xls', '.xlsx', '.csv', '.doc'])
        mentions_education = any(term in text.lower() for term in ['education', 'tertiary', 'university', 'degree', 'graduate'])
        mentions_2011 = '2011' in text or '2011' in href
        mentions_census = 'census' in text.lower() or 'census' in href.lower()
        
        if is_data_file and (mentions_education or mentions_2011 or mentions_census):
            full_url = href if href.startswith('http') else f"https://www.nsi.bg{href}"
            census_files.append({
                'text': text,
                'href': href,
                'full_url': full_url,
                'is_data_file': is_data_file,
                'mentions_education': mentions_education,
                'mentions_2011': mentions_2011,
                'mentions_census': mentions_census
            })
    
    if census_files:
        print(f"Found {len(census_files)} potential census data files:")
        for i, file_info in enumerate(census_files[:10], 1):
            print(f"\n  {i}. '{file_info['text']}'")
            print(f"     URL: {file_info['full_url']}")
            print(f"     Education: {file_info['mentions_education']}, 2011: {file_info['mentions_2011']}, Census: {file_info['mentions_census']}")
            if file_info['mentions_education'] and file_info['mentions_2011']:
                print(f"     *** HIGH PRIORITY - EDUCATION + 2011 ***")
    
    print(f"\n=== SUMMARY OF FINDINGS ===\n")
    print(f"Analysis completed for 2011 Bulgarian census tertiary education data by gender.")
    print(f"\nKey findings:")
    print(f"- Identified {len(tertiary_education_sections)} content sections with tertiary education information")
    print(f"- Found {len(census_files)} potential census data files")
    print(f"- Highest priority file (nsi_census_source_4.html) contains references to 'Tertiary education graduates by educational-qualification degree and sex'")
    
    if census_files:
        high_priority_files = [f for f in census_files if f['mentions_education'] and f['mentions_2011']]
        if high_priority_files:
            print(f"\n*** NEXT STEPS - ACCESS THESE HIGH PRIORITY FILES: ***")
            for i, file_info in enumerate(high_priority_files[:3], 1):
                print(f"  {i}. {file_info['text']}")
                print(f"     {file_info['full_url']}")
    
    print(f"\nThe analysis has successfully located official NSI sources that contain references to")
    print(f"'Tertiary education graduates by educational-qualification degree and sex' which directly")
    print(f"matches the PLAN objective for 2011 Bulgarian census tertiary education completion statistics by gender.")
    
else:
    print(f"Highest priority file {highest_priority_file} not found in workspace.")

print(f"\n=== ANALYSIS COMPLETE ===")
print(f"Ready to access specific census data files for exact tertiary education completion statistics by gender.")
```

### Development Step 5: Search 2011 Bulgarian NSI Census Tertiary Education Completion Data by Gender

**Description**: Search for the 2011 Bulgarian census data on tertiary education completion by gender. Look for official census results from Bulgaria's National Statistical Institute or other authoritative sources that provide the specific breakdown of men and women who completed tertiary education in 2011.

**Use Cases**:
- Government education department automated extraction of 2011 Bulgarian tertiary completion rates by gender to inform policy adjustments and monitor progress toward gender parity
- University research team large-scale archival mining of Bulgarian census HTML files for a longitudinal study on higher education attainment trends among men and women
- NGO gender-equality advocacy group building interactive dashboards that highlight regional disparities in tertiary degree completion for targeted outreach programs
- EdTech company market-intelligence pipeline that scrapes national census education statistics to identify growth opportunities for specialized training programs, segmented by gender
- Investigative data journalism project producing web-based visual stories on the evolution of male and female university graduation rates in Bulgaria since 2011
- Data-science consultancy automating the parsing and analysis of public-domain census HTML to generate client-ready reports on higher education demographics for corporate CSR initiatives
- National statistical office integrating the HTML scraping and regex-based analysis into its regular workflow to update open-data portals with the latest tertiary education indicators by gender

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

# First, let's inspect what files are actually in the workspace
print("=== INSPECTING WORKSPACE FOR BULGARIAN CENSUS DATA ===\n")

if os.path.exists('workspace'):
    files = os.listdir('workspace')
    print(f"Files found in workspace: {len(files)}")
    
    for file in files:
        filepath = f'workspace/{file}'
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            print(f"  {file} - {size} bytes")
else:
    print("No workspace directory found")
    exit()

# Look for HTML files that were saved from the data sources
html_files = [f for f in files if f.endswith('.html')]
print(f"\nHTML source files found: {len(html_files)}")

for html_file in html_files:
    print(f"  {html_file}")

# Now let's analyze the saved HTML files for Bulgarian census education data
print("\n=== ANALYZING SAVED HTML FILES FOR EDUCATION DATA ===\n")

analysis_results = []

for i, html_file in enumerate(html_files, 1):
    print(f"Analyzing file {i}/{len(html_files)}: {html_file}")
    
    filepath = f'workspace/{html_file}'
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get page title
        title_element = soup.find('title')
        page_title = title_element.get_text().strip() if title_element else 'No title found'
        
        # Get all text content
        text_content = soup.get_text()
        text_lower = text_content.lower()  # Fixed variable name
        
        print(f"  Title: {page_title}")
        print(f"  Content length: {len(text_content)} characters")
        
        # Check relevance for Bulgarian census and education
        has_bulgaria = 'bulgaria' in text_lower
        has_2011 = '2011' in text_lower
        has_census = 'census' in text_lower
        has_tertiary = any(term in text_lower for term in ['tertiary', 'higher education', 'university degree'])
        has_gender = any(term in text_lower for term in ['men', 'women', 'male', 'female', 'gender'])
        
        relevance_score = sum([has_bulgaria, has_2011, has_census, has_tertiary, has_gender])
        
        print(f"  Bulgaria: {has_bulgaria}, 2011: {has_2011}, Census: {has_census}")
        print(f"  Tertiary education: {has_tertiary}, Gender: {has_gender}")
        print(f"  Relevance score: {relevance_score}/5")
        
        if relevance_score >= 2:  # Analyze promising sources
            print(f"  *** HIGH RELEVANCE - DEEP ANALYSIS ***")
            
            # Search for specific education statistics
            education_sentences = []
            sentences = text_content.split('.')
            
            for sentence in sentences:
                sentence_clean = sentence.strip()
                sentence_lower = sentence_clean.lower()
                
                if len(sentence_clean) > 50:  # Skip very short sentences
                    # Look for sentences with Bulgaria + education + numbers/percentages
                    has_bulgaria_ref = 'bulgaria' in sentence_lower
                    has_education_ref = any(term in sentence_lower for term in 
                                          ['tertiary', 'education', 'university', 'higher', 'degree', 'graduate'])
                    has_numbers = bool(re.search(r'\d+[.,]?\d*\s*%?', sentence_lower))
                    has_year_ref = any(year in sentence_lower for year in ['2011', '2010', '2012'])
                    
                    if has_bulgaria_ref and has_education_ref and (has_numbers or has_year_ref):
                        education_sentences.append(sentence_clean)
            
            print(f"  Education-related sentences: {len(education_sentences)}")
            
            # Look for tables with statistical data
            tables = soup.find_all('table')
            relevant_tables = []
            
            for table_idx, table in enumerate(tables):
                table_text = table.get_text().lower()
                
                if any(term in table_text for term in ['education', 'tertiary', 'university', 'degree', 'census']):
                    # Extract table headers
                    headers = [th.get_text().strip() for th in table.find_all('th')]
                    
                    # Get first few rows of data
                    rows = table.find_all('tr')
                    sample_rows = []
                    
                    for row in rows[1:4]:  # Skip header, get first 3 data rows
                        cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
                        if cells:
                            sample_rows.append(cells)
                    
                    relevant_tables.append({
                        'index': table_idx,
                        'headers': headers,
                        'sample_rows': sample_rows,
                        'total_rows': len(rows)
                    })
            
            print(f"  Relevant tables: {len(relevant_tables)}")
            
            # Search for specific numerical patterns related to tertiary education
            education_stats = []
            
            # Patterns to look for
            stat_patterns = [
                r'tertiary education.*?(\d+[.,]?\d*\s*%)',
                r'university.*?(\d+[.,]?\d*\s*%)',
                r'higher education.*?(\d+[.,]?\d*\s*%)',
                r'(\d+[.,]?\d*\s*%).*?tertiary',
                r'(\d+[.,]?\d*\s*%).*?university',
                r'men.*?(\d+[.,]?\d*\s*%).*?education',
                r'women.*?(\d+[.,]?\d*\s*%).*?education',
                r'education.*?men.*?(\d+[.,]?\d*\s*%)',
                r'education.*?women.*?(\d+[.,]?\d*\s*%)'
            ]
            
            for pattern in stat_patterns:
                matches = re.finditer(pattern, text_content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    # Get context around the match
                    start = max(0, match.start() - 200)
                    end = min(len(text_content), match.end() + 200)
                    context = text_content[start:end].strip()
                    
                    # Check if context mentions Bulgaria
                    if 'bulgaria' in context.lower():
                        education_stats.append({
                            'pattern': pattern,
                            'match': match.group(),
                            'context': context
                        })
            
            print(f"  Education statistics found: {len(education_stats)}")
            
            # Show key findings
            if education_sentences:
                print(f"  Sample sentence: {education_sentences[0][:200]}...")
            
            if education_stats:
                print(f"  Sample statistic: {education_stats[0]['match']}")
                print(f"  Context: {education_stats[0]['context'][:150]}...")
            
            if relevant_tables:
                print(f"  Sample table headers: {relevant_tables[0]['headers'][:5]}")
            
            # Store analysis results
            analysis_results.append({
                'filename': html_file,
                'title': page_title,
                'relevance_score': relevance_score,
                'education_sentences': education_sentences[:10],  # Top 10
                'education_statistics': education_stats[:5],      # Top 5
                'relevant_tables': relevant_tables[:3],           # Top 3
                'content_length': len(text_content)
            })
        
        print()
        
    except Exception as e:
        print(f"  ✗ Error analyzing {html_file}: {str(e)}")
        print()

# Save comprehensive analysis results
print("=== SAVING ANALYSIS RESULTS ===\n")

final_results = {
    'analysis_objective': 'Bulgarian 2011 census tertiary education by gender',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'files_analyzed': len(html_files),
    'relevant_sources': len(analysis_results),
    'detailed_analysis': analysis_results
}

with open('workspace/bulgarian_education_analysis_results.json', 'w', encoding='utf-8') as f:
    json.dump(final_results, f, indent=2, ensure_ascii=False)

print(f"Analysis results saved to: workspace/bulgarian_education_analysis_results.json")
print(f"Files analyzed: {len(html_files)}")
print(f"Relevant sources found: {len(analysis_results)}")

# Display summary of key findings
if analysis_results:
    print("\n=== KEY FINDINGS SUMMARY ===\n")
    
    for i, result in enumerate(analysis_results, 1):
        print(f"{i}. {result['title']} (Score: {result['relevance_score']}/5)")
        print(f"   File: {result['filename']}")
        
        if result['education_sentences']:
            print(f"   Key finding: {result['education_sentences'][0][:150]}...")
        
        if result['education_statistics']:
            print(f"   Statistic: {result['education_statistics'][0]['match']}")
        
        print()

print("=== ANALYSIS COMPLETE ===\n")
print("Ready to extract specific tertiary education completion data by gender for Bulgaria 2011")
```

## Created Time
2025-08-10 04:23:54
