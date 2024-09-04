# 2048-game-using-pygame
This project is a recreation of the popular 2048 puzzle game, built using Pygame, a Python library for creating video games. The objective of the game is to slide numbered tiles on a grid to combine them and create a tile with the number 2048.
Features
Smooth Tile Movement: Tiles move fluidly across the grid in response to arrow key inputs, providing a seamless gameplay experience.
Tile Merging: When two tiles with the same number collide, they merge into one with double the value, just like in the classic 2048 game.
Random Tile Generation: After each move, a new tile (with a value of 2 or 4) is randomly placed on the grid, adding to the challenge.
Grid Outline and Design: The game features a clean and minimalistic design, with a well-defined grid and easy-to-read tile numbers.
Game Over Detection: The game detects when there are no more valid moves, resulting in a game over.
How to Play
Use the arrow keys (←, ↑, →, ↓) to slide the tiles across the grid.
Combine tiles of the same number to create larger numbered tiles.
Try to create a tile with the value of 2048 to win the game!
The game continues even after reaching 2048, allowing you to achieve higher scores.
Requirements
Python 3.x
Pygame library (pip install pygame)
Running the Game
Clone this repository:
bash
Copy code
git clone https://github.com/yourusername/2048-pygame.git
Navigate to the project directory:
bash
Copy code
cd 2048-pygame
Run the game:
bash
Copy code
python 2048.py
