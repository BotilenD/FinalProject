import socket
import tkinter as tk
from tkinter import filedialog, messagebox

# הגדרת כתובת השרת
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5001

# יצירת סוקט לקוח
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

# פונקציות GUI
def upload_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        filename = filepath.split("/")[-1]
        client_socket.send("upload".encode())
        client_socket.send(filename.encode())
        with open(filepath, 'rb') as f:
            while True:
                bytes_read = f.read(4096)
                if not bytes_read:
                    break
                client_socket.send(bytes_read)
        messagebox.showinfo("הודעה", f"File {filename} uploaded successfully!")

def download_file():
    filename = filename_entry.get()
    if filename:
        client_socket.send("download".encode())
        client_socket.send(filename.encode())
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=filename)
        if filepath:
            with open(filepath, 'wb') as f:
                while True:
                    bytes_read = client_socket.recv(4096)
                    if not bytes_read or "not found" in bytes_read.decode():
                        break
                    f.write(bytes_read)
            messagebox.showinfo("הודעה", f"File {filename} downloaded successfully!")

def list_files():
    client_socket.send("list".encode())
    files = client_socket.recv(4096).decode()
    files_list.delete(0, tk.END)
    for file in files.split("\n"):
        files_list.insert(tk.END, file)

# הגדרת GUI ב-Tkinter
root = tk.Tk()
root.title("מנהל אחסון קבצים")

upload_button = tk.Button(root, text="העלאת קובץ", command=upload_file)
upload_button.pack(pady=10)

filename_entry = tk.Entry(root)
filename_entry.pack(pady=10)

download_button = tk.Button(root, text="הורדת קובץ", command=download_file)
download_button.pack(pady=10)

list_button = tk.Button(root, text="רשימת קבצים", command=list_files)
list_button.pack(pady=10)

files_list = tk.Listbox(root, width=50)
files_list.pack(pady=10)

# הפעלת הלולאה של Tkinter
root.mainloop()
