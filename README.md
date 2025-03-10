# MiniMax Overview
A program in Python to simulate a minimax algorithm used in checkers - an adversarial game. Success relies upon the player's ability to conduct strategic planning, exploit their opponent's weaknesses, and adapt to dynamic environments.

## Features

- User-selectable search depth (1-6)

- Predefined board states for mid-game and late-game scenarios

- Minimax AI decision-making for best move evaluation

- Move sequence tracking to display the best possible path to victory, loss, or draw

- Terminal state evaluation to determine the game's outcome

## How It Works

User selects Minimax search depth

Depth determines how many moves ahead the AI will consider.

Higher depth increases decision-making accuracy but slows down computation.

Recommended depth: 1-6 (Depth > 6 would significantly slow down processing.)

User selects a predefined board state

The board is displayed before evaluation.

Minimax evaluates the best possible outcome

If AI (X) wins → "AI (X) wins!"

If Player (O) wins → "Player (O) wins!"

If no winner is found → "It's a draw."

Best move sequence is displayed

The AI shows the step-by-step best move sequence leading to the game's outcome.

## Usage

Run the program

```python3 checkers.py```

## Example Output

Understanding Depth in Minimax:
1. Depth determines how many moves ahead the AI will look.
2. A higher depth means a smarter AI but takes longer to compute.
3. Typically, a depth of 2-4 is reasonable for Checkers at this stage of the game.
4. Going beyond depth 6 may slow down the AI significantly.
Enter Minimax search depth: 3

Choose a predefined board state:
Enter a number (1-8): 2

Here is the board you selected:
```
O . O . O . O .
. O . O . O . O
O . O . O . O .
. . . . . . . .
. . . . . . . .
. X . X . X . X
X . X . X . X .
. X . X . X . X
```

Best Possible Outcome:
AI (X) wins! (1)

Best Move Sequence to Achieve This Outcome:
Step 1: Move from (5,2) to (4,3)
Step 2: Move from (6,3) to (5,4)
...
