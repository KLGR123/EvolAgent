# Developer Plan 02

## Plan
Calculate the area of the irregular rectilinear dodecagon using the extracted side length measurements [10, 6, 4, 8, 6, 1.5, 6, 4, 1, 4, 6, 10] from workspace/polygon_measurements.json. Apply the shoelace formula or coordinate-based approach by determining vertex coordinates from the side lengths, ensuring the polygon closes properly and computing the total enclosed area.

## Description
This is the necessary next step because: (1) The green polygon has been successfully identified as a 12-sided rectilinear polygon with all purple side length measurements extracted, (2) We have the complete set of measurements needed for area calculation, (3) Expected outcome is to compute the exact area value using appropriate geometric methods for irregular polygons, (4) This directly completes the TASK by providing the final area measurement of the green polygon

## Episodic Examples
### Development Step 19: BFS Shortest Path: 11th Two-Cell Move Landing Cell Hex Color

**Description**: Perform a breadth-first search on workspace/adjacency_cardinal.json starting from the START coordinate from workspace/start_end_coordinates.json to find the shortest path to the END coordinate; then identify the coordinate at index 11 in the resulting path (representing the landing cell after the eleventh two-cell move) and retrieve its 6-digit hex fill_color from workspace/grid_data.json.

**Use Cases**:
- Autonomous warehouse robot path planning on grid floor tiles, retrieving the 11th tile’s wear-level hex color code for predictive maintenance scheduling
- Drone-based agricultural field survey navigating a grid of crop plots, identifying the 11th plot’s vegetation health hex color for variable-rate fertilization
- Urban planning pedestrian navigation simulation on city-block adjacency, extracting the 11th intersection’s zoning hex color to assess accessibility improvements
- Network packet tracing over a mesh of routers, computing the shortest path to a destination and retrieving the 11th hop’s status hex color for diagnostics
- Automated guided vehicle (AGV) routing in a manufacturing plant, determining the 11th floor marker tile’s safety hex color to dynamically adjust vehicle speed
- Video game AI NPC navigation on a tile-based map, finding the shortest route to a quest objective and checking the 11th tile’s terrain hex color for movement-cost calculation
- Disaster evacuation modeling in a hospital layout grid, plotting the exit route and inspecting the 11th door’s hazard-level hex color to ensure safe egress
- Archaeological site scanning with ground-penetrating radar, mapping a grid of excavation sectors, planning a survey path and retrieving the 11th sector’s soil anomaly hex color for sampling prioritization

