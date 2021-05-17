import acp_times
import arrow
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_opening():
    test_time = arrow.Arrow(2021,1,1)
    assert acp_times.open_time(0, 200, arrow.get(test_time)) == (test_time.shift(hours=0,minutes=0)).isoformat()
    assert acp_times.open_time(0, 300, arrow.get(test_time)) == (test_time.shift(hours=0,minutes=0)).isoformat()
    assert acp_times.open_time(0, 400, arrow.get(test_time)) == (test_time.shift(hours=0,minutes=0)).isoformat()
    assert acp_times.open_time(0, 600, arrow.get(test_time)) == (test_time.shift(hours=0,minutes=0)).isoformat()

def test_closing():
    test_time = arrow.Arrow(2021,1,1)
    assert acp_times.close_time(100, 200, arrow.get(test_time)) == (test_time.shift(hours=6,minutes=40)).isoformat()
    assert acp_times.close_time(100, 300, arrow.get(test_time)) == (test_time.shift(hours=6,minutes=40)).isoformat()
    assert acp_times.close_time(100, 400, arrow.get(test_time)) == (test_time.shift(hours=6,minutes=40)).isoformat()
    assert acp_times.close_time(100, 600, arrow.get(test_time)) != (test_time.shift(hours=0,minutes=0)).isoformat()
