import imp
import math
import requests
import argparse
import json
# from pygame import mixer
from time import sleep
# from sense_hat import SenseHat

# mixer.init()
# sense = SenseHat()

# def display_status(pixels):
#     sense.set_pixels(pixels)

g = (0, 255, 0)
b = (0, 0, 0)
r = (255, 0, 0)
y = (255, 255, 0)
w = (255, 255, 255)

idle_pixels = [
    g, g, g, g, g, g, g, w,
    g, g, g, g, g, g, w, w,
    g, g, g, g, g, w, w, g,
    w, g, g, g, w, w, g, g,
    w, w, g, w, w, g, g, g,
    g, w, w, w, g, g, g, g,
    g, g, w, g, g, g, g, g,
    g, g, g, g, g, g, g, g,
]

waiting_pixels = [
    y, y, w, w, w, w, y, y,
    y, y, w, w, w, w, y, y,
    y, y, w, w, w, w, y, y,
    y, y, y, w, w, y, y, y,
    y, y, y, w, w, y, y, y,
    y, y, w, y, y, w, y, y,
    y, y, w, y, y, w, y, y,
    y, y, w, w, w, w, y, y,
]

busy_pixels = [
    r, w, r, r, r, r, w, r,
    r, w, w, r, r, w, w, r,
    r, r, w, w, w, w, r, r,
    r, r, r, w, w, r, r, r,
    r, r, w, w, w, w, r, r,
    r, w, w, r, r, w, w, r,
    r, w, r, r, r, r, w, r,
    r, r, r, r, r, r, r, r,
]

clear_pixels = [
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
]

def getMovement(src, dst):
    speed = 0.0001          # divide by 10 to get back original speed
    dst_x, dst_y = dst
    x, y = src
    direction = math.sqrt((dst_x - x)**2 + (dst_y - y)**2)
    longitude_move = speed * ((dst_x - x) / direction )
    latitude_move = speed * ((dst_y - y) / direction )
    return longitude_move, latitude_move

def moveDrone(src, d_long, d_la):
    x, y = src
    x = x + d_long
    y = y + d_la        
    return (x, y)

def send_location(SERVER_URL, id, drone_coords, status):
    with requests.Session() as session:
        drone_info = {'id': id,
                      'longitude': drone_coords[0],
                      'latitude': drone_coords[1],
                       'status': status
                    }
        resp = session.post(SERVER_URL, json=drone_info)

def distance(_fr, _to):
    _dist = ((_to[0] - _fr[0])**2 + (_to[1] - _fr[1])**2)*10**6
    return _dist
        
def run(id, current_coords, from_coords, to_coords, SERVER_URL):
    drone_coords = current_coords
    joystick = True
    # order recevied play sound and change led to display busy animation 

    # mixer.music.load("./sounds/doorbell-1.wav")
    # mixer.music.play()

    # while mixer.music.get_busy() == True:
    # Move from current_coodrs to from_coords
    d_long, d_la =  getMovement(drone_coords, from_coords)
    while distance(drone_coords, from_coords) > 0.0002:
        # display_status(busy_pixels)
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='busy')
        sleep(0.1)
        # display_status(clear_pixels)

        # mixer.music.stop()
        # mixer.music.unload()


    # we have arrived to from address led to waiting, and play sound effect and await joystick input to continue
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='waiting')
    # display_status(waiting_pixels)
    # mixer.music.load("./sounds/space-odyssey.mp3")
    # mixer.music.play()

    # while mixer.music.get_busy() == True:
        # while joystick:
        #     for event in sense.stick.get_events():
        #         if event.action == "pressed":
        #             joystick = False

        # joystick = True
        # mixer.music.stop()
        # mixer.music.unload()

    # after continue play sound effect and change led to busy animation
    # mixer.music.load("./sounds/space-odyssey.mp3")
    # mixer.play()

    # while mixer.music.get_busy() == True:
        # Move from from_coodrs to to_coords
    d_long, d_la =  getMovement(drone_coords, to_coords)
    while distance(SERVER_URL, drone_coords, to_coords) > 0.0002:
        # display_status(busy_pixels)
        drone_coords = moveDrone(drone_coords, d_long, d_la)
        send_location(id=id, drone_coords=drone_coords, status='busy')
        sleep(0.1)
        # display_status(clear_pixels)


        # mixer.stop()
        # mixer.unload()
    
    # when we have arrived led to waiting symbol and sound effect await joystick input to continue
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='waiting')
    # display_status(waiting_pixels)

    # Music
    # mixer.music.load("./sounds/space-odyssey.mp3")
    # mixer.music.play()

    # while mixer.music.get_busy() == True:
        # while joystick:
        #     for event in sense.stick.get_events():
        #         if event.action == "pressed":
        #             joystick = False

        # joystick = True
        # mixer.music.stop()
        # mixer.music.unload()

    # Stop and update status to database
    send_location(SERVER_URL, id=id, drone_coords=drone_coords, status='idle')
    
    return drone_coords[0], drone_coords[1]
   
   
if __name__ == "__main__":
    # Fill in the IP address of server, in order to location of the drone to the SERVER
    #===================================================================
    SERVER_URL = "http://10.11.44.125:5001/drone"
    #===================================================================
    print("in sim")

    parser = argparse.ArgumentParser()
    parser.add_argument("--clong", help='current longitude of drone location' ,type=float)
    parser.add_argument("--clat", help='current latitude of drone location',type=float)
    parser.add_argument("--flong", help='longitude of input [from address]',type=float)
    parser.add_argument("--flat", help='latitude of input [from address]' ,type=float)
    parser.add_argument("--tlong", help ='longitude of input [to address]' ,type=float)
    parser.add_argument("--tlat", help ='latitude of input [to address]' ,type=float)
    parser.add_argument("--id", help ='drones ID' ,type=str)
    args = parser.parse_args()

    current_coords = (args.clong, args.clat)
    from_coords = (args.flong, args.flat)
    to_coords = (args.tlong, args.tlat)

    print(current_coords, from_coords, to_coords)
    drone_long, drone_lat = run(args.id, current_coords, from_coords, to_coords, SERVER_URL)
    # drone_long and drone_lat is the final location when drlivery is completed, find a way save the value, and use it for the initial coordinates of next delivery
    #=============================================================================
    data = {'long' : drone_long, 'lat' : drone_lat}
    with open('data.json', 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

    # Display lights
    # when done play sound effect and change led to idle 
    # display_status(idle_pixels)

    # Music 
    # mixer.music.load("./sounds/coin.wav")
    # mixer.music.play()

    # while mixer.music.get_busy() == True:
    #     sleep(2)
    #     mixer.music.stop()

