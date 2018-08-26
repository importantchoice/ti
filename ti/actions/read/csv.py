from __future__ import print_function

from ti.dataaccess.utils import get_data_store
from ti.dateutils import *
from ti.actions.utils import reportingutils


def action_csv():
    sep = '|'
    data = get_data_store().load()
    work = data['work']

    for item in work:
        start_time = parse_isotime(item['start'])
        if 'end' in item:
            notes = reportingutils.get_notes_from_workitem(item)
            duration = parse_isotime(item['end']) - parse_isotime(item['start'])
            print(reportingutils.extract_day(item['start']), sep, item['name'], sep, format_csv_time(item['start']), sep,
                  format_csv_time(item['end']), sep, reportingutils.remove_seconds(duration), sep, notes, sep)


def format_csv_time(somedatetime):
    local_dt = isotime_utc_to_local(somedatetime)
    return local_dt.strftime('%H:%M')
