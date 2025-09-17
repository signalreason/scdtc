#!/usr/bin/env python3
import socket, threading

# Sierra's DTC server (inside VM)
DTC_HOST = "127.0.0.1"
DTC_PORT = 11099

# Proxy server (listens inside VM for mac clients)
PROXY_HOST = "0.0.0.0"
PROXY_PORT = 12000   # pick any open port

def pipe(src, dst):
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    finally:
        src.close()
        dst.close()

def handle_client(client_sock):
    # Connect to Sierra's local DTC
    dtc_sock = socket.create_connection((DTC_HOST, DTC_PORT))
    # Two pipes: client→DTC, DTC→client
    threading.Thread(target=pipe, args=(client_sock, dtc_sock), daemon=True).start()
    threading.Thread(target=pipe, args=(dtc_sock, client_sock), daemon=True).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((PROXY_HOST, PROXY_PORT))
    server.listen(5)
    print(f"Proxy listening on {PROXY_HOST}:{PROXY_PORT}")
    while True:
        client_sock, addr = server.accept()
        print("Client connected:", addr)
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    main()
