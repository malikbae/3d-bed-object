import numpy as np
from OpenGL.GL import *
import ctypes
from meshes.bed import Bed

class Model:
    def __init__(self):
        self.get_bed_model()
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        self.setup_vertex_attributes()

    def get_bed_model(self):
        frame_vertices, frame_indices = Bed.get_frame_data()
        bed_vertices, bed_indices = Bed.get_bed_data()
        first_pillow_vertices, first_pillow_indices = Bed.get_first_pillow_data()
        second_pillow_vertices, second_pillow_indices = Bed.get_second_pillow_data()
        blanket_vertices, blanket_indices = Bed.get_blanket_data()
        back_side_blanket_vertices, back_side_blanket_indices = Bed.get_back_side_blanket_data()

        bed_indices = bed_indices + int(len(frame_vertices) / 6)

        total_length = len(frame_vertices) + len(bed_vertices)
        first_pillow_indices = first_pillow_indices + int(total_length / 6)

        total_length = total_length + len(first_pillow_vertices)
        second_pillow_indices = second_pillow_indices + int(total_length / 6)

        total_length = total_length + len(second_pillow_vertices)
        blanket_indices = blanket_indices + int(total_length / 6)

        total_length = total_length + len(blanket_vertices)
        back_side_blanket_indices = back_side_blanket_indices + int(total_length / 6)
        
        self.vertices = np.concatenate([frame_vertices, bed_vertices, first_pillow_vertices, second_pillow_vertices, blanket_vertices, back_side_blanket_vertices])
        self.indices = np.concatenate([frame_indices, bed_indices, first_pillow_indices, second_pillow_indices, blanket_indices, back_side_blanket_indices])

        return self.vertices, self.indices

    def setup_vertex_attributes(self):
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def draw(self):
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
