import socket
from threading import Thread
import random

def find_free_port():
    """Находит свободный порт в диапазоне 50000-60000"""
    while True:
        port = random.randint(50000, 60000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('', port))
                return port
            except:
                continue

def handle_client(conn, addr):
    try:
        print(f"Подключен клиент: {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Получено: {data.decode()}")
            conn.sendall(b"OK")
    finally:
        conn.close()

def start_server():
    port = find_free_port()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen()

        print(f"Порт: {port}")

        while True:
            conn, addr = s.accept()
            Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == '__main__':
    start_server()
