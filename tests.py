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
        '''Tests that the directions to the L and R of each direction are linked properly'''
        self.assertIsInstance(self.directions.nodes, dict)
        self.assertEqual(self.directions.n.left.direction, 'W')
        self.assertEqual(self.directions.n.right.direction, 'E')
        self.assertEqual(self.directions.s.left.direction, 'E')
        self.assertEqual(self.directions.s.right.direction, 'W')
        self.assertEqual(self.directions.e.left.direction, 'N')
        self.assertEqual(self.directions.e.right.direction, 'S')
        self.assertEqual(self.directions.w.left.direction, 'S')
        self.assertEqual(self.directions.w.right.direction, 'N')

    def test_get_node_from_val(self):
        '''Tests that the correct node can be retrieved using the direction (N,S,W,E)'''
        north_node = self.directions.get_node_from_val('N')
        self.assertEqual(north_node.direction, 'N')
        south_node = self.directions.get_node_from_val('S')
        self.assertEqual(south_node.direction, 'S')
        west_node = self.directions.get_node_from_val('W')
        self.assertEqual(west_node.direction, 'W')
        east_node = self.directions.get_node_from_val('E')
        self.assertEqual(east_node.direction, 'E')

class PlateauTests(unittest.TestCase):
    '''Tests the laying out of the matrix and transposition'''
    def setUp(self):
        self.plateau_2x4 = mars_rover.Plateau([1,3])
        self.plateau_4x4 = mars_rover.Plateau([3,3])
        self.plateau_6x6 = mars_rover.Plateau([5,5])

        self.assertEqual(self.plateau_4x4.size, (4,4))
        self.assertEqual(self.plateau_6x6.size, (6,6))
        self.assertEqual(self.plateau_2x4.size, (2,4))
    
    def test_transpose(self):
        '''
        Tests the location of the grid transposed from the source at lower left corner, and from x,y to row, column

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


class RoverTests(unittest.TestCase):
    def setUp(self):
        self.plateau = mars_rover.Plateau([5,5])
        self.start_location = [1,2]
        self.rover = mars_rover.Rover(*self.start_location, 'N', self.plateau)

        self.assertEqual(self.rover.location, (3,1))
        self.assertEqual(self.plateau.grid[3][1], 1)
        self.assertEqual(self.rover.current_orientation.direction, 'N')
    
    def test_change_loc(self):
        dest = (3,2)
        self.rover.change_loc(dest)
        self.assertEqual(self.plateau.grid[3][1], 0)
        self.assertEqual(self.plateau.grid[3][2], 1)


    def test_move(self):
        '''Test the move function of the rover in different directions, checking the new location'''
        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(*self.start_location, 'N', self.plateau)
        self.rover.move()
        self.assertEqual(self.rover.location, (2,1))

        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(*self.start_location, 'S', self.plateau)
        self.rover.move()
        self.assertEqual(self.rover.location, (4,1))

        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(*self.start_location, 'W', self.plateau)
        self.rover.move()
        self.assertEqual(self.rover.location, (3,0))

        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(*self.start_location, 'E', self.plateau)
        self.rover.move()
        self.assertEqual(self.rover.location, (3,2))

        '''If it reaches the edge it should remain in place'''
        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(0,0, 'S', self.plateau)
        self.assertEqual(self.rover.location, (5,0))
        self.rover.move()
        self.assertEqual(self.rover.location, (5,0))

        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(0,0, 'W', self.plateau)
        self.assertEqual(self.rover.location, (5,0))
        self.rover.move()
        self.assertEqual(self.rover.location, (5,0))

        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(0,5, 'N', self.plateau)
        self.assertEqual(self.rover.location, (0,0))
        self.rover.move()
        self.assertEqual(self.rover.location, (0,0))

        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(5,5, 'E', self.plateau)
        self.assertEqual(self.rover.location, (0,5))
        self.rover.move()
        self.assertEqual(self.rover.location, (0,5))

    def test_turn(self):
        '''Tests left and right turns for each orientation'''
        self.rover = mars_rover.Rover(*self.start_location, 'N', self.plateau)
        self.rover.turn('left')
        self.assertEqual(self.rover.current_orientation.direction, 'W')

        self.rover = mars_rover.Rover(*self.start_location, 'N', self.plateau)
        self.rover.turn('right')
        self.assertEqual(self.rover.current_orientation.direction, 'E')

        self.rover = mars_rover.Rover(*self.start_location, 'S', self.plateau)
        self.rover.turn('left')
        self.assertEqual(self.rover.current_orientation.direction, 'E')

        self.rover = mars_rover.Rover(*self.start_location, 'S', self.plateau)
        self.rover.turn('right')
        self.assertEqual(self.rover.current_orientation.direction, 'W')

        self.rover = mars_rover.Rover(*self.start_location, 'W', self.plateau)
        self.rover.turn('left')
        self.assertEqual(self.rover.current_orientation.direction, 'S')

        self.rover = mars_rover.Rover(*self.start_location, 'W', self.plateau)
        self.rover.turn('right')
        self.assertEqual(self.rover.current_orientation.direction, 'N')

        self.rover = mars_rover.Rover(*self.start_location, 'E', self.plateau)
        self.rover.turn('left')
        self.assertEqual(self.rover.current_orientation.direction, 'N')

        self.rover = mars_rover.Rover(*self.start_location, 'E', self.plateau)
        self.rover.turn('right')
        self.assertEqual(self.rover.current_orientation.direction, 'S')
    
    def test_take_commands(self):
        self.plateau = mars_rover.Plateau([5,5])
        self.rover = mars_rover.Rover(*self.start_location, 'N', self.plateau)
        self.rover.take_commands('mmlr')
        print(self.rover.location)
        print(self.rover.transposed_location)
        print(self.rover.current_orientation.direction)
        self.assertEqual(self.rover.location, (1,1))
        self.assertEqual(self.rover.transposed_location, (1,4))
        self.assertEqual(self.rover.orientation.direction, 'N')



if __name__ == "__main__":
    unittest.main()
