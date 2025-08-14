# Developer Plan 01

## Plan
Parse and analyze the attached Excel file data/gaia/2023/validation/3da89939-209c-4086-8520-7eb734e6b4ef.xlsx to extract all table data and identify the structure of the spreadsheet. Examine each table's content, captions, headers, and any identifying information that could help match them to source papers referenced in the 'Trans fatty acid contents in chocolates and chocolate wafers in Turkey' paper.

## Description
This is the optimal first step because: (1) We need to understand the Excel file structure and extract all table data before we can identify their sources, (2) No previous analysis has been performed on this file, (3) Expected outcome is to have complete inventory of all tables with their content and any identifying information, (4) This provides the foundation needed to then search for the original 'Trans fatty acid' paper and match each table to its corresponding reference in the bibliography

## Episodic Examples
### Development Step 1: Parse Excel Fast-Food Sales Data: Identify Structure, Categorize Items, Compute Food Sales

**Description**: Parse and analyze the attached Excel file data/gaia/2023/validation/7bd855d8-463d-4ed5-93ca-5fe35145f733.xlsx to extract all sales data for the fast-food chain menu items. Identify the structure of the spreadsheet including column headers, data organization, and categorize menu items to distinguish between food items and drinks. Extract sales figures for each item and prepare the data for calculating total food sales excluding beverages.

**Use Cases**:
- Monthly revenue reporting for a fast-food franchise’s finance department, automatically extracting food-only sales figures to reconcile budgets and P&L statements
- Automated inventory reorder triggers in the supply chain system, using daily food item sales volumes (excluding beverages) to forecast stock depletion and place purchase orders
- Regional menu performance benchmarking for corporate strategy teams, comparing unit sales of burgers, fries, and salads across multiple outlets to inform promotional campaigns
- Academic study on consumer eating habits, correlating time-of-day food sales data (excluding drinks) with demographic surveys to publish insights in a nutrition journal
- Point-of-sale system integration that updates digital menu availability and highlights top-selling food items in real time based on parsed Excel sales exports
- Restaurant staff scheduling optimization tool that analyzes peak food-only sales periods to allocate kitchen and counter staff efficiently, reducing labor costs
- Product development research for new menu items, using historical food sales trends (without beverages) to identify gaps in offerings and guide R&D decisions

