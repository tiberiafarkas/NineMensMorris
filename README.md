# Nine Men’s Morris

Python implementation of the classic board game **Nine Men’s Morris** with both **GUI** and **UI** versions, multiple play modes, and an AI opponent using the **Minimax algorithm with Alpha-Beta pruning**.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [GUI Version](#gui-version)
  - [UI Version](#ui-version)
- [AI Overview](#ai-overview)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)

---

## Features
- **Multiple play modes:**
  - Human vs Human
  - Human vs Computer 
  - Human vs AI (Minimax + Alpha-Beta)
- **Game phases:** Placing, Moving, Flying
- **AI opponent:**
  - **Point-Based AI:** Selects moves based on rewards for forming or blocking mills, creating opportunities, and removing opponent pieces strategically
  - **Minimax AI:** Uses Alpha-Beta pruning and a heuristic considering mills, mobility, and blocking opponent mills
- **GUI & UI versions:**
  - **GUI:** Click or drag pieces to move, interactive board
  - **UI:** Text-based board with letter-number coordinates (A–G, 1–7)
- Full **rule enforcement:** mill detection, piece removal, valid moves

---

## Installation

1. Ensure you have **Python 3.12** installed.

2. Install required libraries:

```bash
pip install tabulate numpy pygame pyfiglet
```

> `random`, `deepcopy`, `unittest`, `sys`, and `time` are part of the standard Python library.

---

## Usage

### GUI Version

1. Run the GUI script:

```bash
python gui.py
```

2. A page with rules and gameplay instructions will appear.

3. Press **Start**, then choose the desired level:
   - Human vs Human
   - Human vs Computer
   - Human vs AI (Minimax)

4. During gameplay:
   - Click or drag pieces to move them.
   - When removing a piece, click the piece to remove.

5. At the end, press **Restart** or **Quit**.

---

### UI Version

1. Run the UI script:

```bash
python ui.py
```

2. A title screen with rules and instructions will appear.

3. Press `1`, `2`, or `3` to select the level:
   - `1` = Human vs Human
   - `2` = Human vs Computer 
   - `3` = Human vs AI (Minimax)

4. Gameplay instructions:
   - **Stage 1 (Placing):** Enter the coordinates (letter + number) to place a piece (e.g., `A1`).
   - **Stage 2 (Moving):** First enter the piece you want to move (letter+number), then you will be asked to enter the destination (letter+number).
   - **Stage 3 (Flying):** Same as moving, but pieces can move to any empty valid position if only 3 remain.
   - **Removing a piece:** Enter the coordinates of the opponent piece to remove.

---

## AI Overview

### Point-Based AI Rewards

#### Placing Phase
- Block opponent mill → +600 points  
- Form own mill → +400 points  
- Form open mill → +1000 points  
- Get 2 pieces in a row → +200 points  
- Block opponent 2 in a row → +300 points  

**Removing opponent pieces during placing:**
- Remove piece in mill if opponent has only mills → +500 points  
- Remove piece which can help form a mill → +600 points  
- Remove piece which can block your mill → +500 points  
- Remove piece where there are 2 in a row → +400 points  
- Remove random piece → +100 points  

#### Moving Phase
- Form own mill → +500 points  
- Block opponent mill → +600 points  
- Block opponent 2 in a row → +300 points  
- Form 2 in a row → +400 points  
- Move 1 piece randomly → +100 points  
- Only valid move is to move from a mill → +50 points  

#### Flying Phase
- Form own mill → +500 points  
- Block opponent mill → +400 points  
- Block opponent 2 in a row → +200 points  
- Form 2 in a row → +300 points  
- Move 1 piece randomly → +100 points  

### Minimax AI
- **Algorithm:** Minimax with Alpha-Beta pruning  
- **Heuristic:** Considers mills formed, mobility of pieces, and blocking opponent mills  
- **Search depth:** 3 (default)  
- **Approximate board positions evaluated per move:** ~1,000 – 12,000 depending on the game phase

> Both AIs are functional; project is work-in-progress and can be further optimized.

---

## Project Structure
- `game.py` — Core game logic and rules  
- `ai.py` — Minimax AI implementation (Alpha-Beta, heuristic evaluations)
- `computer_player.py` - Point-Based AI
- `gui.py` — Graphical interface using Pygame (click/drag support)  
- `ui.py` — Text-based interface (console input with coordinates A–G,1–7)  
- `tests/` — Unit tests for game logic (if present)  

---

## Screenshots

- GUI Start Screen:  
![GUI Start Screen](assets/gui_start.png)

- GUI Gameplay (Placing / Moving / Flying):  
![GUI Gameplay](assets/gui_gameplay.png)

- UI Text Board example:  
![UI Board](assets/ui_board.png)

---


