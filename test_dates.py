import unittest
from contextlib import redirect_stdout
from io import StringIO

from dates import main


class DatePickerTest(unittest.TestCase):
    def test_combined_filters(self):
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(['--where', 'out', '--budget', '0', '--minutes', '45']), 0)
        self.assertIn('sunset photo walk', output.getvalue())

    def test_no_matches(self):
        with redirect_stdout(StringIO()):
            self.assertEqual(main(['--minutes', '1']), 1)
