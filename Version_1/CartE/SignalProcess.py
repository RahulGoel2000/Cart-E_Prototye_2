# Function to parse the data in wifi_signals.txt
# and take the average of each line's wifi signals
import os
import time
from collections import deque

floorplans = ["u1", "u2", "u3", "p1", "p2", "p3"]

class Cart:

    def __init__(self, idx, data_file, history_file):
        self.locw         = deque()
        self.loch         = deque()
        self.room         = deque()
        self.time         = deque()
        self.floor        = ""
        self.idx          = idx
        self.data_file    = data_file
        self.history_file = history_file

carts = ["94:E6:86:C4:2F:50","94:E6:86:C3:E0:0C", "94:E6:86:C5:67:8C", "94:E6:86:C4:21:CC"]
cart_list = [] 
for i in range(len(carts)):
    cart_list.append(Cart(i, "./signals/" + carts[i]+"_wifi_signals.txt", "./history/"+carts[i]+"_history.txt"))

def parse_data(cart):

    if (os.path.getsize(cart.data_file) == 0):
            cart.locw = 300
            cart.loch = 20
            cart.room = "NOT SURE"
    else:
        # parse data from wifi signal files
        with open(cart.data_file, 'r') as f:
            mac_list = []
            dB_list = []
            for line in f:
                if(line.find("mac") == 0):
                    # find mac address
                    mac_index = line.find("mac = ")
                    dB_index = line.find(", dB = ")
                    mac_list.append(line[mac_index+len("mac = "):dB_index])

                    time_index = line.find("time = ")
                    if(time_index >= 0):
                        cart.time.append(line[time_index+len("time = "):-1])
                    
                        sub_line = line[dB_index+len(", dB = "):time_index-len(", ")]
                        num = ""
                        for n in sub_line:
                            # make sure it is a number
                            if(n != " "):
                                num = num + n
                        # each number is seperated by a space
                        dB_list.append(int(num))
                        num = ""
                # else:

        f.close()

        # record the current location
        with open(cart.history_file, "w") as f:
            for i in range(len(mac_list)):
                curr_locw, curr_loch, curr_room, cart.floor = find_cart(mac_list[i])

                if(len(cart.locw) == 10):
                    cart.locw.popleft()
                    cart.loch.popleft()
                    cart.room.popleft()
                cart.locw.append(curr_locw)
                cart.loch.append(curr_loch)
                cart.room.append(curr_room)

                f.write("CART location: " + str(curr_room) + "," + str(cart.time[i]))
                f.write('\n')
        f.close()

# update the maps based on floor-plan
def display(floor):
    with open("./static/"+floor+"_template.html", "r") as template_f:
        with open ("./static/"+floor+"_map.html", "w") as out_f:
            tmp = template_f.read()
            counter = 0
            for i in range(len(cart_list)):
                if(floor == cart_list[i].floor):
                    tmp = tmp.replace("C"+str(counter), '"CART'+str(i)+'-HERE"')
                    tmp = tmp.replace("LOCW"+str(counter), str(cart_list[i].locw[0]))
                    tmp = tmp.replace("LOCH"+str(counter), str(cart_list[i].loch[0]))
                    counter = counter + 1
            out_f.write(tmp)
        out_f.close()
    template_f.close()

# update the history table
def update_history(cart_list):
    # overwrite html file location.html
    with open("./static/location_template.html", "r") as template_f:
        with open ("./static/location.html", "w") as out_f:
            tmp = template_f.read()
            for cart in cart_list:
                for i in range(len(cart.room)):
                    tmp = tmp.replace("CART"+str(cart.idx)+"_HIS_"+str(i), cart.room[i])
                    on_idx = cart.time[i].find(" on ")
                    year_idx = cart.time[i].find(", ")
                    time_txt = cart.time[i][:on_idx] + ", " + cart.time[i][on_idx+len(" on "):year_idx]
                    tmp = tmp.replace("CART"+str(cart.idx)+"_POS_"+str(i), time_txt)
            out_f.write(tmp)
        out_f.close()
    template_f.close()    


