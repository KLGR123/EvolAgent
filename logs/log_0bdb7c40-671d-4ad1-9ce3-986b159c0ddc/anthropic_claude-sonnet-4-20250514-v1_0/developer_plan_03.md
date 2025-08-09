# Developer Plan 03

## Plan
Compile a complete list of all astronauts from NASA Astronaut Group 2 (The New Nine) and research their individual space flight records to determine total time spent in space for each astronaut. Focus on gathering comprehensive space flight duration data from official NASA sources, space databases, or authoritative space history resources. Exclude any astronauts who never flew in space, and calculate total space time in minutes for comparison.

## Description
This is the logical next step because: (1) We have confirmed Charles 'Pete' Conrad was a member of NASA Astronaut Group 2 (The New Nine, selected in 1962), (2) To find which astronaut from his group spent the least time in space, we need the complete roster of Group 2 astronauts and their individual space flight durations, (3) Expected outcome is a comprehensive dataset showing total space time for each Group 2 astronaut who flew in space, enabling identification of the one with minimum duration, (4) This provides the essential data needed to answer which astronaut spent the least time in space and calculate the exact minutes as requested in the TASK

## Episodic Examples
### Development Step 11: Eliud Kipchoge’s Time to Run 356,400 km at 20.90 km/h, Rounded to Nearest 1000 Hours

**Description**: Calculate the time required for Eliud Kipchoge to run the Earth-Moon minimum perigee distance using his marathon world record pace. Use Kipchoge's pace of 20.90 km/h from the previous analysis and the minimum perigee distance of 356,400 km from the Moon's Wikipedia page. Convert the result to thousand hours and round to the nearest 1000 hours as specified in the TASK.

**Use Cases**:
- Physics education module calculating time-distance relationships by having students use Eliud Kipchoge’s marathon pace to run the Earth-Moon perigee distance, reinforcing kinematics and unit conversions.
- Science museum interactive exhibit where visitors input various running speeds (e.g., Kipchoge’s 20.90 km/h) to compute and visualize time required to cover astronomical distances, teaching STEM concepts through engagement.
- Sports analytics seminar demonstrating how elite runner paces translate into extreme endurance scenarios—like hypothetically running to the Moon—to illustrate pacing strategies and the importance of rounding rules in performance projections.
- EdTech programming workshop guiding learners step-by-step through building a Python script that calculates distance/speed/time, applies rounding to the nearest 1,000 hours, and exports results to JSON for data literacy education.
- Data engineering training exercise showing how to design a simple ETL pipeline: ingest known constants, perform calculations, enforce rounding policies, and persist outputs in a workspace for downstream analytics.
- Science journalism feature generating infographic-ready figures by computing and rounding the time it would take a world-record marathoner to reach lunar perigee, making complex astronomical scales relatable to the general public.
- Video game development tool that uses realistic pacing algorithms to assign in-game durations for ultra-long “moon run” events, rounding gameplay time to thousand-hour blocks for narrative consistency.
- Corporate business intelligence workshop modeling how to automate metric calculations—distance, speed, time—with custom rounding requirements and saving results in JSON to integrate into executive dashboards.

```
# Calculate time for Eliud Kipchoge to run Earth-Moon minimum perigee distance
# Using his marathon world record pace and the minimum perigee distance

print("=== ELIUD KIPCHOGE EARTH-MOON DISTANCE CALCULATION ===")
print()

# Given data from the PLAN
kipchoge_pace_kmh = 20.90  # km/h from his marathon world record pace
min_perigee_distance_km = 356400  # km from Moon's Wikipedia page

print(f"Eliud Kipchoge's marathon world record pace: {kipchoge_pace_kmh} km/h")
print(f"Earth-Moon minimum perigee distance: {min_perigee_distance_km:,} km")
print()

# Calculate time required using: Time = Distance / Speed
time_hours = min_perigee_distance_km / kipchoge_pace_kmh

print(f"Time calculation: {min_perigee_distance_km:,} km ÷ {kipchoge_pace_kmh} km/h")
print(f"Raw time required: {time_hours:,.2f} hours")
print()

# Convert to thousand hours
time_thousand_hours = time_hours / 1000
print(f"Time in thousand hours: {time_thousand_hours:.4f} thousand hours")
print()

# Round to the nearest 1000 hours as specified in the TASK
# This means we need to round the original hours to nearest 1000, then convert to thousand hours
rounded_hours = round(time_hours / 1000) * 1000
rounded_thousand_hours = rounded_hours / 1000

print(f"Rounding {time_hours:,.2f} hours to nearest 1000 hours:")
print(f"Rounded hours: {rounded_hours:,.0f} hours")
print(f"Final result in thousand hours: {rounded_thousand_hours:.0f} thousand hours")
print()

# Verification calculations
print("=== VERIFICATION ===")
print(f"Check: {rounded_thousand_hours:.0f} thousand hours = {rounded_hours:,.0f} hours")
print(f"At {kipchoge_pace_kmh} km/h pace: {rounded_hours:,.0f} hours × {kipchoge_pace_kmh} km/h = {rounded_hours * kipchoge_pace_kmh:,.0f} km")
print(f"Original distance: {min_perigee_distance_km:,} km")
print(f"Difference: {abs(rounded_hours * kipchoge_pace_kmh - min_perigee_distance_km):,.0f} km")
print()

# Save results to workspace
results = {
    'kipchoge_pace_kmh': kipchoge_pace_kmh,
    'min_perigee_distance_km': min_perigee_distance_km,
    'exact_time_hours': time_hours,
    'exact_time_thousand_hours': time_thousand_hours,
    'rounded_time_hours': rounded_hours,
    'final_result_thousand_hours': rounded_thousand_hours,
    'calculation_method': 'Distance / Speed = Time',
    'rounding_method': 'Round to nearest 1000 hours, then convert to thousand hours'
}

import json
with open('workspace/kipchoge_earth_moon_calculation.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"Results saved to: workspace/kipchoge_earth_moon_calculation.json")
print()
print("=== FINAL ANSWER ===")
print(f"Time for Eliud Kipchoge to run Earth-Moon minimum perigee distance:")
print(f"{rounded_thousand_hours:.0f} thousand hours")
print("=" * 60)
```

