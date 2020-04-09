#!/usr/bin/env python

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
        self.e.left, self.e.right = (self.s, self.n)
        self.w.left, self.w.right = (self.n, self.s)

    def get_node_from_val(self, value):
        return self.nodes[value]

class Plateau:
    '''A matrix (list of lists). The origin of the plateau is at the lower left corner. This requires the numberst to be transposed'''
    def __init__(self, top_right):
        self.grid = [[0] * (top_right[0] + 1)] * (top_right[1] + 1)
        self.size = len(self.grid[0]), len(self.grid)

    def transpose(self, x, y, reverse=False):
        '''Transpose from list of lists (row, column) to plateau (with (0,0) in bottom left corner). reverse=True will transpose the from plateau to lists'''
        if not reverse:
            if x > self.size[0] - 1:
                return None
            return self.size[1] - 1 - y, x
        else:
            if y > self.size[0] - 1:
                return None
            return y, self.size[0] - 1 - x

    def set_value(self, x, y, value):
        print(x,y,value)
        self.grid[x][y] = value
    

def main():
    pass

if __name__ == '__main__':
    main()