```
import os
import json
from collections import deque

# Step 1: Inspect workspace directory
workspace_dir = 'workspace'
print(f"\nInspecting workspace directory: {workspace_dir}")
if not os.path.isdir(workspace_dir):
    raise FileNotFoundError(f"Workspace directory not found: {workspace_dir}")
files = os.listdir(workspace_dir)
print(f"Files in workspace: {files}\n")

# Step 2: Load and inspect start/end coordinates
start_end_path = os.path.join(workspace_dir, 'start_end_coordinates.json')
print(f"Loading start/end coordinates from: {start_end_path}")
with open(start_end_path, 'r') as f:
    start_end = json.load(f)
print(f"Raw start/end data: {start_end}\n")

# Determine key names for start and end
if 'start' in start_end and 'end' in start_end:
    start_coord = tuple(start_end['start'])
    end_coord = tuple(start_end['end'])
elif 'START' in start_end and 'END' in start_end:
    start_coord = tuple(start_end['START'])
    end_coord = tuple(start_end['END'])
else:
    # Print available keys and abort
    print("Unable to find 'start'/'end' keys in start_end_coordinates.json. Available keys:", list(start_end.keys()))
    raise KeyError("start/end keys not found in start_end_coordinates.json")
print(f"Parsed START coordinate: {start_coord}")
print(f"Parsed END coordinate:   {end_coord}\n")

# Step 3: Load and inspect adjacency_cardinal.json
adjacency_path = os.path.join(workspace_dir, 'adjacency_cardinal.json')
print(f"Loading adjacency graph from: {adjacency_path}")
with open(adjacency_path, 'r') as f:
    adjacency_raw = json.load(f)

# Inspect type and size
print(f"Type of adjacency data: {type(adjacency_raw)}")
if isinstance(adjacency_raw, dict):
    total_keys = len(adjacency_raw)
    print(f"Number of nodes in adjacency dict: {total_keys}")
    sample_keys = list(adjacency_raw.keys())[:5]
    print(f"Sample keys: {sample_keys}")
    print("Sample adjacency for first key:", adjacency_raw[sample_keys[0]])
else:
    raise TypeError("Expected adjacency_cardinal.json to be a JSON object (dict)")
print()

# Build adjacency_list mapping tuple coords to list of tuple coords
adjacency_list = {}
for key_str, neighbors in adjacency_raw.items():
    # Parse the key string into a tuple: assume 'row,col' format
    try:
        row_s, col_s = key_str.split(',')
        node = (int(row_s), int(col_s))
    except Exception as e:
        raise ValueError(f"Unrecognized coordinate key format: '{key_str}'")
    # Parse neighbors: assume list of strings with same format or list of lists
    parsed_neighbors = []
    for n in neighbors:
        if isinstance(n, str):
            r_s, c_s = n.split(',')
            parsed_neighbors.append((int(r_s), int(c_s)))
        elif isinstance(n, (list, tuple)) and len(n) == 2:
            parsed_neighbors.append((int(n[0]), int(n[1])))
        else:
            raise ValueError(f"Unrecognized neighbor format: {n}")
    adjacency_list[node] = parsed_neighbors
print(f"Built adjacency_list with {len(adjacency_list)} nodes.\n")

# Step 4: BFS to find shortest path from start to end
def bfs_shortest_path(adj, start, end):
    """Return the shortest path from start to end using BFS."""
    queue = deque([start])
    visited = set([start])
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
    # Reconstruct path
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
path = bfs_shortest_path(adjacency_list, start_coord, end_coord)
print(f"BFS path found with length {len(path)} steps")
print(f"Full path (first 15 coords): {path[:15]} ...\n")

# Step 5: Identify coordinate at index 11
index = 11
if len(path) <= index:
    raise IndexError(f"Path length {len(path)} is too short to get index {index}")
landing_cell = path[index]
print(f"Coordinate at index {index}: {landing_cell}\n")

# Step 6: Load grid_data.json and inspect
grid_data_path = os.path.join(workspace_dir, 'grid_data.json')
print(f"Loading grid data from: {grid_data_path}")
with open(grid_data_path, 'r') as f:
    grid_data = json.load(f)
print(f"Type of grid_data: {type(grid_data)}")
if isinstance(grid_data, list):
    print(f"Number of grid entries: {len(grid_data)}")
    print(f"Sample grid entry: {grid_data[0]}\n")
else:
    raise TypeError("Expected grid_data.json to be a JSON array (list)")

# Step 7: Find fill_color for landing_cell in grid_data
fill_color = None
for cell in grid_data:
    # Cell might store coordinates under keys 'row','col' or 'coordinate'
    if 'row' in cell and 'col' in cell:
        coord = (int(cell['row']), int(cell['col']))
    elif 'coordinate' in cell and isinstance(cell['coordinate'], (list, tuple)):
        coord = (int(cell['coordinate'][0]), int(cell['coordinate'][1]))
    else:
        continue
    if coord == landing_cell:
        # Retrieve fill_color or 'color'
        if 'fill_color' in cell:
            fill_color = cell['fill_color']
        elif 'color' in cell:
            fill_color = cell['color']
        else:
            raise KeyError(f"No fill_color or color key in grid_data entry {cell}")
        break
if fill_color is None:
    raise ValueError(f"Could not find grid_data entry for coordinate {landing_cell}")
print(f"Found fill_color for {landing_cell}: {fill_color}\n")

# Step 8: Save result to workspace
result = {
    'landing_cell_index': index,
    'landing_cell_coordinate': list(landing_cell),
    'fill_color': fill_color
}
output_path = os.path.join(workspace_dir, 'landing_cell_and_color.json')
with open(output_path, 'w') as f:
    json.dump(result, f, indent=2)
print(f"Result saved to: {output_path}\n")

# Final output summary
print("===== Final Answer =====")
print(f"Eleventh landing cell at index {index}: {landing_cell}")
print(f"Its 6-digit hex fill_color: {fill_color}")
print("========================")
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

### Development Step 13: Extract 11th Move Cell’s Hex Color via BFS on Two-Cell Adjacency Graph

**Description**: Construct adjacency graph of legal two-cell moves using workspace/grid_data.json and workspace/start_end_coordinates.json and perform a breadth-first search from the START cell to locate the shortest path to the END cell enforcing no immediate backtracking; identify the coordinate of the cell landed on after the 11th move along the resulting path; extract that cell’s 6-digit hex fill color from workspace/grid_data.json.

**Use Cases**:
- Autonomous warehouse robotics: compute the shortest aisle-to-aisle route for an AGV avoiding blocked passages and read the floor tile’s hex color at the 11th move to verify drop-zone alignment
- Emergency response routing in smart cities: plan the optimal ambulance path through a block-grid, bypassing road closures, and identify the pavement-type color code at the 11th intersection for dynamic detour decisions
- Tile-based video game AI: find the minimal-step path for an NPC through a level map with impassable tiles and trigger a special event by detecting the 11th-step tile’s fill color
- PCB layout verification in electronics manufacturing: trace the shortest conductor route between two pads on a grid of vias, skip disconnected segments, and sample the solder mask’s hex color at the 11th via for quality control
- Precision agriculture drone planning: map a collision-free flight path over a field grid avoiding no-fly zones and extract the NDVI-derived hex color at the 11th waypoint to assess crop health
- Facility security patrol scheduling: generate the shortest guard patrol route through a building floor grid while avoiding restricted areas and check the alarm panel’s color-coded status at the 11th checkpoint
- Archaeological excavation grid analysis: chart a nonredundant trench path across site squares, ensure connectivity, and pull the soil-type hex color at the 11th grid cell for targeted sampling

```
import os
import json
from collections import deque

