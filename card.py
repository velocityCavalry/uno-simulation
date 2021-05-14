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
        return self.colors[self.color]

    def __get_number(self):
        return self.number

    def __get_type(self):
        return self.type

    def __is_functional(self):
        return self.type in {"plus2", "plus4", "stop", "change color"}

    def get_num_plus(self):
        if self.type.startswith('plus'):
            return int(self.type.replace('plus'))

    def __str__(self):
        s = ''
        if self.color is not None:
            s += f'{self.__get_color()}'
        if self.number is not None:
            s += f' {self.__get_number()}'
        if self.type is not None:
            s += f' {self.__get_type()}'
        return s

