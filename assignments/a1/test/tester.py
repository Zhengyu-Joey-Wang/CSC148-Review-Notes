import pytest

from application import create_customers, process_event_history
from filter import DurationFilter, CustomerFilter, LocationFilter

"""
This is a sample test file with a limited set of cases, which are similar in
nature to the full autotesting suite

Use this framework to check some of your work and as a starting point for
creating your own tests

*** Passing these tests does not mean that it will necessarily pass the
autotests ***
"""
# MAP_MIN = (-79.697878, 43.799568)
# MAP_MAX = (-79.196382, 43.576959)
test_dict = {'events': [
    {"type": "sms",
     "src_number": "1",
     "dst_number": "2",
     "time": "2017-12-01 01:01:01",
     "src_loc": [-79.697878, 43.588115],
     "dst_loc": [-79.196382, 43.597462]},
    {"type": "sms",
     "src_number": "1",
     "dst_number": "2",
     "time": "2018-01-01 01:01:01",
     "src_loc": [-79.69, 43.612874],
     "dst_loc": [-79.197, 43.612874]},
    {"type": "sms",
     "src_number": "2",
     "dst_number": "3",
     "time": "2018-02-01 01:01:02",
     "src_loc": [-79.4, 43.616942],
     "dst_loc": [-79.5, 43.623401]},
    {"type": "sms",
     "src_number": "3",
     "dst_number": "4",
     "time": "2018-03-01 01:01:03",
     "src_loc": [-79.4, 43.623401],
     "dst_loc": [-79.5, 43.623401]},
    {"type": "sms",
     "src_number": "2",
     "dst_number": "4",
     "time": "2018-04-01 01:01:03",
     "src_loc": [-79.4, 43.632011],
     "dst_loc": [-79.5, 43.632011]},
    {"type": "sms",
     "src_number": "3",
     "dst_number": "4",
     "time": "2018-05-01 01:01:03",
     "src_loc": [-79.4, 43.649827],
     "dst_loc": [-79.5, 43.649827]},
    {"type": "sms",
     "src_number": "3",
     "dst_number": "4",
     "time": "2018-06-01 01:01:03",
     "src_loc": [-79.69, 43.702349],
     "dst_loc": [-79.5, 43.702349]},
    {"type": "sms",
     "src_number": "3",
     "dst_number": "4",
     "time": "2018-07-01 01:01:03",
     "src_loc": [-79.4, 43.6],
     "dst_loc": [-79.69, 43.58]},
    {"type": "call",
     "src_number": "1",
     "dst_number": "8",
     "time": "2018-08-01 01:01:06",
     "duration": 1200,
     "src_loc": [-79.680121, 43.588115],
     "dst_loc": [-79.643482, 43.588115]},
    {"type": "call",
     "src_number": "2",
     "dst_number": "5",
     "time": "2018-08-05 01:01:04",
     "duration": 3600,
     "src_loc": [-79.620094, 43.597462],
     "dst_loc": [-79.573725, 43.597462]},
    {"type": "call",
     "src_number": "3",
     "dst_number": "6",
     "time": "2018-08-03 01:01:05",
     "duration": 2400,
     "src_loc": [-79.4, 43.612874],
     "dst_loc": [-79.5, 43.612874]},
    {"type": "call",
     "src_number": "2",
     "dst_number": "8",
     "time": "2018-08-01 01:01:06",
     "duration": 3000,
     "src_loc": [-79.467882, 43.616942],
     "dst_loc": [-79.386234, 43.616942]},
    {"type": "call",
     "src_number": "5",
     "dst_number": "9",
     "time": "2018-09-01 01:01:06",
     "duration": 360,
     "src_loc": [-79.337646, 43.623401],
     "dst_loc": [-79.307385, 43.623401]},
    {"type": "call",
     "src_number": "6",
     "dst_number": "9",
     "time": "2018-10-01 01:01:06",
     "duration": 300,
     "src_loc": [-79.265799, 43.632011],
     "dst_loc": [-79.247105, 43.632011]},
    {"type": "call",
     "src_number": "8",
     "dst_number": "9",
     "time": "2018-10-02 01:01:07",
     "duration": 120000,
     "src_loc": [-79.215672, 43.649827],
     "dst_loc": [-79.204927, 43.649827]},
    {"type": "call",
     "src_number": "9",
     "dst_number": "8",
     "time": "2018-10-01 01:01:06",
     "duration": 54000,
     "src_loc": [-79.680121, 43.702349],
     "dst_loc": [-79.643482, 43.702349]},
    {"type": "call",
     "src_number": "9",
     "dst_number": "8",
     "time": "2018-11-01 01:01:06",
     "duration": 240000,
     "src_loc": [-79.620094, 43.721588],
     "dst_loc": [-79.573725, 43.721588]},
    {"type": "sms",
     "src_number": "3",
     "dst_number": "4",
     "time": "2018-12-01 01:01:03",
     "src_loc": [-79.467882, 43.6],
     "dst_loc": [-79.386234, 43.7]},
    {"type": "call",
     "src_number": "8",
     "dst_number": "9",
     "time": "2019-1-01 01:01:06",
     "duration": 5400,
     "src_loc": [-79.337646, 43.744606],
     "dst_loc": [-79.307385, 43.744606]},
    {"type": "call",
     "src_number": "8",
     "dst_number": "6",
     "time": "2019-1-01 01:01:06",
     "duration": 600,
     "src_loc": [-79.307385, 43.786521],
     "dst_loc": [-79.247105, 43.799568]},
    {"type": "call",
     "src_number": "8",
     "dst_number": "8",
     "time": "2019-1-01 01:01:06",
     "duration": 1800,
     "src_loc": [-79.215672, 43.786521],
     "dst_loc": [-79.204927, 43.799568]},
    # {"type": "call",
    #  "src_number": "4",
    #  "dst_number": "5",
    #  "time": "2019-1-01 01:01:06",
    #  "duration": 1800,
    #  "src_loc": [-79.215672, 43.786521],
    #  "dst_loc": [-79.204927, 43.799568]},
    # {"type": "call",
    #  "src_number": "8",
    #  "dst_number": "9",
    #  "time": "2019-7-01 01:01:06",
    #  "duration": 1800,
    #  "src_loc": [-79.215672, 43.786521],
    #  "dst_loc": [-79.204927, 43.799568]}

],
    "customers": [
        {"lines": [{"number": "1", "contract": "term"},
                   {"number": "2", "contract": "mtm"},
                   {"number": "3", "contract": "prepaid"}], "id": 1001},
        {"lines": [{"number": "4", "contract": "term"},
                   {"number": "6", "contract": "mtm"},
                   {"number": "5", "contract": "prepaid"}], "id": 1002},
        {"lines": [{"number": "8", "contract": "term"},
                   {"number": "9", "contract": "prepaid"}], "id": 1003}
    ]
}


