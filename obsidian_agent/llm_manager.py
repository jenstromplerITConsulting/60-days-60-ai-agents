import requests
import json
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

class OllamaProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        self.base_url = config.get('base_url', 'http://localhost:11434')
        self.model = config.get('model', 'llama3.1')
    
    def generate_response(self, prompt: str) -> str:
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', 'Keine Antwort erhalten')
        
        except requests.exceptions.RequestException as e:
            return f"Fehler bei Ollama-Anfrage: {e}"
        except Exception as e:
            return f"Unerwarteter Fehler: {e}"

class OpenAIProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.max_tokens = config.get('max_tokens', 2000)
        
        if not self.api_key:
            raise ValueError("OpenAI API Key ist erforderlich")
    
    def generate_response(self, prompt: str) -> str:
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
        
        except ImportError:
            return "OpenAI-Bibliothek nicht installiert. Führe aus: pip install openai"
        except Exception as e:
            return f"Fehler bei OpenAI-Anfrage: {e}"

class ClaudeProvider(LLMProvider):
    def __init__(self, config: Dict[str, Any]):
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'claude-3-sonnet-20240229')
        self.max_tokens = config.get('max_tokens', 2000)
        
        if not self.api_key:
            raise ValueError("Claude API Key ist erforderlich")
    
    def generate_response(self, prompt: str) -> str:
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
        
        except ImportError:
            return "Anthropic-Bibliothek nicht installiert. Führe aus: pip install anthropic"
        except Exception as e:
            return f"Fehler bei Claude-Anfrage: {e}"

class LLMManager:
    def __init__(self, llm_config: Dict[str, Any]):
        self.provider_name = llm_config['provider']
        self.config = llm_config['config']
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self) -> LLMProvider:
        if self.provider_name == 'ollama':
            return OllamaProvider(self.config)
        elif self.provider_name == 'openai':
            return OpenAIProvider(self.config)
        elif self.provider_name == 'claude':
            return ClaudeProvider(self.config)
        else:
            raise ValueError(f"Unbekannter Provider: {self.provider_name}")
    
    def generate_response(self, prompt: str) -> str:
        return self.provider.generate_response(prompt)
    
    def test_connection(self) -> bool:
        try:
            test_response = self.generate_response("Antworte nur mit 'OK'")
            return "OK" in test_response or len(test_response) < 50
        except Exception:
            return False