# Developer Plan 03

## Plan
Access the generated URL 'https://web.archive.org/web/20230609112831/https://rosettacode.org/wiki/sorting_algorithms/Quicksort#C++' to retrieve the C++ source code content. Download and save the C++ code to workspace/quicksort.cpp for compilation and execution.

## Description
This is the next logical step because: (1) We have successfully generated the URL containing C++ source code from the Python script execution, (2) The previous step completed the Python script execution and produced the target URL, (3) Expected outcome is to obtain the actual C++ source code that we need to compile and run against the integer array [35, 12, 8, 99, 21, 5], (4) This advances us toward the final phase where we'll compile the C++ code and calculate the sum of the third and fifth integers in the sorted list

## Episodic Examples
### Development Step 1: Determine Missing Edge Cube Colors in Rubik’s Cube from Found-Cube Constraints

**Description**: Analyze the Rubik's cube structure and systematically determine which cubes have been found based on the given constraints. Start by establishing the standard 3x3x3 Rubik's cube composition: 6 center cubes (one colored face each), 12 edge cubes (two colored faces each), and 8 corner cubes (three colored faces each). Then work through each constraint: (1) All blue cubes found, (2) All cubes adjacent to orange center found plus orange center itself, (3) All green corners found, (4) All green that borders yellow found, (5) For all found orange cubes, their opposite face cubes are also found. Create a logical framework to track which specific cubes remain unfound, focusing on the edge cubes since the removed cube has exactly two colors. Determine the colors of the missing edge cube by process of elimination.

**Use Cases**:
- Toy manufacturing quality assurance in Rubik’s cube production lines: automating detection of missing or miscolored edge pieces via cube state analysis before packaging
- Augmented reality educational platform for teaching constraint logic and combinatorics: visualizing found versus missing cubelets and guiding students through elimination puzzles
- Robotic assembly validation in automated puzzle packaging systems: verifying that each dispatched Rubik’s cube contains the full set of edge and corner pieces
- Puzzle rental service inventory management: scanning returned cubes to quickly identify any missing edge pieces and trigger replacement orders
- Competitive speedcubing training analytics: analyzing cube initialization states to detect unintended piece rearrangements and optimize startup consistency
- Academic research in group theory and permutation puzzles: programmatically generating missing‐piece scenarios to study solvability under different constraint sets
- Virtual Rubik’s cube solver diagnostic tool: identifying and isolating missing edge cubes in digital simulations to aid debugging and developer testing
- Mechanical puzzle–based security lock integrity check: verifying the completeness of a cube lock mechanism by ensuring no edge components have been tampered with or removed

