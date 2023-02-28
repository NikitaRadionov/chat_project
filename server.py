import socket
from select import select

active_users = []
active_chats = []

tasks = []
to_read = {}
to_write = {}


class User:

    def __init__(self, socket_bridge, id):
        self.socket = socket_bridge
        self.id = id # имя человека либо три цифры
        # self.type = type


    def __str__(self):
        return str(self.id)


    __repr__ = __str__


class Chat:

    def __init__(self, name):
        self.name = name
        self.conversation = []


    def get_conversation(self):
        response = '\n'.join(self.conversation)
        response = 'Chat is empty' if response == '' else response
        return response

    def __str__(self):
        return str(self.name)

    __repr__ = __str__


# commands:

def register_user(client_socket, args):

    user_id = args[0]
    for user in active_users:
        if user.id == user_id:
            return 'User already exist'
    active_users.append(User(client_socket, user_id))
    return 'Success registration'


def get_active_users(client_socket, args):
    response = ', '.join(map(str, active_users))
    response = 'No active users' if response == '' else response
    return response


def get_active_chats(client_socket, args):
    response = ', '.join(map(str, active_chats))
    response = 'No active chats' if response == '' else response
    return response


def create_chat(client_socket, args):
    chat_name = args[0]
    for chat in active_chats:
        if chat_name == chat.name:
            return 'Chat already exist'
    active_chats.append(Chat(chat_name))
    return 'Chat have successfully created'



def open_chat(client_socket, args):
    chat_name = args[0]
    for chat in active_chats:
        if chat.name == chat_name:
            target_chat = chat
    conversation = target_chat.get_conversation()
    return conversation


def send_in_chat(client_socket, args):
    chat_name = args[0]
    message = ' '.join(args[1:]) if len(args) > 2 else args[1]
    for chat in active_chats:
        if chat.name == chat_name:
            target_chat = chat
    for user in active_users:
        if user.socket is client_socket:
            user_id = user.id
    target_chat.conversation.append(f'{user_id}: {message}')
    conversation = target_chat.get_conversation()
    return conversation


all_commands = {
    'register_user': register_user,
    'get_active_chats': get_active_chats,
    'get_active_users': get_active_users,
    'create_chat': create_chat,
    'open_chat': open_chat,
    'send_in_chat': send_in_chat,
}


# kernel functions:

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(4)

    while True:
        yield ('read', server_socket)
        client_socket, address = server_socket.accept()
        tasks.append(client(client_socket))


def client(client_socket):

    while True:
        yield ('read', client_socket)
        request = client_socket.recv(4096).decode('utf-8')
        if not request:
            break
        else:
            command, *arguments = request.split()
            response = all_commands[command](client_socket, arguments)
            yield ('write', client_socket)
            client_socket.sendall(response.encode('utf-8'))

    client_socket.close()


# kernel

def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:

            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:

            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task

            if reason == 'write':
                to_write[sock] = task

        except StopIteration:
            pass

        

if __name__ == '__main__':
    tasks.append(server())
    event_loop()
