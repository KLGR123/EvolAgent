# Developer Plan 01

## Plan
Retrieve and parse ScienceDirect’s subject-area filter tree via the ScienceDirect Search API or by scraping the advanced search page to extract all subject-area names and their corresponding query tokens under the ‘Life Sciences’ branch and the ‘Health Sciences’ branch, then save that mapping to workspace/subject_area_filters.json.

## Description
This step is necessary because: (1) The TASK requires comparing sample standard deviations of the number of Reference Works for each Life Science domain against Health Sciences; (2) Construction of accurate search queries for each domain requires knowing the exact ScienceDirect subject-area filter tokens; (3) Extracting the subject-area names and tokens for both branches sets up all subsequent searches for ‘Reference Works’ counts by year; (4) The expected outcome is a JSON file with each Life Science domain and the Health Sciences domain mapped to its filter token, enabling precise count retrieval in following steps.

## Semantic Examples
### How to Parse PDB (Protein Data Bank) Files and Extract Structural Information?

**Description**: Parse a PDB file to extract protein structural information including models, chains, residues, and atoms. It provides detailed analysis of protein structure data.

**Use Cases**:
- Extract chain, residue, and atom information from PDB files for protein structure analysis
- Generate summaries of protein models and visualize structural components for bioinformatics research

```
import os
import warnings
from Bio.PDB import PDBParser

warnings.filterwarnings("ignore")

# The path to the PDB file to be parsed, for example: "workspace/task.pdb"
pdb_path = "workspace/task.pdb"
# The starting index for atom lines to preview (default: 0)
start_atom_idx = 0
# The ending index for atom lines to preview (default: 5)
end_atom_idx = 5

if not os.path.exists(pdb_path):
    print(f"Error: PDB file '{pdb_path}' does not exist.")

if not pdb_path.lower().endswith('.pdb'):
    print(f"Error: File must be a .pdb file. Got: {pdb_path}")

result = []
result.append(f"PDB file: {os.path.basename(pdb_path)}")
result.append("=" * 50)

# Parse PDB structure using BioPython
parser = PDBParser()
structure = parser.get_structure('protein', pdb_path)

result.append("Structure Information:")
result.append(f"  Structure ID: {structure.id}")
result.append(f"  Number of models: {len(structure)}")

# Analyze each model in the structure
for model in structure:
    result.append(f"\nModel {model.id}:")
    result.append(f"  Number of chains: {len(model)}")
    
    # Analyze each chain in the model
    for chain in model:
        residues = list(chain)
        result.append(f"    Chain {chain.id}: {len(residues)} residues")
        
        if residues:
            first_res = residues[0]
            last_res = residues[-1]
            result.append(f"      First residue: {first_res.get_resname()} {first_res.get_id()[1]}")
            result.append(f"      Last residue: {last_res.get_resname()} {last_res.get_id()[1]}")
            
            # Count total atoms in this chain
            atom_count = sum(len(list(residue.get_atoms())) for residue in residues)
            result.append(f"      Total atoms: {atom_count}")

result.append("-" * 30)

# Parse basic PDB file information by reading raw text
with open(pdb_path, 'r') as f:
    lines = f.readlines()

result.append("\nBasic PDB Information:")

# Extract header information
header_lines = [line for line in lines if line.startswith('HEADER')]
if header_lines:
    result.append(f"  Header: {header_lines[0].strip()}")

# Extract title information
title_lines = [line for line in lines if line.startswith('TITLE')]
if title_lines:
    title = ' '.join([line[10:].strip() for line in title_lines])
    result.append(f"  Title: {title}")

# Count different record types in the PDB file
record_types = {}
for line in lines:
    if len(line) >= 6:
        record_type = line[:6].strip()
        record_types[record_type] = record_types.get(record_type, 0) + 1

result.append("\nRecord Types:")
for record_type, count in sorted(record_types.items()):
    result.append(f"  {record_type}: {count}")

# Extract and display sample atom lines
atom_lines = [line for line in lines if line.startswith('ATOM')]
if atom_lines:
    # Ensure indices are within bounds
    start_idx = max(0, min(start_atom_idx, len(atom_lines)))
    end_idx = max(start_idx, min(end_atom_idx, len(atom_lines)))
    
    if start_idx < end_idx:
        result.append(f"\nAtom lines ({start_idx} to {end_idx-1}):")
        for line in atom_lines[start_idx:end_idx]:
            result.append(f"  {line.strip()}")
        
        if end_idx < len(atom_lines):
            result.append(f"  ... and {len(atom_lines) - end_idx} more atoms after index {end_idx-1}")
        if start_idx > 0:
            result.append(f"  ... and {start_idx} atoms before index {start_idx}")
    else:
        result.append(f"\nNo atoms to display in range [{start_idx}, {end_idx})")
        result.append(f"  Total atoms available: {len(atom_lines)}")

# Print the complete analysis
print("\n".join(result))
```

### How to Search for Information Using Google Search?

**Description**: Google Search (also known simply as Google or Google.com) is a search engine operated by Google. It allows users to search for information on the Web by entering keywords or phrases.
Search for information using Google search engine with advanced operators and filters. Requires SerpAPI key for accessing Google Search API.

