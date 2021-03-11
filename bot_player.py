from random import randint, choice, shuffle, random

from configs import Side
from helpers import PriorityQueue

RANDOM_CHANCE = 0.05


class RandomBot:
    def __init__(self, field=None):
        self.__direction = randint(0, 3)

    def get_move(self, apple=None, head=None, maze=None):
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
        self.__direction = Side.east

    def get_move(self, apple, head, maze=None):
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


class UpgradedPointToAppleBot:
    def __init__(self, field):
        self.field = field
        self.__direction = Side.east

    def get_move(self, apple, head, maze):
        temp = []
        directions = [(head[0] + 1, head[1] + 0),  # east
                      (head[0] - 1, head[1] + 0),  # west
                      (head[0] + 0, head[1] + 1),  # north
                      (head[0] + 0, head[1] - 1)]  # south
        if (apple[1] > head[1]) and (self.__direction != Side.south):
            if (directions[2] not in maze) and self.field.on_field(directions[2]):
                temp.append(Side.north)

        if (apple[0] > head[0]) and (self.__direction != Side.west):
            if (directions[0] not in maze) and self.field.on_field(directions[0]):
                temp.append(Side.east)

        if (apple[1] < head[1]) and (self.__direction != Side.north):
            if (directions[3] not in maze) and self.field.on_field(directions[3]):
                temp.append(Side.south)

        if (apple[0] < head[0]) and (self.__direction != Side.east):
            if (directions[1] not in maze) and self.field.on_field(directions[1]):
                temp.append(Side.west)

        if len(temp) != 0:
            self.__direction = choice(temp)
        else:
            directs = [Side.east, Side.west, Side.north, Side.south]
            neighbours = []
            for i in range(4):
                node = directions[i]
                if (node not in maze) and self.field.on_field(node):
                    neighbours.append(directs[i])
            if len(neighbours) != 0:
                self.__direction = choice(neighbours)
            else:
                self.__direction = choice(directs)

        return self.__direction


class AStarBot:
    def __init__(self, field):
        self.head = None
        self.field = field
        self.apple = None

    def get_move(self, apple, head, maze):
        self.apple = apple
        self.head = head
        if random() < RANDOM_CHANCE:
            direction = self.__panic_mode(maze)
        else:
            direction = self.a_star(maze)
        return direction

    def __calc_h(self, coord):
        return abs(self.apple[0] - coord[0]) + abs(self.apple[1] - coord[1])

    def __panic_mode(self, maze):
        directions = [Side.east, Side.west, Side.north, Side.south]
        neighbours = []
        temp = [(self.head[0] + 1, self.head[1] + 0),  # east
                (self.head[0] - 1, self.head[1] + 0),  # west
                (self.head[0] + 0, self.head[1] + 1),  # north
                (self.head[0] + 0, self.head[1] - 1)]  # south
        for i in range(4):
            node = temp[i]
            if (node not in maze) and self.field.on_field(node):
                neighbours.append(directions[i])
        if len(neighbours) != 0:
            direction = choice(neighbours)
        else:
            direction = choice(directions)
        return direction

    def a_star(self, maze):
        open_nodes = PriorityQueue()
        open_nodes.push(0, self.head)
        came_from = dict()
        path_cost = dict()
        came_from[self.head] = None
        path_cost[self.head] = 0

        while not open_nodes.empty():
            current = open_nodes.pop()

            if current[1] == self.apple:
                break

            neighbours = []
            temp = [(current[1][0] + 1, current[1][1] + 0),  # east
                    (current[1][0] - 1, current[1][1] + 0),  # west
                    (current[1][0] + 0, current[1][1] + 1),  # north
                    (current[1][0] + 0, current[1][1] - 1)]  # south
            shuffle(temp)
            for node in temp:
                if (node not in maze) and self.field.on_field(node):
                    neighbours.append(node)

            for next_node in neighbours:
                new_cost = path_cost[current[1]] + 1
                if (next_node not in path_cost) or (new_cost < path_cost[next_node]):
                    path_cost[next_node] = new_cost
                    cost = new_cost + self.__calc_h(next_node)
                    open_nodes.push(cost, next_node)
                    came_from[next_node] = current[1]

        node = self.apple
        try:
            while came_from[node] != self.head:
                node = came_from[node]
        except KeyError:
            return self.__panic_mode(maze)

        direction = None
        if node[0] < self.head[0]:
            direction = Side.west
        elif node[0] > self.head[0]:
            direction = Side.east
        elif node[1] > self.head[1]:
            direction = Side.north
        elif node[1] < self.head[1]:
            direction = Side.south

        return direction
