import pytest
from datetime import datetime, date

from application import create_customers, process_event_history, find_customer_by_number
from contract import TermContract, MTMContract, PrepaidContract, Contract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter
from phoneline import PhoneLine
from callhistory import CallHistory
from call import Call

def create_single_customer_with_all_lines() -> Customer:
    """ Create a customer with one of each type of PhoneLine
    """
    contracts = [
        TermContract(start=date(year=2017, month=12, day=25),
                     end=date(year=2019, month=6, day=25)),
        MTMContract(start=date(year=2017, month=12, day=25)),
        PrepaidContract(start=date(year=2017, month=12, day=25),
                        balance=100)
    ]
    numbers = ['867-5309', '273-8255', '649-2568']
    customer = Customer(cid=7777)

    for i in range(len(contracts)):
        customer.add_phone_line(PhoneLine(numbers[i], contracts[i]))

    customer.new_month(12, 2017)
    return customer


def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")


def create_call_objects_no_dutation(scr_num: int, dst_num: int, call_time: datetime) -> Call:
    """ Create diffent call object for test case """
    dutation_in_seconds = 50
    src_loc = (-79.42848154284123, 43.641401675960374)
    dst_loc = (-79.52745693913239, 43.750338501653374)
    call = Call(scr_num,dst_num,call_time,dutation_in_seconds,src_loc,dst_loc)
    return call


def test_make_call_exist_number():
    """ Test Customer make_call() method with a number that exist """
    call_date1 = str_to_datetime("2018-01-01 01:01:03")
    call_date2 = str_to_datetime("2018-02-01 01:01:03")    
    # Create a diffent call object
    term_call1 = create_call_objects_no_dutation("867-5309", "273-8255", call_date1)
    prep_call = create_call_objects_no_dutation("649-2568", "273-8255", call_date1)
    term_call2 = create_call_objects_no_dutation("867-5309", "273-8255", call_date2)
    mtm_call = create_call_objects_no_dutation("273-8255", "649-2568", call_date2)
    
    # create an custorm
    cust = create_single_customer_with_all_lines()
    
    # make call
    # data1
    cust.new_month(call_date1.month, call_date1.year)
    cust.make_call(term_call1)
    cust.make_call(prep_call)
    # data2
    cust.new_month(call_date2.month, call_date2.year)
    cust.make_call(term_call2)
    cust.make_call(mtm_call)
    
    number = ["867-5309", "273-8255", "649-2568"]
    total_call = [2, 1, 1]
    # Check if call asign correct
    assert len(cust.get_history()[0]) == 4
    assert len(cust.get_call_history()) == 3
    for i in range(len(number)):
        all_call_history = cust.get_call_history(number[i])
        assert len(all_call_history) != 0
        call_history = all_call_history[0]
        monthly_history = call_history.get_monthly_history()
        assert len(monthly_history[0]) == total_call[i]
    
    term_his = cust.get_call_history(number[0])[0]
    term_date1_his = term_his.get_monthly_history(call_date1.month, call_date1.year)[0]
    assert len(term_date1_his) == 1
    assert term_date1_his[0] == term_call1
    term_date2_his = term_his.get_monthly_history(call_date2.month, call_date2.year)[0]
    assert len(term_date2_his) == 1
    assert term_date2_his[0] == term_call2
    
    # Check bill
    bill1 = cust.generate_bill(call_date1.month, call_date1.year)
    assert bill1[1] == pytest.approx(-29.975)
    bill2 = cust.generate_bill(call_date2.month, call_date2.year)
    assert bill2[1] == pytest.approx(-29.925)


def test_make_call_not_exist_number():
    """ Test Customer make_call() method with a number that not exist """
    call_date = str_to_datetime("2018-01-01 01:01:03")
    
    # Create a diffent call object
    sample_call = create_call_objects_no_dutation("123-1234", "223-4567", call_date)
    
    cust = create_single_customer_with_all_lines()
    cust.new_month(call_date.month, call_date.year)
    
    cust.make_call(sample_call)
    
    # Check if call asign correct
    assert len(cust.get_history()[0]) == 0
    assert len(cust.get_call_history("123-1234")) == 0
    
    # Check bill
    bill = cust.generate_bill(call_date.month, call_date.year)
    assert bill[1] == pytest.approx(-30)
    

def test_receive_call_exist_number():
    """ Test Customer receive_call() method with a number that exist """
    call_date1 = str_to_datetime("2018-01-01 01:01:03")
    call_date2 = str_to_datetime("2018-02-01 01:01:03")    
    # Create a diffent call object
    term_call1 = create_call_objects_no_dutation("867-5309", "273-8255", call_date1)
    prep_call = create_call_objects_no_dutation("649-2568", "273-8255", call_date1)
    term_call2 = create_call_objects_no_dutation("867-5309", "273-8255", call_date2)
    mtm_call = create_call_objects_no_dutation("273-8255", "649-2568", call_date2)
    
    # create an custorm
    cust = create_single_customer_with_all_lines()
    
    # make call
    # data1
    cust.new_month(call_date1.month, call_date1.year)
    cust.receive_call(term_call1)
    cust.receive_call(prep_call)
    # data2
    cust.new_month(call_date2.month, call_date2.year)
    cust.receive_call(term_call2)
    cust.receive_call(mtm_call)
    
    number = ["867-5309", "273-8255", "649-2568"]
    total_call = [0, 3, 1]
    # Check if call asign correct
    assert len(cust.get_history()[1]) == 4
    assert len(cust.get_call_history()) == 3
    for i in range(len(number)):
        all_call_history = cust.get_call_history(number[i])
        assert len(all_call_history) != 0
        call_history = all_call_history[0]
        monthly_history = call_history.get_monthly_history()
        assert len(monthly_history[1]) == total_call[i]
    
    mtm_his = cust.get_call_history(number[1])[0]
    mtm_date1_his = mtm_his.get_monthly_history(call_date1.month, call_date1.year)[1]
    assert len(mtm_date1_his) == 2
    assert mtm_date1_his[0] == term_call1
    assert mtm_date1_his[1] == prep_call
    mtm_date2_his = mtm_his.get_monthly_history(call_date2.month, call_date2.year)[1]
    assert len(mtm_date2_his) == 1
    assert mtm_date2_his[0] == term_call2
    
    # Check bill
    bill1 = cust.generate_bill(call_date1.month, call_date1.year)
    assert bill1[1] == pytest.approx(-30)
    bill2 = cust.generate_bill(call_date2.month, call_date2.year)
    assert bill2[1] == pytest.approx(-30)
    
    
def test_receive_call_not_exist_number():
    """ Test Customer receive_call() method with a number that not exist """
    call_date = str_to_datetime("2018-01-01 01:01:03")
    
    # Create a diffent call object
    sample_call = create_call_objects_no_dutation("123-1234", "223-4567", call_date)
    
    cust = create_single_customer_with_all_lines()
    cust.new_month(call_date.month, call_date.year)
    
    cust.receive_call(sample_call)
    
    
    # Check if call asign correct
    assert len(cust.get_history()[0]) == 0
    assert len(cust.get_call_history("123-1234")) == 0
    
    # Check bill
    bill = cust.generate_bill(call_date.month, call_date.year)
    assert bill[1] == pytest.approx(-30)
    
if __name__ == "__main__":
    pytest.main(["cusomer_tests.py"])
    
    
    
    
    
    

