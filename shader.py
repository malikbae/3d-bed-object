from OpenGL.GL import *

class Shader:
    def __init__(self, vertex_source, fragment_source):
        self.program = glCreateProgram()
        self.vertex_shader = self.compile_shader(GL_VERTEX_SHADER, vertex_source)
        self.fragment_shader = self.compile_shader(GL_FRAGMENT_SHADER, fragment_source)

        glAttachShader(self.program, self.vertex_shader)
        glAttachShader(self.program, self.fragment_shader)
        glLinkProgram(self.program)
        glValidateProgram(self.program)

        glDeleteShader(self.vertex_shader)
        glDeleteShader(self.fragment_shader)

    def compile_shader(self, type, source):
        shader = glCreateShader(type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            info_log = glGetShaderInfoLog(shader)
            print(f"Failed to compile {'vertex' if type == GL_VERTEX_SHADER else 'fragment'} shader:")
            print(info_log.decode())
            glDeleteShader(shader)
            return None

        return shader

    def use(self):
        glUseProgram(self.program)

    def __del__(self):
        glDeleteProgram(self.program)
