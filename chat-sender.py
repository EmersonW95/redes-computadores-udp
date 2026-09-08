import socket
import threading

TARGET_IP = '127.0.0.1'
PORT = 5001

pending_messages = {}
msg_counter = 1
lock = threading.Lock()


def listen_receipts(sock):
    while True:
        try:
            data, _ = sock.recvfrom(1024)
            raw = data.decode('utf-8')

            # TODO 1: Parsing do recibo
            parts = raw.split('|')

            # TODO 2: Checar se é 'DELIVERED'
            if len(parts) < 2 or parts[0] != 'DELIVERED':
                continue

            # TODO 3: Extrair o ID
            msg_id = int(parts[1])

            # TODO 4: Remover de pending_messages e exibir confirmação
            with lock:
                if msg_id in pending_messages:
                    texto = pending_messages.pop(msg_id)
                    print(f"\n[Entregue ✓ Azul] ID {msg_id}: \"{texto}\" confirmado pelo destinatário.")
        except Exception:
            break


def run_chat_sender():
    global msg_counter
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        listener = threading.Thread(target=listen_receipts, args=(s,), daemon=True)
        listener.start()

        while True:
            try:
                user_input = input("Digite uma mensagem: ").strip()
                if not user_input:
                    continue

                if user_input == "/status":
                    # TODO 5: Exibir mensagens pendentes
                    with lock:
                        if not pending_messages:
                            print("[STATUS] Nenhuma mensagem pendente. Todas confirmadas.")
                        else:
                            print(f"[STATUS] {len(pending_messages)} mensagem(ns) pendente(s):")
                            for pid, texto in pending_messages.items():
                                print(f"  [Pendente ○ Cinza] ID {pid}: \"{texto}\"")
                    continue

                if user_input == "/reenviar":
                    # TODO 6: Reenviar mensagens pendentes
                    with lock:
                        if not pending_messages:
                            print("[REENVIAR] Nenhuma mensagem pendente para reenviar.")
                        else:
                            for pid, texto in list(pending_messages.items()):
                                packet = f"MSG|{pid}|{texto}"
                                s.sendto(packet.encode('utf-8'), (TARGET_IP, PORT))
                                print(f"[REENVIADO] ID {pid}: \"{texto}\"")
                    continue

                # TODO 7 a 10: Cadastrar mensagem, enviar MSG|<ID>|<TXT> e exibir status
                with lock:
                    current_id = msg_counter
                    msg_counter += 1
                    pending_messages[current_id] = user_input

                packet = f"MSG|{current_id}|{user_input}"
                s.sendto(packet.encode('utf-8'), (TARGET_IP, PORT))
                print(f"[Pendente ○ Cinza] ID {current_id} enviado, aguardando confirmação...")

            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    run_chat_sender()