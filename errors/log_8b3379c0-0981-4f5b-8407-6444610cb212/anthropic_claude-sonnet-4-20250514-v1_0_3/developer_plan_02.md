# Developer Plan 02

## Plan
Convert the final answer from feet to meters since the TASK specifically requests the measurement in meters. Calculate the conversion from 30 feet to meters using the standard conversion factor (1 foot = 0.3048 meters) and provide only the numerical value as requested.

## Description
This conversion step is necessary because: (1) The developer found that the Giant Pacific Octopus (identified as #9) has a maximum length of 30 feet according to Monterey Bay Aquarium data, (2) The TASK specifically requests the answer in meters with just the number, (3) Expected outcome is the precise metric conversion of 30 feet to meters, (4) This provides the final numerical answer in the correct units as specified in the TASK requirements.

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

### Development Step 62: Extract Fish Bag Volume in Cubic Meters from Dragon Diet PDF

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Aquaculture facility management: automated extraction of fish tank and bag volume specs from operational PDFs to optimize feeding schedules and stocking densities
- Laboratory protocol automation: retrieving reagent container volumes from protocol PDFs for precise solution preparation in chemical experiments
- Marine biology research: parsing scuba equipment manuals to extract air tank capacities for dive plan optimization and safety checks
- Shipping and logistics automation: extracting cargo container volume dimensions from transport specification PDFs to calculate load capacity and plan routes
- Aquarium retail operations: reading product datasheet PDFs to import aquarium tank and accessory volumes into inventory systems for online catalog listings
- Construction equipment planning: extracting concrete mixer drum volumes from machinery manuals to integrate into resource allocation and project scheduling tools
- Environmental impact assessment: pulling pollutant dispersion chamber volumes from technical reports to model air quality and regulatory compliance
- Food processing quality control: retrieving silo and packaging bag volumes from supplier specification PDFs to synchronize batch production and packaging workflows

```
import os
import re
from PyPDF2 import PdfReader

print("=== FISH BAG VOLUME EXTRACTION (FIXED VARIABLE NAMES) ===")

# Step 1: Locate the workspace directory (handle random suffixes)
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    print("Error: No directory starting with 'workspace' found in current working directory.")
    exit(1)
workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Step 2: Locate the dragon_diet_fish_bag PDF file
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

# Regex to capture number + cubic meter units
time.sleep(0)
volume_pattern = re.compile(r"(\d+(?:[.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)
keyword_terms = ['volume', 'm3', 'm³', 'cubic meter']

findings = []
for i, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ''
    text_lower = text.lower()  # define lowercase copy before use

    # Print a short preview for debugging
    print(f"--- Page {i} Preview ---")
    preview = text.replace('\n', ' ')[:200]
    print(preview + ('...' if len(text) > 200 else ''))

    # Check for any volume-related keyword in lowercase text
    if any(term in text_lower for term in keyword_terms):
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
    with open(out_path, 'w') as f:
        f.write(f"{volume_value} {unit}\n")
    print(f"Volume saved to: {out_path}")

```

### Development Step 60: Locate and Extract Fish Bag Volume (m³) from dragon_diet_fish_bag.pdf

**Description**: Search within workspace/dragon_diet_fish_bag.pdf for the section or table where the fish bag volume is calculated, locate the numeric value reported in cubic meters, and extract that volume number directly from the PDF.

**Use Cases**:
- Aquaculture feed supply chain automation: extract fish feed bag volume from supplier PDFs to update ERP inventory levels and trigger automatic reorder processes
- Wildlife conservation project planning: parse field kit datasheet PDFs to obtain fish transport bag volumes for designing safe relocation protocols
- Environmental modeling and water quality assessment: researchers pull bag volume specifications from technical reports to calibrate pollutant dispersion simulations
- Industrial packaging quality control: QA engineers validate fish feed bag volumetric specs from manufacturer PDFs to calibrate automated filling machinery
- Marine biology lab sample management: laboratory staff extract container volumes from equipment datasheets to standardize specimen storage records
- Regulatory compliance auditing for feed manufacturers: auditors automatically extract packaging volume figures from product spec PDFs to verify labeling accuracy
- E-commerce product catalog enrichment: online retailers parse supplier PDF manuals to populate fish feed bag volume attributes in their inventory database

```
import os
import re
from PyPDF2 import PdfReader

print("=== FIXED FISH BAG VOLUME EXTRACTION ===")

# Step 1: Locate the workspace directory (robust to random suffixes)
cwd = os.getcwd()
workspace_dirs = [d for d in os.listdir(cwd) if os.path.isdir(d) and d.startswith('workspace')]
if not workspace_dirs:
    print("Error: No directory starting with 'workspace' found in current working directory.")
    exit(1)
workspace_dir = workspace_dirs[0]
print(f"Using workspace directory: {workspace_dir}\n")

# Step 2: Find the dragon_diet_fish_bag PDF file
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

# Regex to capture number + cubic meter units
volume_pattern = re.compile(r"(\d+(?:[\.,]\d+)*)\s*(?:m\^?3|m³|cubic meters?)", re.IGNORECASE)
keyword_terms = ['volume', 'm3', 'm³', 'cubic meter']

findings = []
for i, page in enumerate(reader.pages):
    text = page.extract_text() or ''
    text_lower = text.lower()

    # Print a short preview for debugging
    print(f"--- Page {i+1} Preview ---")
    preview = text[:200].replace('\n', ' ')
    print(preview + ('...' if len(text) > 200 else ''))

    # Check for any volume-related keyword
    if any(term in text_lower for term in keyword_terms):
        print(f"Page {i+1} contains volume-related term(s). Searching regex matches...")
        for match in volume_pattern.finditer(text):
            full_match = match.group(0)
            vol_str = match.group(1)
            unit_str = full_match[len(vol_str):].strip()
            start, end = match.start(), match.end()
            context = text[max(0, start-50):min(len(text), end+50)].replace('\n', ' ')

            print(f"Match on page {i+1}: '{full_match}' -> value: {vol_str} unit: {unit_str}")
            print(f"Context: ...{context.strip()}...")

            findings.append({
                'page': i+1,
                'value': vol_str,
                'unit': unit_str,
                'context': context.strip()
            })

if not findings:
    print("\nNo volume number found matching the pattern.")
else:
    first = findings[0]
    volume_value = first['value']
    unit = first['unit']
    page_no = first['page']
    print(f"\n>>> Extracted fish bag volume: {volume_value} {unit} (from page {page_no})")

    # Step 4: Save result to workspace
    out_path = os.path.join(workspace_dir, 'fish_bag_volume.txt')
    with open(out_path, 'w') as f:
        f.write(f"{volume_value} {unit}\n")
    print(f"Volume saved to: {out_path}")
```

## Created Time
2025-08-11 08:29:34
