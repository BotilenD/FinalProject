import socket
import threading
import os

# הגדרת תיקיית אחסון קבצים
STORAGE_DIR = 'server_storage'

# יצירת תיקיית אחסון אם לא קיימת
if not os.path.exists(STORAGE_DIR):
    os.makedirs(STORAGE_DIR)

# הגדרת השרת
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001

# יצירת סוקט TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# רשימה לאחסון כל החיבורים
clients = []

def handle_client(client_socket):
    while True:
        try:
            # קבלת הפקודה מהלקוח
            command = client_socket.recv(1024).decode()
            if command.lower() == 'upload':
                filename = client_socket.recv(1024).decode()
                with open(os.path.join(STORAGE_DIR, filename), 'wb') as f:
                    while True:
                        bytes_read = client_socket.recv(4096)
                        if not bytes_read:
                            break
                        f.write(bytes_read)
                print(f"[+] File {filename} uploaded successfully.")
                client_socket.send(f"File {filename} uploaded successfully.".encode())
            elif command.lower() == 'download':
                filename = client_socket.recv(1024).decode()
                if os.path.exists(os.path.join(STORAGE_DIR, filename)):
                    client_socket.send(f"File {filename} found.".encode())
                    with open(os.path.join(STORAGE_DIR, filename), 'rb') as f:
                        while True:
                            bytes_read = f.read(4096)
                            if not bytes_read:
                                break
                            client_socket.send(bytes_read)
                else:
                    client_socket.send("File not found.".encode())
            elif command.lower() == 'list':
                files = os.listdir(STORAGE_DIR)
                files_list = "\n".join(files)
                client_socket.send(files_list.encode())
            else:
                client_socket.send("Invalid command.".encode())
        except:
            client_socket.close()
            return

# קבלה וניהול חיבורים חדשים
def receive_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"[+] {client_address} connected.")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket,)).start()

# הפעלת קבלת החיבורים
receive_connections()
