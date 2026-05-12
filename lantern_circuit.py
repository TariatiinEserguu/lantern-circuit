"""A two-player lantern puzzle."""
import argparse
import tkinter as tk
from pathlib import Path
from dataclasses import dataclass, replace

BOARDS = (
    (
        "#########",
        "#       #",
        "#a $ .  #",
        "#       #",
        "#  . $ b#",
        "#       #",
        "#########",
    ),
    (
        "#########",
        "#   .   #",
        "# # $ # #",
        "#a #   b#",
        "#   $ # #",
        "# .     #",
        "#########",
    ),
    (
        "##########",
        "#   #    #",
        "#a  $ .  #",
        "# .$#    #",
        "#   # $ b#",
        "#      . #",
        "##########",
    ),
    (
        "#########",
        "#  . .  #",
        "#   #   #",
        "#a $ $ b#",
        "# # . # #",
        "#   $   #",
        "#       #",
        "#########",
    ),
)
CONTROLS = {
    'w': (0, 0, -1), 'a': (0, -1, 0), 's': (0, 0, 1), 'd': (0, 1, 0),
    'up': (1, 0, -1), 'left': (1, -1, 0), 'down': (1, 0, 1), 'right': (1, 1, 0),
}


@dataclass(frozen=True)
class Board:
    walls: frozenset
    pads: frozenset
    lanterns: frozenset
    players: tuple
    width: int
    height: int

    @classmethod
    def load(cls, layout):
        if not layout or not layout[0] or any(len(row) != len(layout[0]) for row in layout):
            raise ValueError('A room must be a nonempty rectangle')
        width, height = len(layout[0]), len(layout)
        tiles = {token: set() for token in '#.$ab'}
        for y, row in enumerate(layout):
            for x, token in enumerate(row):
                if (x in (0, width - 1) or y in (0, height - 1)) and token != '#':
                    raise ValueError('The room must be enclosed by walls')
                if token in tiles:
                    tiles[token].add((x, y))
                elif token != ' ':
                    raise ValueError(f'Unknown room tile {token!r}')
        if len(tiles['a']) != 1 or len(tiles['b']) != 1:
            raise ValueError('A room needs one start tile for each player')
        if not tiles['$'] or len(tiles['$']) != len(tiles['.']):
            raise ValueError('A room needs the same number of lanterns and pads')
        return cls(frozenset(tiles['#']), frozenset(tiles['.']),
                   frozenset(tiles['$']), (tiles['a'].pop(), tiles['b'].pop()),
                   len(layout[0]), len(layout))

    @property
    def solved(self):
        return self.lanterns == self.pads

    @property
    def has_corner_trap(self):
        for x, y in self.lanterns - self.pads:
            horizontal = (x - 1, y) in self.walls or (x + 1, y) in self.walls
            vertical = (x, y - 1) in self.walls or (x, y + 1) in self.walls
            if horizontal and vertical:
                return True
        return False

    def move(self, player, dx, dy):
        x, y = self.players[player]
        target = x + dx, y + dy
        if target in self.walls or target in self.players:
            return self
        lanterns = self.lanterns
        if target in lanterns:
            beyond = target[0] + dx, target[1] + dy
            if beyond in self.walls or beyond in lanterns or beyond in self.players:
                return self
            lanterns = (lanterns - {target}) | {beyond}
        players = list(self.players)
        players[player] = target
        return replace(self, players=tuple(players), lanterns=lanterns)


def read_rooms(path):
    rooms = tuple(tuple(room.splitlines()) for room in path.read_text(encoding='utf-8').strip('\n').split('\n\n'))
    if not 1 <= len(rooms) <= 9:
        raise ValueError('A pack must contain one to nine rooms')
    for room in rooms:
        Board.load(room)
        if len(room) > 10 or len(room[0]) > 16:
            raise ValueError('Rooms can use at most 16 columns and 10 rows')
    return rooms


