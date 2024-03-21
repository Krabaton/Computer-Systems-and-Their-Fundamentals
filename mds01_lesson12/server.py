import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        host = socket.gethostbyname(socket.gethostname())
        print(host)
        sock.bind((host, 8000))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            with conn:
                print('Connected by', addr)
                data = conn.recv(1024).decode()
                if not data:
                    continue
                print('Received', repr(data))
                conn.send(data.encode())


if __name__ == '__main__':
    main()
