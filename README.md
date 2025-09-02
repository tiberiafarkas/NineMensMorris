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
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484563684-bbcc966a-24fa-4fef-a1a1-bc12118713a4.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTY2NjMsIm5iZiI6MTc1NjgxNjM2MywicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjM2ODQtYmJjYzk2NmEtMjRmYS00ZmVmLWExYTEtYmMxMjExODcxM2E0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyMzI0M1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTk3NTQ5OGFmY2UxMmUzZmEwNWI2ZTUzMzJmYTJiYjc3NzY0NzEyZmVjZDJhYmI5NDI0ZTgyZWRiYmE4NjExMGImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.wyvkcuXDHv4K8vIZnEhwRzsfKPuxWECZq9yyZRyD-zo" />

- GUI Choose Level:
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484563823-e9a6cf69-bb4f-4d46-bd4e-d8cd9c7472a8.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTY5OTgsIm5iZiI6MTc1NjgxNjY5OCwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjM4MjMtZTlhNmNmNjktYmI0Zi00ZDQ2LWJkNGUtZDhjZDljNzQ3MmE4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyMzgxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTM2YTM1NmIwYWMwYzlkNjZkMTA2ZmI3MDE4ZGQwMTg5ODU2NzcxNzhiNDVlNmYxODZjZjU1YTFmNzk1ZDE3ZTEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.ay3IbFuS4td5YcLAPa6bVpJ-kC1uH9Uw5BTtJYQ7Tig"/>

- GUI Gameplay (Placing / Moving / Flying):  
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484564082-7c75e6f2-8c9c-42e0-b130-e8b0de487358.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTY5OTgsIm5iZiI6MTc1NjgxNjY5OCwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjQwODItN2M3NWU2ZjItOGM5Yy00MmUwLWIxMzAtZThiMGRlNDg3MzU4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyMzgxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY4ZDUzNGEyNzk0Njg5MzNhODJjYmZlYzJjNTFhZjlkZjE0YTAwNTY0Mzk2OGVmNTIwYWMwN2ZhODljY2E1MzcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.vraX1g8S6NshchtgmsVwQ78UQgSOKO9w9tm_dzHTSiI"/>
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484564219-d2b05de5-d484-44d9-bf70-f6a0644304eb.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTY5OTgsIm5iZiI6MTc1NjgxNjY5OCwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjQyMTktZDJiMDVkZTUtZDQ4NC00NGQ5LWJmNzAtZjZhMDY0NDMwNGViLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyMzgxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTVlYzA3YmNkYjQxY2QyODg0MGNhMjI1YWE0NTIyOTY5MDU4NzM1MzY1NDEyMzQyOTU3ZWI0MGFjNTg4Mjg3MTEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.ZB7DqOs-43T3JH5MzUTyB0zXHzJpLYJbTAnlmnO2Hf0"/>
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484564686-bf20e937-d950-448b-9c50-ab7727e8e3ee.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTY5OTgsIm5iZiI6MTc1NjgxNjY5OCwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjQ2ODYtYmYyMGU5MzctZDk1MC00NDhiLTljNTAtYWI3NzI3ZThlM2VlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyMzgxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTFlNzA5NDU2OTAxMDkyMmJlZmIyZGViMWM3NjNmN2ZmZGY0MmUxNTE3MjUxMzRjYjA1ZWUxMGVjZGQ5ZTU4ZmYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.X5Hbyy38QPyEPIV3AQnFnjoEokgzTXBe4VmyJQrtYNY"/>

- UI Start Screen:
<img width="400" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484565071-5cb25cee-69b8-466b-9f6f-9e682e327dc3.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTY5OTgsIm5iZiI6MTc1NjgxNjY5OCwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjUwNzEtNWNiMjVjZWUtNjliOC00NjZiLTlmNmYtOWU2ODJlMzI3ZGMzLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyMzgxOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTBiOTRjOWNlNzc4ZjVmZWYyZGM3ZGU2NTE2YzM1NGE1YmEzOTU3NjBjOWJlZDlhMzM1ZGMzZWQ4MGNjYmZmMzkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.VZrhiCc5FEX-2oTzVswF0xW8hj7rRswxAYtBAIWkKTc"/>
<img width="400" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484565135-85f07cc4-ca27-4519-b9b6-eb6055e7f286.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTcyODEsIm5iZiI6MTc1NjgxNjk4MSwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjUxMzUtODVmMDdjYzQtY2EyNy00NTE5LWI5YjYtZWI2MDU1ZTdmMjg2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyNDMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTdhY2Y4NGQxNjc3OWZkYzg3YjQwYWJiZWUzYjk0ZDcyNzE3NWRjZjkxNzJjOGRmM2FhOWNkODVjN2I2ZTM4YzQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.nXpCV8x0nNJiiw0ri8Djj0PAiAnIu0w5vvQtyPvp9_o"/>

- UI Text Board example:  
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484565224-654cf507-65bb-4527-adf8-8cd5e1fd7d5b.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTcyODEsIm5iZiI6MTc1NjgxNjk4MSwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjUyMjQtNjU0Y2Y1MDctNjViYi00NTI3LWFkZjgtOGNkNWUxZmQ3ZDViLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyNDMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTNjMjQ3ODZjYzVhNjcyNWFiN2U2NTk1NTMwNTU5MDQ2ZTk0ODVkNGY1NWVmMmFhZDg2MmRiYWFkZGY5NzMwMGImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.5TlL1HnJqpF6kezZ_MdZFVkwnTAMQxCfSaTdcWTKUpU"/>
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484565492-7f3678cb-c731-49cf-8b5b-8f258ed02fea.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTcyODEsIm5iZiI6MTc1NjgxNjk4MSwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjU0OTItN2YzNjc4Y2ItYzczMS00OWNmLThiNWItOGYyNThlZDAyZmVhLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyNDMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTc3ZTA0NzIyYTA3MzgzMTc0ZDQwMWVmYjUzNDFmZWNmYmRjMDg2NWFmODUyOTQxMThjZmY0ZDhiNDFmMzliY2ImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.hcwggfSGcFxNLiVG8Gxhe4FaywS7-4Pv9WYVtHyRky8"/>
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484565790-79c31445-ebb1-4816-977a-91f099a7cd88.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTcyODEsIm5iZiI6MTc1NjgxNjk4MSwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjU3OTAtNzljMzE0NDUtZWJiMS00ODE2LTk3N2EtOTFmMDk5YTdjZDg4LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyNDMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWEwMDEyNjYyYjQ1MTYzMDRiMjAyYzBkZjg1NTQ0NDgzMTI1MmNkOWNiZjc4YjhiMzExMzBkZTE5NDVjNDcxMDcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.sbkppH4_TAxxR5_-99nZwhlsVKthVeHYma9vy52nHBE"/>
<img width="300" alt="image" src="https://private-user-images.githubusercontent.com/93712786/484565871-659ae138-6395-4fef-9c57-aa4a0dfc24bb.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTY4MTcyODEsIm5iZiI6MTc1NjgxNjk4MSwicGF0aCI6Ii85MzcxMjc4Ni80ODQ1NjU4NzEtNjU5YWUxMzgtNjM5NS00ZmVmLTljNTctYWE0YTBkZmMyNGJiLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA5MDIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwOTAyVDEyNDMwMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTc0MTFhYzZhNTdiNTRiYjlhNmMzMGVkYzNhM2Q5ZmIxYzhmMGQxODRkYTFiYjkwODkyZTUyMDBjOTczMjE0NDgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.VeJkNIrz91ug3KLwP30Yb_rT6LnPWmqJOSSoUbpaSG0"/>

---