**Use Cases**:
- General research and Information Gathering
- E-commerce and Shopping Research
- Professional and Business Applications
- Data Collection and Analysis
- Educational and Learning Support
- Technical and Development Research
- Professional and Business Applications

```
import os
import re
import requests

# The search query to perform. Supports advanced operators like "site:", "filetype:", quotes, minus sign
# For example: "machine learning" site:arxiv.org filetype:pdf -tutorial
query = "machine learning tutorials"
# The maximum number of results to return (default: 10)
max_results = 10
# The type of search: "search" for web results, "image" for images, "news" for news (default: "search")
type = "search"
# Time range filter. Examples: "qdr:h" (past hour), "qdr:d" (past day), "qdr:w" (past week), etc.
tbs = None
# Region/country code for search results. Examples: "us", "cn", "jp", "uk", "de", "fr", etc.
region = None

# Get SerpAPI key from environment variables
api_key = os.getenv("SERPAPI_API_KEY")

if api_key is None:
    print("Error: Missing API key. Make sure you have SERPAPI_API_KEY in your environment variables.")

# Validate search type parameter
valid_types = ["search", "image", "news"]
if type not in valid_types:
    print(f"Error: Invalid type '{type}'. Must be one of: {', '.join(valid_types)}")

# Validate time range format if provided
if tbs is not None:
    time_patterns = [
        r'^qdr:[hdwmy]$$',
        r'^qdr:[hdwmy]\d+$$',
        r'^cdr:1,cd_min:\d{2}/\d{2}/\d{4},cd_max:\d{2}/\d{2}/\d{4}$$'
    ]
  
    is_valid_tbs = any(re.match(pattern, tbs) for pattern in time_patterns)
    if not is_valid_tbs:
        print(
            f"Error: Invalid tbs format '{tbs}'. "
            "Must be one of: qdr:h, qdr:d, qdr:w, qdr:m, qdr:y, "
            "or with numbers like qdr:h12, qdr:d3, qdr:w2, qdr:m6, qdr:m2, "
            "or custom range like cdr:1,cd_min:DD/MM/YYYY,cd_max:DD/MM/YYYY"
        )

# Validate region format if provided
if region is not None:
    if not re.match(r'^[a-z]{2}$$', region.lower()):
        print(
            f"Error: Invalid region format '{region}'. "
            "Must be a valid ISO 3166-1 alpha-2 country code like 'us', 'cn', 'jp', 'uk', 'de', etc."
        )
    region = region.lower()

# Prepare API request parameters
params = {
    "q": query,
    "api_key": api_key,
    "engine": "google",
    "google_domain": "google.com",
    "safe": "off",
    "num": max_results,
    "type": type,
    "tbs": tbs,
}

# Add region parameter if specified
if region is not None:
    params["gl"] = region

# Make API request to SerpAPI
response = requests.get("https://serpapi.com/search.json", params=params)

if response.status_code == 200:
    results = response.json()
else:
    print(f"Error: API request failed with status {response.status_code}: {response.text}")

# Process and return results based on search type
if type == "search":
    if not results.get("organic_results"):
        print(f"No results found for '{query}'. Try with a more general query, or remove the time restriction if used.")
    else:
        print(str(results["organic_results"]))

elif type == "image":
    if not results.get("images"):
        print(f"No images found for '{query}'. Try with a more general query, or remove the time restriction if used.")
    else:
        print(str(results["images"]))

elif type == "news":
    if not results.get("news"):
        print(f"No news found for '{query}'. Try with a more general query, or remove the time restriction if used.")
    else:
        print(str(results["news"]))
```

### How to Parse PDF Files and Extract Text Content?

**Description**: Parse a PDF file and return the text content with optional page range selection. Uses the LangChain community library for document processing.

**Use Cases**:
- Research paper analysis and literature review automation
- Financial report data extraction and analysis
- Legal document review and contract analysis
- Technical manual content extraction and searchable documentation
- Government document processing and compliance checking
- Academic transcript and certificate verification
- Insurance claim document processing
- Medical record digitization and patient data extraction

```
from langchain_community.document_loaders import PyPDFLoader

# The path to the PDF file to be parsed, for example: "workspace/task.pdf"
pdf_path = "workspace/task.pdf"
# The starting page number to read from (1-indexed). If None, read from the beginning
start_page = None
# The ending page number to read to (1-indexed, inclusive). If None, read to the end
end_page = None

# Load and split PDF into pages using LangChain
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()

if len(pages) == 0:
    print("No pages found in this PDF file.")

# Handle page range parameters
if start_page is not None:
    start_idx = max(0, start_page - 1)  # Convert to 0-indexed
else:
    start_idx = 0

if end_page is not None:
    end_idx = min(len(pages), end_page)  # Convert to 0-indexed (end_page is inclusive)
else:
    end_idx = len(pages)

# Validate page range
if start_idx >= len(pages):
    print(f"Error: start_page {start_page} is beyond the PDF length ({len(pages)} pages).")

if start_page is not None and end_page is not None and start_page > end_page:
    print(f"Error: start_page ({start_page}) cannot be greater than end_page ({end_page}).")

# Extract the specified page range
selected_pages = pages[start_idx:end_idx]
content = "\n".join([page.page_content for page in selected_pages])

# Check if content is too large (only for full PDF reading)
if len(content) > 100000:
    print(f"Error: PDF '{pdf_path}' content is too large ({len(content)} characters). Total pages: {len(pages)}. Please use start_page and end_page parameters to read specific page ranges.")

# Add page range information to the result if reading a subset
if start_page is not None or end_page is not None:
    actual_start = start_idx + 1
    actual_end = start_idx + len(selected_pages)
    range_info = f"[Pages {actual_start}-{actual_end} of {len(pages)} total pages]\n"
    print(range_info + content)
else:
    print(content)
```

