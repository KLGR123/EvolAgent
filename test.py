from mcp import StdioServerParameters, ClientSession
from mcp.client import stdio
import os
import asyncio
from pathlib import Path

import nest_asyncio
nest_asyncio.apply()

# 定义工作空间路径
workspace_path = Path("./browser_output")
workspace_path.mkdir(exist_ok=True)

# 配置browser-use工具从 `playwright-mcp`
server_parameters = StdioServerParameters(
    command="npx",
    args=[
        "-y", 
        "@playwright/mcp@latest", 
        "--viewport-size", "1920,1080", 
        "--output-dir", str(workspace_path),
        "--isolated"  # --isolated 用于创建多个浏览器实例
    ],
    env={"UV_PYTHON": "3.11", **os.environ},
)

# 全局变量来保持连接
client_connection = None

async def initialize_browser():
    """初始化浏览器连接"""
    global client_connection
    
    if client_connection is None:
        stdio_client = stdio.stdio_client(server_parameters)
        read, write = await stdio_client.__aenter__()
        
        client_session = ClientSession(read, write)
        await client_session.__aenter__()
        await client_session.initialize()
        
        client_connection = {
            'session': client_session,
            'stdio_client': stdio_client,
            'read': read,
            'write': write
        }
        print("浏览器连接已初始化")
    
    return client_connection['session']

async def close_browser():
    """关闭浏览器连接"""
    global client_connection
    if client_connection:
        try:
            await client_connection['session'].__aexit__(None, None, None)
            await client_connection['stdio_client'].__aexit__(None, None, None)
            client_connection = None
            print("浏览器连接已关闭")
        except Exception as e:
            print(f"关闭连接时出错: {e}")

async def list_tools():
    """获取可用工具列表"""
    session = await initialize_browser()
    tools_response = await session.list_tools()
    return tools_response.tools

async def browser_navigate(url):
    """导航到指定网页"""
    session = await initialize_browser()
    result = await session.call_tool("browser_navigate", {"url": url})
    return result

async def main():
    """主函数"""
    try:
        print("初始化浏览器...")
        await initialize_browser()

        print("\n获取可用工具...")
        tools = await list_tools()
        print(f"可用工具数量: {len(tools)}")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")

        print("\n导航到网页...")
        result = await browser_navigate("https://example.com")
        print(f"导航结果: {result}")

    except Exception as e:
        print(f"执行过程中出错: {e}")
    finally:
        # 如果你想让浏览器保持打开状态，注释掉下面这行
        # await close_browser()
        return

# 运行主函数
if __name__ == "__main__":
    asyncio.run(main())