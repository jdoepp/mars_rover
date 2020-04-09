#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mars_rover
import unittest
from unittest import mock

class NodeTests(unittest.TestCase):
    
    def test_node(self):
        node = mars_rover.Node('N')
        self.assertEqual(node.direction, 'N')
        self.assertEqual(node.left, None)
        self.assertEqual(node.right, None)

class DirectionsTests(unittest.TestCase):
    
    def setUp(self):
        self.directions = mars_rover.Directions()
    def test_add_notes(self):
        '''Test that the directions to the L and R of each direction are linked properly'''
        self.assertIsInstance(self.directions.nodes, dict)
        self.assertEqual(self.directions.n.left.direction, 'W')
        self.assertEqual(self.directions.n.right.direction, 'E')
        self.assertEqual(self.directions.s.left.direction, 'E')
        self.assertEqual(self.directions.s.right.direction, 'W')
        self.assertEqual(self.directions.e.left.direction, 'S')
        self.assertEqual(self.directions.e.right.direction, 'N')
        self.assertEqual(self.directions.w.left.direction, 'N')
        self.assertEqual(self.directions.w.right.direction, 'S')

    def test_get_node_from_val(self):
        '''Test that the correct node can be retrieved using the direction (N,S,W,E)'''
        north_node = self.directions.get_node_from_val('N')
        self.assertEqual(north_node.direction, 'N')
        south_node = self.directions.get_node_from_val('S')
        self.assertEqual(south_node.direction, 'S')
        west_node = self.directions.get_node_from_val('W')
        self.assertEqual(west_node.direction, 'W')
        east_node = self.directions.get_node_from_val('E')
        self.assertEqual(east_node.direction, 'E')

class PlateauTests(unittest.TestCase):
    '''Test the laying out of the matrix and transposition'''
    def setUp(self):
        self.plateau_2x4 = mars_rover.Plateau([1,3])
        self.plateau_4x4 = mars_rover.Plateau([3,3])
        self.plateau_6x6 = mars_rover.Plateau([5,5])

        self.assertEqual(self.plateau_4x4.size, (4,4))
        self.assertEqual(self.plateau_6x6.size, (6,6))
        self.assertEqual(self.plateau_2x4.size, (2,4))
    
    def test_transpose(self):
        '''
        A 4x4 grid transposed: plateau to matrix grid
             (0,3) (1,3) (2,3) (3,3)      (0,0) (0,1) (0,2) (0,3)
             (0,2) (1,2) (2,2) (3,2) ==>  (1,0) (1,1) (1,2) (1,3)       
             (0,1) (1,1) (2,1) (3,1)      (2,0) (2,1) (2,2) (2,3)       
             (0,0) (1,0) (2,0) (3,0) <==  (3,0) (3,1) (3,2) (3,3)  
             (x,y)                  reverse  

        2x4 grid
            (0,3) (1,3)     (0,0) (0,1)
            (0,2) (1,2)     (1,0) (1,1)
            (0,1) (1,1)     (2,0) (2,1)
            (0,0) (1,0)     (3,0) (3,1)
        '''
        location = [0, 0]
        new_location = self.plateau_6x6.transpose(*location)
        self.assertEqual(new_location, (5,0))

        new_location = self.plateau_4x4.transpose(*location)
        self.assertEqual(new_location, (3,0))

        new_location = self.plateau_2x4.transpose(*location)
        self.assertEqual(new_location, (3,0))

        new_location = self.plateau_4x4.transpose(*location, reverse=True)
        self.assertEqual(new_location, (0,3))

        location = [1, 2]
        new_location = self.plateau_6x6.transpose(*location)
        self.assertEqual(new_location, (3,1))

        new_location = self.plateau_4x4.transpose(*location)
        self.assertEqual(new_location, (1,1))

        new_location = self.plateau_2x4.transpose(*location)
        self.assertEqual(new_location, (1,1))
        
        new_location = self.plateau_6x6.transpose(*location, reverse=True)
        self.assertEqual(new_location, (2,4))

        new_location = self.plateau_4x4.transpose(*location, reverse=True)
        self.assertEqual(new_location, (2,2))

        new_location = self.plateau_2x4.transpose(*location, reverse=True)
        self.assertEqual(new_location, None)

        location = [2,0]
        new_location = self.plateau_2x4.transpose(*location)
        self.assertEqual(new_location, None)

    def test_set_value(self):
        self.plateau_6x6.set_value(3,3, 1)
        self.assertEqual(self.plateau_6x6.grid[3][3], 1)

if __name__ == "__main__":
    unittest.main()