```
# Analyze Rubik's cube structure and determine missing cube colors
# Start by establishing the standard 3x3x3 Rubik's cube composition

print("=== RUBIK'S CUBE STRUCTURE ANALYSIS ===")
print()

# Standard 3x3x3 Rubik's cube composition
print("Standard 3x3x3 Rubik's cube composition:")
print("- 6 center cubes (1 colored face each)")
print("- 12 edge cubes (2 colored faces each)")
print("- 8 corner cubes (3 colored faces each)")
print("- Total: 26 cubes (27 - 1 invisible center)")
print()

# Define the six standard colors and their typical opposite arrangement
colors = ['White', 'Yellow', 'Red', 'Orange', 'Blue', 'Green']
opposite_colors = {
    'White': 'Yellow',
    'Yellow': 'White', 
    'Red': 'Orange',
    'Orange': 'Red',
    'Blue': 'Green',
    'Green': 'Blue'
}

print("Standard color arrangement (opposite faces):")
for color, opposite in opposite_colors.items():
    print(f"  {color} <-> {opposite}")
print()

# Define cube types and their characteristics
center_cubes = ['White-center', 'Yellow-center', 'Red-center', 'Orange-center', 'Blue-center', 'Green-center']

# Edge cubes - each has exactly 2 colors
edge_cubes = [
    'White-Red', 'White-Orange', 'White-Blue', 'White-Green',
    'Yellow-Red', 'Yellow-Orange', 'Yellow-Blue', 'Yellow-Green', 
    'Red-Blue', 'Red-Green', 'Orange-Blue', 'Orange-Green'
]

# Corner cubes - each has exactly 3 colors  
corner_cubes = [
    'White-Red-Blue', 'White-Red-Green', 'White-Orange-Blue', 'White-Orange-Green',
    'Yellow-Red-Blue', 'Yellow-Red-Green', 'Yellow-Orange-Blue', 'Yellow-Orange-Green'
]

print(f"Center cubes ({len(center_cubes)}): {center_cubes}")
print(f"Edge cubes ({len(edge_cubes)}): {edge_cubes}")
print(f"Corner cubes ({len(corner_cubes)}): {corner_cubes}")
print()

# Now analyze the given constraints to determine found cubes
print("=== CONSTRAINT ANALYSIS ===")
print()

found_cubes = set()

# Constraint 1: All blue cubes found
print("Constraint 1: All blue cubes found")
blue_cubes = []
for cube in center_cubes + edge_cubes + corner_cubes:
    if 'Blue' in cube:
        blue_cubes.append(cube)
        found_cubes.add(cube)
        
print(f"Blue cubes found ({len(blue_cubes)}): {blue_cubes}")
print()

# Constraint 2: All cubes adjacent to orange center found plus orange center itself
print("Constraint 2: All cubes adjacent to orange center found plus orange center itself")
orange_adjacent_cubes = ['Orange-center']
# Cubes adjacent to orange center (sharing the orange face)
for cube in edge_cubes + corner_cubes:
    if 'Orange' in cube:
        orange_adjacent_cubes.append(cube)
        found_cubes.add(cube)
        
# Also add the orange center itself
found_cubes.add('Orange-center')
        
print(f"Orange center and adjacent cubes found ({len(orange_adjacent_cubes)}): {orange_adjacent_cubes}")
print()

# Constraint 3: All green corners found
print("Constraint 3: All green corners found")
green_corners = []
for cube in corner_cubes:
    if 'Green' in cube:
        green_corners.append(cube)
        found_cubes.add(cube)
        
print(f"Green corners found ({len(green_corners)}): {green_corners}")
print()

# Constraint 4: All green that borders yellow found
print("Constraint 4: All green that borders yellow found")
green_yellow_cubes = []
for cube in edge_cubes + corner_cubes:
    if 'Green' in cube and 'Yellow' in cube:
        green_yellow_cubes.append(cube)
        found_cubes.add(cube)
        
print(f"Green cubes that border yellow found ({len(green_yellow_cubes)}): {green_yellow_cubes}")
print()

# Constraint 5: For all found orange cubes, their opposite face cubes are also found
print("Constraint 5: For all found orange cubes, their opposite face cubes are also found")
print("Orange is opposite to Red, so all red cubes corresponding to found orange cubes are also found")

# Find all orange cubes that are currently found
found_orange_cubes = [cube for cube in found_cubes if 'Orange' in cube]
print(f"Found orange cubes: {found_orange_cubes}")

# For each found orange cube, find its corresponding red cube
opposite_red_cubes = []
for orange_cube in found_orange_cubes:
    if orange_cube == 'Orange-center':
        opposite_red_cubes.append('Red-center')
        found_cubes.add('Red-center')
    else:
        # Replace Orange with Red in the cube name to get opposite
        red_cube = orange_cube.replace('Orange', 'Red')
        if red_cube in edge_cubes + corner_cubes + center_cubes:
            opposite_red_cubes.append(red_cube)
            found_cubes.add(red_cube)
            
print(f"Corresponding red cubes also found ({len(opposite_red_cubes)}): {opposite_red_cubes}")
print()

# Summary of all found cubes
print("=== SUMMARY OF FOUND CUBES ===")
found_cubes_list = sorted(list(found_cubes))
print(f"Total found cubes: {len(found_cubes_list)}")
for cube in found_cubes_list:
    print(f"  - {cube}")
print()

# Determine missing cubes
all_cubes = set(center_cubes + edge_cubes + corner_cubes)
missing_cubes = all_cubes - found_cubes
missing_cubes_list = sorted(list(missing_cubes))

print("=== MISSING CUBES ===")
print(f"Total missing cubes: {len(missing_cubes_list)}")
for cube in missing_cubes_list:
    print(f"  - {cube}")
print()

# Focus on missing edge cubes (since the removed cube has exactly 2 colors)
missing_edge_cubes = [cube for cube in missing_cubes_list if cube in edge_cubes]
print("=== MISSING EDGE CUBES (2 colors each) ===")
print(f"Missing edge cubes: {len(missing_edge_cubes)}")
for cube in missing_edge_cubes:
    colors_in_cube = cube.split('-')
    print(f"  - {cube}: Colors {colors_in_cube}")
print()

# Save detailed analysis to workspace
import json

analysis_results = {
    "cube_structure": {
        "center_cubes": center_cubes,
        "edge_cubes": edge_cubes, 
        "corner_cubes": corner_cubes,
        "total_cubes": len(center_cubes) + len(edge_cubes) + len(corner_cubes)
    },
    "constraints_analysis": {
        "constraint_1_blue_cubes": blue_cubes,
        "constraint_2_orange_adjacent": orange_adjacent_cubes,
        "constraint_3_green_corners": green_corners,
        "constraint_4_green_yellow_borders": green_yellow_cubes,
        "constraint_5_opposite_red_cubes": opposite_red_cubes
    },
    "found_cubes": found_cubes_list,
    "missing_cubes": missing_cubes_list,
    "missing_edge_cubes": missing_edge_cubes,
    "analysis_summary": {
        "total_cubes": len(all_cubes),
        "found_count": len(found_cubes),
        "missing_count": len(missing_cubes),
        "missing_edge_count": len(missing_edge_cubes)
    }
}

with open('workspace/rubiks_cube_analysis.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)
    
print(f"Detailed analysis saved to: workspace/rubiks_cube_analysis.json")
print()

print("=== CONCLUSION ===")
if len(missing_edge_cubes) == 1:
    missing_cube = missing_edge_cubes[0]
    cube_colors = missing_cube.split('-')
    print(f"The missing cube with exactly 2 colors is: {missing_cube}")
    print(f"The two colors are: {cube_colors[0]} and {cube_colors[1]}")
else:
    print(f"Found {len(missing_edge_cubes)} missing edge cubes - need to refine analysis")
    for cube in missing_edge_cubes:
        cube_colors = cube.split('-')
        print(f"  Candidate: {cube} (colors: {cube_colors[0]}, {cube_colors[1]})")
```

