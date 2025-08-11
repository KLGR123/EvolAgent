# Developer Plan 01

## Plan
Parse and analyze the attached Excel file data/gaia/2023/validation/4d51c4bf-4b0e-4f3d-897b-3f6687a7d9f2.xlsx to extract the complete client list for the retractable awning company. Identify the data structure including client information and street addresses, then determine which clients have even-numbered street addresses (indicating west-facing houses that would need sunset awning designs) versus odd-numbered addresses (indicating east-facing houses that would need sunrise awning designs). Count the total number of clients who will receive sunset awning designs based on their even-numbered street addresses.

## Description
This is the optimal first step because: (1) We need to understand the Excel file structure and extract all client data including street addresses before determining awning design requirements, (2) No previous analysis has been performed on this file, (3) Expected outcome is to have complete client data with street addresses identified and categorized by odd/even numbering, (4) This provides the foundation needed to count clients with even-numbered addresses who will receive sunset awning designs as requested in the TASK

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

### Development Step 2: Identify and Visualize Earl Smith’s Green Land Plot Cells in Excel Layout

**Description**: Parse and analyze the attached Excel spreadsheet file data/gaia/2023/validation/5cfb274c-0207-4aa7-9575-6ac0bd95d9b2.xlsx to identify all green cells representing Earl Smith's land plots. Extract the cell positions, colors, and create a visual representation of the spreadsheet layout to understand the spatial distribution of Earl's plots relative to other landowners' plots.

**Use Cases**:
- Real estate portfolio mapping and visual distribution analysis for commercial property management firms
- Municipal zoning extraction and GIS integration for urban planning departments
- Agricultural subsidy eligibility scanning and field plot mapping for government farm agencies
- Habitat conservation data parsing and protected area mapping for environmental NGOs
- Utility service area identification and maintenance scheduling for energy infrastructure operators
- Construction site allocation parsing and resource coordination for general contractor firms
- Insurance risk plot identification and premium calculation optimization for underwriting teams
- Community land tenure extraction and documentation mapping for international development NGOs

