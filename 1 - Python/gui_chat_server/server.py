"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

actions = {
    "message": int(1).to_bytes(1, byteorder="big", signed=False),
    "client_list": int(2).to_bytes(1, byteorder="big", signed=False),
}

client_actions = {
    "exit": int(0).to_bytes(1, byteorder="big", signed=False),
    "name": int(1).to_bytes(1, byteorder="big", signed=False),
    "send": int(2).to_bytes(1, byteorder="big", signed=False),
    "send_to": int(3).to_bytes(1, byteorder="big", signed=False),
}


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        send_message(client, "Nhập tên của bạn!")
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def send_message(client, string, prefix=""):
    client.send(actions["message"])
    message_bytes = bytes(prefix + string, "utf8")
    message_length = len(message_bytes)
    client.send(int(message_length).to_bytes(4, byteorder="big", signed=False))
    client.send(message_bytes)


def broadcast(string, prefix=""):
    for client in clients:
        send_message(client, string, prefix)


def update_client_list():
    client_names = list(clients.values())
    for client in clients:
        client.send(actions["client_list"])
        client_length = len(client_names)
        client.send(int(client_length).to_bytes(4, byteorder="big", signed=False))
        for name in client_names:
            name_bytes = bytes(name, "utf8")
            name_length = len(name_bytes)
            client.send(int(name_length).to_bytes(4, byteorder="big", signed=False))
            client.send(name_bytes)


def handle_client(client):
    while True:
        action = client.recv(1)
        if action == client_actions["exit"]:
            name = clients[client]
            del clients_by_name[name]
            del clients[client]
            client.close()
            update_client_list()
            broadcast(name + " đã rời khỏi phòng chat!")
            break
        elif action == client_actions["name"]:
            name_length = int.from_bytes(client.recv(4), byteorder="big", signed=False)
            name = client.recv(name_length).decode("utf8")
            if client in clients:
                send_message(client, "Bạn đã đăng nhập rồi!", "error: ")
                continue
            if name in clients_by_name:
                send_message(client, "Tên đã tồn tại!", "error: ")
                continue

            clients_by_name[name] = client
            clients[client] = name
            update_client_list()
            broadcast(name + " đã tham gia phòng chat!")
        elif action == client_actions["send"]:
            message_length = int.from_bytes(client.recv(4), byteorder="big", signed=False)
            msg = client.recv(message_length).decode("utf8")
            if clients[client] is None:
                send_message(client, "Bạn chưa đăng nhập!", "error: ")
                continue
            broadcast(msg, clients[client] + ": ")
        elif action == client_actions["send_to"]:
            name_length = int.from_bytes(client.recv(4), byteorder="big", signed=False)
            name = client.recv(name_length).decode("utf8")
            message_length = int.from_bytes(client.recv(4), byteorder="big", signed=False)
            msg = client.recv(message_length).decode("utf8")
            if name not in clients_by_name:
                client.send(bytes("Không tìm thấy người dùng!", "utf8"))
                continue

            prefix = clients[client] + " -> " + name + ": "
            send_message(clients_by_name[name], msg, prefix)
            send_message(client, msg, prefix)
        else:
            print("Không rõ hành động của client")
            client.close()
            name = clients[client]
            del clients_by_name[name]
            del clients[client]
            break


clients_by_name = {}
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Chờ kết nối từ các client...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
