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
  ti (i|interrupt)
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
# from datasources import JsonStore

from datetime import datetime, timedelta
from collections import defaultdict


from ti.dataaccess.utils import get_data_store

from ti.colors import *

from ti.actions.write import *


def action_on(name, time):
    data = get_store().load()
    work = data['work']

    if work and 'end' not in work[-1]:
        raise AlreadyOn("You are already working on %s. Stop it or use a "
                        "different sheet." % (colorizer.yellow(work[-1]['name']),))

    entry = {
        'name': name,
        'start': time,
    }

    work.append(entry)
    get_store().dump(data)

    print('Start working on ' + colorizer.green(name) + '.')


def action_fin(time, back_from_interrupt=True):
    ensure_working()

    data = get_store().load()

    current = data['work'][-1]
    current['end'] = time
    get_store().dump(data)
    print('So you stopped working on ' + colorizer.red(current['name']) + '.')

    if back_from_interrupt and len(data['interrupt_stack']) > 0:
        name = data['interrupt_stack'].pop()['name']
        get_store().dump(data)
        action_on(name, time)
        if len(data['interrupt_stack']) > 0:
            print('You are now %d deep in interrupts.'
                  % len(data['interrupt_stack']))
        else:
            print('Congrats, you\'re out of interrupts!')


def action_interrupt(name, time):
    ensure_working()

    action_fin(time, back_from_interrupt=False)

    data = get_store().load()
    if 'interrupt_stack' not in data:
        data['interrupt_stack'] = []
    interrupt_stack = data['interrupt_stack']

    interrupted = data['work'][-1]
    interrupt_stack.append(interrupted)
    get_store().dump(data)

    action_on('interrupt: ' + colorizer.green(name), time)
    print('You are now %d deep in interrupts.' % len(interrupt_stack))


def action_note(content):
    ensure_working()

    data = get_store().load()
    current = data['work'][-1]

    if 'notes' not in current:
        current['notes'] = [content]
    else:
        current['notes'].append(content)

    get_store().dump(data)

    print('Yep, noted to ' + colorizer.yellow(current['name']) + '.')


def action_tag(tags):
    ensure_working()

    data = get_store().load()
    current = data['work'][-1]

    current['tags'] = set(current.get('tags') or [])
    current['tags'].update(tags)
    current['tags'] = list(current['tags'])

    get_store().dump(data)

    tag_count = len(tags)
    print("Okay, tagged current work with %d tag%s."
          % (tag_count, "s" if tag_count > 1 else ""))


def action_status():
    ensure_working()

    data = get_store().load()
    current = data['work'][-1]

    start_time = parse_isotime(current['start'])
    diff = timegap(start_time, datetime.utcnow())

    isotime_local = isotime_utc_to_local(current['start'])
    start_h_m = isotime_local.strftime('%H:%M')
    now_time_str = datetime.now().strftime('%H:%M');

    print('You have been working on {0} for {1}, since {2}; It is now {3}.'
          .format(colorizer.green(current['name']), colorizer.yellow(diff),
                  colorizer.yellow(start_h_m), colorizer.yellow(now_time_str)))

    if 'notes' in current:
        for note in current['notes']:
            print('  * ', note)