```
import os
import pandas as pd
from openpyxl import load_workbook
import json

# First, let's inspect the existing analysis file to understand its structure
analysis_file = 'workspace/earl_smith_analysis_initial.json'

print("=== INSPECTING PREVIOUS ANALYSIS RESULTS ===")
if os.path.exists(analysis_file):
    print(f"Found existing analysis file: {analysis_file}")
    
    # Read and inspect the JSON structure
    with open(analysis_file, 'r') as f:
        analysis_data = json.load(f)
    
    print("\nJSON structure:")
    for key in analysis_data.keys():
        print(f"  - {key}: {type(analysis_data[key])}")
        if isinstance(analysis_data[key], list) and len(analysis_data[key]) > 0:
            print(f"    Sample item: {analysis_data[key][0]}")
        elif isinstance(analysis_data[key], dict):
            print(f"    Keys: {list(analysis_data[key].keys())[:5]}...")
    
    print(f"\nTotal green cells from previous analysis: {analysis_data.get('total_green_cells', 0)}")
    
    # Display green cells for verification
    green_cells = analysis_data.get('green_cells', [])
    print(f"\nDetailed green cell analysis:")
    for i, cell in enumerate(green_cells):
        print(f"  {i+1}. {cell.get('address', 'Unknown')} - Value: '{cell.get('value', '')}' - Color: {cell.get('fill_color', 'None')}")
else:
    print(f"Analysis file not found: {analysis_file}")

# Now let's reload the Excel file and do a more comprehensive analysis
print("\n" + "="*60)
print("COMPREHENSIVE ANALYSIS: EARL SMITH'S LAND PLOTS")
print("="*60)

xlsx_path = "data/gaia/2023/validation/5cfb274c-0207-4aa7-9575-6ac0bd95d9b2.xlsx"

# Load the workbook
wb = load_workbook(xlsx_path, data_only=False)
sheet = wb.active  # Get the first (and only) sheet

print(f"\nAnalyzing sheet: {sheet.title}")
print(f"Dimensions: {sheet.max_row} rows x {sheet.max_column} columns")

# Create a complete grid analysis
print("\n=== COMPLETE CELL GRID ANALYSIS ===")

# First, let's examine ALL cells to understand the layout
all_cells = []
for row in range(1, sheet.max_row + 1):
    for col in range(1, sheet.max_column + 1):
        cell = sheet.cell(row=row, column=col)
        
        # Get cell value
        cell_value = cell.value if cell.value is not None else ""
        
        # Get fill color information
        fill_color = None
        fill_type = None
        
        if cell.fill and hasattr(cell.fill, 'start_color') and cell.fill.start_color:
            if hasattr(cell.fill.start_color, 'rgb') and cell.fill.start_color.rgb:
                fill_color = cell.fill.start_color.rgb
                fill_type = 'rgb'
        
        # Create cell address (A1, B2, etc.)
        cell_address = f"{chr(64 + col)}{row}" if col <= 26 else f"{chr(64 + col//26)}{chr(64 + col%26)}{row}"
        
        cell_data = {
            'row': row,
            'col': col,
            'address': cell_address,
            'value': str(cell_value),
            'fill_color': fill_color,
            'fill_type': fill_type
        }
        
        all_cells.append(cell_data)

print(f"Analyzed {len(all_cells)} total cells")

# Identify Earl Smith's plots by examining both green colors AND text content
print("\n=== IDENTIFYING EARL SMITH'S PLOTS ===")

earl_plots = []
green_cells = []
other_colored_cells = []

# First, let's examine cells with any content or color
for cell in all_cells:
    has_content = cell['value'] and cell['value'].strip() != ""
    has_color = cell['fill_color'] and cell['fill_color'] != "00000000"
    
    if has_content or has_color:
        print(f"Cell {cell['address']}: Value='{cell['value']}', Color={cell['fill_color']}")
        
        # Check if it's green (FF00FF00 as identified in previous analysis)
        if cell['fill_color'] == 'FF00FF00':
            green_cells.append(cell)
            print(f"  -> GREEN CELL identified")
            
            # Check if this is Earl Smith's plot
            if 'earl' in cell['value'].lower() or 'smith' in cell['value'].lower():
                earl_plots.append(cell)
                print(f"  -> EARL SMITH'S PLOT confirmed by text")
            else:
                # Even if no text confirmation, green cells are likely Earl's based on problem context
                earl_plots.append(cell)
                print(f"  -> Assumed EARL SMITH'S PLOT (green color)")
        
        elif cell['fill_color'] and cell['fill_color'] != "00000000":
            other_colored_cells.append(cell)
            print(f"  -> Other colored cell")

print(f"\nSUMMARY:")
print(f"Total green cells (FF00FF00): {len(green_cells)}")
print(f"Earl Smith's plots identified: {len(earl_plots)}")
print(f"Other colored cells: {len(other_colored_cells)}")

# Create visual representation
print("\n=== VISUAL REPRESENTATION OF SPREADSHEET LAYOUT ===")
print("Legend: E = Earl Smith's plot, X = Other landowner, . = Empty")
print()

# Create a visual grid
print("   ", end="")
for col in range(1, sheet.max_column + 1):
    print(f"{chr(64 + col):>3}", end="")
print()

for row in range(1, sheet.max_row + 1):
    print(f"{row:>2} ", end="")
    
    for col in range(1, sheet.max_column + 1):
        # Find the cell data for this position
        cell_data = next((c for c in all_cells if c['row'] == row and c['col'] == col), None)
        
        if cell_data:
            if cell_data['fill_color'] == 'FF00FF00':
                print("  E", end="")  # Earl Smith's plot
            elif cell_data['fill_color'] and cell_data['fill_color'] != "00000000":
                print("  X", end="")  # Other landowner
            else:
                print("  .", end="")  # Empty or no color
        else:
            print("  .", end="")  # Empty
    
    print()  # New line for next row

# Create detailed analysis of Earl's plots
print("\n=== DETAILED ANALYSIS OF EARL SMITH'S PLOTS ===")
print(f"Earl Smith owns {len(earl_plots)} land plots:")

for i, plot in enumerate(earl_plots, 1):
    print(f"Plot {i}: Cell {plot['address']} (Row {plot['row']}, Column {plot['col']})")
    print(f"  Value: '{plot['value']}'")
    print(f"  Color: {plot['fill_color']}")

# Analyze spatial distribution
if earl_plots:
    rows = [plot['row'] for plot in earl_plots]
    cols = [plot['col'] for plot in earl_plots]
    
    print(f"\nSpatial Distribution:")
    print(f"  Row range: {min(rows)} to {max(rows)}")
    print(f"  Column range: {min(cols)} to {max(cols)}")
    print(f"  Total area span: {max(rows) - min(rows) + 1} rows x {max(cols) - min(cols) + 1} columns")

# Save comprehensive results
results = {
    'analysis_summary': {
        'total_cells_analyzed': len(all_cells),
        'earl_smith_plots': len(earl_plots),
        'green_cells_total': len(green_cells),
        'other_colored_cells': len(other_colored_cells)
    },
    'earl_smith_plots': earl_plots,
    'green_cells': green_cells,
    'other_colored_cells': other_colored_cells,
    'spatial_analysis': {
        'rows_occupied': list(set(plot['row'] for plot in earl_plots)),
        'columns_occupied': list(set(plot['col'] for plot in earl_plots)),
        'row_range': [min(plot['row'] for plot in earl_plots), max(plot['row'] for plot in earl_plots)] if earl_plots else None,
        'column_range': [min(plot['col'] for plot in earl_plots), max(plot['col'] for plot in earl_plots)] if earl_plots else None
    }
}

with open('workspace/earl_smith_complete_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nComplete analysis saved to: workspace/earl_smith_complete_analysis.json")
print("\nAnalysis complete! Earl Smith's land plots have been identified and mapped.")
```

