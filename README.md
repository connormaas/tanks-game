# Tanks Game

A 2D tank battle in Python. Steer through randomized obstacles, bank missiles off walls, and survive CPU tanks that hunt you down and dodge your shots.

**Demo:** [watch on YouTube](https://www.youtube.com/watch?v=2mKSOPMFp-k)

One of my first big programs, built in 2020.

## Features

- **8 direction movement** for every tank
- **Mouse aiming** with missiles that bounce off walls and obstacles
- **Levels** that bring faster tanks, faster missiles, and new enemy types
- **Randomized maps** that change every level
- **Enemies**
  - **Shooter tank:** dodges your missiles and fires back
  - **Attack tank:** charges at you and explodes on contact

## Code

- `tanks.py`: game loop, input, enemy AI, collisions, levels, and scoring
- `graphics.py`: a modified version of CMU's tkinter based [cmu_112_graphics](https://www.cs.cmu.edu/~112/notes/notes-graphics.html)
- `images/`: sprites

## Run It

```bash
git clone https://github.com/connormaas/tanks-game.git
cd tanks-game
pip install -r requirements.txt
python tanks.py
```

Tested on Python 3.7.
