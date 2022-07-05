from socket import socket
import PySimpleGUI as sg
import json

format = "utf8"

sg.theme("DarkAmber")  # Add a touch of color
# All the stuff inside your window.

PASSWORD_FORM = "Have at least six digits, at least one upper-case letter"


def LoginMenu():

    layout = [
        [sg.Text("Username: ")],
        [sg.InputText(key="-Username-")],
        [sg.Text("Password: ")],
        [sg.Text("Wrong Password", visible=False, key="-WrongPassword-")],
        [
            sg.InputText(key="-Password-", password_char="*", tooltip=PASSWORD_FORM),
            sg.Button("Show", key="-Show-", size=(5)),
        ],
        [sg.Button("Login"), sg.Button("Sign Up"), sg.Button("Cancel")],
    ]

    return sg.Window("Login", layout, resizable=True)


def SignUpMenu():
    layout = [
        [sg.Text("Username: ")],
        [sg.InputText(key="-Username-")],
        [sg.Text("Password: ")],
        [sg.Text(f"{PASSWORD_FORM}", visible=False, key="-WrongPassword-")],
        [sg.InputText(key="-Password1-", password_char="*", tooltip=PASSWORD_FORM)],
        [sg.Text("Retype password: ")],
        [sg.Text("Unmatch Password", visible=False, key="-Unmatch-")],
        [sg.InputText(key="-Password2-", password_char="*", tooltip=PASSWORD_FORM)],
        [sg.Button("Confirm"), sg.Button("Cancel")],
    ]

    return sg.Window("Sign Up", layout, resizable=True)


def Login(conn: socket):
    window = LoginMenu()

    while True:
        event, value = window.read()

        if event in (sg.WIN_CLOSED, "Cancel"):
            window.close()
            return (False, "")

        if event == "Login":
            username = window["-Username-"].get()
            password = window["-Password-"].get()

            # Check password is in the correct format
            if len(password) < 6 or not any(c.isupper() for c in password):
                window["-WrongPassword-"].update(visible=True)
                window["-WrongPassword-"].update(
                    value="Password is not in the correct format"
                )
                continue

            conn.send("SignIn".encode(format))
            conn.recv(1024).decode(format)
            # Send username and password to server
            conn.send(username.encode(format))
            conn.recv(1024).decode(format)
            conn.send(password.encode(format))
            conn.recv(1024).decode(format)

            # Server respond
            if conn.recv(1024).decode(format) == "True":
                sg.popup("Login Success")
                window.close()
                return (True, username)

            else:
                sg.popup("Login Failed")
                continue

        if event == "-Show-":
            if window["-Show-"].get_text() == "Show":
                window["-Password-"].update(password_char="")
                window["-Show-"].update("Hide")
            else:
                window["-Password-"].update(password_char="*")
                window["-Show-"].update("Show")

        if event == "Sign Up":
            window.close()
            window = SignUpMenu()

        if event == "Confirm":
            username = window["-Username-"].get()
            password_one = window["-Password1-"].get()

            if len(password_one) < 6 or not any(c.isupper() for c in password_one):
                window["-WrongPassword-"].update(visible=True)
                continue

            password_two = window["-Password2-"].get()

            if password_one != password_two:
                window["-Unmatch-"].update(visible=True)
                continue

            conn.send("SignUp".encode(format))
            conn.recv(1024).decode(format)
            # Send username and password to server
            conn.send(username.encode(format))
            conn.recv(1024).decode(format)
            conn.send(password_one.encode(format))
            conn.recv(1024).decode(format)

            # Server respond
            if conn.recv(1024).decode(format) == "True":
                sg.popup("Sign Up Success")
                window.close()
                return (True, username)
            else:
                sg.popup("Sign Up Fail")
                window.close()
                window = SignUpMenu()

    window.close()
    return True
