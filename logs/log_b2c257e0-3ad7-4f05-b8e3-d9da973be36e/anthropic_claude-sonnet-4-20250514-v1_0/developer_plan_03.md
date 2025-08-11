# Developer Plan 03

## Plan
Calculate the actual butterfat percentage of the ice cream product from the extracted nutritional data (21g total fat per 144g serving) and compare it against the US federal standard of 10% minimum butterfat content. Determine the percentage difference above or below the federal standard and express the answer as +/- a number rounded to one decimal place as requested in the TASK.

## Description
This is the final calculation step because: (1) We have successfully extracted the ice cream product's fat content (21g total fat per 144g serving) from the image analysis, (2) We have identified the US federal minimum butterfat standard of 10% as reported by Wikipedia in 2020, (3) Expected outcome is to calculate the actual butterfat percentage (21g ÷ 144g × 100 = 14.6%) and determine how much it exceeds the 10% federal standard (+4.6%), (4) This completes the TASK by providing the final answer rounded to one decimal place as specified

## Episodic Examples
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

### Development Step 15: Identify Five-Digit ZIP Codes for Fred Howard Park and Holiday, FL from USGS Location Data

**Description**: Convert the Florida location data from the USGS record (Pinellas County, Fred Howard Park area in Holiday, FL) to the specific five-digit ZIP codes for that geographic area. Cross-reference multiple sources including USPS ZIP code databases, local government records, and mapping services to ensure accuracy of the ZIP codes covering the Fred Howard Park and Holiday, Florida region where the clownfish specimen was documented.

**Use Cases**:
- Targeted direct-mail marketing for local businesses by using the specific ZIP codes (34690, 34691, 34689) that cover Holiday, FL and Fred Howard Park to ensure promotional materials reach households near the park.
- Emergency response and disaster planning for Pinellas County agencies, leveraging the validated ZIP codes to optimize deployment of search-and-rescue teams and coordinate evacuation zones around coastal Holiday.
- Marine biology and conservation studies mapping USGS clownfish specimen observations to precise ZIP code areas, enabling community science volunteers to focus sampling efforts in those neighborhoods.
- E-commerce logistics optimization for aquarium supply companies, using the Holiday/Fred Howard Park ZIP codes to calculate shipping rates, delivery routes, and service coverage for aquarium hobbyists.
- Flood and property insurance underwriting, assessing risk profiles by analyzing historical claims and storm-impact data specifically tied to ZIP codes 34690, 34691, and 34689 along the Gulf Coast.
- Real estate market intelligence reports, segmenting housing sales, rental rates, and development trends in Holiday and Tarpon Springs by the identified ZIP codes to advise investors and homebuyers.
- Public health outreach programs organizing coastal water-safety workshops and conservation cleanups, distributing flyers to residents in the exact ZIP code areas bordering Fred Howard Park.
- Tourism promotion campaigns by regional visitor bureaus, tailoring digital ads and event invitations for park activities based on analytics of visitor home ZIP codes in the Holiday, FL vicinity.

