import yaml
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent / "config.yaml"
        self.config_path = Path(config_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing config file: {e}")
    
    def get_vault_path(self) -> str:
        vault_path = self.config.get('vault', {}).get('path', '')
        if not vault_path or not os.path.exists(vault_path):
            raise ValueError(f"Invalid vault path: {vault_path}")
        return vault_path
    
    def get_llm_config(self) -> Dict[str, Any]:
        llm_config = self.config.get('llm', {})
        provider = llm_config.get('provider', 'ollama')
        
        if provider not in ['ollama', 'openai', 'claude']:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        return {
            'provider': provider,
            'config': llm_config.get(provider, {})
        }
    
    def get_agent_config(self) -> Dict[str, Any]:
        return self.config.get('agent', {
            'max_notes_per_query': 10,
            'search_depth': 'content',
            'summary_max_length': 500
        })
    
    def validate_config(self) -> bool:
        try:
            self.get_vault_path()
            self.get_llm_config()
            return True
        except (ValueError, FileNotFoundError):
            return False