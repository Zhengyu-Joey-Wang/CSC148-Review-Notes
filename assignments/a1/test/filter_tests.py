import time
import datetime
import pytest
from call import Call
from customer import Customer
from filter import CustomerFilter, DurationFilter, LocationFilter
from application import create_customers, process_event_history
from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from phoneline import PhoneLine

def test_filter_more_detail():
    filter_test_data = {
        "events": [
            {"type": "sms",
            "src_number": "867-5309",
            "dst_number": "273-8255",
            "time": "2018-01-01 01:01:01",
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "sms",
            "src_number": "273-8255",
            "dst_number": "649-2568",
            "time": "2018-01-01 01:01:02",
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "sms",
            "src_number": "649-2568",
            "dst_number": "867-5309",
            "time": "2018-01-01 01:01:03",
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "call",
            "src_number": "273-8255",
            "dst_number": "867-5309",
            "time": "2018-01-01 01:01:04",
            "duration": 10,
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "call",
            "src_number": "867-5309",
            "dst_number": "649-2568",
            "time": "2018-01-01 01:01:05",
            "duration": 50,
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745693913239, 43.750338501653374]},
            {"type": "call",
            "src_number": "649-2568",
            "dst_number": "273-8255",
            "time": "2018-01-01 01:01:06",
            "duration": 50,
            "src_loc": [-79.42848154284123, 43.641401675960374],
            "dst_loc": [-79.52745688913239, 43.750338512653374]},
            {"type": "call",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-03 02:14:31",
            "duration": 80,
            "src_loc": [-79.45188229255501, 43.62186408875201],
            "dst_loc": [-79.45188229255502, 43.62186408875202]},
            {"type": "call",
            "src_number": "861-1710",
            "dst_number": "386-6346",
            "time": "2018-01-04 02:14:31",
            "duration": 90,
            "src_loc": [-79.45188229255503, 43.62186408875203],
            "dst_loc": [-79.45188229255504, 43.62186408875204]}
        ],
        "customers": [
            {"lines": [
                {"number": "867-5309",
                "contract": "term"},
                {"number": "273-8255",
                "contract": "mtm"},
                {"number": "649-2568",
                "contract": "prepaid"}
            ],
                "id": 7777},
            {"lines": [{"number": "861-1710", "contract": "mtm"}], "id": 2247},
            {"lines": [{"number": "386-6346", "contract": "term"}], "id": 3895}
        ]
    }
    customers = create_customers(filter_test_data)
    process_event_history(filter_test_data, customers)

    # Populate the list of calls:
    calls = []
    for c in customers:
        hist = c.get_history()
        # only consider outgoing calls, we don"t want to duplicate calls in the test
        calls.extend(hist[0])

    # The different filters we are testing
    filters = [
        DurationFilter(),
        CustomerFilter(),
        LocationFilter()
    ]

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    loc_fs1 = f"-79.45188229255502, 43.62186408875201, -79.45188229255501, 43.62186408875202"
    loc_fs2 = f"-79.45188229255504, 43.62186408875201, -79.45188229255501, 43.62186408875204"
    loc_fs3 = f"-80.0, 42.0, -78.0, 43.0"
    loc_fs4 = f"-79.45188229255501, 43.62186408875202, -79.45188229255502, 43.62186408875201"
    filter_strings = [
        ["L050", "G010", "L000", "50", "AA", "", "G01F"],
        ["7777", "2247", "3895", "aaaaaaaa", "", "1234"],
        [loc_fs1, loc_fs2, loc_fs3, loc_fs4]
    ]
    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [
        [1, 4, 0, 5, 5, 5, 5],
        [3, 2, 2, 5, 5, 5],
        [1, 2, 5, 5, 5]
    ]

    for i in range(len(filters)):
        for j in range(len(filter_strings[i])):
            result = filters[i].apply(customers, calls, filter_strings[i][j])
            if len(result) != expected_return_lengths[i][j]:
                print(result)
                print(filter_strings[i][j])
            assert len(result) == expected_return_lengths[i][j]
            
            
if __name__ == "__main__":
    pytest.main(["filter_tests.py"])