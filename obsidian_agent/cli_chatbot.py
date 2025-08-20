#!/usr/bin/env python3
import sys
import os
from pathlib import Path
from obsidian_agent import ObsidianAgent
from config_manager import ConfigManager

class ObsidianCLI:
    def __init__(self):
        self.agent = None
        self.running = True
        self.commands = {
            'help': self.show_help,
            'exit': self.exit_app,
            'quit': self.exit_app,
            'stats': self.show_stats,
            'config': self.show_config,
            'test': self.test_connection,
            'summarize': self.summarize_command,
            'note': self.note_details_command,
            'connections': self.connections_command,
            'clear': self.clear_screen
        }
    
    def initialize_agent(self):
        try:
            config_path = Path(__file__).parent / "config.yaml"
            self.agent = ObsidianAgent(str(config_path))
            print("✅ Obsidian Agent erfolgreich initialisiert!")
            return True
        except Exception as e:
            print(f"❌ Fehler beim Initialisieren des Agents: {e}")
            print("\n💡 Tipps:")
            print("1. Überprüfe deine config.yaml Datei")
            print("2. Stelle sicher, dass der Vault-Pfad korrekt ist")
            print("3. Bei Ollama: Stelle sicher, dass Ollama läuft")
            return False
    
    def run(self):
        print("🧠 Obsidian Vault Agent")
        print("=" * 50)
        
        if not self.initialize_agent():
            return
        
        print("\nTippe 'help' für verfügbare Befehle oder stelle direkt eine Frage!")
        print("Tipp: Du kannst auch direkt Fragen zu deinem Vault stellen.\n")
        
        while self.running:
            try:
                user_input = input("📝 Deine Frage: ").strip()
                
                if not user_input:
                    continue
                
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Auf Wiedersehen!")
                break
            except EOFError:
                break
    
    def process_input(self, user_input: str):
        if user_input.lower() in self.commands:
            self.commands[user_input.lower()]()
        elif user_input.lower().startswith('summarize '):
            self.summarize_with_args(user_input[10:].strip())
        elif user_input.lower().startswith('note '):
            self.note_details_with_args(user_input[5:].strip())
        elif user_input.lower().startswith('connections '):
            self.connections_with_args(user_input[12:].strip())
        else:
            self.ask_question(user_input)
    
    def ask_question(self, question: str):
        print("\n🤔 Durchsuche Vault...")
        try:
            response = self.agent.search_and_answer(question)
            print(f"\n💬 Antwort:\n{response}\n")
        except Exception as e:
            print(f"\n❌ Fehler bei der Anfrage: {e}\n")
    
    def summarize_command(self):
        print("\n📊 Erstelle Zusammenfassung aller Notizen...")
        try:
            response = self.agent.summarize_notes()
            print(f"\n📋 Zusammenfassung:\n{response}\n")
        except Exception as e:
            print(f"\n❌ Fehler bei der Zusammenfassung: {e}\n")
    
    def summarize_with_args(self, args: str):
        if args.startswith('#'):
            tags = [args[1:]]
            print(f"\n📊 Erstelle Zusammenfassung für Tag: {args}")
            try:
                response = self.agent.summarize_notes(tags=tags)
                print(f"\n📋 Zusammenfassung:\n{response}\n")
            except Exception as e:
                print(f"\n❌ Fehler bei der Zusammenfassung: {e}\n")
        else:
            print(f"\n📊 Erstelle Zusammenfassung für: {args}")
            try:
                response = self.agent.summarize_notes(search_term=args)
                print(f"\n📋 Zusammenfassung:\n{response}\n")
            except Exception as e:
                print(f"\n❌ Fehler bei der Zusammenfassung: {e}\n")
    
    def note_details_command(self):
        note_title = input("📄 Notiz-Titel eingeben: ").strip()
        if note_title:
            self.note_details_with_args(note_title)
    
    def note_details_with_args(self, note_title: str):
        print(f"\n📄 Analysiere Notiz: {note_title}")
        try:
            response = self.agent.get_note_details(note_title)
            print(f"\n📄 Notiz-Details:\n{response}\n")
        except Exception as e:
            print(f"\n❌ Fehler bei der Notiz-Analyse: {e}\n")
    
    def connections_command(self):
        topic = input("🔗 Thema für Verbindungsanalyse: ").strip()
        if topic:
            self.connections_with_args(topic)
    
    def connections_with_args(self, topic: str):
        print(f"\n🔗 Analysiere Verbindungen für: {topic}")
        try:
            response = self.agent.find_connections(topic)
            print(f"\n🔗 Verbindungen:\n{response}\n")
        except Exception as e:
            print(f"\n❌ Fehler bei der Verbindungsanalyse: {e}\n")
    
    def show_stats(self):
        print("\n📊 Lade Vault-Statistiken...")
        try:
            stats = self.agent.get_vault_statistics()
            print(f"\n{stats}\n")
        except Exception as e:
            print(f"\n❌ Fehler beim Laden der Statistiken: {e}\n")
    
    def show_config(self):
        try:
            config = self.agent.config_manager
            print("\n⚙️  Aktuelle Konfiguration:")
            print(f"   Vault-Pfad: {config.get_vault_path()}")
            print(f"   LLM-Provider: {config.get_llm_config()['provider']}")
            print(f"   Max. Notizen pro Query: {config.get_agent_config().get('max_notes_per_query', 10)}")
            print()
        except Exception as e:
            print(f"\n❌ Fehler beim Laden der Konfiguration: {e}\n")
    
    def test_connection(self):
        print("\n🔍 Teste LLM-Verbindung...")
        try:
            if self.agent.llm_manager.test_connection():
                print("✅ LLM-Verbindung erfolgreich!\n")
            else:
                print("❌ LLM-Verbindung fehlgeschlagen!\n")
        except Exception as e:
            print(f"❌ Fehler beim Testen der Verbindung: {e}\n")
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_help(self):
        print("\n📚 Verfügbare Befehle:")
        print("=" * 30)
        print("🔍 Direkte Frage stellen:")
        print("   Einfach deine Frage eintippen")
        print("\n📋 Spezielle Befehle:")
        print("   help              - Diese Hilfe anzeigen")
        print("   stats             - Vault-Statistiken anzeigen")
        print("   config            - Aktuelle Konfiguration anzeigen")
        print("   test              - LLM-Verbindung testen")
        print("   clear             - Bildschirm löschen")
        print("\n📊 Zusammenfassungen:")
        print("   summarize         - Alle Notizen zusammenfassen")
        print("   summarize THEMA   - Notizen zu einem Thema zusammenfassen")
        print("   summarize #TAG    - Notizen mit einem Tag zusammenfassen")
        print("\n📄 Notiz-Details:")
        print("   note              - Notiz-Titel eingeben und analysieren")
        print("   note TITEL        - Spezifische Notiz analysieren")
        print("\n🔗 Verbindungen:")
        print("   connections       - Thema eingeben für Verbindungsanalyse")
        print("   connections THEMA - Verbindungen zu einem Thema finden")
        print("\n🚪 Beenden:")
        print("   exit / quit       - Programm beenden")
        print()
    
    def exit_app(self):
        print("\n👋 Auf Wiedersehen!")
        self.running = False

def main():
    cli = ObsidianCLI()
    cli.run()

if __name__ == "__main__":
    main()