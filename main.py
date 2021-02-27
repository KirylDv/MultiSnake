from pyglet.window import key

from configs import *
from game import Game

game = Game(FIELD_SIZE, PLAYERS)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.F5:
        game.reset(FIELD_SIZE, PLAYERS)
    elif symbol == key.PAUSE:
        game.finish()
    elif symbol == key.W:
        game.key_pressed((1, Side.north))
    elif symbol == key.UP:
        game.key_pressed((0, Side.north))
    elif symbol == key.A:
        game.key_pressed((1, Side.west))
    elif symbol == key.LEFT:
        game.key_pressed((0, Side.west))
    elif symbol == key.S:
        game.key_pressed((1, Side.south))
    elif symbol == key.DOWN:
        game.key_pressed((0, Side.south))
    elif symbol == key.D:
        game.key_pressed((1, Side.east))
    elif symbol == key.RIGHT:
        game.key_pressed((0, Side.east))
    elif symbol == key.ESCAPE:
        pyglet.app.exit()


@window.event
def on_draw():
    game.paint(window)


def main():
    fps = 10
    pyglet.clock.schedule_interval(game.run, 1 / fps)
    pyglet.app.run()


if __name__ == "__main__":
    main()
