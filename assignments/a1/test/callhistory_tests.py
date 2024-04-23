import pytest
from datetime import datetime

from application import create_customers, process_event_history, find_customer_by_number
from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine
from callhistory import CallHistory
from call import Call

###############################
# register_outgoing_call test #
###############################
def test_register_outgoing_call_one_call():
    call_history = CallHistory()
    date = datetime.strptime("2018-01-03 02:14:31", "%Y-%m-%d %H:%M:%S")
    call = Call("123-4567", "890-1234", date, 120, (-79.42, 43.64), (-79.52, 43.75))
    call_history.register_outgoing_call(call)

    assert len(call_history.outgoing_calls) == 1
    assert call in call_history.outgoing_calls[(date.month, date.year)]

def test_register_outgoing_call_same_month():
    call_history = CallHistory()
    date = datetime.strptime("2018-01-03 02:14:31", "%Y-%m-%d %H:%M:%S")
    calls = []
    calls.append(Call("123-4567", "890-1234", date, 120, (-79.42, 43.64), (-79.52, 43.75)))
    call_history.register_outgoing_call(calls[0])
    
    # more call in same month
    calls.append(Call("131-4520", "114-5141", date, 120, (-79.53, 43.64), (-79.64, 43.75)))
    calls.append(Call("123-3333", "890-1314", date, 120, (-79.53, 43.64), (-79.64, 43.75)))
    call_history.register_outgoing_call(calls[1])
    call_history.register_outgoing_call(calls[2])

    assert len(call_history.outgoing_calls) == 1
    for c in calls:
        assert c in call_history.outgoing_calls[(date.month, date.year)] 

def test_register_outgoing_call_diff_month():
    call_history = CallHistory()
    times = ["2018-01-03 02:14:31", "2018-02-04 02:14:31", "2017-12-04 02:14:31", "2019-01-04 02:14:31"]
    
    src_num = ["131-4520", "123-4567", "123-3333", "888-8888"]
    dst_num = ["114-5141", "890-1314", "250-0520", "148-2050"]
    dates = []
    for t in times:
        dates.append(datetime.strptime(t, "%Y-%m-%d %H:%M:%S"))
    
    calls = []
    for i in range(4):
        call = Call(src_num[i], dst_num[i], dates[i], 120, (-79.42, 43.64), (-79.52, 43.75))
        calls.append(call)
        call_history.register_outgoing_call(call)
        

    assert len(call_history.outgoing_calls) == 4
    for i in range(4):
        assert calls[i] in call_history.outgoing_calls[(dates[i].month, dates[i].year)]

def test_register_outgoing_call_mix_month():
    call_history = CallHistory()
    times = ["2018-01-03 02:14:31", "2018-01-04 02:14:31", "2017-12-04 02:14:31", "2017-12-25 02:14:31"]
    
    src_num = ["131-4520", "123-4567", "123-3333", "888-8888"]
    dst_num = ["114-5141", "890-1314", "250-0520", "148-2050"]
    dates = []
    for t in times:
        dates.append(datetime.strptime(t, "%Y-%m-%d %H:%M:%S"))
    
    calls = []
    for i in range(4):
        call = Call(src_num[i], dst_num[i], dates[i], 120, (-79.42, 43.64), (-79.52, 43.75))
        calls.append(call)
        call_history.register_outgoing_call(call)
        

    assert len(call_history.outgoing_calls) == 2
    for i in range(4):
        assert calls[i] in call_history.outgoing_calls[(dates[i].month, dates[i].year)]

###############################
# register_incoming_call test #
###############################
def test_register_incoming_call_one_call():
    call_history = CallHistory()
    date = datetime.strptime("2018-01-03 02:14:31", "%Y-%m-%d %H:%M:%S")
    call = Call("123-4567", "890-1234", date, 120, (-79.42, 43.64), (-79.52, 43.75))
    call_history.register_incoming_call(call)

    assert len(call_history.incoming_calls) == 1
    assert call in call_history.incoming_calls[(date.month, date.year)]


def test_register_incoming_call_same_month():
    call_history = CallHistory()
    date = datetime.strptime("2018-01-03 02:14:31", "%Y-%m-%d %H:%M:%S")
    calls = []
    calls.append(Call("123-4567", "890-1234", date, 120, (-79.42, 43.64), (-79.52, 43.75)))
    call_history.register_incoming_call(calls[0])
    
    # more call in same month
    calls.append(Call("131-4520", "114-5141", date, 120, (-79.53, 43.64), (-79.64, 43.75)))
    calls.append(Call("123-3333", "890-1314", date, 120, (-79.53, 43.64), (-79.64, 43.75)))
    call_history.register_incoming_call(calls[1])
    call_history.register_incoming_call(calls[2])

    assert len(call_history.incoming_calls) == 1
    for c in calls:
        assert c in call_history.incoming_calls[(date.month, date.year)] 


def test_register_incoming_call_diff_month():
    call_history = CallHistory()
    times = ["2018-01-03 02:14:31", "2018-02-04 02:14:31", "2017-12-04 02:14:31", "2019-01-04 02:14:31"]
    
    src_num = ["131-4520", "123-4567", "123-3333", "888-8888"]
    dst_num = ["114-5141", "890-1314", "250-0520", "148-2050"]
    dates = []
    for t in times:
        dates.append(datetime.strptime(t, "%Y-%m-%d %H:%M:%S"))
    
    calls = []
    for i in range(4):
        call = Call(src_num[i], dst_num[i], dates[i], 120, (-79.42, 43.64), (-79.52, 43.75))
        calls.append(call)
        call_history.register_incoming_call(call)
        

    assert len(call_history.incoming_calls) == 4
    for i in range(4):
        assert calls[i] in call_history.incoming_calls[(dates[i].month, dates[i].year)]


def test_register_incoming_call_mix_month():
    call_history = CallHistory()
    times = ["2018-01-03 02:14:31", "2018-01-04 02:14:31", "2017-12-04 02:14:31", "2017-12-25 02:14:31"]
    
    src_num = ["131-4520", "123-4567", "123-3333", "888-8888"]
    dst_num = ["114-5141", "890-1314", "250-0520", "148-2050"]
    dates = []
    for t in times:
        dates.append(datetime.strptime(t, "%Y-%m-%d %H:%M:%S"))
    
    calls = []
    for i in range(4):
        call = Call(src_num[i], dst_num[i], dates[i], 120, (-79.42, 43.64), (-79.52, 43.75))
        calls.append(call)
        call_history.register_incoming_call(call)
        

    assert len(call_history.incoming_calls) == 2
    for i in range(4):
        assert calls[i] in call_history.incoming_calls[(dates[i].month, dates[i].year)]


if __name__ == "__main__":
    pytest.main(["callhistory_tests.py"])