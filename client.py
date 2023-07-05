import socket

SERVER_IP = '192.168.1.6'
SERVER_PORT = 5678


def send_message(message,s):

    s.sendall(message.encode())
    response = s.recv(1024)
    print(response.decode())


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))

    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        action = input("Are you signing up or logging in? (Type 'signup' or 'login'): ")

        message = f"{action},{username},{password}"
        send_message(message,s)