from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import time
import random

app = Flask(__name__)
socketio = SocketIO(app)

positions = {}

# Function to continuously update positions and send them over WebSocket
def update_positions():
    global positions
    while True:
        # Generate random positions for demonstration
        positions = {
            'esp32_1': [random.randint(0, 800), random.randint(0, 600)],
            'esp32_2': [random.randint(0, 800), random.randint(0, 600)],
            'esp32_3': [random.randint(0, 800), random.randint(0, 600)]
        }
        socketio.emit('positions', positions)  # Send positions over WebSocket
        time.sleep(0.1)  # Adjust the frequency of updates as needed

# # Start the thread to update positions
# update_thread = threading.Thread(target=update_positions)
# update_thread.daemon = True
# update_thread.start()

@app.route('/')
def index():
    return render_template('visualise.html')

if __name__ == '__main__':
    # socketio.run(app,host='0.0.0.0',port=80, debug=True)
    app.run(host='0.0.0.0', port=80)
