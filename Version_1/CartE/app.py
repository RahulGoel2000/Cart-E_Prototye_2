from flask import Flask, request
import os
from collections import deque
from datetime import datetime
import pytz

timeZ_Ny = pytz.timezone('America/New_York')

# app = Flask(__name__)
app = Flask(__name__, static_folder='static', static_url_path='')

class Cart:

    def __init__(self, id):
        self.mac = deque()
        self.dB = deque()
        self.time = deque()
        self.id = id

carts = ["94:E6:86:C4:2F:50","94:E6:86:C3:E0:0C", "94:E6:86:C5:67:8C", "94:E6:86:C4:21:CC"]
cart_list = [] 
for i in carts:
    cart_list.append(Cart(i))

# @app.route("/")
# def checklive():
#     return "owendpersonal.com is live"

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if(request.method == 'POST'):
        print(request.data)
        return "DATA Received"
    else:
        print("GET")
        return "GET data"

@app.route("/data", methods=['GET', 'POST'])
def data_receive():
    if(request.method == 'POST'):
        store_signals(request.data)
        return "DATA Received"
    else:
        print("GET")
        return "GET data"

@app.route('/getLocation')
def galaxy():
    return app.send_static_file('first_page.html')

@app.route('/svg_map')
def refresh_map():
    os.system('python3 SignalProcess.py')
    return app.send_static_file('svg_map.html')

@app.route('/location')
def refresh_history_table():
    os.system('python3 SignalProcess.py')
    return app.send_static_file('location.html')

# only update the singal data when a new post comes in 
def store_signals(data):
    curr_cart = cart_list[0]
    data_string = data.decode("utf-8")

    mac_idx  = 0
    dB_idx   = 0

    # Find mac and dB for each signal
    while(mac_idx >= 0 and dB_idx >= 0):

        # find the mac address
        mac_idx = data_string.find('MAC:')
        mac_address = data_string[mac_idx+len("MAC:"):mac_idx+len("MAC:")+16]
        data_string = data_string[mac_idx+len("MAC:")+16:]
        
        # find the dB strength
        dB_idx = data_string.find('dB:')
        dB_string = data_string[dB_idx+len("dB:"):dB_idx+len("dB:")+3]

        if(dB_string != "100"):
            dB_string = data_string[dB_idx+len("dB:"):dB_idx+len("dB:")+2]

        data_string = data_string[dB_idx+len("dB:")+2:]

        # find the mac address of the current Cart-E
        cart_idx = data_string.find("ESP:")
        cart_mac = data_string[cart_idx+len("ESP:"):cart_idx+len("ESP:")+17]

        # find which cart this signal is from
        for i in range(len(carts)):
            if(cart_mac == carts[i]):
                curr_cart = cart_list[i]

        # store the mac address and dB information to the file
        # only save 10 latest history in the queue
        # First in first out, remove the oldest data if the queue is full
        if(len(curr_cart.mac) == 10):
            curr_cart.mac.pop()
        curr_cart.mac.appendleft(mac_address)
            
        if(len(curr_cart.dB) == 10):
            curr_cart.dB.pop()
        curr_cart.dB.appendleft(dB_string)

        # record the current time
        if(len(curr_cart.time) == 10):
            curr_cart.time.pop()
        dt_Ny = datetime.now(timeZ_Ny)

        curr_cart.time.appendleft(dt_Ny.strftime('%l:%M%p %Z on %b %d, %Y'))

        # check if there are any more address
        mac_idx = data_string.find('MAC:')

    # record the wifi signal information in corresponding file
    # each file has the prefix of the cart's mac address as its id number
    f = open("./signals/"+cart_mac+"_wifi_signals.txt", "w")
    for i in range(len(curr_cart.mac)):
        f.write("mac = " + curr_cart.mac[i] + ', dB = ' + curr_cart.dB[i] + ", time = " + curr_cart.time[i] + '\n')
            
    # f.write("time = " + time.strftime('%l:%M%p %Z on %b %d, %Y')+"\n")
    f.write("cart = " + cart_mac)
    f.close() 

if __name__ == '__main__':
    # open('wifi_signals.txt', 'w').close()
    app.run(threaded=True, host='0.0.0.0', port=80)