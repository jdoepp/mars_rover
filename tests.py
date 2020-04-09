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


        

if __name__ == "__main__":
    unittest.main()
