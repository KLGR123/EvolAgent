### How to Access and Manipulate Local File Systems Using MCP

**Description**: Connect to and interact with local file systems through the Model Context Protocol (MCP) filesystem server. This powerful integration enables programmatic file management, directory traversal, content reading and writing, and comprehensive file system operations through a standardized protocol interface. MCP provides a unified way to access file system resources, eliminating the need for direct file I/O operations while maintaining security and consistency across different environments.

**Use Cases**:
- Browse and navigate complex directory structures programmatically for data analysis projects
- Read and process multiple files simultaneously for batch data processing workflows
- Create, modify, and organize files and folders for automated content management systems
- Monitor file system changes and perform automated backup or synchronization operations
- Search through large file collections and extract specific content based on patterns or criteria
- Manage configuration files, logs, and application data across different system environments
- Process documents, images, and media files stored in local directories for content analysis
- Implement file-based data pipelines that require systematic file manipulation and organization
- Automate file cleanup, archiving, and maintenance tasks for system administration
- Access and process legacy data stored in various file formats across directory hierarchies

```
import asyncio
import json
import os
import time
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from dotenv import load_dotenv

load_dotenv()

# Set up MCP filesystem connection to access current working directory
workspace_path = os.getcwd()  # Use current working directory
fs_transport = StdioTransport(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", workspace_path]
)

async def main():
    async with Client(fs_transport) as client:
        print("🔍 Starting filesystem analysis and data processing...")
        
        # Get available filesystem tools and show connection status
        tools = await client.list_tools()
        print(f"📁 Connected to filesystem. Available tools: {[tool.name for tool in tools]}")
        
        # List all files and directories in the root workspace
        directory_listing = await client.call_tool(
            "list_directory",
            arguments={"path": "."}
        )
        print(f"\n📂 Workspace directory contents:")
        print(f"{directory_listing.content}")
        
        # Search for important configuration files
        config_files = await client.call_tool(
            "search_files",
            arguments={
                "pattern": "*.json",
                "path": "."
            }
        )
        print(f"\n⚙️ Found configuration files:")
        print(f"{config_files.content}")
        
        # Create a comprehensive data processing report
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Try to read an existing configuration file if available
        try:
            config_content = await client.call_tool(
                "read_file", 
                arguments={"path": "package.json"}
            )
            project_info = "Found project configuration"
            config_size = len(str(config_content.content))
            print(f"📋 Project configuration loaded ({config_size} chars)")
        except Exception as e:
            project_info = "No package.json found - creating new workspace"
            print(f"📋 {project_info}")
        
        # Generate processing report with detailed analysis
        report_content = f"""📊 FILESYSTEM ANALYSIS REPORT
Generated: {timestamp}
Workspace: {workspace_path}
Project Status: {project_info}

📁 DIRECTORY ANALYSIS:
{directory_listing.content}

⚙️ CONFIGURATION FILES:
{config_files.content}

🔍 PROCESSING SUMMARY:
• Analysis timestamp: {timestamp}
• Workspace scanned: {workspace_path}
• Tools available: {len(tools)}
• Files catalogued: Processing completed
"""
        
        # Save the analysis report
        report_filename = f"workspace/filesystem_analysis_{timestamp}.txt"
        write_result = await client.call_tool(
            "write_file",
            arguments={
                "path": report_filename,
                "content": report_content
            }
        )
        print(f"📄 Created analysis report: {write_result.content}")
        
        # Find all Python files for development analysis
        python_files = await client.call_tool(
            "search_files",
            arguments={
                "pattern": "*.py",
                "path": "."
            }
        )
        print(f"\n🐍 Python files in workspace:")
        print(f"{python_files.content}")
        
        # Search for data files for potential processing
        data_files = await client.call_tool(
            "search_files",
            arguments={
                "pattern": "*.csv",
                "path": "."
            }
        )
        print(f"\n📊 Data files found:")
        print(f"{data_files.content}")
        
        # Create a project summary file
        summary_content = f"""🏗️ PROJECT WORKSPACE SUMMARY
Generated: {timestamp}

📈 WORKSPACE STATISTICS:
• Analysis completed at: {timestamp}
• Tools utilized: {', '.join([tool.name for tool in tools[:5]])}
• File types scanned: JSON, Python, CSV
• Reports generated: 1 analysis report

📁 DIRECTORY STRUCTURE:
{directory_listing.content}

🎯 NEXT STEPS:
• Review filesystem analysis report: {report_filename}
• Process any data files found: {len(str(data_files.content).split()) if data_files.content else 0} items
• Analyze Python codebase: {len(str(python_files.content).split()) if python_files.content else 0} files
"""
        
        summary_filename = f"workspace/workspace_summary_{timestamp}.txt"
        await client.call_tool(
            "write_file",
            arguments={
                "path": summary_filename,
                "content": summary_content
            }
        )
        
        print(f"\n✅ Filesystem analysis completed successfully!")
        print(f"📁 Analysis report: {report_filename}")
        print(f"📋 Workspace summary: {summary_filename}")
        print(f"🎯 Scanned workspace: {workspace_path}")
        print(f"📊 Total tools available: {len(tools)}")

asyncio.run(main())
```
