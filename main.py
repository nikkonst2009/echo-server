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
clients = {}  # словарь IP -> сокет

def handle_client(conn, ip):
    try:
        # Если клиенту отказано в доступе, закрываем соединение сразу
        if not verify_client(ip):
            conn.sendall(f"Отказано в доступе клиенту {ip}".encode("UTF-8"))
            conn.close()  # Закрываем соединение при отказе
            return

        print(f"Клиент {ip} есть в списке разрешенных IP-адресов")
        clients[ip] = conn

        # Отправляем историю чата новому клиенту
        print(f"Отправка истории сообщений клиенту {ip}")
        with open("messages.txt", "r") as file:
            history = file.read()
            if history != "":
                conn.sendall(history.encode("UTF-8"))
            else:
                conn.sendall("Список сообщений пуст. Напишите что-нибудь.\nGithub сервера: github.com/nikkonst2009/echo-server\nGithub мессенджера: github.com/nikkonst2009/echo-messenger".encode("UTF-8"))

        while True:
            data = conn.recv(1024)
            if not data:
                break

            decoded_data = data.decode()
            print(f"Новое расшифрованное сообщение от клиента {ip}\n* {decoded_data}")

            with open("messages.txt", "a") as messages_file:
                messages_file.write(decoded_data + "\n")
            print(f"Новое сообщение записано в файл истории сообщений")

            # Читаем историю один раз для всех клиентов
            with open("messages.txt", "r") as file:
                history = file.read()
            
            # Создаем копию словаря для безопасной итерации
            for client_ip, client_conn in list(clients.items()):
                try:
                    if history:
                        print(f"Отправка истории сообщений клиенту {client_ip}")
                        client_conn.sendall(history.encode("UTF-8"))
                except Exception as e:
                    print(f"Ошибка отправки клиенту {client_ip}: {str(e)}")
                    # Удаляем нерабочий сокет из словаря
                    client_conn.close()
                    del clients[client_ip]

    except Exception as e:
        print(f"Отключение клиента {ip} из-за ошибки: ", str(e))
    finally:
        # Гарантированно закрываем соединение и чистим словарь
        if ip in clients:
            clients[ip].close()
            del clients[ip]
        conn.close()  # Дополнительная страховка

def verify_client(ip):
    with open("allowed_ip_adresses.txt", "r") as f:
        ip_adresses_list = f.read().splitlines()
    return ip in ip_adresses_list

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
