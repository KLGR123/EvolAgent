# Developer Plan 03

## Plan
Analyze the cross-referencing results from workspace/complete_bibliography_analysis.json to determine the most likely reference number matches for each of the 6 table captions from the Excel file. Use the keyword matching scores, semantic similarity analysis, and content relevance to assign the appropriate reference numbers (1-21) to each table caption in the order they appear from top to bottom in the Excel file, then provide the final comma-separated list of reference numbers.

## Description
This is the final step because: (1) We have successfully extracted both the 6 table captions from the Excel file and the complete 21-reference bibliography from the 'Trans fatty acid contents in chocolates and chocolate wafers in Turkey' paper, (2) The developer has performed comprehensive cross-referencing analysis with keyword matching and semantic similarity scoring between table captions and bibliography entries, (3) Expected outcome is to determine the best reference number matches for each table caption based on the analysis results and provide the final answer as a comma-separated list in the order requested, (4) This completes the TASK by filling in the missing reference numbers that would go in the Excel file cells from top to bottom

## Episodic Examples
### Development Step 1: Excel Grid Parsing: Record Cell Coordinates, Text, Fill Colors, Identify START and END Cells

**Description**: Parse and analyze the attached Excel file data/gaia/2023/validation/65afbc8a-89ca-4ad5-8d62-355bb401f61d.xlsx to extract the complete grid structure: record for each cell its row–column coordinate, displayed text, and fill color as a 6-digit hex code, then identify the coordinates of the cell containing 'START' and the cell containing 'END'.

**Use Cases**:
- Project timeline extraction for construction management: parse a color-coded Gantt chart in Excel to import each task’s grid position, label, and scheduling colors, then automatically locate the “START” kickoff milestone and “END” completion point.
- Retail shelf planogram automation: extract the full store shelving grid with product names and color-coded stock levels from an Excel layout, identify the beginning (“START”) and end (“END”) of each aisle for dynamic planogram updates.
- AGV navigation map generation in manufacturing: read an Excel-based factory floor grid with zones highlighted by fill color, output precise coordinates for every cell, and locate the “START” docking station and “END” delivery bay for autonomous guided vehicles.
- Classroom seating performance analysis: parse a teacher’s Excel seating chart where student names and test scores are color-coded, record each desk’s coordinates and find designated “START” and “END” rows for group activities arrangement.
- Game level prototyping: convert a level design represented in Excel cells (with obstacles and power-ups color-coded) into JSON; pinpoint the “START” spawn cell and “END” exit cell for rapid engine import.
- Real estate floorplan digitization: extract room labels, dimensions, and color-coded zones (e.g., living, kitchen, bedrooms) from an Excel blueprint, capturing each cell’s coordinates and fill color, then identify the main “START” entrance and emergency “END” exits.
- High-throughput screening data mapping in biotech: interpret a microtiter plate layout from Excel, record each well’s row–column address, sample identifier, and color-coded assay result, and locate the “START” reference well and “END” control well for automated analysis.

