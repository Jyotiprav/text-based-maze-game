# Text-based-maze-game
This game includes following functions:
## make_grid(): 
Given two integers width w and height h, append sublists into the variable "grid" to make a maze of the specified width and height. The coordinates for the player and the gold is also given as two two-element tuples. For each tuple, the first element has the x-coordinate and the second element has the y-coordinate. The player and the gold should be included in the grid in the positions specified by these tuples.
The player is represented with the string '(x)'
The gold is represented with the string '(o)'
All other spaces are represented with the string '(_)'
This function does not return anything. It just modifies the "grid" list, by appending to it.
## update_grid():
Given the player's current position as px and py,and the directional changes in dx and dy, update the "grid" to change the player's x-coordinate by dx, and their y-coordinate by dy.
More information:
Use the given w and h (representing the grid's width and height) to figure out whether or not the move is valid. If the move is not valid (that is, if it is outside of the grid's boundaries), then NO change occurs to the grid. The grid stays the same, and nothing is returned. If the move IS possible, then the grid is updated by adding dx to the player's x-coordinate, and adding dy to the player's y-coordinate. The new position in the grid is changed to the player icon '(x)', and the old position the player used to be in is changed to an empty space '(_)'. The new x- and y- coordinates of the player is returned as a tuple.
## get_moves():
Given a direction that is either 'N', 'S', 'E' or 'W' (standing for North, South, East or West), return a tuple representing the changes that would occur to the x- and y- coordinates if a move is made in that direction.e.g. If d is 'W', that means the player should move
to the left. In order to do so, their x-coordinate should decrease by 1. Their y-coordinate should stay the same.
These changes can be represented as the tuple (-1, 0), because the x-coordinate would have -1 added to it, and the y-coordinate would have 0 added to it

   
