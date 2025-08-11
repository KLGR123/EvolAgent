# Developer Plan 02

## Plan
Parse and analyze the downloaded PDF files from the previous search to extract the specific sample standard deviations for the number of Reference Works in Life Sciences and Health Sciences domains from 2022. Focus on locating statistical tables, charts, or data sections that contain numerical values for Reference Works distribution across these academic domains. Calculate the difference between the two sample standard deviations to 3 decimal places as requested in the TASK.

## Description
This is the necessary next step because: (1) The developer successfully downloaded 5 PDF files totaling 54+ MB of authoritative Elsevier/ScienceDirect materials from 2022, including 'Elsevier Major Reference Works 2022' and related statistical sources, (2) The search phase identified high-relevance sources containing Reference Works distribution metrics and domain-specific data, (3) Expected outcome is to extract the specific sample standard deviation values for Life Sciences and Health Sciences Reference Works and compute their difference to 3 decimal places, (4) This completes the TASK by providing the precise numerical answer from the authoritative ScienceDirect statistical data

## Episodic Examples
### Development Step 2: Parse PDF to Extract Seahorse Island Accommodation Types and Compare Their Average Ratings

**Description**: Parse and analyze the attached PDF file data/gaia/2023/validation/67e8878b-5cef-4375-804e-e6291fdbe78a.pdf to extract information about all accommodations in Seahorse Island. Identify the different types of accommodations (such as hotels, motels, rental houses, campgrounds, etc.) and their corresponding ratings. Calculate the average rating for each accommodation type to determine which type has the highest average rating.

**Use Cases**:
- Tourism board of Seahorse Island uses automated PDF parsing to aggregate and compare average guest ratings of hotels, motels, rental houses, and campgrounds for their annual visitor satisfaction report.
- Hotel chain operations team extracts competitor ratings from public PDF brochures to benchmark performance across their various property types and pinpoint underperforming segments.
- Online travel agency automates extraction and analysis of PDF property review sheets to continuously update their website’s top-rated lodging categories based on up-to-date guest scores.
- Municipal parks department processes campground inspection PDF reports, categorizes sites (traditional campsite, glamping, RV hookup), and calculates average safety and satisfaction ratings for targeted maintenance planning.
- Market research firm parses supplier PDF catalogs of electronics, classifies items into laptops, tablets, and accessories, then computes average customer review scores to advise retail buyers on the highest-rating segments.
- Real estate investment group analyzes PDF property assessment documents, classifies residential units (apartments, condos, single-family homes), and computes average condition ratings to guide acquisition and renovation priorities.
- Event planning agency automates parsing of venue PDF data sheets, categorizes spaces (ballroom, conference rooms, outdoor pavilions), and computes average attendee feedback ratings to recommend the best fit for corporate retreats.

