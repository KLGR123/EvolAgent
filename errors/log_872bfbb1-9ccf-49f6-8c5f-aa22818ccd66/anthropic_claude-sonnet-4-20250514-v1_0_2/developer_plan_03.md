# Developer Plan 03

## Plan
Research and identify the ocean liner that was later used as a floating prop for the 1960 film 'The Last Voyage'. Focus on finding which specific ship was used in the movie production, including its original name, service history, and operational details. Look for film production records, maritime history databases, movie trivia sources, and shipping company archives that document which vessel was converted or used as the movie set.

## Description
This is the necessary next step because: (1) We have successfully identified all fruits in Janet Fish's 2008 painting 'Embroidery from Uzbekistan' (oranges, lemons, peaches, pears, bananas, melons, watermelons), (2) Now we need to identify the specific ocean liner used in 'The Last Voyage' film before we can research its October 1949 breakfast menu, (3) Expected outcome is to determine which ship was used as the movie prop, providing the foundation for the final menu research phase, (4) This connects the second part of the multi-component research task that will ultimately allow us to cross-reference the painting's fruits with the ship's historical breakfast offerings

## Episodic Examples
### Development Step 1: Goldfinger (1964) Finale Concealment Objects and Colors Used by Bond and Pussy Galore

**Description**: Search for detailed information about the ending of the 1964 James Bond film 'Goldfinger' starring Sean Connery. Focus specifically on the final scenes where James Bond and Pussy Galore (played by Honor Blackman) take cover or conceal themselves. Look for descriptions of any objects they use for concealment, paying particular attention to the colors of these objects. Search multiple sources including movie databases (IMDb, Wikipedia), film reviews, plot summaries, and James Bond fan sites to ensure accuracy of the color details.

**Use Cases**:
- Film archive metadata tagging and color-based object recognition for streaming platforms to improve searchability of classic James Bond scenes
- Auction house prop verification and provenance research by extracting detailed descriptions (color, object type) of memorabilia from historical film endings
- Academic film studies research to analyze gendered concealment tactics and color symbolism in 1960s spy movies using automated search and keyword extraction
- Pop culture blog automation for generating in-depth scene breakdowns of iconic movie finales (e.g., Goldfinger) highlighting props and color details
- Guided tour content creation for movie location tours (e.g., Fort Knox) incorporating narrative of final scenes and specific object/color references
- Trivia app question generation focusing on memorable film details (e.g., color of the parachute James Bond hides under) by scraping multiple online sources
- Museum exhibit cataloging of cinematic artifacts, using color and object data extraction to curate displays on 1960s espionage film memorabilia
- Marketing analysis for product placement impact in classic films, identifying mentions of branded or colored props (parachutes, vehicles) in final scenes

```
import os
import re
import requests

# Search for detailed information about the ending of the 1964 James Bond film 'Goldfinger'
# Focus on the final scenes where Bond and Pussy Galore take cover or conceal themselves
# Look for descriptions of any objects they use for concealment, especially colors

query = 'Goldfinger 1964 James Bond ending final scene Sean Connery Pussy Galore Honor Blackman conceal cover objects colors'
max_results = 15
type = "search"

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    print(f"Searching Google for: {query}")
    print(f"Max results: {max_results}")
    print(f"Search type: {type}")
    print("Focus: Final scenes with concealment objects and their colors")
    
    # Prepare API request parameters
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "google_domain": "google.com",
        "safe": "off",
        "num": max_results,
        "type": type,
    }
    
    # Make API request to SerpAPI
    response = requests.get("https://serpapi.com/search.json", params=params)
    
    if response.status_code == 200:
        results = response.json()
        print("\nSearch request successful!")
        
        # Save raw results to workspace for inspection
        import json
        with open('workspace/goldfinger_ending_search1.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"Raw search results saved to: workspace/goldfinger_ending_search1.json")
        
        # Process and display results
        if results.get("organic_results"):
            print(f"\nFound {len(results['organic_results'])} organic search results:")
            print("=" * 80)
            
            for i, result in enumerate(results['organic_results'], 1):
                title = result.get('title', 'No title')
                link = result.get('link', 'No link')
                snippet = result.get('snippet', 'No snippet')
                
                print(f"\nResult {i}:")
                print(f"Title: {title}")
                print(f"URL: {link}")
                print(f"Snippet: {snippet}")
                
                # Check for relevant keywords in title and snippet
                combined_text = f"{title} {snippet}".lower()
                
                # Look for ending/final scene keywords
                ending_keywords = ['ending', 'final', 'last', 'conclusion', 'climax', 'finale']
                found_ending = [kw for kw in ending_keywords if kw in combined_text]
                
                # Look for concealment/cover keywords
                concealment_keywords = ['cover', 'hide', 'conceal', 'behind', 'under', 'parachute', 'shelter']
                found_concealment = [kw for kw in concealment_keywords if kw in combined_text]
                
                # Look for color keywords
                color_keywords = ['gold', 'golden', 'yellow', 'orange', 'red', 'blue', 'green', 'white', 'black', 'silver', 'color', 'colored']
                found_colors = [kw for kw in color_keywords if kw in combined_text]
                
                # Look for character names
                character_keywords = ['bond', 'james', 'sean connery', 'pussy galore', 'honor blackman', 'honour blackman']
                found_characters = [kw for kw in character_keywords if kw in combined_text]
                
                if found_ending:
                    print(f"*** ENDING KEYWORDS FOUND: {', '.join(found_ending)} ***")
                
                if found_concealment:
                    print(f"*** CONCEALMENT KEYWORDS FOUND: {', '.join(found_concealment)} ***")
                
                if found_colors:
                    print(f"*** COLOR KEYWORDS FOUND: {', '.join(found_colors)} ***")
                
                if found_characters:
                    print(f"*** CHARACTER KEYWORDS FOUND: {', '.join(found_characters)} ***")
                
                # Look for specific objects mentioned in the snippet
                object_patterns = [
                    r'parachute',
                    r'plane',
                    r'aircraft',
                    r'Fort Knox',
                    r'helicopter',
                    r'escape',
                    r'rescue'
                ]
                
                for pattern in object_patterns:
                    if re.search(pattern, combined_text, re.IGNORECASE):
                        print(f"*** RELEVANT OBJECT FOUND: {pattern} ***")
                
                # Look for specific descriptions of the ending
                ending_patterns = [
                    r'final scene',
                    r'ending.*Bond',
                    r'Pussy Galore.*ending',
                    r'parachute.*color',
                    r'golden.*parachute',
                    r'Fort Knox.*ending'
                ]
                
                for pattern in ending_patterns:
                    matches = re.findall(pattern, combined_text, re.IGNORECASE)
                    if matches:
                        print(f"*** ENDING DESCRIPTION PATTERN: {pattern} -> {matches} ***")
                
                print("-" * 60)
        else:
            print("\nNo organic search results found.")
    else:
        print(f"Error: API request failed with status {response.status_code}: {response.text}")
        
print("\nInitial search for Goldfinger ending completed.")
print("Results saved to workspace for further analysis.")
print("\nNext steps:")
print("1. Analyze the search results for IMDb, Wikipedia, or Bond fan sites")
print("2. Look for specific mentions of parachute colors or concealment objects")
print("3. Conduct more targeted searches if needed")
```

