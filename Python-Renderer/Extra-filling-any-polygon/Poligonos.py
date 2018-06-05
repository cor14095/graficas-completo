# Python 3 file.

import struct
import math
import random
import time
import struct

# ===============================================================
# Utilities
# ===============================================================

def char(c):
  """
  Input: requires a size 1 string
  Output: 1 byte of the ascii encoded char
  """
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  """
  Input: requires a number such that (-0x7fff - 1) <= number <= 0x7fff
         ie. (-32768, 32767)
  Output: 2 bytes

  Example:
  >>> struct.pack('=h', 1)
  b'\x01\x00'
  """
  return struct.pack('=h', w)

def dword(d):
  """
  Input: requires a number such that -2147483648 <= number <= 2147483647
  Output: 4 bytes

  Example:
  >>> struct.pack('=l', 1)
  b'\x01\x00\x00\x00'
  """
  return struct.pack('=l', d)

def color(r, g, b):
  """
  Input: each parameter must be a number such that 0 <= number <= 255
         each number represents a color in rgb
  Output: 3 bytes

  Example:
  >>> bytes([0, 0, 255])
  b'\x00\x00\xff'
  """
  return bytes([b, g, r])


# ===============================================================
# Constants
# ===============================================================

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
GREEN = color(50, 200, 50)
RED = color(200, 50, 50)
BLUE = color(50, 50, 200)

# ===============================================================
# Renders a BMP file
# ===============================================================

class Render(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()

  def clear(self):
    self.pixels = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    f = open(filename, 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    # Pixel data (width x height x 3 pixels)
    for x in range(self.height):
      for y in range(self.width):
        f.write(self.pixels[x][y])

    f.close()

  def display(self):
    """
    Displays the image, a external library (wand) is used, but only for convenience during development
    """
    filename = 'out.bmp'
    self.write(filename)

    from wand.image import Image
    from wand.display import display

    with Image(filename=filename) as image:
      display(image)

  def set_color(self, color):
    self.current_color = color

  def point(self, x, y, color = None):
    # 0,0 was intentionally left in the bottom left corner to mimic opengl
    self.pixels[y][x] = color or self.current_color

  def line(self, start, end, color = None):
    """
    Draws a line in the screen.
    Input:
      start: size 2 array with x,y coordinates
      end: size 2 array with x,y coordinates
    """
    x1, y1 = start
    x2, y2 = end

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)
    steep = dy > dx

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dy = abs(y2 - y1)
    dx = abs(x2 - x1)

    offset = 0
    threshold = dx

    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            self.point(y, x, color)
        else:
            self.point(x, y, color)

        offset += dy * 2
        if offset >= threshold:
            y += 1 if y1 < y2 else -1
            threshold += dx * 2

  def polygon(self, points, color, fill = False):
        maxY = 0
        maxX = 0
        minY = 1000
        minX = 1000
        '''
        First we're gonna draw the exterior polygon.
        '''
        for pointSet in points:
            for i in range(len(pointSet)):
                # This if make that the last point is connected with the first point
                if (i < (len(pointSet) - 1)):
                    self.line(pointSet[i], pointSet[i + 1], color)
                else:
                    self.line(pointSet[i], pointSet[0], color)
                # Now we look for a the largest and lowest (x,y)
                # Max X
                if (pointSet[i][0] > maxX):
                    maxX = pointSet[i][0]
                # Max Y
                if (pointSet[i][1] > maxY):
                    maxY = pointSet[i][1]
                # Min X
                if (pointSet[i][0] < minX):
                    minX = pointSet[i][0]
                # Min Y
                if (pointSet[i][1] < minY):
                    minY = pointSet[i][1]
        if (fill):
            # print ("maxX: %s, maxY: %s, minX: %s, minY: %s" % (maxX, maxY, minY, minY))
            # Now we start to fill it.
            for y in range(minY, maxY + 1):
                # Initialize some variables.
                point1 = (0, 0)
                point2 = (0, 0)
                initPoint = False
                endPoint = False
                pointCounter = 0
                for x in range(minX, maxX + 1):
                    # Get points:
                    point = (self.pixels[y][x][0], self.pixels[y][x][1], self.pixels[y][x][2])
                    nextPoint = (self.pixels[y][x + 1][0], self.pixels[y][x + 1][1], self.pixels[y][x + 1][2])
                    prevPoint = (self.pixels[y][x - 1][0], self.pixels[y][x - 1][1], self.pixels[y][x - 1][2])

                    # Here I find a point with white.
                    if ((point == (255, 255, 255)) and (not initPoint) and (nextPoint == (0, 0, 0))):
                        #  and (nextPoint == (0, 0, 0))
                        # print ("Next point color is: ({})".format(nextPoint))
                        point1 = (x + 1, y)
                        initPoint = True
                        pointCounter += 1
                    # End point white,
                    elif ((point == (255, 255, 255)) and (not endPoint) and (nextPoint == (0, 0, 0))):
                        # and (x != point1[0] + 1)
                        # print ("Previous point color is: ({})".format(prevPoint))
                        point2 = (x - 1, y)
                        endPoint = True
                        pointCounter += 1

                    # Here I check if I have both points and draw a line.
                    if (initPoint and endPoint):
                        # print ("Points to print: ({}, {})".format(point1, point2))
                        initPoint = False
                        endPoint = False
                        # print("line from: ({}, {}) to: ({}, {})".format(point1[0], point1[1], point2[0], point2[1]))
                        self.line(point1, point2, GREEN)
                        # point1 = point2
                # print ("Line {} has {} points.".format(y, pointCounter))

'''
Main program start
'''

start_time = time.time()

polygon1 = [
    (165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360),
    (250, 380), (220, 385), (205, 410), (193, 383)
]

polygon2 = [
    (321, 335), (288, 286), (339, 251), (374, 302)
]

polygon3 = [
    (377, 249), (411, 197), (436, 249)
]

polygon4 = [
    (413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37),
    (660, 52), (750, 145), (761, 179), (672, 192), (659, 214), (615, 214),
    (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)
    ]

polygon4_5 = [
    (682, 175), (708, 120), (735, 148), (739, 170)
]

r = Render(800, 800)
r.polygon([polygon4, polygon4_5], WHITE, True)
# r.polygon(polygonPoints, WHITE, True)
r.write('polygon.bmp')

print("--- %s seconds ---" % (time.time() - start_time))
