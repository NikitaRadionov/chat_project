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
        user_socket.sendall(register_request) # блокирующая функция
        response = user_socket.recv(4096).decode('utf-8') # блокирующая функция
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
        user_socket.sendall(get_active_users_request) # блокирующая функция
        active_users = user_socket.recv(4096)
        print(active_users.decode('utf-8'))
    except:
        print('Can\'t get active users')


def get_active_chats():
    try:
        get_active_chats_request ='get_active_chats'.encode('utf-8')
        user_socket.sendall(get_active_chats_request) # блокирующая функция
        active_chats = user_socket.recv(4096)
        print(active_chats.decode('utf-8'))
    except:
        print('Can\'t get active chats')


def create_chat(args):
    chat_name = args[0]
    try:
        create_chat_request = f'create_chat {chat_name}'.encode('utf-8') # блокирующая функция
        user_socket.sendall(create_chat_request)
        response = user_socket.recv(4096)
        print(response.decode('utf-8'))
    except:
        print('Can\'t create chat')


def open_chat(args):
    chat_name = args[0]
    try:
        open_chat_request = f'open_chat {chat_name}'.encode('utf-8') # блокирующая функция
        user_socket.sendall(open_chat_request)
        response = user_socket.recv(4096)
        print(response.decode('utf-8'))
    except:
        print('Can\'t open chat')


def send_in_chat(args):
    chat_name = args[0]
    message = ' '.join(args[1:]) if len(args) > 2 else args[1]
    try:
        send_in_chat_request = f'send_in_chat {chat_name} {message}'.encode('utf-8') # блокирующая функция
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


# base using:
# connect_to_server()
# register_user()
# get_active_users()
# chats_event_loop()
# end_programm()

# Пользователь может создать чат (create_chat), пользователь может подсоединиться к уже существующему чату (open_chat), пользователь может писать в чат (send_in_chat)



if __name__ == "__main__":
    run_client()









#свалка:

# Пока что реализуем такую схему:
# Диалог всегда начинает первый пользователь
# Первый пользователь написал, а затем он ждет ответа второго пользователя
# Второй пользователь написал, а затем он ждет ответа от первого пользователя
# И так далее






# tasks = []
# to_read = {}
# to_write = {}
# def start_chat_with(user_id):
#     user_socket.sendall(user_id.encode('utf-8')) # блокирующая функция
#     control_message = user_socket.recv(4096).decode('utf-8') # блокирующая функция
#     if control_message in ('yes', 'Yes'):
#         pass
#     else:
#         print(f'User {user_id} don\'t want chat with you')


# def chats_event_loop():

#     while any([tasks, to_read, to_write]):

#         while not tasks:

#             ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

#             for sock in ready_to_read:
#                 pass

#             for sock in ready_to_write:
#                 pass

#         task = tasks.pop(0)
#         next(task)