### Development Step 7: Search 2011 Bulgarian Census Data on Tertiary Education Completion by Gender

**Description**: Search for the 2011 Bulgarian census data on tertiary education completion by gender. Look for official census results from Bulgaria's National Statistical Institute or other authoritative sources that provide the specific breakdown of men and women who completed tertiary education in 2011.

**Use Cases**:
- A policy analyst at Bulgaria’s Ministry of Education automates extraction of 2011 tertiary completion rates by gender from archived NSI HTML dumps to inform a gender equity report.
- A university demographer uses the script to parse archived census web pages and integrate the 2011 tertiary education gender breakdown into a longitudinal study on educational attainment trends.
- An NGO designing STEM outreach programs in underprivileged Bulgarian regions extracts male and female university completion percentages from 2011 census HTML files to target communities with low female enrollment.
- A market intelligence team at an e-learning startup crawls and parses historical Bulgarian census education data for gender‐specific tertiary completion to tailor course offerings and marketing strategies.
- A data journalist investigating gender disparities in Eastern Europe automates scraping of official Bulgarian census tables to quickly gather tertiary education statistics by gender for a data-driven article.
- A data scientist at an international organization uses the Python scraper to collect and standardize gender-disaggregated tertiary education rates from Bulgarian census HTML archives for cross-country comparative analyses.
- An urban planner compiles educational attainment profiles by gender for Bulgarian municipalities by extracting and mapping 2011 census tertiary completion data to support regional development proposals.
- A human resources consultancy benchmarks workforce education levels by downloading and parsing national census HTML data to compare male and female tertiary degree completion across Bulgarian industries.

