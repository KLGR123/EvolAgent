### How to Access and Manage GitHub Repositories Using MCP Integration

**Description**: Connect to and interact with GitHub repositories and services through the Model Context Protocol (MCP) GitHub server. This comprehensive integration enables automated repository management, issue tracking, pull request operations, code search functionality, and comprehensive GitHub API interactions through a standardized protocol interface. MCP provides seamless access to version control operations, repository analytics, and collaborative development workflows without requiring direct API implementation.

**Use Cases**:
- Search and discover repositories based on specific programming languages, topics, or popularity metrics
- Automate issue creation, assignment, and tracking for project management and bug reporting workflows
- Monitor repository activity, commits, and collaboration patterns for development analytics
- Extract repository metadata, statistics, and contributor information for research and analysis
- Manage pull requests, code reviews, and merge operations programmatically
- Access repository contents, file structures, and commit histories for code analysis projects
- Implement automated workflows for continuous integration and deployment processes
- Track project dependencies, security vulnerabilities, and licensing compliance across repositories
- Generate reports on development progress, team productivity, and code quality metrics
- Integrate GitHub data with external tools for comprehensive project management and analytics

```
import asyncio
import json
import os
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from dotenv import load_dotenv

load_dotenv()

# Set up GitHub MCP connection with authentication
github_token = os.getenv("GITHUB_API_TOKEN")
gh_transport = StdioTransport(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_API_TOKEN": github_token}
)

async def main():
    async with Client(gh_transport) as client:
        print("🔍 Starting GitHub repository analysis...")
        
        # Get available GitHub MCP tools
        tools = await client.list_tools()
        print(f"🔗 Connected to GitHub MCP. Available tools: {[tool.name for tool in tools]}")
        
        # Search for trending Python machine learning repositories
        ml_search = await client.call_tool(
            "search_repositories",
            arguments={
                "query": "machine learning language:python stars:>1000",
                "sort": "stars",
                "per_page": 5
            }
        )
        
        print(f"📊 Found repositories matching ML criteria")
        print(f"🔍 Search result type: {type(ml_search.content)}")
        
        # Process search results - GitHub MCP returns list with TextContent
        repositories = []
        if isinstance(ml_search.content, list) and len(ml_search.content) > 0:
            # Extract JSON from the first TextContent object
            first_item = ml_search.content[0]
            if hasattr(first_item, 'text'):
                try:
                    # Parse the JSON string from TextContent
                    search_data = json.loads(first_item.text)
                    repositories = search_data.get('items', [])[:3]
                    print(f"📊 Successfully parsed {len(repositories)} repositories from search results")
                except Exception as e:
                    print(f"⚠️ JSON parsing failed: {str(e)[:50]}...")
                    repositories = []
            else:
                print("⚠️ First item doesn't have text attribute")
        else:
            print("⚠️ No search results or unexpected format")
        
        print(f"📈 Analyzing top {len(repositories)} ML repositories:")
        
        repo_analysis = []
        for i, repo_data in enumerate(repositories):
            # Now repo_data should be actual repository dictionary
            repo_name = repo_data.get('full_name', f'Unknown Repository {i+1}')
            owner = repo_data.get('owner', {}).get('login', 'unknown')
            name = repo_data.get('name', 'unknown')
            
            print(f"\n🔬 {i+1}. Analyzing: {repo_name}")
            
            # Extract available information from search results and try to get additional details
            if owner != "unknown" and name != "unknown":
                # Search results provide limited info, let's extract what's available
                description = repo_data.get('description', 'N/A')
                updated_at = repo_data.get('updated_at', 'N/A')
                created_at = repo_data.get('created_at', 'N/A')
                default_branch = repo_data.get('default_branch', 'main')
                
                # Try to get README file to extract more information
                try:
                    readme_content = await client.call_tool(
                        "get_file_contents",
                        arguments={
                            "owner": owner,
                            "repo": name,
                            "path": "README.md"
                        }
                    )
                    
                    # Extract README length as a proxy for project maturity
                    if hasattr(readme_content.content, 'text'):
                        readme_text = readme_content.content.text
                        readme_length = len(readme_text)
                        has_readme = "Yes"
                    else:
                        readme_length = len(str(readme_content.content)) if readme_content.content else 0
                        has_readme = "Yes" if readme_length > 0 else "No"
                    
                    print(f"   📄 README: {has_readme} ({readme_length} chars)")
                    
                except Exception as e:
                    has_readme = "No"
                    readme_length = 0
                    print(f"   📄 README: {has_readme}")
                
                print(f"   🏗️ Created: {created_at}")
                print(f"   📅 Updated: {updated_at}")
                print(f"   🌿 Branch: {default_branch}")
                print(f"   📝 Description: {description[:100]}..." if len(str(description)) > 100 else f"   📝 Description: {description}")
                
                repo_analysis.append({
                    'name': repo_name,
                    'readme': has_readme,
                    'readme_size': readme_length,
                    'created': created_at,
                    'updated': updated_at,
                    'branch': default_branch,
                    'description': description
                })
            else:
                print(f"   ⚠️ Invalid repository data structure")
                repo_analysis.append({
                    'name': repo_name,
                    'readme': 'N/A',
                    'readme_size': 0,
                    'created': 'N/A',
                    'updated': 'N/A',
                    'branch': 'N/A',
                    'description': 'N/A'
                })
        
        # Search for additional repositories to expand our analysis
        print(f"\n🤖 Searching for additional machine learning frameworks...")
        
        try:
            # Search for popular ML frameworks instead of code
            framework_search = await client.call_tool(
                "search_repositories",
                arguments={
                    "query": "deep learning pytorch tensorflow language:python",
                    "sort": "stars",
                    "per_page": 5
                }
            )
            
            # Process framework search results 
            if isinstance(framework_search.content, list) and len(framework_search.content) > 0:
                first_item = framework_search.content[0]
                if hasattr(first_item, 'text'):
                    try:
                        framework_data = json.loads(first_item.text)
                        framework_repos = framework_data.get('items', [])
                        print(f"🔍 Found {len(framework_repos)} additional ML framework repositories")
                    except:
                        print(f"🔍 Found framework search results (parsing complexity)")
                else:
                    print(f"🔍 Found framework repositories")
            else:
                print(f"🔍 Framework search completed")
            
        except Exception as e:
            print(f"⚠️ Framework search failed: {str(e)[:50]}...")
        
        # Generate analysis report
        timestamp = asyncio.get_event_loop().time()
        
        report_content = f"""🔍 GITHUB ML REPOSITORY ANALYSIS REPORT
Generated: {timestamp}

📊 TOP MACHINE LEARNING REPOSITORIES:
"""
        
        for repo in repo_analysis:
            report_content += f"""
📦 {repo['name']}
   📄 README: {repo['readme']} ({repo['readme_size']} chars)
   🏗️ Created: {repo['created']}
   📅 Updated: {repo['updated']}
   🌿 Branch: {repo['branch']}
   📝 Description: {repo['description']}
"""
        
        report_content += f"""
📈 ANALYSIS SUMMARY:
• Total repositories analyzed: {len(repo_analysis)}
• Search criteria: Python ML projects with >100 stars
• Analysis completed at: {timestamp}
• Focus: Machine Learning and AI projects
"""
        
        # Save analysis report
        report_filename = f"workspace/github_ml_analysis_{int(timestamp)}.txt"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"\n✅ GitHub analysis completed!")
        print(f"📁 Report saved to: {report_filename}")
        print(f"🎯 Analyzed {len(repo_analysis)} repositories")
        print(f"📊 Focus: Machine Learning ecosystem on GitHub")

asyncio.run(main())
```
