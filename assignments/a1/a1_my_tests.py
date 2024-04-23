import pytest
from datetime import datetime, date

from application import create_customers, process_event_history, find_customer_by_number
from bill import Bill
from callhistory import CallHistory
from call import Call
from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from filter import DurationFilter, CustomerFilter, ResetFilter, LocationFilter
from phoneline import PhoneLine

###################
# Helper function #
###################
def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

def create_call_objects(scr_num: str, dst_num: str, call_time: datetime, durtation: int) -> Call:
    """ Create diffent call object for test case """
    dutation_in_seconds = durtation
    src_loc = (-79.42848154284123, 43.641401675960374)
    dst_loc = (-79.52745693913239, 43.750338501653374)
    call = Call(scr_num, dst_num, call_time, dutation_in_seconds, src_loc, dst_loc)
    return call

def create_call_objects_no_dutation(scr_num: str, dst_num: str, call_time: datetime) -> Call:
    """ Create diffent call object for test case """
    dutation_in_seconds = 50
    src_loc = (-79.42848154284123, 43.641401675960374)
    dst_loc = (-79.52745693913239, 43.750338501653374)
    call = Call(scr_num,dst_num,call_time,dutation_in_seconds,src_loc,dst_loc)
    return call

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

########################
# Test case start here #
########################
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
            assert pl.contract.start == date(
                year=2017, month=12, day=25)
            if hasattr(pl.contract, 'end'):  # only check if there is an end date (TermContract)
                assert pl.contract.end == date(
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
            assert len(result) == expected_return_lengths[i][j]


if __name__ == "__main__":
    pytest.main(["a1_my_tests.py"])