```
import os
import json
import re
from collections import defaultdict

print("=== SEAHORSE ISLAND ACCOMMODATION RATINGS ANALYSIS ===")
print("Step 2: Parse structured data and calculate average ratings by type\n")

# First, let's examine what files are available in the workspace
print("Examining workspace contents...")
workspace_files = []
for root, dirs, files in os.walk('workspace'):
    for file in files:
        file_path = os.path.join(root, file)
        workspace_files.append(file_path)
        print(f"Found: {file_path}")

if not workspace_files:
    print("No workspace files found yet.")

# Look for the raw content file that should contain the PDF data
raw_content_file = None
for file_path in workspace_files:
    if 'raw' in file_path.lower() and file_path.endswith('.txt'):
        raw_content_file = file_path
        break

if raw_content_file:
    print(f"\nFound raw content file: {raw_content_file}")
    print("Loading raw accommodation data...")
    
    with open(raw_content_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    print(f"Raw content length: {len(raw_content)} characters")
    print("\n=== RAW CONTENT PREVIEW ===\n")
    print(raw_content[:500] + "..." if len(raw_content) > 500 else raw_content)
else:
    # Use the content from the history since we know what it contains
    print("\nUsing accommodation data from PDF analysis...")
    raw_content = """Name Rating (out of 5)Vacancy Pool Sample Review
Hotels
Neptune's Palace 5 Yes Yes A hotel fit for a king.
Admiral Sturgeon 5 No Yes The breakfast was wonderful. The price was not.
Currents 4 Yes Yes The staff was helpful and accomodating.
The Laughing Gull 3 No Yes Great proximity to the beach.
Loach Towers 2 Yes No Good view of the water.
Motels
Sea Escape Inn 5 Yes Yes Don't let the "motel" look scare you. This place made for a clean and comfortable vacation.
Wash Inn 3 No Yes It was nice that they had laundry machines for guests.
Boulevard Motel 2 Yes No Real close to the gas station.
Good Motel 1 Yes No Name is false advertising.
Sea Larva Motel 0 Yes Yes Name is true advertising.
Rental Houses
Cape Super 4 No No The owner was very nice. A pleasure to talk to.
Bleek Island 3 No No We got a personalized box of chocolates upon our arrival. How sweet!
Pinedrift Avenue 4 Yes No This would be a good place if it wasn't an hour away from everything.
Ocean and Main 5 No Yes The location is great, if you don't mind the noise.
4th Street Cottage 5 No No The board games in the living room were nice to have.
Shelley's Place 4 Yes Yes The floorboards creaked too loud! Made it hard to walk and sleep at the same time.
Creakwood Creek 3 No Yes Tried fishing in the creek but nothing was biting.
Headrush Beach 3 No No The accomodations are rough, but the private beach is amazing.
Shiplap Cabin 3 Yes No Pretty sure this place is haunted.
Haddonfield House 1 Yes No The kitchen made it easy to prepare our own meals during our stay.
Campgrounds
The Glampground 4 Yes Yes Has the most Ultra HD TVs out of any campground I've been to.
Gull Crest 5 Yes Yes A bird defecated on our tent... never going back.
Barnacle Isle 3 No No Hard to bring our RV here when the only access to the island is by boat.
Cozy Wood 4 Yes Yes Not the most secluded, but clean and comfortable.
Gravel Lot Campground 1 Yes No No water or electric hookups for our camper... talk about "roughing it"."""

print("\n=== PARSING ACCOMMODATION DATA BY TYPE ===")

# Parse the structured data line by line
lines = raw_content.strip().split('\n')
print(f"Total lines to process: {len(lines)}")

# Initialize data structures
accommodation_types = ['Hotels', 'Motels', 'Rental Houses', 'Campgrounds']
accommodations_by_type = defaultdict(list)
current_category = None

print("\nParsing accommodations by category...")

for i, line in enumerate(lines):
    line = line.strip()
    print(f"Line {i+1}: {line}")
    
    # Skip the header line
    if 'Name Rating' in line and 'Vacancy Pool' in line:
        print("  -> Header line, skipping")
        continue
    
    # Check if this line is a category header
    if line in accommodation_types:
        current_category = line
        print(f"  -> Category found: {current_category}")
        continue
    
    # Skip empty lines
    if not line:
        print("  -> Empty line, skipping")
        continue
    
    # Parse accommodation data lines
    if current_category:
        # Extract rating using regex - look for the first digit 0-5 in the line
        rating_match = re.search(r'\b([0-5])\b', line)
        if rating_match:
            rating = int(rating_match.group(1))
            
            # Extract name (everything before the rating)
            rating_pos = rating_match.start()
            name = line[:rating_pos].strip()
            
            # Extract additional info after rating
            after_rating = line[rating_match.end():].strip()
            
            # Parse the rest of the line for vacancy, pool, and review
            parts = after_rating.split(None, 2)  # Split into max 3 parts
            vacancy = parts[0] if len(parts) > 0 else ''
            pool = parts[1] if len(parts) > 1 else ''
            review = parts[2] if len(parts) > 2 else ''
            
            accommodation = {
                'name': name,
                'category': current_category,
                'rating': rating,
                'vacancy': vacancy,
                'pool': pool,
                'review': review
            }
            
            accommodations_by_type[current_category].append(accommodation)
            print(f"  -> Parsed: {name} ({current_category}) - Rating: {rating}")
        else:
            print(f"  -> Could not find rating in line: {line}")

print("\n=== ACCOMMODATION PARSING RESULTS ===")

for category in accommodation_types:
    count = len(accommodations_by_type[category])
    print(f"{category}: {count} accommodations")
    for acc in accommodations_by_type[category]:
        print(f"  - {acc['name']}: {acc['rating']}/5")

print("\n=== CALCULATING AVERAGE RATINGS BY TYPE ===")

# Calculate average ratings for each accommodation type
average_ratings = {}
rating_details = {}

for category in accommodation_types:
    accommodations = accommodations_by_type[category]
    if accommodations:
        ratings = [acc['rating'] for acc in accommodations]
        total_ratings = sum(ratings)
        count = len(ratings)
        average = total_ratings / count
        
        average_ratings[category] = average
        rating_details[category] = {
            'count': count,
            'total': total_ratings,
            'average': average,
            'ratings': ratings,
            'accommodations': accommodations
        }
        
        print(f"{category}:")
        print(f"  Count: {count} accommodations")
        print(f"  Individual ratings: {ratings}")
        print(f"  Total: {total_ratings}")
        print(f"  Average: {average:.2f}/5")
        print()
    else:
        print(f"{category}: No accommodations found")
        average_ratings[category] = 0

print("=== FINAL RESULTS ===")
print("Average ratings by accommodation type:")
print("-" * 40)

# Sort by average rating to find the highest
sorted_averages = sorted(average_ratings.items(), key=lambda x: x[1], reverse=True)

for i, (category, avg_rating) in enumerate(sorted_averages):
    if avg_rating > 0:
        rank_symbol = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "  "
        print(f"{rank_symbol} {category}: {avg_rating:.2f}/5 ({rating_details[category]['count']} accommodations)")
    else:
        print(f"   {category}: No data")

# Identify the winner
if sorted_averages and sorted_averages[0][1] > 0:
    winner_category = sorted_averages[0][0]
    winner_average = sorted_averages[0][1]
    winner_count = rating_details[winner_category]['count']
    
    print(f"\n*** ANSWER ***")
    print(f"The accommodation type with the HIGHEST AVERAGE RATING is:")
    print(f"🏆 {winner_category.upper()} with an average rating of {winner_average:.2f}/5")
    print(f"(Based on {winner_count} accommodations)")
    
    # Show all accommodations in the winning category
    print(f"\n{winner_category} accommodations and their ratings:")
    for acc in rating_details[winner_category]['accommodations']:
        print(f"  • {acc['name']}: {acc['rating']}/5")
else:
    print("\n*** ERROR: No valid accommodation data found ***")

# Save detailed results
results_data = {
    'accommodation_types': accommodation_types,
    'accommodations_by_type': dict(accommodations_by_type),
    'average_ratings': average_ratings,
    'rating_details': rating_details,
    'highest_rated_type': sorted_averages[0] if sorted_averages and sorted_averages[0][1] > 0 else None,
    'analysis_summary': f"Analyzed {sum(len(accs) for accs in accommodations_by_type.values())} total accommodations across {len(accommodation_types)} categories"
}

with open('workspace/accommodation_ratings_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(results_data, f, indent=2, ensure_ascii=False)

# Create a summary report
summary_report = f"""SEAHORSE ISLAND ACCOMMODATION RATINGS ANALYSIS
{'='*50}

TOTAL ACCOMMODATIONS ANALYZED: {sum(len(accs) for accs in accommodations_by_type.values())}

AVERAGE RATINGS BY TYPE:
{'-'*30}
"""

for category, avg_rating in sorted_averages:
    if avg_rating > 0:
        count = rating_details[category]['count']
        summary_report += f"{category}: {avg_rating:.2f}/5 ({count} properties)\n"

if sorted_averages and sorted_averages[0][1] > 0:
    winner = sorted_averages[0]
    summary_report += f"\n🏆 HIGHEST RATED TYPE: {winner[0]} ({winner[1]:.2f}/5)\n"

with open('workspace/accommodation_ratings_summary.txt', 'w', encoding='utf-8') as f:
    f.write(summary_report)

print(f"\nDetailed analysis saved to: workspace/accommodation_ratings_analysis.json")
print(f"Summary report saved to: workspace/accommodation_ratings_summary.txt")
print("\n=== ANALYSIS COMPLETE ===")
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

### Development Step 59: Extract Fish Bag Volume (m³) from dragon_diet_fish_bag.pdf

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Aquaculture feed calculation and ration planning: automatically extract fish bag volume from technical spec PDFs to determine optimal feed-to-water ratios on commercial fish farms
- Environmental compliance reporting for fisheries: parse containment vessel volumes in fish bag specification documents to generate accurate data for water discharge permits and regulatory submissions
- Marine biology research on stocking densities: batch process PDF manuals to aggregate fish bag volumes for habitat density simulations and ecological impact studies
- Cold chain logistics optimization in seafood transport: extract packaging container volumes from vendor PDFs to optimize refrigerated truck loading plans and minimize spoilage
- Manufacturing quality control in fish bag production: cross-validate extracted bag volumes from design documents against actual measurements to identify deviations and ensure product consistency
- Inventory catalog maintenance for aquaculture suppliers: automate ingestion of fish bag volume data from supplier PDFs into product databases to streamline SKU management and ordering processes
- Insurance risk assessment for fisheries operations: retrieve containment volumes from safety data sheets to model flood or contamination scenarios and support policy underwriting

```
import os
import re
from PyPDF2 import PdfReader