class LanternCircuit:
    def __init__(self, root, rooms=BOARDS, start_room=0):
        self.root = root
        self.rooms = rooms
        self.room_keys = {str(i + 1): i for i in range(len(rooms))}
        root.title('Lantern Circuit')
        root.configure(bg='#171823')
        self.canvas = tk.Canvas(root, width=700, height=548, bg='#171823', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        root.minsize(600, 520)
        self.canvas.bind('<Configure>', lambda event: self.draw())
        root.bind('<KeyPress>', self.on_key)
        self.best_moves = {}
        self.load(start_room)

    def load(self, level):
        self.level = level
        self.board = Board.load(self.rooms[level])
        self.history = []
        self.redo_history = []
        self.pushes = 0
        self.draw()

    def on_key(self, event):
        key = event.keysym.lower()
        if key in self.room_keys and self.level != self.room_keys[key]:
            self.load(self.room_keys[key])
            return
        if key == 'r':
            self.load(self.level)
        elif key == 'u' and self.history:
            previous = self.history.pop()
            self.pushes -= self.board.lanterns != previous.lanterns
            self.redo_history.append(self.board)
            self.board = previous
        elif key == 'y' and self.redo_history:
            next_board = self.redo_history.pop()
            self.pushes += self.board.lanterns != next_board.lanterns
            self.history.append(self.board)
            self.board = next_board
        elif key == 'return' and self.board.solved and self.level + 1 < len(self.rooms):
            self.load(self.level + 1)
        elif key in CONTROLS and not self.board.solved:
            after = self.board.move(*CONTROLS[key])
            if after is not self.board:
                self.pushes += self.board.lanterns != after.lanterns
                self.history.append(self.board)
                self.board = after
                self.redo_history.clear()
        if self.board.solved:
            moves = len(self.history)
            self.best_moves[self.level] = min(moves, self.best_moves.get(self.level, moves))
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete('all')
        width = max(c.winfo_width(), 600)
        height = max(c.winfo_height(), 520)
        c.create_text(36, 31, anchor='w', text='Lantern Circuit', fill='#fff1dd', font=('TkDefaultFont', 23, 'bold'))
        c.create_text(38, 68, anchor='w', text=f'Room {self.level + 1} of {len(self.rooms)}  /  Push every lantern onto a marked tile',
                      fill='#c6b7cb', font=('TkDefaultFont', 11))
        board = self.board
        size = min((width - 74) // board.width, (height - 160) // board.height, 62)
        left = (width - size * board.width) // 2
        top = 88 + (height - 160 - size * board.height) // 2

        for y in range(board.height):
            for x in range(board.width):
                pos = (x, y)
                x0, y0 = left + x * size, top + y * size
                x1, y1 = x0 + size, y0 + size
                cx, cy = x0 + size / 2, y0 + size / 2
                wall = pos in board.walls
                floor = '#28263a' if (x + y) % 2 else '#302a41'
                c.create_rectangle(x0, y0, x1, y1, fill='#45405a' if wall else floor, outline='#1c1b28', width=2)
                if wall:
                    c.create_line(x0 + 5, y0 + 5, x1 - 5, y0 + 5, fill='#5a526d', width=2)
                if pos in board.pads:
                    c.create_oval(cx - 13, cy - 13, cx + 13, cy + 13, outline='#f3a654', width=2, dash=(3, 3))
                if pos in board.lanterns:
                    light = '#ffe49a' if pos in board.pads else '#ed9854'
                    c.create_rectangle(cx - 13, cy - 15, cx + 13, cy + 15, fill=light, outline='#ffdb98', width=2)
                    c.create_line(cx - 7, cy - 15, cx - 7, cy + 15, fill='#9c4e3d')
                    c.create_line(cx + 7, cy - 15, cx + 7, cy + 15, fill='#9c4e3d')
                if pos in board.players:
                    player = board.players.index(pos)
                    color = ('#a5e8d6', '#c9b0ff')[player]
                    c.create_oval(cx - 15, cy - 15, cx + 15, cy + 15, fill=color, outline='')
                    c.create_text(cx, cy, text=str(player + 1), fill='#202033', font=('TkDefaultFont', 12, 'bold'))

        status = f'{len(board.pads & board.lanterns)}/{len(board.pads)} lanterns lit  ·  {len(self.history)} moves  ·  {self.pushes} pushes'
        if board.solved:
            status = 'All rooms lit!' if self.level + 1 == len(self.rooms) else 'Room lit! Press Enter for the next room.'
        elif board.has_corner_trap:
            status = 'Lantern trapped in a corner. Press U to undo.'
        if self.level in self.best_moves:
            status += f'  ·  Best: {self.best_moves[self.level]}'
        c.create_text(width / 2, height - 57, text=status, fill='#ffe49a', font=('TkDefaultFont', 12, 'bold'))
        c.create_text(width / 2, height - 27, text=f'P1 WASD    P2 Arrows    U Undo    Y Redo    R Restart    1–{len(self.rooms)} Rooms',
                      fill='#c6b7cb', font=('TkDefaultFont', 10))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rooms', type=Path, help='Load a custom pack of rooms')
    parser.add_argument('--room', type=int, default=1, help='Room number to open first')
    parser.add_argument('--check', action='store_true', help='Validate rooms without opening a window')
    args = parser.parse_args(argv)
    try:
        rooms = read_rooms(args.rooms) if args.rooms else BOARDS
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if not 1 <= args.room <= len(rooms):
        parser.error(f'Room must be between 1 and {len(rooms)}')
    if args.check:
        print(f'Validated {len(rooms)} room(s).')
        return
    root = tk.Tk()
    LanternCircuit(root, rooms, args.room - 1)
    root.mainloop()


if __name__ == '__main__':
    main()