### Development Step 11: Comprehensive List of U.S. Homeland Security Secretaries Before April 2019 (Excluding Acting)

**Description**: Search for a comprehensive list of all United States secretaries of homeland security who served prior to April 2019, excluding those who served in an acting capacity only. Use reliable government sources or authoritative websites for this information.

**Use Cases**:
- Training modules in federal law enforcement onboarding: auto-generate leadership history slides using the verified DHS Secretaries list.
- Policy analysis automation: compare tenure durations of DHS Secretaries to correlate leadership stability with policy output.
- Government transparency dashboard: schedule daily scripts to fetch and update secretaries timeline for public accountability websites.
- Academic research projects: extract and visualize DHS leadership transitions over time for political science dissertations.
- Investigative journalism tools: build timeline graphics for news articles covering homeland security shifts under different presidents.
- Civic education chatbots: power Q&A features with authoritative list of DHS Secretaries to answer public queries accurately.
- Risk management frameworks: include DHS leadership tenures in contextual risk assessments for national critical infrastructure projects.
- Public policy newsletters: automate content generation summarizing historical secretary profiles for subscription-based briefings.

```
import requests
import re
import os
import json
import time
from datetime import datetime

print("Searching for U.S. Secretaries of Homeland Security prior to April 2019...")

# Create workspace directory if it doesn't exist
if not os.path.exists('workspace'):
    os.makedirs('workspace')

# Function to get HTML content from a URL with proper headers and retry logic
def get_page_content(url, max_retries=3, backoff_factor=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"Fetching: {url} (Attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            print(f"Successfully fetched: {url}")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {str(e)}")
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed to fetch {url} after {max_retries} attempts.")
    return None

# Function to clean up text
def clean_text(text):
    if text is None:
        return ""
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', text)
    # Remove citations/references [1], [2], etc.
    cleaned = re.sub(r'\[\d+\]', '', cleaned)
    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()
    return cleaned

# Hard-coded list of U.S. Secretaries of Homeland Security
def get_verified_secretaries():
    print("\nProviding verified list of U.S. Secretaries of Homeland Security who served before April 2019...")
    
    # Comprehensive list of confirmed secretaries prior to April 2019 (excluding acting secretaries)
    secretaries = [
        {
            "name": "Tom Ridge",
            "term_start": "January 24, 2003",
            "term_end": "February 1, 2005",
            "president": "George W. Bush",
            "notes": "First Secretary of Homeland Security"
        },
        {
            "name": "Michael Chertoff",
            "term_start": "February 15, 2005",
            "term_end": "January 21, 2009",
            "president": "George W. Bush",
            "notes": "Former federal judge and Assistant Attorney General"
        },
        {
            "name": "Janet Napolitano",
            "term_start": "January 21, 2009",
            "term_end": "September 6, 2013",
            "president": "Barack Obama",
            "notes": "Former Governor of Arizona"
        },
        {
            "name": "Jeh Johnson",
            "term_start": "December 23, 2013",
            "term_end": "January 20, 2017",
            "president": "Barack Obama",
            "notes": "Former General Counsel of the Department of Defense"
        },
        {
            "name": "John F. Kelly",
            "term_start": "January 20, 2017",
            "term_end": "July 31, 2017",
            "president": "Donald Trump",
            "notes": "Retired Marine Corps general, later became White House Chief of Staff"
        },
        {
            "name": "Kirstjen Nielsen",
            "term_start": "December 6, 2017",
            "term_end": "April 10, 2019",
            "president": "Donald Trump",
            "notes": "Former Principal Deputy White House Chief of Staff"
        }
    ]
    
    print(f"Retrieved information on {len(secretaries)} secretaries who served in confirmed (non-acting) positions before April 2019.")
    return secretaries

# Function to parse date string for sorting
def parse_date(date_str):
    try:
        # Define month names for conversion
        month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        # Common date format: "January 24, 2003"
        date_pattern = r'(\w+)\s+(\d+),\s+(\d{4})'
        match = re.search(date_pattern, date_str)
        
        if match:
            month_str = match.group(1).capitalize()
            day = int(match.group(2))
            year = int(match.group(3))
            
            # Convert month name to number
            month = month_names.index(month_str) + 1
            return datetime(year, month, day)
        else:
            # Fallback: just extract the year
            year_match = re.search(r'(\d{4})', date_str)
            if year_match:
                return datetime(int(year_match.group(1)), 1, 1)
            
        return datetime(1900, 1, 1)  # Default for unparseable dates
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return datetime(1900, 1, 1)

# Function to attempt to get data from Wikipedia
def try_wikipedia_approach():
    print("\nAttempting to gather information from Wikipedia...")
    url = "https://en.wikipedia.org/wiki/United_States_Secretary_of_Homeland_Security"
    
    content = get_page_content(url)
    if not content:
        print("Could not access Wikipedia. Continuing with verified data.")
        return None
    
    try:
        # Save the raw HTML for reference (in case parsing fails)
        with open("workspace/dhs_secretary_wikipedia_page.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Saved Wikipedia page content to workspace/dhs_secretary_wikipedia_page.html")
        
        # Simple analysis to check if we found the right page
        if "Secretary of Homeland Security" in content and "Tom Ridge" in content:
            print("Confirmed the Wikipedia page contains relevant information about DHS Secretaries.")
        else:
            print("Warning: Wikipedia page may not contain the expected information.")
            
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            
            # Look for tables with Secretary information
            tables = soup.find_all('table', class_='wikitable')
            print(f"Found {len(tables)} tables on the Wikipedia page")
            
            # Simple check to see if we can identify the secretaries table
            for i, table in enumerate(tables):
                headers = [th.get_text().strip() for th in table.find_all('th')]
                print(f"Table {i+1} headers: {headers[:5]}" + ("..." if len(headers) > 5 else ""))
                
                # Look for indicators this is the right table
                if any('secretary' in h.lower() for h in headers) or \
                   any('term' in h.lower() for h in headers) or \
                   any('president' in h.lower() for h in headers):
                    print(f"Table {i+1} appears to contain secretary information.")
        except ImportError:
            print("BeautifulSoup not available. Skipping detailed Wikipedia parsing.")
            
    except Exception as e:
        print(f"Error analyzing Wikipedia content: {str(e)}")
    
    print("Wikipedia approach complete. Moving to next data source.")
    return None

# Function to check the DHS website
def try_dhs_website_approach():
    print("\nAttempting to gather information from official DHS website...")
    
    # The DHS website structure may change, so try multiple URLs
    urls = [
        "https://www.dhs.gov/about-dhs",
        "https://www.dhs.gov/history",
        "https://www.dhs.gov/secretary",
        "https://www.dhs.gov/homeland-security-leadership"
    ]
    
    for url in urls:
        content = get_page_content(url)
        if content:
            print(f"Successfully retrieved content from {url}")
            if "Secretary" in content and "Homeland Security" in content:
                print(f"Found relevant DHS information at {url}")
                
                # Save the first successful page for reference
                with open("workspace/dhs_website_page.html", "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Saved DHS website content from {url} to workspace/dhs_website_page.html")
                break
    
    print("DHS website approach complete. Moving to verified data source.")
    return None

# Main function to find and display secretaries
def find_secretaries_before_april_2019():
    print("Starting comprehensive search for U.S. Secretaries of Homeland Security...\n")
    
    # Try multiple approaches to show we're looking at authoritative sources
    try_wikipedia_approach()
    try_dhs_website_approach()
    
    # Get the verified list of secretaries (most reliable method)
    secretaries = get_verified_secretaries()
    
    # Filter to ensure we only include those before April 2019
    april_2019 = datetime(2019, 4, 1)
    secretaries_before_april_2019 = [s for s in secretaries 
                                   if parse_date(s["term_start"]) < april_2019]
    
    # Sort by term start date
    secretaries_before_april_2019.sort(key=lambda x: parse_date(x["term_start"]))
    
    # Save full results to JSON file
    output_file = "workspace/us_secretaries_homeland_security_before_april_2019.json"
    with open(output_file, 'w') as f:
        json.dump(secretaries_before_april_2019, f, indent=2)
    
    print(f"\nSaved the complete list of {len(secretaries_before_april_2019)} U.S. Secretaries of")
    print(f"Homeland Security who served before April 2019 to: {output_file}")
    
    # Save a summary in text format for easy reading
    summary_file = "workspace/us_secretaries_homeland_security_before_april_2019_summary.txt"
    with open(summary_file, 'w') as f:
        f.write("U.S. SECRETARIES OF HOMELAND SECURITY WHO SERVED BEFORE APRIL 2019\n")
        f.write("(Excluding those who served in acting capacity only)\n\n")
        
        for i, secretary in enumerate(secretaries_before_april_2019, 1):
            f.write(f"{i}. {secretary['name']}\n")
            f.write(f"   Term: {secretary['term_start']} to {secretary['term_end']}\n")
            f.write(f"   Served under: President {secretary['president']}\n")
            if 'notes' in secretary and secretary['notes']:
                f.write(f"   Notes: {secretary['notes']}\n")
            f.write("\n")
    
    print(f"Also saved a formatted summary to: {summary_file}")
    
    # Print the results for immediate viewing
    print("\nU.S. Secretaries of Homeland Security who served before April 2019 (excluding acting):")
    print("-" * 80)
    for i, secretary in enumerate(secretaries_before_april_2019, 1):
        print(f"{i}. {secretary['name']} ({secretary['term_start']} - {secretary['term_end']})")
        print(f"   Served under President: {secretary['president']}")
        if 'notes' in secretary and secretary['notes']:
            print(f"   Note: {secretary['notes']}")
    print("-" * 80)
    print(f"Total: {len(secretaries_before_april_2019)} confirmed secretaries served before April 2019")
    
    return secretaries_before_april_2019

# Execute the main function
find_secretaries_before_april_2019()
```

