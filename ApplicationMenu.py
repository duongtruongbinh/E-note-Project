import socket
import PySimpleGUI as sg
import Transfer as tf
import os
import LoginMenu
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

format = "utf8"

client_path = os.getcwd()

CHUNK_SIZE = 1024 * 10  # 10KB


def send_file(conn: socket, username, source_file_name):
    # Send username and filename to server
    conn.send(username.encode(format))
    temp1 = conn.recv(1024).decode(format)
    conn.send(source_file_name.encode(format))
    temp2 = conn.recv(1024).decode(format)

    os.chdir(client_path + "\Resource")

    with open(source_file_name, "rb") as source_file:
        file_size = os.path.getsize(source_file_name)
        # +1 for the last chunk, if the file is divisible by CHUNK_SIZE, the last chunk will be empty
        n = file_size // CHUNK_SIZE + 1

        for i in range(n):
            conn.send(source_file.read(CHUNK_SIZE))
            conn.recv(1024).decode(format)
        conn.send("Stop".encode(format))
        conn.recv(1024).decode(format)

    os.chdir("..")


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
                key="-Notename-",
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
        [
            sg.Button("Save", key="-Save-", expand_x=True),
            sg.Button("Open", key="-Open-", expand_x=True),
            sg.Button("Delete", key="-Delete-", expand_x=True),
        ],
    ]

    download_layout = [
        [sg.Text("Select a file to download:")],
        [
            sg.Listbox(
                values=list_of_file,
                size=(30, 10),
                key="-FileList-",
                no_scrollbar=True,
                expand_y=True,
                expand_x=True,
            )
        ],
        [sg.Button("Download", key="-Download-", expand_x=True)],
    ]

    upload_layout = [
        [sg.Text("Select a file to upload:")],
        [sg.Input(expand_x=True, expand_y=True), sg.FileBrowse(key="-FileBrowse-")],
        [sg.Button("Upload", expand_x=True)],
    ]

    layout = [
        [
            sg.TabGroup(
                [
                    [sg.Tab("Note", note_layout)],
                    [sg.Tab("Download", download_layout)],
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
        if event == sg.WIN_CLOSED or event == "Exit":
            conn.send("Disconnect".encode(format))
            break

        if event == "-Save-":
            # Get the note name and node text
            note_name = window["-Notename-"].get()
            note_text = window["-Text-"].get()
            # Save the note to resource folder
            with open(f"Resource/{note_name}.txt", "w") as f:
                f.write(note_text)

            conn.send("Upload".encode(format))
            conn.recv(1024).decode(format)

            send_file(conn, username, f"{note_name}.txt")

            if conn.recv(1024).decode(format) == "Received":
                sg.popup("Save file successfully")

            list_of_file = receive_list_file(conn)
            window["-FileList-"].update(values=list_of_file)
            # window.close()
            # window = MainMenu(username, conn)

        if event == "-Open-":
            # Show all the txt file in local and server
            # list_of_file = .GetListOfNotes()
            sg.popup("Open")

        if event == "-Download-":
            # Tell server to send file to this client
            file_name = window["-FileList-"].get()
            tf.SendFile(file_name)
            # Get the file from server
            tf.ReceiveFile(file_name)
            # Open the file

        if event == "-Upload-":
            # Get the file name
            file_name = window["-FileBrowse-"].get()
            # Send the file to server
            tf.SendFile(file_name)
            # Get the file from server
    window.close()
