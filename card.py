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

    def get_color(self):
        # if change color / plus 4 => no color available
        if self.color in range(0, 4):
            return self.colors[self.color]
        else:
            return None

    def get_number(self):
        return self.number

    def get_type(self):
        return self.type

    def is_functional(self):
        return self.type in {"plus2", "plus4", "stop", "change color"}

    def is_plus(self):
        if self.type.startswith('plus'):
            return int(self.type.replace('plus'))
        return 0

    def __str__(self):
        s = ''
        if self.color is not None:
            s += f'{self.get_color()}'
        if self.number is not None:
            s += f' {self.get_number()}'
        if self.type is not None:
            if self.type == 'plus2' or self.type == 'stop':
                s += f' {self.get_type()}'
            elif self.type == 'plus4' or self.type == 'change color':
                s += f'{self.get_type()}'
        return s

    def set_color(self):
        assert self.type == 'change color' or self.type == 'plus4'