# Voice Recognition MCP Service

This service provides voice recognition and text extraction capabilities through both stdio and MCP modes.

## Features

- Voice recognition from file
- Voice recognition from base64 encoded data
- Text extraction
- Support for both stdio and MCP modes
- Structured voice recognition results
- AIO protocol compliant responses

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

## Response Format

The service follows the AIO protocol for response formatting. Here are examples of different response types:

### Voice Recognition Response
```json
{
    "jsonrpc": "2.0",
    "output": {
        "type": "voice",
        "message": "Voice processed successfully",
        "text": "test test test",
        "metadata": {
            "language": "en",
            "emotion": "unknown",
            "audio_type": "speech",
            "speaker": "woitn",
            "raw_text": "test test test"
        }
    },
    "id": 1
}
```

### Help Information Response
```json
{
    "jsonrpc": "2.0",
    "result": {
        "type": "voice_service",
        "description": "This service provides voice recognition and text extraction services",
        "author": "AIO-2030",
        "version": "1.0.0",
        "github": "https://github.com/AIO-2030/mcp_voice_identify",
        "transport": ["stdio"],
        "methods": [
            {
                "name": "help",
                "description": "Show this help information."
            },
            {
                "name": "identify_voice",
                "description": "Identify voice from file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Voice file path"
                        }
                    },
                    "required": ["file_path"]
                }
            },
            {
                "name": "identify_voice_base64",
                "description": "Identify voice from base64 encoded data",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "base64_data": {
                            "type": "string",
                            "description": "Base64 encoded voice data"
                        }
                    },
                    "required": ["base64_data"]
                }
            },
            {
                "name": "extract_text",
                "description": "Extract text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to extract"
                        }
                    },
                    "required": ["text"]
                }
            }
        ]
    },
    "id": 1
}
```

### Error Response
```json
{
    "jsonrpc": "2.0",
    "output": {
        "type": "error",
        "message": "503 Server Error: Service Unavailable",
        "error_code": 503
    },
    "id": 1
}
```

### Response Fields

The service provides three types of responses:

1. Voice Recognition Response (using `output` field):
| Field     | Description                          | Example Value |
|-----------|--------------------------------------|---------------|
| type      | Response type                        | "voice"       |
| message   | Status message                       | "Voice processed successfully" |
| text      | Recognized text content              | "test test test" |
| metadata  | Additional information               | See below     |

2. Help Information Response (using `result` field):
| Field         | Description                          | Example Value |
|---------------|--------------------------------------|---------------|
| type          | Service type                         | "voice_service" |
| description   | Service description                  | "This service provides..." |
| author        | Service author                       | "AIO-2030"    |
| version       | Service version                      | "1.0.0"       |
| github        | GitHub repository URL                | "https://github.com/..." |
| transport     | Supported transport modes            | ["stdio"]     |
| methods       | Available methods                    | See methods list |

3. Error Response (using `output` field):
| Field       | Description                          | Example Value |
|-------------|--------------------------------------|---------------|
| type        | Response type                        | "error"       |
| message     | Error message                        | "503 Server Error: Service Unavailable" |
| error_code  | HTTP status code                     | 503          |

### Metadata Fields

The `metadata` field in voice recognition responses contains:

| Field       | Description                          | Example Value |
|-------------|--------------------------------------|---------------|
| language    | Language code                        | "en"          |
| emotion     | Emotion state                        | "unknown"     |
| audio_type  | Audio type                          | "speech"      |
| speaker     | Speaker identifier                   | "woitn"       |
| raw_text    | Original recognized text             | "test test test" |

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
