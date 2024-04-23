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
import json

from contract import TermContract, MTMContract, PrepaidContract
from customer import Customer
from phoneline import PhoneLine
from visualizer import Visualizer
from call import Call


def import_data() -> dict[str, list[dict]]:
    """ Open the file <dataset.json> which stores the json data, and return
    a dictionary that stores this data in a format as described in the A1
    handout.

    Precondition: the dataset file must be in the json format.
    """
    with open("dataset.json") as o:
        log = json.load(o)
        return log


def create_customers(log: dict[str, list[dict]]) -> list[Customer]:
    """ Returns a list of Customer instances for each customer from the input
    dataset from the dictionary <log>.

    Precondition:
    - The <log> dictionary contains the input data in the correct format,
    matching the expected input format described in the handout.
    """
    customer_list = []
    for cust in log['customers']:
        customer = Customer(cust['id'])
        for line in cust['lines']:
            contract = None
            if line['contract'] == 'prepaid':
                # start with $100 credit on the account
                contract = PrepaidContract(datetime.date(2017, 12, 25), 100)
            elif line['contract'] == 'mtm':
                contract = MTMContract(datetime.date(2017, 12, 25))
            elif line['contract'] == 'term':
                contract = TermContract(datetime.date(2017, 12, 25),
                                        datetime.date(2019, 6, 25))
            else:
                print("ERROR: unknown contract type")

            line = PhoneLine(line['number'], contract)
            customer.add_phone_line(line)
        customer_list.append(customer)
    return customer_list


def find_customer_by_number(number: str, customer_list: list[Customer]) \
        -> Customer:
    """ Return the Customer with the phone number <number> in the list of
    customers <customer_list>.
    If the number does not belong to any customer, return None.
    """
    cust = None
    for customer in customer_list:
        if number in customer:
            cust = customer
    return cust


def new_month(customer_list: list[Customer], month: int, year: int) -> None:
    """ Advance all customers in <customer_list> to a new month of their
    contract, as specified by the <month> and <year> arguments.
    """
    for cust in customer_list:
        cust.new_month(month, year)


def process_event_history(log: dict[str, list[dict]],
                          customer_list: list[Customer]) -> None:
    """ Process the calls from the <log> dictionary. The <customer_list>
    list contains all the customers that exist in the <log> dictionary.

    Construct Call objects from <log> and register the Call into the
    corresponding customer's call history.

    Hint: You must advance all customers to a new month using the new_month()
    function, everytime a new month is detected for the current event you are
    extracting.

    Preconditions:
    - All calls are ordered chronologically (based on the call's date and time),
    when retrieved from the dictionary <log>, as specified in the handout.
    - The <log> argument guarantees that there is no "gap" month with zero
    activity for ALL customers, as specified in the handout.
    - The <log> dictionary is in the correct format, as defined in the
    handout.
    - The <customer_list> already contains all the customers from the <log>.
    """
    for event_data in log['events']:
        billing_date = datetime.datetime.strptime(event_data['time'],
                                                  "%Y-%m-%d %H:%M:%S")
        new_month(customer_list, billing_date.month, billing_date.year)
        if event_data['type'] == "call":
            # Create call object
            sn = event_data['src_number']
            dn = event_data['dst_number']
            time = datetime.datetime.strptime(event_data['time'],
                                              "%Y-%m-%d %H:%M:%S")
            duration = event_data['duration']
            sl = (event_data['src_loc'][0], event_data['src_loc'][1])
            dl = (event_data['dst_loc'][0], event_data['dst_loc'][1])
            call = Call(sn, dn, time, duration, sl, dl)
            # Assign the call to the customer
            customer_send = find_customer_by_number(sn, customer_list)
            customer_receive = find_customer_by_number(dn, customer_list)
            customer_send.make_call(call)
            customer_receive.receive_call(call)


if __name__ == '__main__':
    v = Visualizer()
    print("Toronto map coordinates:")
    print("  Lower-left corner: -79.697878, 43.576959")
    print("  Upper-right corner: -79.196382, 43.799568")

    input_dictionary = import_data()
    customers = create_customers(input_dictionary)
    process_event_history(input_dictionary, customers)

    # ----------------------------------------------------------------------
    # NOTE: You do not need to understand any of the implementation below,
    # to be able to solve this assignment. However, feel free to
    # read it anyway, just to get a sense of how the application runs.
    # ----------------------------------------------------------------------

    # Gather all calls to be drawn on screen for filtering, but we only want
    # to plot each call only once, so only plot the outgoing calls to screen.
    # (Each call is registered as both an incoming and outgoing)
    all_calls = []
    for c in customers:
        hist = c.get_history()
        all_calls.extend(hist[0])
    print("\n-----------------------------------------")
    print("Total Calls in the dataset:", len(all_calls))

    # Main loop for the application.
    # 1) Wait for user interaction with the system and processes everything
    #    appropriately
    # 2) Take the calls from the results of the filtering and create the
    #    drawables and connection lines for those calls
    # 3) Display the calls in the visualization window
    events = all_calls
    while not v.has_quit():
        events = v.handle_window_events(customers, events)

        connections = []
        drawables = []
        for event in events:
            connections.append(event.get_connection())
            drawables.extend(event.get_drawables())

        # Put the connections on top of the other sprites
        drawables.extend(connections)
        v.render_drawables(drawables)

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'json', 'datetime',
            'visualizer', 'customer', 'call', 'contract', 'phoneline'
        ],
        'allowed-io': [
            'create_customers', 'import_data'
        ],
        'generated-members': 'pygame.*'
    })
