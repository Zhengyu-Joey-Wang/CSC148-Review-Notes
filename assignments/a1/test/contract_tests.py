import pytest
from datetime import datetime, date

from application import create_customers, process_event_history, find_customer_by_number
from contract import TermContract, MTMContract, PrepaidContract, Contract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine
from callhistory import CallHistory
from call import Call
from bill import Bill

def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")


def create_call_objects(scr_num: str, dst_num: str, call_time: datetime, durtation: int) -> Call:
    """ Create diffent call object for test case """
    dutation_in_seconds = durtation
    src_loc = (-79.42848154284123, 43.641401675960374)
    dst_loc = (-79.52745693913239, 43.750338501653374)
    call = Call(scr_num, dst_num, call_time, dutation_in_seconds, src_loc, dst_loc)
    return call


def test_term_contract_with_no_call():
    """ Test the TermContract class basic method """
    start = date(year=2017, month=12, day=25)
    end = date(year=2018, month=12, day=25)
    term_contract = TermContract(start, end)
    
    # check if the start and end date corrct
    assert term_contract.start == start
    assert term_contract.end == end
    
    # check if the first bill take correctly
    term_contract.new_month(12, 2017, Bill())
    first_bill = term_contract.bill

    assert first_bill.billed_min == 0
    assert first_bill.free_min == 0
    assert first_bill.min_rate == 0.1
    assert first_bill.fixed_cost == 320
    assert first_bill.type == "TERM"
    assert first_bill.get_cost() == pytest.approx(320)
    
    # bill take after first month
    term_contract.new_month(1, 2018, Bill())
    new_bill = term_contract.bill
    assert new_bill.billed_min == 0
    assert new_bill.free_min == 0
    assert new_bill.min_rate == 0.1
    assert new_bill.fixed_cost == 20
    assert new_bill.type == "TERM"
    assert new_bill.get_cost() == pytest.approx(20)
    

def test_term_contract_with_call_under_free_min():
    start = date(year=2017, month=12, day=25)
    end = date(year=2018, month=12, day=25)
    term_contract = TermContract(start, end)
    
    term_contract.new_month(1, 2018, Bill())
    
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 600)
    term_contract.bill_call(call)
    
    # check if billed correct
    new_bill = term_contract.bill
    assert new_bill.billed_min == 0
    assert new_bill.free_min == 10
    assert new_bill.min_rate == 0.1
    assert new_bill.fixed_cost == 20
    assert new_bill.type == "TERM"
    assert new_bill.get_cost() == pytest.approx(20)
    

def test_term_contract_with_call_over_free_min():
    start = date(year=2017, month=12, day=25)
    end = date(year=2018, month=12, day=25)
    term_contract = TermContract(start, end)
    
    term_contract.new_month(1, 2018, Bill())
    
    # with one call
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 7200)
    term_contract.bill_call(call)
    
    # check if billed correct
    new_bill = term_contract.bill
    assert new_bill.billed_min == 20
    assert new_bill.free_min == 100
    assert new_bill.min_rate == 0.1
    assert new_bill.fixed_cost == 20.0
    assert new_bill.type == "TERM"
    assert new_bill.get_cost() == pytest.approx(22)
    
    # with more than one call
    term_contract.new_month(2, 2018, Bill())
    
    call_time = date(year=2018, month=2, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 5400)
    term_contract.bill_call(call)
    assert term_contract.bill.free_min == 90
    assert term_contract.bill.get_cost() == pytest.approx(20)
    
    new_call = create_call_objects("123-1234", "321-4321", call_time, 690)
    term_contract.bill_call(new_call)
    # check if billed correct
    new_bill = term_contract.bill
    assert new_bill.billed_min == 2
    assert new_bill.free_min == 100
    assert new_bill.min_rate == 0.1
    assert new_bill.fixed_cost == 20.0
    assert new_bill.type == "TERM"
    assert new_bill.get_cost() == pytest.approx(20.2)
    
    
