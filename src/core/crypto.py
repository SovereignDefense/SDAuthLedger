from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import os

# --- Geração de Chaves ---
def generate_key_pair():
    """Gera um par de chaves de assinatura (Ed25519)."""
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    # Retorna em formato Hex para fácil armazenamento em disco/ledger
    return signing_key.encode(HexEncoder).decode(), verify_key.encode(HexEncoder).decode()

# --- Assinatura de Dados ---
def sign_data(private_key_hex, data):
    """Assina os dados usando a chave privada (SigningKey)."""
    signing_key = SigningKey(private_key_hex, encoder=HexEncoder)
    # Assina a mensagem e retorna a assinatura em Hex
    signed = signing_key.sign(data.encode('utf-8'))
    return signed.signature.hex()

# --- Verificação de Assinatura ---
def verify_signature(public_key_hex, data, signature_hex):
    """Verifica a assinatura usando a chave pública (VerifyKey)."""
    try:
        verify_key = VerifyKey(public_key_hex, encoder=HexEncoder)
        signature_bytes = bytes.fromhex(signature_hex)
        # Tenta verificar: se falhar, levanta uma exceção
        verify_key.verify(data.encode('utf-8'), signature_bytes)
        return True
    except Exception as e:
        # Captura exceções de assinatura inválida ou chave inválida
        print(f"Erro de Verificação: {e}")
        return False