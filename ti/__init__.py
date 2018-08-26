# coding: utf-8

"""
ti is a simple and extensible time tracker for the command line. Visit the
project page (http://ti.sharats.me) for more details.

Usage:
  ti (o|on) <name> [<time>...]
  ti (f|fin) [<time>...]
  ti (s|status)
  ti (t|tag) <tag>...
  ti (n|note) <note-text>...
  ti (l|log) [today]
  ti (e|edit)
  ti --no-color
  ti -h | --help

Options:
  -h --help         Show this help.
  <start-time>...   A time specification (goto http://ti.sharats.me for more on
                    this).
  <tag>...          Tags can be made of any characters, but its probably a good
                    idea to avoid whitespace.
  <note-text>...    Some arbitrary text to be added as `notes` to the currently
                    working project.
"""

from __future__ import print_function
from __future__ import unicode_literals

import sys

from dateutils import *
from exceptions import *

from ti.dataaccess.utils import get_data_store

from ti.colors import *

from ti.actions.write import edit
from ti.actions.write import start
from ti.actions.write import stop
from ti.actions.write import tag

from ti.actions.read import log
from ti.actions.read import csv
from ti.actions.read import report
from ti.actions.read import status

from ti.actions.utils import reportingutils
from ti.actions.utils.utils import ensure_working


def action_note(content):
    data = get_store().load()

    ensure_working(data)

    current = data['work'][-1]

    if 'notes' not in current:
        current['notes'] = [content]
    else:
        current['notes'].append(content)

    get_store().dump(data)

    print('Yep, noted to ' + colorizer.yellow(current['name']) + '.')


def parse_args(argv=sys.argv):

    if '--no-color' in argv:
        colorizer.set_use_color(False)
        argv.remove('--no-color')

    # prog = argv[0]
    if len(argv) == 1:
        raise BadArguments("You must specify a command.")

    head = argv[1]
    tail = argv[2:]

    if head in ['-h', '--help', 'h', 'help']:
        raise BadArguments()

    elif head in ['e', 'edit']:
        fn = edit.action_edit
        args = {}

    elif head in ['o', 'on', 'start']:
        if not tail:
            raise BadArguments("Need the name of whatever you are working on.")

        fn = start.action_start
        args = {
            'colorizer': colorizer,
            'name': tail[0],
            'time': to_datetime(' '.join(tail[1:])),
        }

    elif head in ['f', 'fin', 'stop']:
        fn = stop.action_stop
        args = {'colorizer': colorizer, 'time': to_datetime(' '.join(tail))}

    elif head in ['s', 'status']:
        fn = status.action_status
        args = {'colorizer': colorizer}

    elif head in ['l', 'log']:
        fn = log.action_log
        args = {'period': tail[0] if tail else None}

    elif head in ['csv']:
        fn = csv.action_csv
        args = {}

    elif head in ['report']:
        fn = report.action_report
        if not tail:
            raise BadArguments('Please provide the name of the activity to generate the report for')
        args = {'colorizer': colorizer, 'activity': tail[0]}

    elif head in ['t', 'tag']:
        if not tail:
            raise BadArguments("Please provide at least one tag to add.")

        fn = tag.action_tag
        args = {'tags': tail}

    elif head in ['n', 'note']:
        if not tail:
            raise BadArguments("Please provide some text to be noted.")

        fn = action_note
        args = {'content': ' '.join(tail)}

    elif head in ['setdate', 'sd']:
        if not tail:
            raise BadArguments("Need the date you want to set.")
        fn = action_setdate
        args = {'today': tail[0]}
    else:
        raise BadArguments("I don't understand %r" % (head,))

    return fn, args


def main():
    try:
        fn, args = parse_args()
        fn(**args)
    except TIError as e:
        msg = str(e) if len(str(e)) > 0 else __doc__
        print(msg, file=sys.stderr)
        sys.exit(1)


def get_store():
    return get_data_store('JSON')


colorizer = Colorizer(True)

if __name__ == '__main__':
    main()