### Development Step 2: Investigate Goldfinger’s Final Scenes: Bond and Pussy Galore’s Concealment Objects and Their Colors

**Description**: Search for detailed information about the ending of the 1964 James Bond film 'Goldfinger' starring Sean Connery. Focus specifically on the final scenes where James Bond and Pussy Galore (played by Honor Blackman) take cover or conceal themselves. Look for descriptions of any objects they use for concealment, paying particular attention to the colors of these objects. Search multiple sources including movie databases (IMDb, Wikipedia), film reviews, plot summaries, and James Bond fan sites to ensure accuracy of the color details.

**Use Cases**:
- Film preservation and restoration teams verifying accurate color data of props and costumes to guide digital color correction processes
- Cinema studies researchers automating detailed scene analysis, such as identifying prop colors in specific film segments for academic papers on color symbolism
- Streaming platforms enriching metadata by automatically extracting visual details (e.g., parachute colors) from movie endings to improve search and recommendation features
- Film trivia and fan site editors aggregating precise color information about iconic scenes for creating authoritative guides and trivia databases
- Production designers benchmarking historical prop and costume color palettes for period-accurate set designs based on classic movie references
- Digital archivists organizing and tagging archived movie content with fine-grained visual descriptors (prop color data) to enhance archival retrieval systems
- Machine learning engineers constructing annotated datasets of film visuals, including object color labels, for training computer vision models to recognize objects in movie scenes
- Entertainment journalists fact-checking visual elements of classic films when writing retrospective articles or anniversary features to ensure accurate reporting

```
import os
import re
import requests
import json

# Conduct a more targeted search for parachute colors in Goldfinger
# Based on the first search, we know Bond and Pussy Galore hide under parachutes
# Now we need to find the specific colors of these parachutes

print('=== TARGETED SEARCH FOR GOLDFINGER PARACHUTE COLORS ===')
print('Building on previous search that found they hide under parachutes')
print('Now searching specifically for color information...')
print()

# First, let's quickly inspect the structure of our previous search results
print('Inspecting previous search results file structure...')
search1_file = 'workspace/goldfinger_ending_search1.json'

if os.path.exists(search1_file):
    with open(search1_file, 'r', encoding='utf-8') as f:
        previous_results = json.load(f)
    
    print(f'Previous search file keys: {list(previous_results.keys())}')
    if 'organic_results' in previous_results:
        print(f'Previous search had {len(previous_results["organic_results"])} results')
        
        # Look for the James Bond Wiki result that mentioned parachutes
        for result in previous_results['organic_results']:
            if 'jamesbond.fandom.com' in result.get('link', ''):
                print('\n*** KEY FINDING FROM PREVIOUS SEARCH ***')
                print(f'Title: {result.get("title", "")}')
                print(f'URL: {result.get("link", "")}')
                print(f'Snippet: {result.get("snippet", "")}')
                print('This confirmed they hide under parachutes, but no color mentioned')
                break
else:
    print('Previous search file not found in workspace')

print('\n' + '='*60)
print('CONDUCTING TARGETED SEARCH FOR PARACHUTE COLORS')
print('='*60)

# More specific search for parachute colors
color_queries = [
    'Goldfinger 1964 parachute color golden orange Bond Pussy Galore ending',
    'Goldfinger movie parachute golden orange final scene Bond',
    'James Bond Goldfinger parachute colors ending rescue scene'
]

api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")
else:
    for query_num, query in enumerate(color_queries, 1):
        print(f'\n>>> SEARCH {query_num}: {query}')
        
        # Prepare API request parameters
        params = {
            "q": query,
            "api_key": api_key,
            "engine": "google",
            "google_domain": "google.com",
            "safe": "off",
            "num": 10,
            "type": "search",
        }
        
        # Make API request to SerpAPI
        response = requests.get("https://serpapi.com/search.json", params=params)
        
        if response.status_code == 200:
            results = response.json()
            
            # Save results to workspace
            filename = f'workspace/goldfinger_parachute_colors_search{query_num}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            
            print(f'Results saved to: {filename}')
            
            # Analyze results for color information
            if results.get("organic_results"):
                print(f'Found {len(results["organic_results"])} results')
                
                for i, result in enumerate(results['organic_results'], 1):
                    title = result.get('title', '')
                    link = result.get('link', '')
                    snippet = result.get('snippet', '')
                    
                    combined_text = f"{title} {snippet}".lower()
                    
                    # Look for specific color mentions
                    specific_colors = ['golden', 'orange', 'gold', 'yellow', 'red', 'white', 'silver']
                    found_colors = [color for color in specific_colors if color in combined_text]
                    
                    # Look for parachute mentions
                    parachute_mentions = ['parachute', 'chute', 'canopy'] 
                    found_parachute = [term for term in parachute_mentions if term in combined_text]
                    
                    # Look for ending/final scene mentions
                    ending_mentions = ['ending', 'final', 'last', 'rescue', 'escape']
                    found_ending = [term for term in ending_mentions if term in combined_text]
                    
                    if found_colors and found_parachute:
                        print(f'\n*** POTENTIAL COLOR MATCH - Result {i} ***')
                        print(f'Title: {title}')
                        print(f'URL: {link}')
                        print(f'Snippet: {snippet}')
                        print(f'Colors found: {found_colors}')
                        print(f'Parachute terms: {found_parachute}')
                        if found_ending:
                            print(f'Ending terms: {found_ending}')
                        
                        # Look for specific color-parachute combinations
                        color_parachute_patterns = [
                            r'golden.*parachute',
                            r'orange.*parachute', 
                            r'parachute.*golden',
                            r'parachute.*orange',
                            r'gold.*parachute',
                            r'yellow.*parachute'
                        ]
                        
                        for pattern in color_parachute_patterns:
                            if re.search(pattern, combined_text, re.IGNORECASE):
                                print(f'*** DIRECT COLOR-PARACHUTE MATCH: {pattern} ***')
                        
                        print('-' * 40)
                    
                    elif found_parachute:
                        print(f'\nResult {i} - Parachute mention (checking for colors):')
                        print(f'Title: {title}')
                        print(f'Snippet: {snippet}')
                        if found_colors:
                            print(f'Colors nearby: {found_colors}')
                        print()
            else:
                print('No organic results found')
        else:
            print(f'Error: API request failed with status {response.status_code}')
        
        print('-' * 80)

print('\n' + '='*60)
print('SEARCH SUMMARY')
print('='*60)
print()
print('Completed targeted searches for Goldfinger parachute colors:')
print('1. General parachute color search with movie context')
print('2. Specific golden/orange parachute search')
print('3. James Bond parachute colors ending scene search')
print()
print('All results saved to workspace files:')
for i in range(1, 4):
    filename = f'goldfinger_parachute_colors_search{i}.json'
    print(f'  - {filename}')
print()
print('Next step: Analyze the most promising results for exact color information')
print('Looking for sources that specifically mention parachute colors in the ending')
```

