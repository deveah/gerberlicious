
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

