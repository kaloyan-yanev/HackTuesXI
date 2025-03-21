import socket
import json

server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)  # RFCOMM specific protocol
server.bind(("4C:34:88:E4:C5:B3", 4))  # MAC Address and Channel 4
server.listen(1)

print("Waiting for connection...")

client, addr = server.accept()
print(f"Accepted connection from {addr}")

try:
    while True:
        data = client.recv(1024)
        if not data:
            break

        print(f"Received: {data.decode('utf-8')}")
        id = "A803"
        temperature = 21
        humidity = 53
        message = json.dumps({'id': id , 'a_t': temperature, 'a_h':humidity})
        client.send(message.encode('utf-8'))
except OSError:
    pass

print("Disconnected")

client.close()
server.close()