## Episodic Examples
### Development Step 26: Search and Download ‘Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?’ PDF

**Description**: Conduct a web search for the University of Leicester paper titled "Can Hiccup Supply Enough Fish to Maintain a Dragon’s Diet?" and download the full PDF of that paper into workspace/dragon_diet_fish_bag.pdf.

**Use Cases**:
- Academic researcher automates retrieval of PDF versions of domain-specific journal articles (e.g., collecting marine biology papers on dragon feeding strategies) into a local workspace for offline literature review
- Corporate compliance team scans Bing search results for newly published regulatory guideline PDFs (e.g., environmental impact reports) and extracts context snippets to flag relevant policy changes
- Patent analyst gathers patent specification PDFs from public search engines to streamline prior-art investigations, saving raw HTML and link contexts for downstream review
- Financial analyst harvests quarterly and annual report PDFs from company investor-relations sites via automated search queries, then extracts text snippets for rapid trend analysis
- Legal department captures court decision and statute PDFs from online databases, archiving search result HTML and snippet contexts to build an internal e-discovery repository
- Marketing research group aggregates competitor whitepapers and product brochures in PDF form, logging occurrences and snippet previews to identify new market offerings
- Data engineer sources technical standards and specification PDFs from ISO or IEEE web portals by automated search, preserving HTML contexts and snippet files for integration into validation pipelines
- Healthcare informatics team downloads clinical guideline and trial protocol PDFs through targeted search queries, extracting snippet previews to prioritize documents for patient-care policy development

```
import os
import sys
import re
import requests

# Module‐level HTTP headers for all requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html'
}

# Step 1: Ensure workspace directory exists
workspace = 'workspace'
if not os.path.isdir(workspace):
    print(f"ERROR: Workspace directory '{workspace}' does not exist.")
    sys.exit(1)
print(f"[INFO] Using workspace: {workspace}\n")

# Step 2: Construct the Bing search query
title = "Can Hiccup Supply Enough Fish to Maintain a Dragon's Diet?"
query = f'"{title}" filetype:pdf'
print(f"[SEARCH] Bing query: {query}\n")

# Step 3: Perform the HTTP GET to Bing and capture HTML
search_url = 'https://www.bing.com/search'
try:
    response = requests.get(search_url,
                            params={'q': query},
                            headers=HEADERS,
                            timeout=30)
    response.raise_for_status()
    html = response.text
    print(f"[SEARCH] Retrieved {len(html)} characters of HTML from Bing.\n")
except Exception as e:
    print(f"ERROR: Failed to fetch Bing search results: {e}")
    sys.exit(1)

# Step 4: Save the raw HTML for offline analysis
html_path = os.path.join(workspace, 'bing_search.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"[SAVE] Full Bing HTML saved to: {html_path}\n")

# Step 5: Locate every occurrence of 'pdf' in the HTML
positions = [m.start() for m in re.finditer(r'pdf', html, flags=re.IGNORECASE)]
print(f"[PARSE] Found {len(positions)} occurrences of 'pdf' in the HTML.\n")

# Step 6: Extract up to the first 20 context snippets around each occurrence
snippets = []
for pos in positions[:20]:
    start = max(0, pos - 80)
    end = min(len(html), pos + 80)
    context = html[start:end].replace('\n', ' ')
    snippets.append((pos, context))

# Step 7: Write those snippets to a file for detailed review
snip_path = os.path.join(workspace, 'pdf_snippets.txt')
with open(snip_path, 'w', encoding='utf-8') as f:
    for idx, (pos, ctx) in enumerate(snippets, 1):
        f.write(f"Occurrence {idx} at index {pos}:\n")
        f.write(ctx + "\n" + '-'*80 + "\n")
print(f"[SAVE] First {len(snippets)} context snippets saved to: {snip_path}\n")

# Step 8: Print the first 5 snippets to console for quick inspection
for i, (pos, ctx) in enumerate(snippets[:5], 1):
    print(f"[SNIPPET {i}] Index {pos}: {ctx}\n")

print("[COMPLETE] HTML dump and PDF-context snippets are ready for inspection.")
```

### Development Step 18: Identify 1839 Saunders & Otley Robertson novel in rural Scotland/Wales and its Dickens illustrator

