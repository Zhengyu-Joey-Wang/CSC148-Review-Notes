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
from typing import Union
from phoneline import PhoneLine
from call import Call
from callhistory import CallHistory


class Customer:
    """ A MewbileTech customer.

    """
    # === Private Attributes ===
    # _id:
    #     this customer's 4 digit Customer id
    # _phone_lines:
    #     this customer's phone lines
    _id: int
    _phone_lines: list[PhoneLine]

    def __init__(self, cid: int) -> None:
        """ Create a new Customer with the <cid> id
        """
        self._id = cid
        self._phone_lines = []

    def new_month(self, month: int, year: int) -> None:
        """ Advance to a new month (specified by <month> and <year>) in the
        contracts for each phone line that this customer owns.

        Note: we don't care about payments; we assume that this customer pays
        the bill amount in full for the previous month.
        """
        for line in self._phone_lines:
            line.new_month(month, year)

    def make_call(self, call: Call) -> None:
        """ Record that a call was made from the source phone number of <call>.

        Precondition: The phone line associated with the source phone number of
        <call>, is owned by this customer
        """
        src_number = call.src_number
        for phone_line in self._phone_lines:
            number = phone_line.get_number()
            if number == src_number:
                phone_line.make_call(call)

    def receive_call(self, call: Call) -> None:
        """ Record that a call was made to the destination phone number of
        <call>.

        Precondition: The phone line associated with the destination phone
        number of <call>, is owned by this customer
        """
        dst_number = call.dst_number
        for phone_line in self._phone_lines:
            number = phone_line.get_number()
            if number == dst_number:
                phone_line.receive_call(call)

    def cancel_phone_line(self, number: str) -> Union[float, None]:
        """ Remove PhoneLine with number <number> from this customer and return
        the amount still owed by this customer.
        Return None if <number> is not owned by this customer.
        """
        fee = None
        for pl in self._phone_lines:
            if pl.get_number() == number:
                self._phone_lines.remove(pl)
                fee = pl.cancel_line()
        return fee

    # ----------------------------------------------------------
    # NOTE: You do not need to understand the implementation of
    # the following methods, to be able to solve this assignment
    # but feel free to read them to get a sense of what these do.
    # ----------------------------------------------------------

    def add_phone_line(self, pline: PhoneLine) -> None:
        """ Add a new PhoneLine to this customer.
        """
        self._phone_lines.append(pline)

    def get_phone_numbers(self) -> list[str]:
        """ Return a list of all of the numbers this customer owns
        """
        numbers = []
        for line in self._phone_lines:
            numbers.append(line.get_number())
        return numbers

    def get_id(self) -> int:
        """ Return the id for this customer
        """
        return self._id

    def __contains__(self, item: str) -> bool:
        """ Check if this customer owns the phone number <item>
        """
        contains = False
        for line in self._phone_lines:
            if line.get_number() == item:
                contains = True
        return contains

    def generate_bill(self, month: int, year: int) \
            -> tuple[int, float, list[dict]]:
        """ Return a bill summary for the <month> and <year> billing cycle,
        as a Tuple containing the customer id, total cost for all phone lines,
        and a List of bill summaries generated for each phone line.
        """
        bills = []
        total = 0
        for line in self._phone_lines:
            line_bill = line.get_bill(month, year)
            if line_bill is not None:
                bills.append(line_bill)
                total += line_bill['total']
        return self._id, total, bills

    def print_bill(self, month: int, year: int) -> None:
        """ Print the bill for the <month> and <year> billing cycle, to the
        console.

        Precondition:
        - <month> and <year> correspond to a valid bill for this customer.
        That is, the month and year cannot be outside the range of the historic
        records from the input dataset.
        """
        bill_data = self.generate_bill(month, year)
        print("========= BILL ===========")
        print("Customer id: " + str(self._id) + " month: "
              + str(month) + "/" + str(year))
        print(f'Total due this month: {bill_data[1]:.2f}')
        for line in bill_data[2]:
            print("\tnumber: " + line['number'] + "  type: " + line['type'])
        print("==========================")

    def get_history(self) \
            -> tuple[list[Call], list[Call]]:
        """ Return all the calls from the call history of this
        customer, as a tuple in the following format:
        (outgoing calls, incoming calls)
        """
        history = ([], [])
        for line in self._phone_lines:
            line_history = line.get_monthly_history()
            history[0].extend(line_history[0])
            history[1].extend(line_history[1])
        return history

    def get_call_history(self, number: str = None) -> list[CallHistory]:
        """ Return the call history for <number>, stored into a list.
        If <number> is not provided, return a list of all call histories for all
        phone lines owned by this customer.
        """
        history = []
        for line in self._phone_lines:
            if number is not None:
                if line.get_number() == number:
                    history.append(line.get_call_history())
            else:
                history.append(line.get_call_history())
        return history


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'phoneline', 'call', 'callhistory'
        ],
        'allowed-io': ['print_bill'],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