def test_customer_creation() -> None:
    """ Test for the correct creation of Customer, PhoneLine, and Contract
    classes
    """
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    assert len(customer) == 3

    assert len(customer[0].get_phone_numbers()) == 3
    assert len(customer[1].get_phone_numbers()) == 3
    assert len(customer[2].get_phone_numbers()) == 2


def test_event_1() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    bill_1 = customer[1].generate_bill(12, 2017)
    assert bill_1[0] == 1002
    assert bill_1[1] == 270
    assert len(bill_1[2]) == 3
    assert bill_1[2][0]['total'] == 320
    assert bill_1[2][0]['free_mins'] == 0
    assert bill_1[2][1]['total'] == 50
    assert bill_1[2][2]['total'] == -100


def test_event_2() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    bill_2 = customer[0].generate_bill(8, 2018)

    assert len(bill_2) == 3
    assert bill_2[0] == 1001
    assert bill_2[1] == -23.5
    assert len(bill_2[2]) == 3
    assert bill_2[2][0]['total'] == 20
    assert bill_2[2][0]['free_mins'] == 20
    assert bill_2[2][1]['total'] == 55.5
    assert bill_2[2][2]['total'] == -99


def test_term_1() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    bill_3 = customer[2].generate_bill(10, 2018)

    assert len(bill_3) == 3
    assert bill_3[0] == 1003
    assert bill_3[1] == 132.5
    assert len(bill_3[2]) == 2
    assert bill_3[2][0]['total'] == 210
    assert bill_3[2][0]['free_mins'] == 100
    assert bill_3[2][0]['billed_mins'] == 1900
    assert bill_3[2][1]['total'] == -77.5


def test_prepaid_1() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    bill_4 = customer[2].generate_bill(11, 2018)
    assert bill_4[0] == 1003
    assert bill_4[1] == 42.5
    assert len(bill_4[2]) == 2
    assert bill_4[2][0]['total'] == 20
    assert bill_4[2][0]['free_mins'] == 0
    assert bill_4[2][0]['billed_mins'] == 0
    assert bill_4[2][1]['billed_mins'] == 4000
    assert bill_4[2][1]['total'] == 22.5


def test_prepaid_2() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    bill_5 = customer[2].generate_bill(12, 2018)
    assert bill_5[0] == 1003
    assert bill_5[1] == 17.5
    assert len(bill_5[2]) == 2
    assert bill_5[2][0]['total'] == 20
    assert bill_5[2][0]['free_mins'] == 0
    assert bill_5[2][0]['billed_mins'] == 0
    assert bill_5[2][1]['billed_mins'] == 0
    assert bill_5[2][1]['total'] == -2.5


