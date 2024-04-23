"""
CSC148, Winter 2024
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime

import pytest

from application import create_customers, process_event_history
from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine

"""
This is a sample test file with a limited set of cases, which are similar in
nature to the full autotesting suite

Use this framework to check some of your work and as a starting point for
creating your own tests

*** Passing these tests does not mean that it will necessarily pass the
autotests ***
"""


def create_single_customer_with_all_lines() -> Customer:
    """ Create a customer with one of each type of PhoneLine
    """
    contracts = [
        TermContract(start=datetime.date(year=2017, month=12, day=25),
                     end=datetime.date(year=2019, month=6, day=25)),
        MTMContract(start=datetime.date(year=2017, month=12, day=25)),
        PrepaidContract(start=datetime.date(year=2017, month=12, day=25),
                        balance=100)
    ]
    numbers = ['867-5309', '273-8255', '649-2568']
    customer = Customer(cid=7777)

    for i in range(len(contracts)):
        customer.add_phone_line(PhoneLine(numbers[i], contracts[i]))

    customer.new_month(12, 2017)
    print(str(customer))
    return customer


test_dict = {
    'events': [
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
        "dst_loc": [-79.52745693913239, 43.750338501653374]}
    ],
    'customers': [
        {'lines': [
            {'number': '867-5309',
             'contract': 'term'},
            {'number': '273-8255',
             'contract': 'mtm'},
            {'number': '649-2568',
             'contract': 'prepaid'}
        ],
            'id': 7777}
    ]
}

def test_customer_creation() -> None:
    """ Test for the correct creation of Customer, PhoneLine, and Contract
    classes
    """
    customer = create_single_customer_with_all_lines()
    bill = customer.generate_bill(12, 2017)

    assert len(customer.get_phone_numbers()) == 3
    assert len(bill) == 3
    assert bill[0] == 7777
    assert bill[1] == 270.0
    assert len(bill[2]) == 3
    assert bill[2][0]['total'] == 320
    assert bill[2][1]['total'] == 50
    assert bill[2][2]['total'] == -100

    # Check for the customer creation in application.py
    customer = create_customers(test_dict)[0]
    customer.new_month(12, 2017)
    bill = customer.generate_bill(12, 2017)

    assert len(customer.get_phone_numbers()) == 3
    assert len(bill) == 3
    assert bill[0] == 7777
    assert bill[1] == 270.0
    assert len(bill[2]) == 3
    assert bill[2][0]['total'] == 320
    assert bill[2][1]['total'] == 50
    assert bill[2][2]['total'] == -100


def test_events() -> None:
    """ Test the ability to make calls, and ensure that the CallHistory objects
    are populated
    """
    customers = create_customers(test_dict)
    customers[0].new_month(1, 2018)

    process_event_history(test_dict, customers)

    # Check the bill has been computed correctly
    bill = customers[0].generate_bill(1, 2018)
    assert bill[0] == 7777
    assert bill[1] == pytest.approx(-29.925)
    assert bill[2][0]['total'] == pytest.approx(20)
    assert bill[2][0]['free_mins'] == 1
    assert bill[2][1]['total'] == pytest.approx(50.05)
    assert bill[2][1]['billed_mins'] == 1
    assert bill[2][2]['total'] == pytest.approx(-99.975)
    assert bill[2][2]['billed_mins'] == 1

    # Check the CallHistory objects are populated
    history = customers[0].get_call_history('867-5309')
    assert len(history) == 1
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1

    history = customers[0].get_call_history()
    assert len(history) == 3
    assert len(history[0].incoming_calls) == 1
    assert len(history[0].outgoing_calls) == 1


def test_contract_start_dates() -> None:
    """ Test the start dates of the contracts.

    Ensure that the start dates are the correct dates as specified in the given
    starter code.
    """
    customers = create_customers(test_dict)
    for c in customers:
        for pl in c._phone_lines:
            assert pl.contract.start == datetime.date(
                year=2017, month=12, day=25)
            if hasattr(pl.contract, 'end'):  # only check if there is an end date (TermContract)
                assert pl.contract.end == datetime.date(
                    year=2019, month=6, day=25)


def test_filters() -> None:
    """ Test the functionality of the filters.

    We are only giving you a couple of tests here, you should expand both the
    dataset and the tests for the different types of applicable filters
    """
    customers = create_customers(test_dict)
    process_event_history(test_dict, customers)

    # Populate the list of calls:
    calls = []
    hist = customers[0].get_history()
    # only consider outgoing calls, we don't want to duplicate calls in the test
    calls.extend(hist[0])

    # The different filters we are testing
    filters = [
        DurationFilter(),
        CustomerFilter(),
        ResetFilter()
    ]

    # These are the inputs to each of the above filters in order.
    # Each list is a test for this input to the filter
    filter_strings = [
        ["L050", "G010", "L000", "50", "AA", ""],
        ["7777", "1111", "9999", "aaaaaaaa", ""],
        ["rrrr", ""]
    ]

    # These are the expected outputs from the above filter application
    # onto the full list of calls
    expected_return_lengths = [
        [1, 2, 0, 3, 3, 3],
        [3, 3, 3, 3, 3],
        [3, 3]
    ]

    for i in range(len(filters)):
        for j in range(len(filter_strings[i])):
            result = filters[i].apply(customers, calls, filter_strings[i][j])
            if len(result) != expected_return_lengths[i][j]:
                print(i, j)
            assert len(result) == expected_return_lengths[i][j]


if __name__ == '__main__':
    pytest.main(['sample_tests.py'])
