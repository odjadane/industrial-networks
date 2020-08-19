import socket, json, logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# DATA
with open('data.json', encoding='utf-8') as f:
    provinces = json.load(f)

# Create a TCP/IP socket and bind it
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDRESS_SERVER = ('192.168.1.98', 5000)
sock.bind(ADDRESS_SERVER)

# Listen for incoming connections
sock.listen(1)

while True:
    # waiting
    connection, address_client = sock.accept()

    while True:
        # receiving
        data = connection.recv(8)
        logging.info("{} sent \"{}\"".format(address_client, data.decode()))
        if data:
            # processing
            code = data.decode()
            response = provinces.get(code, 'INVALID CODE')
            # send back result
            connection.sendall(response.encode())
            logging.info("\"{}\" sent back to {}".format(response, address_client))
        else:
            break
    # Close connection
    connection.close()