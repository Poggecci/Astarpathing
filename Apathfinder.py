'''
A star pathing implementation.
g cost is the distance from the start to the current
h cost is from end to current
f cost is g + h
'''
import pygame
import math

size = (1000, 1000)
screen = pygame.display.set_mode(size)
rows = 50
columns = 50
width = size[0] // columns
height = size[1] // rows
openSet = []
closedSet = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
white = (255, 255, 255)
# grid creation
grid = [0 for a in range(columns)]
for a in range(len(grid)):
    grid[a] = [0 for b in range(rows)]


# Creates objects for every square of the grid we'll be pathing through
# includes functions that allows user to display the obstacles they mark

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g_cost = math.inf
        self.h_cost = 0
        self.f_cost = 0
        self.neighbors = []
        self.parent = None
        self.obstacle = False
        self.open = True
        self.value = 1

    # updates the color of a square in the grid if the node is open
    def show(self, color, border_width):
        if self.open:
            pygame.draw.rect(screen, color, (self.x * width, self.y * height, width, height), border_width)
            pygame.display.update()

    def path(self, color, border_width):
        pygame.draw.rect(screen, color, (self.x * width, self.y * height, width, height), border_width)
        pygame.display.update()

    def add_neighbors(self, grid):
        row = self.y
        column = self.x
        if row < rows - 1 and grid[row + 1][column].obstacle is False:
            self.neighbors.append(grid[row + 1][column])
        if row > 0 and grid[row - 1][column].obstacle is False:
            self.neighbors.append(grid[row - 1][column])
        if column < columns - 1 and grid[row][column + 1].obstacle is False:
            self.neighbors.append(grid[row][column + 1])
        if column > 0 and grid[row][column - 1].obstacle is False:
            self.neighbors.append(grid[row][column - 1])


def mouse_press():
    global columns
    global rows
    global start
    global end
    pos = pygame.mouse.get_pos()
    x_pos = pos[0]
    y_pos = pos[1]
    x_matrix = x_pos // width
    y_matrix = y_pos // height
    active = grid[y_matrix][x_matrix]
    if active != end and active != start:
        if active.obstacle is False:
            active.obstacle = True
            active.show(white, 0)


# uses distance as a heuristic to calculate the h cost
def heuristic(current_node, end_node):
    distance = ((end_node.y - current_node.y) ** 2 + (end_node.x - current_node.x) ** 2) ** 0.5
    #distance = abs(end_node.y - current_node.y) + abs(end_node.x - current_node.x)
    return distance


def main():
    openSet.append(start)
    start.g_cost = 0
    start.f_cost = heuristic(start, end)
    while True:
        if len(openSet) > 0:
            lowest_index = 0
            for a in range(len(openSet)):
                if openSet[a].f_cost < openSet[lowest_index].f_cost:
                    lowest_index = a
            current = openSet[lowest_index]
        current.add_neighbors(grid)
        if len(openSet) == 0:
            print('There is no accessible path')
            break
        openSet.pop(lowest_index)
        closedSet.append(current)
        for a in range(len(current.neighbors)):
            neighbor = current.neighbors[a]
            temp_g_cost = current.g_cost + current.value
            if neighbor.g_cost > temp_g_cost:
                neighbor.parent = current
                neighbor.g_cost = temp_g_cost
                neighbor.h_cost = heuristic(neighbor, end)
                neighbor.f_cost = neighbor.g_cost + neighbor.h_cost
                if neighbor not in openSet:
                    openSet.append(neighbor)
        closedSet.append(current)
        if current == end:
            print('The final f cost was:' + str(current.f_cost))
            while current != start:
                current.open = True
                current.show(red, 0)
                current = current.parent
            end.show(blue, 0)
            return


# making every item in the grid into an object of the class Square
for a in range(rows):
    for b in range(columns):
        grid[a][b] = Square(b, a)

# SHOW RECT
for column in range(columns):
    for row in range(rows):
        grid[row][column].show(white, 1)

while True:
    start = input('enter starting point coordinates:')
    end = input('enter end point coordinates:')
    start = start.split(',')
    end = end.split(',')
    try:
        start = grid[int(start[1])][int(start[0])]
        end = grid[int(end[1])][int(end[0])]
        break
    except:
        print('Coordinates are outside of the scope of the grid')

# main game loop
running = True
selecting = True
pathing = True
while running:
    start.show(blue, 0)
    end.show(blue, 0)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                selecting = False
        if event.type == pygame.QUIT:
            running = False
            break

        if pygame.mouse.get_pressed()[0] and selecting:
            mouse_press()
    if pathing and not selecting:
        main()
        pathing = False
    pygame.display.update()
