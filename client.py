import socket

host = "127.0.1.1"
port = 8282

def main():
    s = socket.socket()
    s.connect((host, port))

    while True:
        msg = input("Client: ")
        s.sendall(bytes(msg, "utf8"))

        if msg == "quit":
            break

        response = s.recv(1024).decode("utf8")
        print("Server: ", response)

    s.close()


if __name__ == "__main__":
    main()