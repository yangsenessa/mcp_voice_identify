# Voice Recognition MCP Service

This service provides voice recognition and text extraction capabilities through both stdio and MCP modes.

## Features

- Voice recognition from file
- Voice recognition from base64 encoded data
- Text extraction
- Support for both stdio and MCP modes

## Project Structure

- `voice_service.py` - Core service implementation
- `stdio_server.py` - stdio mode entry point
- `mcp_server.py` - MCP mode entry point
- `build.py` - Build script for executables
- `build_exec.sh` - Build execution script
- `test_*.sh` - Test scripts for different functionalities

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AIO-2030/mcp_voice_identify.git
cd mcp_voice_identify
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```
API_URL=your_api_url
API_KEY=your_api_key
```

## Usage

### stdio Mode

1. Run the service:
```bash
python stdio_server.py
```

2. Send JSON-RPC requests via stdin:
```json
{
    "jsonrpc": "2.0",
    "method": "help",
    "params": {},
    "id": 1
}
```

3. Or use the executable:
```bash
./dist/voice_stdio
```

### MCP Mode

1. Run the service:
```bash
python mcp_server.py
```

2. Or use the executable:
```bash
./dist/voice_mcp
```

## Building Executables

1. Make the build script executable:
```bash
chmod +x build_exec.sh
```

2. Build stdio mode executable:
```bash
./build_exec.sh
```

3. Build MCP mode executable:
```bash
./build_exec.sh mcp
```

The executables will be created at:
- stdio mode: `dist/voice_stdio`
- MCP mode: `dist/voice_mcp`

## Testing

Run the test scripts:

```bash
chmod +x test_*.sh
./test_help.sh
./test_voice_file.sh
./test_voice_base64.sh
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
