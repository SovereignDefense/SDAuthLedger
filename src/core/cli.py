import argparse
import os
import sys

# Garante que os módulos core possam ser importados
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from crypto import generate_key_pair, sign_data, verify_signature
from ledger import register_identity, is_key_active, load_ledger

# Diretório para salvar as chaves
KEY_DIR = 'keys'

def save_key(filename, content):
    """Função auxiliar para salvar conteúdo em arquivo."""
    os.makedirs(KEY_DIR, exist_ok=True)
    filepath = os.path.join(KEY_DIR, filename)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"🔑 Chave salva em: {filepath}")
    return filepath

def load_key(filepath):
    """Função auxiliar para carregar conteúdo de arquivo."""
    try:
        with open(filepath, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo de chave não encontrado em {filepath}")
        sys.exit(1)

def handle_generate(args):
    """Lógica para gerar um novo par de chaves (Identidade)."""
    print(f"\n--- Gerando Nova Identidade Criptográfica para: {args.id} ---")
    
    priv_key_hex, pub_key_hex = generate_key_pair()

    # Salva as chaves
    priv_filename = f"{args.id}.priv"
    pub_filename = f"{args.id}.pub"
    
    save_key(priv_filename, priv_key_hex)
    save_key(pub_filename, pub_key_hex)
    
    print("\n✅ Identidade Gerada com Sucesso.")
    print(f"   Chave Pública (compartilhável): {pub_key_hex[:16]}...")
    print(f"   Chave Privada (secreta): {priv_key_hex[:16]}...")

def handle_register(args):
    """Lógica para registrar uma chave pública no Ledger Simulado."""
    print(f"\n--- Registrando Chave Pública no SD-AuthLedger ---")
    
    # Carrega a chave pública do arquivo
    pub_key_hex = load_key(args.pubkey_file)
    
    success, message = register_identity(pub_key_hex, args.owner)
    
    if success:
        print(f"✅ Registro de {args.pubkey_file} SUCESSO. Proprietário: {args.owner}")
        print(f"   Registro: {message}")
    else:
        print(f"⚠️ Registro de {args.pubkey_file} FALHOU.")
        print(f"   Motivo: {message}")

def handle_sign(args):
    """Lógica para assinar uma mensagem/requisição com a chave privada."""
    print(f"\n--- Assinando Dados Criptograficamente ---")
    
    # Carrega a chave privada do arquivo
    priv_key_hex = load_key(args.privkey_file)
    
    signature = sign_data(priv_key_hex, args.data)
    
    print(f"📄 Dados a Assinar: '{args.data}'")
    print(f"✍️ Assinatura Gerada (HEX):")
    print(f"{signature}")
    print("\n⚠️  Esta assinatura deve ser verificada com a Chave Pública correspondente.")
    
    # Salva a assinatura para facilitar o teste de verificação
    sig_filename = "last_signature.txt"
    save_key(sig_filename, signature)


def handle_verify(args):
    """Lógica para verificar uma assinatura usando a chave pública e o Ledger."""
    print(f"\n--- Verificando Assinatura Contra o Ledger ---")
    
    # 1. Carrega as chaves e dados
    pub_key_hex = load_key(args.pubkey_file)
    
    # 2. Verifica o status da Chave Pública no Ledger (Soberania)
    if not is_key_active(pub_key_hex):
        print("🛑 FALHA NA AUTENTICAÇÃO: Chave Pública não está registrada ou foi revogada no Ledger.")
        sys.exit(1)

    print("☑️ Status da Chave no Ledger: ATIVA.")

    # 3. Verifica a Assinatura Criptograficamente
    is_valid = verify_signature(pub_key_hex, args.data, args.signature)
    
    print("-" * 40)
    if is_valid:
        print("✅ AUTENTICAÇÃO SUCESSO! Assinatura válida e Chave Ativa.")
    else:
        print("❌ AUTENTICAÇÃO FALHA! Assinatura inválida para os dados fornecidos.")
        sys.exit(1)


def handle_show_ledger(args):
    """Exibe o conteúdo atual do Ledger."""
    print("\n--- Conteúdo do SD-AuthLedger ---")
    ledger = load_ledger()
    if not ledger:
        print("O Ledger está vazio.")
        return
        
    for pub_key, record in ledger.items():
        print("-" * 30)
        print(f"🔑 Chave (Hash): {pub_key[:16]}...")
        print(f"  Proprietário: {record['owner']}")
        print(f"  Status: {record['status']}")
        print(f"  Registro: {record['timestamp']}")


def main():
    parser = argparse.ArgumentParser(
        description="SD-AuthLedger (Sovereign Defense - Authentication Ledger) CLI",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Cria os subparsers para os comandos
    subparsers = parser.add_subparsers(dest='command', required=True, help='Comando a ser executado')

    # --- Comando GENERATE ---
    parser_gen = subparsers.add_parser('generate', help='Gera um par de chaves (Identidade).')
    parser_gen.add_argument('--id', required=True, help='Nome da identidade (ex: servidor-bunker-01). As chaves serão salvas como <id>.pub e <id>.priv.')
    parser_gen.set_defaults(func=handle_generate)

    # --- Comando REGISTER ---
    parser_reg = subparsers.add_parser('register', help='Registra uma chave pública no Ledger.')
    parser_reg.add_argument('--pubkey-file', required=True, help='Caminho para o arquivo da Chave Pública (ex: keys/servidor-bunker-01.pub).')
    parser_reg.add_argument('--owner', required=True, help='Entidade proprietária da chave (ex: Comando-Geral).')
    parser_reg.set_defaults(func=handle_register)
    
    # --- Comando SIGN ---
    parser_sign = subparsers.add_parser('sign', help='Assina uma string de dados (requisição) com a chave privada.')
    parser_sign.add_argument('--privkey-file', required=True, help='Caminho para o arquivo da Chave Privada (ex: keys/servidor-bunker-01.priv).')
    parser_sign.add_argument('--data', required=True, help='A string de dados a ser assinada (ex: "GET /api/status").')
    parser_sign.set_defaults(func=handle_sign)

    # --- Comando VERIFY ---
    parser_verify = subparsers.add_parser('verify', help='Verifica uma assinatura usando a Chave Pública e o Ledger.')
    parser_verify.add_argument('--pubkey-file', required=True, help='Caminho para o arquivo da Chave Pública usada para verificação.')
    parser_verify.add_argument('--data', required=True, help='A string de dados original que foi assinada.')
    parser_verify.add_argument('--signature', required=True, help='A assinatura (em formato HEX) a ser verificada.')
    parser_verify.set_defaults(func=handle_verify)

    # --- Comando SHOW-LEDGER ---
    parser_show = subparsers.add_parser('show-ledger', help='Exibe o conteúdo atual do Livro-Razão (Ledger).')
    parser_show.set_defaults(func=handle_show_ledger)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()