```
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import json

# The path to the Excel file to be analyzed
xlsx_path = "data/gaia/2023/validation/7bd855d8-463d-4ed5-93ca-5fe35145f733.xlsx"

print("=== FAST-FOOD CHAIN SALES DATA ANALYSIS ===")
print(f"Analyzing file: {xlsx_path}")

# Check if file exists
if not os.path.exists(xlsx_path):
    print(f"Error: Excel file '{xlsx_path}' does not exist.")
    exit()

print(f"File exists: {xlsx_path}")
file_size = os.path.getsize(xlsx_path)
print(f"File size: {file_size} bytes")

# Load workbook with openpyxl to examine structure and formatting
print("\nLoading workbook with openpyxl to examine structure...")
wb = load_workbook(xlsx_path, data_only=True)  # Use data_only=True to get calculated values

print(f"Number of worksheets: {len(wb.worksheets)}")
print(f"Worksheet names: {[sheet.title for sheet in wb.worksheets]}")

# Examine each worksheet
for sheet_idx, sheet in enumerate(wb.worksheets):
    print(f"\n=== ANALYZING WORKSHEET: {sheet.title} ===")
    
    max_row = sheet.max_row
    max_col = sheet.max_column
    print(f"Sheet dimensions: {max_row} rows x {max_col} columns")
    
    # Get the range of actual data
    min_row = sheet.min_row
    min_col = sheet.min_column
    print(f"Data range: rows {min_row}-{max_row}, columns {min_col}-{max_col}")
    
    print("\n=== FIRST 10 ROWS PREVIEW ===")
    # Display first 10 rows to understand structure
    for row in range(min_row, min(max_row + 1, min_row + 10)):
        row_data = []
        for col in range(min_col, max_col + 1):
            cell = sheet.cell(row=row, column=col)
            cell_value = cell.value if cell.value is not None else ""
            row_data.append(str(cell_value))
        print(f"Row {row}: {row_data}")
    
    print("\n=== COLUMN HEADERS ANALYSIS ===")
    # Examine the first row as potential headers
    headers = []
    for col in range(min_col, max_col + 1):
        cell = sheet.cell(row=min_row, column=col)
        header_value = cell.value if cell.value is not None else f"Col_{col}"
        headers.append(str(header_value))
        print(f"Column {col}: '{header_value}'")
    
    print(f"\nIdentified headers: {headers}")
    
    # Sample some data rows to understand content
    print("\n=== DATA SAMPLE (Rows 2-6) ===")
    for row in range(min_row + 1, min(max_row + 1, min_row + 6)):
        row_data = {}
        print(f"Row {row}:")
        for col_idx, col in enumerate(range(min_col, max_col + 1)):
            cell = sheet.cell(row=row, column=col)
            cell_value = cell.value if cell.value is not None else ""
            header = headers[col_idx] if col_idx < len(headers) else f"Col_{col}"
            row_data[header] = cell_value
            print(f"  {header}: '{cell_value}'")
    
    # Look for potential menu item categories or patterns
    print("\n=== SEARCHING FOR MENU CATEGORIES ===")
    category_keywords = ['food', 'drink', 'beverage', 'burger', 'sandwich', 'fries', 'soda', 'coffee', 'salad']
    
    found_categories = []
    for row in range(min_row, min(max_row + 1, min_row + 20)):  # Check first 20 rows
        for col in range(min_col, max_col + 1):
            cell = sheet.cell(row=row, column=col)
            if cell.value:
                cell_text = str(cell.value).lower()
                for keyword in category_keywords:
                    if keyword in cell_text:
                        found_categories.append({
                            'row': row,
                            'col': col,
                            'value': cell.value,
                            'keyword': keyword
                        })
                        print(f"Found category keyword '{keyword}' in cell ({row}, {col}): '{cell.value}'")
    
    print(f"\nTotal category keywords found: {len(found_categories)}")

# Also load with pandas for easier data manipulation
print("\n" + "="*60)
print("PANDAS DATAFRAME ANALYSIS")
print("="*60)

try:
    # Try to read the Excel file with pandas
    df = pd.read_excel(xlsx_path, sheet_name=None)  # Read all sheets
    
    print(f"Pandas successfully loaded {len(df)} sheet(s)")
    
    for sheet_name, sheet_df in df.items():
        print(f"\n=== PANDAS ANALYSIS: {sheet_name} ===")
        print(f"DataFrame shape: {sheet_df.shape}")
        print(f"Column names: {list(sheet_df.columns)}")
        print(f"Data types:\n{sheet_df.dtypes}")
        
        print("\nFirst 5 rows:")
        print(sheet_df.head())
        
        print("\nBasic statistics for numeric columns:")
        numeric_cols = sheet_df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print(sheet_df[numeric_cols].describe())
        else:
            print("No numeric columns found")
        
        print("\nMissing values:")
        print(sheet_df.isnull().sum())
        
except Exception as e:
    print(f"Error reading with pandas: {e}")
    print("Will proceed with openpyxl analysis only")

# Save initial analysis
analysis_data = {
    'file_path': xlsx_path,
    'file_size': file_size,
    'worksheets': [sheet.title for sheet in wb.worksheets],
    'analysis_timestamp': pd.Timestamp.now().isoformat()
}

with open('workspace/fast_food_initial_analysis.json', 'w') as f:
    json.dump(analysis_data, f, indent=2)

print(f"\nInitial analysis saved to: workspace/fast_food_initial_analysis.json")
print("Next step: Extract and categorize menu items and sales data")
```

### Development Step 2: Extract and Categorize Fast-Food Menu Sales from Excel, Prepare Food-Only Sales Totals

**Description**: Parse and analyze the attached Excel file data/gaia/2023/validation/7bd855d8-463d-4ed5-93ca-5fe35145f733.xlsx to extract all sales data for the fast-food chain menu items. Identify the structure of the spreadsheet including column headers, data organization, and categorize menu items to distinguish between food items and drinks. Extract sales figures for each item and prepare the data for calculating total food sales excluding beverages.

