# CS 162 - Hasami Shogi 

This is a Python implementation of the board game Hasami Shogi - specifically, "Variant 1" of the game as described [on Wikipedia](https://en.wikipedia.org/wiki/Hasami_shogi). Players select either red or black, and control 9 identical pieces on a grid-shaped board. The goal of the game is to capture all opposing pieces; capturing is done by surrounding an enemy piece on either its horizontal or vertical edges. 

This was the final project for Oregon State's **CS 162 - Introduction to Computer Science II**. 

## Installation 
Simply download and run the file `HasamiShogiGame.py`. 

## Usage
The HasamiShogiGame class contains all game logic, and includes the following public methods: 
* **make_move(origin: str, destination:str)** - Takes two strings representing an origin and destination square, and moves the piece on origin to destination if move is valid. Returns "True" if move valid, "False" if invalid.
* **get_game_state()** - returns either 'UNFINISHED', 'RED_WON', or 'BLACK_ONE'
* **get_active_player()** - returns either 'RED' or 'BLACK'
* **get_num_captured_pieces(color: str)** - returns the number of pieces of a given color that have been captured
* **get_square_occupant(square: str)** - returns the occupant of the provided square (either 'RED', 'BLACK', or 'NONE').

An example of how to begin a game and make initial moves: 

```
game = HasamiShogiGame()
move_result = game.make_move('i5', 'e5') # returns True
print(game.get_active_player()) # returns 'RED'
print(game.get_square_occupant('a4')) # returns 'NONE'
print(game.get_game_state()) # returns 'UNFINISHED'
move_result = game.make_move('a4', 'e4')
```

After these moves, the board state would be as follows: 

```
  1 2 3 4 5 6 7 8 9
a R R R . R R R R R
b . . . . . . . . .
c . . . . . . . . .
d . . . . . . . . .
e . . . R B . . . .
f . . . . . . . . .
g . . . . . . . . .
h . . . . . . . . .
i B B B B . B B B B
```

