#!/bin/bash
# Setup-Skript für AI Agents Entwicklungsumgebung

echo "🚀 AI Agents Entwicklungsumgebung Setup"
echo "======================================"

# Virtual Environment aktivieren
if [ ! -d "venv" ]; then
    echo "📦 Erstelle Virtual Environment..."
    python3 -m venv venv
fi

echo "🔧 Aktiviere Virtual Environment..."
source venv/bin/activate

echo "📥 Installiere Dependencies..."
pip install -r requirements.txt

echo "✅ Setup abgeschlossen!"
echo ""
echo "🔗 Um das Environment zu aktivieren:"
echo "source venv/bin/activate"
echo ""
echo "🤖 Um den Obsidian Agent zu starten:"
echo "cd obsidian_agent && python cli_chatbot.py"