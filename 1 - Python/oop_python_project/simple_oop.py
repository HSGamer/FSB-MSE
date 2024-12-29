class Point:
    __numbers_of_points = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        type(self).__numbers_of_points += 1

    @classmethod
    def get_numbers_of_points(cls):
        return cls.__numbers_of_points

    def __str__(self):
        return f'Point({self.__x}, {self.__y})'

    def __del__(self):
        type(self).__numbers_of_points -= 1
        print('Object deleted')

    def __repr__(self):
        return f'Point({self.__x}, {self.__y})'

    @property
    def tuple(self):
        return self.__x, self.__y

point = Point(1, 2)
print(point)  # Point(1, 2)
print(point.tuple)  # (1, 2)
print(Point.get_numbers_of_points())  # 1
del point
print(Point.get_numbers_of_points())  # 0