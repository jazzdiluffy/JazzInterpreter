import pygame
import time

look = {
    '0': 'right',
    '1': 'down',
    '2': 'left',
    '3': 'up'
}

cells = {
    ' ': 'EMPTY',
    'e': 'EXIT',
    'w': 'WALL'
}


class Cell():
    def __init__(self, type):
        self.type = type


    def __repr__(self):
        return f'{self.type}'


class Robot:
    def __init__(self, x, y, turn, map, window=None):
        self.x = x
        self.y = y
        self.turn = turn
        self.map = map
        self.wall_cell = pygame.image.load('/Users/jazzdiluffy/Desktop/JazzInterpreter/back/wall.png')
        self.wall_cell = pygame.transform.scale(self.wall_cell, (70, 70))
        self.exit_cell = pygame.image.load('/Users/jazzdiluffy/Desktop/JazzInterpreter/back/exit.png')
        self.exit_cell = pygame.transform.scale(self.exit_cell, (70, 70))
        self.grass_cell = pygame.image.load('/Users/jazzdiluffy/Desktop/JazzInterpreter/back/grass.png')
        self.grass_cell = pygame.transform.scale(self.grass_cell, (70, 70))
        self.robot_cell = pygame.image.load('/Users/jazzdiluffy/Desktop/JazzInterpreter/back/sprite.png')
        self.robot_cell = pygame.transform.scale(self.robot_cell, (70,70))
        self.window = window

    def show2(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if i == self.y and j == self.x:
                    print('ROBOT', end='  ')
                else:
                    print(self.map[i][j].type, end='  ')
            print()

    def show(self):
        size = 70
        time.sleep(1)
        pygame.display.update()
        self.window.fill((255, 255, 255))
        y = 0
        for row in range(len(self.map)):
            x = 0
            for cell in range(len(self.map[row])):
                if self.map[row][cell].type == 'EMPTY':
                    if (y == self.y) and (x == self.x):
                        # robot
                        self.window.blit(self.robot_cell, (x * size, y * size))
                        x += 1
                    else:
                        # empty
                        self.window.blit(self.grass_cell, (x * size, y * size))
                        x += 1
                elif self.map[row][cell].type == 'EXIT':
                    self.window.blit(self.exit_cell, (x * size, y * size))
                    x += 1
                else:
                    # wall
                    self.window.blit(self.wall_cell, (x * size, y * size))
                    x += 1
            y += 1

    def __repr__(self):
        return f'''\n x = {self.x}\n y = {self.y}\n turn: {look[str(self.turn)]}'''


    def wall(self):
        print("WALL")
        count = 1
        if self.turn == 0:
            while self.map[self.y][self.x+count].type == 'EMPTY':
                count += 1
        elif self.turn == 1:
            while self.map[self.y+count][self.x].type == 'EMPTY':
                count += 1
        elif self.turn == 2:
            while self.map[self.y][self.x-count].type == 'EMPTY':
                count += 1
        elif self.turn == 3:
            while self.map[self.y-count][self.x].type == 'EMPTY':
                count += 1
        return count - 1

    def exit(self):
        print("EXIT")
        count = 1
        flag = False
        if self.turn == 0:
            while self.map[self.y][self.x + count].type == 'EMPTY':
                count += 1
            if self.map[self.y][self.x+count].type == 'EXIT':
                flag = True
        elif self.turn == 1:
            while self.map[self.y + count][self.x].type == 'EMPTY':
                count += 1
            if self.map[self.y + count][self.x].type == 'EXIT':
                flag = True
        elif self.turn == 2:
            while self.map[self.y][self.x - count].type == 'EMPTY':
                count += 1
            if self.map[self.y][self.x - count].type == 'EXIT':
                flag = True
        elif self.turn == 3:
            while self.map[self.y - count][self.x].type == 'EMPTY':
                count += 1
            if self.map[self.y - count][self.x].type == 'EXIT':
                flag = True
        return flag

    def right(self):
        print("RIGHT")
        self.turn = (self.turn+1) % 4

    def left(self):
        print("LEFT")
        self.turn = (self.turn-1) % 4

    def move(self, dist):
        print("MOVE")
        distance = self.wall()
        if dist > distance:
            return False
        if self.turn == 0:
            for i in range(dist):
                self.x += 1
                self.show()
        elif self.turn == 1:
            for i in range(dist):
                self.y += 1
                self.show()
        elif self.turn == 2:
            for i in range(dist):
                self.x -= 1
                self.show()
        elif self.turn == 3:
            for i in range(dist):
                self.y -= 1
                self.show()
        return True


if __name__ == '__main__':
    r = Robot(0, 0, 3, [])
    r.left()