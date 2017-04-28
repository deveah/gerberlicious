
class Drawable:
    """
    Any object that can be rendered on the canvas.
    """

    def __init__(self):
        pass

class PointList(Drawable):
    """
    A list of points which, when rendered onto the canvas, are drawn as
    connecting segments.
    """

    def __init__(self, aperture):
        self.aperture = aperture
        self.points = []

    def add_point(self, point):
        self.points.append(point)

class ApertureFlash(Drawable):
    """
    A single point flash of an aperture (analogous to touching the paper with
    the tip of the pencil, thus forming a dot).
    """

    def __init__(self, aperture, point):
        self.aperture = aperture
        self.point = point
