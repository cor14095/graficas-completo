import random
import pygame
import numpy
import random
import ctypes

import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders


RED = (255, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL|pygame.DOUBLEBUF)

vertex_shader = """
#version 330
layout (location = 0) in vec4 position;
layout (location = 1) in vec4 randomColor;
layout (location = 2) in vec2 texIn;

uniform float offset;
out vec4 randomColorVertex;
out vec2 textCoords;
void main(){
    gl_Position = vec4(position.x + offset, position.yz, 1.0);
    randomColorVertex = randomColor;
    textCoords = texIn;
}
"""

fragment_shader = """
#version 330
in vec4 randomColorVertex;
in vec2 textCoords;
uniform sampler2D sampler;
void main(){
    gl_FragColor = randomColorVertex * texture(sampler, textCoords);
}
"""

shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
)




vertex_data = numpy.array([
    -0.5, -0.5, -0.5,   1, 1, 1,   0.0, 0.0,
     0.5, -0.5, -0.5,   1, 1, 1,   1.0, 0.0,
     0.5,  0.5, -0.5,   1, 1, 1,   1.0, 1.0,
     0.5,  0.5, -0.5,   1, 1, 1,   1.0, 1.0,
    -0.5,  0.5, -0.5,   1, 1, 1,   0.0, 1.0,
    -0.5, -0.5, -0.5,   1, 1, 1,   0.0, 0.0,
], dtype = numpy.float32)

# texture
textureSurface = pygame.image.load('./texture.jpg')
textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
width = textureSurface.get_width()
height = textureSurface.get_height()

gl.glEnable(gl.GL_TEXTURE_2D)
texture = gl.glGenTextures(1)
gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, textureData)
gl.glGenerateMipmap(gl.GL_TEXTURE_2D)


# vertex buffer object

vertex_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_object)
gl.glBufferData(gl.GL_ARRAY_BUFFER, 48*4, vertex_data, gl.GL_STATIC_DRAW)

# vertex array object
vertex_array_object = gl.glGenVertexArrays(1)
gl.glBindVertexArray(vertex_array_object)

# shaders

gl.glEnableVertexAttribArray(0)
gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 8*4, ctypes.c_void_p(0)) #Padding and info to grab vertexs

gl.glEnableVertexAttribArray(1)
gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False, 8*4, ctypes.c_void_p(3*4))

gl.glEnableVertexAttribArray(2)
gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, False, 8*4, ctypes.c_void_p(6*4))

done = False

x = 0
y = 50
offset = 0.01
rect = pygame.Rect(x, y, 100,100)

gl.glClearColor(0.5, 1.0, 0.5, 1.0)
gl.glUseProgram(shader)

while not done:

    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    offsetLocation = gl.glGetUniformLocation(shader, 'offset')
    gl.glUniform1f(offsetLocation, offset)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 6)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_RIGHT]:
        offset += 0.01
    if pressed[pygame.K_DOWN]:
        y += 20
    if pressed[pygame.K_LEFT]:
        offset -= 0.01
    if pressed[pygame.K_UP]:
        y -= 20

    print(event.type)

    pass
