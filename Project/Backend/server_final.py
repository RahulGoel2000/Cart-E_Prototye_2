from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
# import random
import pandas as pd
from flask import Flask, request
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.utils import shuffle
import json

# Load the data
data = pd.read_excel("router_data_3.xlsx")

# Shuffle the data
data_shuffled = shuffle(data, random_state=42)

# Split data into features (signal strengths) and labels (x and y coordinates)
X = data_shuffled.drop(columns=["x", "y","z"])
# y = data_shuffled[["x", "y"]]
y = data_shuffled[["x", "y", "z"]]

# Normalize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the KNN model on the entire dataset
k = 3  # Number of neighbors
knn = KNeighborsRegressor(n_neighbors=k)
knn.fit(X_scaled, y)

# Take a contiguous subset of the data for testing
subset_size = 100  # Size of the subset
X_subset = X.iloc[:subset_size]
y_subset = y.iloc[:subset_size]



# Normalize the subset features
X_subset_scaled = scaler.transform(X_subset)

# Make predictions on the subset
y_subset_pred = knn.predict(X_subset_scaled)

# Evaluate the model
mse_subset = mean_squared_error(y_subset, y_subset_pred)
print("Mean Squared Error on Subset:", mse_subset)

# import matplotlib.pyplot as plt
# import numpy as np

# # Calculate errors
# errors = np.sqrt((y_subset_pred[:,0] - y_subset.values[:,0])**2 + (y_subset_pred[:,1] - y_subset.values[:,1])**2)

# # Plot error distribution
# plt.figure(figsize=(8, 6))
# plt.hist(errors, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
# plt.xlabel('Error')
# plt.ylabel('Frequency')
# plt.title('Distribution of Prediction Errors')
# plt.grid(True)
# plt.show()

# # Calculate accuracy
# accuracy = np.mean(errors)
# print("Average Prediction Error:", accuracy)

# import matplotlib.pyplot as plt
# import numpy as np

# # Calculate errors
# errors = np.sqrt((y_subset_pred[:,0] - y_subset.values[:,0])**2 + (y_subset_pred[:,1] - y_subset.values[:,1])**2)

# # Plot error distribution
# plt.figure(figsize=(8, 6))
# plt.hist(errors, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
# plt.xlabel('Error')
# plt.ylabel('Frequency')
# plt.title('Distribution of Prediction Errors')
# plt.grid(True)

# # Calculate accuracy
# accuracy = np.mean(errors)
# plt.text(0.7, 0.9, f'Average Prediction Error: {accuracy:.7f}', transform=plt.gca().transAxes, fontsize=12, verticalalignment='top', bbox=dict(facecolor='white', alpha=0.5))

# plt.show()



app = Flask(__name__)
socketio = SocketIO(app)

positions = {}

# Function to continuously update positions and send them over WebSocket
def update_positions():
    global positions
    while True:
        socketio.emit('positions', positions)  # Send positions over WebSocket
        print(('positions', positions))
        time.sleep(0.03)  # Adjust the frequency of updates as needed

# # Start the thread to update positions
# update_thread = threading.Thread(target=update_positions)
# update_thread.daemon = True
# update_thread.start()

@app.route('/floor2')
def floor2():
    return render_template('Visualise1.html')

@app.route('/floor3')
def floor3():
    return render_template('Visualise2.html')


count=0
x=100
y=100

