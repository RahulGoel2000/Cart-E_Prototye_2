import pandas as pd
from flask import Flask, request
# import pandas as pd

app = Flask(__name__)
count=0
x=100
y=100

# List of MAC addresses to consider
mac_addresses = ['20:9C:B4:09:25:80', '20:9C:B4:09:25:81', '20:9C:B4:09:25:82', '44:12:44:0F:50:80', '44:12:44:0F:50:81', '44:12:44:0F:50:82', 'E8:26:89:37:BD:80', 'E8:26:89:37:BD:81', 'E8:26:89:37:BD:82', '44:12:44:10:69:60', '44:12:44:10:69:61', '44:12:44:10:69:62', '44:12:44:10:74:A0', '44:12:44:10:74:A1', '44:12:44:10:74:A2', '44:12:44:10:06:20', '44:12:44:10:06:21', '44:12:44:10:06:22', '44:12:44:0F:8B:C0', '44:12:44:0F:8B:C1', '44:12:44:0F:8B:C2', 'CC:88:C7:10:A4:40', 'CC:88:C7:10:A4:41', 'CC:88:C7:10:A4:42', '44:12:44:0F:A4:40', '44:12:44:0F:A4:41', '44:12:44:0F:A4:42', '44:12:44:10:60:E0', '44:12:44:10:60:E1', '44:12:44:10:60:E2', 'E8:26:89:37:EB:C0', 'E8:26:89:37:EB:C1', 'E8:26:89:37:EB:C2', 'CC:88:C7:10:6A:20', 'CC:88:C7:10:6A:21', 'CC:88:C7:10:6A:22', '44:12:44:10:72:00', '44:12:44:10:72:01', '44:12:44:10:72:02', '44:12:44:0F:92:C0', '44:12:44:0F:92:C1', '44:12:44:0F:92:C2', '44:12:44:10:80:80', '44:12:44:10:80:81', '44:12:44:10:80:82']

def parse_data(data):
    parsed_data = {"device_id": "", "networks": []}
    lines = data.strip().split("\n")
    parsed_data["device_id"] = lines[0]
    if len(lines) > 1:
        for line in lines[1:]:
            if "MAC:" in line:
                parts = line.split(",")
                if len(parts) >= 1:
                    mac_address = parts[0].split(": ")[1]
                    if mac_address in mac_addresses:
                        strength = int(parts[1].split(": ")[1].replace("%", ""))
                        parsed_data["networks"].append((mac_address, strength))
    return parsed_data


def append_to_excel(data, file_name):
    global x,y
    print("x:",x)
    print("y:",y)
    try:
        df = pd.read_excel(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["x", "y"] + mac_addresses)
    

    
    # Create a new row with zeros
    new_row = [x, y] + [0] * len(mac_addresses)

    
    
    # Update strengths if MAC address exists in data
    for mac, strength in data["networks"]:
        try:
            index = mac_addresses.index(mac)
            new_row[index + 2] = strength  # Offset by 2 to account for 'x' and 'y' columns
        except ValueError:
            # MAC address not found, skip it
            pass
    print(new_row)
    new_df = pd.DataFrame([new_row], columns=df.columns)
    df = pd.concat([df, new_df], ignore_index=True)
    
    df.to_excel(file_name, index=False)



@app.route('/data', methods=['POST'])
def receive_data():
    global count
    global x,y
    if count==20:
        count=0
    if count==0:
        x = int(input("Enter x coordinate: "))
        y = int(input("Enter y coordinate: "))
    data = request.data.decode('utf-8')  # Decode the received data
    print("Received data:")
    print(data)
    print(count)
    count=count+1
    parsed_data = parse_data(data)
    append_to_excel(parsed_data, "router_data_3.xlsx")
    # Process the received data as needed
    # For example, you can save it to a file, store it in a database, or perform any other operation.
    return 'Data received successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Run the server on port 80