### Development Step 1: Parse File Road Layout, Locate Houses, Mile Markers, Define Coordinates, Compute House-Tower Distances

**Description**: Parse and analyze the attached file data/gaia/2023/validation/389793a7-ca17-4e82-81cb-2b3a2391b4b9.txt to understand the road layout, identify all house positions, and map their locations relative to mile markers. Extract the visual representation showing dashes (-) as mile markers and H symbols as houses, then determine the coordinate system and calculate distances between houses and potential tower locations.

**Use Cases**:
- Rural broadband deployment planning: parse the ASCII road layout to extract house locations by mile marker, then calculate optimal fiber cable routes to bring high-speed internet to each home.
- Emergency medical services optimization: analyze the distances between mapped house positions and candidate ambulance station sites to determine the fastest response coverage along a remote highway.
- Postal delivery route automation: ingest the text-based road map to pinpoint rural mailbox locations, then compute the shortest delivery loop for mail carriers using mile-marker coordinates.
- Electric grid maintenance scheduling: map household positions relative to power line inspection crews’ depots to sequence pipeline or line checks by proximity and minimize downtime.
- Mobile network coverage analysis: identify service gaps by measuring distances from village houses to existing cell towers and recommend new tower installations to fill black spots.
- Environmental sensor network design: use the extracted house coordinates along farmland roads to position weather or soil-moisture sensors at optimal intervals for agricultural research.
- Real estate site evaluation: chart the distribution of roadside properties via mile markers to spotlight high-density clusters for targeted development and marketing campaigns.

```
import os

# First, let's examine the attached file to understand its structure and content
file_path = 'data/gaia/2023/validation/389793a7-ca17-4e82-81cb-2b3a2391b4b9.txt'

print("=== FILE ANALYSIS ===")
print(f"Examining file: {file_path}")

# Check if file exists
if os.path.exists(file_path):
    print(f"File exists: {file_path}")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    print(f"File size: {file_size} bytes")
    
    # Read and display the entire content since it's likely a small text file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\nFile content length: {len(content)} characters")
    print(f"Number of lines: {len(content.splitlines())}")
    
    print("\n=== FULL FILE CONTENT ===")
    print(content)
    print("=== END OF FILE CONTENT ===")
    
    # Analyze the content structure
    lines = content.splitlines()
    print(f"\n=== CONTENT ANALYSIS ===")
    print(f"Total lines: {len(lines)}")
    
    # Look for patterns in each line
    for i, line in enumerate(lines, 1):
        print(f"Line {i}: '{line}' (length: {len(line)})")
        
        # Check for specific characters that might represent houses (H) and mile markers (-)
        h_count = line.count('H')
        dash_count = line.count('-')
        space_count = line.count(' ')
        
        if h_count > 0 or dash_count > 0:
            print(f"  -> Houses (H): {h_count}, Dashes (-): {dash_count}, Spaces: {space_count}")
    
    # Look for any numeric patterns that might indicate mile markers or coordinates
    import re
    numbers = re.findall(r'\d+', content)
    if numbers:
        print(f"\nNumbers found in content: {numbers}")
    
    # Save the content to workspace for further processing
    with open('workspace/road_layout_raw.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\nRaw content saved to: workspace/road_layout_raw.txt")
    
else:
    print(f"Error: File not found at {file_path}")
    print("Available files in data directory:")
    if os.path.exists('data'):
        for root, dirs, files in os.walk('data'):
            for file in files:
                print(f"  - {os.path.join(root, file)}")
    else:
        print("  - data directory not found")
```

