from collections import deque

from pyglet.sprite import Sprite

from configs import Side, SCALE_X, SCALE_Y, BLOCK_SIZE


class Player:
    def __init__(self, x_size, y_size, team, body_sprite, head_sprites, parts):
        super(Player, self).__init__()
        self.__body = deque([(int(x_size / 2 - 2), int(y_size * team / parts)),
                             (int(x_size / 2 - 1), int(y_size * team / parts)),
                             (int(x_size / 2 + 0), int(y_size * team / parts))])
        self.__direction = Side.east
        self.body_sprite = body_sprite
        self.head_sprites = head_sprites
        self.__alive = True
        self.__head = (int(x_size / 2 + 1), int(y_size * team / parts))
        self.__last = self.__body[0]
        self.__score = len(self.__body)
        self.life = 0

    def move(self):
        if self.__alive:
            self.life += 1
            self.__body.append(self.__head)
            self.__head = (self.__head[0] + self.__direction.value[0],
                           self.__head[1] + self.__direction.value[1])
            self.__last = self.__body.popleft()

    def eat(self):
        self.__body.appendleft(self.__last)
        self.__score += 1

    def get_score(self):
        return self.__score

    def get_body(self):
        return set(self.__body)

    def get_head(self):
        return self.__head

    def get_direction(self):
        return self.__direction

    def is_alive(self):
        return self.__alive

    def change_direction(self, direction):
        if (self.__direction == Side.east) and (direction != Side.west):
            self.__direction = direction
        elif (self.__direction == Side.west) and (direction != Side.east):
            self.__direction = direction
        elif (self.__direction == Side.north) and (direction != Side.south):
            self.__direction = direction
        elif (self.__direction == Side.south) and (direction != Side.north):
            self.__direction = direction

    def die(self):
        self.__alive = False
        self.__body.clear()
        self.__head = None

    def draw_snake(self):
        if self.__alive:
            for block in self.__body:
                block_pic = Sprite(self.body_sprite,
                                   x=block[0] * BLOCK_SIZE[0],
                                   y=block[1] * BLOCK_SIZE[1])
                block_pic.update(scale_x=SCALE_X, scale_y=SCALE_Y)
                block_pic.draw()
            if self.__direction == Side.west:
                head_sprite = self.head_sprites.w
            elif self.__direction == Side.north:
                head_sprite = self.head_sprites.n
            elif self.__direction == Side.south:
                head_sprite = self.head_sprites.s
            else:
                head_sprite = self.head_sprites.e
            head_pic = Sprite(head_sprite,
                              x=self.__head[0] * BLOCK_SIZE[0],
                              y=self.__head[1] * BLOCK_SIZE[1])
            head_pic.update(scale_x=SCALE_X, scale_y=SCALE_Y)
            head_pic.draw()