# List of MAC addresses to consider
mac_addresses = ['20:9C:B4:09:25:80', '20:9C:B4:09:25:81', '20:9C:B4:09:25:82', '44:12:44:0F:50:80', '44:12:44:0F:50:81', '44:12:44:0F:50:82', 'E8:26:89:37:BD:80', 'E8:26:89:37:BD:81', 'E8:26:89:37:BD:82', '44:12:44:10:69:60', '44:12:44:10:69:61', '44:12:44:10:69:62', '44:12:44:10:74:A0', '44:12:44:10:74:A1', '44:12:44:10:74:A2', '44:12:44:10:06:20', '44:12:44:10:06:21', '44:12:44:10:06:22', '44:12:44:0F:8B:C0', '44:12:44:0F:8B:C1', '44:12:44:0F:8B:C2', 'CC:88:C7:10:A4:40', 'CC:88:C7:10:A4:41', 'CC:88:C7:10:A4:42', '44:12:44:0F:A4:40', '44:12:44:0F:A4:41', '44:12:44:0F:A4:42', '44:12:44:10:60:E0', '44:12:44:10:60:E1', '44:12:44:10:60:E2', 'E8:26:89:37:EB:C0', 'E8:26:89:37:EB:C1', 'E8:26:89:37:EB:C2', 'CC:88:C7:10:6A:20', 'CC:88:C7:10:6A:21', 'CC:88:C7:10:6A:22', '44:12:44:10:72:00', '44:12:44:10:72:01', '44:12:44:10:72:02', '44:12:44:0F:92:C0', '44:12:44:0F:92:C1', '44:12:44:0F:92:C2', '44:12:44:10:80:80', '44:12:44:10:80:81', '44:12:44:10:80:82']
# mac_addresses_max_signl=[
# '20:9C:B4:09:25:80',
# '20:9C:B4:09:25:81',
# '20:9C:B4:09:25:82',
# '44:12:44:0F:50:80',
# '44:12:44:0F:50:81',
# '44:12:44:0F:50:82',
# 'E8:26:89:37:BD:80',
# 'E8:26:89:37:BD:81',
# 'E8:26:89:37:BD:82',
# '44:12:44:10:69:60',
# '44:12:44:10:69:61',
# '44:12:44:10:69:62',
# '44:12:44:10:74:A0',
# '44:12:44:10:74:A1',
# '44:12:44:10:74:A2',
# '44:12:44:10:06:20',
# '44:12:44:10:06:21',
# '44:12:44:10:06:22',
# '44:12:44:0F:8B:C0',
# '44:12:44:0F:8B:C1',
# '44:12:44:0F:8B:C2',
# 'E8:26:89:37:BD:80',
# 'E8:26:89:37:BD:81',
# 'E8:26:89:37:BD:82',
# '44:12:44:0F:50:80',
# '44:12:44:0F:50:81',
# '44:12:44:0F:50:82']

mac_addresses_max_signl=[
'20:9C:B4:09:25:80',
'20:9C:B4:09:25:81',
'20:9C:B4:09:25:82',
'44:12:44:0F:50:80',
'44:12:44:0F:50:81',
'44:12:44:0F:50:82',
'E8:26:89:37:BD:80',
'E8:26:89:37:BD:81',
'E8:26:89:37:BD:82',
'44:12:44:10:69:60',
'44:12:44:10:69:61',
'44:12:44:10:69:62',
'44:12:44:10:74:A0',
'44:12:44:10:74:A1',
'44:12:44:10:74:A2',
'44:12:44:10:06:20',
'44:12:44:10:06:21',
'44:12:44:10:06:22',
'44:12:44:0F:8B:C0',
'44:12:44:0F:8B:C1',
'44:12:44:0F:8B:C2',
'E8:26:89:37:BD:80',
'E8:26:89:37:BD:81',
'E8:26:89:37:BD:82',
'44:12:44:0F:50:80',
'44:12:44:0F:50:81',
'44:12:44:0F:50:82',
'44:12:44:0F:A4:40',
'44:12:44:0F:A4:41',
'44:12:44:0F:A4:42',
'44:12:44:10:60:E0',
'44:12:44:10:60:E1',
'44:12:44:10:60:E2',
'E8:26:89:37:EB:C0',
'E8:26:89:37:EB:C1',
'E8:26:89:37:EB:C2',
'CC:88:C7:10:6A:20',
'CC:88:C7:10:6A:21',
'CC:88:C7:10:6A:22',
'44:12:44:10:72:00',
'44:12:44:10:72:01',
'44:12:44:10:72:02',
'44:12:44:0F:92:C0',
'44:12:44:0F:92:C1',
'44:12:44:0F:92:C2',
'44:12:44:10:80:80',
'44:12:44:10:80:81',
'44:12:44:10:80:82']



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