### Development Step 1: Visualizing Earl Smith’s Green Cells in Land Plot Excel Spreadsheet

**Description**: Parse and analyze the attached Excel spreadsheet file data/gaia/2023/validation/5cfb274c-0207-4aa7-9575-6ac0bd95d9b2.xlsx to identify all green cells representing Earl Smith's land plots. Extract the cell positions, colors, and create a visual representation of the spreadsheet layout to understand the spatial distribution of Earl's plots relative to other landowners' plots.

**Use Cases**:
- Government cadastral mapping and land registry automation by extracting color‐coded ownership plots to update digital map databases
- Real estate due diligence workflows that visualize Excel‐highlighted property parcels owned by specific investors for investment analysis
- Agricultural field management systems identifying green‐coded crop plots per farmer to optimize resource allocation and yield forecasting
- Environmental impact assessments locating green‐highlighted conservation areas within survey spreadsheets to integrate with GIS for habitat protection
- Urban planning and zoning compliance checks extracting color‐designated residential, commercial, and industrial parcels from city planning documents
- Insurance underwriting risk profiling by mapping green-shaded floodplain or landslide-prone zones in survey workbooks for policy pricing
- Infrastructure project land acquisition tracking by compiling Excel‐flagged stakeholder parcels into visual layouts for negotiation and planning
- Legal boundary dispute resolution supporting attorneys in extracting lawyer‐marked colored cells representing contested lot lines to prepare court exhibits

