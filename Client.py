import socket
import LoginMenu
import ApplicationMenu
import PySimpleGUI as sg

format = "utf8"

HOST = "127.0.0.1"
PORT = 50007

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = (HOST, PORT)


def Connect():
    client.connect(serverAddress)
    layout = [
        [sg.Text("Client")],
        [sg.Text(f"[CONNECTED] Client connected to server at : {HOST} : {PORT}")],
        [sg.Button("OK", key="-OK-")],
    ]
    return sg.Window("Connecting", layout)



def main():
    #   Connect to server
    window = Connect()

    while True:
        event,value = window.read()

        if event == sg.WIN_CLOSED:
            window.close()
            break

        window.close()
        # If connect successfully go to login menu
        if event == "-OK-":
            result, username = LoginMenu.Login(client)
            if result == True:
                # And go to E-note app
                ApplicationMenu.Menu(username,client)
            break


if __name__ == "__main__":
    main()
