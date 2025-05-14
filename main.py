import socket
from threading import Thread
import random
from os.path import exists

def find_free_port():
    while True:
        port = random.randint(50000, 60000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except:
                continue

port = find_free_port()
clients = {} # словарь IP -> сокет

def handle_client(conn, ip):
    try:
        # Если клиенту отказано в доступе, то игнорируем клиента
        if not verify_client(ip):
            conn.sendall(f"Отказано в доступе клиенту {ip}".encode("UTF-8"))
            return

        print(f"Сокет сервера: Клиент {ip} есть в списке разрешенных IP-адресов")
        clients[ip] = conn

        # Отправляем историю чата новому клиенту
        print(f"Сокет сервера: Отправка истории сообщений клиенту {ip}")
        with open("messages.txt", "r") as file:
            history = file.read()
            if history:
                conn.sendall(history.encode("UTF-8"))

        while True:
            data = conn.recv(1024)
            if not data:
                break

            decoded_data = data.decode()
            print(f"Сокет сервера: Новое расшифрованное сообщение от клиента {ip}\n* {decoded_data}")

            messages_file = open("messages.txt", "a")
            messages_file.write(decoded_data + "\n")
            messages_file.close()
            print(f"Компьютер: Новое сообщение записано в файл истории сообщений")

            print(f"Сокет сервера: Отправка сообщений всем клиентам")
            for ip in clients:
                with open("messages.txt", "r") as file:
                    history = file.read()
                    if history:
                        print(f"Сокет клиента {ip}: Отправка истории сообщений клиенту {ip}")
                        clients[ip].sendall(history.encode("UTF-8"))


    except Exception as e:
        print(f"Отключение клиента {ip} из-за ошибки: ", str(e))

    clients[ip].close()
    del clients[ip]

def verify_client(ip):
    # Проверяем, от какого IP-адреса идет запрос до обработки и отправки данных
    ip_adresses_list = open("allowed_ip_adresses.txt", "r").read().split(sep="\n")
    is_ip_valid = ip in ip_adresses_list

    if not is_ip_valid:
        print(f"Неудачное подключение к серверу: Отказано в доступе клиенту {ip}")
        return False
    else:
        return True

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen()

        print(f"Порт: {port}")

        while True:
            conn, addr = s.accept()
            Thread(target=handle_client, daemon=True, args=(conn, addr[0])).start()

if __name__ == '__main__':
    start_server()
