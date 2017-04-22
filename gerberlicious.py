
"""
    gerberlicious.py
    A Python library for programmatically generating Gerber files.

    NOTES:
    
    TODO:
    * Polarity for Shapes.
    * More apertures.
    * Circular interpolation (G02/G03).
    * File attributes.

    RESOURCES:
    * http://www.artwork.com/gerber/appl2.htm
    * https://www.ucamco.com/files/downloads/file/81/the_gerber_file_format_specification.pdf

"""

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

class Point:
    """
    A pair of coordinates (x, y).
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def _render_number(self, n, integer_positions, decimal_positions):
        res = ""

        if n == 0:
            return "0"

        if n < 0:
            res += "-"

        if n >= 1:
            res += str(int(n))

        res += ("%.*f" % (decimal_positions, n - int(n)))[2:]

        return res

    def render(self, integer_positions, decimal_positions):
        res =   "X" + self._render_number(self.x, integer_positions, decimal_positions) + \
                "Y" + self._render_number(self.y, integer_positions, decimal_positions)
        return res

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

    def render(self, integer_positions, decimal_positions):
        res = ""
        
        # select aperture
        res += "D" + self.aperture.aperture_identifier + "*\n"

        # render the start of the shape
        res +=  self.points[0].render(integer_positions, decimal_positions) + \
                "D02*\n"
       
        # render the rest of the shape
        for i in range(1, len(self.points)):
            res +=  self.points[i].render(integer_positions, decimal_positions) + \
                    "D01*\n"

        return res

class ApertureFlash(Drawable):
    """
    A single point flash of an aperture (analogous to touching the paper with
    the tip of the pencil, thus forming a dot).
    """

    def __init__(self, aperture, point):
        self.aperture = aperture
        self.point = point

    def render(self, integer_positions, decimal_positions):
        res = ""
        
        # select aperture
        res += "D" + self.aperture.aperture_identifier + "*\n"

        # render the aperture flash;
        res +=  self.point.render(integer_positions, decimal_positions) + \
                "D03*\n"

        return res

class Layer:
    """
    A canvas onto which Drawables are rendered.
    """

    def __init__(self, integer_positions=2, decimal_positions=5, unit='IN'):
        self.integer_positions = integer_positions
        self.decimal_positions = decimal_positions
        self.unit = unit
        self.apertures = []
        self.shapes = []
        self.attributes = {}

    def add_shape(self, shape):
        self.shapes.append(shape)

    def add_aperture(self, aperture):
        self.apertures.append(aperture)

    def set_attribute(self, attribute, value):
        self.attributes[attribute] = value

    def render(self):
        res = ""

        # Format Specification
        res +=  "%FSLA" + \
                "X" + str(self.integer_positions) + str(self.decimal_positions) + \
                "Y" + str(self.integer_positions) + str(self.decimal_positions) + \
                "*%\n"

        # Unit
        res +=  "%MO" + \
                self.unit + \
                "*%\n"

        # render apertures
        for aperture in self.apertures:
            res += aperture.render()

        # render shapes
        for shape in self.shapes:
            res += shape.render(self.integer_positions, self.decimal_positions)

        # End of file
        res += "M02*"
        
        return res

if __name__ == "__main__":
    layer = Layer()
    
    aperture1 = CircleAperture("10", 0.1)
    layer.add_aperture(aperture1)

    aperture2 = CircleAperture("11", 0.5, 0.2)
    layer.add_aperture(aperture2)

    square = PointList(aperture1)
    square.add_point(Point(2.5, 0))
    square.add_point(Point(5, 0))
    square.add_point(Point(5, 5))
    square.add_point(Point(0, 5))
    square.add_point(Point(0, 2.5))
    square.add_point(Point(2.5, 0))
    layer.add_shape(square)

    donut = ApertureFlash(aperture2, Point(0, 5))
    layer.add_shape(donut)

    print(layer.render())