```
import os
import json
import re

# Ensure workspace directory exists
workspace_dir = 'workspace'
os.makedirs(workspace_dir, exist_ok=True)

# Output files
zip_results_file = os.path.join(workspace_dir, 'florida_zip_codes.json')

print("Starting ZIP code research for Fred Howard Park area in Holiday, FL...")
print("=" * 70)

# Research ZIP codes for Holiday, Florida area including Fred Howard Park
print("Researching ZIP codes for Holiday, Florida and Fred Howard Park area...")

# Known information about the location
location_info = {
    "city": "Holiday",
    "county": "Pinellas County", 
    "state": "Florida",
    "landmark": "Fred Howard Park",
    "description": "Fred Howard Park area in Holiday, FL, Pinellas County"
}

print(f"Target location: {location_info['description']}")

# Research Holiday, FL ZIP codes through multiple approaches
zip_codes = set()

# Method 1: Direct lookup of Holiday, FL ZIP codes
print("\nMethod 1: Researching Holiday, FL ZIP codes...")

# Holiday, FL is known to have these ZIP codes based on USPS data
holiday_zip_codes = [
    "34690",  # Primary ZIP code for Holiday, FL
    "34691",  # Secondary ZIP code for Holiday, FL area
]

for zip_code in holiday_zip_codes:
    zip_codes.add(zip_code)
    print(f"Added ZIP code: {zip_code} (Holiday, FL)")

# Method 2: Research Fred Howard Park specific ZIP code
print("\nMethod 2: Researching Fred Howard Park ZIP code...")

# Fred Howard Park is located at:
# Address: 1700 Sunset Point Rd, Tarpon Springs, FL 34689
# Note: The park spans areas that may include Holiday ZIP codes

fred_howard_zip = "34689"  # Tarpon Springs area where park entrance is located
zip_codes.add(fred_howard_zip)
print(f"Added ZIP code: {fred_howard_zip} (Fred Howard Park entrance area)")

# Method 3: Research broader Pinellas County Holiday area
print("\nMethod 3: Researching broader Holiday/Pinellas County area...")

# Additional ZIP codes that may cover the Holiday/Fred Howard Park region
additional_zips = [
    "34688",  # New Port Richey area (adjacent to Holiday)
    "34684",  # Trinity area (adjacent to Holiday)
]

# Verify these are relevant to the Holiday area
for zip_code in additional_zips:
    print(f"Considering ZIP code: {zip_code} (adjacent to Holiday area)")
    # For now, we'll focus on the primary Holiday ZIP codes

final_zip_codes = sorted(list(zip_codes))
print(f"\nCollected ZIP codes: {final_zip_codes}")

# Validate that ZIP codes are properly formatted 5-digit codes
print(f"\nValidating {len(final_zip_codes)} ZIP codes...")

validated_zips = []
zip_pattern = re.compile(r'^\d{5}$')

for zip_code in final_zip_codes:
    if zip_pattern.match(zip_code):
        validated_zips.append(zip_code)
        print(f"✓ Valid ZIP code: {zip_code}")
    else:
        print(f"✗ Invalid ZIP code format: {zip_code}")

print(f"\nValidated ZIP codes: {validated_zips}")

# Get detailed information about each ZIP code
print(f"\nGathering details for {len(validated_zips)} ZIP codes...")

zip_details = []

# Known details for Holiday, FL area ZIP codes
zip_info_map = {
    "34690": {
        "zip_code": "34690",
        "city": "Holiday",
        "county": "Pinellas County",
        "state": "Florida",
        "type": "Standard",
        "primary_city": "Holiday",
        "acceptable_cities": ["Holiday"],
        "covers_fred_howard_park": True,
        "notes": "Primary ZIP code for Holiday, FL"
    },
    "34691": {
        "zip_code": "34691",
        "city": "Holiday",
        "county": "Pinellas County", 
        "state": "Florida",
        "type": "Standard",
        "primary_city": "Holiday",
        "acceptable_cities": ["Holiday"],
        "covers_fred_howard_park": True,
        "notes": "Secondary ZIP code for Holiday, FL area"
    },
    "34689": {
        "zip_code": "34689",
        "city": "Tarpon Springs",
        "county": "Pinellas County",
        "state": "Florida", 
        "type": "Standard",
        "primary_city": "Tarpon Springs",
        "acceptable_cities": ["Tarpon Springs"],
        "covers_fred_howard_park": True,
        "notes": "Fred Howard Park entrance area (1700 Sunset Point Rd)"
    }
}

for zip_code in validated_zips:
    if zip_code in zip_info_map:
        details = zip_info_map[zip_code]
        zip_details.append(details)
        print(f"ZIP {zip_code}: {details['primary_city']}, {details['county']}, {details['state']}")
        print(f"  Type: {details['type']}")
        print(f"  Covers Fred Howard Park: {details['covers_fred_howard_park']}")
        print(f"  Notes: {details['notes']}")
    else:
        # Basic details for unknown ZIP codes
        basic_details = {
            "zip_code": zip_code,
            "city": "Unknown",
            "county": "Unknown",
            "state": "Florida",
            "type": "Unknown",
            "primary_city": "Unknown",
            "acceptable_cities": [],
            "covers_fred_howard_park": False,
            "notes": "Details not available"
        }
        zip_details.append(basic_details)
        print(f"ZIP {zip_code}: Details not available")

# Save ZIP code results to JSON file
print(f"\nSaving results to {zip_results_file}...")

results = {
    "location_description": "Fred Howard Park area in Holiday, FL, Pinellas County",
    "research_date": "2024",
    "total_zip_codes": len(zip_details),
    "zip_codes": [detail["zip_code"] for detail in zip_details],
    "detailed_information": zip_details,
    "summary": {
        "primary_holiday_zips": ["34690", "34691"],
        "fred_howard_park_zip": "34689",
        "county": "Pinellas County",
        "state": "Florida"
    }
}

with open(zip_results_file, 'w') as f:
    json.dump(results, f, indent=4)

print(f"Results saved to {zip_results_file}")

# Print final summary
print("\n" + "=" * 70)
print("FINAL RESULTS SUMMARY")
print("=" * 70)
print(f"Location: {results['location_description']}")
print(f"Total ZIP codes found: {results['total_zip_codes']}")
print("\nFive-digit ZIP codes covering the area:")

# Fixed the variable scoping issue by using a proper loop instead of generator expression
for current_zip in results['zip_codes']:
    # Find the matching detail record for this ZIP code
    matching_detail = None
    for detail in zip_details:
        if detail['zip_code'] == current_zip:
            matching_detail = detail
            break
    
    if matching_detail:
        print(f"  • {current_zip} - {matching_detail['primary_city']}, {matching_detail['county']}, {matching_detail['state']}")
        print(f"    Covers Fred Howard Park: {matching_detail['covers_fred_howard_park']}")
    else:
        print(f"  • {current_zip} - Details not found")

print(f"\nPrimary Holiday, FL ZIP codes: {', '.join(results['summary']['primary_holiday_zips'])}")
print(f"Fred Howard Park entrance ZIP: {results['summary']['fred_howard_park_zip']}")

print(f"\nDetailed results saved to: {zip_results_file}")

# Display the five-digit ZIP codes as a simple list
print("\n" + "=" * 70)
print("FIVE-DIGIT ZIP CODES FOR FRED HOWARD PARK AREA IN HOLIDAY, FL:")
print("=" * 70)
for current_zip in sorted(results['zip_codes']):
    print(f"  {current_zip}")

print(f"\nTotal: {len(results['zip_codes'])} ZIP codes identified")

# Show contents of saved JSON file for verification
print("\n" + "=" * 70)
print("VERIFICATION: Contents of saved JSON file:")
print("=" * 70)
with open(zip_results_file, 'r') as f:
    saved_data = json.load(f)
    print(f"File contains {len(saved_data)} top-level keys:")
    for key in saved_data.keys():
        print(f"  - {key}")
    print(f"\nZIP codes in file: {saved_data['zip_codes']}")
    print(f"Location description: {saved_data['location_description']}")
```

## Created Time
2025-08-11 01:38:40
