# Lantern Circuit

A small 2D puzzle for two players on one keyboard. Push the lanterns onto the marked floor tiles to light four rooms. Work together to clear tight passages, or play solo by switching between the two sets of controls.

## Play

```sh
python3 lantern_circuit.py
```

Requires Python 3.10+ with Tkinter and a graphical desktop. On Debian and Ubuntu, install `python3-tk` if Tkinter is missing.

| Control | Action |
| --- | --- |
| WASD | Move player 1 |
| Arrow keys | Move player 2 |
| U | Undo one move |
| Y | Redo an undone move |
| R | Restart the room |
| Enter | Continue after solving a room |
| 1–4 | Jump to a room and start it fresh |

You can push one lantern at a time. Walls, lanterns, and the other player can block a push. You can move a lantern off a marked tile to make room. The game warns you if a lantern gets stuck in a corner without a pad.

Each room has its own move history. A new move after an undo clears the redo history. Your best move count for each room is tracked until you close the game.

## Custom rooms

Run `python3 lantern_circuit.py --rooms my-rooms.txt` to load a pack. Write one rectangular grid per room and separate rooms with a blank line. Use `#` for walls, spaces for floor, `$` for lanterns, `.` for pads, and `a` and `b` for the two player starts. Enclose every room with walls and use the same number of pads and lanterns. Custom packs can contain up to nine rooms.

Run `python3 lantern_circuit.py --rooms my-rooms.txt --check` to check the layout without opening the game. This checks the room format. Playtest the room to make sure it can be solved.
