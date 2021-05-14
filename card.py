class UnoCard:
    def __init__(self, color, number, type):
        """
        :param color: string
        :param number: int
        :param type: string
        """
        self.colors = ['red', 'yellow', 'blue', 'green']
        self.color = color
        self.number = number
        self.type = type  # type=None if number?

    def __get_color(self):
        # if change color / plus 4 => no color available
        return self.colors[self.color] if self.color else "no color available"

    def __get_number(self):
        return self.number if self.number else "no number available"

    def __get_type(self):
        return self.type

    def __is_functional(self):
        return self.type in {"plus2", "plus4", "stop", "change color"}


