from multiprocessing import RLock
from posixpath import split, splitext
import socket
import threading
import json
import os
import time

CHUNK_SIZE = 1024 * 10


server_path = os.getcwd()

format = "utf8"

HOST = "10.126.2.104"
PORT = 50007


username_list = []

thread_list = []


def sign_in(username, password):
    with open("User/User.json", "r") as json_file:
        data = json.loads(json_file.read())
    length = len(data)
    i = 0
    while i < length:
        if data[i]["user_name"] == username:
            if data[i]["password"] == password:
                return True
            else:
                return False
        i += 1
    return False


def validate_name(name, password):
    with open("User/User.json", "r") as json_file:
        data = json.loads(json_file.read())
    length = len(data)
    i = 0
    while i < length:
        if data[i]["user_name"] == name:
            return False
        i += 1
    return True


def sign_up(name, password):
    if validate_name(name, password) == False:
        return False
    else:
        data = []
        with open("User/User.json", "r") as json_file:
            data = json.loads(json_file.read())

        data.append(dict([("user_name", name), ("password", password)]))
        with open("User/User.json", "w") as json_file:
            json.dump(data, json_file, indent=4)
        return True


def send_list_file(conn: socket, username):
    # Check folder exist if not create folder with username
    if os.path.isdir(f"{server_path}\ServerResource\{username}") == False:
        os.mkdir(f"{server_path}\ServerResource\{username}")
    os.chdir(f"ServerResource\{username}")

    # List all file has been saved
    list_of_file = os.listdir()
    os.chdir(server_path)

    # Send list file to client
    for i in list_of_file:
        conn.send(i.encode(format))
        conn.recv(1024).decode(format)
    conn.send("Stop".encode(format))
    conn.recv(1024).decode(format)


def receive_file(conn: socket):
    # Receive username and filename from client
    str = conn.recv(1024).decode(format)
    conn.send("Received USERNAME and FILE_NAME".encode(format))

    username = str.split(":")[0]
    file_name = str.split(":")[1]

    file_size = conn.recv(1024).decode(format)
    file_size = int(file_size)

    os.chdir(f"{server_path}\ServerResource\{username}")

    curr_size = 0

    # Write the data sent by client into file
    with open(file_name, "wb") as f:
        while True:
            data = conn.recv(CHUNK_SIZE)
            f.write(data)
            curr_size += len(data)
            if curr_size >= file_size:
                break

    os.chdir(server_path)


def send_file(conn: socket):
    # Receive username and filename from client
    mess = conn.recv(1024).decode(format)
    conn.send("Received USERNAME and FILE_NAME".encode(format))

    username = mess.split(":")[0]
    file_name = mess.split(":")[1]

    os.chdir(f"./ServerResource/{username}")

    # Get file size and send to server
    file_size = os.path.getsize(file_name)
    conn.send(str(file_size).encode(format))

    time.sleep(0.5)

    with open(file_name, "rb") as source_file:
        file_size = os.path.getsize(file_name)
        # +1 for the last chunk, if the file is divisible by CHUNK_SIZE, the last chunk will be empty
        n = file_size // CHUNK_SIZE + 1

        for i in range(n):
            conn.send(source_file.read(CHUNK_SIZE))

    os.chdir(server_path)


def handleClient(conn: socket, address, index):
    print(f"[NEW CONNECTION] {address} connected.")
    lock = RLock()

    # Verify login and sign up
    username = ""
    option = conn.recv(1024).decode(format)
    conn.send("x".encode(format))
    if option == "Disconnect":
        conn.close()
        print(f"{conn} closed")
        return

    if option == "SignIn":
        while True:
            username = conn.recv(1024).decode(format)
            conn.send("x".encode(format))

            if username == "SignIn" or username == "SignUp":
                username = conn.recv(1024).decode(format)
                conn.send("x".encode(format))
            password = conn.recv(1024).decode(format)
            conn.send("x".encode(format))

            # Check sign in and respond
            if sign_in(username, password):
                conn.send("True".encode(format))
                conn.recv(1024).decode(format)
                break
            else:
                conn.send("False".encode(format))
                conn.recv(1024).decode(format)

    else:
        while True:
            username = conn.recv(1024).decode(format)
            conn.send("x".encode(format))
            if username == "SignIn" or username == "SignUp":
                username = conn.recv(1024).decode(format)
                conn.send("x".encode(format))
            password = conn.recv(1024).decode(format)
            conn.send("x".encode(format))

            # Check sign up and respond
            if sign_up(username, password):
                conn.send("True".encode(format))
                conn.recv(1024).decode(format)
                break
            else:
                conn.send("False".encode(format))
                conn.recv(1024).decode(format)

    username_list.append(username)

    # Send list of files to client
    send_list_file(conn, username)

    while True:
        event = conn.recv(1024).decode(format)
        conn.send("x".encode(format))

        if event == "Disconnect":
            conn.close()
            print(f"{conn} closed")
            break

        if event == "Upload":
            receive_file(conn)

            # Save into file json
            temp_list = []

            for i in os.listdir(f"{server_path}/ServerResource/{username}"):
                temp_list.append(
                    dict(
                        [
                            ("name", i),
                            ("id", i.split(".")[0]),
                            ("path", f"{os.getcwd()}/{i}"),
                        ]
                    )
                )
            with open(f"./User/{username}.json", "w") as f:
                json.dump(temp_list, f, indent=4)

            # Respond to client
            conn.send("Received".encode(format))
            conn.recv(1024).decode(format)

            # Update list file
            send_list_file(conn, username)

        if event == "Download":
            send_file(conn)

            # Respond to client
            # conn.send("Sent".encode(format))
            # conn.recv(1024).decode(format)

        if event == "Open":
            send_file(conn)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    countClient = 0
    s.listen()

    print("==== SERVER ====")
    print("Server:", HOST, PORT)
    print("Waiting for client")

    while countClient < 5:
        conn, address = s.accept()

        thr = threading.Thread(target=handleClient,
                               args=(conn, address, countClient))
        thread_list.append(thr)

        thr.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

        countClient += 1
    for i in thread_list:
        i.join()

    print("Server closed")

    s.close()


if __name__ == "__main__":
    main()
