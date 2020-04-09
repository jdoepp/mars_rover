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

def main():
    pass

if __name__ == '__main__':
    main()
