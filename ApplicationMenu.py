import subprocess
import socket
import PySimpleGUI as sg
import os
from ctypes import windll
import shutil
import time

windll.shcore.SetProcessDpiAwareness(1)

format = "utf8"

client_path = os.getcwd()

CHUNK_SIZE = 1024 * 10  # 10KB


def send_file(conn: socket, username, source_file_name):
    # Send username and filename to server
    mess = username + ":" + source_file_name
    conn.send(mess.encode(format))
    conn.recv(1024).decode(format)

    os.chdir(client_path + "\Resource")

    # Get file size and send it to server
    file_size = os.path.getsize(source_file_name)
    conn.send(str(file_size).encode(format))

    time.sleep(0.5)

    with open(source_file_name, "rb") as source_file:
        file_size = os.path.getsize(source_file_name)
        # +1 for the last chunk, if the file is divisible by CHUNK_SIZE, the last chunk will be empty
        n = file_size // CHUNK_SIZE + 1

        for i in range(n):
            conn.send(source_file.read(CHUNK_SIZE))

    os.chdir("..")


def receive_file(conn: socket, username, file_name):
    # Send username and filename to server
    mess = username + ":" + file_name
    conn.send(mess.encode(format))
    conn.recv(1024).decode(format)

    file_size = conn.recv(1024).decode(format)
    file_size = int(file_size)

    curr_size = 0   # Current size of file

    with open(f"./Resource/{file_name}", "wb") as f:
        while True:
            data = conn.recv(CHUNK_SIZE)
            f.write(data)
            curr_size += len(data)
            if curr_size >= file_size:
                break


def receive_list_file(conn: socket):
    list_of_file = []
    while True:
        file_name = conn.recv(1024).decode(format)
        conn.send("x".encode(format))  # Receive and send one by one
        if file_name == "Stop":
            break
        else:
            list_of_file.append(file_name)
    return list_of_file


def MainMenu(username, conn: socket):
    sg.theme("DarkAmber")  # Add a touch of color
    # All the stuff inside your window.

    # Server send list of files

    list_of_file = receive_list_file(conn)

    note_layout = [
        [
            sg.Input(
                default_text="Untitled",
                key="-NoteName-",
                enable_events=True,
                expand_x=True,
            )
        ],
        [
            sg.Multiline(
                default_text="Write your note here",
                size=(30, 10),
                key="-Text-",
                autoscroll=True,
                no_scrollbar=True,
                expand_y=True,
                expand_x=True,
            )
        ],
        [sg.Button("Save", key="-Save-", expand_x=True)],
    ]

    open_layout = [
        [sg.Text("Select a file:")],
        [
            sg.Listbox(
                values=list_of_file,
                size=(30, 10),
                key="-FileList-",
                select_mode="single",
                no_scrollbar=True,
                expand_y=True,
                expand_x=True,
            )
        ],
        [
            sg.Button("Download", key="-Download-", expand_x=True),
            sg.Button("Open", key="-Open-", expand_x=True),
        ],
    ]

    upload_layout = [
        [sg.Text("Select a file to upload:")],
        [
            sg.InputText(key="-FilePath-", expand_x=False, expand_y=False),
            sg.FileBrowse(key="-FileBrowse-", initial_folder=client_path),
        ],
        [sg.Button("Upload", key="-Upload-", expand_x=True)],
    ]

    layout = [
        [
            sg.TabGroup(
                [
                    [sg.Tab("Note", note_layout)],
                    [sg.Tab("Open", open_layout)],
                    [sg.Tab("Upload", upload_layout)],
                ],
                key="-TabGroup-",
                expand_x=True,
                expand_y=True,
            )
        ]
    ]

    return sg.Window("E-Note", layout, resizable=True)


def Menu(username, conn: socket):

    window = MainMenu(username, conn)

    # Initialize the value list for later use
    value = []

    while True:
        event, value = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-Save-":
            # Get the note name and note text
            note_name = window["-NoteName-"].get()
            note_text = window["-Text-"].get()
            # Save the note to resource folder
            with open(f"Resource/{note_name}.txt", "w") as f:
                f.write(note_text)

            conn.send("Upload".encode(format))
            conn.recv(1024).decode(format)

            send_file(conn, username, f"{note_name}.txt")

            # Server respond
            if conn.recv(1024).decode(format) == "Received":
                sg.popup("Save file successfully")

            # Update new list file
            list_of_file = receive_list_file(conn)
            window["-FileList-"].update(values=list_of_file)

        if event == "-Open-":
            file_name = window["-FileList-"].get()[0]

            conn.send("Download".encode(format))
            conn.recv(1024).decode(format)

            receive_file(conn, username, file_name)

            # If the file is txt, open it in app window
            # validation = conn.recv(1024).decode(format)
            # conn.send("x".encode(format))
            if file_name.split(".")[1] == "txt":
                window["-NoteName-"].update(file_name.split(".")[0])
                with open(f"./Resource/{file_name}", "r") as f:
                    data = f.read()
                    window["-Text-"].update(data)
            else:
                cmd = f"{os.getcwd()}/Resource/{file_name}"
                subprocess.run(cmd, shell=True)

        if event == "-Download-":
            file_name = window["-FileList-"].get()[0]

            conn.send("Download".encode(format))
            conn.recv(1024).decode(format)

            receive_file(conn, username, file_name)

            # Server respond
            validation = conn.recv(1024).decode(format)
            conn.send("x".encode(format))
            if validation == "Sent":
                sg.popup("Download File Successfully")

        if event == "-Upload-":
            # Get the file path and file name
            file_path = window["-FilePath-"].get()
            file_name = file_path.split("/")[-1]

            # Copy file to folder Resource
            delete = True
            if os.path.exists(f"./Resource/{file_name}"):
                delete = False
            shutil.copyfile(file_path, f"./Resource/{file_name}")

            conn.send("Upload".encode(format))
            conn.recv(1024).decode(format)
            # Send the file to server
            send_file(conn, username, file_name)

            if delete == True:
                os.remove(f"./Resource/{file_name}")

            # Server respond
            conn.recv(1024).decode(format)
            conn.send("x".encode(format))

            sg.popup("Save file successfully")

            # Update new list file
            list_of_file = receive_list_file(conn)
            window["-FileList-"].update(values=list_of_file)

    window.close()
