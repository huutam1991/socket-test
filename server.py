import socket
import selectors
import client

host = ""
port = 8282

def get_ip():
    try:
        hostname = socket.gethostname()
        IP = socket.gethostbyname(hostname)
    except Exception:
        IP = '127.3.3.1'

    return IP

def initSelectors(server):
    sel = selectors.DefaultSelector()
    sel.register(server, selectors.EVENT_READ, data = None)

    return sel

def initConnection(server, sel):
    client, address = server.accept()
    print("Get connection from: ", address)

    sel.register(client, selectors.EVENT_READ | selectors.EVENT_WRITE, data = '')

def checkClientMessage(client, mask, sel):
    clientSocket = client.fileobj
    data = client.data

    if mask & selectors.EVENT_READ:
        msg = clientSocket.recv(1024).decode("utf8")
        print("Client: ", msg)

        if msg == 'quit':
            clientSocket.close()
            sel.unregister(clientSocket)
            return

        data += msg

    if mask & selectors.EVENT_WRITE:
        if data != '':
            response = 'Server response: ' + data
            clientSocket.sendall(bytes(response, "utf8"))
            print(response)

            data = ''
        

def main():
    print("Host name: ", get_ip())

    print(type(client.main))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    server.setblocking(False)

    sel = initSelectors(server)

    while True:

        events = sel.select(timeout = None)

        for data, mask in events:
            if (data.data is None):
                initConnection(data.fileobj, sel)
            else:
                checkClientMessage(data, mask, sel)

    server.close()

if __name__ == "__main__":
    main()