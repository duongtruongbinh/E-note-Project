from operator import truediv
import socket
import threading
import Transfer


format = "utf8"

HOST = "127.0.0.1"
PORT = 50007


def handleClient(conn: socket, address):
    print(f"[NEW CONNECTION] {address} connected.")
    msg = None
    while msg != "x":
        msg = conn.recv(1024).decode(format)

        print(f"[{address}] {msg}")
        if msg == "x":
            continue
        if msg == "send 2":
            filename = conn.recv(1024).decode(format)
            Transfer.split_file(filename)
            Transfer.merge_file(filename)

        msg = input(f"[{address}]: ").encode(format)
        conn.send(msg)

    conn.send("x".encode(format))
    print(conn.getsockname(), "closed")


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
        thr = threading.Thread(target=handleClient, args=(conn, address))
        # thr.daemon = True
        thr.start()
        
        print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

        countClient += 1
        

    print("Server closed")
    # input()
    s.close()


if __name__ == "__main__":
    main()
