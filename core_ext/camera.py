from numpy.linalg import inv

from core.matrix import Matrix
from core_ext.object3d import Object3D


class Camera(Object3D):
    """  Represents the virtual camera used to view the scene """
    def __init__(self, angle_of_view=60, aspect_ratio=1, near=0.1, far=1000):
        super().__init__()
        self._projection_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)
        self._view_matrix = Matrix.make_identity()  # inverse of self._matrix

    @property
    def projection_matrix(self):
        return self._projection_matrix

    @property
    def view_matrix(self):
        return self._view_matrix

    def set_perspective(self, angle_of_view=50, aspect_ratio=1, near=0.1, far=1000):
        self._projection_matrix = Matrix.make_perspective(angle_of_view, aspect_ratio, near, far)

    def set_orthographic(self, left=-1, right=1, bottom=-1, top=1, near=-1, far=1):
        self._projection_matrix = Matrix.make_orthographic(left, right, bottom, top, near, far)

    def update_view_matrix(self):
        self._view_matrix = inv(self.global_matrix)

    def get_position(self):
        return [self._matrix[0][3], self._matrix[1][3], self._matrix[2][3]]
    
    def set_position(self, position):
        self._matrix[0][3] = position[0]
        self._matrix[1][3] = position[1] 
        self._matrix[2][3] = position[2]
        self.update_view_matrix()
    