def get_coordinates(mac_address, excel_file='router_Locations.xlsx'):
    # Read Excel file
    df = pd.read_excel(excel_file)
    
    # Filter rows based on MAC address
    filtered_df = df[df['Mac Address'] == mac_address]
    
    # Check if the MAC address exists in the dataframe
    if filtered_df.empty:
        return None  # Return None if MAC address not found
    
    # Extract x, y, z coordinates
    x = int(filtered_df['x'].iloc[0])  # Convert to int
    y = int(filtered_df['y'].iloc[0])  # Convert to int
    z = int(filtered_df['z'].iloc[0])  # Convert to int
    
    return x, y, z

def append_to_excel(data, file_name):
    global positions
    # global x,y
    # print("x:",x)
    # print("y:",y)
    # try:
    #     df = pd.read_excel(file_name)
    # except FileNotFoundError:
    #     df = pd.DataFrame(columns=["x", "y"] + mac_addresses)
    
    global X,scaler,knn
    
    # Create a new row with zeros
    new_row = [0] * len(mac_addresses)
    # find_max=1
    required_max_mac=''
    
    
    # Update strengths if MAC address exists in data
    for mac, strength in data["networks"]:
        try:
            index = mac_addresses.index(mac)
            new_row[index] = strength  # Offset by 2 to account for 'x' and 'y' columns
        except ValueError:
            # MAC address not found, skip it
            pass
    # print(required_max_mac)
    for mac, strength in data["networks"]:
        try:
            index = mac_addresses_max_signl.index(mac)
            required_max_mac=mac  # Offset by 2 to account for 'x' and 'y' columns
            break
        except ValueError:
            # MAC address not found, skip it
            pass

    coordinates = get_coordinates(required_max_mac)
    # print(coordinates)

    new_signal_strengths = new_row

    # Create a DataFrame with the new signal strengths
    new_X = pd.DataFrame([new_signal_strengths], columns=X.columns)

    # Normalize the features using the same scaler
    new_X_scaled = scaler.transform(new_X)

    # Make predictions using the trained KNN model
    # predicted_coordinates = knn.predict(new_X_scaled)
    # print(data['device_id'])
    # positions[data['device_id']]=predicted_coordinates
    # print("Predicted coordinates (x, y):", predicted_coordinates)
    predicted_coordinates = knn.predict(new_X_scaled)
    # print("Predicted coordinates (x, y):", predicted_coordinates)
    # Convert NumPy array to Python list
    predicted_coordinates_list = predicted_coordinates.tolist()

    # Assuming data['device_id'] is the key to identify the device
    device_id = data['device_id']

    # Store the predicted coordinates in positions dictionary
    positions[device_id] = predicted_coordinates_list[0]
    positions[device_id+'_maxSig'] = coordinates

    # Convert positions dictionary to JSON format
    positions_json = json.dumps(positions)
    update_positions()




@app.route('/data', methods=['POST'])
def receive_data():
    global count
    global x,y
    # if count==20:
    #     count=0
    # if count==0:
    #     x = int(input("Enter x coordinate: "))
    #     y = int(input("Enter y coordinate: "))
    data = request.data.decode('utf-8')  # Decode the received data
    # print("Received data:")
    # print(data)
    # print(count)
    # count=count+1
    parsed_data = parse_data(data)
    append_to_excel(parsed_data, "router_data_2.xlsx")
    # Process the received data as needed
    # For example, you can save it to a file, store it in a database, or perform any other operation.
    return 'Data received successfully'


if __name__ == '__main__':
    # socketio.run(app, host='0.0.0.0', port=80, debug=False)
    app.run(host='0.0.0.0', port=80)
    