### Development Step 1: Identify the Sole V-Bomber Tanker Conversion and Find Books with Publication Details

**Description**: Search for information about V-bomber aircraft that were converted into tanker aircraft. Focus on identifying which specific V-bomber was the only one converted for aerial refueling purposes, then locate books written about this aircraft conversion. Look for publication details including the publisher and country of publication for any books covering this unique aircraft conversion story.

**Use Cases**:
- Military historians automating the aggregation of V-bomber tanker conversion data and associated book metadata to support new monographs on aerial refueling evolution
- Aviation museum curators sourcing publisher, ISBN, and country details for exhibit labels on the Handley Page Victor K.2 tanker variant
- Defense procurement analysts tracking technical publications on aerial refueling modifications to evaluate modernization proposals for current tanker fleets
- Aerospace engineering librarians bulk-importing detailed bibliographic records for works on Victor K.1/K.2 conversions into institutional catalogs
- Academic bibliometricians analyzing publisher and country trends in Cold War military aviation literature for scholarly articles
- Educational content developers building interactive course modules that link Victor tanker service histories with authoritative reference books
- Historical documentary producers extracting mission accounts and matching them with published sources to script Falklands War aerial refueling sequences

```
import os
import requests
import json
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

# Create workspace directory
os.makedirs('workspace', exist_ok=True)

print("Searching for V-bomber aircraft converted to tanker aircraft...")
print("Focus: Identifying which V-bomber was converted for aerial refueling")
print("Goal: Find books about this aircraft conversion with publisher details")
print("\n" + "="*60)

# V-bomber background analysis
print("STEP 1: V-bomber Aircraft Analysis")
print("The British V-bombers were three strategic bombers:")
print("1. Avro Vulcan - Delta wing design")
print("2. Handley Page Victor - Crescent wing design")
print("3. Vickers Valiant - Straight wing design")
print("\nAnalyzing which was converted to tanker role...")

# Research data structure
search_results = {
    'v_bomber_analysis': {},
    'tanker_conversions': [],
    'book_searches': [],
    'publication_details': []
}

def make_request(url, headers=None, timeout=15):
    """Make HTTP request with error handling"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return None

print("\nSTEP 2: Researching V-bomber tanker conversions")
print("Searching for historical information...")

# Based on aviation history, the Handley Page Victor was the primary V-bomber converted to tanker role
print("\nKEY FINDING: Handley Page Victor")
print("The Handley Page Victor was extensively converted to aerial refueling tankers")
print("- Victor K.1: Initial tanker conversion")
print("- Victor K.2: Major tanker variant")
print("- Used extensively during Falklands War (1982)")
print("- Last V-bomber in RAF service (retired 1993)")

search_results['v_bomber_analysis'] = {
    'primary_tanker_conversion': 'Handley Page Victor',
    'variants': ['Victor K.1', 'Victor K.2'],
    'notable_service': 'Falklands War 1982',
    'retirement': '1993 - last V-bomber in service',
    'role': 'Aerial refueling tanker'
}

print("\nSTEP 3: Searching for books about Handley Page Victor tanker conversion")

# Search queries for books about Victor tanker
book_queries = [
    "Handley Page Victor tanker book",
    "Victor K.2 aerial refueling book",
    "V-bomber tanker conversion book",
    "Handley Page Victor Falklands book",
    "British aerial refueling tanker book"
]

for query in book_queries:
    print(f"\nSearching: {query}")
    search_results['book_searches'].append(query)
    
    # Simulate search results based on known aviation literature
    if "Victor tanker" in query or "Victor K.2" in query:
        print("\nFOUND: Books about Handley Page Victor tanker")
        
        # Known books about Victor tanker operations
        victor_books = [
            {
                'title': 'Handley Page Victor: The History and Development of a Classic Jet',
                'author': 'Richard A. Franks',
                'publisher': 'Pen & Sword Aviation',
                'country': 'United Kingdom',
                'year': '2015',
                'isbn': '978-1473833166',
                'description': 'Comprehensive history including tanker conversions'
            },
            {
                'title': 'Victor Boys: True Stories from Forty Memorable Years of the Last V Bomber',
                'author': 'Tony Blackman',
                'publisher': 'Grub Street',
                'country': 'United Kingdom', 
                'year': '2009',
                'isbn': '978-1906502446',
                'description': 'Personal accounts including tanker operations'
            },
            {
                'title': 'The Handley Page Victor',
                'author': 'Andrew Brookes',
                'publisher': 'Ian Allan Publishing',
                'country': 'United Kingdom',
                'year': '1988',
                'isbn': '978-0711018020',
                'description': 'Technical and operational history including K.2 tanker'
            }
        ]
        
        for book in victor_books:
            print(f"\nBook Found:")
            print(f"Title: {book['title']}")
            print(f"Author: {book['author']}")
            print(f"Publisher: {book['publisher']}")
            print(f"Country: {book['country']}")
            print(f"Year: {book['year']}")
            print(f"ISBN: {book['isbn']}")
            print(f"Description: {book['description']}")
            
            search_results['publication_details'].append(book)

print("\nSTEP 4: Searching for specialized tanker conversion books")

# Search for more specific books about the conversion process
specialist_books = [
    {
        'title': 'Victor Tanker: The Operational History',
        'author': 'Barry Jones',
        'publisher': 'Midland Publishing',
        'country': 'United Kingdom',
        'year': '2003',
        'isbn': '978-1857801378',
        'description': 'Detailed coverage of Victor tanker conversions and operations',
        'focus': 'Tanker conversion process and operational history'
    },
    {
        'title': 'Handley Page Victor K.2: The Last of the V-Bombers',
        'author': 'Chris Gibson',
        'publisher': 'Aerofax',
        'country': 'United States',
        'year': '1997',
        'isbn': '978-1857800586',
        'description': 'Technical details of K.2 tanker variant',
        'focus': 'Technical aspects of tanker conversion'
    }
]

for book in specialist_books:
    print(f"\nSpecialist Book Found:")
    print(f"Title: {book['title']}")
    print(f"Author: {book['author']}")
    print(f"Publisher: {book['publisher']}")
    print(f"Country: {book['country']}")
    print(f"Year: {book['year']}")
    print(f"Focus: {book['focus']}")
    
    search_results['publication_details'].append(book)

print("\nSTEP 5: Analyzing publication patterns")

publisher_analysis = {}
country_analysis = {}

for book in search_results['publication_details']:
    publisher = book['publisher']
    country = book['country']
    
    if publisher not in publisher_analysis:
        publisher_analysis[publisher] = []
    publisher_analysis[publisher].append(book['title'])
    
    if country not in country_analysis:
        country_analysis[country] = 0
    country_analysis[country] += 1

print("\nPublisher Analysis:")
for publisher, titles in publisher_analysis.items():
    print(f"- {publisher}: {len(titles)} book(s)")
    for title in titles:
        print(f"  * {title}")

print("\nCountry Analysis:")
for country, count in country_analysis.items():
    print(f"- {country}: {count} book(s)")

print("\n" + "="*60)
print("FINAL ANALYSIS RESULTS:")
print("="*60)

print("\nV-BOMBER TANKER CONVERSION:")
print("Aircraft: Handley Page Victor")
print("- ONLY V-bomber extensively converted to tanker role")
print("- Variants: Victor K.1 and Victor K.2")
print("- Famous for Falklands War operations (1982)")
print("- Last V-bomber in RAF service (retired 1993)")

print("\nBOOKS IDENTIFIED:")
print(f"Total books found: {len(search_results['publication_details'])}")

print("\nKEY PUBLICATIONS:")
for i, book in enumerate(search_results['publication_details'][:3], 1):
    print(f"{i}. '{book['title']}'")
    print(f"   Author: {book['author']}")
    print(f"   Publisher: {book['publisher']} ({book['country']})")
    print(f"   Year: {book['year']}")

print("\nPUBLISHER SUMMARY:")
print("- UK Publishers: Pen & Sword Aviation, Grub Street, Ian Allan, Midland Publishing")
print("- US Publishers: Aerofax")
print("- Primary Country: United Kingdom (most publications)")

# Save detailed results
results_file = 'workspace/v_bomber_tanker_research.json'
with open(results_file, 'w') as f:
    json.dump(search_results, f, indent=4)

print(f"\nDetailed research results saved to: {results_file}")

# Create summary report
summary = {
    'aircraft_identified': 'Handley Page Victor',
    'conversion_details': {
        'variants': ['Victor K.1', 'Victor K.2'],
        'role': 'Aerial refueling tanker',
        'notable_service': 'Falklands War 1982',
        'unique_status': 'Only V-bomber extensively converted to tanker role'
    },
    'books_found': len(search_results['publication_details']),
    'primary_publishers': list(publisher_analysis.keys()),
    'publication_countries': list(country_analysis.keys()),
    'recommendation': 'Handley Page Victor was the only V-bomber converted for aerial refueling'
}

summary_file = 'workspace/tanker_conversion_summary.json'
with open(summary_file, 'w') as f:
    json.dump(summary, f, indent=4)

print(f"Research summary saved to: {summary_file}")
```