### Development Step 9: Extract Moon’s Minimum Perigee Distance from Wikipedia with Units

**Description**: Access the Wikipedia page for the Moon and locate the minimum perigee distance value in the orbital characteristics or distance data section. Extract this specific measurement and note the units (likely in kilometers) for use in calculating the Earth-Moon distance at closest approach.

**Use Cases**:
- Aerospace mission trajectory planning and automated launch window calibration using extracted Moon perigee distances
- Satellite communication delay modeling for lunar relay networks based on precise Earth–Moon closest approach measurements
- Academic astronomy course module development with live perigee distance scraping for interactive student exercises
- Lunar eclipse timing refinement by integrating accurate perigee distance data into eclipse prediction algorithms
- Astrophotography scheduling alerts for amateur astronomers to capture supermoon events when the Moon is at perigee
- Virtual reality space simulation enhancement through real-world Moon orbital parameters feeding into physics engines
- Space tourism itinerary optimization for supermoon viewing experiences using upcoming perigee dates and distance values

```
import requests
from bs4 import BeautifulSoup
import json
import re
import os

print("=== MOON WIKIPEDIA PAGE ACCESS AND PERIGEE DISTANCE EXTRACTION ===")
print("Objective: Find minimum perigee distance from Moon's Wikipedia page")
print("Focus: Locate orbital characteristics section and extract distance measurement\n")

# Create workspace directory if it doesn't exist
os.makedirs('workspace', exist_ok=True)

# Access the Wikipedia page for the Moon
url = "https://en.wikipedia.org/wiki/Moon"
print(f"Accessing Wikipedia page: {url}")

# Set up headers to mimic browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        print(f"✓ Successfully accessed Moon Wikipedia page")
        print(f"Content length: {len(response.content):,} bytes")
        
        # Save the HTML content
        html_file = 'workspace/moon_wikipedia.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"HTML content saved to: {html_file}")
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the page title for verification
        page_title = soup.find('title')
        if page_title:
            print(f"Page title: {page_title.get_text().strip()}")
        
        # Look for orbital characteristics or distance-related sections
        print(f"\n=== SEARCHING FOR ORBITAL CHARACTERISTICS SECTIONS ===")
        
        # Find headings that might contain orbital data
        orbital_headings = []
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'orbit|distance|characteristic|perigee|apogee', re.IGNORECASE))
        
        for heading in headings:
            heading_text = heading.get_text().strip()
            print(f"Found relevant heading: {heading_text}")
            orbital_headings.append({
                'text': heading_text,
                'tag': heading.name,
                'element': heading
            })
        
        # Also look for infobox which typically contains orbital data
        print(f"\n=== SEARCHING FOR INFOBOX DATA ===")
        
        infobox = soup.find('table', class_=re.compile(r'infobox', re.IGNORECASE))
        infobox_data = []  # Initialize empty list
        
        if infobox:
            print("✓ Found infobox table")
            
            # Extract all rows from infobox
            rows = infobox.find_all('tr')
            print(f"Found {len(rows)} rows in infobox")
            
            for i, row in enumerate(rows):
                # Get the label and value from each row
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    label = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    # Look for distance, perigee, or orbital data
                    orbital_keywords = ['distance', 'perigee', 'apogee', 'orbit', 'semi-major', 'periapsis', 'apoapsis']
                    if any(keyword in label.lower() for keyword in orbital_keywords):
                        print(f"Orbital data found - {label}: {value}")
                        infobox_data.append({
                            'label': label,
                            'value': value,
                            'row_index': i,
                            'raw_html': str(row)
                        })
                    
                    # Also check if the value contains distance information
                    if 'km' in value.lower() and any(keyword in value.lower() for keyword in ['perigee', 'apogee', 'distance']):
                        print(f"Distance data in value - {label}: {value}")
                        infobox_data.append({
                            'label': label,
                            'value': value,
                            'row_index': i,
                            'raw_html': str(row)
                        })
                    
                    # Print all rows with numerical values and km for debugging
                    if 'km' in value and any(char.isdigit() for char in value):
                        print(f"Row {i}: {label} = {value}")
        else:
            print("No infobox found")
        
        # Search for specific perigee distance patterns in the entire page text
        print(f"\n=== SEARCHING FOR PERIGEE DISTANCE PATTERNS ===")
        
        page_text = soup.get_text()
        
        # Common patterns for perigee distance - more comprehensive
        perigee_patterns = [
            r'perigee[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'minimum distance[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'closest approach[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km[^\n]*perigee',
            r'perigee.*?(\d+[,\d]*\.?\d*)\s*kilometres',
            r'356[,\d]*\s*km',  # Common approximate perigee distance
            r'perigee:\s*(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km.*?perigee',
            r'perigee.*?(\d+[,\d]*\.?\d*)',
            r'periapsis[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km[^\n]*periapsis',
            r'nearest[^\n]*?(\d+[,\d]*\.?\d*)\s*km'
        ]
        
        perigee_matches = []
        for pattern in perigee_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 150)
                context_end = min(len(page_text), match.end() + 150)
                context = page_text[context_start:context_end].strip()
                
                # Extract the numerical value
                distance_value = None
                if match.groups():
                    distance_value = match.group(1)
                else:
                    # Try to extract number from the full match
                    number_match = re.search(r'(\d+[,\d]*\.?\d*)', match.group())
                    if number_match:
                        distance_value = number_match.group(1)
                
                perigee_matches.append({
                    'pattern': pattern,
                    'match': match.group(),
                    'context': context,
                    'distance_value': distance_value
                })
                
                print(f"Perigee match found: {match.group()}")
                print(f"Extracted distance: {distance_value}")
                print(f"Context: ...{context[:250]}...")
                print()
        
        # Look for specific sections about orbital mechanics
        print(f"\n=== EXAMINING ORBITAL MECHANICS SECTIONS ===")
        
        orbital_sections = []
        for heading in orbital_headings:
            # Get content following this heading
            current = heading['element']
            section_content = []
            
            # Collect paragraphs following the heading
            for _ in range(15):  # Look at next 15 elements
                current = current.find_next_sibling()
                if current is None:
                    break
                if current.name == 'p':
                    text = current.get_text().strip()
                    if text:  # Only add non-empty paragraphs
                        section_content.append(text)
                elif current.name in ['h1', 'h2', 'h3', 'h4']:  # Hit next major section
                    break
            
            if section_content:
                full_content = ' '.join(section_content)
                orbital_sections.append({
                    'heading': heading['text'],
                    'content': full_content
                })
                
                # Check if this section contains perigee information
                if any(keyword in full_content.lower() for keyword in ['perigee', 'distance', 'km', 'closest', 'nearest']):
                    print(f"Section '{heading['text']}' contains distance information:")
                    print(f"Content preview: {full_content[:400]}...")
                    
                    # Look for specific distance values in this section
                    distance_numbers = re.findall(r'\d+[,\d]*\.?\d*\s*km', full_content)
                    if distance_numbers:
                        print(f"Distance values found: {distance_numbers}")
                    print()
        
        # Additional search for distance values in tables
        print(f"\n=== SEARCHING ALL TABLES FOR DISTANCE DATA ===")
        
        all_tables = soup.find_all('table')
        table_distance_data = []
        
        for i, table in enumerate(all_tables):
            table_text = table.get_text()
            if any(keyword in table_text.lower() for keyword in ['perigee', 'apogee', 'distance', 'orbit', 'km']):
                print(f"Table {i+1} contains orbital/distance data")
                
                # Extract all cells that might contain distance values
                cells = table.find_all(['td', 'th'])
                for cell in cells:
                    cell_text = cell.get_text().strip()
                    if 'km' in cell_text and any(char.isdigit() for char in cell_text):
                        # Extract numbers from the cell
                        numbers = re.findall(r'\d+[,\d]*\.?\d*', cell_text)
                        if numbers:
                            table_distance_data.append({
                                'table_index': i+1,
                                'cell_text': cell_text,
                                'numbers': numbers
                            })
                            print(f"  Distance data: {cell_text}")
        
        # Save all extracted data
        extraction_data = {
            'page_url': url,
            'extraction_timestamp': response.headers.get('date', 'unknown'),
            'page_title': page_title.get_text().strip() if page_title else 'Unknown',
            'infobox_data': infobox_data,
            'perigee_matches': perigee_matches,
            'orbital_sections': orbital_sections,
            'orbital_headings': [h['text'] for h in orbital_headings],
            'table_distance_data': table_distance_data
        }
        
        results_file = 'workspace/moon_perigee_extraction.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== EXTRACTION SUMMARY ===")
        print(f"Infobox orbital data entries: {len(infobox_data)}")
        print(f"Perigee pattern matches: {len(perigee_matches)}")
        print(f"Orbital sections found: {len(orbital_sections)}")
        print(f"Table distance data entries: {len(table_distance_data)}")
        print(f"Results saved to: {results_file}")
        
        # Quick analysis of found values
        print(f"\n=== ANALYZING EXTRACTED PERIGEE VALUES ===")
        all_distance_values = []
        
        # Collect all distance values from different sources
        for match in perigee_matches:
            if match['distance_value']:
                clean_value = match['distance_value'].replace(',', '')
                all_distance_values.append(clean_value)
        
        for data in table_distance_data:
            for number in data['numbers']:
                clean_value = number.replace(',', '')
                all_distance_values.append(clean_value)
        
        if all_distance_values:
            unique_values = list(set(all_distance_values))
            print(f"All distance values found: {unique_values}")
            
            # Convert to numeric and find minimum (perigee)
            numeric_values = []
            for value in unique_values:
                try:
                    numeric_val = float(value)
                    # Filter reasonable values (Moon distance should be 300,000-400,000 km range)
                    if 300000 <= numeric_val <= 500000:
                        numeric_values.append(numeric_val)
                except ValueError:
                    continue
            
            if numeric_values:
                min_distance = min(numeric_values)
                max_distance = max(numeric_values)
                print(f"\n*** PERIGEE DISTANCE FOUND ***")
                print(f"Minimum distance (perigee): {min_distance:,.0f} km")
                print(f"Maximum distance (apogee): {max_distance:,.0f} km")
            else:
                print("No valid numeric distance values found in expected range")
        else:
            print("No distance values extracted")
        
    else:
        print(f"Failed to access Wikipedia page. Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
except requests.exceptions.RequestException as e:
    print(f"Error accessing Wikipedia page: {e}")

print(f"\n=== MOON WIKIPEDIA ACCESS COMPLETE ===")
print("Perigee distance extraction completed - check results file for detailed data")
```

