
class Aperture:
    """
    The look and shape of the "tip of the pencil" with which a shape of any
    sorts is drawn on the canvas.
    """

    def __init__(self):
        pass

class CircleAperture(Aperture):
    """
    An Aperture in the shape of a circle, with an optional hole inside, which
    would actually turn it into the shape of a donut.
    """

    def __init__(self, aperture_identifier, radius, hole_radius=0):
        self.aperture_identifier = aperture_identifier
        self.radius = radius
        self.hole_radius = hole_radius