def test_term_2() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    bill_3 = customer[2].generate_bill(1, 2019)

    assert len(bill_3) == 3
    assert bill_3[0] == 1003
    assert bill_3[1] == -4.5
    assert len(bill_3[2]) == 2
    assert bill_3[2][0]['total'] == 23
    assert bill_3[2][0]['free_mins'] == 100
    assert bill_3[2][0]['billed_mins'] == 30
    assert bill_3[2][1]['total'] == -27.5


# def test_cancel_contract() -> None:
#     customer = create_customers(test_dict)
#     process_event_history(test_dict, customer)
#     a = 20
#     term_1 = customer[0].cancel_phone_line('1')
#     assert term_1 == 20
#
#     term_2 = customer[1].cancel_phone_line('4')
#     assert term_2 == 23
#
#     term_3 = customer[2].cancel_phone_line('8')
#     assert term_3 == -280
#
#     mtm_1 = customer[0].cancel_phone_line('2')
#     assert mtm_1 == 50
#
#     mtm_2 = customer[0].cancel_phone_line('5')
#     assert mtm_2 == 50
#
#     prepaid_1 = customer[2].cancel_phone_line('9')
#     assert prepaid_1 == 50


def test_call_history_1() -> None:
    """ Test the ability to make calls, and ensure that the CallHistory objects
    are populated
    """
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    # Check the CallHistory objects are populated
    history = customer[2].get_call_history('9')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 3
    assert len(history[0].incoming_calls[(10, 2018)]) == 2

    assert len(history[0].outgoing_calls) == 2


def test_call_history_2() -> None:
    customer = create_customers(test_dict)
    process_event_history(test_dict, customer)

    history = customer[0].get_call_history()
    assert len(history) == 3
    assert len(history[0].incoming_calls) == 0
    assert len(history[0].outgoing_calls) == 1
    assert len(history[0].outgoing_calls[(8, 2018)]) == 1
    assert len(history[1].outgoing_calls[(8, 2018)]) == 2
    assert len(history[2].outgoing_calls[(8, 2018)]) == 1


def test_customer_filter() -> None:
    """ Test the functionality of the filters.

    We are only giving you a couple of tests here, you should expand both the
    dataset and the tests for the different types of applicable filters
    """
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)

    # Populate the list of calls:
    calls = []
    for i in range(len(customers)):
        hist = customers[i].get_history()
        for call in hist[0]:
            if call not in calls:
                calls.append(call)
        for call in hist[1]:
            if call not in calls:
                calls.append(call)

    # The different filters we are testing
    filter_1 = CustomerFilter()

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = ["7777", "1001", "1002", "1003", 'hello', 'nihao', '!@$%^&*(']

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [12, 4, 5, 10, 12, 12, 12]

    for i in range(len(filter_strings)):
        result = filter_1.apply(customers, calls, filter_strings[i])
        assert len(result) == expected_return_lengths[i]


def test_duration_filter() -> None:
    """ Test the functionality of the filters.

    We are only giving you a couple of tests here, you should expand both the
    dataset and the tests for the different types of applicable filters
    """
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)

    # Populate the list of calls:
    calls = []
    for i in range(len(customers)):
        hist = customers[i].get_history()
        for call in hist[0]:
            if call not in calls:
                calls.append(call)
        for call in hist[1]:
            if call not in calls:
                calls.append(call)

    # The different filters we are testing
    filter_2 = DurationFilter()

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = ["G200", 'G300', "L999", "Hello", '?', 'Q123', '4859']

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [12, 11, 3, 12, 12, 12, 12]

    for i in range(len(filter_strings)):
        result = filter_2.apply(customers, calls, filter_strings[i])
        if len(result) != expected_return_lengths[i]:
            print(i)
        assert len(result) == expected_return_lengths[i]


MAP_MIN = (-79.697878, 43.799568)
MAP_MAX = (-79.196382, 43.576959)


def test_location_filters() -> None:
    """ Test the functionality of the filters.

        We are only giving you a couple of tests here, you should expand both the
        dataset and the tests for the different types of applicable filters
        """
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)

    # Populate the list of calls:
    calls = []
    for i in range(len(customers)):
        hist = customers[i].get_history()
        for call in hist[0]:
            if call not in calls:
                calls.append(call)
        for call in hist[1]:
            if call not in calls:
                calls.append(call)

    # The different filters we are testing
    filter_3 = LocationFilter()

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = ["-79.643482, 43.616942, -79.247105, 43.744606",
                      '-79.6, 43.6, -79.3, 43.7',
                      "-79.643482, 43.616942, -79.247105, 43.744606",
                      "-79.9, 43.616942,-79.247105, 43.744606",
                      '12356478463829347',
                      '-79.204927, 43.799568, -79.204927, 43.799568',
                      '4859']

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [6, 3, 6, 12, 12, 1, 12]

    for i in range(len(filter_strings)):
        result = filter_3.apply(customers, calls, filter_strings[i])
        assert len(result) == expected_return_lengths[i]


if __name__ == '__main__':
    pytest.main(['tester.py'])