```
import os
import json
from openpyxl import load_workbook

# Path to the Excel file
xlsx_path = 'data/gaia/2023/validation/65afbc8a-89ca-4ad5-8d62-355bb401f61d.xlsx'

print('=== EXCEL GRID EXTRACTION SCRIPT ===')
# Verify the file exists
if not os.path.exists(xlsx_path):
    print(f"Error: Excel file not found at '{xlsx_path}'")
    exit(1)
print(f"Found Excel file: {xlsx_path}")

# Load workbook without evaluating formulas (to preserve formatting)
wb = load_workbook(xlsx_path, data_only=False)
sheet = wb.active
print(f"Active sheet: '{sheet.title}'")

# Determine the grid dimensions
max_row = sheet.max_row
max_col = sheet.max_column
print(f"Sheet dimensions: {max_row} rows x {max_col} columns")

# Prepare containers for all cells and START/END coordinates
all_cells = []
start_coord = None
end_coord = None

print('Beginning cell-by-cell analysis...')
for row in range(1, max_row + 1):
    for col in range(1, max_col + 1):
        cell = sheet.cell(row=row, column=col)
        raw_value = cell.value
        # Normalize displayed text
        display_text = str(raw_value) if raw_value is not None else ''

        # Extract fill color (ARGB -> take last 6 hex digits)
        fill = cell.fill
        hex_color = ''
        if hasattr(fill, 'start_color') and fill.start_color is not None:
            rgb = getattr(fill.start_color, 'rgb', None)
            # rgb is often in the form 'FFRRGGBB'
            if isinstance(rgb, str) and len(rgb) == 8:
                hex_color = rgb[-6:]

        # Record this cell's data
        cell_record = {
            'row': row,
            'col': col,
            'value': display_text,
            'fill_color': hex_color
        }
        all_cells.append(cell_record)

        # Check for START/END markers (exact match)
        if display_text == 'START':
            start_coord = {'row': row, 'col': col}
            print(f"-> Found START at row {row}, col {col}")
        elif display_text == 'END':
            end_coord = {'row': row, 'col': col}
            print(f"-> Found END at row {row}, col {col}")

print('Cell analysis complete.')

# Summarize findings
total_cells = len(all_cells)
print(f"Total cells recorded: {total_cells}")
if not start_coord:
    print('Warning: START cell not found in sheet.')
if not end_coord:
    print('Warning: END cell not found in sheet.')

# Save the full grid data and the START/END coordinates to workspace
os.makedirs('workspace', exist_ok=True)

grid_output_path = 'workspace/grid_data.json'
with open(grid_output_path, 'w', encoding='utf-8') as f:
    json.dump(all_cells, f, indent=2)
print(f"Saved full grid data to: {grid_output_path}")

coords = {
    'START': start_coord,
    'END': end_coord
}
coords_output_path = 'workspace/start_end_coordinates.json'
with open(coords_output_path, 'w', encoding='utf-8') as f:
    json.dump(coords, f, indent=2)
print(f"Saved START/END coordinates to: {coords_output_path}")

print('Script finished.')
```

### Development Step 3: Extract and Format Ascending Comma-Delimited Page Numbers for Calculus Midterm Preparation

**Description**: Extract and format the page numbers from the completed audio analysis into the final comma-delimited list in ascending order as requested. Based on the developer's results showing the corrected page list [132, 133, 134, 197, 245, 1197], format this into the exact output format specified in the TASK: a comma-delimited list of page numbers in ascending order for the Calculus mid-term study preparation.

**Use Cases**:
- Legal deposition audio indexing and page reference generation for law firms preparing evidence portfolios
- Medical lecture audio analysis to extract slide and page numbers for building CME (Continuing Medical Education) study packets
- Corporate compliance training video transcript pagination to create quick-reference guides for HR and audit teams
- eLearning platform automated extraction of chapter and page markers from audio lectures for improved student navigation
- Research lab meeting audio recordings page-number tagging to streamline protocol reviews and experimental replication
- Publishing house quality assurance of audiobook pagination consistency by extracting and validating spoken page references
- Digital library archival of oral history interviews with page-based metadata extraction for enhanced search and retrieval

```
# Final step: Format the corrected page numbers into the requested comma-delimited list
# Based on the completed audio analysis results

# The corrected page numbers from the audio analysis
corrected_page_numbers = [132, 133, 134, 197, 245, 1197]

print("=== FINAL PAGE NUMBER FORMATTING ===\n")
print(f"Extracted page numbers from audio analysis: {corrected_page_numbers}")
print(f"Number of pages: {len(corrected_page_numbers)}")

# Verify they are in ascending order
is_ascending = all(corrected_page_numbers[i] <= corrected_page_numbers[i+1] for i in range(len(corrected_page_numbers)-1))
print(f"Already in ascending order: {is_ascending}")

# Sort to ensure ascending order (though they should already be sorted)
sorted_pages = sorted(corrected_page_numbers)
print(f"Final sorted page numbers: {sorted_pages}")

# Create the comma-delimited list format as requested
final_output = ', '.join(map(str, sorted_pages))

print("\n" + "="*50)
print("FINAL RESULT FOR CALCULUS MID-TERM STUDY")
print("="*50)
print(f"Page numbers (comma-delimited, ascending order): {final_output}")
print("="*50)

# Save the final result to workspace for reference
with open('workspace/final_page_list.txt', 'w') as f:
    f.write(f"Calculus Mid-term Study - Page Numbers\n")
    f.write(f"Final comma-delimited list: {final_output}\n")
    f.write(f"Total pages: {len(sorted_pages)}\n")
    f.write(f"Individual pages: {sorted_pages}\n")

print(f"\nFinal result saved to: workspace/final_page_list.txt")
print(f"\n*** TASK COMPLETE ***")
print(f"Answer: {final_output}")
```

