from ti.dataaccess.utils import get_data_store
from ti.actions.utils.utils import ensure_working


def action_stop(colorizer, time):
    data = get_data_store('JSON').load()

    ensure_working(data)

    current = data['work'][-1]
    current['end'] = time
    get_data_store('JSON').dump(data)
    print('So you stopped working on ' + colorizer.red(current['name']) + '.')