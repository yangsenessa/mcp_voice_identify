import json
import sys
from voice_service import VoiceService

def main():
    service = VoiceService(
        api_url="https://openapi.emchub.ai/emchub/api/openapi/task/executeTaskByUser/edgematrix:yiminger/extract_text",
        api_key="833_txLiSbJibu160317539183112192"
    )
    
    # Read input from stdin
    for line in sys.stdin:
        try:
            # Parse JSON-RPC request
            request = json.loads(line)
            
            # Get method and params
            method = request.get("method")
            params = request.get("params", {})
            
            # Handle different methods
            if method == "help":
                response = service.help()
            elif method == "identify_voice":
                response = {
                    "jsonrpc": "2.0",
                    "result": service.identify_voice(params.get("file_path")),
                    "id": request.get("id")
                }
            elif method == "identify_voice_base64":
                response = {
                    "jsonrpc": "2.0",
                    "result": service.identify_voice_base64(params.get("base64_data")),
                    "id": request.get("id")
                }
            elif method == "extract_text":
                response = {
                    "jsonrpc": "2.0",
                    "result": service.extract_text(params.get("text")),
                    "id": request.get("id")
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": request.get("id")
                }
            
            # Write response to stdout
            print(json.dumps(response))
            sys.stdout.flush()
            
        except json.JSONDecodeError:
            print(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                },
                "id": None
            }))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": str(e)
                },
                "id": request.get("id") if "request" in locals() else None
            }))
            sys.stdout.flush()

if __name__ == "__main__":
    main() 