**Use Cases**:
- Multi-location franchise performance benchmarking: aggregate and compare food vs beverage sales across outlets to identify top-performing restaurants and underperforming regions
- Inventory procurement optimization for supply chain teams: parse POS export spreadsheets to compute accurate demand for burgers, salads, fries, etc., excluding beverages to streamline restocking orders
- Financial auditing and compliance reporting for hospitality accountants: automatically extract and categorize sales figures from daily sales logs to generate audit trails and tax reports focusing on taxable food items
- Menu engineering and dynamic pricing analysis for marketing managers: analyze historical sales volume per menu category to adjust pricing, promotions, and product placement for maximizing food item revenue excluding drinks
- Demand forecasting and supply planning for operations teams: ingest weekly Excel sales exports, aggregate item-level food sales excluding beverages, and feed into forecasting models for ingredient ordering
- Loyalty program ROI assessment for CRM platforms: extract item-level sales data by location to measure uplift in food purchases during targeted promotions or discount campaigns, excluding beverage sales
- Business intelligence dashboard integration for executive reporting: transform raw Excel sales data into structured JSON and text summaries for real-time ingestion into BI tools to visualize food-only revenue trends across all outlets
- Competitive benchmarking and market analysis for consultancy firms: use categorized sales data to compare menu performance against industry benchmarks and advise clients on menu mix optimization

