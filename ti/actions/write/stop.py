from dataaccess.utils import get_data_store
from actions.utils.utils import ensure_working


def action_stop(colorizer, time):
    data = get_data_store().load()

    ensure_working(data)

    current = data['work'][-1]
    current['end'] = time
    get_data_store().dump(data)
    print('So you stopped working on ' + colorizer.red(current['name']) + '.')
