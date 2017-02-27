

# Py2016

The project of Python 2016 Course.

This is a mini game **Shift**, written by **Python**, using *pygame* library.

## Requirements

Python 3 (3.4 / 3.5)

Pygame 1.9.2a0

## Start

Open the *Py2016* directory, and run *main.py*.
You can also run *main.py* in other directories.

Such as this:

```bash
    cd Py2016
    python3 main.py
    # or python main.py if your default python is python3.
    # or ./main.py on unix.
```

## How To Play

The main window of the game is a menu. You can start a new game(clear all records), continue a past game,
open an editor (not implemented), show helps, select levels, and quit game.

After clicking **New Game** or **Continue**, you will enter the level select screen. You can select a level here.

The rules of the game are simple and are very easy to learn.

Key `Left arrow` is left.
Key `Right arrow` is right.
Key `Up arrow` or `Space` is jump.
Key `Shift` will shift to another world.

More details can be seen in `config/keymap.txt`.

## Add Your Own Levels

If you want to add your own levels, you can add a map file in `data/levels/` directory.
The file will be added into game automatically. You can select it in **Select Levels**.
The format of map file can be seen in `basic.txt`.

## More

I am moving this project to another bigger project [MiniGames](https://github.com/fyabc/MiniGames), but it may take some times.
