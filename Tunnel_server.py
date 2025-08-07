import socket
import threading

def forward(source, destination):
    while True:
        data = source.recv(2048)
        if not data:
            destination.shutdown(socket.SHUT_WR)
            break
        destination.sendall(data)

class PseudoSocks5Server:
    def __init__(self, local_port=9000, tunnel_host='0.0.0.0', tunnel_port=8889):
        self.local_port = local_port
        self.tunnel_host = tunnel_host
        self.tunnel_port = tunnel_port
        self.running = False

    def start(self):
        self.running = True

        # waiting for a tunnel connection
        tunnel_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tunnel_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Prevent port occupation
        tunnel_sock.bind((self.tunnel_host, self.tunnel_port))
        tunnel_sock.listen(5)
        print(f"[*] Server startup, listening {self.tunnel_host}:{self.tunnel_port}")
        tunnel_sock_client, client_addr = tunnel_sock.accept()
        print(f"[+] Accept the connection from {client_addr}")
        
        try:
            while self.running:
                try:
                    while True:
                        # Listening a port for socks5 app
                        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        server_sock.bind(('0.0.0.0', self.local_port))
                        server_sock.listen(5)
                        print(f'Socks5 client listening on port {self.local_port}')
                        client_sock, addr = server_sock.accept()
                        print(f'Accepted connection from {addr}')
                        tunnel_sock_client.send(b'create a new socket')
                        response = tunnel_sock_client.recv(100)
                        if response == b'socket created':
                            tunnel_transfer_sock_client, client_addr = tunnel_sock.accept()
                        threading.Thread(target=forward, args=(client_sock, tunnel_transfer_sock_client)).start()
                        threading.Thread(target=forward, args=(tunnel_transfer_sock_client, client_sock)).start()
                except KeyboardInterrupt:
                    print('Shutting down...')
                    self.running = False
                except Exception as e:
                    print(f'Server error: {e}')
        
        finally:
            server_sock.close()
            tunnel_sock.close()
            self.running = False


if __name__ == '__main__':
    # local_port: the pseudo socks5 server listening port which provide supply for application in local machine
    # tunnel_host & tunnel_port: use to establish tunnel connection
    socks5_server = PseudoSocks5Server(local_port=9000, tunnel_host='0.0.0.0', tunnel_port=8889)
    socks5_server.start()
