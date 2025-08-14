### How to Perform Web Navigation and Browser Automation Using MCP Integration

**Description**: Connect to and control web browsers through the Model Context Protocol (MCP) browser automation server. This powerful integration enables comprehensive webpage reading, web navigation, browser control, automated web testing, screenshot capture, and interactive web content manipulation through a standardized protocol interface. MCP provides seamless access to browser functionality, DOM interaction, and web content extraction without requiring direct browser driver management or complex automation framework setup.

**Use Cases**:
- Navigate websites programmatically for automated testing and quality assurance workflows
- Capture screenshots and visual content from web pages for documentation and monitoring
- Extract data from dynamic websites with JavaScript-rendered content and interactive elements
- Automate form filling, button clicking, and user interaction sequences for testing workflows
- Monitor website changes, performance metrics, and visual regression testing
- Scrape e-commerce sites, social media platforms, and data-rich web applications
- Perform automated web searches and content discovery across multiple search engines
- Test web application functionality, user interfaces, and cross-browser compatibility
- Generate reports from web-based dashboards, analytics platforms, and administrative interfaces
- Access and interact with web APIs, single-page applications, and progressive web applications
- Automate repetitive web tasks such as data entry, content publishing, and account management
- Perform web content analysis, SEO auditing, and accessibility testing
- Monitor competitor websites, pricing changes, and market intelligence gathering

```
import asyncio
import os
import time
import json
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from dotenv import load_dotenv

load_dotenv()

# Set up browser automation MCP connection
playwright_transport = StdioTransport(
    command="npx",
    args=["-y", "@playwright/mcp@latest"]
)

async def main():
    async with Client(playwright_transport) as client:
        print("🔄 Starting web content monitoring...")
        
        # Get available browser automation tools
        tools = await client.list_tools()
        print(f"🌐 Connected to browser automation. Available tools: {[tool.name for tool in tools]}")
        
        # Navigate to Hacker News for tech story extraction
        await client.call_tool(
            "browser_navigate",
            arguments={"url": "https://news.ycombinator.com"}
        )
        
        await client.call_tool("browser_wait_for", arguments={"time": 3})
        
        # Capture homepage screenshot
        await client.call_tool("browser_take_screenshot")
        print("📸 Homepage screenshot captured")
        
        # Extract clean story titles from Hacker News
        stories_raw = await client.call_tool(
            "browser_evaluate",
            arguments={
                "function": """() => {
                    const titles = [];
                    const links = document.querySelectorAll('.titleline > a');
                    for (let i = 0; i < Math.min(5, links.length); i++) {
                        const title = links[i].textContent.trim();
                        if (title && !title.includes('Result') && !title.includes('###')) {
                            titles.push(title);
                        }
                    }
                    return titles.join('###SEPARATOR###');
                }"""
            }
        )
        
        # Process Hacker News stories
        hn_stories = []
        if stories_raw.content and not str(stories_raw.content).startswith('### Result'):
            # Extract only the actual content, ignore metadata
            content_text = str(stories_raw.content)
            if '###SEPARATOR###' in content_text:
                hn_stories = [s.strip() for s in content_text.split('###SEPARATOR###') if s.strip()]
            else:
                # Fallback: try to extract clean text
                lines = content_text.split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('###') and not line.startswith('```'):
                        if len(line.strip()) > 10:  # Filter out short metadata
                            hn_stories.append(line.strip())
                            if len(hn_stories) >= 5:
                                break
        
        print("\n📰 Top Hacker News Stories:")
        for i, story in enumerate(hn_stories[:5]):
            print(f"  {i+1}. {story}")
        
        # Navigate to a simple news aggregation approach
        await client.call_tool(
            "browser_navigate", 
            arguments={"url": "https://lobste.rs"}
        )
        
        await client.call_tool("browser_wait_for", arguments={"time": 3})
        print("🔄 Switched to Lobsters for additional tech news...")
        
        # Extract Lobsters stories as backup content
        lobsters_stories = await client.call_tool(
            "browser_evaluate",
            arguments={
                "function": """() => {
                    const titles = [];
                    const links = document.querySelectorAll('.story_liner .link a');
                    for (let i = 0; i < Math.min(3, links.length); i++) {
                        const title = links[i].textContent.trim();
                        if (title) {
                            titles.push(title);
                        }
                    }
                    return titles.join('###SEPARATOR###');
                }"""
            }
        )
        
        # Process Lobsters stories
        lobster_list = []
        if lobsters_stories.content:
            content = str(lobsters_stories.content)
            if '###SEPARATOR###' in content:
                lobster_list = [s.strip() for s in content.split('###SEPARATOR###') if s.strip()]
        
        print("\n🦞 Additional Tech Stories from Lobsters:")
        for i, story in enumerate(lobster_list[:3]):
            print(f"  {i+1}. {story}")
        
        # Generate a clean, comprehensive report
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        
        report_content = f"""🔍 TECH NEWS MONITORING REPORT
Generated: {timestamp}
Sources: Hacker News + Lobsters

📈 TOP HACKER NEWS STORIES:
"""
        
        for i, story in enumerate(hn_stories[:5]):
            report_content += f"\n{i+1}. {story}\n"
        
        if lobster_list:
            report_content += "\n🦞 ADDITIONAL STORIES FROM LOBSTERS:\n"
            for i, story in enumerate(lobster_list[:3]):
                report_content += f"\n• {story}\n"
        
        report_content += f"\n📊 SUMMARY:\n"
        report_content += f"• Hacker News stories tracked: {len(hn_stories)}\n"
        report_content += f"• Lobsters stories tracked: {len(lobster_list)}\n"
        report_content += f"• Total unique tech stories: {len(hn_stories) + len(lobster_list)}\n"
        report_content += f"• Report generated at: {timestamp}\n"
        
        # Save monitoring results
        report_filename = f"workspace/tech_news_{timestamp}.txt"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"\n✅ Monitoring completed successfully!")
        print(f"📁 Report saved to: {report_filename}")
        print(f"📊 Tracked {len(hn_stories)} HN stories + {len(lobster_list)} Lobsters stories")
        print(f"🎯 Total: {len(hn_stories) + len(lobster_list)} tech news items monitored")

asyncio.run(main())
```