def test_term_contract_cancel():
    start = date(year=2017, month=12, day=25)
    end = date(year=2018, month=12, day=25)
    
    # cancel at start month
    term_contract = TermContract(start, end)
    term_contract.new_month(12, 2017, Bill())
    deposit = term_contract.cancel_contract()
    assert term_contract.start is None
    assert term_contract.end is None
    assert deposit == 320
    
    # cancel between start and end month
    term_contract = TermContract(start, end)
    term_contract.new_month(3, 2018, Bill())
    deposit = term_contract.cancel_contract()
    assert term_contract.start is None
    assert term_contract.end is None
    assert deposit == 20
    
    # cancel at end month
    term_contract = TermContract(start, end)
    term_contract.new_month(12, 2018, Bill())
    deposit = term_contract.cancel_contract()
    assert term_contract.start is None
    assert term_contract.end is None
    assert deposit == pytest.approx(20)
    
    # cancel after end month
    term_contract = TermContract(start, end)
    term_contract.new_month(1, 2019, Bill())
    deposit = term_contract.cancel_contract()
    assert term_contract.start is None
    assert term_contract.end is None
    assert deposit == pytest.approx(-280)
    
    
def test_mtm_contract_with_no_call():
    """ Test the TermContract class basic method """
    start = date(year=2017, month=12, day=25)
    mtm_contract = MTMContract(start)
    
    # check if the start and end date corrct
    assert mtm_contract.start == start
    
    # check if the first bill take correctly
    mtm_contract.new_month(12, 2017, Bill())
    first_bill = mtm_contract.bill

    assert first_bill.billed_min == 0
    assert first_bill.free_min == 0
    assert first_bill.min_rate == 0.05
    assert first_bill.fixed_cost == 50
    assert first_bill.type == "MTM"
    assert first_bill.get_cost() == pytest.approx(50)
    
    # bill take after first month
    mtm_contract.new_month(1, 2018, Bill())
    new_bill = mtm_contract.bill
    assert new_bill.billed_min == 0
    assert new_bill.free_min == 0
    assert new_bill.min_rate == 0.05
    assert new_bill.fixed_cost == 50
    assert new_bill.type == "MTM"
    assert new_bill.get_cost() == pytest.approx(50)
    
    
def test_mtm_contract_with_call():
    start = date(year=2017, month=12, day=25)
    mtm_contract = MTMContract(start)
    
    # check if the start and end date corrct
    assert mtm_contract.start == start
    
    mtm_contract.new_month(1, 2018, Bill())
    
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 600)
    mtm_contract.bill_call(call)
    
    # check if billed correct
    new_bill = mtm_contract.bill
    assert new_bill.billed_min == 10
    assert new_bill.free_min == 0
    assert new_bill.min_rate == 0.05
    assert new_bill.fixed_cost == 50
    assert new_bill.type == "MTM"
    assert new_bill.get_cost() == pytest.approx(50.5)
    
    
def test_mtm_contract_cancel():
    start = date(year=2017, month=12, day=25)
    mtm_contract = MTMContract(start)
    
    # check if the start and end date corrct
    assert mtm_contract.start == start
    
    mtm_contract.new_month(1, 2018, Bill())
    left_bill = mtm_contract.cancel_contract()
    assert mtm_contract.start is None
    assert left_bill == pytest.approx(50)
    
    
def test_prepaid_contract_with_no_call():
    start = date(year=2017, month=12, day=25)
    prepaid_contract = PrepaidContract(start, 100)
    
    # check init correct
    assert prepaid_contract.start == start
    assert prepaid_contract.balance == -100
    
    # check if the inition bill correct
    prepaid_contract.new_month(12, 2017, Bill())
    assert prepaid_contract.balance == -100
    first_bill = prepaid_contract.bill
    assert first_bill.billed_min == 0
    assert first_bill.free_min == 0
    assert first_bill.min_rate == 0.025
    assert first_bill.fixed_cost == -100
    assert first_bill.type == "PREPAID"
    assert first_bill.get_cost() == pytest.approx(-100)
    
    # bill take after first month
    prepaid_contract.new_month(1, 2018, Bill())
    assert prepaid_contract.balance == -100
    new_bill = prepaid_contract.bill
    assert new_bill.billed_min == 0
    assert new_bill.free_min == 0
    assert new_bill.min_rate == 0.025
    assert new_bill.fixed_cost == -100
    assert new_bill.type == "PREPAID"
    assert new_bill.get_cost() == pytest.approx(-100)
    
    
def test_prepaid_contract_with_call_balance_over_10():
    start = date(year=2017, month=12, day=25)
    prepaid_contract = PrepaidContract(start, 20)
    
    # check init correct
    assert prepaid_contract.start == start
    assert prepaid_contract.balance == -20
    
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 12000)
    prepaid_contract.new_month(1, 2018, Bill())
    assert prepaid_contract.balance == -20
    prepaid_contract.bill_call(call)

    assert prepaid_contract.balance == pytest.approx(-15)

    # check if billed correct
    new_bill = prepaid_contract.bill
    assert new_bill.billed_min == 200
    assert new_bill.free_min == 0
    assert new_bill.min_rate == 0.025
    assert new_bill.fixed_cost == -20
    assert new_bill.type == "PREPAID"
    assert new_bill.get_cost() == pytest.approx(-15)
    
    # check if balance transfer to next month
    prepaid_contract.new_month(2, 2018, Bill())
    assert prepaid_contract.balance == pytest.approx(-15)
    prepaid_contract.new_month(12, 2019, Bill())
    assert prepaid_contract.balance == pytest.approx(-15)
    
    
