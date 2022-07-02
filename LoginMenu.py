from operator import imod
import PySimpleGUI as sg
import json


sg.theme("DarkAmber")  # Add a touch of color
# All the stuff inside your window.

PASSWORD_FORM = "Have at least six digits, at least one upper-case letter"


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


def Login():
    window = LoginMenu()

    while True:
        event, value = window.read()

        if event == sg.WIN_CLOSED or event == "Cancel":
            window.close()
            return False

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

            if sign_in(username, password):
                sg.popup("Login Success")
                return (True, username)

            else:
                sg.popup("Login Failed")
                window.close()
                window = LoginMenu()
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

            if sign_up(username, str(password_one)):
                sg.popup("Sign Up Success")
                break
            else:
                sg.popup("Sign Up Fail")
                window.close()
                window = SignUpMenu()

    window.close()
    return True
