# 🛡️ SDAuthLedger (Sovereign Defense - Authentication Ledger)

![SDAuthLedger](img/banner1.jpg)


  [![SD-Organization](https://img.shields.io/badge/Organization-SovereignDefense-green.svg)](https://github.com/SovereignDefense)
  [![Language](https://img.shields.io/badge/Language-Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![Status](https://img.shields.io/badge/Status-Alpha%20Deployment-yellow.svg)](https://github.com/SovereignDefense/SDAuthLedger)
  [![Criptografia](https://img.shields.io/badge/Crypto-Ed25519_HSM_Ready-blue.svg?style=for-the-badge)](https://en.wikipedia.org/wiki/EdDSA)
  [![Pilar](https://img.shields.io/badge/Pilar-Soberania_Digital-darkgreen.svg?style=for-the-badge)](https://pt.wikipedia.org/wiki/Soberania_digital)
  [![License](https://img.shields.io/badge/License-Apache_2.0-red.svg)](LICENSE)


Categoria: Identidade/Autenticação Distribuída (Soberana)

O SDAuthLedger é um sistema de Prova de Conceito (PoC) leve e focado em algoritmos para demonstrar a Autenticação Descentralizada e Soberana baseada em criptografia de Chave Pública. Ele atua como um pilar de identidade para ecossistemas de defesa, como os protegidos pelo MKDCB e 5GTacticEdge, eliminando a dependência de provedores de identidade estrangeiros (GAFAM).

## 💡 Propósito Estratégico

1.  Soberania Digital: Promover a autonomia no gerenciamento de identidades críticas, garantindo que o ciclo de vida (criação, uso e revogação) da identidade permaneça dentro da jurisdição nacional.
2.  Garantia de Confiança: Assegurar que os sistemas críticos de infraestrutura (protegidos pelo MKDCB) sejam acessados apenas por entidades cuja identidade é criptograficamente verificada e registrada soberanamente no Ledger.
3.  Base Tecnológica: Criar um asset de código nacional focado em algoritmos de identidade, facilitando a auditoria e a evolução para soluções de identidade mais robustas (como DIDs ou VCs).

![SD-AuthLedger](img/banner2.jpg)

## ⚙️ MVP (Produto Mínimo Viável)

O MVP foca em 3 funcionalidades essenciais, utilizando pares de chaves Ed25519 (ou similar) para segurança e eficiência:

1.  Geração de Identidade: Criação de um par de chaves pública/privada.
2.  Registro no Ledger: Simulação do registro da Chave Pública no Ledger.
3.  Autenticação (Assinatura e Verificação): Assinatura de uma mensagem/requisição e verificação dessa assinatura usando a chave pública registrada.

![SD-AuthLedger](img/logo.jpg)

## 🛠️ Tecnologias-Chave

* **Linguagem:** Python 3.x
* **Criptografia:** Bibliotecas como `PyNaCl` (fácil de usar e moderna, baseada no NaCl) ou `cryptography` para gestão de chaves Ed25519 (ideal para assinaturas leves).
* **Ledger Simulado:** Um arquivo JSON ou um banco de dados SQLite leve para simular o registro imutável de chaves públicas e hashes de revogação.

## 📂 Estrutura de Pastas

| Pasta/Arquivo | Descrição |
| :--- | :--- |
| `src/core/crypto.py` | Lógica para gerar chaves, assinar dados e verificar assinaturas. O Coração Criptográfico. |
| `src/core/ledger.py` | Lógica para gerenciar o registro (adição e consulta) de identidades (Chaves Públicas). |
| `src/cli.py` | Interface de Linha de Comando para interagir com o MVP e demonstrar suas funcionalidades. |
| `keys/` | Pasta onde as chaves geradas são salvas. |
| `requirements.txt` | Lista as dependências do Python (ex: `pynacl`). |

## 🚀 Como Usar (Exemplo de Demonstração)

1.  Instalação: `pip install -r requirements.txt`
2.  Geração da Identidade: `python src/cli.py generate --id "servidor-bunker-01"`
3.  Registro no Ledger: `python src/cli.py register --pubkey-file "servidor-bunker-01.pub" --owner "Centro-Geral"`
4.  Autenticação (Assinar): `python src/cli.py sign --privkey-file "servidor-bunker-01.priv" --data "Acesso autorizado ao setor Alpha."`
5.  Verificação: `python src/cli.py verify --signature <sig> --pubkey "servidor-bunker-01.pub" --data "Acesso autorizado ao setor Alpha."`


## 🚀 Demonstração de Uso (Passo a Passo)

Certifique-se de que as dependências estão instaladas: `pip install pynacl`

1. 🔑 Geração da Identidade
Cria o par de chaves pública/privada que representa uma nova entidade soberana (ex: um servidor de perímetro).

```bash
python src/cli.py generate --id "servidor-bunker-01"
# Saída esperada:
# --- Gerando Nova Identidade Criptográfica para: servidor-bunker-01 ---
# 🔑 Chave salva em: keys/servidor-bunker-01.priv
# 🔑 Chave salva em: keys/servidor-bunker-01.pub
# ✅ Identidade Gerada com Sucesso.
```
2. 📝 Registro no Ledger (Ato de Soberania)
A chave pública é registrada no livro-razão soberano.

```bash
python src/cli.py register --pubkey-file "keys/servidor-bunker-01.pub" --owner "Centro-Geral-Defesa"
# Saída esperada:
# --- Registrando Chave Pública no SD-AuthLedger ---
# ✅ Registro de keys/servidor-bunker-01.pub SUCESSO. Proprietário: Centro-Geral-Defesa
```

3. ✍️ Assinatura (Requisição de Acesso)
A entidade (usando sua chave privada) assina uma requisição de dados.

```bash
# Definimos o dado que será assinado para provar a identidade e a intenção
DATA_TO_SIGN="GET /recursos/criticos?id=42" 

python src/cli.py sign --privkey-file "keys/servidor-bunker-01.priv" --data "$DATA_TO_SIGN"
# Saída (salva a assinatura em keys/last_signature.txt e a exibe):
# ✍️ Assinatura Gerada (HEX): <hash_longo_da_assinatura>
```

4. ✅ Verificação (Autenticação no Perímetro)
Um sistema de defesa (como o MKDCB) verifica a assinatura, garantindo a autenticidade criptográfica e o status soberano da chave no Ledger

```bash
# Captura a assinatura gerada no passo anterior
SIGNATURE=$(cat keys/last_signature.txt)

python src/cli.py verify --pubkey-file "keys/servidor-bunker-01.pub" --data "$DATA_TO_SIGN" --signature "$SIGNATURE"
# Saída esperada (SUCESSO):
# ☑️ Status da Chave no Ledger: ATIVA.
# ----------------------------------------
# ✅ AUTENTICAÇÃO SUCESSO! Assinatura válida e Chave Ativa.
```

5. 📖 Visualizar Ledger
Consulta rápida ao estado atual das identidades soberanas.

```bash
python src/cli.py show-ledger
# Saída:
# --- Conteúdo do SD-AuthLedger ---
# 🔑 Chave (Hash): <início_do_hash>...
#   Proprietário: Centro-Geral-Defesa
#   Status: active
#   Registro: <timestamp>
```
6. Como Rodar os Testes
Para iniciar os testes no terminal, dentro do diretório raiz do SDAuthLedger

```bash
python tests/test_crypto.py
```


## 🛡️ Licença

**Copyright (c) 2025 MATEUS SILVA DOS SANTOS**

Este projeto é totalmente Open Source e é regido pelos termos da **Apache License, Version 2.0**.

1.  **Exoneração Total de Responsabilidade (AS IS):** O software é fornecido sem garantias ou condições de qualquer tipo, protegendo o autor de processos por danos ou mau funcionamento.
2.  **Concessão de Patente Explícita:** Qualquer contribuidor concede uma licença de uso para as patentes que seu código possa conter, protegendo o projeto de litígios de Propriedade Intelectual (PI).

**Termos Completos:**
Consulte o arquivo [LICENSE](LICENSE) na raiz do repositório para os termos completos.

## 💻 Desenvolvido por

**MATEUS SILVA DOS SANTOS**

[![GitHub](https://camo.githubusercontent.com/17a3cfebe6cf2dcf7b339b7b008adb9a55ddc15aec622a27a2a66b207e1e357a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4769744875622d3130303030303f7374796c653d666f722d7468652d6261646765266c6f676f3d676974687562266c6f676f436f6c6f723d7768697465)](https://github.com/MateusWorkSpace)
