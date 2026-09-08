# Chat via UDP — Confirmação de Entrega e Reenvio Manual

Serviço simplificado de mensagens instantâneas sobre UDP (`SOCK_DGRAM`), com
confirmação de entrega e retransmissão implementadas na camada de aplicação.
O canal simula perda artificial de pacotes (`DROP_RATE = 0.4`), exigindo que
o cliente controle suas próprias pendências.

## Arquivos

- `chat-receiver.py` — servidor: recebe mensagens, descarta ~40% delas
  artificialmente e confirma as demais com `DELIVERED|<ID>`.
- `chat-sender.py` — cliente: envia mensagens com ID sequencial, escuta
  confirmações em uma thread separada e permite consultar/reenviar pendências.
- 📄 **Documentação em PDF**: [Clique aqui para acessar](documentacao/pratica_transporte___UDP_.pdf)

## Como executar

Em dois terminais separados:

```bash
# Terminal 1
python3 chat-receiver.py

# Terminal 2
python3 chat-sender.py
```

## Protocolo

- Mensagem: `MSG|<ID>|<CONTEUDO>`
- Recibo de entrega: `DELIVERED|<ID>`

## Comandos do cliente

| Comando      | Ação                                                        |
|--------------|-------------------------------------------------------------|
| `/status`    | Lista as mensagens ainda pendentes de confirmação           |
| `/reenviar`  | Reenvia todas as mensagens que continuam pendentes          |

## Requisitos

Python 3, sem dependências externas.