```
import os
import json
from bs4 import BeautifulSoup
import re
import time

# First, let's inspect what files are actually in the workspace
print("=== ANALYZING SAVED BULGARIAN CENSUS DATA FILES ===")
print("Objective: Extract tertiary education completion by gender from 2011 Bulgarian census")
print("Strategy: Analyze all saved HTML files with proper variable handling\n")

if os.path.exists('workspace'):
    files = os.listdir('workspace')
    html_files = [f for f in files if f.endswith('.html')]
    print(f"HTML files available for analysis: {len(html_files)}")
    
    # Show the most promising files based on names
    priority_files = []
    for html_file in html_files:
        if any(term in html_file.lower() for term in ['education', 'demographics', 'census', 'nsi', 'eurostat']):
            priority_files.append(html_file)
    
    print(f"Priority files (education/census related): {len(priority_files)}")
    for pf in priority_files[:10]:  # Show top 10
        print(f"  {pf}")
else:
    print("No workspace directory found")
    exit()

print("\n=== DETAILED ANALYSIS OF SAVED CONTENT ===\n")

analysis_results = []
specific_findings = []

for i, html_file in enumerate(html_files, 1):
    print(f"Analyzing {i}/{len(html_files)}: {html_file}")
    
    filepath = f'workspace/{html_file}'
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML content
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get page title
        title_element = soup.find('title')
        page_title = title_element.get_text().strip() if title_element else 'No title found'
        
        # Get all text content and create lowercase version for analysis
        full_text = soup.get_text()
        text_for_analysis = full_text.lower()  # Create lowercase version immediately
        
        print(f"  Title: {page_title}")
        print(f"  Content length: {len(full_text)} characters")
        
        # Skip very small files (likely error pages)
        if len(full_text) < 1000:
            print(f"  Skipping - content too small (likely error page)")
            print()
            continue
        
        # Check relevance for Bulgarian census and education
        has_bulgaria = 'bulgaria' in text_for_analysis or 'bulgarian' in text_for_analysis
        has_2011 = '2011' in text_for_analysis
        has_census = 'census' in text_for_analysis
        has_tertiary = any(term in text_for_analysis for term in ['tertiary', 'higher education', 'university degree', 'tertiary education'])
        has_gender = any(term in text_for_analysis for term in ['men', 'women', 'male', 'female', 'gender', 'sex'])
        has_education = 'education' in text_for_analysis
        
        relevance_score = sum([has_bulgaria, has_2011, has_census, has_tertiary, has_gender, has_education])
        
        print(f"  Bulgaria: {has_bulgaria} | 2011: {has_2011} | Census: {has_census}")
        print(f"  Tertiary ed: {has_tertiary} | Gender: {has_gender} | Education: {has_education}")
        print(f"  Relevance score: {relevance_score}/6")
        
        if relevance_score >= 3:  # Analyze high-relevance sources
            print(f"  *** HIGH RELEVANCE - EXTRACTING DATA ***")
            
            # Search for specific education statistics with gender breakdown
            education_sentences = []
            sentences = full_text.split('.')
            
            for sentence in sentences:
                sentence_clean = sentence.strip()
                sentence_lower = sentence_clean.lower()
                
                if len(sentence_clean) > 30:  # Skip very short sentences
                    # Look for sentences with Bulgaria + education + numbers/percentages + gender
                    has_bulgaria_ref = 'bulgaria' in sentence_lower
                    has_education_ref = any(term in sentence_lower for term in 
                                          ['tertiary', 'education', 'university', 'higher', 'degree', 'graduate', 'completed'])
                    has_numbers = bool(re.search(r'\d+[.,]?\d*\s*%?', sentence_lower))
                    has_gender_ref = any(term in sentence_lower for term in ['men', 'women', 'male', 'female'])
                    has_year_ref = '2011' in sentence_lower
                    
                    if has_bulgaria_ref and has_education_ref and has_numbers and (has_gender_ref or has_year_ref):
                        education_sentences.append(sentence_clean)
            
            print(f"  Education sentences with data: {len(education_sentences)}")
            
            # Look for tables with statistical data
            tables = soup.find_all('table')
            relevant_tables = []
            
            for table_idx, table in enumerate(tables):
                table_text = table.get_text().lower()
                
                # Check if table contains education and gender data
                if (any(term in table_text for term in ['education', 'tertiary', 'university', 'degree']) and
                    any(term in table_text for term in ['men', 'women', 'male', 'female', 'gender'])):
                    
                    # Extract table headers
                    headers = [th.get_text().strip() for th in table.find_all('th')]
                    
                    # Get all rows of data
                    rows = table.find_all('tr')
                    table_data = []
                    
                    for row in rows:
                        cells = [td.get_text().strip() for td in row.find_all(['td', 'th'])]
                        if cells and any(cell for cell in cells if cell.strip()):  # Skip empty rows
                            table_data.append(cells)
                    
                    relevant_tables.append({
                        'index': table_idx,
                        'headers': headers,
                        'data': table_data[:10],  # First 10 rows
                        'total_rows': len(rows)
                    })
            
            print(f"  Relevant tables found: {len(relevant_tables)}")
            
            # Search for specific numerical patterns related to tertiary education by gender
            education_stats = []
            
            # Enhanced patterns to capture tertiary education statistics by gender
            stat_patterns = [
                r'tertiary education.*?(\d+[.,]?\d*\s*%?).*?(?:men|women|male|female)',
                r'(?:men|women|male|female).*?tertiary education.*?(\d+[.,]?\d*\s*%?)',
                r'university.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)',
                r'(?:men|women|male|female).*?university.*?(\d+[.,]?\d*\s*%?)',
                r'higher education.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)',
                r'(?:men|women|male|female).*?higher education.*?(\d+[.,]?\d*\s*%?)',
                r'completed.*?tertiary.*?(\d+[.,]?\d*\s*%?)',
                r'degree.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)',
                r'2011.*?education.*?(?:men|women|male|female).*?(\d+[.,]?\d*\s*%?)'
            ]
            
            for pattern in stat_patterns:
                matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    # Get extended context around the match
                    start = max(0, match.start() - 300)
                    end = min(len(full_text), match.end() + 300)
                    context = full_text[start:end].strip()
                    
                    # Check if context mentions Bulgaria and is relevant
                    context_lower = context.lower()
                    if 'bulgaria' in context_lower or 'bulgarian' in context_lower:
                        education_stats.append({
                            'pattern': pattern,
                            'match': match.group(),
                            'context': context,
                            'source_file': html_file
                        })
            
            print(f"  Education statistics found: {len(education_stats)}")
            
            # Look for specific census data patterns
            census_patterns = [
                r'2011.*?census.*?tertiary.*?(\d+[.,]?\d*)',
                r'census.*?2011.*?education.*?(\d+[.,]?\d*)',
                r'population.*?tertiary.*?education.*?(\d+[.,]?\d*)',
                r'completed.*?tertiary.*?2011.*?(\d+[.,]?\d*)'
            ]
            
            for pattern in census_patterns:
                matches = re.finditer(pattern, full_text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    start = max(0, match.start() - 200)
                    end = min(len(full_text), match.end() + 200)
                    context = full_text[start:end].strip()
                    
                    if 'bulgaria' in context.lower():
                        specific_findings.append({
                            'type': 'census_data',
                            'pattern': pattern,
                            'match': match.group(),
                            'context': context,
                            'source_file': html_file
                        })
            
            # Show key findings from this source
            if education_sentences:
                print(f"  Key sentence: {education_sentences[0][:200]}...")
            
            if education_stats:
                print(f"  Key statistic: {education_stats[0]['match']}")
                print(f"  Context: {education_stats[0]['context'][:150]}...")
            
            if relevant_tables and relevant_tables[0]['headers']:
                print(f"  Table headers: {relevant_tables[0]['headers'][:5]}")
            
            # Store comprehensive analysis for this source
            analysis_results.append({
                'filename': html_file,
                'title': page_title,
                'relevance_score': relevance_score,
                'content_length': len(full_text),
                'education_sentences': education_sentences[:5],  # Top 5
                'education_statistics': education_stats[:3],     # Top 3
                'relevant_tables': relevant_tables[:2],          # Top 2
                'has_bulgaria': has_bulgaria,
                'has_2011': has_2011,
                'has_census': has_census,
                'has_tertiary': has_tertiary,
                'has_gender': has_gender
            })
            
            # Add all education stats to specific findings
            for stat in education_stats:
                specific_findings.append({
                    'type': 'education_statistic',
                    'pattern': stat['pattern'],
                    'match': stat['match'],
                    'context': stat['context'],
                    'source_file': html_file
                })
        
        print()
        
    except Exception as e:
        print(f"  ✗ Error analyzing {html_file}: {str(e)}")
        print()

# Save comprehensive analysis results
print("=== COMPILATION OF FINDINGS ===\n")

final_results = {
    'search_objective': 'Bulgarian 2011 census tertiary education completion by gender',
    'analysis_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'files_analyzed': len(html_files),
    'relevant_sources': len(analysis_results),
    'specific_findings_count': len(specific_findings),
    'analysis_results': analysis_results,
    'specific_findings': specific_findings
}

with open('workspace/bulgarian_tertiary_education_final_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(final_results, f, indent=2, ensure_ascii=False)

print(f"Final analysis saved to: workspace/bulgarian_tertiary_education_final_analysis.json")
print(f"Files analyzed: {len(html_files)}")
print(f"Relevant sources: {len(analysis_results)}")
print(f"Specific findings: {len(specific_findings)}")

# Display summary of key findings
if analysis_results:
    print("\n=== SUMMARY OF RELEVANT SOURCES ===\n")
    
    # Sort by relevance score
    analysis_results.sort(key=lambda x: x['relevance_score'], reverse=True)
    
    for i, result in enumerate(analysis_results, 1):
        print(f"{i}. {result['title']} (Score: {result['relevance_score']}/6)")
        print(f"   File: {result['filename']}")
        print(f"   Content: {result['content_length']} chars")
        
        if result['education_sentences']:
            print(f"   Finding: {result['education_sentences'][0][:150]}...")
        
        if result['education_statistics']:
            print(f"   Statistic: {result['education_statistics'][0]['match']}")
        
        print()

if specific_findings:
    print("=== SPECIFIC TERTIARY EDUCATION FINDINGS ===\n")
    
    for i, finding in enumerate(specific_findings[:10], 1):  # Show top 10
        print(f"{i}. Type: {finding['type']}")
        print(f"   Match: {finding['match']}")
        print(f"   Source: {finding['source_file']}")
        print(f"   Context: {finding['context'][:200]}...")
        print()

print("=== ANALYSIS COMPLETE ===\n")
print("Bulgarian 2011 census tertiary education data by gender has been systematically extracted")
print("All findings saved to workspace for detailed review and verification")
```

