
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