def test_prepaid_contract_with_call_balance_under_10():
    start = date(year=2017, month=12, day=25)
    
    # test when init balance under 10
    prepaid_contract = PrepaidContract(start, 5)
    # check init correct
    assert prepaid_contract.start == start
    assert prepaid_contract.balance == -5
    
    # check if first month bill
    prepaid_contract.new_month(12, 2017, Bill())
    assert prepaid_contract.balance == pytest.approx(-30)
    
    # after call the balance under 10
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 60000)
    prepaid_contract.new_month(1, 2018, Bill())
    prepaid_contract.bill_call(call)
    assert prepaid_contract.balance == pytest.approx(-5)
    # check if billed correct
    new_bill = prepaid_contract.bill
    assert new_bill.billed_min == 1000
    assert new_bill.free_min == 0
    assert new_bill.min_rate == 0.025
    assert new_bill.fixed_cost == -30
    assert new_bill.type == "PREPAID"
    assert new_bill.get_cost() == pytest.approx(-5)
    
    # check if balance add $25 and transfer to next month
    prepaid_contract.new_month(2, 2018, Bill())
    assert prepaid_contract.balance == pytest.approx(-30)
    prepaid_contract.new_month(12, 2019, Bill())
    assert prepaid_contract.balance == pytest.approx(-30)
    
    
def test_cancel_contract_with_credit():
    start = date(year=2017, month=12, day=25)
    
    # check when cancel at start month with no call
    prepaid_contract = PrepaidContract(start, 30)
    prepaid_contract.new_month(12, 2017, Bill())
    left_over_bill = prepaid_contract.cancel_contract()
    assert left_over_bill == 0
    assert prepaid_contract.balance == 0
    assert prepaid_contract.start is None
    
    # check when cancel after start month with no call
    prepaid_contract = PrepaidContract(start, 30)
    prepaid_contract.new_month(12, 2018, Bill())
    left_over_bill = prepaid_contract.cancel_contract()
    assert left_over_bill == 0
    assert prepaid_contract.balance == 0
    assert prepaid_contract.start is None
    
    # check cancel with call and at same month
    prepaid_contract = PrepaidContract(start, 30)
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 60000)
    prepaid_contract.new_month(1, 2018, Bill())
    prepaid_contract.bill_call(call)
    left_over_bill = prepaid_contract.cancel_contract()
    assert left_over_bill == 0
    assert prepaid_contract.balance == 0
    assert prepaid_contract.start is None
    
    # check cancel with call and at different month
    prepaid_contract = PrepaidContract(start, 30)
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 60000)
    prepaid_contract.new_month(1, 2018, Bill())
    prepaid_contract.bill_call(call)
    prepaid_contract.new_month(2, 2018, Bill())
    left_over_bill = prepaid_contract.cancel_contract()
    assert left_over_bill == 0
    assert prepaid_contract.balance == 0
    assert prepaid_contract.start is None
    
def test_cancel_contract_with_no_credit_left():
    start = date(year=2017, month=12, day=25)
    
    # check cancel with call and at same month
    prepaid_contract = PrepaidContract(start, 20)
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 60000)
    prepaid_contract.new_month(1, 2018, Bill())
    prepaid_contract.bill_call(call)
    left_over_bill = prepaid_contract.cancel_contract()
    assert left_over_bill == 5
    assert prepaid_contract.start is None
    
    # check cancel with call and at different month
    prepaid_contract = PrepaidContract(start, 20)
    call_time = date(year=2018, month=1, day=25)
    call = create_call_objects("123-1234", "321-4321", call_time, 60000)
    prepaid_contract.new_month(1, 2018, Bill())
    prepaid_contract.bill_call(call)
    prepaid_contract.new_month(2, 2018, Bill())
    left_over_bill = prepaid_contract.cancel_contract()
    assert left_over_bill == 0
    assert prepaid_contract.balance == 0
    assert prepaid_contract.start is None
    

if __name__ == "__main__":
    pytest.main(["contract_tests.py"])