### Development Step 2: Parse Excel File for Cell Coordinates, Text, Fill Colors, and ‘START’/‘END’ Locations

**Description**: Parse and analyze the attached Excel file data/gaia/2023/validation/65afbc8a-89ca-4ad5-8d62-355bb401f61d.xlsx to extract the complete grid structure: record for each cell its row–column coordinate, displayed text, and fill color as a 6-digit hex code, then identify the coordinates of the cell containing 'START' and the cell containing 'END'.

**Use Cases**:
- Warehouse AGV route optimization and automated navigation using Excel grid layouts; extract cell coordinates, fill colors for storage zones, and identify START (loading bay) and END (docking station)
- Video game level map ingestion and design automation by parsing Excel-based tile grids, reading cell colors for terrain types, and locating START/END spawn points
- Construction site safety path planning with hazard zone extraction from color-coded Excel floor plans; determine safe route from START (entrance) to END (exit)
- Manufacturing line process monitoring by parsing Excel diagrams of assembly stations, capturing status color codes, and locating START and END of the production flow
- Clinical laboratory sample rack layout processing; read Excel grid to map sample positions by fill-color status and identify START (first sample) and END (last sample) wells for automated pipetting
- Research experiment plate map analysis for high-throughput screening; extract cell coordinates and reagent status colors, then pinpoint START and END wells for liquid handling robots
- Event seating arrangement and attendee flow mapping by parsing color-coded Excel seating charts; extract seat coordinates and colors for zones, identifying START (entry gate) and END (exit gate) points

```
import os
import json
import traceback
from openpyxl import load_workbook

# Path to the Excel file
xlsx_path = 'data/gaia/2023/validation/65afbc8a-89ca-4ad5-8d62-355bb401f61d.xlsx'

print('=== EXCEL GRID EXTRACTION SCRIPT V2 ===')
# 1) Verify the file exists
if not os.path.exists(xlsx_path):
    print(f"Error: Excel file not found at '{xlsx_path}'")
    exit(1)
print(f"Found Excel file: {xlsx_path}")

# 2) Attempt to load the workbook with debug prints
print('Loading workbook now...')
try:
    wb = load_workbook(xlsx_path, data_only=False)
    print('Workbook loaded successfully')
except Exception as e:
    print('Error loading workbook: ', e)
    traceback.print_exc()
    exit(1)

# 3) Access active sheet and print its details
try:
    sheet = wb.active
    print(f"Active sheet: '{sheet.title}' (index 0)")
    max_row = sheet.max_row
    max_col = sheet.max_column
    print(f"Sheet dimensions: {max_row} rows x {max_col} columns")
except Exception as e:
    print('Error accessing active sheet or dimensions:', e)
    traceback.print_exc()
    exit(1)

# 4) Prepare to scan every cell for value and fill
all_cells = []
start_coord = None
end_coord = None
print('Beginning cell-by-cell analysis...')

# 5) Iterate and capture cell data
for row in range(1, max_row + 1):
    for col in range(1, max_col + 1):
        cell = sheet.cell(row=row, column=col)
        raw_value = cell.value
        display_text = str(raw_value) if raw_value is not None else ''

        # Extract fill color
        hex_color = ''
        try:
            fill = cell.fill
            rgb = getattr(fill.start_color, 'rgb', None)
            if isinstance(rgb, str) and len(rgb) == 8:
                hex_color = rgb[-6:]
        except Exception:
            # If any issue reading fill, leave hex_color empty and continue
            pass

        # Record this cell's data
        cell_record = {
            'row': row,
            'col': col,
            'value': display_text,
            'fill_color': hex_color
        }
        all_cells.append(cell_record)

        # Detect START/END exactly
        if display_text == 'START':
            start_coord = {'row': row, 'col': col}
            print(f"-> Found START at (row={row}, col={col})")
        elif display_text == 'END':
            end_coord = {'row': row, 'col': col}
            print(f"-> Found END at (row={row}, col={col})")

print('Cell analysis loop complete.')
print(f"Total cells recorded: {len(all_cells)}")
if not start_coord:
    print('Warning: START cell not found.')
if not end_coord:
    print('Warning: END cell not found.')

# 6) Save results to workspace/
os.makedirs('workspace', exist_ok=True)

grid_output_path = 'workspace/grid_data.json'
print(f"Saving full grid data to {grid_output_path}...")
with open(grid_output_path, 'w', encoding='utf-8') as f:
    json.dump(all_cells, f, indent=2)
print('Grid data saved.')

coords = {'START': start_coord, 'END': end_coord}
coords_output_path = 'workspace/start_end_coordinates.json'
print(f"Saving START/END coordinates to {coords_output_path}...")
with open(coords_output_path, 'w', encoding='utf-8') as f:
    json.dump(coords, f, indent=2)
print('Coordinates data saved.')

print('=== Script finished ===')
```

