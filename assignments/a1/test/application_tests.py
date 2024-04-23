
import pytest
from datetime import datetime

from application import create_customers, process_event_history, find_customer_by_number
from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine


def test_process_event_history_no_events():
    log = {
        "events": [],
        "customers": [
            {"lines": [{"number": "861-1710", "contract": "mtm"}], "id": 2247},
            {"lines": [{"number": "386-6346", "contract": "term"}], "id": 3895}
        ]
    }
    customer_list = create_customers(log)
    process_event_history(log, customer_list)
    customer_send = find_customer_by_number("861-1710", customer_list)
    customer_receive = find_customer_by_number("386-6346", customer_list)
    assert len(customer_send.get_history()[0]) == 0
    assert len(customer_receive.get_history()[1]) == 0
    
    
def test_process_event_history_multiple_events():
    log = {
        "events": [
            {"type": "sms",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-01 01:01:01",
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "sms",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-01 01:01:02",
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "sms",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-01 01:01:03",
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "call",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-03 02:14:31",
            "duration": 80,
            "src_loc": [-79.45188229255568, 43.62186408875219],
            "dst_loc": [-79.36866519485261, 43.680793196449336]},
            {"type": "call",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-04 02:14:31",
            "duration": 90,
            "src_loc": [-79.45188229255568, 43.62186408875219],
            "dst_loc": [-79.36866519485261, 43.680793196449336]}
        ],
        "customers": [
            {"lines": [{"number": "861-1710", "contract": "mtm"}], "id": 2247},
            {"lines": [{"number": "386-6346", "contract": "term"}], "id": 3895}
        ]
    }
    customer_list = create_customers(log)
    process_event_history(log, customer_list)
    customer_send = find_customer_by_number("861-1710", customer_list)
    customer_receive = find_customer_by_number("386-6346", customer_list)
    sender_call_history = customer_send.get_history()[0]
    receiver_call_history = customer_receive.get_history()[1]
    
    assert len(sender_call_history) == 2
    sender_duration = 0
    for s in sender_call_history:
        sender_duration += s.duration
    assert sender_duration == 170
    
    assert len(receiver_call_history) == 2
    receiver_duration = 0
    for r in receiver_call_history:
        receiver_duration += r.duration
    assert receiver_duration == 170
    assert receiver_duration == 170
    
    
def test_process_event_history_genral():
    log = {
        "events": [
            {"type": "call",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-03 02:14:31",
            "duration": 80,
            "src_loc": [-79.45188229255568, 43.62186408875219],
            "dst_loc": [-79.36866519485261, 43.680793196449336]}
        ],
        "customers": [
            {"lines": [{"number": "861-1710", "contract": "mtm"}], "id": 2247},
            {"lines": [{"number": "386-6346", "contract": "term"}], "id": 3895}
        ]
    }
    customer_list = create_customers(log)

    process_event_history(log, customer_list)
    customer_send = find_customer_by_number("861-1710", customer_list)
    customer_receive = find_customer_by_number("386-6346", customer_list)
    sender_call_history = customer_send.get_history()[0]
    receiver_call_history = customer_receive.get_history()[1]

    # Check if the call is correctly registered in the call history of the sender
    assert len(sender_call_history) == 1
    assert sender_call_history[0].src_number == "861-1710"
    assert sender_call_history[0].dst_number == "386-6346"
    assert sender_call_history[0].src_loc == [-79.45188229255568, 43.62186408875219]
    assert sender_call_history[0].dst_loc == [-79.36866519485261, 43.680793196449336]
    assert sender_call_history[0].duration == 80
    assert sender_call_history[0].time == datetime.strptime("2018-01-03 02:14:31", "%Y-%m-%d %H:%M:%S")

    # Check if the call is correctly registered in the call history of the receiver
    assert len(receiver_call_history) == 1
    assert receiver_call_history[0].src_number == "861-1710"
    assert receiver_call_history[0].dst_number == "386-6346"
    assert receiver_call_history[0].src_loc == [-79.45188229255568, 43.62186408875219]
    assert receiver_call_history[0].dst_loc == [-79.36866519485261, 43.680793196449336]
    assert receiver_call_history[0].duration == 80
    assert receiver_call_history[0].time == datetime.strptime("2018-01-03 02:14:31", "%Y-%m-%d %H:%M:%S")


# def test_process_event_history_no_customers():
#     log = {
#         "events": [
#             {"type": "call",
#             "src_number": "861-1710",
#             "dst_number": "386-6346",
#             "time": "2018-01-03 02:14:31",
#             "duration": 80,
#             "src_loc": [-79.45188229255568, 43.62186408875219],
#             "dst_loc": [-79.36866519485261, 43.680793196449336]}
#         ],
#         "customers": []
#     }
#     customer_list = create_customers(log)
#     process_event_history(log, customer_list)
#     customer_send = find_customer_by_number("861-1710", customer_list)
#     customer_receive = find_customer_by_number("386-6346", customer_list)
#     assert customer_send is None
#     assert customer_receive is None


if __name__ == '__main__':
    pytest.main(['application_tests.py'])