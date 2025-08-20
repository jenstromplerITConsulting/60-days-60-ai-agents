import os
import re
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Note:
    title: str
    content: str
    file_path: str
    created_time: datetime
    modified_time: datetime
    tags: List[str]
    links: List[str]

class VaultReader:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(f"Vault path does not exist: {vault_path}")
    
    def get_all_notes(self) -> List[Note]:
        notes = []
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.is_file():
                note = self._parse_note(md_file)
                if note:
                    notes.append(note)
        return notes
    
    def _parse_note(self, file_path: Path) -> Note:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            stat = file_path.stat()
            created_time = datetime.fromtimestamp(stat.st_ctime)
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            title = self._extract_title(content, file_path.stem)
            tags = self._extract_tags(content)
            links = self._extract_links(content)
            
            return Note(
                title=title,
                content=content,
                file_path=str(file_path),
                created_time=created_time,
                modified_time=modified_time,
                tags=tags,
                links=links
            )
        except Exception as e:
            print(f"Error parsing note {file_path}: {e}")
            return None
    
    def _extract_title(self, content: str, filename: str) -> str:
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                return line[2:].strip()
        return filename
    
    def _extract_tags(self, content: str) -> List[str]:
        tag_pattern = r'#([a-zA-Z0-9_/-]+)'
        tags = re.findall(tag_pattern, content)
        return list(set(tags))
    
    def _extract_links(self, content: str) -> List[str]:
        link_pattern = r'\[\[([^\]]+)\]\]'
        links = re.findall(link_pattern, content)
        return list(set(links))
    
    def search_notes(self, query: str, search_in: str = "content") -> List[Note]:
        notes = self.get_all_notes()
        matching_notes = []
        
        query_lower = query.lower()
        
        for note in notes:
            match = False
            
            if search_in in ["title", "both"]:
                if query_lower in note.title.lower():
                    match = True
            
            if search_in in ["content", "both"]:
                if query_lower in note.content.lower():
                    match = True
            
            if match:
                matching_notes.append(note)
        
        return matching_notes
    
    def search_by_tags(self, tags: List[str]) -> List[Note]:
        notes = self.get_all_notes()
        matching_notes = []
        
        tags_lower = [tag.lower() for tag in tags]
        
        for note in notes:
            note_tags_lower = [tag.lower() for tag in note.tags]
            if any(tag in note_tags_lower for tag in tags_lower):
                matching_notes.append(note)
        
        return matching_notes
    
    def get_linked_notes(self, note_title: str) -> List[Note]:
        notes = self.get_all_notes()
        linked_notes = []
        
        for note in notes:
            if note_title in note.links or note.title in note.links:
                linked_notes.append(note)
        
        return linked_notes
    
    def get_note_by_title(self, title: str) -> Note:
        notes = self.get_all_notes()
        for note in notes:
            if note.title.lower() == title.lower():
                return note
        return None