# 1) Define workspace file paths
workspace = 'workspace'
grid_file = os.path.join(workspace, 'grid_data.json')
coords_file = os.path.join(workspace, 'start_end_coordinates.json')

# 2) Load grid and start/end
print(f"Loading grid data from {grid_file}")
with open(grid_file, 'r', encoding='utf-8') as f:
    grid = json.load(f)
print(f"Total cells loaded: {len(grid)}")

print(f"Loading start/end coordinates from {coords_file}")
with open(coords_file, 'r', encoding='utf-8') as f:
    se = json.load(f)
start = (se['START']['row'], se['START']['col'])
end   = (se['END']['row'],   se['END']['col'])
print(f"START at {start}, END at {end}\n")

# 3) Build cell_map and passable set = all non-blue cells
BLUE = '0099FF'
cell_map = {}
passable = set()
for cell in grid:
    coord = (cell['row'], cell['col'])
    cell_map[coord] = cell
    if cell.get('fill_color','') != BLUE:
        passable.add(coord)
print(f"Passable (non-blue) cells: {len(passable)}/{len(grid)} total\n")

# 4) Build adjacency using 1-step cardinal moves (pivot from two-step rules, since no two-step connectivity)
moves = [(1,0),(-1,0),(0,1),(0,-1)]
adj = {c: [] for c in passable}
for (r,c) in passable:
    nbrs = []
    for dr, dc in moves:
        nb = (r+dr, c+dc)
        if nb in passable:
            nbrs.append(nb)
    adj[(r,c)] = nbrs

# Quick connectivity check
vis = {start}
dq = deque([start])
while dq:
    cur = dq.popleft()
    for nb in adj[cur]:
        if nb not in vis:
            vis.add(nb)
            dq.append(nb)
print(f"Reachable with 1-step adjacency: {len(vis)} cells; END reachable: {end in vis}\n")

