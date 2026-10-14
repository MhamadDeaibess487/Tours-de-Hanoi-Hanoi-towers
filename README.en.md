# Towers of Hanoi

[Documentation française](README.md)

A Python puzzle game with a desktop interface, a console mode and an animated recursive solver. Originally developed for INF101 by **Mhamad Deaibess and Karim Hammoud**, the project now separates game rules, presentation and persistence.

![Game interface](docs/screenshots/hanoi.png)

## Features

- Three towers and 1–10 disks, with validated moves and victory detection.
- Dark interface, hover states and alternating ranking rows with highlighted best scores.
- Mouse and keyboard controls, move counter and successive undo.
- Free play and challenge mode: at most `2ⁿ − 1 + 5` moves.
- Recursive solution animation with pause, resume, stop and adjustable delay.
- Independent demonstration that preserves the player's game.
- Persistent JSON scores, multiple games per player and a complete ranking.
- Console mode requiring no graphical display.

The current game interface and console prompts are in French.

## Installation

Requires **Python 3.10+**. The game uses only the standard library; desktop mode requires Tkinter.

```bash
git clone https://github.com/MhamadDeaibess487/Tours-de-Hanoi-Hanoi-towers.git
cd Tours-de-Hanoi-Hanoi-towers
python -m hanoi
```

Use `python3` if required by your system. On Debian/Ubuntu, install Tkinter with `sudo apt install python3-tk` if missing. Official Windows Python installers normally include Tcl/Tk; on macOS use a Python distribution with Tkinter support.

```bash
python -m hanoi --cli
python Projet-Hanoi.py
```

No account, external service or API key is required.

## Controls

Move all disks from tower 1 to tower 3. Move one disk at a time, never placing a larger disk on a smaller one.

Choose the disk count and challenge option, then press **Nouvelle partie**. Click a source tower and a destination, or press **1**, **2**, **3**. **Escape** clears the selection. **Annuler** undoes a move; **Solution** starts a demonstration from the initial board; **Pause / reprendre** pauses or resumes it. **Arrêter** restores your own game after a demonstration. Animation delay is measured in milliseconds. **Scores** opens the ranking.

In console mode enter a move such as `1 3`, or use `annuler`, `solution`, `scores`, `nouvelle`, `quitter`. The console solver prints its moves. Victory prompts for a player name and another game.

Undo reduces the move counter. Reaching the challenge limit still allows undo or restart. Demonstrations never save scores.

## Architecture and algorithm

| Module | Responsibility |
| --- | --- |
| `hanoi/game.py` | State, legal moves, victory, counter and undo |
| `hanoi/solver.py` | Lazy recursive solution generator |
| `hanoi/scores.py` | JSON validation, atomic persistence and ranking |
| `hanoi/ui.py` | Tkinter widgets, scalable Canvas and event scheduling |
| `hanoi/cli.py` | Console interactions |
| `hanoi/__main__.py` | Entry point and mode selection |
| `tests/` | Rules, solver, storage, console and desktop tests |

The solver recursively moves `n − 1` disks to the auxiliary tower, moves the largest disk, then moves the remaining disks onto it. It generates exactly **`2ⁿ − 1` moves** in **O(2ⁿ)** time and **O(n)** auxiliary memory. The ten-disk limit bounds demonstration time and keeps the board readable.

## Development

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest -q
ruff check .
ruff format --check .
```

The desktop test is skipped when `DISPLAY` is absent. On headless Linux:

```bash
sudo apt install xvfb
xvfb-run -a python -m pytest -q
```

GitHub Actions runs tests and Ruff checks on Python 3.10, 3.12 and 3.13 using a virtual display. Tests cover minimal legal solutions for 1–10 disks, undo, invalid moves, the exact challenge limit, corrupted score preservation and desktop gameplay.

## Data and troubleshooting

Scores are saved in `hanoi/scores.json` under the user's data directory:

- Linux: `$XDG_DATA_HOME`, or `~/.local/share`.
- macOS: `~/Library/Application Support`.
- Windows: `%LOCALAPPDATA%`, or `~/AppData/Local`.

Dates use UTC. Ranking sorts by disk count, move count and date. Invalid score files are reported and preserved; back them up before repairing them. Saving uses a temporary file and atomic replacement. Concurrent writes from multiple application instances are not supported.

Use `--cli` if no graphical display is available. Invalid inputs and moves leave the board unchanged. Closing the window cancels scheduled animation.

## Credits

Original INF101 project by **Mhamad Deaibess and Karim Hammoud**. Modernization preserves manual play, undo, scores, recursive solving and visualization. Tkinter Canvas replaces Turtle; the historical launcher remains available.

The project demonstrates recursion, model invariants, separation of concerns, event-driven interfaces, persistence and automated testing. No redistribution license has been selected; that decision requires agreement from the authors.
