## Project 2: Adversarial Search and Games

### I. Introduction

An instance of the 2048-puzzle game is played on a 4×4 grid, with numbered tiles that slide in all four directions when a player moves them. Every turn, a new tile will randomly appear in an empty spot on the board, with a value of either 2 or 4. Per the input direction given by the player, all tiles on the grid slide as far as possible in that direction, until they either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide while moving, they will merge into a single tile, valued at the sum of the two original tiles that collided. The resulting tile cannot merge with another tile again in the same move.

In the first assignment, you had ample experience with the process of abstracting ideas and designing functions, classes, and data structures. The goal was to get familiar with how objects, states, nodes, functions, and implicit or explicit search trees are implemented and interact in practice. This time, the focus is strictly on the ground-level details of the algorithms. You will be provided with all the skeleton code necessary to get started, so that you can focus solely on optimizing your algorithm.

With typical board games like chess, the two players in the game (i.e. the "Computer AI" and the "Player") take similar actions in their turn, and have similar objectives to achieve in the game. In the 2048-puzzle game, the setup is inherently asymmetric; that is, the computer and player take drastically different actions in their turns. Specifically, the computer is responsible for placing random tiles of 2 or 4 on the board, while the player is responsible for moving the pieces. However, adversarial search can be applied to this game just the same.

### II. Algorithm Review

Before you begin, review the lecture slides on adversarial search. Is this a zero-sum game? What is the minimax principle? In the 2048-puzzle game, the computer AI is technically not "adversarial". In particular, all it does is spawn random tiles of 2 and 4 each turn, with a designated probability of either a 2 or a 4; it certainly does not specifically spawn tiles at the most inopportune locations to foil the player's progress. However, we will create a "Player AI" to play as if the computer is completely adversarial. In particular, we will employ the minimax algorithm in this assignment.
Remember, in game-playing we generally pick a strategy to employ. With the minimax algorithm, the strategy assumes that the computer opponent is perfect in minimizing the player's outcome. Whether or not the opponent is actually perfect in doing so is another question. As a general principle, how far the actual opponent's actual behavior deviates from the assumption certainly affects how well the AI performs. However, you will see that this strategy works well in this game. In this assignment, we will implement and optimize the minimax algorithm.

### III. Using The Skeleton Code

To let you focus on the details of the algorithm, a skeleton code is provided to help you get started, and to allow you to test your algorithm on your own. The skeleton code includes the following files. Note that you will only be working in one of them, and the rest of them are read-only:

- Read-only: `GameManager.py`. This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other. See below on how to execute this program.
- Read-only: `Grid.py`. This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.
- Read-only: `BaseAI.py`. This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).
- Read-only: `ComputerAI.py`. This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.
- Writable: `PlayerAI.py`. You will create this file, and this is where you will be doing your work. This should inherit from BaseAI. The getMove() function, which you will need to implement, returns a number that indicates the player’s action. In particular, 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", and 3 stands for "Right". You need to create this file and make it as intelligent as possible. You may include other files in your submission, but they will have to be included through this file.
- Read-only: `BaseDisplayer.py` and `Displayer.py`. These print the grid.
.
To test your code, execute the game manager like so:
`$ python3 GameManager_3.py`