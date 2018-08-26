from ti.exceptions import AlreadyOn
from ti.dataaccess.utils import get_data_store


def action_start(colorizer, name, time):
    data = get_data_store().load()
    work = data['work']

    if work and 'end' not in work[-1]:
        raise AlreadyOn("You are already working on %s. Stop it or use a "
                        "different sheet." % (colorizer.yellow(work[-1]['name']),))

    entry = {
        'name': name,
        'start': time,
    }

    work.append(entry)
    get_data_store().dump(data)

    print('Start working on ' + colorizer.green(name) + '.')