```
import os
import pandas as pd
from openpyxl import load_workbook
import json

# The path to the Excel file to be analyzed
xlsx_path = "data/gaia/2023/validation/7bd855d8-463d-4ed5-93ca-5fe35145f733.xlsx"

print("=== COMPLETE FAST-FOOD CHAIN SALES DATA EXTRACTION ===")
print(f"Analyzing file: {xlsx_path}")

# Load the Excel file with pandas for complete data extraction
print("\nLoading complete dataset with pandas...")
df = pd.read_excel(xlsx_path)

print(f"Dataset shape: {df.shape}")
print(f"Column names: {list(df.columns)}")

# Display the complete dataset
print("\n=== COMPLETE DATASET ===")
print(df.to_string(index=False))

# Save complete data to workspace for reference
with open('workspace/complete_sales_data.txt', 'w') as f:
    f.write("=== FAST-FOOD CHAIN COMPLETE SALES DATA ===\n")
    f.write(f"Dataset shape: {df.shape}\n")
    f.write(f"Column names: {list(df.columns)}\n\n")
    f.write("Complete dataset:\n")
    f.write(df.to_string(index=False))
    f.write("\n\n")

print(f"\nComplete dataset saved to: workspace/complete_sales_data.txt")

# Analyze the data structure and categorize menu items
print("\n=== MENU ITEM CATEGORIZATION ===")

# Based on the column names, categorize items
columns = list(df.columns)
print(f"All columns: {columns}")

# Exclude the Location column and categorize the rest
menu_columns = [col for col in columns if col != 'Location']
print(f"Menu item columns: {menu_columns}")

# Categorize menu items (food vs beverages)
food_items = ['Burgers', 'Hot Dogs', 'Salads', 'Fries', 'Ice Cream']
beverage_items = ['Soda']

# Verify categorization matches actual columns
actual_food_items = [item for item in food_items if item in menu_columns]
actual_beverage_items = [item for item in beverage_items if item in menu_columns]

print(f"\nFood items identified: {actual_food_items}")
print(f"Beverage items identified: {actual_beverage_items}")
print(f"Other items (if any): {[item for item in menu_columns if item not in food_items and item not in beverage_items]}")

# Extract sales data for each location
print("\n=== SALES DATA BY LOCATION ===")
for index, row in df.iterrows():
    location = row['Location']
    print(f"\nLocation: {location}")
    
    total_food_sales = 0
    total_beverage_sales = 0
    
    print("  Food sales:")
    for item in actual_food_items:
        sales = row[item]
        total_food_sales += sales
        print(f"    {item}: ${sales:,.2f}")
    
    print("  Beverage sales:")
    for item in actual_beverage_items:
        sales = row[item]
        total_beverage_sales += sales
        print(f"    {item}: ${sales:,.2f}")
    
    print(f"  TOTAL FOOD SALES (excluding beverages): ${total_food_sales:,.2f}")
    print(f"  Total beverage sales: ${total_beverage_sales:,.2f}")
    print(f"  Grand total (all items): ${total_food_sales + total_beverage_sales:,.2f}")

# Calculate overall totals across all locations
print("\n" + "="*60)
print("SUMMARY: TOTAL SALES ACROSS ALL LOCATIONS")
print("="*60)

# Calculate total food sales (excluding beverages)
total_food_sales_all = df[actual_food_items].sum().sum()
total_beverage_sales_all = df[actual_beverage_items].sum().sum()
grand_total_all = total_food_sales_all + total_beverage_sales_all

print(f"\nFood items totals across all locations:")
for item in actual_food_items:
    item_total = df[item].sum()
    print(f"  {item}: ${item_total:,.2f}")

print(f"\nBeverage items totals across all locations:")
for item in actual_beverage_items:
    item_total = df[item].sum()
    print(f"  {item}: ${item_total:,.2f}")

print(f"\n*** FINAL ANSWER ***")
print(f"TOTAL FOOD SALES (excluding beverages): ${total_food_sales_all:,.2f}")
print(f"Total beverage sales: ${total_beverage_sales_all:,.2f}")
print(f"Grand total (all items): ${grand_total_all:,.2f}")

# Create detailed analysis report
analysis_report = {
    'dataset_info': {
        'file_path': xlsx_path,
        'shape': df.shape,
        'columns': list(df.columns)
    },
    'categorization': {
        'food_items': actual_food_items,
        'beverage_items': actual_beverage_items
    },
    'sales_summary': {
        'total_food_sales': float(total_food_sales_all),
        'total_beverage_sales': float(total_beverage_sales_all),
        'grand_total': float(grand_total_all)
    },
    'individual_item_totals': {
        item: float(df[item].sum()) for item in menu_columns
    },
    'location_breakdown': []
}

# Add location-specific breakdowns
for index, row in df.iterrows():
    location_data = {
        'location': row['Location'],
        'food_sales': float(sum(row[item] for item in actual_food_items)),
        'beverage_sales': float(sum(row[item] for item in actual_beverage_items)),
        'item_breakdown': {item: float(row[item]) for item in menu_columns}
    }
    analysis_report['location_breakdown'].append(location_data)

# Save comprehensive analysis
with open('workspace/fast_food_sales_analysis.json', 'w') as f:
    json.dump(analysis_report, f, indent=2)

print(f"\nComprehensive analysis saved to: workspace/fast_food_sales_analysis.json")

# Also save a summary report
with open('workspace/sales_summary.txt', 'w') as f:
    f.write("FAST-FOOD CHAIN SALES ANALYSIS SUMMARY\n")
    f.write("="*50 + "\n\n")
    f.write(f"Dataset: {os.path.basename(xlsx_path)}\n")
    f.write(f"Locations analyzed: {len(df)}\n")
    f.write(f"Menu items: {len(menu_columns)}\n\n")
    
    f.write("CATEGORIZATION:\n")
    f.write(f"Food items: {', '.join(actual_food_items)}\n")
    f.write(f"Beverage items: {', '.join(actual_beverage_items)}\n\n")
    
    f.write("FINAL RESULTS:\n")
    f.write(f"Total Food Sales (excluding beverages): ${total_food_sales_all:,.2f}\n")
    f.write(f"Total Beverage Sales: ${total_beverage_sales_all:,.2f}\n")
    f.write(f"Grand Total (all items): ${grand_total_all:,.2f}\n")

print(f"Sales summary saved to: workspace/sales_summary.txt")
print("\n*** ANALYSIS COMPLETE ***")
print(f"The total food sales excluding beverages is: ${total_food_sales_all:,.2f}")
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

### Development Step 7: Title:  
Extract and Analyze XML Category Texts to Identify Unique Food Item from Spreadsheet Data

**Description**: Parse and analyze the attached XML file data/gaia/2023/validation/9b54f9d9-35ee-4a14-b62f-d130ea00317f/CATEGORIES.xml to extract all text elements under the CATEGORIES section. Examine the structure and content of each category element to understand how foods are organized. Then cross-reference the three unique food items identified from the spreadsheet analysis ('goat meat', 'mutton', and 'turtle soup') against the XML categories to determine which specific text element would contain the one food that appears only once in the spreadsheet without duplicates.

**Use Cases**:
- Food safety compliance auditing by cross-referencing regulated food items from spreadsheets against official XML food category lists in government databases
- Restaurant menu engineering to identify unique or rare menu items by comparing internal inventory spreadsheets with standardized food taxonomy XML files
- Automated quality assurance in food delivery platforms by validating that all menu items are properly categorized and uniquely identified in the system’s XML configuration
- Nutrition research projects that require mapping unique food consumption entries from survey spreadsheets to standardized food categories in public health XML datasets
- Supply chain traceability for specialty meats by ensuring that unique items (e.g., “goat meat”, “turtle soup”) in supplier spreadsheets are accurately reflected in centralized XML product catalogs
- Data migration for legacy food service systems, ensuring that unique or non-duplicated food items are preserved and correctly categorized during transfer from spreadsheets to XML-based databases
- Retail analytics for supermarkets, where unique food products identified in sales spreadsheets are matched against XML-based product hierarchies to optimize shelf placement and category management
- Regulatory reporting in the seafood industry by verifying that rare or protected food items from catch logs are cross-checked against XML lists of approved categories for compliance

```
import os
import xml.etree.ElementTree as ET
import json

