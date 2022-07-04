import socket
import LoginMenu
import ApplicationMenu
import PySimpleGUI as sg

format = "utf8"

HOST = "127.0.0.1"
PORT = 50007

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = (HOST, PORT)


def main():
    client.connect(serverAddress)
    
    result, username = LoginMenu.Login(client)
    if result == True:
        # And go to E-note app
        ApplicationMenu.Menu(username,client)
    


if __name__ == "__main__":
    main()
