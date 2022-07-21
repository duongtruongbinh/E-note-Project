import socket
import LoginMenu
import ApplicationMenu


format = "utf8"

HOST = "10.123.0.169"
PORT = 50007

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverAddress = (HOST, PORT)


def main():
    client.connect(serverAddress)

    result, username = LoginMenu.Login(client)
    if result == True:
        # And go to E-note app
        ApplicationMenu.Menu(username, client)    
    client.send("Disconnect".encode(format))
    client.recv(1024).decode(format)


if __name__ == "__main__":
    main()
