import unittest
from pathlib import Path

from lantern_circuit import BOARDS, Board, read_rooms


class BoardTests(unittest.TestCase):
    def test_all_builtin_rooms_are_valid(self):
        for room in BOARDS:
            with self.subTest(room=room):
                self.assertFalse(Board.load(room).solved)

    def test_example_pack_is_valid(self):
        self.assertEqual(len(read_rooms(Path(__file__).with_name('example_rooms.txt'))), 2)

    def test_rejects_open_boundary(self):
        with self.assertRaisesRegex(ValueError, 'enclosed'):
            Board.load(('#####', '#a$.#', '#b  #', '## ##'))

    def test_push_into_wall_preserves_state(self):
        board = Board.load(('#####', '#$.b#', '#a  #', '#####'))
        self.assertIs(board.move(0, 0, -1), board)
        self.assertTrue(board.has_corner_trap)


if __name__ == '__main__':
    unittest.main()