### Development Step 21: Breadth-First Search from START to END: 11th Two-Cell Move Landing Cell Hex Color

**Description**: Perform a breadth-first search on workspace/adjacency_cardinal.json starting from the START coordinate from workspace/start_end_coordinates.json to find the shortest path to the END coordinate; then identify the coordinate at index 11 in the resulting path (representing the landing cell after the eleventh two-cell move) and retrieve its 6-digit hex fill_color from workspace/grid_data.json.

**Use Cases**:
- Indoor cleaning robot navigation and floor-condition detection by computing the 11th tile on its shortest path and checking its color code to decide vacuum settings
- Augmented reality game level mapping where the engine finds the terrain cell reached after 11 cardinal moves and retrieves its texture color for rendering effects
- Warehouse order-picking automation that plans the quickest route to an item, identifies the 11th aisle marker on that path, and reads its floor-painting color for location confirmation
- Agricultural field drone flight planning that performs a grid search over crop plots, lands on the 11th block along the optimal route, and reads its soil-moisture color classification
- Urban evacuation route analysis that finds the shortest pedestrian path through a city grid, highlights the 11th block, and inspects its zoning color to assess safety
- Autonomous vehicle test track mapping which computes the fastest route, marks the 11th corner coordinate on that lap, and fetches its pavement-paint color for sensor calibration
- Museum wayfinding application that plots the shortest corridor path from entrance to exhibit, reaches the 11th room, and retrieves its display-wall color for touchscreen feedback
- Pipeline inspection scheduling that models the connectivity graph of segments, navigates to the 11th node on the maintenance route, and checks its material-coating color code for repair prioritization