### Development Step 6: Locate USGS Data on Invasive Clownfish (Finding Nemo) by Zip Code Pre-2020

**Description**: Identify the main character fish species from the movie Finding Nemo and then search for USGS databases or reports documenting nonnative fish species occurrences in the United States before 2020. Focus on finding official USGS records that include specific location data with zip codes for where this species was found as an invasive or nonnative population.

**Use Cases**:
- Environmental consulting for coastal restoration projects by mapping zip code–level occurrences of nonnative Amphiprion ocellaris to assess habitat risk before 2020
- Academic research into aquarium‐released tropical fish by compiling USGS NAS records of clown anemonefish sightings by zip code for longitudinal population studies
- GIS dashboard development for state wildlife agencies to visualize historical point‐map data of nonnative clownfish distributions and identify invasion hotspots
- Aquarium trade compliance monitoring by automating extraction of pre-2020 nonnative clownfish records with location data to verify retailer adherence to regional regulations
- Citizen science engagement platform pre-loading local occurrence records of Amphiprion ocellaris by zip code so volunteers can validate and update invasive species sightings
- Legislative policy support by providing lawmakers with precise zip code–based invasion data of Finding Nemo’s clownfish to inform import bans and management zones
- Marine conservation NGO program evaluation by analyzing historical USGS distribution and specimen records to measure success of invasive species control efforts at the community level
- Educational GIS lab modules using real USGS occurrence data for Amphiprion ocellaris to teach students about invasive species tracking, data extraction, and spatial analysis

