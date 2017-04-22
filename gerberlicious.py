
"""
    gerberlicious, a python library for programmatically generating Gerber files

    Example script.
"""

from gerberlicious.point import Point
from gerberlicious.layer import Layer
from gerberlicious.aperture import CircleAperture
from gerberlicious.drawable import PointList, ApertureFlash

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
