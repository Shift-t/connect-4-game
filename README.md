# CLI Connect 4 Game in Python

This repository contains a command-line interface (CLI) implementation of the classic Connect 4 game, written in Python. The game supports two local players, features falling piece terminal animations, tracks game statistics, and saves high scores to a leaderboard file across sessions.

---

## Setup and How to Play

### Prerequisites
*   Python 3.x installed on your operating system.
*   A terminal/console emulator supporting screen clearing commands (`clear` or `cls`).

### Running the Game
To run the game, navigate to the repository directory in your terminal and execute:

```bash
python3 connect4.py
```

> [!WARNING]
> **Terminal Compatibility Limitation:** Running the game inside IDE consoles (like PyCharm's default output window) fails to clear the screen properly and outputs raw ANSI escape codes (like `\x1b[2J`). It is highly recommended to run the script in a native system terminal (such as bash or cmd.exe) to ensure proper screen rendering.

### Gameplay Instructions
1.  **Start-up:** The program prompts Player 1 and Player 2 to input their names and custom piece characters (limited to 1 character, cannot be empty or identical).
2.  **Taking Turns:** Players alternate entering a column index (`1` through `7`) to drop their piece.
3.  **Winning:** The first player to align four of their pieces wins the game, and their score is written to `High_Scores.txt`.
4.  **Game Over:** After a game ends (or resulting in a draw), you can choose to replay by entering `Y` or quit by entering `N`, which outputs the final scoreboard.

---

## Functional Components Overview

The game follows a modular structure, separating screen rendering, move validation, win checking, and file score-saving into distinct subroutines:

| Component / Function | Responsibility | Operation Details |
| :--- | :--- | :--- |
| `start(empty)` | Game Setup & UI | Prints the start header, calls instructions, and obtains player settings. |
| `get_users(empty)` | User Registration | Prompts for player names (max 16 characters) and custom token symbols (1 character). |
| `printboard(the_board)` | Console Rendering | Clears the terminal screen and draws the updated board state. |
| `check_full(the_board, empty)` | Draw Validation | Checks if any empty slots remain on the board; declares a draw if full. |
| `check_input()` | Move Input Validation | Ensures column choices are integers strictly between 1 and 7. |
| `insert_piece(...)` | Piece Physics & Animation | Places a token in the lowest empty row of the chosen column and animates the fall. |
| `taketurn(...)` | Round Management | Coordinates column inputs, piece placement, win checking, and turn-switching. |
| `check_win(...)` | Win Orchestrator | Checks horizontal, vertical, and diagonal win configurations, calculating scores on a win. |
| `update_scores(...)` | Score Leaderboard Update | Appends and sorts player names and scores in descending order in the score file. |
| `print_scores()` | Leaderboard Visualizer | Formats and displays the historical high scores when the program exits. |

---

## File Structure

*   `connect4.py`: The main game source file containing the loop, input/output validation, animations, and scoring logic.
*   `High_Scores.txt`: Text file storing player high scores in descending order.

---

## Detailed Specifications

### Winning Condition Checking
The game checks four win orientations after each move:
1.  **Horizontal:** Searches for 4 consecutive tokens in any row.
2.  **Vertical:** Searches for 4 consecutive tokens in any column.
3.  **Diagonal Left-to-Right:** Searches for 4 consecutive tokens along a diagonal ascending from left to right.
4.  **Diagonal Right-to-Left:** Searches for 4 consecutive tokens along a diagonal descending from left to right.

### Dynamic Animation
The falling animation is achieved by printing the board at successive intervals while shifting the token row index downwards, pausing briefly for `0.15` seconds before erasing the temporary cell state.

### Score Calculation
Scores are calculated dynamically to reward efficiency:
$$\text{Score} = 1120 - \left(\lfloor \frac{\text{Turns Taken}}{2} \rfloor \times 40\right)$$
The maximum possible score is 1000, and points decrease as the number of turns taken to win increases.
