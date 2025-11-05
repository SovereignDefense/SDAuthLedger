import unittest
import os
import sys

# Ajusta o path para importar os módulos core
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/core'))

from crypto import generate_key_pair, sign_data, verify_signature
from ledger import register_identity, is_key_active, LEDGER_FILE

class TestSDAuthLedger(unittest.TestCase):
    
    # --- Configuração de Testes ---
    @classmethod
    def setUpClass(cls):
        """Prepara o ambiente de teste: remove o ledger file se existir."""
        if os.path.exists(LEDGER_FILE):
            os.remove(LEDGER_FILE)

    def setUp(self):
        """Executado antes de cada teste: gera um novo par de chaves para cada teste."""
        self.priv_key, self.pub_key = generate_key_pair()
        self.data = "Esta é uma mensagem de teste para o SD-AuthLedger."
    
    def tearDown(self):
        """Executado após cada teste: Limpa o ledger entre testes, se necessário."""
        # Para testes de ledger mais isolados, poderíamos re-inicializar o LEDGER_FILE aqui
        pass

    # --- Testes de Criptografia (crypto.py) ---
    
    def test_01_generate_key_pair(self):
        """Verifica se a geração de chaves cria chaves válidas (hex string e tamanho)."""
        # Verifica se as chaves são strings não vazias
        self.assertTrue(isinstance(self.priv_key, str))
        self.assertTrue(isinstance(self.pub_key, str))
        
        # Ed25519 em Hex: Chave privada = 64 caracteres (32 bytes * 2); Chave pública = 64 caracteres
        # O PyNaCl em HexEncoder retorna 64 bytes (128 caracteres) para a Chave Privada,
        # que é a chave de assinatura + a chave de verificação. Vamos checar apenas o não-vazio.
        self.assertGreater(len(self.priv_key), 64) 
        self.assertEqual(len(self.pub_key), 64) # Chave pública é sempre 32 bytes (64 hex)

    def test_02_sign_and_verify_success(self):
        """Testa o ciclo completo de assinatura e verificação com dados corretos."""
        signature = sign_data(self.priv_key, self.data)
        
        # 1. Verifica se a assinatura foi gerada
        self.assertTrue(isinstance(signature, str))
        self.assertGreater(len(signature), 0)

        # 2. Verifica se a verificação é bem-sucedida
        is_valid = verify_signature(self.pub_key, self.data, signature)
        self.assertTrue(is_valid, "A assinatura válida falhou na verificação.")

    def test_03_verify_failure_tampered_data(self):
        """Testa falha na verificação quando os dados são alterados."""
        signature = sign_data(self.priv_key, self.data)
        tampered_data = "Esta é uma mensagem de teste TAMPERADA."
        
        is_valid = verify_signature(self.pub_key, tampered_data, signature)
        self.assertFalse(is_valid, "A verificação deve falhar com dados adulterados.")

    def test_04_verify_failure_wrong_key(self):
        """Testa falha na verificação com a chave pública errada."""
        _, wrong_pub_key = generate_key_pair() # Gera uma chave pública diferente
        signature = sign_data(self.priv_key, self.data)
        
        is_valid = verify_signature(wrong_pub_key, self.data, signature)
        self.assertFalse(is_valid, "A verificação deve falhar com a chave pública errada.")

    # --- Testes de Ledger (ledger.py) ---
    
    def test_05_register_and_check_identity(self):
        """Testa o registro e a consulta de status no Ledger."""
        # Inicialmente, a chave NÃO deve estar ativa
        self.assertFalse(is_key_active(self.pub_key), "A chave não deveria estar ativa antes do registro.")
        
        # 1. Registra a identidade
        success, message = register_identity(self.pub_key, "Unidade de Teste A")
        self.assertTrue(success, "O registro da identidade falhou.")
        
        # 2. Verifica se a chave está ativa após o registro
        self.assertTrue(is_key_active(self.pub_key), "A chave deveria estar ativa após o registro.")
        
    def test_06_re_register_failure(self):
        """Testa se o registro falha ao tentar registrar a mesma chave duas vezes."""
        # Garante que a chave foi registrada no teste anterior (ou registra agora)
        register_identity(self.pub_key, "Unidade de Teste B")
        
        # Tenta registrar novamente
        success, message = register_identity(self.pub_key, "Unidade de Teste B - Tenta Novamente")
        
        self.assertFalse(success, "O re-registro da mesma chave deve falhar.")
        self.assertIn("já registrada", message, "A mensagem de erro deve indicar re-registro.")


if __name__ == '__main__':
    # Roda os testes usando a linha de comando
    unittest.main(argv=['first-arg-is-ignored'], exit=False)