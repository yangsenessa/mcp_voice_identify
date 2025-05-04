import os
import time
import base64
import re
from typing import Dict, Any, Optional
import requests

class VoiceService:
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.name = "Voice Recognition Service"
        self.version = "1.0.0"
        self.author = "AIO-2030"
        self.github = "https://github.com/AIO-2030/mcp_voice_identify"
        
        # Initialize API configuration
        self.api_url = api_url or os.getenv("API_URL")
        self.api_key = api_key or os.getenv("API_KEY")
        
        if not self.api_url or not self.api_key:
            raise ValueError("API_URL and API_KEY must be provided either through constructor or environment variables")

    def parse_label_result(self, label_result: str) -> Dict[str, str]:
        """Parse label result into structured format"""
        # Extract values between <| and |>
        pattern = r'<\|(.*?)\|>'
        matches = re.findall(pattern, label_result)
        
        # Initialize result dictionary
        result = {
            "lan": "unknown",
            "emo": "unknown",
            "type": "unknown",
            "speaker": "unknown",
            "text": ""
        }
        
        # Map labels to keys
        label_mapping = {
            "en": "lan",
            "EMO_UNKNOWN": "emo",
            "Speech": "type",
            "woitn": "speaker"
        }
        
        # Process matches
        for match in matches:
            if match in label_mapping:
                result[label_mapping[match]] = match.lower()
            elif match not in ["", " "]:
                result["text"] = match
        
        return result

    def restructure_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Restructure API response with parsed label result"""
        if "label_result" in response:
            parsed_label = self.parse_label_result(response["label_result"])
            response["label_result"] = parsed_label
        return response

    def get_help_info(self, include_mcp: bool = True) -> Dict[str, Any]:
        """Return help information"""
        help_info = {
            "type": "voice_service",
            "description": "This service provides voice recognition and text extraction services",
            "author": self.author,
            "version": self.version,
            "github": self.github,
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
        }

        if include_mcp:
            help_info["transport"].append("mcp")
            help_info["methods"].extend([
                {
                    "name": "tools_list",
                    "description": "List all available tools"
                },
                {
                    "name": "tools_call",
                    "description": "Call a tool",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Tool name"
                            },
                            "arguments": {
                                "type": "object",
                                "description": "Tool arguments"
                            }
                        },
                        "required": ["name"]
                    }
                }
            ])
            help_info["prompts"] = [
                {
                    "name": "voice_recognition_prompt",
                    "description": "Create a voice recognition prompt template",
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
                }
            ]
            help_info["resources"] = [
                {
                    "name": "voice_resource",
                    "description": "Provide voice file content as a resource",
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
                }
            ]

        return help_info

    def help(self) -> Dict[str, Any]:
        """Return help information in JSON-RPC 2.0 format"""
        return {
            "jsonrpc": "2.0",
            "result": self.get_help_info(include_mcp=False),
            "id": int(time.time() * 1000)
        }

    def identify_voice(self, file_path: str) -> Dict[str, Any]:
        """Identify voice from file"""
        try:
            with open(file_path, "rb") as f:
                files = {'file': f}
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'accept': 'application/json'
                }
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                return self.restructure_response(result)
        except Exception as e:
            return {"error": str(e)}

    def identify_voice_base64(self, base64_data: str) -> Dict[str, Any]:
        """Identify voice from base64 encoded data"""
        try:
            # Convert base64 to file-like object
            import io
            file_data = base64.b64decode(base64_data)
            file_obj = io.BytesIO(file_data)
            file_obj.name = 'audio.wav'  # Set a filename
            
            files = {'file': file_obj}
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'accept': 'application/json'
            }
            response = requests.post(
                self.api_url,
                headers=headers,
                files=files
            )
            response.raise_for_status()
            result = response.json()
            return self.restructure_response(result)
        except Exception as e:
            return {"error": str(e)}

    def extract_text(self, text: str) -> Dict[str, Any]:
        """Extract text"""
        try:
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"text": text}
            )
            response.raise_for_status()
            result = response.json()
            return self.restructure_response(result)
        except Exception as e:
            return {"error": str(e)}

    def voice_recognition_prompt(self, file_path: str) -> str:
        """Create a voice recognition prompt template"""
        return f"Please process this voice file: {file_path}"

    def voice_resource(self, file_path: str) -> str:
        """Provide voice file content as a resource"""
        try:
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode()
        except Exception as e:
            return {"error": str(e)} 