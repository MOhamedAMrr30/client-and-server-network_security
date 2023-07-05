import socket
import hashlib
import secrets

SERVER_IP = '192.168.1.6'
SERVER_PORT = 5678


def generate_salt():
    salt = secrets.token_hex(16)  # Generate a 16-byte (32-character) salt
    return salt

def hash_password(password, salt): #take password and salt as input 
    salted_password = password + salt
    hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
    return hashed_password

def store_user_info(username, hashed_password, salt, user_database):
    users = {'username': username, 'hashed_password': hashed_password, 'salt': salt}
    user_database.append(users)

def verify_password(username, password, user_database):
    for user_info in user_database:
        if user_info['username'] == username:
            stored_hashed_password = user_info['hashed_password']
            salt = user_info['salt']
            salted_password = password + salt
            hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
            return hashed_password == stored_hashed_password
    return False


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn, addr = s.accept()
    print('Connection accepted from: {addr}')

    user_database = []  # Initialize an empty user database

    # User sign-up process
    while True:
        data = conn.recv(1024)
        data = data.decode()
        action,username,password = data.split(',')

        if action == 'signup':
            salt = generate_salt()
            hashed_password = hash_password(password, salt)
            store_user_info(username, hashed_password, salt, user_database)# database bey store feha
            conn.send("SUCCESSFULLY SIGNEDUP,khoush ya aloot".encode())
        elif action == 'login':

            if verify_password(username, password, user_database):
                conn.send('Authentication successful. You are logged in.'.encode())
            else:
                conn.send('Authentication failed. Invalid username or password.'.encode())

            store_user_info(username, hashed_password, salt, user_database)