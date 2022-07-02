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


# try:
#     msg = None
#     while msg != "x":
#         msg = input("[CLIENT]: ").encode(format)
#         client.send(msg)
#         if msg.decode(format) == "send 2":
#             filename = input("Filename: ").encode(format)
#             client.send(filename)
#         else:
#             msg = client.recv(1024).decode(format)
#             print(f"[SERVER] {msg}")

#     print("End chat")

# except:
#     print("Error")
# finally:
#     client.close()
#     print("Client closed")


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
            result, username = LoginMenu.Login()
            if result == True:
                # And go to E-note app
                ApplicationMenu.Menu(username)
            break


if __name__ == "__main__":
    main()
