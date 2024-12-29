import tkinter
from tkinter import ttk, messagebox
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

# Ket noi toi server
HOST = '127.0.0.1'
PORT = 33000
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

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

client_name = None


def receive():
    while True:
        action = client_socket.recv(1)
        print(action)
        if action == actions["message"]:
            message_length = int.from_bytes(client_socket.recv(4), byteorder="big", signed=False)
            msg = client_socket.recv(message_length).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        elif action == actions["client_list"]:
            client_list_length = int.from_bytes(client_socket.recv(4), byteorder="big", signed=False)
            client_list = []
            for i in range(client_list_length):
                name_length = int.from_bytes(client_socket.recv(4), byteorder="big", signed=False)
                name = client_socket.recv(name_length).decode("utf8")
                if name == client_name:
                    continue
                client_list.append(name)
            message_type_combobox["values"] = ["All"] + client_list
        else:
            print("Không rõ hành động của server")
            break


def send(event=None):
    msg = my_msg.get()
    if not msg or not msg.strip():
        messagebox.showerror("Lỗi", "Không thể gửi tin nhắn trống")
        return

    my_msg.set("")
    if msg == "{quit}":
        client_socket.send(client_actions["exit"])
        client_socket.close()
        top.quit()
    else:
        global client_name
        if not client_name:
            if msg == "All":
                messagebox.showerror("Lỗi", "Tên không thể là All")
                return
            client_socket.send(client_actions["name"])
            client_socket.send(len(msg).to_bytes(4, byteorder="big", signed=False))
            client_socket.send(bytes(msg, "utf8"))
            client_name = msg
        elif message_type.get() != "All":
            client_socket.send(client_actions["send_to"])
            client_socket.send(len(message_type.get()).to_bytes(4, byteorder="big", signed=False))
            client_socket.send(bytes(message_type.get(), "utf8"))
            client_socket.send(len(msg).to_bytes(4, byteorder="big", signed=False))
            client_socket.send(bytes(msg, "utf8"))
        else:
            client_socket.send(client_actions["send"])
            client_socket.send(len(msg).to_bytes(4, byteorder="big", signed=False))
            client_socket.send(bytes(msg, "utf8"))



def on_closing(event=None):
    my_msg.set("{quit}")
    send()


top = tkinter.Tk()
top.title("Chatter")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

message_type = tkinter.StringVar()
message_type.set("All")
message_type_combobox = ttk.Combobox(top, textvariable=message_type, values=["All"])
message_type_combobox.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Gửi", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()
