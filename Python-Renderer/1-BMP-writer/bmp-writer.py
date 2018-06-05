# Python 3 file.

import struct
import math
import random

sign = lambda x: (1, -1)[x < 0]

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def color(r,g,b):
    return bytes([b, g, r])

class Render(object):
    """docstring for Render."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
        self.clear()

    def clear(self):
        self.pixels = [
            [color(0, 0, 0) for _ in range(self.width)]
            for __ in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        # File header (14 bites)
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        # Image header (40 bites)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(2835))
        f.write(dword(2835))
        f.write(dword(0))
        f.write(dword(0))

        # Pixel data (width x height x 3)
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()

    def point(self, x, y, color):
        self.pixels[x][y] = color


r = Render(800, 600)
r.point(10, 100, color(255, 255, 255))
r.write('out.bmp')
