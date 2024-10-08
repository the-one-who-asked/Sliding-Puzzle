# Sliding Puzzle
A small, simple game written in python. It's a combination game that challenges the player to slide pieces along certain routes in order to get them in the right order. The player can choose the board size by enterring a number at the start (the number enterred will be the length of the board), with 3 being at easy difficulty, 4 at medium,  5 at hard and 7 at expert. Of course, the player can choose higher difficulties, lower difficulties or anything in between. Note that any size above 12 can take ages to shuffle (this is because the shuffle has a time complexity of O(n^3), which is necessary because not all random arrangements of pieces are solvable).

# Rules
A board is built with in a square arrangement of pieces, with one piece in the corner missing. The pieces on the board are then shuffled to create a random arrangement, but with pieces still labelled with their original order. The player must now slide pieces adjacent to the empty square into the empty square to swap the position of this piece with the position of the empty square. The player can push groups of pieces in the same row or column as the empty square to move them all in one direction at once. The player must continuously use these two techniques to get the pieces back into their original position.

Let's see how fast you can solve it!

Wikihow provides an elegant guide on how to solve [here](https://www.wikihow.com/Solve-Slide-Puzzles).

# Controls
Press *any key* (other than the contol keys listed below) to shuffle the board.

*Left*: Move the piece to the right of of the empty square left onto the empty square, essentially swapping that piece's position with that of the empty square.

*Right*: Move a piece right onto the empty square

*Up*: Move a piece up onto the empty square

*Down*: Move a piece down onto the empty square

You can also *click on a piece* to slide all pieces between that piece and the empty square (including the piece itself) onto the empty square.

Arrow key while holding *shift*: Slide an entire row, from the direction of the arrow you've chosen, onto the empty square

*Number key*: Choose the number of pieces that are slid onto the empty square when an arrow key is pressed while holding shift. The default is an entire row of pieces. You can press *0* to reset this number to the default (an entire row).

Use the *search bar* to search for a piece you can't find (this can be useful if you're playing with a large arrangement of pieces). The piece with the id enterred will be highlighted in yellow and the piece in the position which your selected piece your piece should be in will be highlighted in orange. If the piece is in the correct place, it will be highlighted in green.