# Parse the XML file to extract all text elements under CATEGORIES
xml_path = "data/gaia/2023/validation/9b54f9d9-35ee-4a14-b62f-d130ea00317f/CATEGORIES.xml"

print("=== PARSING XML CATEGORIES FILE ===")
print(f"Analyzing file: {xml_path}")

# Check if file exists
if not os.path.exists(xml_path):
    print(f"Error: XML file '{xml_path}' does not exist.")
else:
    print(f"File exists: {xml_path}")
    file_size = os.path.getsize(xml_path)
    print(f"File size: {file_size} bytes")
    
    # Parse the XML file
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        print(f"\nRoot element: {root.tag}")
        print(f"Root attributes: {root.attrib}")
        
        # Display the XML structure
        print("\n=== XML STRUCTURE ANALYSIS ===")
        
        def analyze_element(element, level=0):
            indent = "  " * level
            print(f"{indent}Element: {element.tag}")
            if element.attrib:
                print(f"{indent}Attributes: {element.attrib}")
            if element.text and element.text.strip():
                print(f"{indent}Text: '{element.text.strip()}'")
            
            # Analyze children
            children = list(element)
            if children:
                print(f"{indent}Children count: {len(children)}")
                for child in children:
                    analyze_element(child, level + 1)
            
            return element.tag, element.text, element.attrib, len(children)
        
        # Analyze the complete structure
        analyze_element(root)
        
        # Extract all text elements specifically under CATEGORIES section
        print("\n=== EXTRACTING CATEGORIES TEXT ELEMENTS ===")
        
        categories_elements = []
        
        # Look for CATEGORIES elements
        categories_nodes = root.findall('.//CATEGORIES') + root.findall('.//categories')
        if not categories_nodes:
            # Try case-insensitive search
            for elem in root.iter():
                if elem.tag.lower() == 'categories':
                    categories_nodes.append(elem)
        
        print(f"Found {len(categories_nodes)} CATEGORIES nodes")
        
        if categories_nodes:
            for i, categories_node in enumerate(categories_nodes):
                print(f"\n--- CATEGORIES Node {i+1} ---")
                print(f"Tag: {categories_node.tag}")
                print(f"Attributes: {categories_node.attrib}")
                
                # Extract all text content from this categories node
                def extract_text_elements(element, path=""):
                    current_path = f"{path}/{element.tag}" if path else element.tag
                    
                    # If element has text content
                    if element.text and element.text.strip():
                        text_content = element.text.strip()
                        categories_elements.append({
                            'path': current_path,
                            'tag': element.tag,
                            'text': text_content,
                            'attributes': element.attrib
                        })
                        print(f"  Text element: {current_path} = '{text_content}'")
                    
                    # Process children
                    for child in element:
                        extract_text_elements(child, current_path)
                
                extract_text_elements(categories_node)
        else:
            print("No CATEGORIES section found. Extracting all text elements from XML...")
            
            # Extract all text elements from the entire XML
            def extract_all_text_elements(element, path=""):
                current_path = f"{path}/{element.tag}" if path else element.tag
                
                if element.text and element.text.strip():
                    text_content = element.text.strip()
                    categories_elements.append({
                        'path': current_path,
                        'tag': element.tag,
                        'text': text_content,
                        'attributes': element.attrib
                    })
                    print(f"  Text element: {current_path} = '{text_content}'")
                
                for child in element:
                    extract_all_text_elements(child, current_path)
            
            extract_all_text_elements(root)
        
        print(f"\nTotal text elements extracted: {len(categories_elements)}")
        
        # Now cross-reference with the three unique food items from spreadsheet analysis
        print("\n=== CROSS-REFERENCING WITH UNIQUE FOOD ITEMS ===")
        
        # From the previous analysis, the three unique food items are:
        unique_food_items = ['goat meat', 'mutton', 'turtle soup']
        print(f"Unique food items to search for: {unique_food_items}")
        
        # Search for these items in the XML text elements
        matches_found = []
        
        for food_item in unique_food_items:
            print(f"\n--- Searching for '{food_item}' ---")
            item_matches = []
            
            for element in categories_elements:
                text_lower = element['text'].lower()
                food_lower = food_item.lower()
                
                # Check for exact match
                if food_lower == text_lower:
                    item_matches.append({
                        'match_type': 'exact',
                        'element': element
                    })
                    print(f"  EXACT MATCH: {element['path']} = '{element['text']}'")
                
                # Check for partial match (contains)
                elif food_lower in text_lower or text_lower in food_lower:
                    item_matches.append({
                        'match_type': 'partial',
                        'element': element
                    })
                    print(f"  PARTIAL MATCH: {element['path']} = '{element['text']}'")
            
            if item_matches:
                matches_found.append({
                    'food_item': food_item,
                    'matches': item_matches
                })
                print(f"  Total matches for '{food_item}': {len(item_matches)}")
            else:
                print(f"  No matches found for '{food_item}'")
        
        # Determine which food item appears in XML categories
        print("\n=== FINAL ANALYSIS ===")
        
        if matches_found:
            print(f"Found matches for {len(matches_found)} food items:")
            
            for match_info in matches_found:
                food_item = match_info['food_item']
                matches = match_info['matches']
                
                print(f"\n'{food_item}' found in {len(matches)} XML elements:")
                for match in matches:
                    element = match['element']
                    print(f"  - {element['path']}: '{element['text']}' ({match['match_type']} match)")
                
                # If this food item has exact matches, it's a strong candidate
                exact_matches = [m for m in matches if m['match_type'] == 'exact']
                if exact_matches:
                    print(f"  *** '{food_item}' has {len(exact_matches)} exact match(es) in XML categories ***")
        else:
            print("No matches found for any of the unique food items in XML categories.")
        
        # Save analysis results
        xml_analysis = {
            'xml_file': xml_path,
            'file_size': file_size,
            'root_element': root.tag,
            'total_text_elements': len(categories_elements),
            'text_elements': categories_elements,
            'unique_food_items_searched': unique_food_items,
            'matches_found': matches_found
        }
        
        os.makedirs('workspace', exist_ok=True)
        with open('workspace/xml_categories_analysis.json', 'w') as f:
            json.dump(xml_analysis, f, indent=2)
        
        print(f"\nXML analysis saved to: workspace/xml_categories_analysis.json")
        
        # Summary
        print("\n=== SUMMARY ===")
        print(f"XML file parsed successfully: {xml_path}")
        print(f"Total text elements in categories: {len(categories_elements)}")
        print(f"Unique food items from spreadsheet: {unique_food_items}")
        print(f"Food items found in XML: {len(matches_found)}")
        
        if matches_found:
            print("\nFood items that appear in XML categories:")
            for match_info in matches_found:
                food_item = match_info['food_item']
                exact_count = len([m for m in match_info['matches'] if m['match_type'] == 'exact'])
                partial_count = len([m for m in match_info['matches'] if m['match_type'] == 'partial'])
                print(f"  - '{food_item}': {exact_count} exact, {partial_count} partial matches")
        
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
    except Exception as e:
        print(f"Error processing XML file: {e}")
```

## Created Time
2025-08-13 21:45:48
