from flask import Flask, request
import pandas as pd

app = Flask(__name__)



# Read the Excel file
df = pd.read_csv('data.csv')

# Convert DataFrame to dictionary
mac_id_dict = df.set_index('Mac Address').to_dict()['SS ID']

print(len(list(mac_id_dict.keys())))


def parse_data(data):
    parsed_data = {"device_id": "", "networks": []}
    lines = data.strip().split("\n")
    parsed_data["device_id"] = lines[0]
    if len(lines) > 1:
        for line in lines[1:]:
            if "MAC:" in line:
                parts = line.split(",")
                mac_address = parts[0].split(": ")[1]
                strength = int(parts[1].split(": ")[1].replace("%", ""))
                parsed_data["networks"].append({"mac_address": mac_address, "strength": strength})
    return parsed_data

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')  # Decode the received data
    print("Received data:")
    print(data)
    # Process the received data as needed
    # For example, you can save it to a file, store it in a database, or perform any other operation.
    return 'Data received successfully'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Run the server on port 80