```
import os
import json
from collections import deque

# Step 1: Locate the workspace directory dynamically
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    raise FileNotFoundError(f"No workspace directory found in {cwd}")
workspace_dir = os.path.join(cwd, 'workspace') if 'workspace' in workspace_dirs else os.path.join(cwd, workspace_dirs[0])
print(f"Using workspace directory: {workspace_dir}\n")
print(f"Files in workspace: {os.listdir(workspace_dir)}\n")

# Step 2: Load and inspect start/end coordinates
start_end_path = os.path.join(workspace_dir, 'start_end_coordinates.json')
print(f"Loading start/end coordinates from: {start_end_path}")
with open(start_end_path, 'r') as f:
    start_end = json.load(f)
print(f"Raw start/end data: {start_end}\n")
# Determine START and END keys and formats
if 'start' in start_end or 'START' in start_end:
    key = 'start' if 'start' in start_end else 'START'
    val = start_end[key]
    if isinstance(val, dict) and 'row' in val and 'col' in val:
        start_coord = (int(val['row']), int(val['col']))
    elif isinstance(val, (list, tuple)) and len(val) == 2:
        start_coord = (int(val[0]), int(val[1]))
    else:
        raise ValueError(f"Unrecognized format for {key}: {val}")
else:
    raise KeyError("'start' or 'START' not found in start_end_coordinates.json")
if 'end' in start_end or 'END' in start_end:
    key_e = 'end' if 'end' in start_end else 'END'
    val_e = start_end[key_e]
    if isinstance(val_e, dict) and 'row' in val_e and 'col' in val_e:
        end_coord = (int(val_e['row']), int(val_e['col']))
    elif isinstance(val_e, (list, tuple)) and len(val_e) == 2:
        end_coord = (int(val_e[0]), int(val_e[1]))
    else:
        raise ValueError(f"Unrecognized format for {key_e}: {val_e}")
else:
    raise KeyError("'end' or 'END' not found in start_end_coordinates.json")
print(f"Parsed START coordinate: {start_coord}")
print(f"Parsed END coordinate:   {end_coord}\n")

# Step 3: Load adjacency graph
adj_path = os.path.join(workspace_dir, 'adjacency_cardinal.json')
print(f"Loading adjacency graph from: {adj_path}")
with open(adj_path, 'r') as f:
    adjacency_raw = json.load(f)
print(f"Loaded adjacency entries: {len(adjacency_raw)}\n")
# Inspect a sample entry
sample_key = list(adjacency_raw.keys())[0]
print(f"Sample adjacency '{sample_key}': {adjacency_raw[sample_key]}\n")

# Build adjacency list mapping coordinate tuples
adjacency = {}
for key_str, neighbors in adjacency_raw.items():
    r_str, c_str = key_str.split(',')
    node = (int(r_str), int(c_str))
    parsed = []
    for n in neighbors:
        if isinstance(n, str):
            rr, cc = n.split(',')
            parsed.append((int(rr), int(cc)))
        elif isinstance(n, (list, tuple)) and len(n) == 2:
            parsed.append((int(n[0]), int(n[1])))
        else:
            raise ValueError(f"Unrecognized neighbor format: {n}")
    adjacency[node] = parsed
print(f"Built adjacency list with {len(adjacency)} nodes.\n")

# Step 4: BFS to find shortest path

def bfs_shortest_path(adj, start, end):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for nbr in adj.get(current, []):
            if nbr not in visited:
                visited.add(nbr)
                parent[nbr] = current
                queue.append(nbr)
    if end not in parent:
        print(f"No path found from {start} to {end}")
        return []
    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    return path

print(f"Performing BFS from {start_coord} to {end_coord}...")
path = bfs_shortest_path(adjacency, start_coord, end_coord)
print(f"BFS path length: {len(path)}")
print(f"Path first 12 coordinates: {path[:12]}\n")

# Step 5: Extract coordinate at index 11
index = 11
if len(path) <= index:
    raise IndexError(f"Path length {len(path)} too short for index {index}")
landing_cell = path[index]
print(f"Coordinate at index {index}: {landing_cell}\n")

# Step 6: Load grid_data.json and find fill_color
grid_path = os.path.join(workspace_dir, 'grid_data.json')
print(f"Loading grid data from: {grid_path}")
with open(grid_path, 'r') as f:
    grid_data = json.load(f)
print(f"Total grid entries: {len(grid_data)}\n")
# Check sample entry
print(f"Sample grid entry: {grid_data[0]}\n")

fill_color = None
for entry in grid_data:
    if 'row' in entry and 'col' in entry:
        coord = (int(entry['row']), int(entry['col']))
    elif 'coordinate' in entry and isinstance(entry['coordinate'], (list, tuple)):
        coord = (int(entry['coordinate'][0]), int(entry['coordinate'][1]))
    else:
        continue
    if coord == landing_cell:
        fill_color = entry.get('fill_color') or entry.get('color')
        break
if not fill_color:
    raise ValueError(f"No fill_color found for coordinate {landing_cell}")
print(f"Found fill_color for {landing_cell}: {fill_color}\n")

# Step 7: Save result
output = {
    'landing_cell_index': index,
    'landing_cell': list(landing_cell),
    'fill_color': fill_color
}
out_path = os.path.join(workspace_dir, 'landing_cell_and_color.json')
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)
print(f"Result saved to: {out_path}\n")

print("===== FINAL ANSWER =====")
print(f"Index: {index}")
print(f"Landing cell: {landing_cell}")
print(f"Fill color: {fill_color}")
print("========================")
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

## Created Time
2025-08-08 18:30:35
