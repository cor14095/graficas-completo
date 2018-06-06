from render import *

r = Render(800, 800)

r.viewport(np.matrix([
        [3, 0, 0, 100],
        [0, 3, 0, 120],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./Modelos/box.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./Modelos/box.obj',texture=t,shader=shader)

r.viewport(np.matrix([
        [1, 0, 0, 130],
        [0, 1, 0, 160],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./Modelos/fox.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./Modelos/fox.obj',texture=t,shader=shader)

r.viewport(np.matrix([
        [2, 0, 0, 80],
        [0, 2, 0, 180],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ]))
t = Texture('./Modelos/pumpkin.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./Modelos/pumpkin.obj',texture=t,shader=shader)

r.viewport(np.matrix([
        [200, 0, 0, 300],
        [0, 200, 0, 10],
        [0, 0, 1, 10],
        [0, 0, 0, 1]
        ]))
t = Texture('./Modelos/camero.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,1,0),V3(0,1,0))
r.load('./Modelos/camero.obj',texture=t,shader=shader)

r.viewport(np.matrix([
        [10, 0, 0, 500],
        [0, 10, 0, 5],
        [0, 0, 1, -100],
        [0, 0, 0, 1]
        ]))
t = Texture('./Modelos/house.bmp')
r.light = V3(0,0,1)
r.lookAt(V3(1,1,1),V3(0,0,0),V3(0,1,0))
r.load('./Modelos/house.obj',texture=t,shader=shader)

r.display('out.bmp')
