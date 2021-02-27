from random import randint


class Apple:
    def __init__(self, x_size, y_size, snakes):
        super(Apple, self).__init__()
        self.__x_size = x_size
        self.__y_size = y_size
        self.__x = 0
        self.__y = 0
        self.gen_apple(snakes)

    def gen_apple(self, snakes):
        while True:
            self.__x = randint(0, self.__x_size)
            self.__y = randint(0, self.__y_size)
            if (self.__x, self.__y) not in snakes:
                break

    def get_coord(self):
        return self.__x, self.__y
