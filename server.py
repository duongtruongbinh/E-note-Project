from posixpath import split, splitext
import socket
import threading
import json
import Transfer
import os

CHUNK_SIZE = 1024 * 10


server_path = os.getcwd()

format = "utf8"

HOST = "127.0.0.1"
PORT = 50007

option_list = ["Disconnect", "Upload", "Download", "View"]

username_list = []


def sign_in(username, password):
    with open("User/User.json", "r") as json_file:
        data = json.loads(json_file.read())
    length = len(data)
    i = 0
    while i < length:
        if data[i]["user_name"] == username:
            if data[i]["password"] == password:
                return True
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
    os.chdir("..")
    os.chdir("..")

    # Send list file to client
    for i in list_of_file:
        conn.send(i.encode(format))
        conn.recv(1024).decode(format)
    conn.send("Stop".encode(format))
    conn.recv(1024).decode(format)


def receive_file(conn: socket):
    # Receive username and filename from client
    username = conn.recv(1024).decode(format)
    conn.send("x".encode(format))
    file_name = conn.recv(1024).decode(format)
    conn.send("x".encode(format))

    os.chdir(f"{server_path}\ServerResource\{username}")

    # Write the data sent by client into file
    with open(file_name, "wb") as f:
        while True:
            data = conn.recv(Transfer.CHUNK_SIZE)
            conn.send("x".encode(format))
            if data == b"Stop":
                break
            f.write(data)

    os.chdir(server_path)
    return file_name


def handleClient(conn: socket, address, index):
    print(f"[NEW CONNECTION] {address} connected.")

    # Verify login and sign up
    username = ""
    option = conn.recv(1024).decode(format)
    conn.send("x".encode(format))

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
                break
            else:
                conn.send("False".encode(format))
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
                break
            else:
                conn.send("False".encode(format))

    username_list.append(username)

    # Send list of files to client
    send_list_file(conn, username)

    while True:
        option = conn.recv(1024).decode(format)
        conn.send("x".encode(format))

        if option == "Disconnect":
            conn.close()
            break
        if option == "Upload":
            receive_file(conn)
            os.chdir(f"{os.getcwd()}/User")
            # Save into file json
            temp_list = []
            with open(f"{username}.json") as f:
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
            with open(f"{username}.json", "w") as f:
                json.dump(temp_list, f, indent=4)

            os.chdir(server_path)
            # Respond to client
            conn.send("Received".encode(format))

            send_list_file(conn, username)


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
        thr = threading.Thread(target=handleClient, args=(conn, address, countClient))
        thr.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

        countClient += 1

    print("Server closed")
    # input()
    s.close()


if __name__ == "__main__":
    main()
