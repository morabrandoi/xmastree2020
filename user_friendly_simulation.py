##_ all comments made by me, (morabrandoi), will be preceded by "##_"

# Here are the libraries I am currently using:
import time
##_ import board
##_ import neopixel
import re
import math

# You are welcome to add any of these:
import random
# import numpy
# import scipy
# import sys

##_
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation


#NOTE THE LEDS ARE GRB COLOUR (NOT RGB)

# If you want to have user changable values, they need to be entered from the command line
# so import sys sys and use sys.argv[0] etc
# some_value = int(sys.argv[0])

COORDS_FILE_PATH = "./coords.txt"

# IMPORT THE COORDINATES (please don't break this bit)
# Coordinates in form [[x0,y0,z0], [x1,y1,z1], ...]
def import_coords():
    fin = open(COORDS_FILE_PATH,'r')
    coords_raw = fin.readlines()

    coords_bits = [i.split(",") for i in coords_raw]

    coords = []

    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    return coords

##_ Pixels in form [[g0, r0, b0], [g1, r1, b1], ...]
def intialize_pixels(coords):
    ##_ currently assigning colors randomly
    pixel_colors = []
    
    for _ in range(len(coords)):
        rand_g = random.randrange(0,256)
        rand_r = random.randrange(0,256)
        rand_b = random.randrange(0,256)
        pixel_colors.append((rand_g, rand_r, rand_b))

    return pixel_colors

def normalize_grb_to_rgb(pixel_colors):
    normed_pixel_colors = []
    for pixel in pixel_colors:
        norm_g = pixel[0] / 255.0
        norm_r = pixel[1] / 255.0
        norm_b = pixel[2] / 255.0
        normed_pixel_colors.append((norm_r, norm_g, norm_b))       
    
    return normed_pixel_colors

def configure_matplotlib(coords, pixel_colors):
    x_coords = []
    y_coords = []
    z_coords = []
    for x, y, z in coords:
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ax.scatter(x_coords, y_coords, z_coords)
    scatter = ax.scatter(x_coords, y_coords, z_coords, c=normalize_grb_to_rgb(pixel_colors))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    return fig, ax, scatter

def get_initial_state(coords):
    heights = []
    for i in coords:
        heights.append(i[2])

    min_alt = min(heights)
    max_alt = max(heights)

    return {
        "min_alt": min_alt,
        "max_alt": max_alt,
        "dinc": 1,            # how much the rotation points moves each time
        "buffer": 200,        # a buffer so it does not hit to extreme top or bottom of the tree
        "slow": 0,            # pause between cycles (normally zero as it is already quite slow)
        "angle": 0,           # startin angle (in radians)
        "inc": 0.1,           # how much the angle changes per cycle
        "colourA": [0,50,50], # purple
        "colourB": [50,50,0], # yellow
        "swap01": 0,
        "swap02": 0,
        "direction": -1,
        "c": 100              # the starting point on the vertical axis
    }

def update_anim(_, coords, pixels, scatter, sleep_time=0.1):
    # YOU CAN EDIT FROM HERE DOWN

    # I get a list of the heights which is not overly useful here other than to set the max and min altitudes
    heights = []
    for i in coords:
        heights.append(i[2])

    min_alt = min(heights)
    max_alt = max(heights)

    # VARIOUS SETTINGS
    dinc = 1           # how much the rotation points moves each time
    buffer = 200       # a buffer so it does not hit to extreme top or bottom of the tree
    slow = 0           # pause between cycles (normally zero as it is already quite slow)
    angle = 0          # startin angle (in radians)
    inc = 0.1          # how much the angle changes per cycle

    # the two colours in GRB order
    # if you are turning a lot of them on at once, keep their brightness down please
    colourA = [0,50,50] # purple
    colourB = [50,50,0] # yellow

    # INITIALISE SOME VALUES
    swap01 = 0
    swap02 = 0

    # direction it moves in
    direction = -1

    # the starting point on the vertical axis
    c = 100 

    # time.sleep(sleep_time)
    
    LED = 0
    while LED < len(coords):
        if math.tan(angle)*coords[LED][1] <= coords[LED][2]+c:
            pixels[LED] = colourA
        else:
            pixels[LED] = colourB
        LED += 1
    
    # use the show() option as rarely as possible as it takes ages
    # do not use show() each time you change a LED but rather wait until you have changed them all
    # pixels.show()
    
    # now we get ready for the next cycle
    
    angle += inc
    if angle > 2*math.pi:
        angle -= 2*math.pi
        swap01 = 0
        swap02 = 0
    
    # this is all to keep track of which colour is 'on top'
    
    if angle >= 0.5*math.pi:
        if swap01 == 0:
            colour_hold = [i for i in colourA]
            colourA =[i for i in colourB]
            colourB = [i for i in colour_hold]
            swap01 = 1
            
    if angle >= 1.5*math.pi:
        if swap02 == 0:
            colour_hold = [i for i in colourA]
            colourA =[i for i in colourB]
            colourB = [i for i in colour_hold]
            swap02 = 1
    
    # and we move the rotation point
    c += direction*dinc
    
    if c <= min_alt+buffer:
        direction = 1
    if c >= max_alt-buffer:
        direction = -1

    scatter._facecolor3d = normalize_grb_to_rgb(pixels)
    scatter._edgecolor3d = normalize_grb_to_rgb(pixels)

    return scatter

# CODE EXECUTION
coords = import_coords()
pixel_colors = intialize_pixels(coords)
fig, ax, scatter = configure_matplotlib(coords, pixel_colors)

state = get_initial_state(coords)

ani = animation.FuncAnimation(fig, update_anim, fargs=(coords, pixel_colors, scatter))
plt.show()
