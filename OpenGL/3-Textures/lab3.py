import pygame
import numpy
import random
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
import ctypes


pygame.init()
WHITE = (255,255,255)
render = pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF)

vertex_shader = """
#version 330
layout (location=0) in vec4 position;
layout (location=1) in vec4 randomColor;
layout (location=2) in vec2 textIn;

uniform float offset;

out vec4 randomColorVertex;
out vec2 textCoords;

void main() {
    gl_Position = vec4(position.x + offset, position.yz,1.0);
    randomColorVertex = randomColor;
    textCoords = textIn;
}
"""

fragment_shader = """
#version 330

in vec4 randomColorVertex;
in vec2 textCoords;
uniform sampler2D sampler;

void main() {
    gl_FragColor = texture(sampler, textCoords );

}
"""

shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
)

vertex_data = numpy.array([
    0.0,0.5,0.0,0.0,0.0,0.0,1,1,
    0.5,-0.5,0.0,1.0,0.5,0.0,1,0,
    -0.5,-0.5,0.0,1.0,0.5,0.0,0,0
], dtype=numpy.float32)

#texture
textureSurface = pygame.image.load('./texture.jpg')
textureData = pygame.image.tostring(textureSurface,"RGB",1)
width = textureSurface.get_width()
height = textureSurface.get_height()

gl.glEnable(gl.GL_TEXTURE_2D)
texture = gl.glGenTextures(1)
gl.glBindTexture(gl.GL_TEXTURE_2D,texture)
gl.glTexImage2D(gl.GL_TEXTURE_2D,0,gl.GL_RGB,width,height,0,gl.GL_UNSIGNED_BYTE,textureData)
gl.glGenerateMipmap(gl.GL_TEXTURE_2D)


#vertex buffer object

vertex_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_object)
gl.glBufferData(gl.GL_ARRAY_BUFFER, 24 * 4, vertex_data,gl.GL_STATIC_DRAW)

#vertex array object

vertext_array_object = gl.glGenVertexArrays(1)
gl.glBindVertexArray(vertext_array_object)

#shaders
#position = gl.glGetAttribLocation(shader, 'position')
gl.glEnableVertexAttribArray(0)
gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False,8*4, ctypes.c_void_p(0))

gl.glEnableVertexAttribArray(1)
gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, False,8*4, ctypes.c_void_p(3*4))

gl.glEnableVertexAttribArray(2)
gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, False,8*4, ctypes.c_void_p(6*4))


done = False
gl.glClearColor(0.5,1.0,0.5,1.0)
gl.glUseProgram(shader)
offset = 0.01
while not done:
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    offsetLocation = gl.glGetUniformLocation(shader, 'offset')
    gl.glUniform1f(offsetLocation,offset)
    gl.glBindTexture(gl.GL_TEXTURE_2D,texture)
    gl.glDrawArrays(gl.GL_TRIANGLES,0,3)

    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            offset += 0.01
    pass

    pygame.display.flip()
