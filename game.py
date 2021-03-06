from functools import cmp_to_key

import pyglet

import configs as config
from apple import Apple
from field import Field
from player import Player


def comp(x, y):
    if x[0] < y[0]:
        return -1
    elif x[0] > y[0]:
        return 1
    elif x[1] > y[1]:
        return 1
    elif x[1] < y[1]:
        return -1
    else:
        return 0


class Game:
    def __init__(self, field_size=(80, 24), players=1):
        super(Game, self).__init__()
        self.__field = None
        self.__players = None
        self.__players_alive = None
        self.__apple = None
        self.in_loop = True
        self.max_score = 0
        self.reset(field_size, players)
        self.o_b_o = [0 for i in range(config.SPAWNED_SNAKES)]

    def run(self, dt=0.5):
        if self.__players_alive != 0:
            for snake in self.__players:
                snake.bot_way(self.__apple.get_coord(), self.__get_walls())
                snake.move()
            self.__check_collisions()

    def __get_walls(self):
        walls = set()
        for snake in self.__players:
            walls |= snake.get_body()
            walls |= {snake.get_head()}
        return walls

    def __check_collisions(self):
        # variables
        walls = set()
        snakes = set()
        heads = []
        for snake in self.__players:
            walls |= snake.get_body()
            heads.append(snake.get_head())
            snakes |= {snake.get_head()}
        snakes |= walls
        need_apple = False
        # food check
        for snake in self.__players:
            if snake.get_head() == self.__apple.get_coord():
                snake.eat()
                need_apple = True
                snakes |= {snake.get_tail()}
                walls |= {snake.get_tail()}
                if (self.__players_alive == 1) and snake.bot:
                    if (snake.get_score() > self.max_score) and (config.SPAWNED_SNAKES != 1):
                        snake.die()
                        self.__players_alive -= 1
                break
        if need_apple:
            self.__apple.gen_apple(snakes)
        # die. no more problems with heads. it wasn't so bad as i think
        for snake in self.__players:
            if snake.is_alive():
                if (snake.get_head() in walls) or \
                        self.__field.not_on_field(snake.get_head()) or \
                        heads.count(snake.get_head()) > 1:
                    snake.die()
                    self.__players_alive -= 1
                    self.max_score = max(snake.get_score(), self.max_score)

    def key_pressed(self, player, key):
        if not self.__players[player].bot:
            self.__players[player].change_direction(key)

    def __finish(self):
        self.reset(config.FIELD_SIZE, config.PLAYERS)
        print(sum(self.o_b_o))
        if sum(self.o_b_o) >= 10:
            pyglet.app.exit()

    def reset(self, field_size=(80, 24), players=1):
        self.__field = Field(*field_size)
        self.__players = [Player(*field_size, i + 1, *config.get_body_parts(i),
                                 config.SPAWNED_SNAKES + 1) for i in range(config.SPAWNED_SNAKES)]
        self.__players_alive = config.SPAWNED_SNAKES
        for player in self.__players[players:]:
            player.bot = True
            player.init_bot(self.__field)
            player.change_color(*config.get_body_parts(2))
        snakes = set()
        for snake in self.__players:
            snakes |= snake.get_body()
            snakes.update({snake.get_head()})
        self.__apple = Apple(*field_size, snakes)
        self.in_loop = True
        self.max_score = 0

    def paint(self):
        if self.__players_alive != 0:
            for snake in self.__players:
                snake.draw_snake()

            apple = pyglet.sprite.Sprite(config.apple_pic,
                                         x=self.__apple.get_coord()[0] * config.BLOCK_SIZE[0],
                                         y=self.__apple.get_coord()[1] * config.BLOCK_SIZE[1])
            apple.update(scale_x=config.SCALE_X, scale_y=config.SCALE_Y)
            apple.draw()
        else:
            self.__end_screen()

    def __end_screen(self):
        winners = []
        score = []
        for i in range(config.SPAWNED_SNAKES):
            score.append((self.__players[i].get_score(),
                          self.__players[i].life, i + 1))
        score = sorted(score, key=cmp_to_key(comp), reverse=True)
        for pl in score:
            if (pl[0] == score[0][0]) and (pl[1] == score[0][1]):
                winners.append(str(pl[2]))
                if self.in_loop:
                    self.o_b_o[pl[2] - 1] += 1
        self.in_loop = False

        text = ', '.join(winners)
        if len(winners) != 1:
            text = 'Draw! ' + text + ' best'
        else:
            text = 'Player ' + text + ' win'
        label1 = pyglet.text.Label(text,
                                   font_name='Times New Roman',
                                   font_size=72,
                                   x=300, y=600)
        label1.draw()
        label2 = pyglet.text.Label(f'Score: {score[0][0]}',
                                   font_name='Times New Roman',
                                   font_size=72,
                                   x=300, y=400)
        label2.draw()
        label3 = pyglet.text.Label(':'.join([str(sc) for sc in self.o_b_o]),
                                   font_name='Times New Roman',
                                   font_size=72,
                                   x=300, y=200)
        label3.draw()
