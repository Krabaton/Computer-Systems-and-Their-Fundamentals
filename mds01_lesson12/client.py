import socket


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        host = socket.gethostbyname(socket.gethostname())
        sock.connect((host, 8000))
        sock.send(b'Hello, world')
        data = sock.recv(1024)
        print('Received', repr(data))


if __name__ == '__main__':
    main()
