import pytest
from datetime import datetime, date

from application import create_customers, process_event_history, find_customer_by_number
from contract import TermContract, MTMContract, PrepaidContract, Contract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine
from callhistory import CallHistory
from call import Call


def create_all_type_phone_line() -> list[PhoneLine]:
    """ Create all type of phone line for test """
    contracts = [
        TermContract(start=date(year=2017, month=12, day=25),
                     end=date(year=2019, month=6, day=25)),
        MTMContract(start=date(year=2017, month=12, day=25)),
        PrepaidContract(start=date(year=2017, month=12, day=25),
                        balance=100)
    ]
    numbers = ['867-5309', '273-8255', '649-2568']
    phone_lines = []
    for i in range(len(contracts)):
        phone_lines.append(PhoneLine(numbers[i], contracts[i]))

    return phone_lines

def create_call_objects_phoneline(phone_lines: list[PhoneLine], call_time: datetime) -> list[Call]:
    """ Create diffent call object for test case """
    dutation_in_seconds = 50
    src_loc = (-79.42848154284123, 43.641401675960374)
    dst_loc = (-79.52745693913239, 43.750338501653374)
    calls = []
    for i in range(len(phone_lines)):
        sn = phone_lines[i].get_number()
        for j in range(len(phone_lines)):
            if i == j:
                continue
            dn = phone_lines[j].get_number()
            call = Call(sn, dn, call_time, dutation_in_seconds, src_loc, dst_loc)
            calls.append(call)
    return calls

def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

def test_make_call():
    # Creating all types phone lines
    phone_lines = create_all_type_phone_line()
    
    # Creating call object
    call_time = str_to_datetime("2018-01-01 01:01:03")
    calls = create_call_objects_phoneline(phone_lines, call_time)
    
    # Make the call
    idx = 0
    for i in range(0, len(calls), 2):
        phone = phone_lines[idx]
        phone.make_call(calls[i])
        phone.make_call(calls[i + 1])
        assert phone.get_number() == calls[i].src_number
        assert phone.get_number() == calls[i + 1].src_number
        idx += 1

    # Check if the call is recorded in call history
    numbers = ['867-5309', '273-8255', '649-2568']
    types = ["TERM", "MTM", "PREPAID"]
    fixed_cost = [20, 50, -100]
    free_mins = [2, 0, 0]
    billed_mins = [0, 2, 2]
    min_rate = [0.1, 0.05, 0.025]
    total_cost = [20, 50.1, -99.95]
    for i in range(len(phone_lines)):
        phone_line = phone_lines[i]
        month = call_time.month
        year = call_time.year
        call_history = phone_line.get_monthly_history(month, year)
        assert len(call_history[0]) == 2
    
        # Check if the call is billed
        bill_data = phone_line.get_bill(month, year)
    
        assert bill_data is not None
        assert bill_data['number'] == numbers[i]
        assert bill_data['type'] == types[i]
        assert bill_data['fixed'] == pytest.approx(fixed_cost[i])
        assert bill_data['free_mins'] == pytest.approx(free_mins[i])
        assert bill_data['billed_mins'] == pytest.approx(billed_mins[i])
        assert bill_data['min_rate'] == pytest.approx(min_rate[i])
        assert bill_data['total'] == pytest.approx(total_cost[i])

def test_receive_call():
    # Creating all types phone lines
    phone_lines = create_all_type_phone_line()
    
    # Creating call object
    call_time = str_to_datetime("2018-01-01 01:01:03")
    calls = create_call_objects_phoneline(phone_lines, call_time)
    
    # receive the call
    idx = 0
    for i in range(0, len(calls), 2):
        phone = phone_lines[idx]
        phone.receive_call(calls[i])
        phone.receive_call(calls[i + 1])
        idx += 1
    
    # Check if the call is recorded in call history
    numbers = ['867-5309', '273-8255', '649-2568']
    types = ["TERM", "MTM", "PREPAID"]
    fixed_cost = [20, 50, -100]
    min_rate = [0.1, 0.05, 0.025]
    total_cost = [20, 50, -100]
    for i in range(len(phone_lines)):
        phone_line = phone_lines[i]
        month = call_time.month
        year = call_time.year
        call_history = phone_line.get_monthly_history(month, year)
        assert len(call_history[1]) == 2
    
        # Check if the call is billed
        bill_data = phone_line.get_bill(month, year)
    
        assert bill_data is not None
        assert bill_data['number'] == numbers[i]
        assert bill_data['type'] == types[i]
        assert bill_data['fixed'] == fixed_cost[i]
        assert bill_data['free_mins'] == 0
        assert bill_data['billed_mins'] == 0
        assert bill_data['min_rate'] == min_rate[i]
        assert bill_data['total'] == total_cost[i]
    
if __name__ == "__main__":
    pytest.main(["phoneline_tests.py"])