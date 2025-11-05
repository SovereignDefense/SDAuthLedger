import json
import os
from datetime import datetime

LEDGER_FILE = 'ledger_data.json'

def load_ledger():
    """Carrega o ledger de um arquivo JSON (simulação de registro)."""
    if os.path.exists(LEDGER_FILE):
        with open(LEDGER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_ledger(ledger):
    """Salva o ledger no arquivo JSON."""
    with open(LEDGER_FILE, 'w') as f:
        json.dump(ledger, f, indent=4)

def register_identity(public_key_hex, owner):
    """Registra uma nova identidade (Chave Pública) no ledger."""
    ledger = load_ledger()
    if public_key_hex in ledger:
        return False, "Identidade já registrada."

    # Estrutura do 'bloco' do ledger
    ledger[public_key_hex] = {
        "owner": owner,
        "timestamp": datetime.now().isoformat(),
        "status": "active"
        # Em uma versão real: campo 'hash_revogacao'
    }
    save_ledger(ledger)
    return True, "Identidade registrada com sucesso."

def is_key_active(public_key_hex):
    """Verifica se uma Chave Pública está ativa no ledger."""
    ledger = load_ledger()
    identity_record = ledger.get(public_key_hex)
    return identity_record is not None and identity_record.get("status") == "active"