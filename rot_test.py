import numpy as np


def getRotation(angle):
    angle = np.radians(angle)
    return np.array(
        [
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1],
        ]
    )


def getTranslation(Tx, Ty):
    return np.array([[1, 0, Tx], [0, 1, Ty], [0, 0, 1]])


def getWorldCoord(points, Tx, Ty, angle):
    transMat = getTranslation(Tx, Ty)
    rotMat = getRotation(angle)
    A = transMat @ rotMat @ np.linalg.inv(transMat)
    for i in range(points.shape[0]):
        A.dot(points[i, :])

    points_world = A.dot(points.T)
    return points_world


def normalize(v):
    norm = np.sqrt(v[0] ** 2 + v[1] ** 2)
    return (v[0] / norm, v[1] / norm)


def arrayToVector(p):
    vecs = []
    for i in range(p.shape[0]):
        vecs.append((p[0][i], p[1][i]))
    return vecs


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def orthogonal(v):
    return (v[1], -v[0])


def edge_direction(p0, p1):
    return (p1[0] - p0[0], p1[1] - p1[0])


def vertices_to_edges(vertices):
    return [
        edge_direction(vertices[i], vertices[(i + 1) % len(vertices)])
        for i in range(len(vertices))
    ]


def project(vertices, axis):
    dots = [dot(vertex, axis) for vertex in vertices]
    return [min(dots), max(dots)]


def contains(n, range_):
    a = range_[0]
    b = range_[1]
    if b < a:
        a = range_[1]
        b = range_[0]
    return (n >= a) and (n <= b)


def overlap(a, b):
    if contains(a[0], b) or contains(a[1], b) or contains(b[0], a) or contains(b[1], a):
        return True
    return False


# region (SAT_coll_fxn)
# def SAT_collision(vertices_a, vertices_b):
#     edges_a = vertices_to_edges(vertices_a)
#     edges_b = vertices_to_edges(vertices_b)
#     proj_a = [float("inf"), float("-inf")]
#     proj_b = [float("inf"), float("-inf")]
#     overlap_val = float("inf")

#     edges = edges_a + edges_b

#     axes = [normalize(orthogonal(edge)) for edge in edges]

#     for i in range(len(axes)):
#         proj_a = project(vertices_a, axes[i])
#         proj_b = project(vertices_b, axes[i])
#         overlapping = overlap(proj_a, proj_b)
#         overlap_val = min(proj_a[1], proj_b[1]) - max(proj_a[0], proj_b[0])
#         if not overlapping:
#             return False
#     return True
# endregion


class SAT_Collision:
    def __init__(self, poly1, poly2):
        self.poly1 = poly1
        self.poly2 = poly2
        self.collide = False
        self.overlap_val = float("inf")

    def collision_dect(self):
        edges_a = vertices_to_edges(self.poly1)
        edges_b = vertices_to_edges(self.poly2)
        edges = edges_a + edges_b
        axes = [normalize(orthogonal(edge)) for edge in edges]

        for i in range(len(axes)):
            proj_a = project(self.poly1, axes[i])
            proj_b = project(self.poly2, axes[i])
            overlapping = overlap(proj_a, proj_b)
            self.overlap_val = min(proj_a[1], proj_b[1]) - max(proj_a[0], proj_b[0])
            if not overlapping:
                return False

        d = vec()

        return True
