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
from math import ceil
from typing import Optional
from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>. 
        This may be the first month of the contract. 
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """ A term contract for a phone line
    
    === Public Attributes ===
    end:
        Stores the end date for this contract.
    current_month:
        Stores the current billing month.
    current_year:
        Stores the current billing year.
    """
    end: datetime.datetime
    current_month: int
    current_year: int

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new TermContract with the specified 
        <start> date and <end> date. The contract starts as inactive.
        """
        super().__init__(start)
        self.end = end

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>. 
        This may be the first month of the contract. 
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost. Also store the <month> and <year> 
        to keep track of the bill current date
        """
        # init the bill
        bill.set_rates("TERM", TERM_MINS_COST)
        bill.add_fixed_cost(TERM_MONTHLY_FEE)

        # check if the bill is the first bill
        if self.start.month == month and self.start.year == year:
            bill.add_fixed_cost(TERM_DEPOSIT)

        self.current_month = month
        self.current_year = year
        self.bill = bill

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        duration = ceil(call.duration / 60.0)
        if self.bill.free_min < TERM_MINS:
            if self.bill.free_min + duration <= TERM_MINS:
                self.bill.add_free_minutes(duration)
            else:
                free_min_left = TERM_MINS - self.bill.free_min
                charge = duration - free_min_left
                self.bill.add_free_minutes(free_min_left)
                self.bill.add_billed_minutes(charge)
        else:
            self.bill.add_billed_minutes(duration)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract. If the customer cancels the contract early, 
        the deposit is forfeited. If the contract is carried to term, 
        the customer gets back the term deposit minus that month's cost.
        
        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        deposit = 0
        if self.current_year >= self.end.year:
            if self.current_year > self.end.year or \
                    self.current_month > self.end.month:

                deposit = TERM_DEPOSIT

        self.start = None
        self.end = None
        return -(deposit - self.bill.get_cost())


class MTMContract(Contract):
    """ A month to month contract for a phone line """

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>. 
        This may be the first month of the contract. 
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        # init the bill
        bill.set_rates("MTM", MTM_MINS_COST)
        bill.add_fixed_cost(MTM_MONTHLY_FEE)

        self.bill = bill


class PrepaidContract(Contract):
    """ A prepaid contract for a phone line 
    
    === Public Attributes ===
    balance:
        Track the balance for this contract, 
        where a negative balance means the customer has this much credit.
    """
    balance: float

    def __init__(self, start: datetime.date, balance: float) -> None:
        """ Create a new PrepaidContract with
        the <start> date and <balance> to tack the credit,
        starts as inactive
        Precondition:
        - <balance> should be a positive float.
        """
        super().__init__(start)
        self.balance = -balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>. 
        This may be the first month of the contract. 
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        Also keep track of balance if balance is less then $10 add $25 to it
        """
        if self.balance > -10:
            self.balance -= 25

        # init the new month bill
        bill.set_rates("PREPAID", PREPAID_MINS_COST)

        bill.fixed_cost = self.balance

        self.bill = bill

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill. Also change the balance according
        to bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))
        self.balance = self.bill.get_cost()

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated 
        with this prepaid contract. If the contract still has some credit 
        on it (a negative balance), then the amount left is forfeited and 
        returned, otherwise, return the balance.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.balance = self.bill.get_cost()
        if self.balance < 0:
            self.balance = 0
        self.start = None
        return self.balance


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
