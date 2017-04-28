
from .drawable import PointList, ApertureFlash
from .aperture import CircleAperture

class SVGRenderer:
    """
    SVG Renderer for Layer objects
    """

    def __init__(self, layer):
        self.layer = layer
        self.setup_canvas()

    def setup_canvas(self):
        self.min_x = 10000   # FIXME
        self.min_y = 10000   # FIXME
        self.max_x = 0
        self.max_y = 0

        self.vertical_padding = 50
        self.horizontal_padding = 50

        self.scale = 100

        for shape in self.layer.shapes:
            if isinstance(shape, PointList):
                for point in shape.points:
                    if point.x < self.min_x:
                        self.min_x = point.x
                    if point.x > self.max_x:
                        self.max_x = point.x
                    if point.y < self.min_y:
                        self.min_y = point.y
                    if point.y > self.max_y:
                        self.max_y = point.y
            elif isinstance(shape, ApertureFlash):
                if shape.point.x < self.min_x:
                    self.min_x = shape.point.x
                if shape.point.x > self.max_x:
                    self.max_x = shape.point.x
                if shape.point.y < self.min_y:
                    self.min_y = shape.point.y
                if shape.point.y > self.max_x:
                    self.max_x = shape.point.y
            else:
                raise NotImplementedError

        self.min_x = self.min_x * self.scale
        self.min_y = self.min_y * self.scale
        self.max_x = self.max_x * self.scale
        self.max_y = self.max_y * self.scale

    def _render_point_list(self, shape):
        res = "<path d=\""

        res += "M %i %i " % ( \
            self.horizontal_padding + shape.points[0].x * self.scale, \
            self.vertical_padding + shape.points[0].y * self.scale)

        for i in range(1, len(shape.points)-1):
            res += "L %i %i " % ( \
                self.horizontal_padding + shape.points[i].x * self.scale, \
                self.vertical_padding + shape.points[i].y * self.scale)

        res += "Z\" fill=\"transparent\" stroke=\"black\" "

        if isinstance(shape.aperture, CircleAperture):
            res += "stroke-linecap=\"round\" stroke-linejoin=\"round\" "
            res += "stroke-width=\"%i\" " % (shape.aperture.radius * self.scale)
        else:
            raise NotImplementedError
        
        res += "/>"
        
        return res

    def _render_aperture_flash(self, shape):
        res = ""

        if shape.aperture.hole_radius > 0:
            res = "<circle cx=\"%i\" cy=\"%i\" r=\"%i\" stroke-width=\"%i\" stroke=\"black\" fill=\"white\" />" % ( \
                self.horizontal_padding + shape.point.x * self.scale, \
                self.vertical_padding + shape.point.y * self.scale, \
                shape.aperture.radius * self.scale / 2, \
                (shape.aperture.radius - shape.aperture.hole_radius) * self.scale)
        else:
            res = "<circle cx=\"%i\" cy=\"%i\" r=\"%i\" fill=\"black\" />" % ( \
                self.horizontal_padding + shape.point.x * self.scale, \
                self.vertical_padding + shape.point.y * self.scale, \
                shape.aperture.radius * self.scale / 2)

        return res

    def render(self):
        res = ( "<svg version=\"1.1\"\n" + \
                "     baseProfile=\"full\"\n" + \
                "     width=\"%i\" height=\"%i\"\n" + \
                "     xmlns=\"http://www.w3.org/2000/svg\">\n") % \
                (self.max_x + 2*self.horizontal_padding, self.max_y + 2*self.vertical_padding)

        for shape in self.layer.shapes:
            if isinstance(shape, PointList):
                res += self._render_point_list(shape)
            elif isinstance(shape, ApertureFlash):
                res += self._render_aperture_flash(shape)
            else:
                raise NotImplementedError

        res += "</svg>"
        return res

    def write_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.render())

class GerberRenderer:
    """
    Gerber file Renderer for Layer objects
    """

    def __init__(self, layer):
        self.layer = layer
        self.setup_canvas()

    def setup_canvas(self):
        pass

    def _render_number(self, n):
        res = ""

        if n == 0:
            return "0"

        if n < 0:
            res += "-"

        if n >= 1:
            res += str(int(n))

        res += ("%.*f" % (self.layer.decimal_positions, n - int(n)))[2:]

        return res

    def _render_point(self, point):
        res =   "X" + self._render_number(point.x) + \
                "Y" + self._render_number(point.y)
        return res


    def _render_point_list(self, shape):
        res = ""
        
        # select aperture
        res += "D" + shape.aperture.aperture_identifier + "*\n"

        # render the start of the shape
        res +=  self._render_point(shape.points[0]) + \
                "D02*\n"
       
        # render the rest of the shape
        for i in range(1, len(shape.points)):
            res +=  self._render_point(shape.points[i]) + \
                    "D01*\n"

        return res

    def _render_aperture_flash(self, shape):
        res = ""
        
        # select aperture
        res += "D" + shape.aperture.aperture_identifier + "*\n"

        # render the aperture flash;
        res +=  self._render_point(shape.point) + \
                "D03*\n"

        return res

    def _render_aperture_definition(self, aperture):
        if isinstance(aperture, CircleAperture):
            res = "%ADD" + aperture.aperture_identifier
            res += "C,%f" % aperture.radius

            if aperture.hole_radius > 0:
                res += "X%f" % aperture.hole_radius

            res += "*%\n"

            return res
        else:
            raise NotImplementedError

    def render(self):
        res = ""

        # Format Specification
        res +=  "%FSLA" + \
                "X" + str(self.layer.integer_positions) + str(self.layer.decimal_positions) + \
                "Y" + str(self.layer.integer_positions) + str(self.layer.decimal_positions) + \
                "*%\n"

        # Unit
        res +=  "%MO" + \
                self.layer.unit + \
                "*%\n"

        # render apertures
        for aperture in self.layer.apertures:
            res += self._render_aperture_definition(aperture)

        # render shapes
        for shape in self.layer.shapes:
            if isinstance(shape, PointList):
                res += self._render_point_list(shape)
            elif isinstance(shape, ApertureFlash):
                res += self._render_aperture_flash(shape)
            else:
                raise NotImplementedError

        # End of file
        res += "M02*"
        
        return res

    def write_file(self, filename):
        with open(filename, "w") as f:
            f.write(self.render())

