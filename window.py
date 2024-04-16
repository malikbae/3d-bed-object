import glfw

class Window:
    def __init__(self, width, height, title):
        if not glfw.init():
            raise Exception("glfw can not be initialized!")

        self.window = glfw.create_window(width, height, title, None, None)

        if not self.window:
            glfw.terminate()
            raise Exception("glfw window can not be created!")

        glfw.set_window_pos(self.window, 400, 200)
        glfw.make_context_current(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

    def poll_events(self):
        glfw.poll_events()

    def set_resize_callback(self, callback):
        glfw.set_window_size_callback(self.window, callback)

    @property
    def width(self):
        return glfw.get_framebuffer_size(self.window)[0]

    @property
    def height(self):
        return glfw.get_framebuffer_size(self.window)[1]

    def __del__(self):
        glfw.terminate()
