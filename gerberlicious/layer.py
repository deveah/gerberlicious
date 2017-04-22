
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