### Development Step 4: Title: Extract Unique Food Items and Identify Non-Duplicates from Excel Inventory Data

**Description**: Parse and analyze the attached Excel file data/gaia/2023/validation/9b54f9d9-35ee-4a14-b62f-d130ea00317f/food_duplicates.xls to extract all food items listed in the spreadsheet. Identify the complete inventory of food names and examine for any duplicates or variations of the same food item appearing under different names. Create a comprehensive list of all unique food items and identify which single food item appears only once without any duplicate entries or alternative naming variations.

**Use Cases**:
- Restaurant chain menu standardization to identify duplicate or variant food items across multiple locations for consistent branding and inventory management
- Food safety compliance audits to detect mislabeled or ambiguously named ingredients in supplier spreadsheets
- Nutrition database consolidation by extracting and unifying food item names from diverse Excel sources, eliminating duplicates and synonyms
- Automated quality control in food manufacturing to ensure unique labeling of products and prevent redundant SKU entries
- Academic research in food science analyzing dietary surveys to accurately count unique food items consumed by study participants
- Retail grocery inventory optimization by merging supplier lists and removing duplicate or synonym product entries for efficient stock management
- Regulatory compliance checks for import/export food documentation to ensure all listed items are uniquely identified and not duplicated under alternative names
- Culinary content curation for recipe websites, ensuring ingredient lists are free from redundant or synonym entries for improved user searchability

