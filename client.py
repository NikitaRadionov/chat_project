import socket
from select import select

user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

user_id = ''


def connect_to_server():
    host, port = input('Please, enter server ip:port: ').split(':')
    print(f'Connecting to {host}:{port}...')
    try:
        user_socket.connect((host, int(port)))
    except:
        print(f'Can\'t connect to {host}:{port}')
        return None
    print(f'Success connection to {host}:{port}')
    print('Please use \'register_user\' for registering on server')


def register_user():
    global user_id
    input_id= input('please enter your name or 3 digits: ')
    try:
        register_request = f'register_user {input_id}'.encode('utf-8')
        user_socket.sendall(register_request)
        response = user_socket.recv(4096).decode('utf-8')
        print(response)
        if response == 'Success registration':
            user_id = input_id
            print('Use \'get_active_chats\' for getting available users for chat')
        else:
            print('Try choose another id')
    except:
        print('Can\'t register on server')


def get_active_users():
    try:
        get_active_users_request ='get_active_users'.encode('utf-8')
        user_socket.sendall(get_active_users_request)
        active_users = user_socket.recv(4096)
        print(active_users.decode('utf-8'))
    except:
        print('Can\'t get active users')


def get_active_chats():
    try:
        get_active_chats_request ='get_active_chats'.encode('utf-8')
        user_socket.sendall(get_active_chats_request)
        active_chats = user_socket.recv(4096)
        print(active_chats.decode('utf-8'))
    except:
        print('Can\'t get active chats')


def create_chat(args):
    chat_name = args[0]
    try:
        create_chat_request = f'create_chat {chat_name}'.encode('utf-8')
        user_socket.sendall(create_chat_request)
        response = user_socket.recv(4096)
        print(response.decode('utf-8'))
    except:
        print('Can\'t create chat')


def open_chat(args):
    chat_name = args[0]
    try:
        open_chat_request = f'open_chat {chat_name}'.encode('utf-8')
        user_socket.sendall(open_chat_request)
        response = user_socket.recv(4096)
        print(response.decode('utf-8'))
    except:
        print('Can\'t open chat')


def send_in_chat(args):
    chat_name = args[0]
    message = ' '.join(args[1:]) if len(args) > 2 else args[1]
    try:
        send_in_chat_request = f'send_in_chat {chat_name} {message}'.encode('utf-8')
        user_socket.sendall(send_in_chat_request)
        response = user_socket.recv(4096)
        print(response.decode('utf-8'))
    except:
        print('Can\'t send message in chat')


def helpme():
    print(', '.join(list(all_commands.keys())) )

all_commands = {
    'helpme': helpme,
    'connect_to_server': connect_to_server,
    'register_user': register_user,
    'get_active_chats': get_active_chats,
    'get_active_users': get_active_users,
    'create_chat': create_chat,
    'open_chat': open_chat,
    'send_in_chat': send_in_chat,
    'stop': 'stop'
}


def run_client():
    print('Welcome stranger')
    print('Enter \'helpme\' for getting all commands')

    while True:
        input_command = input()
        command, *arguments = input_command.split()

        if command in list(all_commands.keys()):
            if command == 'stop':
                break
            else:
                if arguments:
                    all_commands[command](arguments)
                else:
                    all_commands[command]()
        else:
            print('Undefined command. Use \'helpme\' for getting all commands')


if __name__ == "__main__":
    run_client()
