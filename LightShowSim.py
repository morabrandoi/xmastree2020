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

class LightShow:
    def __init__(self):
        self.COORDS_FILE_PATH = "./coords.txt"
        self.coords = self._get_coords()
        self.pixel_colors = self._intialize_pixels()
        self.fig, self.ax, self.scatter = self._configure_matplotlib()

        # EDIT BELOW FOR STATE VALUES OF ANIMATION
        self.min_alt, self.max_alt = self._get_min_max_height()
        self.dinc = 1                                              # how much the rotation points moves each time
        self.buffer = 200                                          # a buffer so it does not hit to extreme top or bottom of the tree
        self.slow = 0                                              # pause between cycles (normally zero as it is already quite slow)
        self.angle = 0                                             # startin angle (in radians)
        self.inc = 0.1                                             # how much the angle changes per cycle
        self.colourA = [0,50,50]                                   # purple
        self.colourB = [50,50,0]                                   # yellow
        self.swap01 = 0
        self.swap02 = 0
        self.direction = -1
        self.c = 100       

        # STOP EDITING HERE FOR THE STATE

    def _get_coords(self):
        fin = open(self.COORDS_FILE_PATH,'r')
        coords_raw = fin.readlines()

        coords_bits = [i.split(",") for i in coords_raw]

        coords = []

        for slab in coords_bits:
            new_coord = []
            for i in slab:
                new_coord.append(int(re.sub(r'[^-\d]','', i)))
            coords.append(new_coord)
        
        return coords


    def _intialize_pixels(self):
        ##_ currently assigning colors randomly
        pixel_colors = []
        
        for _ in range(len(self.coords)):
            rand_g = random.randrange(0,256)
            rand_r = random.randrange(0,256)
            rand_b = random.randrange(0,256)
            pixel_colors.append((rand_g, rand_r, rand_b))

        return pixel_colors

    def _normalize_grb_to_rgb(self, pixels):
        normed_pixel_colors = []
        for pixel in pixels:
            norm_g = pixel[0] / 255.0
            norm_r = pixel[1] / 255.0
            norm_b = pixel[2] / 255.0
            normed_pixel_colors.append((norm_r, norm_g, norm_b))       
        
        return normed_pixel_colors

    def _configure_matplotlib(self):
        x_coords = []
        y_coords = []
        z_coords = []
        for x, y, z in self.coords:
            x_coords.append(x)
            y_coords.append(y)
            z_coords.append(z)
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(x_coords, y_coords, z_coords, s=100, c=self._normalize_grb_to_rgb(self.pixel_colors))
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.set_box_aspect([1,1,2])

        return fig, ax, scatter


    def _get_min_max_height(self):
        heights = []
        for i in self.coords:
            heights.append(i[2])

        min_alt = min(heights)
        max_alt = max(heights)

        return min_alt, max_alt


    def update_loop(self, _):
        LED = 0
        while LED < len(self.coords):
            if math.tan(self.angle)*self.coords[LED][1] <= self.coords[LED][2] + self.c:
                self.pixel_colors[LED] = self.colourA
            else:
                self.pixel_colors[LED] = self.colourB
            LED += 1
        
        # use the show() option as rarely as possible as it takes ages
        # do not use show() each time you change a LED but rather wait until you have changed them all
        # pixels.show()
        
        # now we get ready for the next cycle
        
        self.angle += self.inc
        if self.angle > 2*math.pi:
            self.angle -= 2*math.pi
            self.swap01 = 0
            self.swap02 = 0
        
        # this is all to keep track of which colour is 'on top'
        
        if self.angle >= 0.5*math.pi:
            if self.swap01 == 0:
                colour_hold = [i for i in self.colourA]
                self.colourA =[i for i in self.colourB]
                self.colourB = [i for i in colour_hold]
                self.swap01 = 1
                
        if self.angle >= 1.5*math.pi:
            if self.swap02 == 0:
                colour_hold = [i for i in self.colourA]
                self.colourA =[i for i in self.colourB]
                self.colourB = [i for i in colour_hold]
                self.swap02 = 1
        
        # and we move the rotation point
        self.c += self.direction*self.dinc
        
        if self.c <= self.min_alt+self.buffer:
            self.direction = 1
        if self.c >= self.max_alt-self.buffer:
            self.direction = -1

        self.scatter._facecolor3d = self._normalize_grb_to_rgb(self.pixel_colors)
        self.scatter._edgecolor3d = self._normalize_grb_to_rgb(self.pixel_colors)

        return self.scatter

    def display(self):
        ani = animation.FuncAnimation(self.fig, self.update_loop)
        plt.show()

# CODE EXECUTION
sim = LightShow()
sim.display()