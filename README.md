# Lantern Circuit

A small 2D puzzle for two players on one keyboard. Push the lanterns onto the marked floor tiles to light three rooms. Work together to clear tight passages, or play solo by switching between the two sets of controls.

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
| R | Restart the room |
| Enter | Continue after solving a room |

You can push one lantern at a time. Walls, lanterns, and the other player can block a push. You can move a lantern off a marked tile to make room.