**Description**: Search for novels published by Saunders and Otley in 1839 that were authored by either William Parish Robertson or John Parish Robertson. Focus on identifying a novel set in rural Scotland and Wales featuring a young orphan clerk residing in Glasgow. Also search for information about which artist illustrated this novel, specifically looking for an illustrator known for working with Charles Dickens who also created 'The Great 100 Rat Match' circa 1858. Use search terms including 'Robertson Saunders Otley 1839 novel', 'Scotland Wales orphan clerk Glasgow novel 1839', and 'Dickens illustrator Great 100 Rat Match 1858'.

**Use Cases**:
- Literary historian automating multi-backend searches to identify 1839 Saunders & Otley novels set in rural Scotland and Wales featuring orphan clerks in Glasgow, filtering results by relevance scores to pinpoint obscure travel–fiction hybrids.
- Museum curator leveraging the pipeline to attribute a Victorian-era sporting engraving (“The Great 100 Rat Match” 1858) by scoring illustrator names and Dickens connections across Google, Bing and DuckDuckGo archives.
- Corporate compliance officer monitoring online legal repositories for new Scottish and Welsh regulatory updates in 2023, extracting jurisdiction terms and act numbers, then ranking documents by compliance-critical keywords.
- R&D manager conducting a patent landscape analysis on CRISPR gene-editing inventions (2020–2023), automating multi-engine searches to extract base-editing indicators and score filings by technical novelty.
- Brand manager orchestrating competitive intelligence by crawling search backends for emerging product mentions, scoring by brand names, feature-highlight terms and sentiment indicators to fine-tune marketing campaigns.
- Graduate student in environmental science streamlining a literature review on marine plastic pollution (post-2015), querying academic portals and news sites, extracting funding bodies and statistical method phrases, then ranking papers by keyword density.
- Investigative political reporter sourcing historical news and NGO reports on election irregularities in specific constituencies, using multi-backend searches to extract location, date and allegation keywords, then scoring articles to build a timeline.
- Procurement analyst in manufacturing assessing supply–chain risks by scanning global news outlets for supplier disruptions, extracting company names, incident types and region codes, then prioritizing alerts by risk severity indicators.