def find_cart(mac_address):
    w = 0
    h = 0
    loc = "Phillips_238"
    floor = "not_found"

    # Phillips 1st floor 
    if("94:B4:0F:E6:60:E" in mac_address):
        w = 260
        h = 280
        loc = "Phillips_100cb-1"
        floor = "p1"

    elif("94:B4:0F:E6:62:0" in mac_address):
        w = 310
        h = 335
        loc = "Phillips_100cb-2"
        floor = "p1"

    elif("94:B4:0F:E6:62:4" in mac_address):
        w = 480
        h = 335
        loc = "Phillips_100cb-3"
        floor = "p1"

    # Phillips 2nd floor 
    elif("94:B4:0F:E6:34" in mac_address):
        w = 10
        h = 500
        loc = "Phillips_238"
        floor = "p2"

    elif("F0:5C:19:6E:74" in mac_address):
        w = 200
        h = 520
        loc = "Phillips_239"
        floor = "p2"

    elif("F0:5C:19:6E:A0" in mac_address):
        w = 200
        h = 420
        loc = "Phillips_237"
        floor = "p2"

    elif("94:B4:0F:E6:35" in mac_address):
        w = 30
        h = 140
        loc = "Phillips_200-1"
        floor = "p2"

    elif("94:B4:0F:E6:45:C" in mac_address):
        w = 30
        h = 220
        loc = "Phillips_200-2"
        floor = "p2"

    elif("94:B4:0F:E6:44:E" in mac_address):
        w = 270
        h = 250
        loc = "Phillips_200-3"
        floor = "p2"

    elif("E8:26:89:37:9B" in mac_address):
        w = 5
        h = 100
        loc = "Phillips_203"
        floor = "p2"

    elif("E8:26:89:37:DB" in mac_address):
        w = 5
        h = 270
        loc = "Phillips_219"
        floor = "p2"

    elif("94:B4:0F:E6:45:E" in mac_address):
        w = 470
        h = 250
        loc = "Phillips_232"
        floor = "p2"

    # Upson 1st floor
    elif("F0:5C:19:A9:38:8" in mac_address):
        w = 440
        h = 240
        loc = "upson_10041-2/20041-2"
        floor = "u1"
        print("HERE")
    
    elif("F0:5C:19:A9:5A:8" in mac_address):
        w = 350
        h = 240
        loc = "upson_10041-1"
        floor = "u1"

    elif("F0:5C:19:A9:31:2" in mac_address):
        w = 230
        h = 240
        loc = "upson_10040-2"
        floor = "u1"

    elif("F0:5C:19:A9:32:0" in mac_address):
        w = 130
        h = 240
        loc = "upson_10040-1"
        floor = "u1"

    # Upson 2nd floor
    elif("F0:5C:19:A9:5C:A" in mac_address):
        w = 350
        h = 240
        loc = "upson_20041-1"
        floor = "u2"

    elif("F0:5C:19:A9:59:A" in mac_address):
        w = 230
        h = 240
        loc = "upson_20040-2"
        floor = "u2"

    elif("F0:5C:19:A9:59:C" in mac_address):
        w = 130
        h = 240
        loc = "upson_20040-1"
        floor = "u2"
        
    elif("F0:5C:19:A9:59:8" in mac_address):
        w = 60
        h = 170
        loc = "upson_west_corner"
        floor = "u2"

    # Upson 3rd floor
    elif("B4:5D:50:81:56:E" in mac_address):
        w = 440
        h = 240
        loc = "upson-30041-1"
        floor = "u3"

    elif("B4:5D:50:83:FE:2" in mac_address):
        w = 350
        h = 240
        loc = "upson-30041-2"
        floor = "u3"

    elif("94:B4:0F:E6:62:4" in mac_address):
        w = 230
        h = 240
        loc = "upson-30040-1"
        floor = "u3"

    elif("F0:5C:19:76:3D:C" in mac_address):
        w = 130
        h = 240
        loc = "upson-30040-2"
        floor = "u3"
        
    elif("AC:A3:1E:05:40:E" in mac_address):
        w = 60
        h = 170
        loc = "upson_west_corner"
        floor = "u3"

    return w, h, loc, floor

if __name__ == '__main__':
    # parse_data('wifi_signals.txt', 'path_history.txt', './static/p2_map.html')
    for i in range(len(cart_list)):
        parse_data(cart_list[i])

    for floor in floorplans:
        display(floor)

    update_history(cart_list)