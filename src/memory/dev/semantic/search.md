### How to Search for Academic Papers Using ArXiv?

Search for academic papers and research publications using the ArXiv database. Uses the LangChain community library for ArXiv API integration.

```python
from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper

# The search query to perform, for example: "attention is all you need" or "1605.08386" for specific ArXiv ID
query = "attention is all you need"
# The maximum number of results to return (default: 3)
max_results = 3

# Initialize ArXiv API wrapper with maximum results setting
arxiv = ArxivAPIWrapper(max_results=max_results)
search = ArxivQueryRun(api_wrapper=arxiv)

# Execute the search query and get results
results = search.invoke(query)

print(results)
```

### How to Search for Information Using DuckDuckGo?

Search for general information using the DuckDuckGo search engine. Uses the ddgs library for direct API integration.

```python
from ddgs import DDGS

# The search query to perform, for example: "machine learning tutorial"
query = "machine learning tutorial"
# The maximum number of results to return (default: 3)
max_results = 3
# The region to search in (default: "wt-wt" for worldwide)
region = "wt-wt"
# The time frame for search results: "d" (day), "w" (week), "m" (month), "y" (year)
time = "d"
# The source to search in: "text" for web results, "images" for images, "news" for news (default: "text")
source = "text"

# Initialize DDGS and perform search
with DDGS() as ddgs:
    if source == "text":
        # Text search with time and region filters
        results = list(ddgs.text(
            query, 
            max_results=max_results, 
            region=region,
            timelimit=time
        ))
        
        # Format results for consistency
        formatted_results = []
        for result in results:
            formatted_results.append({
                'title': result.get('title', 'N/A'),
                'link': result.get('href', 'N/A'),
                'snippet': result.get('body', 'N/A')
            })
        
        print(formatted_results)
        
    elif source == "images":
        # Image search
        results = list(ddgs.images(
            query, 
            max_results=max_results, 
            region=region,
            timelimit=time
        ))
        
        print(results)
        
    elif source == "news":
        # News search
        results = list(ddgs.news(
            query, 
            max_results=max_results, 
            region=region,
            timelimit=time
        ))
        
        print(results)
        
    else:
        print(f"Error: Invalid source '{source}'. Must be one of: text, images, news")
```

### How to Search for Information Using Google Search?

Search for information using Google search engine with advanced operators and filters. Requires SerpAPI key for accessing Google Search API.

```python
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

### How to Search Wikipedia for Information?

Search Wikipedia for encyclopedic information and return detailed article content. Uses the LangChain community library for Wikipedia API integration.

```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# The search query to perform, for example: "artificial intelligence", "protein structure", etc.
query = "artificial intelligence"
# The maximum number of results to return (default: 3)
max_results = 3
# The maximum number of characters to return for each document (default: 4000)
doc_content_chars_max = 4000

# Initialize Wikipedia API wrapper with result limits
api_wrapper = WikipediaAPIWrapper(
    top_k_results=max_results, 
    doc_content_chars_max=doc_content_chars_max
)

# Create Wikipedia search tool and execute the query
search_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
results = search_tool.invoke({"query": query})

print(results)
```