```
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import json

# The path to the Excel file to be parsed
xlsx_path = "data/gaia/2023/validation/5cfb274c-0207-4aa7-9575-6ac0bd95d9b2.xlsx"

print("=== EXCEL FILE ANALYSIS FOR EARL SMITH'S LAND PLOTS ===")
print(f"Analyzing file: {xlsx_path}")

# Check if file exists
if not os.path.exists(xlsx_path):
    print(f"Error: Excel file '{xlsx_path}' does not exist.")
    exit()

print(f"File exists: {xlsx_path}")
file_size = os.path.getsize(xlsx_path)
print(f"File size: {file_size} bytes")

# Load workbook with openpyxl to access cell formatting and colors
print("\nLoading workbook with openpyxl to access cell colors...")
wb = load_workbook(xlsx_path, data_only=False)  # Keep formulas and formatting

print(f"Number of worksheets: {len(wb.worksheets)}")
print(f"Worksheet names: {[sheet.title for sheet in wb.worksheets]}")

# Process each worksheet
all_green_cells = []
all_cells_data = []

for sheet_idx, sheet in enumerate(wb.worksheets):
    print(f"\n=== ANALYZING WORKSHEET: {sheet.title} ===")
    
    max_row = sheet.max_row
    max_col = sheet.max_column
    print(f"Sheet dimensions: {max_row} rows x {max_col} columns")
    
    # Get the range of actual data
    min_row = sheet.min_row
    min_col = sheet.min_column
    print(f"Data range: rows {min_row}-{max_row}, columns {min_col}-{max_col}")
    
    green_cells_in_sheet = []
    cells_data_in_sheet = []
    
    # Analyze each cell for content and color
    print("\nScanning cells for content and colors...")
    
    for row in range(min_row, min(max_row + 1, min_row + 50)):  # Limit to first 50 rows for initial analysis
        for col in range(min_col, min(max_col + 1, min_col + 50)):  # Limit to first 50 cols
            cell = sheet.cell(row=row, column=col)
            cell_address = f"{chr(64 + col)}{row}" if col <= 26 else f"{chr(64 + col//26)}{chr(64 + col%26)}{row}"
            
            # Get cell value
            cell_value = cell.value if cell.value is not None else ""
            
            # Get fill color
            fill = cell.fill
            fill_color = None
            fill_type = None
            
            if fill and hasattr(fill, 'start_color') and fill.start_color:
                if hasattr(fill.start_color, 'rgb') and fill.start_color.rgb:
                    fill_color = fill.start_color.rgb
                    fill_type = 'rgb'
                elif hasattr(fill.start_color, 'indexed') and fill.start_color.indexed:
                    fill_color = fill.start_color.indexed
                    fill_type = 'indexed'
                elif hasattr(fill.start_color, 'theme') and fill.start_color.theme:
                    fill_color = fill.start_color.theme
                    fill_type = 'theme'
            
            # Store cell data
            cell_data = {
                'sheet': sheet.title,
                'row': row,
                'col': col,
                'address': cell_address,
                'value': str(cell_value),
                'fill_color': fill_color,
                'fill_type': fill_type
            }
            
            cells_data_in_sheet.append(cell_data)
            
            # Check if cell has green background
            is_green = False
            if fill_color:
                # Check for green colors (various shades)
                if fill_type == 'rgb':
                    # Convert hex to check for green-ish colors
                    if isinstance(fill_color, str) and len(fill_color) >= 6:
                        try:
                            # Extract RGB values
                            r = int(fill_color[-6:-4], 16) if len(fill_color) >= 6 else 0
                            g = int(fill_color[-4:-2], 16) if len(fill_color) >= 4 else 0
                            b = int(fill_color[-2:], 16) if len(fill_color) >= 2 else 0
                            
                            # Check if it's green-ish (green component higher than others)
                            if g > r and g > b and g > 100:  # Some threshold for green
                                is_green = True
                        except ValueError:
                            pass
                
                # For indexed colors, common green indices
                elif fill_type == 'indexed':
                    green_indices = [3, 10, 11, 43, 50, 51]  # Common green color indices in Excel
                    if fill_color in green_indices:
                        is_green = True
            
            if is_green or (cell_value and 'earl' in str(cell_value).lower()):
                green_cells_in_sheet.append(cell_data)
                print(f"  Potential Earl's plot: {cell_address} = '{cell_value}' (color: {fill_color}, type: {fill_type})")
    
    print(f"\nFound {len(green_cells_in_sheet)} potential green cells in {sheet.title}")
    all_green_cells.extend(green_cells_in_sheet)
    all_cells_data.extend(cells_data_in_sheet)

print(f"\n=== SUMMARY ===")
print(f"Total potential green cells found: {len(all_green_cells)}")
print(f"Total cells analyzed: {len(all_cells_data)}")

# Display first few green cells for verification
print("\n=== FIRST 10 POTENTIAL GREEN CELLS ===")
for i, cell in enumerate(all_green_cells[:10]):
    print(f"{i+1}. Sheet '{cell['sheet']}' Cell {cell['address']} (Row {cell['row']}, Col {cell['col']}):")
    print(f"   Value: '{cell['value']}'")
    print(f"   Color: {cell['fill_color']} (type: {cell['fill_type']})")

# Look for all unique colors to understand the color scheme
print("\n=== UNIQUE COLORS FOUND ===")
unique_colors = {}
for cell in all_cells_data:
    if cell['fill_color']:
        color_key = f"{cell['fill_color']} ({cell['fill_type']})"
        if color_key not in unique_colors:
            unique_colors[color_key] = []
        unique_colors[color_key].append(f"{cell['sheet']}!{cell['address']}")

for color, cells in unique_colors.items():
    print(f"Color {color}: {len(cells)} cells")
    if len(cells) <= 5:
        print(f"  Cells: {', '.join(cells)}")
    else:
        print(f"  Sample cells: {', '.join(cells[:5])}... (+{len(cells)-5} more)")

# Save data to workspace for further analysis
analysis_results = {
    'total_green_cells': len(all_green_cells),
    'green_cells': all_green_cells,
    'unique_colors': {color: len(cells) for color, cells in unique_colors.items()},
    'sheets_analyzed': [sheet.title for sheet in wb.worksheets]
}

with open('workspace/earl_smith_analysis_initial.json', 'w') as f:
    json.dump(analysis_results, f, indent=2)

print(f"\nInitial analysis saved to: workspace/earl_smith_analysis_initial.json")
print("\nNext step: Refine green color detection and create visual representation")
```

## Created Time
2025-08-11 07:01:30