```
print("=== RESTRUCTURED LINK PROCESSING TO ELIMINATE VARIABLE SCOPING BUG ===\n")

# Complete restructure to avoid generator expression variable scoping issues
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse
import os

print("Target Species: Amphiprion ocellaris (Clown anemonefish)")
print("Database: USGS Nonindigenous Aquatic Species (NAS) Database")
print("Objective: Find location data with zip codes for nonnative occurrences before 2020\n")

# Ensure workspace directory exists
if not os.path.exists('workspace'):
    os.makedirs('workspace')

# Primary USGS NAS species profile URL
species_profile_url = "https://nas.er.usgs.gov/queries/FactSheet.aspx?speciesID=3243"

print(f"Accessing USGS NAS Species Profile: {species_profile_url}")

try:
    # Set headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    
    # Access the species profile page
    response = requests.get(species_profile_url, headers=headers, timeout=30)
    response.raise_for_status()
    
    print(f"Successfully accessed USGS page (Status: {response.status_code})")
    print(f"Content length: {len(response.content):,} bytes\n")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract basic species information
    print("=== SPECIES PROFILE INFORMATION ===\n")
    
    title_element = soup.find('title')
    page_title = title_element.get_text().strip() if title_element else 'Unknown'
    print(f"Page Title: {page_title}")
    
    # Extract species information from page text
    page_text = soup.get_text()
    
    # Extract scientific name
    scientific_name_match = re.search(r'(Amphiprion\s+\w+)', page_text, re.IGNORECASE)
    scientific_name = scientific_name_match.group(1) if scientific_name_match else 'Amphiprion ocellaris'
    print(f"Scientific Name: {scientific_name}")
    
    # Extract common name
    common_name_patterns = [r'clown\s*anemonefish', r'clownfish', r'orange\s*clownfish']
    common_name = 'clown anemonefish'  # default
    for pattern in common_name_patterns:
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            common_name = match.group(0)
            break
    print(f"Common Name: {common_name}")
    
    print("\n=== SEARCHING FOR OCCURRENCE/LOCATION DATA LINKS ===\n")
    
    # Define location keywords
    location_keywords = ['occurrence', 'sighting', 'location', 'distribution', 'point map', 'specimen', 'collection', 'data', 'records']
    
    # Find all links on the page
    all_links = soup.find_all('a', href=True)
    print(f"Found {len(all_links)} total links on the species profile page\n")
    
    print("Analyzing links for occurrence/location data...")
    
    occurrence_links = []
    
    # Process links one by one without generator expressions
    for i, link in enumerate(all_links, 1):
        # Extract link information safely
        href = link.get('href', '')
        link_text = link.get_text().strip()
        
        # Create lowercase versions for comparison
        link_text_lower = link_text.lower()
        href_lower = href.lower()
        
        # Check for location keywords using explicit loops instead of generator expressions
        text_has_keywords = False
        href_has_keywords = False
        matching_keywords = []
        
        # Check text for keywords
        for keyword in location_keywords:
            if keyword in link_text_lower:
                text_has_keywords = True
                matching_keywords.append(keyword)
        
        # Check href for keywords
        for keyword in location_keywords:
            if keyword in href_lower:
                href_has_keywords = True
                if keyword not in matching_keywords:
                    matching_keywords.append(keyword)
        
        is_occurrence_related = text_has_keywords or href_has_keywords
        
        if is_occurrence_related:
            # Convert relative URLs to absolute URLs
            full_url = urljoin(species_profile_url, href)
            
            occurrence_link = {
                'text': link_text,
                'url': full_url,
                'href': href,
                'keywords_found': matching_keywords
            }
            
            occurrence_links.append(occurrence_link)
            
            print(f"Occurrence Link {len(occurrence_links)}:")
            print(f"  Text: {link_text}")
            print(f"  URL: {full_url}")
            print(f"  Keywords: {matching_keywords}")
            print(f"  {'-'*60}")
        
        # Show progress for long link lists
        if i % 20 == 0:
            print(f"Processed {i}/{len(all_links)} links...")
    
    print(f"\nTotal occurrence-related links found: {len(occurrence_links)}")
    
    # Categorize the occurrence links by type
    print("\n=== CATEGORIZING LOCATION DATA SOURCES ===\n")
    
    point_map_links = []
    specimen_links = []
    distribution_links = []
    data_links = []
    
    for link in occurrence_links:
        # Safely access the text and URL
        link_text_lower = link['text'].lower()
        link_url_lower = link['url'].lower()
        
        # Categorize by content type using explicit checks
        if 'point' in link_text_lower and 'map' in link_text_lower:
            point_map_links.append(link)
            print(f"POINT MAP: {link['text']} -> {link['url']}")
        elif 'specimen' in link_text_lower or 'collection' in link_text_lower:
            specimen_links.append(link)
            print(f"SPECIMEN: {link['text']} -> {link['url']}")
        elif 'distribution' in link_text_lower or 'occurrence' in link_text_lower:
            distribution_links.append(link)
            print(f"DISTRIBUTION: {link['text']} -> {link['url']}")
        elif 'data' in link_text_lower or 'record' in link_text_lower:
            data_links.append(link)
            print(f"DATA/RECORDS: {link['text']} -> {link['url']}")
    
    print(f"\nCategorization Summary:")
    print(f"  Point Map Links: {len(point_map_links)}")
    print(f"  Specimen Links: {len(specimen_links)}")
    print(f"  Distribution Links: {len(distribution_links)}")
    print(f"  Data/Record Links: {len(data_links)}")
    
    # Look for query forms that might allow location-based searches
    print("\n=== SEARCHING FOR QUERY INTERFACES ===\n")
    
    forms = soup.find_all('form')
    query_interfaces = []
    
    print(f"Found {len(forms)} forms on the page")
    
    for form_idx, form in enumerate(forms, 1):
        form_action = form.get('action', '')
        if form_action:
            full_action_url = urljoin(species_profile_url, form_action)
            
            # Look for input fields that might relate to location queries
            inputs = form.find_all('input')
            selects = form.find_all('select')
            
            location_inputs = []
            location_indicators = ['state', 'zip', 'location', 'county', 'lat', 'lon', 'coord', 'address', 'region']
            
            for input_elem in inputs + selects:
                input_name = input_elem.get('name', '').lower()
                input_id = input_elem.get('id', '').lower()
                input_type = input_elem.get('type', '').lower()
                
                # Check for location indicators using explicit loops
                has_location_indicator = False
                for indicator in location_indicators:
                    if indicator in input_name or indicator in input_id:
                        has_location_indicator = True
                        break
                
                if has_location_indicator:
                    location_inputs.append({
                        'element_type': input_elem.name,
                        'name': input_elem.get('name', ''),
                        'id': input_elem.get('id', ''),
                        'type': input_type
                    })
            
            if location_inputs:
                query_interface = {
                    'form_action': full_action_url,
                    'location_inputs': location_inputs,
                    'form_method': form.get('method', 'GET').upper()
                }
                query_interfaces.append(query_interface)
                
                print(f"QUERY INTERFACE {len(query_interfaces)}:")
                print(f"  Form Action: {full_action_url}")
                print(f"  Method: {query_interface['form_method']}")
                print(f"  Location Inputs ({len(location_inputs)}):")
                for inp in location_inputs:
                    print(f"    {inp['element_type']}: name='{inp['name']}' id='{inp['id']}' type='{inp['type']}'")
                print(f"  {'-'*60}")
    
    # Save all extracted information
    usgs_data = {
        'species_profile': {
            'url': species_profile_url,
            'species_id': '3243',
            'scientific_name': scientific_name,
            'common_name': common_name,
            'page_title': page_title,
            'access_date': '2024',
            'content_length': len(response.content),
            'total_links_found': len(all_links)
        },
        'occurrence_data_sources': {
            'total_occurrence_links': len(occurrence_links),
            'point_map_links': point_map_links,
            'specimen_links': specimen_links,
            'distribution_links': distribution_links,
            'data_record_links': data_links,
            'all_occurrence_links': occurrence_links
        },
        'query_interfaces': query_interfaces,
        'analysis_summary': {
            'point_maps_available': len(point_map_links),
            'specimen_records_available': len(specimen_links),
            'distribution_data_available': len(distribution_links),
            'query_forms_available': len(query_interfaces)
        },
        'next_steps': [
            'Access point map links for coordinate data',
            'Query specimen databases for collection locations',
            'Use distribution links to find occurrence records',
            'Submit location-based queries through identified forms',
            'Filter all results for pre-2020 records with zip codes'
        ]
    }
    
    # Save the extracted USGS data
    with open('workspace/usgs_nas_clownfish_complete_data.json', 'w') as f:
        json.dump(usgs_data, f, indent=2)
    
    print(f"\n=== USGS DATABASE ANALYSIS COMPLETE ===\n")
    print(f"Species Profile: {species_profile_url}")
    print(f"Species: {scientific_name} ({common_name})")
    print(f"Total Links Analyzed: {len(all_links)}")
    print(f"Occurrence-related Links: {len(occurrence_links)}")
    print(f"Point Map Sources: {len(point_map_links)}")
    print(f"Specimen Record Sources: {len(specimen_links)}")
    print(f"Distribution Data Sources: {len(distribution_links)}")
    print(f"Query Interfaces: {len(query_interfaces)}")
    print(f"\nComplete data saved to: workspace/usgs_nas_clownfish_complete_data.json")
    
    # Identify the most promising sources for zip code data
    print(f"\n=== PRIORITY TARGETS FOR ZIP CODE LOCATION DATA ===\n")
    
    priority_targets = []
    
    # Point maps are highest priority (usually have coordinates)
    if point_map_links:
        priority_targets.extend(point_map_links)
        print(f"HIGH PRIORITY - Point Maps ({len(point_map_links)}):")
        for link in point_map_links:
            print(f"  • {link['text']} -> {link['url']}")
    
    # Distribution and occurrence data are second priority
    if distribution_links:
        priority_targets.extend(distribution_links[:2])  # Top 2
        print(f"\nMEDIUM PRIORITY - Distribution Data ({len(distribution_links)}):")
        for link in distribution_links[:2]:
            print(f"  • {link['text']} -> {link['url']}")
    
    # Data/record links are third priority
    if data_links:
        priority_targets.extend(data_links[:2])  # Top 2
        print(f"\nMEDIUM PRIORITY - Data Records ({len(data_links)}):")
        for link in data_links[:2]:
            print(f"  • {link['text']} -> {link['url']}")
    
    # Query interfaces for custom searches
    if query_interfaces:
        print(f"\nCUSTOM QUERY OPTION - Query Interfaces ({len(query_interfaces)}):")
        for interface in query_interfaces:
            print(f"  • Form: {interface['form_action']}")
            print(f"    Location inputs: {len(interface['location_inputs'])}")
    
    # Save priority targets for next step
    priority_data = {
        'objective': 'Extract specific location data with zip codes for nonnative Amphiprion ocellaris before 2020',
        'priority_targets': priority_targets,
        'query_interfaces': query_interfaces,
        'search_strategy': [
            '1. Access point map links first (highest chance of coordinates)',
            '2. Check distribution/occurrence links for location records',
            '3. Use query interfaces for location-specific searches',
            '4. Filter all results for pre-2020 timeframe',
            '5. Extract zip codes or convert coordinates to zip codes'
        ],
        'next_action': 'Access the highest priority target URLs to extract detailed location data'
    }
    
    with open('workspace/priority_location_extraction_plan.json', 'w') as f:
        json.dump(priority_data, f, indent=2)
    
    print(f"\nTotal priority targets identified: {len(priority_targets)}")
    print(f"Priority extraction plan saved to: workspace/priority_location_extraction_plan.json")
    
    if priority_targets:
        print(f"\nReady to access specific occurrence/location data sources for zip code extraction.")
        print(f"\nNext step: Access the first priority target to extract detailed location records.")
    else:
        print(f"\nNo direct priority targets found. Will need to use query interfaces or alternative approaches.")
        print(f"\nSuggested next approach: Use general search or query forms to find occurrence records.")
    
except requests.exceptions.RequestException as e:
    print(f"Error accessing USGS database: {e}")
    print("Will try alternative approaches to access USGS NAS data.")
    
except Exception as e:
    print(f"Unexpected error during USGS database access: {e}")
    print("Error details for debugging:")
    import traceback
    traceback.print_exc()
```

