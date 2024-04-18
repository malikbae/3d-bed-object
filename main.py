import glfw
from OpenGL.GL import *
import numpy as np
from window import Window
from shader import Shader
from model import Model

vertex_source = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;

uniform mat4 rotation;

out vec3 v_color;

void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_source = """
# version 330

in vec3 v_color;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

window = Window(1280, 720, "My OpenGL window")
window.set_resize_callback(window_resize)

shader_program = Shader(vertex_source, fragment_source)
shader_program.use()

model = Model()

glClearColor(0.2, 0.2, 0.2, 1)
glEnable(GL_DEPTH_TEST)

rotation_loc = glGetUniformLocation(shader_program.program, "rotation")
scale_factor = 1.2
scale_matrix = np.array([
    [scale_factor, 0.0, 0.0, 0.0],
    [0.0, scale_factor, 0.0, 0.0],
    [0.0, 0.0, scale_factor, 0.0],
    [0.0, 0.0, 0.0, 1.0]
], dtype=np.float32)

while not window.should_close():
    window.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    time = glfw.get_time()

    rot_x = rot_x = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, np.cos(0.5 * time), -np.sin(0.5 * time), 0.0],
        [0.0, np.sin(0.5 * time), np.cos(0.5 * time), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    rot_y = np.array([
        [np.cos(0.8 * time), 0.0, np.sin(0.8 * time), 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [-np.sin(0.8 * time), 0.0, np.cos(0.8 * time), 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ], dtype=np.float32)

    rotation_matrix = np.dot(rot_x, rot_y)

    transform_matrix = np.dot(rotation_matrix, scale_matrix)

    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, transform_matrix)

    model.draw()
    window.swap_buffers()