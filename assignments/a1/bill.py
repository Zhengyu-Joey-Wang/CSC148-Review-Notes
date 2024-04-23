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


class Bill:
    """ A single month's bill for a customer's phone line.

    A bill keeps track of the number of calls used each month, along with the
    corresponding cost per call.
    - The billable minutes and the free minutes are incrementally updated as
    calls are loaded from the historic data.
    - The billing rate per call and the fixed monthly cost depend on the type
    of contract.

    The bill does not store the amount due. Instead, the amount due can be
    computed on demand by the get_cost() method.

    === Public Attributes ===
    billed_min:
         number of billable minutes used in the month associated with this bill.
    free_min:
         number of non-billable minutes used in the month associated with this
         bill.
    min_rate:
         cost for one minute of calling
    fixed_cost:
         fixed costs for the bill (e.g., fixed monthly cost of the
         contract, term deposits, etc.)
    type:
         type of contract

    === Representation Invariants ===
    -   billed_min >= 0
    -   free_min >= 0
    -   min_rate >= 0
    -   type: "" | "MTM" | "TERM" | "PREPAID"
    """
    billed_min: int
    free_min: int
    min_rate: float
    fixed_cost: float
    type: str

    def __init__(self) -> None:
        """ Create a new Bill.
        """
        self.billed_min = 0
        self.free_min = 0
        self.fixed_cost = 0
        self.min_rate = 0
        self.type = ""

    def set_rates(self, contract_type: str, min_cost: float) \
            -> None:
        """ Set this Bill's contract type to <contract_type>.
        Set this Bill's calling rate to <min_cost>.
        """
        self.type = contract_type
        self.min_rate = min_cost

    def add_fixed_cost(self, cost: float) -> None:
        """ Add a fixed one-time cost <cost> onto the bill.
        """
        self.fixed_cost += cost

    def add_billed_minutes(self, minutes: int) -> None:
        """ Add <minutes> minutes as billable minutes
        """
        self.billed_min += minutes

    def add_free_minutes(self, minutes: int) -> None:
        """ Add <minutes> minutes as free minutes
        """
        self.free_min += minutes

    def get_cost(self) -> float:
        """ Return bill amount, considering the rates for billable calls for
        this Bill's contract type.
        """
        return self.min_rate * self.billed_min + self.fixed_cost

    # ----------------------------------------------------------
    # NOTE: You do not need to understand the implementation of
    # the following method, to be able to solve this assignment
    # but feel free to read it to get a sense of what it does.
    # ----------------------------------------------------------

    def get_summary(self) -> dict[str, Union[float, int]]:
        """ Return a bill summary as a dictionary containing the bill details.
        """
        bill_summary = {'type': self.type,
                        'fixed': self.fixed_cost,
                        'free_mins': self.free_min,
                        'billed_mins': self.billed_min,
                        'min_rate': self.min_rate,
                        'total': self.get_cost()
                        }
        return bill_summary


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing'
        ],
        'disable': ['R0902'],
        'generated-members': 'pygame.*'
    })
