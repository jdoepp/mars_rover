#!/usr/bin/env python
import os

class Node:
    '''Node for Linked list, having 3 attributes: direction and the nodes to the left and right'''
    def __init__(self, direction):
        self.direction = direction
        self.left = None
        self.right = None

class Directions:
    '''Linked list with nodes for the directions, and links to the direction to the left and right'''
    def __init__(self):
        self.add_nodes()
        self.nodes = {'N': self.n, 'S': self.s, 'W': self.w, 'E': self.e}
    def add_nodes(self):
        '''Add nodes with the corresponding left and right directions for each direction'''
        self.n = Node('N')
        self.s = Node('S')
        self.e = Node('E')
        self.w = Node('W')
        self.n.left, self.n.right = (self.w, self.e)
        self.s.left, self.s.right = (self.e, self.w)
        self.e.left, self.e.right = (self.n, self.s)
        self.w.left, self.w.right = (self.s, self.n)

    def get_node_from_val(self, value):
        return self.nodes[value.upper()]

class Plateau:
    '''A matrix (list of lists). The origin of the plateau is at the lower left corner. This requires the numberst to be transposed'''
    def __init__(self, top_right):
        self.top_right = top_right
        self.grid = [[0] * (self.top_right[0] + 1) for i in range(self.top_right[1] + 1)]
        self.size = len(self.grid[0]), len(self.grid)


    def transpose(self, x, y, reverse=False):
        '''Transposes from list of lists (row, column) to plateau (with (0,0) in bottom left corner). reverse=True will transpose the from plateau to lists'''
        if not reverse:
            if x > self.size[0] - 1:
                return None
            return self.size[1] - 1 - y, x
        else:
            if y > self.size[0] - 1:
                return None
            return y, self.size[0] - 1 - x

    def set_value(self, x, y, value):
        self.grid[x][y] = value

    

class Rover:
    '''The rover is on the plateau, with starting location, orientation (N,S,W,E)'''
    def __init__(self, x, y, orientation, plateau):
        self.plateau = plateau
        self.location = self.plateau.transpose(x,y)
        self.start_orientation = orientation
        self.current_orientation = Directions().get_node_from_val(orientation)
        directions = Directions()
        
        self.plateau.set_value(*self.location, 1)

    def change_loc(self,dest):
        '''Changes the value of the location on the plateau and change the location to dest'''
        self.plateau.set_value(*self.location, 0)
        self.location = dest
        self.plateau.set_value(*self.location, 1)
        
    def move(self):
        '''Moves the rover forward according to the direction it is facing'''
        if self.current_orientation.direction == 'N':
            dest = (self.location[0] - 1, self.location[1])
            if self.location[0] ==  0:
                print('You\'ve hit the boundary. Not moving!')
            elif self.plateau.grid[dest[0]][dest[1]] == 1:
                print('You can\'t move there; you\'ll hit another rover!')
            else:
                self.change_loc(dest)

        if self.current_orientation.direction == 'S':
            dest = (self.location[0] + 1, self.location[1])
            if self.location[0] == self.plateau.size[1] - 1:
                print('You\'ve hit the boundary. Not moving!')
            elif self.plateau.grid[dest[0]][dest[1]] == 1:
                print('You can\'t move there; you\'ll hit another rover!')
            else:
                self.change_loc(dest)

        elif self.current_orientation.direction == 'W':
            dest = (self.location[0], self.location[1] - 1)
            if self.location[1] == 0:
                print('You\'ve hit the boundary. Not moving!')
            elif self.plateau.grid[dest[0]][dest[1]] == 1:
                print('You can\'t move there; you\'ll hit another rover!')
            else:
                self.change_loc(dest)

        if self.current_orientation.direction == 'E':
            dest = (self.location[0], self.location[1] + 1)
            if self.location[1] == self.plateau.size[0] - 1:
                print('You\'ve hit the boundary. Not moving!')
            elif self.plateau.grid[dest[0]][dest[1]] == 1:
                print('You can\'t move there; you\'ll hit another rover!')
            else:
                self.change_loc(dest)

    def turn(self, direction):
        '''Changes the orientation of the rover on a left or right turn'''
        if direction == 'left':
            self.current_orientation = self.current_orientation.left
        elif direction == 'right':
            self.current_orientation = self.current_orientation.right
            
    def take_commands(self, commands):
        '''Takes an iterable (string) of commands of the letters 'm', 'l', and 'r' moving or turning right or left, and executes them'''
        for command in commands:
            if command.lower() == 'm':
                self.move()
            elif command.lower() == 'l':
                self.turn('left')
            elif command.lower() == 'r':
                self.turn('right')
        self.transposed_location = self.plateau.transpose(*self.location, reverse=True)



def create_tuple(top_right):
    '''Takes a string of two integers separated by a space, split and create a tuple of two integers'''
    try:
        return tuple(int(i) for i in top_right.split(' '))
    except Exception as e:
        print(e)
        return None, None

def get_rover_location(resp):
    '''Splits the location and orientation information for the rover'''
    try:
        resp = resp.split(' ')
        return  [int(i) for i in resp[:2]], resp[2] 
    except Exception as e:
        print(e)
        return None, None


def main():
    top_right = None
    allowed_commands = {'l','r','m'}
    rovers = []
    number_of_rovers = 2
    '''First create the grid for both rovers'''
    while not top_right:
        resp = input('Please enter top right location of plateau (n n): (quit to exit) ')
        if resp.lower == 'quit':
            os.exit(0)
        top_right = create_tuple(resp)
    plateau = Plateau(top_right)

    '''Adds rovers to the rovers list to the desired number (2)'''
    while True: 
        location = None
        commands = None
        if len(rovers) >= number_of_rovers:
            break
        while not location or not orientation:
            resp = input(f'Please enter the location and orientation of rover number {len(rovers) + 1} (n n [N][S][W][E]): ')
            location, orientation = get_rover_location(resp)
            transposed = plateau.transpose(*location) # Transpose also checks if the rover is in the area, and returns None if it is not
            if not transposed:
                print('The rover falls outside the area!')
                location = None
                continue
            '''If the value of the placement is 1, there is another rover in that location and it cannot be placed there'''
            if plateau.grid[transposed[0]][transposed[1]] == 1:
                print('That spot is taken by another rover!')
                location = None
        rover = Rover(*location, orientation, plateau)
        
        while not commands:
            '''Gets the commands to send to the rover'''
            resp = input('Enter directions for rover [L][R][M]:\n e.g: lmlmlmlmm\n ')
            if resp.lower() and set(resp.lower()) | allowed_commands == allowed_commands:
                commands = resp
        rover.take_commands(commands)
        rovers.append(rover)
    for rover in rovers:
        print('{} {}'.format(*rover.transposed_location), rover.current_orientation.direction)
    


    



if __name__ == '__main__':
    main()
