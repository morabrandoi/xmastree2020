##_ For clarity, comments with "##_" will be from me and not Matt Parker


##_ this function animates the plot
def animate_scatters(frame, old_scatter):
    # new_scatter = YOUR_FUNCTION_HERE(old_scatter)
    new_scatter = [[random.randrange(0,50) for _ in range(3)] for j in range(50)]
    return new_scatter

##_ Scatter has the shape [(g0, r0, b0), (g1, r1, b1), ...]
def YOUR_UPDATE_FUNCTION_HERE(old_scatter):
    new_scatter = []
    UPDATE_CONSTANT = 0.1
    for light in old_scatter:
        g, r, b = light[0], light[1], light[2]
        color_average = (g + r + b) / 3.0
        g_delta = (color_average - g)
        r_delta = (color_average - r)
        b_delta = (color_average - b)
        g = int(g + g_delta)
        r = int(r + r_delta)
        b = int(b + b_delta)

        new_scatter.append([g, r, b])


def xmaslight():
    # This is the code from my 
    
    #NOTE THE LEDS ARE GRB COLOUR (NOT RGB)
    
    # Here are the libraries I am currently using:
    import time
    ##_ import board
    ##_ import neopixel
    import re
    import math
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    # You are welcome to add any of these:
    import random
    # import numpy
    # import scipy
    # import sys
    
    # If you want to have user changable values, they need to be entered from the command line
    # so import sys sys and use sys.argv[0] etc
    # some_value = int(sys.argv[0])
    
    # IMPORT THE COORDINATES (please don't break this bit)
    
    coordfilename = "./coords.txt"
	
    fin = open(coordfilename,'r')
    coords_raw = fin.readlines()
    
    coords_bits = [i.split(",") for i in coords_raw]
    
    coords = []
    
    for slab in coords_bits:
        new_coord = []
        for i in slab:
            new_coord.append(int(re.sub(r'[^-\d]','', i)))
        coords.append(new_coord)
    
    #set up the pixels (AKA 'LEDs')
    PIXEL_COUNT = len(coords) # this should be 500
    
    ##_ pixels = neopixel.NeoPixel(board.D18, PIXEL_COUNT, auto_write=False)
    # pixels = coords
    x_coords = []
    y_coords = []
    z_coords = []
    for x, y, z in coords:
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)
    
    ##_ SETTING UP VISUALIZATION
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ##_ END OF VISUALIZATION CODE

    # YOU CAN EDIT FROM HERE DOWN
    
    # I get a list of the heights which is not overly useful here other than to set the max and min altitudes
    heights = []
    for i in coords:
        heights.append(i[2])
    
    min_alt = min(heights)
    max_alt = max(heights)
    
    # VARIOUS SETTINGS
    
    # how much the rotation points moves each time
    dinc = 1
    
    # a buffer so it does not hit to extreme top or bottom of the tree
    buffer = 200
    
    # pause between cycles (normally zero as it is already quite slow)
    slow = 0
    
    # startin angle (in radians)
    angle = 0
    
    # how much the angle changes per cycle
    inc = 0.1
    
    # the two colours in GRB order
    # if you are turning a lot of them on at once, keep their brightness down please
    colourA = [0,50,50] # purple
    colourB = [50,50,0] # yellow
    
    
    # INITIALISE SOME VALUES
    
    swap01 = 0
    swap02 = 0
    
    # direct it move in
    direction = -1
    
    # the starting point on the vertical axis
    c = 100 
    
    # yes, I just run which run is true
    run = 1
    while run == 1:
        
        time.sleep(slow)
        
        LED = 0
        while LED < len(coords):
            if math.tan(angle)*coords[LED][1] <= coords[LED][2]+c:
                pixels[LED] = colourA
            else:
                pixels[LED] = colourB
            LED += 1
        
        # use the show() option as rarely as possible as it takes ages
        # do not use show() each time you change a LED but rather wait until you have changed them all
        ##_ pixels.show()
        plt.show()
        
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
        
    return 'DONE'


# yes, I just put this at the bottom so it auto runs
xmaslight()
