import struct

def color(r,g,b):
    return bytes([r, g, b])

BLACK = color(0,0,0)
WHITE = color(255,255,255)
RED = color(200, 0, 0)

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h',w)

def dword(d):
    return struct.pack('=l',d)

class Obj(object):
    def __init__(self,filename):
        with open(filename) as f:
            self.lines = f.read().splitlines()
        self.vertices = []
        self.vfaces = []
        self.read()

    def read(self):
        for line in self.lines:
            if line:
                prefix,value = line.split(' ',1)
                if prefix == "v":
                    self.vertices.append(list(map(float,value.split(' '))))
                elif prefix =="f":
                    self.vfaces.append([list(map(int,face.split('/'))) for face in value.split(' ')])

class Render(object):
    def __init__(self,width,height):

        self.width = width
        self.height = height
        self.current_color = WHITE
        self.clear()

    def color(self,color):
        r,g,b = color
        return bytes([b,g,r])

    def clear(self):
        self.pixels = [
            [WHITE for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self,filename):
        f = open(filename,'bw')
         #HEADER
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14+40+self.width * self.height *3))
        f.write(dword(0))
        f.write(dword(14+40))

        #IMAGE HEADER (40 BYTES)
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height *3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                f.write(self.pixels[x][y])

        f.close()

    def display(self, filename='out.bmp'):
        self.write(filename)
        try:
            from wand.image import Image
            from wand.display import display
            with Image(filename=filename) as image:
                display(image)
        except ImportError:
            pass

    def point(self, x, y, color = None):
        try:
            self.pixels[y][x] = color or self.current_color
        except:
            pass

    def set_color(self,color):
        self.current_color = color

    def line(self, start, end, color):
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
                self.point(y, x, self.color(color))
            else:
                self.point(x, y, self.color(color))

            offset += dy * 2
            if offset >= threshold:
                y += 1 if y1 < y2 else -1
                threshold += dx * 2

    def load(self, filename, translate=(0, 0), scale=(1, 1)):
        model = Obj(filename)
        for face in model.vfaces:
            vcount = len(face)
            for j in range(vcount):
                f1 = face[j][0]
                f2 = face[(j+1)%vcount][0]

                v1 = model.vertices[f1 - 1]
                v2 = model.vertices[f2 - 1]

                scaleX, scaleY = scale
                translateX, translateY = translate

                x1 = round((v1[0] + translateX) * scaleX)
                y1 = round((v1[1] + translateY) * scaleY)
                x2 = round((v2[0] + translateX) * scaleX)
                y2 = round((v2[1] + translateY) * scaleY)

                self.line((x1, y1), (x2, y2),(0,0,0))

r = Render(800,600)
r.load('hand.obj',(9,2),(70,70))
r.display()
r.display('out.bmp')
