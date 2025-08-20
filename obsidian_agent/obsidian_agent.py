from typing import List, Dict, Any
from vault_reader import VaultReader, Note
from llm_manager import LLMManager
from config_manager import ConfigManager

class ObsidianAgent:
    def __init__(self, config_path: str = None):
        self.config_manager = ConfigManager(config_path)
        self.vault_reader = VaultReader(self.config_manager.get_vault_path())
        self.llm_manager = LLMManager(self.config_manager.get_llm_config())
        self.agent_config = self.config_manager.get_agent_config()
    
    def search_and_answer(self, query: str) -> str:
        relevant_notes = self._find_relevant_notes(query)
        
        if not relevant_notes:
            return "Keine relevanten Notizen für deine Frage gefunden."
        
        context = self._prepare_context(relevant_notes, query)
        prompt = self._create_prompt(query, context)
        
        return self.llm_manager.generate_response(prompt)
    
    def summarize_notes(self, search_term: str = None, tags: List[str] = None) -> str:
        if search_term:
            notes = self.vault_reader.search_notes(search_term, "both")
        elif tags:
            notes = self.vault_reader.search_by_tags(tags)
        else:
            notes = self.vault_reader.get_all_notes()
        
        if not notes:
            return "Keine Notizen gefunden."
        
        max_notes = self.agent_config.get('max_notes_per_query', 10)
        notes = notes[:max_notes]
        
        context = self._prepare_notes_for_summary(notes)
        prompt = f"""Erstelle eine strukturierte Zusammenfassung der folgenden Notizen:

{context}

Erstelle eine Zusammenfassung mit:
1. Hauptthemen und Kategorien
2. Wichtigste Erkenntnisse
3. Verbindungen zwischen den Notizen
4. Actionable Items (falls vorhanden)

Halte die Zusammenfassung auf maximal {self.agent_config.get('summary_max_length', 500)} Wörter."""
        
        return self.llm_manager.generate_response(prompt)
    
    def get_note_details(self, note_title: str) -> str:
        note = self.vault_reader.get_note_by_title(note_title)
        
        if not note:
            return f"Notiz '{note_title}' nicht gefunden."
        
        linked_notes = self.vault_reader.get_linked_notes(note_title)
        
        prompt = f"""Analysiere die folgende Notiz und erstelle eine strukturierte Übersicht:

**Titel:** {note.title}
**Pfad:** {note.file_path}
**Erstellt:** {note.created_time.strftime('%d.%m.%Y %H:%M')}
**Geändert:** {note.modified_time.strftime('%d.%m.%Y %H:%M')}
**Tags:** {', '.join(note.tags) if note.tags else 'Keine Tags'}
**Verlinkte Notizen:** {len(linked_notes)} Notizen

**Inhalt:**
{note.content}

Erstelle eine Analyse mit:
1. Kurzer Zusammenfassung des Inhalts
2. Hauptthemen und Konzepte
3. Verbindungen zu anderen Notizen
4. Wichtige Erkenntnisse oder Actionable Items
"""
        
        return self.llm_manager.generate_response(prompt)
    
    def find_connections(self, topic: str) -> str:
        relevant_notes = self.vault_reader.search_notes(topic, "both")
        
        if len(relevant_notes) < 2:
            return f"Nicht genügend Notizen zum Thema '{topic}' für Verbindungsanalyse gefunden."
        
        max_notes = self.agent_config.get('max_notes_per_query', 10)
        relevant_notes = relevant_notes[:max_notes]
        
        context = self._prepare_context(relevant_notes, topic)
        
        prompt = f"""Analysiere die Verbindungen zwischen diesen Notizen zum Thema '{topic}':

{context}

Identifiziere und erkläre:
1. Gemeinsame Themen und Konzepte
2. Widersprüche oder unterschiedliche Perspektiven
3. Chronologische Entwicklungen
4. Mögliche Zusammenhänge die nicht offensichtlich sind
5. Empfehlungen für weitere Verbindungen
"""
        
        return self.llm_manager.generate_response(prompt)
    
    def _find_relevant_notes(self, query: str) -> List[Note]:
        search_depth = self.agent_config.get('search_depth', 'content')
        max_notes = self.agent_config.get('max_notes_per_query', 10)
        
        notes = self.vault_reader.search_notes(query, search_depth)
        
        return sorted(notes, key=lambda x: x.modified_time, reverse=True)[:max_notes]
    
    def _prepare_context(self, notes: List[Note], query: str) -> str:
        context_parts = []
        
        for i, note in enumerate(notes, 1):
            context_parts.append(f"""--- Notiz {i}: {note.title} ---
Pfad: {note.file_path}
Tags: {', '.join(note.tags) if note.tags else 'Keine'}
Inhalt: {note.content[:1000]}{"..." if len(note.content) > 1000 else ""}
""")
        
        return "\n".join(context_parts)
    
    def _prepare_notes_for_summary(self, notes: List[Note]) -> str:
        context_parts = []
        
        for note in notes:
            context_parts.append(f"""**{note.title}**
Tags: {', '.join(note.tags) if note.tags else 'Keine'}
{note.content[:800]}{"..." if len(note.content) > 800 else ""}
""")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        return f"""Du bist ein hilfreicher Assistent, der Fragen zu einem Obsidian Vault beantwortet.

Frage: {query}

Kontext aus den Notizen:
{context}

Beantworte die Frage basierend auf den bereitgestellten Notizen. Wenn die Antwort nicht vollständig in den Notizen steht, gib das an. Verweise auf spezifische Notizen wenn möglich.
"""
    
    def get_vault_statistics(self) -> str:
        notes = self.vault_reader.get_all_notes()
        
        total_notes = len(notes)
        all_tags = set()
        all_links = set()
        total_content_length = 0
        
        for note in notes:
            all_tags.update(note.tags)
            all_links.update(note.links)
            total_content_length += len(note.content)
        
        stats = f"""**Vault Statistiken:**
- Gesamt Notizen: {total_notes}
- Eindeutige Tags: {len(all_tags)}
- Eindeutige Links: {len(all_links)}
- Durchschnittliche Notizlänge: {total_content_length // total_notes if total_notes > 0 else 0} Zeichen

**Häufigste Tags:**
{', '.join(list(all_tags)[:10]) if all_tags else 'Keine Tags gefunden'}
"""
        
        return stats