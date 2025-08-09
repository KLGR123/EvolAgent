# Developer Plan 04

## Plan
Identify which astronaut from NASA Astronaut Group 2 spent the least time in space (excluding Elliot See who had zero flight time) and convert their total spaceflight duration to minutes rounded to the nearest minute. Based on the comprehensive flight duration data from the previous research, determine the astronaut with the minimum spaceflight time among those who actually flew in space.

## Description
This is the final step because: (1) We have complete spaceflight duration data for all 9 NASA Astronaut Group 2 members from the previous research, (2) The data shows Ed White had the least time in space among astronauts who actually flew (4 days, 1 hour, 56 minutes), excluding Elliot See who never flew, (3) Expected outcome is to convert Ed White's flight time to total minutes and provide the final answer in the required format (last name; minutes), (4) This directly completes the TASK by identifying the astronaut with minimum spaceflight duration and converting to the requested units

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

### Development Step 7: Extract Moon’s Minimum Perigee Distance from Wikipedia for Earth-Moon Closest Approach Calculation

**Description**: Access the Wikipedia page for the Moon and locate the minimum perigee distance value in the orbital characteristics or distance data section. Extract this specific measurement and note the units (likely in kilometers) for use in calculating the Earth-Moon distance at closest approach.

**Use Cases**:
- Lunar mission planning and trajectory optimization in aerospace engineering platforms using automated perigee distance updates
- Satellite orbit perturbation analysis for Earth observation companies assessing lunar gravitational influences at closest approach
- Live planetarium projection systems automatically updating Earth–Moon separation visuals based on the current minimum perigee distance
- Educational mobile and web applications generating interactive supermoon countdowns with accurate perigee measurements
- Data journalism pipelines producing automated infographics for news outlets covering supermoon events and lunar exploration milestones
- Virtual reality spacewalk experiences adjusting scale and distance to the Moon for immersive astronaut training modules
- Oceanographic research tools correlating extreme tidal events with lunar perigee distances for coastal risk management studies
- Realistic space exploration game engines fetching authentic lunar orbital parameters to enhance in-game physics fidelity

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
        if infobox:
            print("✓ Found infobox table")
            
            # Extract all rows from infobox
            infobox_data = []
            rows = infobox.find_all('tr')
            
            for row in rows:
                # Get the label and value from each row
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    label = cells[0].get_text().strip()
                    value = cells[1].get_text().strip()
                    
                    # Look for distance, perigee, or orbital data
                    if any(keyword in label.lower() for keyword in ['distance', 'perigee', 'apogee', 'orbit', 'semi-major']):
                        print(f"Orbital data found - {label}: {value}")
                        infobox_data.append({
                            'label': label,
                            'value': value,
                            'raw_html': str(row)
                        })
        
        # Search for specific perigee distance patterns in the entire page text
        print(f"\n=== SEARCHING FOR PERIGEE DISTANCE PATTERNS ===")
        
        page_text = soup.get_text()
        
        # Common patterns for perigee distance
        perigee_patterns = [
            r'perigee[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'minimum distance[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'closest approach[^\n]*?(\d+[,\d]*\.?\d*)\s*km',
            r'(\d+[,\d]*\.?\d*)\s*km[^\n]*perigee',
            r'perigee.*?(\d+[,\d]*\.?\d*)\s*kilometres',
            r'356[,\d]*\s*km'  # Common approximate perigee distance
        ]
        
        perigee_matches = []
        for pattern in perigee_patterns:
            matches = re.finditer(pattern, page_text, re.IGNORECASE)
            for match in matches:
                context_start = max(0, match.start() - 100)
                context_end = min(len(page_text), match.end() + 100)
                context = page_text[context_start:context_end].strip()
                
                perigee_matches.append({
                    'pattern': pattern,
                    'match': match.group(),
                    'context': context,
                    'distance_value': match.group(1) if match.groups() else match.group()
                })
                
                print(f"Perigee match found: {match.group()}")
                print(f"Context: ...{context}...")
                print()
        
        # Look for specific sections about orbital mechanics
        print(f"\n=== EXAMINING ORBITAL MECHANICS SECTIONS ===")
        
        orbital_sections = []
        for heading in orbital_headings:
            # Get content following this heading
            current = heading['element']
            section_content = []
            
            # Collect paragraphs following the heading
            for _ in range(10):  # Look at next 10 elements
                current = current.find_next_sibling()
                if current is None:
                    break
                if current.name == 'p':
                    text = current.get_text().strip()
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
                if any(keyword in full_content.lower() for keyword in ['perigee', 'distance', 'km', 'closest']):
                    print(f"Section '{heading['text']}' contains distance information:")
                    print(f"Content preview: {full_content[:300]}...")
                    print()
        
        # Save all extracted data
        extraction_data = {
            'page_url': url,
            'extraction_timestamp': response.headers.get('date', 'unknown'),
            'infobox_data': infobox_data if 'infobox_data' in locals() else [],
            'perigee_matches': perigee_matches,
            'orbital_sections': orbital_sections,
            'orbital_headings': [h['text'] for h in orbital_headings]
        }
        
        results_file = 'workspace/moon_perigee_extraction.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n=== EXTRACTION SUMMARY ===")
        print(f"Infobox orbital data entries: {len(infobox_data) if 'infobox_data' in locals() else 0}")
        print(f"Perigee pattern matches: {len(perigee_matches)}")
        print(f"Orbital sections found: {len(orbital_sections)}")
        print(f"Results saved to: {results_file}")
        
    else:
        print(f"Failed to access Wikipedia page. Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
except requests.exceptions.RequestException as e:
    print(f"Error accessing Wikipedia page: {e}")

print(f"\n=== MOON WIKIPEDIA ACCESS COMPLETE ===")
print("Next step: Analyze extracted data to identify the minimum perigee distance value")
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

## Created Time
2025-08-09 05:11:16
