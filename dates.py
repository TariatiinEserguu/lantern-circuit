"""Pick a date idea that fits your evening."""
import argparse
import json
import random
from pathlib import Path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ideas', type=Path, default=Path(__file__).with_name('ideas.json'))
    parser.add_argument('--where', choices=['in', 'out'])
    parser.add_argument('--budget', type=float, help='Maximum cost for two')
    parser.add_argument('--minutes', type=int, help='Maximum duration')
    args = parser.parse_args(argv)
    try:
        ideas = json.loads(args.ideas.read_text(encoding='utf-8'))
        if not isinstance(ideas, list):
            raise ValueError('Expected a list of ideas')
        eligible = []
        for idea in ideas:
            name, where, cost, minutes = (idea[key] for key in ('name', 'where', 'cost', 'minutes'))
            if (not isinstance(name, str) or not name.strip() or where not in ('in', 'out')
                or type(cost) not in (int, float) or not 0 <= cost < float('inf')
                or type(minutes) is not int or minutes <= 0):
                raise ValueError('Invalid idea name, location, cost, or duration')
            if ((args.where is None or where == args.where)
                and (args.budget is None or cost <= args.budget)
                and (args.minutes is None or minutes <= args.minutes)):
                eligible.append((name, cost, minutes))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        parser.error(f'Could not load ideas from {args.ideas} ({exc})')
    if not eligible:
        print('No dates match. Try a higher budget or more time.')
        return 1
    name, cost, minutes = random.choice(eligible)
    print(f'{name} ({minutes} min, estimated cost for two: {cost:g})')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