```
import os
import json
import pandas as pd
from collections import Counter

# Load the Excel file to examine the remaining 5 unique items in context
xls_path = "data/gaia/2023/validation/9b54f9d9-35ee-4a14-b62f-d130ea00317f/food_duplicates.xls"
df = pd.read_excel(xls_path)

print("=== FINAL ANALYSIS: EXAMINING THE LAST 5 UNIQUE ITEMS ===")
print(f"Analyzing file: {xls_path}")

# The 5 remaining unique items from previous analysis
remaining_items = ['boba', 'goat meat', 'mutton', 'tapioca', 'turtle soup']
print(f"\nRemaining 5 unique items to analyze: {remaining_items}")

# Display the complete dataset again to see these items in context
print("\n=== COMPLETE DATASET FOR CONTEXT ===")
print(df.to_string(index=False))

# Let's examine each of the 5 remaining items more carefully
print("\n=== DETAILED ANALYSIS OF REMAINING 5 ITEMS ===")

# Extract all food items including column headers
all_food_items = []
for col in df.columns:
    food_values = [col] + df[col].dropna().tolist()
    for item in food_values:
        item_str = str(item).strip().lower()
        if item_str:
            all_food_items.append(item_str)

print(f"\nTotal food items in dataset: {len(all_food_items)}")

# Check if any of the 5 items might have additional relationships
print("\nAnalyzing each remaining item:")

for item in remaining_items:
    print(f"\n--- {item.upper()} ---")
    
    # Count occurrences
    count = all_food_items.count(item)
    print(f"Occurrences in dataset: {count}")
    
    # Look for potential relationships
    if item == 'boba':
        print("Analysis: Boba is bubble tea pearls, typically tapioca-based")
        print("Potential relationship: Could be related to 'tapioca' since boba is made from tapioca")
    elif item == 'goat meat':
        print("Analysis: Meat from goats")
        print("Note: Different from mutton (sheep meat)")
    elif item == 'mutton':
        print("Analysis: Meat from sheep")
        print("Note: Different from goat meat")
    elif item == 'tapioca':
        print("Analysis: Starch extracted from cassava root")
        print("Potential relationship: Boba pearls are made from tapioca starch")
    elif item == 'turtle soup':
        print("Analysis: Soup made from turtle meat")
        print("Note: Distinct dish, no obvious synonyms")

# Test the potential boba-tapioca relationship
print("\n=== TESTING BOBA-TAPIOCA RELATIONSHIP ===")
print("Boba (bubble tea pearls) are made from tapioca starch.")
print("This could be considered a semantic relationship.")

# Create final synonym dictionary including boba-tapioca
final_food_synonyms = {
    # All previous relationships plus:
    'tapioca': ['boba'],  # Boba is made from tapioca
    
    # Keep all existing relationships from expanded analysis
    'zucchini': ['courgette'],
    'eggplant': ['aubergine'],
    'bell pepper': ['capsicum'],
    'beet': ['beetroot'],
    'cilantro': ['coriander'],
    'arugula': ['rocket'],
    'broccoli rabe': ['rapini'],
    'chickpea': ['garbanzo bean'],
    'avocado': ['alligator pear'],
    'beef': ['cow meat'],
    'veal': ['calf meat'],
    'pigeon': ['squab'],
    'foie gras': ['fatty goose liver'],
    'crawdad': ['mudbug'],
    'clam': ['geoduck'],
    'rice krispies': ['puffed rice'],
    'congee': ['rice porridge'],
    'cotton candy': ['candy floss'],
    'confectioner\'s sugar': ['icing sugar'],
    'jelly donut': ['jam doughnut'],
    'cupcake': ['fairy cake'],
    'candy': ['bonbon'],
    'soda': ['pop'],
    'coffee': ['java'],
    'dried cranberries': ['craisins'],
    'golden raisin': ['sultana'],
    'sandwich': ['hoagie'],
    'fries': ['chips'],
    'angel hair pasta': ['capellini'],
    'soy curds': ['tofu'],
    'fleur de sel': ['salt'],
    'hot wings': ['buffalo wings'],
    'mac and cheese': ['kraft dinner'],
    'pancake': ['flapjack'],
    'rasher': ['bacon strip'],
    'hand pies': ['pasties'],
    'deer meat': ['venison'],
    'stomach': ['tripe'],
    'sweetbread': ['calf thymus'],
    'cottage cheese': ['farmer\'s cheese'],
    'relish': ['pickle'],
    'peas': ['sugar snaps'],
    'squash': ['pumpkin'],
    'nectar': ['agave'],
    'shish kebab': ['skewer'],
    'granola': ['oat cereal'],
    'lizardfish': ['bombay duck']
}

print(f"\nFinal synonym groups: {len(final_food_synonyms)}")

# Create reverse mapping
synonym_groups = {}
for main_term, synonyms in final_food_synonyms.items():
    group = [main_term] + synonyms
    for term in group:
        synonym_groups[term] = tuple(sorted(group))

# Group items by semantic equivalence
semantic_groups = {}
ungrouped_items = []

for item in all_food_items:
    if item in synonym_groups:
        group_key = synonym_groups[item]
        if group_key not in semantic_groups:
            semantic_groups[group_key] = []
        semantic_groups[group_key].append(item)
    else:
        ungrouped_items.append(item)

# Analyze groups
groups_with_duplicates = []
groups_without_duplicates = []

for group_key, items in semantic_groups.items():
    unique_items = list(set(items))
    if len(unique_items) > 1:
        groups_with_duplicates.append((group_key, unique_items))
    else:
        groups_without_duplicates.append((group_key, unique_items))

# Count ungrouped items
ungrouped_counter = Counter(ungrouped_items)
ungrouped_appearing_once = [item for item, count in ungrouped_counter.items() if count == 1]

# Find truly unique items
true_unique_items = ungrouped_appearing_once + [items[0] for _, items in groups_without_duplicates]

print(f"\n=== FINAL RESULTS ===")
print(f"Groups with semantic duplicates: {len(groups_with_duplicates)}")
print(f"Items appearing only once: {len(true_unique_items)}")

print(f"\nFinal unique items:")
for item in sorted(true_unique_items):
    print(f"  - {item}")

# Check if boba-tapioca relationship was applied
if 'boba' in synonym_groups and 'tapioca' in synonym_groups:
    boba_group = synonym_groups['boba']
    tapioca_group = synonym_groups['tapioca']
    if boba_group == tapioca_group:
        print(f"\n✓ Boba-tapioca relationship successfully applied: {list(boba_group)}")
    else:
        print(f"\n✗ Boba-tapioca relationship not applied correctly")
else:
    print(f"\n? Boba-tapioca relationship status unclear")

# Save final analysis
final_analysis = {
    'total_items': len(all_food_items),
    'final_unique_items_count': len(true_unique_items),
    'final_unique_items': sorted(true_unique_items),
    'semantic_duplicates_count': len(groups_with_duplicates),
    'boba_tapioca_relationship_applied': 'boba' in synonym_groups and 'tapioca' in synonym_groups
}

os.makedirs('workspace', exist_ok=True)
with open('workspace/final_unique_analysis.json', 'w') as f:
    json.dump(final_analysis, f, indent=2)

print(f"\nFinal analysis saved to: workspace/final_unique_analysis.json")

if len(true_unique_items) == 1:
    print(f"\n*** FINAL ANSWER: The single food item that appears only once is: '{true_unique_items[0]}' ***")
else:
    print(f"\n*** Found {len(true_unique_items)} items appearing only once ***")
    print("Remaining items to analyze further:")
    for item in sorted(true_unique_items):
        print(f"  - {item}")
```

