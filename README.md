# 60 Days 60 AI Agents

Ein modulares Python-Framework zur Entwicklung spezialisierter AI Agents.

## 🚀 Schnellstart

1. **Setup der Entwicklungsumgebung:**
   ```bash
   cd main
   ./setup.sh
   ```

2. **Environment aktivieren:**
   ```bash
   source venv/bin/activate
   ```

## 🤖 Verfügbare Agents

### Obsidian Vault Agent
Ein intelligenter Agent zur Durchsuchung und Analyse von Obsidian Vaults.

**Features:**
- 📖 Durchsuchen von Notizen nach Inhalt und Titel
- 📊 Automatische Zusammenfassungen
- 🔗 Verbindungsanalyse zwischen Notizen
- 📈 Vault-Statistiken
- 💬 Interaktiver CLI-Chatbot

**Setup:**
1. Konfiguration anpassen:
   ```bash
   cd obsidian_agent
   cp config_example.yaml config.yaml
   # Bearbeite config.yaml und setze deinen Vault-Pfad
   ```

2. Agent starten:
   ```bash
   python cli_chatbot.py
   ```

**Unterstützte LLM-Provider:**
- 🦙 **Ollama** (empfohlen für lokale Entwicklung)
- 🤖 **OpenAI** (GPT-3.5/GPT-4)
- 🧠 **Claude** (Anthropic)

## 📁 Projektstruktur

```
main/
├── venv/                    # Globales Virtual Environment
├── requirements.txt         # Python Dependencies
├── setup.sh                # Setup-Skript
├── .gitignore              # Git-Konfiguration
└── obsidian_agent/         # Obsidian Vault Agent
    ├── config_example.yaml  # Beispiel-Konfiguration
    ├── config.yaml         # Deine Konfiguration (wird ignoriert)
    ├── config_manager.py    # Konfiguration-Management
    ├── vault_reader.py      # Obsidian Vault Parser
    ├── llm_manager.py       # LLM Provider Management
    ├── obsidian_agent.py    # Haupt-Agent Klasse
    └── cli_chatbot.py       # CLI Interface
```

## 🛠 Entwicklung

### Neuen Agent hinzufügen

1. Erstelle einen neuen Ordner für deinen Agent
2. Implementiere die Basis-Klassen:
   - `config_manager.py` - Konfiguration
   - `llm_manager.py` - LLM-Anbindung (kann importiert werden)
   - `your_agent.py` - Agent-Logik
   - `cli_interface.py` - Benutzerinterface

### LLM-Provider konfigurieren

**Ollama (lokal):**
```bash
# Ollama installieren und Modell herunterladen
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1
```

**OpenAI:**
```yaml
llm:
  provider: "openai"
  openai:
    api_key: "sk-your-api-key"
    model: "gpt-3.5-turbo"
```

**Claude:**
```yaml
llm:
  provider: "claude"
  claude:
    api_key: "your-claude-api-key"
    model: "claude-3-sonnet-20240229"
```

## 📝 Lizenz

MIT License - siehe LICENSE Datei für Details.
