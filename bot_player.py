from random import randint, choice

from configs import Side


class RandomBot:
    def __init__(self, field=None):
        self.__direction = randint(0, 3)

    def get_move(self, apple=None, head=None, map=None):
        temp = Side.west
        if self.__direction == 0:
            temp = Side.north
        elif self.__direction == 1:
            temp = Side.east
        elif self.__direction == 2:
            temp = Side.south
        self.__direction = randint(0, 3)
        return temp


class PointToAppleBot:
    def __init__(self, field=None):
        self.head_x = None
        self.head_y = None
        self.apple_x = None
        self.apple_y = None
        self.__direction = Side.east

    def get_move(self, apple, head, map=None):
        temp = [self.__direction]
        if (apple[1] > head[1]) and (self.__direction != Side.south):
            temp.append(Side.north)
        if (apple[0] > head[0]) and (self.__direction != Side.west):
            temp.append(Side.east)
        if (apple[1] < head[1]) and (self.__direction != Side.north):
            temp.append(Side.south)
        if (apple[0] < head[0]) and (self.__direction != Side.east):
            temp.append(Side.west)
        self.__direction = choice(temp)
        return self.__direction