### Development Step 3: Title:  
Extract and Analyze Unique Food Items and Duplicates from Excel Food Inventory Spreadsheet

**Description**: Parse and analyze the attached Excel file data/gaia/2023/validation/9b54f9d9-35ee-4a14-b62f-d130ea00317f/food_duplicates.xls to extract all food items listed in the spreadsheet. Identify the complete inventory of food names and examine for any duplicates or variations of the same food item appearing under different names. Create a comprehensive list of all unique food items and identify which single food item appears only once without any duplicate entries or alternative naming variations.

**Use Cases**:
- Restaurant chain menu standardization by detecting duplicate or variant food names across multiple branch inventory spreadsheets
- Food safety compliance audits to ensure all unique food items are accounted for and no mislabeled duplicates exist in supplier records
- Nutrition database curation to identify and merge semantically equivalent food entries, improving accuracy for diet tracking apps
- Automated cleaning of grocery store product lists to eliminate redundancies and unify naming conventions for inventory systems
- Academic research in food science to analyze survey data for unique dietary items and avoid double-counting due to naming variations
- Food delivery platform onboarding to reconcile restaurant menu uploads and prevent duplicate listings of the same dish under different names
- Supply chain optimization for catering companies by consolidating ingredient lists and identifying unique procurement needs
- Quality assurance in recipe publishing platforms to detect and flag duplicate or synonym food entries submitted by different users

