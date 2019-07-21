from datetime import datetime
from pathlib import Path
import pytz

import kobuddy

# TODO ugh, horrible
def get_test_dbs():
    # db = Path(__file__).absolute().parent.parent / 'KoboShelfes' / 'KoboReader.sqlite.0'
    db = Path(__file__).absolute().parent / 'data' / 'kobo_notes' / 'input' / 'KoboReader.sqlite'
    return [db]
kobuddy._get_all_dbs = get_test_dbs

from kobuddy import _iter_events_aux, get_todos, get_events, get_pages, _iter_highlights


def test_events():
    for e in _iter_events_aux():
        print(e)


def test_hls():
    for h in _iter_highlights():
        print(h)


def test_todos():
    todos = get_todos()
    assert len(todos) > 3


def test_get_all():
    events = get_events()
    assert len(events) > 50
    for d in events:
        print(d)


def test_pages():
    pages = get_pages()

    g = pages[0]
    assert 'Essentialism' in g.book
    hls = g.highlights
    assert len(hls) == 273

    [b] = [h for h in hls if h.eid == '520b7b13-dbef-4402-9a81-0f4e0c4978de']
    # TODO wonder if there might be any useful info? StartContainerPath, EndContainerPath
    assert b.kind == 'bookmark'

    # TODO move to a more specific test?
    # TODO assert sorted by date or smth?
    assert hls[0].kind == 'highlight'
    # TODO assert highlights got no annotation? not sure if it's even necessary to distinguish..

    [ann] = [h for h in hls if h.annotation is not None and len(h.annotation) > 0]

    assert ann.eid == 'eb264817-9a06-42fd-92ff-7bd38cd9ca79'
    assert ann.kind == 'annotation'
    assert ann.text == 'He does this by finding which machine has the biggest queue of materials waiting behind it and finds a way to increase its efficiency.'
    assert ann.annotation == 'Bottleneck'
    assert ann.dt == datetime(year=2017, month=8, day=12, hour=3, minute=49, second=13, microsecond=773000, tzinfo=pytz.utc)
    assert ann.book.author == 'Greg McKeown'

    assert len(pages) == 7