print("=== FISH BAG VOLUME EXTRACTION ===")
# Step 1: Locate the PDF in workspace
dir_path = 'workspace'
if not os.path.isdir(dir_path):
    print(f"Error: workspace directory not found at '{dir_path}'")
    exit(1)

files = os.listdir(dir_path)
print(f"Files in '{dir_path}': {files}")

pdf_name = None
for f in files:
    if f.lower().endswith('.pdf') and 'dragon_diet_fish_bag' in f.lower():
        pdf_name = f
        break

if not pdf_name:
    print("Error: 'dragon_diet_fish_bag.pdf' not found in workspace directory.")
    exit(1)

pdf_path = os.path.join(dir_path, pdf_name)
print(f"Found PDF: {pdf_path}\n")

# Step 2: Read PDF pages and search for volume references
reader = PdfReader(pdf_path)
num_pages = len(reader.pages)
print(f"Total pages in PDF: {num_pages}\n")

volume_pattern = re.compile(r"(\d+(?:[\.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)
keyword_terms = ['volume', 'm3', 'm³', 'cubic meter']

findings = []
for i, page in enumerate(reader.pages):
    try:
        text = page.extract_text() or ''
    except Exception as e:
        print(f"Error extracting text from page {i+1}: {e}")
        continue
    lower = text.lower()
    # Check if any volume-related keyword on this page
    if any(term in lower for term in keyword_terms):
        print(f"\n--- Page {i+1} contains volume-related terms ---")
        # Extract all matches for volume_pattern
        for match in volume_pattern.finditer(text):
            vol_str = match.group(1)
            unit_str = match.group(0)[len(vol_str):].strip()
            # Provide context around match
            start, end = match.start(), match.end()
            ctx_start = max(0, start-50)
            ctx_end = min(len(text), end+50)
            context = text[ctx_start:ctx_end].replace("\n", " ")
            print(f"Match on page {i+1}: '{match.group(0)}' -> value: {vol_str} unit: {unit_str}")
            print(f"Context: ...{context.strip()}...")
            findings.append({
                'page': i+1,
                'value': vol_str,
                'unit': unit_str,
                'context': context.strip()
            })

if not findings:
    print("\nNo volume number found matching the pattern 'number + m3/cubic meters'.")
else:
    # Take the first finding as the reported volume
    first = findings[0]
    volume_value = first['value']
    unit = first['unit']
    print(f"\n>>> Extracted fish bag volume: {volume_value} {unit} (from page {first['page']})")
    # Save to workspace file
    out_path = os.path.join(dir_path, 'fish_bag_volume.txt')
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

## Created Time
2025-08-11 06:28:53
