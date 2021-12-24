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
        self.exit_cell = pygame.image.load('/Users/jazzdiluffy/Desktop/JazzInterpreter/back/exit.png')
        self.robot_cell = pygame.image.load('/Users/jazzdiluffy/Desktop/JazzInterpreter/back/crab.png')
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
        width = height = 25
        size = 25
        time.sleep(0.05)
        pygame.display.update()
        self.window.fill((255, 255, 255))
        y = 0
        for row in range(len(self.map)):
            x = 0
            for cell in range(len(self.map[row])):
                # print(f'[{row},{cell}]')
                if self.map[row][cell].type == 'EMPTY':
                    if (cell == self.y) and (row == self.x):
                        # robot
                        self.window.blit(self.robot_cell, (x * size, y * size))
                        x += 1
                    else:
                        # road
                        pygame.draw.rect(self.window, (100, 100, 100), (x * size, y * size, width, height))
                        x += 1
                elif self.map[row][cell].type == 'EXIT':
                    self.window.blit(self.exit_cell, (x * size, y * size))
                    x += 1
                else:
                    # wall
                    self.window.blit(self.wall, (x * size, y * size))
                    x += 1
            y += 1
        pygame.display.update()

    def __repr__(self):
        return f'''\n x = {self.x}\n y = {self.y}\n turn: {look[str(self.turn)]}'''


    def wall(self):
        print(f"[WALL]: {self.x}, {self.y}")
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
        print(f"[EXIT]: {self.x}, {self.y}")
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
        print(f"[RIGHT]: {self.x}, {self.y}")
        self.turn = (self.turn+1) % 4
        a = 5

    def left(self):
        print(f"[LEFT]: {self.x}, {self.y}")
        self.turn = (self.turn-1) % 4

    def move(self, dist):
        print(f"[MOVE]: {self.x}, {self.y}")
        distance = self.wall()
        if dist > distance:
            return False
        if self.turn == 0:
            self.x += dist
        elif self.turn == 1:
            self.y += dist
        elif self.turn == 2:
            self.x -= dist
        elif self.turn == 3:
            self.y -= dist
        return True


if __name__ == '__main__':
    r = Robot(0, 0, 3, [])
    r.left()