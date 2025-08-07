"""
 Reverse-SOCKS5-proxy-through-SSH-tunnel
 from https://github.com/Pengfei196/Reverse-SOCKS5-proxy-through-SSH-tunnel
"""

import socket
import threading

def start_tcp_client(host='127.0.0.1', port=8889):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"[+] Connected to the server {host}:{port}")
    return client_socket

def forward(source, destination):
    while True:
        data = source.recv(2048)
        if not data:
            destination.shutdown(socket.SHUT_WR)
            break
        destination.sendall(data)

def main(tunnel_client_socket, tunnel_host, tunnel_port, socks5_port):
    # Respond to remote requests and create new tunnel sockets for transfer
    while True:
        try:
            command = tunnel_client_socket.recv(100)
            if command == b'create a new socket':
                tunnel_client_socket.send(b'socket created')
                new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                new_socket.connect(('127.0.0.1', socks5_port))
                transfer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                transfer_socket.connect((tunnel_host, tunnel_port))
                threading.Thread(target=forward, args=(transfer_socket, new_socket)).start()
                threading.Thread(target=forward, args=(new_socket, transfer_socket)).start()
        except KeyboardInterrupt:
            print('Shutting down...')
            break

if __name__ == '__main__':
    tunnel_host = '127.0.0.1'
    tunnel_port = 8889
    socks5_port = 9050
    tunnel_client_socket = start_tcp_client(tunnel_host, tunnel_port)

    main(tunnel_client_socket, tunnel_host, tunnel_port, socks5_port)
