import glfw
from OpenGL.GL import *
import pyrr
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
scale_factor = 1.4
scale_matrix = pyrr.matrix44.create_from_scale([scale_factor, scale_factor, scale_factor])

while not window.should_close():
    window.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.Matrix44.from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfw.get_time())

    rotation_matrix = pyrr.matrix44.multiply(rot_x, rot_y)

    transform_matrix = pyrr.matrix44.multiply(rotation_matrix, scale_matrix)

    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, transform_matrix)

    model.draw()
    window.swap_buffers()