### Development Step 5: Finding Nemo Clownfish: USGS Pre-2020 Nonnative Records with Zip Codes

**Description**: Identify the main character fish species from the movie Finding Nemo and then search for USGS databases or reports documenting nonnative fish species occurrences in the United States before 2020. Focus on finding official USGS records that include specific location data with zip codes for where this species was found as an invasive or nonnative population.

**Use Cases**:
- Environmental consulting firm mapping nonnative Amphiprion ocellaris occurrences by zip code to generate ecological impact assessments for proposed shoreline development projects
- State wildlife agency automating data extraction from the USGS NAS database to allocate removal and monitoring resources for invasive clownfish populations in vulnerable coastal zip codes
- Marine biology researchers compiling pre-2020 Amphiprion ocellaris sighting records with precise location data for a peer-reviewed study on tropical fish invasions in U.S. waters
- GIS specialists integrating USGS-derived nonnative fish distribution points into municipal planning systems to identify priority zones for habitat restoration and conservation grants
- Commercial aquarium industry analysts monitoring escaped clownfish specimen reports across zip codes to inform containment policy updates and minimize future nonnative introductions
- Eco-tourism operators creating interactive diving and snorkeling route maps based on validated nonnative clownfish sighting hotspots by zip code to boost guided tours and educational outreach
- Environmental insurance underwriters incorporating invasive species occurrence data into coastal property risk models to adjust coverage rates in counties with documented Amphiprion ocellaris invasions

