### How to load tools from existing MCP servers

**Description**: Connect to and interact with various Model Context Protocol (MCP) servers to access their tools and capabilities. This script demonstrates how to establish connections with filesystem, GitHub, and browser automation MCP servers, list available tools, and execute specific operations like file system access, GitHub repository searches, and web browser automation.

**Use Cases**:
- Connect to filesystem MCP servers to browse and manipulate local file systems programmatically
- Access GitHub MCP servers to search repositories, manage issues, and interact with GitHub APIs
- Utilize browser automation MCP servers for web scraping, screenshot capture, and automated web testing
- Integrate multiple MCP servers in a single application to create comprehensive automation workflows
- Build AI agents that can interact with various external services through standardized MCP interfaces
- Develop tools that can access file systems, version control platforms, and web browsers simultaneously
- Create automation scripts that leverage different MCP server capabilities for data collection and processing
- Implement cross-platform tools that work with files, code repositories, and web content through unified MCP interfaces

```
import asyncio
import json
import os
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from dotenv import load_dotenv
load_dotenv()

async def main():
    # filesystem mcp
    fs_transport = StdioTransport(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "/Users/xushiyue.6/documents"]
    )
    async with Client(fs_transport) as client:
        tools_dict = {}
        tools = await client.list_tools()
        for tool in tools:
            tools_dict[tool.name] = tool
            print({"tool name:":tool.name, "tool description:":tool.description})
        print("="*50)

    # github mcp
    gh_transport = StdioTransport(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")}
    )
    async with Client(gh_transport) as client:
        tools = await client.list_tools()
        tools_dict = {}
        for tool in tools:
            tools_dict[tool.name] = tool
            print({"tool name:":tool.name, "tool description:":tool.description})
        print("="*50)

        # 搜索trl示例
        search_result = await client.call_tool(
            "search_repositories",
            arguments={
                "query": "verl", 
                "perPage": 1,
            }
        )
        print("\n--- GitHub 搜索结果（trl） ---")
        print(search_result.content)
        print("="*50)

    # browser-use mcp
    playwright_transport = StdioTransport(
        command="npx",
        args=["-y", "@playwright/mcp@latest"],
    )
    # stable client
    async with Client(playwright_transport) as client:
        tools = await client.list_tools()
        tools_dict = {}
        for tool in tools:
            tools_dict[tool.name] = tool
            print({"tool name:":tool.name, "tool description:":tool.description})
        print("="*50)

        print(tools_dict["browser_take_screenshot"])
        # Open browser and access the given website
        await client.call_tool(
            "browser_navigate",
            arguments={
                "url": "https://www.jd.com"
            }
        )

        await client.call_tool(
            "browser_take_screenshot",
        )
        
        # 保持浏览器打开状态，等待关闭信号
        print("\n浏览器已打开并截图完成！")
        print("浏览器将保持打开状态，创建 'close_browser.txt' 文件来关闭浏览器")
        
        # 持续检查关闭信号文件
        import time
        close_file_path = "/tmp/close_browser.txt"
        while True:
            if os.path.exists(close_file_path):
                print("检测到关闭信号，正在关闭浏览器...")
                os.remove(close_file_path)  # 删除信号文件
                break
            time.sleep(1)  # 每秒检查一次

if __name__ == "__main__":
    asyncio.run(main())

```