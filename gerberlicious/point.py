
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