```
import os
import json
import pandas as pd
from collections import Counter

# First, let's inspect the workspace files to understand the current analysis
print("=== INSPECTING WORKSPACE FILES ===")

# Check what files exist in workspace
workspace_files = []
if os.path.exists('workspace'):
    workspace_files = os.listdir('workspace')
    print(f"Files in workspace: {workspace_files}")
else:
    print("No workspace directory found")

# Inspect the semantic analysis JSON file if it exists
semantic_file = 'workspace/semantic_food_analysis.json'
if os.path.exists(semantic_file):
    print(f"\n=== INSPECTING {semantic_file} ===")
    with open(semantic_file, 'r') as f:
        semantic_data = json.load(f)
    
    print("Keys in semantic analysis:")
    for key in semantic_data.keys():
        print(f"  - {key}")
    
    print(f"\nNumber of true unique items found: {len(semantic_data.get('true_unique_items', []))}")
    print("True unique items:")
    for item in semantic_data.get('true_unique_items', [])[:10]:  # Show first 10
        print(f"  - {item}")
    if len(semantic_data.get('true_unique_items', [])) > 10:
        print(f"  ... and {len(semantic_data.get('true_unique_items', [])) - 10} more")
    
    print(f"\nSemantic duplicates found: {len(semantic_data.get('semantic_duplicates', {}))}")
    print("Sample semantic duplicates:")
    for main_term, variants in list(semantic_data.get('semantic_duplicates', {}).items())[:5]:
        print(f"  {main_term}: {variants}")
else:
    print(f"File {semantic_file} not found")

# Now let's reload the original data and expand our synonym detection
print("\n" + "="*60)
print("EXPANDING SEMANTIC DUPLICATE DETECTION")
print("="*60)

# Load the Excel file
xls_path = "data/gaia/2023/validation/9b54f9d9-35ee-4a14-b62f-d130ea00317f/food_duplicates.xls"
df = pd.read_excel(xls_path)

# Extract all food items (including column headers)
all_food_items = []
for col in df.columns:
    food_values = [col] + df[col].dropna().tolist()
    for item in food_values:
        item_str = str(item).strip().lower()
        if item_str:
            all_food_items.append(item_str)

print(f"Total food items: {len(all_food_items)}")
print(f"Unique food items: {len(set(all_food_items))}")

# Expanded synonym dictionary with more comprehensive food relationships
expanded_food_synonyms = {
    # Vegetables
    'zucchini': ['courgette'],
    'eggplant': ['aubergine'],
    'bell pepper': ['capsicum'],
    'beet': ['beetroot'],
    'cilantro': ['coriander'],
    'arugula': ['rocket'],
    'broccoli rabe': ['rapini'],
    
    # Legumes
    'chickpea': ['garbanzo bean'],
    
    # Fruits
    'avocado': ['alligator pear'],
    
    # Meat and Poultry
    'beef': ['cow meat'],
    'veal': ['calf meat'],
    'pigeon': ['squab'],
    'foie gras': ['fatty goose liver'],
    
    # Seafood and Shellfish
    'crawdad': ['mudbug'],
    'clam': ['geoduck'],  # Both are types of clams
    
    # Grains/Cereals
    'rice krispies': ['puffed rice'],
    'congee': ['rice porridge'],
    
    # Sweets/Desserts
    'cotton candy': ['candy floss'],
    'confectioner\'s sugar': ['icing sugar'],
    'jelly donut': ['jam doughnut'],
    'cupcake': ['fairy cake'],
    'candy': ['bonbon'],
    
    # Beverages
    'soda': ['pop'],
    'coffee': ['java'],
    
    # Dried fruits
    'dried cranberries': ['craisins'],
    'golden raisin': ['sultana'],
    
    # Sandwiches and Bread
    'sandwich': ['hoagie'],
    
    # Potatoes
    'fries': ['chips'],
    
    # Pasta
    'angel hair pasta': ['capellini'],
    
    # Dairy and Protein
    'soy curds': ['tofu'],
    
    # Seasonings
    'fleur de sel': ['salt'],
    
    # Additional potential relationships
    'hot wings': ['buffalo wings'],  # Both are chicken wings
    'mac and cheese': ['kraft dinner'],  # Both are boxed mac and cheese
    'pancake': ['flapjack'],  # Both are flat cakes
    'rasher': ['bacon strip'],  # Both are bacon
    'hand pies': ['pasties'],  # Both are small filled pastries
    'deer meat': ['venison'],  # Same meat
    'goat meat': ['mutton'],  # Wait, mutton is sheep, not goat - remove this
    'stomach': ['tripe'],  # Both are organ meat from stomach
    'sweetbread': ['calf thymus'],  # Sweetbread includes thymus
    'cottage cheese': ['farmer\'s cheese'],  # Similar fresh cheeses
    'relish': ['pickle'],  # Both are pickled vegetables
    'peas': ['sugar snaps'],  # Sugar snap peas are a type of pea
    'squash': ['pumpkin'],  # Pumpkin is a type of squash
    'nectar': ['agave'],  # Agave nectar
    'turtle soup': ['boba'],  # This doesn't make sense - remove
    'shish kebab': ['skewer'],  # Kebab is food on a skewer
    'granola': ['oat cereal'],  # Both are oat-based cereals
    'lizardfish': ['bombay duck'],  # Bombay duck is actually a type of lizardfish
}

# Remove incorrect relationships
if 'goat meat' in expanded_food_synonyms:
    del expanded_food_synonyms['goat meat']  # mutton is sheep, not goat
if 'turtle soup' in expanded_food_synonyms:
    del expanded_food_synonyms['turtle soup']  # boba is not turtle soup

print(f"\nExpanded synonym groups: {len(expanded_food_synonyms)}")

# Create reverse mapping
synonym_groups = {}
for main_term, synonyms in expanded_food_synonyms.items():
    group = [main_term] + synonyms
    for term in group:
        synonym_groups[term] = tuple(sorted(group))

# Group items by semantic equivalence
semantic_groups = {}
ungrouped_items = []

for item in all_food_items:
    if item in synonym_groups:
        group_key = synonym_groups[item]
        if group_key not in semantic_groups:
            semantic_groups[group_key] = []
        semantic_groups[group_key].append(item)
    else:
        ungrouped_items.append(item)

print(f"\nSemantic groups found: {len(semantic_groups)}")
print(f"Ungrouped items: {len(ungrouped_items)}")

# Analyze groups
groups_with_duplicates = []
groups_without_duplicates = []

for group_key, items in semantic_groups.items():
    unique_items = list(set(items))
    if len(unique_items) > 1:
        groups_with_duplicates.append((group_key, unique_items))
    else:
        groups_without_duplicates.append((group_key, unique_items))

# Count ungrouped items
ungrouped_counter = Counter(ungrouped_items)
ungrouped_appearing_once = [item for item, count in ungrouped_counter.items() if count == 1]

# Find truly unique items
true_unique_items = ungrouped_appearing_once + [items[0] for _, items in groups_without_duplicates]

print(f"\n=== EXPANDED ANALYSIS RESULTS ===")
print(f"Groups with semantic duplicates: {len(groups_with_duplicates)}")
print(f"Items appearing only once: {len(true_unique_items)}")

print(f"\nItems that appear only once:")
for item in sorted(true_unique_items):
    print(f"  - {item}")

print(f"\nSemantic duplicate groups found:")
for group_key, unique_items in groups_with_duplicates:
    print(f"  {list(group_key)}: {unique_items}")

# Save expanded analysis
expanded_analysis = {
    'total_items': len(all_food_items),
    'unique_items_count': len(true_unique_items),
    'true_unique_items': sorted(true_unique_items),
    'semantic_duplicates': {group_key[0]: unique_items for group_key, unique_items in groups_with_duplicates},
    'expanded_synonyms_used': len(expanded_food_synonyms)
}

os.makedirs('workspace', exist_ok=True)
with open('workspace/expanded_food_analysis.json', 'w') as f:
    json.dump(expanded_analysis, f, indent=2)

print(f"\nExpanded analysis saved to: workspace/expanded_food_analysis.json")

if len(true_unique_items) == 1:
    print(f"\n*** ANSWER: The single food item that appears only once is: '{true_unique_items[0]}' ***")
else:
    print(f"\n*** Still found {len(true_unique_items)} items appearing only once. Need further analysis. ***")
```

## Created Time
2025-08-11 04:37:45
