import asyncio
import time
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.fastmcp.tools import Tool
from voice_service import VoiceService

# Create MCP server instance
mcp = Server("Voice Recognition MCP")

# Initialize VoiceService with explicit values
service = VoiceService(
    api_url="https://openapi.emchub.ai/emchub/api/openapi/task/executeTaskByUser/edgematrix:yiminger/extract_text",  # Replace with your actual API URL
    api_key="833_txLiSbJibu160317539183112192"  # Replace with your actual API key
)

# Define tools
@Tool.from_function
async def help() -> dict:
    """Return help information in JSON-RPC 2.0 format"""
    return {
        "jsonrpc": "2.0",
        "output": service.get_help_info(include_mcp=True),
        "id": int(time.time() * 1000)
    }

@Tool.from_function
async def identify_voice(file_path: str) -> dict:
    """Identify voice from file"""
    return service.identify_voice(file_path)

@Tool.from_function
async def identify_voice_base64(base64_data: str) -> dict:
    """Identify voice from base64 encoded data"""
    return service.identify_voice_base64(base64_data)

@Tool.from_function
async def extract_text(text: str) -> dict:
    """Extract text"""
    return service.extract_text(text)

@Tool.from_function
def voice_recognition_prompt(file_path: str) -> str:
    """Create a voice recognition prompt template"""
    return service.voice_recognition_prompt(file_path)

@Tool.from_function
async def voice_resource(file_path: str) -> str:
    """Provide voice file content as a resource"""
    return service.voice_resource(file_path)

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(read_stream, write_stream, {})

if __name__ == "__main__":
    asyncio.run(main()) 