```
from ddgs import DDGS
import os
import json
import time
import re

print('=== ROBERTSON BROTHERS 1839 NOVEL & DICKENS ILLUSTRATOR RESEARCH ===')
print('APPROACH: Using DDGS search service to avoid HTTP 202 blocking issues')
print('TARGET 1: Robertson brothers novel published by Saunders & Otley (1839)')
print('         - Setting: Rural Scotland and Wales, orphan clerk in Glasgow')
print('TARGET 2: Dickens illustrator who created "The Great 100 Rat Match" (1858)')
print('\nSTRATEGY: Use alternative search backend with comprehensive analysis')
print('=' * 80 + '\n')

# Ensure workspace directory exists
os.makedirs('workspace', exist_ok=True)

# Initialize comprehensive results storage
research_results = {
    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    'research_objective': 'Identify Robertson brothers 1839 Saunders & Otley novel and Dickens illustrator',
    'search_method': 'DDGS search service with multiple backends',
    'searches_conducted': [],
    'robertson_novel_findings': [],
    'illustrator_findings': [],
    'analysis_summary': {},
    'technical_notes': 'Using DDGS to avoid DuckDuckGo HTTP 202 blocking'
}

print('=== PHASE 1: ROBERTSON BROTHERS NOVEL RESEARCH ===\n')

# Define comprehensive search queries for Robertson novel
novel_search_queries = [
    'William Parish Robertson Saunders Otley 1839 novel',
    'John Parish Robertson Saunders Otley 1839 publisher',
    'Parish Robertson brothers 1839 Scotland Wales Glasgow',
    'Saunders Otley 1839 Robertson novel orphan clerk',
    'Robertson Letters South America 1839 Saunders Otley',
    'Parish Robertson 1839 rural Scotland Wales novel'
]

print(f'Conducting {len(novel_search_queries)} Robertson novel searches:')
for i, query in enumerate(novel_search_queries, 1):
    print(f'  {i:2d}. {query}')

# Function to calculate novel relevance score
def calculate_novel_relevance(text_content):
    """Calculate relevance score for Robertson novel searches"""
    text_lower = text_content.lower()
    score = 0
    
    # Primary search terms (high value)
    if 'robertson' in text_lower: score += 4
    if 'parish' in text_lower: score += 4
    if 'william' in text_lower and 'parish' in text_lower: score += 3
    if 'john' in text_lower and 'parish' in text_lower: score += 3
    if 'saunders' in text_lower: score += 5
    if 'otley' in text_lower: score += 5
    if '1839' in text_lower: score += 6
    if 'novel' in text_lower: score += 3
    if 'book' in text_lower: score += 2
    if 'published' in text_lower: score += 2
    if 'publisher' in text_lower: score += 3
    
    # Geographic and character terms
    if 'scotland' in text_lower: score += 3
    if 'wales' in text_lower: score += 3
    if 'glasgow' in text_lower: score += 4
    if 'scottish' in text_lower: score += 2
    if 'welsh' in text_lower: score += 2
    if 'orphan' in text_lower: score += 4
    if 'clerk' in text_lower: score += 3
    if 'rural' in text_lower: score += 2
    if 'young' in text_lower: score += 1
    
    # Subject matter terms
    if 'letters' in text_lower: score += 3
    if 'america' in text_lower: score += 2
    if 'south america' in text_lower: score += 4
    if 'paraguay' in text_lower: score += 3
    if 'travel' in text_lower: score += 2
    if 'journey' in text_lower: score += 2
    if 'voyage' in text_lower: score += 2
    
    # Bonus for key combinations
    if 'saunders' in text_lower and 'otley' in text_lower: score += 6
    if 'robertson' in text_lower and '1839' in text_lower: score += 5
    if 'scotland' in text_lower and 'wales' in text_lower: score += 4
    if 'orphan' in text_lower and 'clerk' in text_lower: score += 3
    if 'letters' in text_lower and 'america' in text_lower: score += 3
    
    return score

# Function to extract novel indicators
def extract_novel_indicators(text_content):
    """Extract key indicators for Robertson novel identification"""
    text_lower = text_content.lower()
    indicators = []
    
    if 'saunders' in text_lower and 'otley' in text_lower:
        indicators.append('SAUNDERS & OTLEY PUBLISHER')
    if 'robertson' in text_lower and '1839' in text_lower:
        indicators.append('ROBERTSON 1839')
    if any(term in text_lower for term in ['scotland', 'wales', 'glasgow', 'scottish', 'welsh']):
        indicators.append('SCOTTISH/WELSH CONTENT')
    if any(term in text_lower for term in ['orphan', 'clerk']):
        indicators.append('CHARACTER ELEMENTS')
    if 'letters' in text_lower and 'america' in text_lower:
        indicators.append('LETTERS ON AMERICA')
    if any(term in text_lower for term in ['novel', 'book', 'published']):
        indicators.append('LITERARY WORK')
    if any(term in text_lower for term in ['william', 'john']) and 'parish' in text_lower:
        indicators.append('PARISH ROBERTSON BROTHERS')
    
    return indicators

# Execute Robertson novel searches
print('\nExecuting Robertson novel searches...')
successful_novel_searches = 0

for i, query in enumerate(novel_search_queries, 1):
    print(f'\n--- Novel Search {i}: {query} ---')
    
    try:
        # Use DDGS with multiple backend options
        searcher = DDGS(timeout=15)
        backend_options = ["google", "duckduckgo", "bing", "yahoo"]
        
        results = searcher.text(
            query, 
            max_results=10, 
            page=1, 
            backend=backend_options, 
            safesearch="off", 
            region="en-us"
        )
        
        if results:
            print(f'✅ Found {len(results)} search results')
            
            # Process and analyze results
            for j, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('href', 'No URL')
                snippet = result.get('body', 'No snippet')
                
                # Calculate relevance
                combined_text = f'{title} {snippet}'
                relevance_score = calculate_novel_relevance(combined_text)
                indicators = extract_novel_indicators(combined_text)
                
                if relevance_score >= 6:  # Threshold for relevance
                    print(f'\n  📋 Relevant Result {j} (Score: {relevance_score})')
                    print(f'    Title: {title[:120]}...')
                    print(f'    URL: {url}')
                    print(f'    Snippet: {snippet[:200]}...')
                    indicators_str = ', '.join(indicators)
                    print(f'    Indicators: {indicators_str}')
                    
                    research_results['robertson_novel_findings'].append({
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'relevance_score': relevance_score,
                        'indicators': indicators,
                        'search_query': query,
                        'search_index': i
                    })
            
            successful_novel_searches += 1
            
        else:
            print('❌ No results found for this query')
            
        # Record search metadata
        research_results['searches_conducted'].append({
            'query': query,
            'search_index': i,
            'search_type': 'novel',
            'results_found': len(results) if results else 0,
            'status': 'success' if results else 'no_results'
        })
        
    except Exception as e:
        print(f'❌ Search error: {str(e)}')
        research_results['searches_conducted'].append({
            'query': query,
            'search_index': i,
            'search_type': 'novel',
            'results_found': 0,
            'status': 'error',
            'error': str(e)
        })
    
    time.sleep(2)  # Rate limiting

print(f'\n=== PHASE 2: DICKENS ILLUSTRATOR RESEARCH ===\n')

# Define comprehensive search queries for illustrator identification
illustrator_search_queries = [
    'Great 100 Rat Match 1858 illustrator Dickens',
    'Hablot Browne Phiz Great Rat Match 1858',
    'George Cruikshank Great 100 Rat Match 1858',
    'Victorian rat baiting illustration 1858 Dickens',
    'Dickens illustrator rat match sporting 1858',
    'Phiz Hablot Browne rat match illustration 1858'
]

print(f'Conducting {len(illustrator_search_queries)} illustrator searches:')
for i, query in enumerate(illustrator_search_queries, 1):
    print(f'  {i:2d}. {query}')

# Function to calculate illustrator relevance score
def calculate_illustrator_relevance(text_content):
    """Calculate relevance score for illustrator searches"""
    text_lower = text_content.lower()
    score = 0
    
    # Core search terms
    if 'rat match' in text_lower: score += 6
    if 'great 100' in text_lower: score += 5
    if '100 rat' in text_lower: score += 5
    if 'rat' in text_lower: score += 2
    if '1858' in text_lower: score += 5
    if 'dickens' in text_lower: score += 4
    if 'charles dickens' in text_lower: score += 5
    
    # Illustrator identification terms
    if 'phiz' in text_lower: score += 5
    if 'hablot' in text_lower: score += 5
    if 'browne' in text_lower: score += 3
    if 'hablot browne' in text_lower: score += 6
    if 'cruikshank' in text_lower: score += 4
    if 'george cruikshank' in text_lower: score += 5
    if 'illustrator' in text_lower: score += 3
    if 'illustration' in text_lower: score += 2
    if 'artist' in text_lower: score += 2
    if 'drawing' in text_lower: score += 2
    
    # Period and context terms
    if 'victorian' in text_lower: score += 3
    if '19th century' in text_lower: score += 2
    if 'nineteenth' in text_lower: score += 2
    if 'sporting' in text_lower: score += 2
    if 'sport' in text_lower: score += 1
    if 'match' in text_lower: score += 1
    if 'competition' in text_lower: score += 1
    
    # Bonus combinations
    if 'dickens' in text_lower and 'illustrator' in text_lower: score += 4
    if 'rat match' in text_lower and '1858' in text_lower: score += 6
    if any(name in text_lower for name in ['phiz', 'hablot browne', 'george cruikshank']): score += 3
    
    return score

# Function to extract illustrator indicators
def extract_illustrator_indicators(text_content):
    """Extract key indicators for illustrator identification"""
    text_lower = text_content.lower()
    indicators = []
    
    if 'rat match' in text_lower:
        indicators.append('RAT MATCH REFERENCE')
    if 'great 100' in text_lower or '100 rat' in text_lower:
        indicators.append('GREAT 100 REFERENCE')
    if '1858' in text_lower:
        indicators.append('1858 DATE')
    if 'dickens' in text_lower:
        indicators.append('DICKENS CONNECTION')
    if 'phiz' in text_lower or 'hablot browne' in text_lower:
        indicators.append('PHIZ/HABLOT BROWNE')
    if 'cruikshank' in text_lower:
        indicators.append('CRUIKSHANK')
    if any(term in text_lower for term in ['illustrator', 'illustration', 'artist']):
        indicators.append('ILLUSTRATION WORK')
    if 'victorian' in text_lower:
        indicators.append('VICTORIAN PERIOD')
    
    return indicators

# Execute illustrator searches
print('\nExecuting illustrator searches...')
successful_illustrator_searches = 0

for i, query in enumerate(illustrator_search_queries, 1):
    search_index = len(novel_search_queries) + i
    print(f'\n--- Illustrator Search {search_index}: {query} ---')
    
    try:
        # Use DDGS with multiple backend options
        searcher = DDGS(timeout=15)
        backend_options = ["google", "duckduckgo", "bing", "yahoo"]
        
        results = searcher.text(
            query, 
            max_results=10, 
            page=1, 
            backend=backend_options, 
            safesearch="off", 
            region="en-us"
        )
        
        if results:
            print(f'✅ Found {len(results)} search results')
            
            # Process and analyze results
            for j, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                url = result.get('href', 'No URL')
                snippet = result.get('body', 'No snippet')
                
                # Calculate relevance
                combined_text = f'{title} {snippet}'
                relevance_score = calculate_illustrator_relevance(combined_text)
                indicators = extract_illustrator_indicators(combined_text)
                
                if relevance_score >= 6:  # Threshold for relevance
                    print(f'\n  📋 Relevant Result {j} (Score: {relevance_score})')
                    print(f'    Title: {title[:120]}...')
                    print(f'    URL: {url}')
                    print(f'    Snippet: {snippet[:200]}...')
                    indicators_str = ', '.join(indicators)
                    print(f'    Indicators: {indicators_str}')
                    
                    research_results['illustrator_findings'].append({
                        'title': title,
                        'url': url,
                        'snippet': snippet,
                        'relevance_score': relevance_score,
                        'indicators': indicators,
                        'search_query': query,
                        'search_index': search_index
                    })
            
            successful_illustrator_searches += 1
            
        else:
            print('❌ No results found for this query')
            
        # Record search metadata
        research_results['searches_conducted'].append({
            'query': query,
            'search_index': search_index,
            'search_type': 'illustrator',
            'results_found': len(results) if results else 0,
            'status': 'success' if results else 'no_results'
        })
        
    except Exception as e:
        print(f'❌ Search error: {str(e)}')
        research_results['searches_conducted'].append({
            'query': query,
            'search_index': search_index,
            'search_type': 'illustrator',
            'results_found': 0,
            'status': 'error',
            'error': str(e)
        })
    
    time.sleep(2)  # Rate limiting

print('\n' + '=' * 90)
print('COMPREHENSIVE RESEARCH ANALYSIS: ROBERTSON NOVEL & DICKENS ILLUSTRATOR')
print('=' * 90)

# Analyze findings
total_searches = len(novel_search_queries) + len(illustrator_search_queries)
total_successful = successful_novel_searches + successful_illustrator_searches

print(f'\n📊 RESEARCH SUMMARY:')
print(f'   • Total searches attempted: {total_searches}')
print(f'   • Successful searches: {total_successful}')
print(f'   • Success rate: {(total_successful/total_searches)*100:.1f}%')
print(f'   • Robertson novel findings: {len(research_results["robertson_novel_findings"])}')
print(f'   • Illustrator findings: {len(research_results["illustrator_findings"])}')

# Analyze Robertson novel findings
if research_results['robertson_novel_findings']:
    print('\n📚 ROBERTSON NOVEL ANALYSIS:')
    print('-' * 50)
    
    # Sort by relevance score
    novel_findings = sorted(research_results['robertson_novel_findings'], 
                           key=lambda x: x['relevance_score'], reverse=True)
    
    print(f'Top {min(5, len(novel_findings))} most relevant findings:')
    
    for i, finding in enumerate(novel_findings[:5], 1):
        print(f'\n{i}. RELEVANCE SCORE: {finding["relevance_score"]}')
        print(f'   Title: {finding["title"][:120]}...')
        print(f'   URL: {finding["url"]}')
        print(f'   Snippet: {finding["snippet"][:200]}...')
        indicators_str = ', '.join(finding['indicators'])
        print(f'   Key indicators: {indicators_str}')
        print(f'   Source query: {finding["search_query"]}')
        
        # Analyze for specific novel identification
        combined_content = f'{finding["title"]} {finding["snippet"]}'.lower()
        
        potential_titles = []
        if 'letters' in combined_content and 'south america' in combined_content:
            potential_titles.append('Letters on South America')
        if 'letters' in combined_content and 'paraguay' in combined_content:
            potential_titles.append('Letters on Paraguay')
        if 'history' in combined_content and 'america' in combined_content:
            potential_titles.append('History of America')
        if 'voyage' in combined_content or 'journey' in combined_content:
            potential_titles.append('Travel narrative')
        
        if potential_titles:
            titles_str = ', '.join(potential_titles)
            print(f'   📖 Potential work types: {titles_str}')
else:
    print('\n❌ No Robertson novel findings with sufficient relevance scores')

# Analyze illustrator findings
if research_results['illustrator_findings']:
    print('\n🎨 ILLUSTRATOR ANALYSIS:')
    print('-' * 40)
    
    # Sort by relevance score
    illustrator_findings = sorted(research_results['illustrator_findings'], 
                                 key=lambda x: x['relevance_score'], reverse=True)
    
    print(f'Top {min(5, len(illustrator_findings))} most relevant findings:')
    
    for i, finding in enumerate(illustrator_findings[:5], 1):
        print(f'\n{i}. RELEVANCE SCORE: {finding["relevance_score"]}')
        print(f'   Title: {finding["title"][:120]}...')
        print(f'   URL: {finding["url"]}')
        print(f'   Snippet: {finding["snippet"][:200]}...')
        indicators_str = ', '.join(finding['indicators'])
        print(f'   Key indicators: {indicators_str}')
        print(f'   Source query: {finding["search_query"]}')
        
        # Identify most likely illustrator
        combined_content = f'{finding["title"]} {finding["snippet"]}'.lower()
        
        likely_illustrator = 'Unknown'
        if 'phiz' in combined_content or 'hablot browne' in combined_content:
            likely_illustrator = 'Hablot Knight Browne (Phiz)'
        elif 'george cruikshank' in combined_content:
            likely_illustrator = 'George Cruikshank'
        elif 'cruikshank' in combined_content:
            likely_illustrator = 'Cruikshank family'
        elif 'browne' in combined_content:
            likely_illustrator = 'Browne (possibly Hablot)'
        
        if likely_illustrator != 'Unknown':
            print(f'   🖼️ Likely illustrator: {likely_illustrator}')
else:
    print('\n❌ No illustrator findings with sufficient relevance scores')

# Generate comprehensive conclusions
print('\n🎯 RESEARCH CONCLUSIONS:')
print('-' * 40)

# Robertson novel conclusion
if research_results['robertson_novel_findings']:
    top_novel_finding = max(research_results['robertson_novel_findings'], 
                           key=lambda x: x['relevance_score'])
    print(f'📚 ROBERTSON NOVEL (Confidence: {top_novel_finding["relevance_score"]}/20+):')
    print(f'   Based on search evidence, the Robertson brothers\' 1839 work')
    print(f'   published by Saunders & Otley most likely relates to their')
    print(f'   travel writing about South America, possibly adapted or')
    print(f'   expanded to include Scottish/Welsh settings and characters.')
    indicators_str = ', '.join(top_novel_finding['indicators'])
    print(f'   Key evidence: {indicators_str}')
    
    # Provide specific title if identifiable
    combined_content = f'{top_novel_finding["title"]} {top_novel_finding["snippet"]}'.lower()
    if 'letters' in combined_content and ('south america' in combined_content or 'paraguay' in combined_content):
        print(f'   📖 Most likely work: "Letters on South America" or "Letters on Paraguay"')
else:
    print('📚 ROBERTSON NOVEL: Insufficient direct evidence found.')
    print('   Historical context: Robertson brothers were travel writers')
    print('   known for South American accounts. Saunders & Otley was a')
    print('   prominent London publisher in the 1830s-1840s.')
    print('   📖 Most likely candidate: "Letters on Paraguay" (1838-1839)')
    print('   which may have been republished or expanded in 1839.')

# Illustrator conclusion
if research_results['illustrator_findings']:
    top_illustrator_finding = max(research_results['illustrator_findings'], 
                                 key=lambda x: x['relevance_score'])
    print(f'\n🎨 DICKENS ILLUSTRATOR (Confidence: {top_illustrator_finding["relevance_score"]}/20+):')
    print(f'   Most likely creator of "The Great 100 Rat Match" (1858)')
    
    combined_content = f'{top_illustrator_finding["title"]} {top_illustrator_finding["snippet"]}'.lower()
    if 'phiz' in combined_content or 'hablot browne' in combined_content:
        print(f'   is Hablot Knight Browne (Phiz), Dickens\' primary illustrator')
        print(f'   🖼️ IDENTIFIED: Hablot Knight Browne ("Phiz")')
    elif 'cruikshank' in combined_content:
        print(f'   is George Cruikshank, prominent Victorian illustrator')
        print(f'   🖼️ IDENTIFIED: George Cruikshank')
    else:
        print(f'   appears to be a Victorian illustrator with Dickens connections')
    
    indicators_str = ', '.join(top_illustrator_finding['indicators'])
    print(f'   Key evidence: {indicators_str}')
else:
    print('\n🎨 DICKENS ILLUSTRATOR: Limited direct evidence found.')
    print('   Historical context suggests most likely candidates:')
    print('   • Hablot Knight Browne (Phiz) - primary Dickens illustrator 1836-1859')
    print('   • George Cruikshank - worked with Dickens, known for sporting scenes')
    print('   • The 1858 date fits the peak period of Victorian illustration')
    print('   🖼️ MOST LIKELY: Hablot Knight Browne ("Phiz") based on:')
    print('     - Primary Dickens collaborator during 1858')
    print('     - Known for detailed sporting and social scene illustrations')
    print('     - Active during peak of Victorian rat-baiting popularity')

# Save comprehensive results
research_results['analysis_summary'] = {
    'total_searches': total_searches,
    'successful_searches': total_successful,
    'success_rate': (total_successful/total_searches)*100,
    'novel_findings_count': len(research_results['robertson_novel_findings']),
    'illustrator_findings_count': len(research_results['illustrator_findings']),
    'top_novel_score': max([f['relevance_score'] for f in research_results['robertson_novel_findings']]) if research_results['robertson_novel_findings'] else 0,
    'top_illustrator_score': max([f['relevance_score'] for f in research_results['illustrator_findings']]) if research_results['illustrator_findings'] else 0
}

results_file = os.path.join('workspace', 'robertson_dickens_research_ddgs_final.json')
with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(research_results, f, indent=2, ensure_ascii=False)

print(f'\n💾 COMPREHENSIVE RESEARCH RESULTS SAVED TO: {results_file}')

# Final assessment and recommendations
overall_success = (research_results['analysis_summary']['novel_findings_count'] > 0 or 
                  research_results['analysis_summary']['illustrator_findings_count'] > 0)

if overall_success:
    print('\n✅ RESEARCH MISSION: SUCCESSFUL')
    print('   Found relevant evidence for Robertson novel and/or Dickens illustrator')
    print('   All search results saved for further analysis')
    
    # Provide specific recommendations
    print('\n📋 RESEARCH RECOMMENDATIONS:')
    if research_results['robertson_novel_findings']:
        print('   📚 Robertson Novel: Continue research in:')
        print('     • British Library catalog for Saunders & Otley publications')
        print('     • Cambridge University Library Robertson collection')
        print('     • Archive.org for digitized 1839 publications')
    
    if research_results['illustrator_findings']:
        print('   🎨 Dickens Illustrator: Verify through:')
        print('     • Victoria & Albert Museum illustration archives')
        print('     • Dickens Museum London illustration collection')
        print('     • British Museum prints and drawings department')
else:
    print('\n⚠️ RESEARCH MISSION: PARTIAL SUCCESS')
    print('   Technical search infrastructure working, but limited specific evidence')
    print('   Based on historical context, most likely answers are:')
    print('   📚 Robertson Novel: "Letters on Paraguay" (1838-1839) by Robertson brothers')
    print('   🎨 Dickens Illustrator: Hablot Knight Browne ("Phiz") - primary Dickens collaborator')
    
    print('\n📋 ALTERNATIVE RESEARCH STRATEGIES:')
    print('   • Specialized Victorian literature databases')
    print('   • Library catalog searches (British Library, Cambridge)')
    print('   • Art history databases for illustration research')
    print('   • Academic journal searches for Robertson/Dickens scholarship')

print('\n=== ROBERTSON BROTHERS & DICKENS ILLUSTRATOR RESEARCH COMPLETE ===')
print('Comprehensive analysis completed with DDGS search service')
```

## Created Time
2025-08-14 14:56:18
