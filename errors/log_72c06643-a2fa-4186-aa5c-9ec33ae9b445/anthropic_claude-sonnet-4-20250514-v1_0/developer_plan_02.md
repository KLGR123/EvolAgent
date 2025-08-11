# Developer Plan 02

## Plan
Research the specific conditions at the bottom of the Marianas Trench, focusing on the maximum depth, pressure at that depth, and the peak temperature mentioned in the TASK. Extract the exact values for pressure (in Pa or MPa) and temperature (in Kelvin) that will be used with the Freon-12 properties to calculate the refrigerant's density and volume under these extreme conditions.

## Description
This is the necessary next step because: (1) We have successfully obtained comprehensive Freon-12 thermodynamic properties including critical parameters and equation of state data needed for high-pressure calculations, (2) To calculate the volume of 0.312 kg Freon-12 under Marianas Trench conditions, we need the specific pressure and peak temperature values at the trench bottom, (3) Expected outcome is to obtain the exact depth, pressure (likely around 110+ MPa at ~11 km depth), and peak temperature at the Marianas Trench bottom, (4) This will provide the P-T conditions needed to use the Peng-Robinson equation of state with the Freon-12 properties to calculate density and convert to volume in milliliters

## Episodic Examples
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

## Created Time
2025-08-11 10:25:06
