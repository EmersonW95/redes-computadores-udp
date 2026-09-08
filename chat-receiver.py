import socket
import random

HOST = '0.0.0.0'
PORT = 5001
DROP_RATE = 0.4  # 40% de perda simulada no canal


def run_chat_receiver():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"[Chat Server] Online na porta {PORT} (Drop Rate: {DROP_RATE * 100}%)...")

        while True:
            data, addr = s.recvfrom(1024)

            if random.random() < DROP_RATE:
                print("[CANAL] Pacote descartado artificialmente!")
                continue

            raw_message = data.decode('utf-8')

            # TODO 1: Fazer o split da mensagem delimitada por '|'
            parts = raw_message.split('|')

            # TODO 2: Verificar se a mensagem é do tipo 'MSG'
            if len(parts) < 3 or parts[0] != 'MSG':
                print(f"[AVISO] Mensagem em formato desconhecido: {raw_message}")
                continue

            # TODO 3: Extrair o ID da mensagem e o texto do usuário
            msg_id = parts[1]
            # Junta de volta caso o próprio conteúdo contenha o caractere '|'
            conteudo = '|'.join(parts[2:])

            # TODO 4: Exibir no terminal a mensagem recebida e o ID correspondente
            print(f"[RECEBIDO] ID {msg_id} de {addr}: {conteudo}")

            # TODO 5: Montar o pacote de recibo no formato 'DELIVERED|<ID>'
            receipt = f"DELIVERED|{msg_id}"

            # TODO 6: Enviar o recibo de volta para a origem usando s.sendto(..., addr)
            s.sendto(receipt.encode('utf-8'), addr)


if __name__ == '__main__':
    run_chat_receiver()