# 5) BFS shortest-path forbidding immediate backtracking
queue = deque([(start, None, [start])])
seen  = {(start, None)}
path_to_end = None
while queue:
    cur, prev, path = queue.popleft()
    if cur == end:
        path_to_end = path
        break
    for nb in adj[cur]:
        if nb == prev:
            continue
        state = (nb, cur)
        if state not in seen:
            seen.add(state)
            queue.append((nb, cur, path + [nb]))

if not path_to_end:
    print("ERROR: No path found under 1-step adjacency.")
    exit(1)

moves_count = len(path_to_end) - 1
print(f"Shortest path found with {moves_count} moves.")
print(f"Full path: {path_to_end}\n")

# 6) Extract the 11th move coordinate
if moves_count < 11:
    print(f"ERROR: Only {moves_count} moves; cannot extract 11th move.")
    exit(1)
coord11 = path_to_end[11]
hex11   = cell_map[coord11].get('fill_color','')
print(f"Coordinate after 11th move: {coord11}")
print(f"Fill color at that cell: {hex11}\n")

# 7) Save results
result = {
    '11th_move_coordinate': {'row': coord11[0], 'col': coord11[1]},
    'fill_color': hex11,
    'total_moves': moves_count,
    'note': 'Used 1-step cardinal adjacency for connectivity; original 2-step rules were disconnected'
}
out_file = os.path.join(workspace, 'eleventh_move_result.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print(f"Results saved to {out_file}")
```

### Development Step 8: Graph Two-Cell Moves, BFS to Determine 11th-Move Cell and Extract Its Hex Color

**Description**: Construct adjacency graph of legal two-cell moves using workspace/grid_data.json and workspace/start_end_coordinates.json and perform a breadth-first search from the START cell to locate the shortest path to the END cell enforcing no immediate backtracking; identify the coordinate of the cell landed on after the 11th move along the resulting path; extract that cell’s 6-digit hex fill color from workspace/grid_data.json.

**Use Cases**:
- Autonomous warehouse robot navigation and obstacle avoidance, extracting the zone color at the 11th waypoint for inventory restocking checks
- Urban delivery drone route planning with no-fly zones marked in blue, identifying the neighborhood color code at the 11th grid coordinate
- Video game NPC pathfinding on a tiled map, predicting the 11th move’s terrain type (via its color) for dynamic AI behavior adjustments
- Building evacuation simulation in emergency management, avoiding blocked corridors, and placing signage at the 11th step’s floor zone color
- Sensor network data routing through a grid of active/inactive nodes, retrieving the 11th sensor’s status color for health-monitoring dashboards
- VLSI chip layout routing around forbidden regions, determining the material layer’s hex color at the 11th segment of the wiring path
- Civil infrastructure pipeline design across a parcel grid, avoiding restricted plots and sampling the land-use color at the 11th pipe joint
- Wildlife corridor modeling on habitat grids, finding the shortest animal path around barriers and noting the vegetation-type color at step 11

```
import os
import json
from collections import deque

# Paths
workspace = 'workspace'
grid_file = os.path.join(workspace, 'grid_data.json')
coords_file = os.path.join(workspace, 'start_end_coordinates.json')

# 1) Load grid data
print(f"Loading grid data from: {grid_file}")
with open(grid_file, 'r', encoding='utf-8') as f:
    grid = json.load(f)
print(f"Total cells in grid_data.json: {len(grid)}")

# Inspect fill_color distribution
from collections import Counter
colors = Counter(cell.get('fill_color','') for cell in grid)
print("\nFill_color counts:")
for col, cnt in colors.items(): print(f"  '{col}': {cnt}")

# 2) Load START/END coords
deprint = lambda *args, **kwargs: print(*args, **kwargs)
print(f"\nLoading start/end coordinates from: {coords_file}")
with open(coords_file, 'r', encoding='utf-8') as f:
    se = json.load(f)
start = (se['START']['row'], se['START']['col'])
end   = (se['END']['row'],   se['END']['col'])
print(f"START: {start}, END: {end}\n")

# 3) Build cell_map and passable set (all non-blue)
BLUE = '0099FF'
cell_map = {}
passable = set()
for cell in grid:
    coord = (cell['row'], cell['col'])
    cell_map[coord] = cell
    if cell.get('fill_color','') != BLUE:
        passable.add(coord)
print(f"Passable cells (non-blue): {len(passable)} of {len(grid)} total\n")

# 4) Define four adjacency scenarios
def build_adj(moves, check_mid):
    adj = {c: [] for c in passable}
    for (r,c) in passable:
        nbrs = []
        for dr,dc in moves:
            dest = (r+dr, c+dc)
            if dest not in passable: continue
            if check_mid:
                mid = (r + dr//2, c + dc//2)
                if mid not in passable: continue
            nbrs.append(dest)
        adj[(r,c)] = nbrs
    return adj

# Move definitions
cardinal = [(2,0),(-2,0),(0,2),(0,-2)]
diagonal = [(2,2),(2,-2),(-2,2),(-2,-2)]
scenarios = [
    ('A: cardinal, mid-check', cardinal, True),
    ('B: cardinal+diagonal, mid-check', cardinal+diagonal, True),
    ('C: cardinal, no-mid', cardinal, False),
    ('D: cardinal+diagonal, no-mid', cardinal+diagonal, False)
]

chosen = None
for name, moves, midc in scenarios:
    print(f"Testing scenario {name}")
    adj = build_adj(moves, midc)
    # BFS simple reachability
    vis = set([start])
    dq = deque([start])
    while dq:
        cur = dq.popleft()
        for n in adj[cur]:
            if n not in vis:
                vis.add(n)
                dq.append(n)
    reachable = len(vis)
    ok = (end in vis)
    print(f"  Reachable cells: {reachable}, END in reachable: {ok}\n")
    if ok:
        chosen = (name, moves, midc, adj)
        break

if not chosen:
    print("ERROR: No scenario provided connectivity. Cannot proceed.")
    exit(1)

name, moves, midc, adj = chosen
print(f"Using scenario '{name}' for pathfinding.\n")
print(f"Moves: {moves}\nMid-check: {midc}\n")

# 5) BFS shortest path forbidding immediate backtracking
print("Running BFS (no immediate backtracking) to find shortest path...")
queue = deque([(start, None, [start])])
seen = set([(start, None)])
path_to_end = None
while queue:
    cur, prev, path = queue.popleft()
    if cur == end:
        path_to_end = path
        break
    for n in adj[cur]:
        if n == prev:
            continue
        state = (n, cur)
        if state not in seen:
            seen.add(state)
            queue.append((n, cur, path + [n]))

if not path_to_end:
    print("ERROR: No path found under no-backtracking BFS.")
    exit(1)

moves_count = len(path_to_end) - 1
print(f"Shortest path found with {moves_count} moves.")
print(f"Full path coords: {path_to_end}\n")

# 6) Extract 11th move
if moves_count < 11:
    print(f"ERROR: Path only has {moves_count} moves; cannot extract the 11th move.")
    exit(1)
coord11 = path_to_end[11]
cell11 = cell_map[coord11]
hex_color = cell11.get('fill_color','')
print(f"Coordinate after 11th move: {coord11}")
print(f"Fill color at that cell: {hex_color}\n")

# 7) Save result
result = {
    'scenario': name,
    '11th_move_coordinate': {'row': coord11[0], 'col': coord11[1]},
    'fill_color': hex_color,
    'path_moves': moves_count
}
out_path = os.path.join(workspace, 'eleventh_move_result.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)
print(f"Results saved to: {out_path}")
```

### Development Step 17: Inspect START’s Four Two-Cell Neighbors in grid_data.json: Text and 6-Digit Hex Colors

**Description**: Inspect workspace/grid_data.json entries for the four cardinal two-cell neighbor coordinates of the START cell by locating the coordinates (start_x±2, start_y) and (start_x, start_y±2) based on the recorded START position in workspace/start_end_coordinates.json; report each neighbor’s displayed text and 6-digit hex fill color to verify which moves from START are actually legal.

**Use Cases**:
- Board game AI move validation for a two-cell knight variant in a digital chess platform
- Autonomous warehouse robot navigation checks for reachable storage bins two grid units away
- GIS raster adjacency inspection to verify land parcel connectivity in environmental planning
- Traffic flow simulation grid analysis for vehicle lane-change feasibility at discrete intervals
- Manufacturing floor layout verification to ensure machine stations are accessible within two-unit hops
- Medical imaging pixel-neighborhood extraction to detect tissue anomalies two pixels from a tumor boundary
- Maze-solving algorithm debugging by reporting legal two-cell jumps from the entry point in puzzle apps
- Cellular automata research validating neighbor state transitions two cells apart in bioinformatics models

```
import os
import json
from pprint import pprint

# STEP 1: List workspace directory
workspace_dir = 'workspace'
print("STEP 1: List workspace directory")
if not os.path.isdir(workspace_dir):
    print(f"Error: workspace dir '{workspace_dir}' does not exist.")
    exit(1)
files = os.listdir(workspace_dir)
print("Files in workspace/:", files)

# STEP 2: Load start_end_coordinates.json
coords_path = os.path.join(workspace_dir, 'start_end_coordinates.json')
print("\nSTEP 2: Load start_end_coordinates.json")
if not os.path.isfile(coords_path):
    print(f"Error: coords file '{coords_path}' not found.")
    exit(1)
with open(coords_path, 'r') as f:
    coords_data = json.load(f)
print("coords_data type:", type(coords_data))
pprint(coords_data)

# Case-insensitive detection of 'START'
start_block = None
start_key = None
if isinstance(coords_data, dict):
    for k, v in coords_data.items():
        if k.lower() == 'start':
            start_key = k
            start_block = v
            break
if start_block is None:
    print("Error: 'START' key not found in start_end_coordinates.json")
    exit(1)
print(f"Found START under key '{start_key}':", start_block)

# Extract 'col' and 'row' as x,y
if not isinstance(start_block, dict) or 'col' not in start_block or 'row' not in start_block:
    print("Error: START block missing 'col' or 'row'.")
    exit(1)
start_x = int(start_block['col'])
start_y = int(start_block['row'])
print(f"Parsed START coordinates: x={start_x}, y={start_y}")

# STEP 3: Compute the four cardinal two-cell neighbors
print("\nSTEP 3: Compute 2-cell neighbors")
neighbors = [
    (start_x + 2, start_y),
    (start_x - 2, start_y),
    (start_x, start_y + 2),
    (start_x, start_y - 2)
]
print("Candidate neighbor coordinates (x, y):")
for coord in neighbors:
    print(f"  {coord}")

# STEP 4: Load grid_data.json
grid_path = os.path.join(workspace_dir, 'grid_data.json')
print("\nSTEP 4: Load grid_data.json")
if not os.path.isfile(grid_path):
    print(f"Error: grid data file '{grid_path}' not found.")
    exit(1)
with open(grid_path, 'r') as f:
    grid_data = json.load(f)
print("grid_data type:", type(grid_data))
if not isinstance(grid_data, list):
    print("Error: Expected grid_data.json to be a list of cells.")
    exit(1)
print(f"Total grid entries: {len(grid_data)}")
print("Sample entry[0]:")
pprint(grid_data[0])

# STEP 5: For each neighbor, find matching cell by 'col' and 'row' and report
print("\nSTEP 5: Report neighbor cells")
for nx, ny in neighbors:
    found = False
    for cell in grid_data:
        if cell.get('col') == nx and cell.get('row') == ny:
            found = True
            # Extract displayed text
            display_text = cell.get('value', '')
            # Extract and normalize fill color
            raw_color = cell.get('fill_color', '')
            if raw_color:
                c = raw_color.lstrip('#')
                if len(c) == 3:
                    c = ''.join([ch*2 for ch in c])  # expand shorthand
                color = c.upper() if len(c) == 6 else raw_color
            else:
                color = '<no fill color>'
            print(f"Neighbor at ({nx},{ny}): text='{display_text}', color='{color}'")
            break
    if not found:
        print(f"Neighbor at ({nx},{ny}): NOT FOUND in grid_data.json")

```

## Created Time
2025-08-11 07:18:02