def action_log(period):
    data = get_store().load()
    work = data['work'] + data['interrupt_stack']
    log = defaultdict(lambda: {'delta': timedelta()})
    current = None

    for item in work:
        start_time = parse_isotime(item['start'])

        if 'end' in item:
            log[item['name']]['delta'] += (
                    parse_isotime(item['end']) - start_time)
        else:
            log[item['name']]['delta'] += datetime.utcnow() - start_time
            current = item['name']

    name_col_len = 0

    for name, item in log.items():
        name_col_len = max(name_col_len, len(strip_color(name)))

        secs = item['delta'].total_seconds()
        tmsg = []

        if secs > 3600:
            hours = int(secs // 3600)
            secs -= hours * 3600
            tmsg.append(str(hours) + ' hour' + ('s' if hours > 1 else ''))

        if secs > 60:
            mins = int(secs // 60)
            secs -= mins * 60
            tmsg.append(str(mins) + ' minute' + ('s' if mins > 1 else ''))

        if secs:
            tmsg.append(str(secs) + ' second' + ('s' if secs > 1 else ''))

        print(tmsg)
        log[name]['tmsg'] = ', '.join(tmsg)[::-1].replace(',', '& ', 1)[::-1]

    for name, item in sorted(log.items(), key=(lambda x: x[0]), reverse=True):
        print(ljust_with_color(name, name_col_len), ' ∙∙ ', item['tmsg'],
              end=' ← working\n' if current == name else '\n')


def format_csv_time(somedatetime):
    local_dt = isotime_utc_to_local(somedatetime)
    return local_dt.strftime('%H:%M')


def extract_day_custom_formatter(datetime_local_tz, format_string):
    local_dt = isotime_utc_to_local(datetime_local_tz)
    return local_dt.strftime(format_string)


def extract_day(datetime_local_tz):
    return extract_day_custom_formatter(datetime_local_tz, '%Y-%m-%d')


def remove_seconds(timedelta):
    return ':'.join(str(timedelta).split(':')[:2])


def get_notes_from_workitem(item):
    notes = ''
    if 'notes' in item:
        for note in item['notes']:
            notes += note + ' ; '
    return notes


def action_csv():
    sep = '|'
    data = get_store().load()
    work = data['work']

    for item in work:
        start_time = parse_isotime(item['start'])
        if 'end' in item:
            notes = get_notes_from_workitem(item)
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            print(extract_day(item['start']), sep, item['name'], sep, format_csv_time(item['start']), sep,
                  format_csv_time(item['end']), sep, remove_seconds(duration), sep, notes, sep)


def format_time(duration_timedelta):
    return format_time_seconds(duration_timedelta.seconds)


def format_time_seconds(duration_secs):
    hours, rem = divmod(duration_secs, 3600)
    mins, secs = divmod(rem, 60)
    formatted_time_str = str(hours).rjust(2, str('0')) + ':' + str(mins).rjust(2, str('0'))
    if hours >= 8:
        return colorizer.green(formatted_time_str)
    else:
        return colorizer.red(formatted_time_str)


def get_min_date(date_1, date_2):
    if date_1 is None:
        date_1 = parse_isotime('2022-01-01T00:00:00.000001Z')
    return date_1 if date_1 < date_2 else date_2


def get_max_date(date_1, date_2):
    if date_1 is None:
        date_1 = parse_isotime('2015-01-01T00:00:00.000001Z')
    return date_1 if date_1 > date_2 else date_2


def action_report(activity):
    print('Displaying all entries for ', colorizer.yellow(activity), ' grouped by day:', sep='')
    print()
    sep = ' | '
    data = get_store().load()
    work = data['work']
    report = defaultdict(lambda: {'sum': timedelta(), 'notes': '', 'weekday': '', 'start_time': None, 'end_time': None})

    total_time = 0
    for item in work:
        if item['name'] == activity and 'end' in item:
            start_time = parse_isotime(item['start'])
            end_time = parse_isotime(item['end'])
            day = extract_day(item['start'])
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            report[day]['sum'] += duration
            report[day]['notes'] += get_notes_from_workitem(item);
            report[day]['weekday'] = extract_day_custom_formatter(item['start'], '%a')
            report[day]['start_time'] = get_min_date(report[day]['start_time'], start_time)
            report[day]['end_time'] = get_max_date(report[day]['end_time'], end_time)
            total_time += duration.seconds

    print('weekday', sep, 'date', sep, 'total duration', sep, 'start time', sep, 'end time', sep, 'break', sep,
          'description', sep)

    for date, details in sorted(report.items()):
        start_time = utc_to_local(details['start_time']).strftime("%H:%M")
        end_time = utc_to_local(details['end_time']).strftime("%H:%M")
        break_duration = get_break_duration(details['start_time'], details['end_time'], details['sum'])
        print(details['weekday'], sep, date, sep, format_time(details['sum']), sep, start_time, sep, end_time, sep,
              format_time(break_duration), sep, details['notes'], sep="")

    should_hours = 8 * len(report.items());
    should_hours_str = str(should_hours) + ':00'
    print()
    print('Based on your current entries, you should have logged ', colorizer.green(should_hours_str), ' ; you instead logged ',
          format_time_seconds(total_time), sep='')


def get_break_duration(start_time, end_time, net_work_duration):
    total_work_duration = end_time - start_time
    return total_work_duration - net_work_duration


# def action_edit():
#     if "EDITOR" not in os.environ:
#         raise NoEditor("Please set the 'EDITOR' environment variable")
#
#     data = get_store().load()
#     yml = yaml.safe_dump(data, default_flow_style=False, allow_unicode=True)
#
#     cmd = os.getenv('EDITOR')
#     fd, temp_path = tempfile.mkstemp(suffix='.yml', prefix='ti.')
#     with open(temp_path, "r+") as f:
#         f.write(yml.replace('\n- ', '\n\n- '))
#         f.seek(0)
#         subprocess.check_call(cmd + ' ' + temp_path, shell=True)
#         yml = f.read()
#         f.truncate()
#         f.close
#
#     os.close(fd)
#     os.remove(temp_path)
#
#     try:
#         data = yaml.load(yml)
#     except:
#         raise InvalidYAML("Oops, that YAML doesn't appear to be valid!")
#
#     get_store().dump(data)


def is_working():
    data = get_store().load()
    return data.get('work') and 'end' not in data['work'][-1]


def ensure_working():
    if is_working():
        return

    raise NoTask("For all I know, you aren't working on anything. "
                 "I don't know what to do.\n"
                 "See `ti -h` to know how to start working.")


def parse_args(argv=sys.argv):
    global use_color

    if '--no-color' in argv:
        colorizer.use_color(False)
        argv.remove('--no-color')

    # prog = argv[0]
    if len(argv) == 1:
        raise BadArguments("You must specify a command.")

    head = argv[1]
    tail = argv[2:]

    if head in ['-h', '--help', 'h', 'help']:
        raise BadArguments()

    elif head in ['e', 'edit']:
        fn = action_edit
        args = {}

    elif head in ['o', 'on', 'start']:
        if not tail:
            raise BadArguments("Need the name of whatever you are working on.")

        fn = action_on
        args = {
            'name': tail[0],
            'time': to_datetime(' '.join(tail[1:])),
        }

    elif head in ['f', 'fin', 'stop']:
        fn = action_fin
        args = {'time': to_datetime(' '.join(tail))}

    elif head in ['s', 'status']:
        fn = action_status
        args = {}

    elif head in ['l', 'log']:
        fn = action_log
        args = {'period': tail[0] if tail else None}

    elif head in ['csv']:
        fn = action_csv
        args = {}

    elif head in ['report']:
        fn = action_report
        if not tail:
            raise BadArguments('Please provide the name of the activity to generate the report for')
        args = {'activity': tail[0]}

    elif head in ['t', 'tag']:
        if not tail:
            raise BadArguments("Please provide at least one tag to add.")

        fn = action_tag
        args = {'tags': tail}

    elif head in ['n', 'note']:
        if not tail:
            raise BadArguments("Please provide some text to be noted.")

        fn = action_note
        args = {'content': ' '.join(tail)}

    elif head in ['i', 'interrupt']:
        if not tail:
            raise BadArguments("Need the name of whatever you are working on.")

        fn = action_interrupt
        args = {
            'name': tail[0],
            'time': to_datetime(' '.join(tail[1:])),
        }
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


store = get_data_store('JSON')

use_color = True

colorizer = Colorizer(True)

if __name__ == '__main__':
    main()
