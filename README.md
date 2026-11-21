# Date Night Roulette

Pick a date idea based on where you want to go, how much time you have, and what you want to spend.

Requires Python 3.10 or newer. No packages to install.

```sh
python3 dates.py --where out --budget 10 --minutes 60
```

Omit any filter to consider all values for it. Add your own ideas to `ideas.json`, or use `--ideas path/to/ideas.json` for a separate list. Each entry has a name, a location (`in` or `out`), estimated cost for two, and duration in minutes. Use the same currency throughout your list.

Run the tests with `python3 -m unittest discover`.