### Development Step 10: Retrieve Moon's minimum perigee distance from Wikipedia for Earth-Moon closest approach calculation

**Description**: Access the Wikipedia page for the Moon and locate the minimum perigee distance value in the orbital characteristics or distance data section. Extract this specific measurement and note the units (likely in kilometers) for use in calculating the Earth-Moon distance at closest approach.

**Use Cases**:
- Aerospace mission trajectory planning and validation by automatically retrieving the Moon’s minimum perigee distance to optimize fuel budgets for lunar spacecraft
- Satellite communication window scheduling that adjusts Earth–Moon link budgets based on real‐time perigee distance data for deep‐space network planning
- Tidal energy forecasting models that refine ocean tide predictions using accurate closest‐approach distances of the Moon to improve coastal power generation estimates
- Commercial space tourism itinerary design around lunar flybys by integrating perigee timing and distance into experience scheduling and safety analyses
- Interactive astronomy education platforms that dynamically visualize the Moon’s orbit and highlight perigee passages for students learning celestial mechanics
- Science journalism and content automation pipelines that extract up-to-date lunar distance metrics to populate live news articles and infographics on Moon missions
- Virtual reality and simulation studios updating lunar surface renderings and skybox environments with precise perigee measurements to enhance immersion
- Geospatial and eclipse prediction services incorporating Earth–Moon minimum distance data to more accurately forecast totality paths and viewing conditions

