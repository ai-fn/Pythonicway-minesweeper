# Pythonic Minesweeper

Pythonic Minesweeper is a command-line implementation of the classic Minesweeper game using Python. It provides a fun and interactive way to play Minesweeper on the desktop.

## Features

- Customizable grid size and number of mines by level change
- Interactive gameplay with reveal and flag actions
- Real-time mine count updates
- Game over detection and win condition
- Color-coded grid display for enhanced visibility

## Requirements

- Python 3.x

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/ai-fn/Pythonicway-minesweeper.git
```
2. Navigate to the project directory:
```bash
cd Pythonicway-minesweeper
```
4. Run the game:
```python
python Pythonicway_Minesweeper.py
```

## How to Play

- Click left mouse button to reveal a cell.
- Click right mouse button to flag/unflag a cell.
- The number on each revealed cell represents the number of adjacent mines.
- Avoid clicking on mines. Revealing a mine ends the game.
- To win, flag all the mines and reveal all the safe cells.

## Customization

You can customize the game by modifying the following parameters in `Pythonicway_Minesweeper.py` settings:

- `Level`: Set the size of the grid and number of mines in the grid

Allowed levels (in format `level`: {grid size, number of mines}):
- `beginner`: {10, 16}
- `middle`: {16, 40}
- `pro`: {23, 99}


## Acknowledgements

This project was inspired by the classic Minesweeper game. Special thanks to the Python community for their continuous support and inspiration.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## Contact

For any questions or inquiries, please reach out to [isapsanov@list.ru](mailto:isapsanov@list.ru).

Enjoy the game!
