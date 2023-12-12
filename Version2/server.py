import socket
import json
from datetime import datetime

s = socket.socket()         
s.bind(('0.0.0.0', 8090))
s.listen(0)                 

while True:
    client, addr = s.accept()

    data_buffer = b''  # Buffer to store incomplete data between recv calls

    while True:
        content = client.recv(4096)

        if len(content) == 0:
            break

        data_buffer += content

        print("Received data length:", len(content))

        while b'\n' in data_buffer:
            json_str, data_buffer = data_buffer.split(b'\n', 1)
            
            try:
                data = json.loads(json_str.decode('utf-8'))
                print("Received data:")
                print("SSID:", data.get("SSID"))
                print("BSSID:", data.get("BSSID"))
                print("RSSI:", data.get("RSSI"))
                print("Channel:", data.get("Channel"))
                print("Encryption:", data.get("Encryption"))

                # Append data to a file with timestamp
                with open('received_data.txt', 'a') as file:
                    file.write(f"{datetime.now()} - {json.dumps(data)}\n")

            except json.JSONDecodeError as e:
                print("Error decoding JSON:", e)

    print("Closing connection")
    client.close()