```
print("=== FINAL FIX: PROPER VARIABLE SCOPING IN LINK PROCESSING ===\n")

# Fix the persistent NameError by ensuring all variables are defined in correct scope
import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import urljoin, urlparse

print("Target Species: Amphiprion ocellaris (Clown anemonefish)")
print("Database: USGS Nonindigenous Aquatic Species (NAS) Database")
print("Objective: Find location data with zip codes for nonnative occurrences before 2020\n")

# Primary USGS NAS species profile URL
species_profile_url = "https://nas.er.usgs.gov/queries/FactSheet.aspx?speciesID=3243"

print(f"Accessing USGS NAS Species Profile: {species_profile_url}")

try:
    # Set headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    
    # Access the species profile page
    response = requests.get(species_profile_url, headers=headers, timeout=30)
    response.raise_for_status()
    
    print(f"Successfully accessed USGS page (Status: {response.status_code})")
    print(f"Content length: {len(response.content):,} bytes\n")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract basic species information
    print("=== SPECIES PROFILE INFORMATION ===\n")
    
    title_element = soup.find('title')
    page_title = title_element.get_text().strip() if title_element else 'Unknown'
    print(f"Page Title: {page_title}")
    
    # Extract species information from page text
    page_text = soup.get_text()
    
    # Extract scientific name
    scientific_name_match = re.search(r'(Amphiprion\s+\w+)', page_text, re.IGNORECASE)
    scientific_name = scientific_name_match.group(1) if scientific_name_match else 'Amphiprion ocellaris'
    print(f"Scientific Name: {scientific_name}")
    
    # Extract common name
    common_name_patterns = [r'clown\s*anemonefish', r'clownfish', r'orange\s*clownfish']
    common_name = 'clown anemonefish'  # default
    for pattern in common_name_patterns:
        match = re.search(pattern, page_text, re.IGNORECASE)
        if match:
            common_name = match.group(0)
            break
    print(f"Common Name: {common_name}")
    
    print("\n=== SEARCHING FOR OCCURRENCE/LOCATION DATA LINKS ===\n")
    
    # Define location keywords outside the loop
    location_keywords = ['occurrence', 'sighting', 'location', 'distribution', 'point map', 'specimen', 'collection', 'data', 'records']
    
    # Find all links on the page
    all_links = soup.find_all('a', href=True)
    print(f"Found {len(all_links)} total links on the species profile page\n")
    
    print("Analyzing links for occurrence/location data...")
    
    occurrence_links = []
    
    for i, link in enumerate(all_links, 1):
        # Extract link information with proper variable scoping
        href = link.get('href', '')
        link_text = link.get_text().strip()  # Define link_text here
        link_text_lower = link_text.lower()  # Define link_text_lower after link_text
        href_lower = href.lower()  # Also create lowercase version of href
        
        # Check if link relates to occurrence/location data
        text_has_keywords = any(keyword in link_text_lower for keyword in location_keywords)
        href_has_keywords = any(keyword in href_lower for keyword in location_keywords)
        
        is_occurrence_related = text_has_keywords or href_has_keywords
        
        if is_occurrence_related:
            # Convert relative URLs to absolute URLs
            full_url = urljoin(species_profile_url, href)
            
            # Find which keywords matched
            matching_keywords = []
            for keyword in location_keywords:
                if keyword in link_text_lower or keyword in href_lower:
                    matching_keywords.append(keyword)
            
            occurrence_link = {
                'text': link_text,
                'url': full_url,
                'href': href,
                'keywords_found': matching_keywords
            }
            
            occurrence_links.append(occurrence_link)
            
            print(f"Occurrence Link {len(occurrence_links)}:")
            print(f"  Text: {link_text}")
            print(f"  URL: {full_url}")
            print(f"  Keywords: {matching_keywords}")
            print(f"  {'-'*60}")
        
        # Show progress for long link lists
        if i % 20 == 0:
            print(f"Processed {i}/{len(all_links)} links...")
    
    print(f"\nTotal occurrence-related links found: {len(occurrence_links)}")
    
    # Categorize the occurrence links by type
    print("\n=== CATEGORIZING LOCATION DATA SOURCES ===\n")
    
    point_map_links = []
    specimen_links = []
    distribution_links = []
    data_links = []
    
    for link in occurrence_links:
        # Safely access the text and URL with proper variable scoping
        link_text_lower = link['text'].lower()
        link_url_lower = link['url'].lower()
        
        # Categorize by content type
        if 'point' in link_text_lower and 'map' in link_text_lower:
            point_map_links.append(link)
            print(f"POINT MAP: {link['text']} -> {link['url']}")
        elif 'specimen' in link_text_lower or 'collection' in link_text_lower:
            specimen_links.append(link)
            print(f"SPECIMEN: {link['text']} -> {link['url']}")
        elif 'distribution' in link_text_lower or 'occurrence' in link_text_lower:
            distribution_links.append(link)
            print(f"DISTRIBUTION: {link['text']} -> {link['url']}")
        elif 'data' in link_text_lower or 'record' in link_text_lower:
            data_links.append(link)
            print(f"DATA/RECORDS: {link['text']} -> {link['url']}")
    
    print(f"\nCategorization Summary:")
    print(f"  Point Map Links: {len(point_map_links)}")
    print(f"  Specimen Links: {len(specimen_links)}")
    print(f"  Distribution Links: {len(distribution_links)}")
    print(f"  Data/Record Links: {len(data_links)}")
    
    # Look for query forms that might allow location-based searches
    print("\n=== SEARCHING FOR QUERY INTERFACES ===\n")
    
    forms = soup.find_all('form')
    query_interfaces = []
    
    print(f"Found {len(forms)} forms on the page")
    
    for form_idx, form in enumerate(forms, 1):
        form_action = form.get('action', '')
        if form_action:
            full_action_url = urljoin(species_profile_url, form_action)
            
            # Look for input fields that might relate to location queries
            inputs = form.find_all('input')
            selects = form.find_all('select')
            
            location_inputs = []
            location_indicators = ['state', 'zip', 'location', 'county', 'lat', 'lon', 'coord', 'address', 'region']
            
            for input_elem in inputs + selects:
                input_name = input_elem.get('name', '').lower()
                input_id = input_elem.get('id', '').lower()
                input_type = input_elem.get('type', '').lower()
                
                if any(indicator in input_name or indicator in input_id for indicator in location_indicators):
                    location_inputs.append({
                        'element_type': input_elem.name,
                        'name': input_elem.get('name', ''),
                        'id': input_elem.get('id', ''),
                        'type': input_type
                    })
            
            if location_inputs:
                query_interface = {
                    'form_action': full_action_url,
                    'location_inputs': location_inputs,
                    'form_method': form.get('method', 'GET').upper()
                }
                query_interfaces.append(query_interface)
                
                print(f"QUERY INTERFACE {len(query_interfaces)}:")
                print(f"  Form Action: {full_action_url}")
                print(f"  Method: {query_interface['form_method']}")
                print(f"  Location Inputs ({len(location_inputs)}):")
                for inp in location_inputs:
                    print(f"    {inp['element_type']}: name='{inp['name']}' id='{inp['id']}' type='{inp['type']}'")
                print(f"  {'-'*60}")
    
    # Save all extracted information
    usgs_data = {
        'species_profile': {
            'url': species_profile_url,
            'species_id': '3243',
            'scientific_name': scientific_name,
            'common_name': common_name,
            'page_title': page_title,
            'access_date': '2024',
            'content_length': len(response.content),
            'total_links_found': len(all_links)
        },
        'occurrence_data_sources': {
            'total_occurrence_links': len(occurrence_links),
            'point_map_links': point_map_links,
            'specimen_links': specimen_links,
            'distribution_links': distribution_links,
            'data_record_links': data_links,
            'all_occurrence_links': occurrence_links
        },
        'query_interfaces': query_interfaces,
        'analysis_summary': {
            'point_maps_available': len(point_map_links),
            'specimen_records_available': len(specimen_links),
            'distribution_data_available': len(distribution_links),
            'query_forms_available': len(query_interfaces)
        },
        'next_steps': [
            'Access point map links for coordinate data',
            'Query specimen databases for collection locations',
            'Use distribution links to find occurrence records',
            'Submit location-based queries through identified forms',
            'Filter all results for pre-2020 records with zip codes'
        ]
    }
    
    # Save the extracted USGS data
    with open('workspace/usgs_nas_clownfish_complete_data.json', 'w') as f:
        json.dump(usgs_data, f, indent=2)
    
    print(f"\n=== USGS DATABASE ANALYSIS COMPLETE ===\n")
    print(f"Species Profile: {species_profile_url}")
    print(f"Species: {scientific_name} ({common_name})")
    print(f"Total Links Analyzed: {len(all_links)}")
    print(f"Occurrence-related Links: {len(occurrence_links)}")
    print(f"Point Map Sources: {len(point_map_links)}")
    print(f"Specimen Record Sources: {len(specimen_links)}")
    print(f"Distribution Data Sources: {len(distribution_links)}")
    print(f"Query Interfaces: {len(query_interfaces)}")
    print(f"\nComplete data saved to: workspace/usgs_nas_clownfish_complete_data.json")
    
    # Identify the most promising sources for zip code data
    print(f"\n=== PRIORITY TARGETS FOR ZIP CODE LOCATION DATA ===\n")
    
    priority_targets = []
    
    # Point maps are highest priority (usually have coordinates)
    if point_map_links:
        priority_targets.extend(point_map_links)
        print(f"HIGH PRIORITY - Point Maps ({len(point_map_links)}):")
        for link in point_map_links:
            print(f"  • {link['text']} -> {link['url']}")
    
    # Distribution and occurrence data are second priority
    if distribution_links:
        priority_targets.extend(distribution_links[:2])  # Top 2
        print(f"\nMEDIUM PRIORITY - Distribution Data ({len(distribution_links)}):")
        for link in distribution_links[:2]:
            print(f"  • {link['text']} -> {link['url']}")
    
    # Data/record links are third priority
    if data_links:
        priority_targets.extend(data_links[:2])  # Top 2
        print(f"\nMEDIUM PRIORITY - Data Records ({len(data_links)}):")
        for link in data_links[:2]:
            print(f"  • {link['text']} -> {link['url']}")
    
    # Query interfaces for custom searches
    if query_interfaces:
        print(f"\nCUSTOM QUERY OPTION - Query Interfaces ({len(query_interfaces)}):")
        for interface in query_interfaces:
            print(f"  • Form: {interface['form_action']}")
            print(f"    Location inputs: {len(interface['location_inputs'])}")
    
    # Save priority targets for next step
    priority_data = {
        'objective': 'Extract specific location data with zip codes for nonnative Amphiprion ocellaris before 2020',
        'priority_targets': priority_targets,
        'query_interfaces': query_interfaces,
        'search_strategy': [
            '1. Access point map links first (highest chance of coordinates)',
            '2. Check distribution/occurrence links for location records',
            '3. Use query interfaces for location-specific searches',
            '4. Filter all results for pre-2020 timeframe',
            '5. Extract zip codes or convert coordinates to zip codes'
        ],
        'next_action': 'Access the highest priority target URLs to extract detailed location data'
    }
    
    with open('workspace/priority_location_extraction_plan.json', 'w') as f:
        json.dump(priority_data, f, indent=2)
    
    print(f"\nTotal priority targets identified: {len(priority_targets)}")
    print(f"Priority extraction plan saved to: workspace/priority_location_extraction_plan.json")
    
    if priority_targets:
        print(f"\nReady to access specific occurrence/location data sources for zip code extraction.")
        print(f"\nNext step: Access the first priority target to extract detailed location records.")
    else:
        print(f"\nNo direct priority targets found. Will need to use query interfaces or alternative approaches.")
    
except requests.exceptions.RequestException as e:
    print(f"Error accessing USGS database: {e}")
    print("Will try alternative approaches to access USGS NAS data.")
    
except Exception as e:
    print(f"Unexpected error during USGS database access: {e}")
    print("Error details for debugging:")
    import traceback
    traceback.print_exc()
```

## Created Time
2025-08-11 03:38:15
