import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS_SERVER = ('192.168.1.98', 5000)
request = ''

# open connection
sock.connect(ADDRESS_SERVER)

print("Enter a province code or type q to exit")
while True:
    # process input
    request = input('>> ')
    if request == 'q' or request == 'Q':
        print('<< Quitting...')
        break
    # send request
    sock.sendall(request.encode())
    # receive response
    response = sock.recv(32)
    # print response
    print('<< {}'.format(response.decode()))

# close connection
sock.close()