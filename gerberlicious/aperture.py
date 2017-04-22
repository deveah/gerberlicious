
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

    def __init__(self, aperture_identifier, radius, hole_diameter=0):
        self.aperture_identifier = aperture_identifier
        self.radius = radius
        self.hole_diameter = hole_diameter

    def render(self):
        res = "%ADD" + self.aperture_identifier
        res += "C,%f" % self.radius

        if self.hole_diameter > 0:
            res += "X%f" % self.hole_diameter

        res += "*%\n"

        return res


