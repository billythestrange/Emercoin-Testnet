#!/bin/bash
# Hilfsskript zum Starten des Coin Control CLI mit optionalen Argumenten
# Erlaubt auch direktes Ausführen von RPC-Befehlen

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/emercoin_coincontrol_cli.py"

# Farben für Terminal-Ausgabe
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Prüfe ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Fehler: Python3 nicht installiert${NC}"
    exit 1
fi

# Prüfe ob requests Library installiert ist
if ! python3 -c "import requests" 2>/dev/null; then
    echo -e "${YELLOW}Warnung: requests Library nicht installiert${NC}"
    echo -e "${BLUE}Installiere: pip install requests${NC}"
    pip install requests
fi

# Prüfe ob das Skript existiert
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo -e "${RED}Fehler: $PYTHON_SCRIPT nicht gefunden${NC}"
    exit 1
fi

# Hauptmenü bei fehlenden Argumenten
if [ $# -eq 0 ]; then
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  🪙 Emercoin Coin Control Launcher${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Optionen:"
    echo "  1) Coin Control CLI starten"
    echo "  2) Dashboard starten"
    echo "  3) RPC-Test durchführen"
    echo "  4) Beenden"
    echo ""
    read -p "Wähle Option (1-4): " choice
    
    case $choice in
        1)
            echo -e "${GREEN}Starte Coin Control CLI...${NC}"
            python3 "$PYTHON_SCRIPT"
            ;;
        2)
            dashboard_script="$SCRIPT_DIR/emer-testchain_dashboard.py"
            if [ -f "$dashboard_script" ]; then
                echo -e "${GREEN}Starte Dashboard...${NC}"
                python3 "$dashboard_script"
            else
                echo -e "${RED}Fehler: Dashboard-Skript nicht gefunden${NC}"
                exit 1
            fi
            ;;
        3)
            echo -e "${BLUE}Führe RPC-Test durch...${NC}"
            python3 << 'EOF'
import requests
import json

RPC_USER = "emma"
RPC_PASS = "testnetemma"
RPC_URL = "http://127.0.0.1:16662"

payload = {
    "jsonrpc": "1.0",
    "id": "test",
    "method": "getbalance",
    "params": []
}

try:
    response = requests.post(
        RPC_URL,
        auth=(RPC_USER, RPC_PASS),
        json=payload,
        timeout=5
    )
    result = response.json()
    
    if "error" in result and result["error"]:
        print(f"❌ RPC Fehler: {result['error']}")
        exit(1)
    else:
        balance = result.get("result", 0)
        print(f"✅ Verbindung erfolgreich!")
        print(f"   Guthaben: {balance} EMC")
        exit(0)
except Exception as e:
    print(f"❌ Fehler: {e}")
    exit(1)
EOF
            ;;
        4)
            echo -e "${YELLOW}Beende Launcher${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Ungültige Auswahl${NC}"
            exit 1
            ;;
    esac
else
    # Direkt Coin Control CLI starten
    python3 "$PYTHON_SCRIPT" "$@"
fi
