class Field:
    def __init__(self, x_size, y_size):
        super(Field, self).__init__()
        self.__x_size = x_size
        self.__y_size = y_size

    def not_on_field(self, point):
        flag = False
        if (point[0] < 0) or (point[0] > self.__x_size):
            flag = True
        if (point[1] < 0) or (point[1] > self.__y_size):
            flag = True
        return flag

    def get_x(self):
        return self.__x_size

    def get_y(self):
        return self.__y_size