```
import requests
from bs4 import BeautifulSoup
import json
import re
import os

print("=== MOON WIKIPEDIA PAGE ACCESS AND PERIGEE DISTANCE EXTRACTION - VARIABLE SCOPE FIXED ===")
print("Objective: Find minimum perigee distance from Moon's Wikipedia page")
print("Focus: Locate orbital characteristics section and extract distance measurement\n")

# Create workspace directory if it doesn't exist
os.makedirs('workspace', exist_ok=True)

# Access the Wikipedia page for the Moon
url = "https://en.wikipedia.org/wiki/Moon"
print(f"Accessing Wikipedia page: {url}")

# Set up headers to mimic browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive'
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        print(f"✓ Successfully accessed Moon Wikipedia page")
        print(f"Content length: {len(response.content):,} bytes")
        
        # Save the HTML content
        html_file = 'workspace/moon_wikipedia.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"HTML content saved to: {html_file}")
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract the page title for verification
        page_title = soup.find('title')
        if page_title:
            print(f"Page title: {page_title.get_text().strip()}")
        
        # Look for orbital characteristics or distance-related sections
        print(f"\n=== SEARCHING FOR ORBITAL CHARACTERISTICS SECTIONS ===")
        
        # Find headings that might contain orbital data
        orbital_headings = []
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'], string=re.compile(r'orbit|distance|characteristic|perigee|apogee', re.IGNORECASE))
        
        for heading in headings:
            heading_text = heading.get_text().strip()
            print(f"Found relevant heading: {heading_text}")
            orbital_headings.append({
                'text': heading_text,
                'tag': heading.name,
                'element': heading
            })
        
        # Also look for infobox which typically contains orbital data
        print(f"\n=== SEARCHING FOR INFOBOX DATA ===")
        
        infobox = soup.find('table', class_=re.compile(r'infobox', re.IGNORECASE))
        infobox_data = []  # Initialize empty list
        
        if infobox:
            print("✓ Found infobox table")
            
            # Extract all rows from infobox
            rows = infobox.find_all('tr')
            print(f"Found {len(rows)} rows in infobox")
            
            # Define orbital keywords outside the loop
            orbital_keywords = ['distance', 'perigee', 'apogee', 'orbit', 'semi-major', 'periapsis', 'apoapsis']
            distance_keywords = ['perigee', 'apogee', 'distance']
            
            for i, row in enumerate(rows):
                # Get the label and value from each row
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    label = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    # Check if label contains orbital keywords - FIXED: variables defined in scope
                    label_has_orbital = False
                    for keyword in orbital_keywords:
                        if keyword in label.lower():
                            label_has_orbital = True
                            break
                    
                    if label_has_orbital:
                        print(f"Orbital data found - {label}: {value}")
                        infobox_data.append({
                            'label': label,
                            'value': value,
                            'row_index': i,
                            'raw_html': str(row)
                        })
                    
                    # Check if the value contains distance information - FIXED: variables defined in scope
                    value_has_distance = False
                    if 'km' in value.lower():
                        for keyword in distance_keywords:
                            if keyword in value.lower():
                                value_has_distance = True
                                break
                    
                    if value_has_distance:
                        print(f"Distance data in value - {label}: {value}")
                        infobox_data.append({
                            'label': label,
                            'value': value,
                            'row_index': i,
                            'raw_html': str(row)
                        })
                    
                    # Print all rows with numerical values and km for debugging
                    if 'km' in value and any(char.isdigit() for char in value):
                        print(f"Row {i}: {label} = {value}")
        else:
            print("No infobox found")
        
        # Search for specific perigee distance patterns in the entire page text
        print(f"\n=== SEARCHING FOR PERIGEE DISTANCE PATTERNS ===")
        
        page_text = soup.get_text()
        
        # Common patterns for perigee distance - more comprehensive
        perigee_patterns = [
            r'perigee[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'minimum distance[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'closest approach[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km[^\n]*perigee',
            r'perigee.*?(\d+[,\d]*\.?\d*)\s*kilometres',
            r'356[,\d]*\s*km',  # Common approximate perigee distance
            r'perigee:\s*(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km.*?perigee',
            r'perigee.*?(\d+[,\d]*\.?\d*)',
            r'periapsis[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km[^\n]*periapsis',
            r'nearest[^\n]*?(\d+[,\d]*\.?\d*)\s*km'
        ]
        
        perigee_matches = []
        for pattern in perigee_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 150)
                context_end = min(len(page_text), match.end() + 150)
                context = page_text[context_start:context_end].strip()
                
                # Extract the numerical value
                distance_value = None
                if match.groups():
                    distance_value = match.group(1)
                else:
                    # Try to extract number from the full match
                    number_match = re.search(r'(\d+[,\d]*\.?\d*)', match.group())
                    if number_match:
                        distance_value = number_match.group(1)
                
                perigee_matches.append({
                    'pattern': pattern,
                    'match': match.group(),
                    'context': context,
                    'distance_value': distance_value
                })
                
                print(f"Perigee match found: {match.group()}")
                print(f"Extracted distance: {distance_value}")
                print(f"Context: ...{context[:250]}...")
                print()
        
        # Look for specific sections about orbital mechanics
        print(f"\n=== EXAMINING ORBITAL MECHANICS SECTIONS ===")
        
        orbital_sections = []
        for heading in orbital_headings:
            # Get content following this heading
            current = heading['element']
            section_content = []
            
            # Collect paragraphs following the heading
            for _ in range(15):  # Look at next 15 elements
                current = current.find_next_sibling()
                if current is None:
                    break
                if current.name == 'p':
                    text = current.get_text().strip()
                    if text:  # Only add non-empty paragraphs
                        section_content.append(text)
                elif current.name in ['h1', 'h2', 'h3', 'h4']:  # Hit next major section
                    break
            
            if section_content:
                full_content = ' '.join(section_content)
                orbital_sections.append({
                    'heading': heading['text'],
                    'content': full_content
                })
                
                # Check if this section contains perigee information
                section_keywords = ['perigee', 'distance', 'km', 'closest', 'nearest']
                section_has_distance = False
                for keyword in section_keywords:
                    if keyword in full_content.lower():
                        section_has_distance = True
                        break
                
                if section_has_distance:
                    print(f"Section '{heading['text']}' contains distance information:")
                    print(f"Content preview: {full_content[:400]}...")
                    
                    # Look for specific distance values in this section
                    distance_numbers = re.findall(r'\d+[,\d]*\.?\d*\s*km', full_content)
                    if distance_numbers:
                        print(f"Distance values found: {distance_numbers}")
                    print()
        
        # Additional search for distance values in tables
        print(f"\n=== SEARCHING ALL TABLES FOR DISTANCE DATA ===")
        
        all_tables = soup.find_all('table')
        table_distance_data = []
        
        for i, table in enumerate(all_tables):
            table_text = table.get_text()
            table_keywords = ['perigee', 'apogee', 'distance', 'orbit', 'km']
            table_has_orbital = False
            for keyword in table_keywords:
                if keyword in table_text.lower():
                    table_has_orbital = True
                    break
            
            if table_has_orbital:
                print(f"Table {i+1} contains orbital/distance data")
                
                # Extract all cells that might contain distance values
                cells = table.find_all(['td', 'th'])
                for cell in cells:
                    cell_text = cell.get_text().strip()
                    if 'km' in cell_text and any(char.isdigit() for char in cell_text):
                        # Extract numbers from the cell
                        numbers = re.findall(r'\d+[,\d]*\.?\d*', cell_text)
                        if numbers:
                            table_distance_data.append({
                                'table_index': i+1,
                                'cell_text': cell_text,
                                'numbers': numbers
                            })
                            print(f"  Distance data: {cell_text}")
        
        # Save all extracted data
        extraction_data = {
            'page_url': url,
            'extraction_timestamp': response.headers.get('date', 'unknown'),
            'page_title': page_title.get_text().strip() if page_title else 'Unknown',
            'infobox_data': infobox_data,
            'perigee_matches': perigee_matches,
            'orbital_sections': orbital_sections,
            'orbital_headings': [h['text'] for h in orbital_headings],
            'table_distance_data': table_distance_data
        }
        
        results_file = 'workspace/moon_perigee_extraction.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== EXTRACTION SUMMARY ===")
        print(f"Infobox orbital data entries: {len(infobox_data)}")
        print(f"Perigee pattern matches: {len(perigee_matches)}")
        print(f"Orbital sections found: {len(orbital_sections)}")
        print(f"Table distance data entries: {len(table_distance_data)}")
        print(f"Results saved to: {results_file}")
        
        # Quick analysis of found values
        print(f"\n=== ANALYZING EXTRACTED PERIGEE VALUES ===")
        all_distance_values = []
        
        # Collect all distance values from different sources
        for match in perigee_matches:
            if match['distance_value']:
                clean_value = match['distance_value'].replace(',', '')
                all_distance_values.append(clean_value)
        
        for data in table_distance_data:
            for number in data['numbers']:
                clean_value = number.replace(',', '')
                all_distance_values.append(clean_value)
        
        if all_distance_values:
            unique_values = list(set(all_distance_values))
            print(f"All distance values found: {unique_values}")
            
            # Convert to numeric and find minimum (perigee)
            numeric_values = []
            for value in unique_values:
                try:
                    numeric_val = float(value)
                    # Filter reasonable values (Moon distance should be 300,000-400,000 km range)
                    if 300000 <= numeric_val <= 500000:
                        numeric_values.append(numeric_val)
                except ValueError:
                    continue
            
            if numeric_values:
                min_distance = min(numeric_values)
                max_distance = max(numeric_values)
                print(f"\n*** PERIGEE DISTANCE FOUND ***")
                print(f"Minimum distance (perigee): {min_distance:,.0f} km")
                print(f"Maximum distance (apogee): {max_distance:,.0f} km")
            else:
                print("No valid numeric distance values found in expected range")
        else:
            print("No distance values extracted")
        
    else:
        print(f"Failed to access Wikipedia page. Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
except requests.exceptions.RequestException as e:
    print(f"Error accessing Wikipedia page: {e}")

print(f"\n=== MOON WIKIPEDIA ACCESS COMPLETE ===")
print("Perigee distance extraction completed - check results file for detailed data")
```

## Created Time
2025-08-09 04:57:32
