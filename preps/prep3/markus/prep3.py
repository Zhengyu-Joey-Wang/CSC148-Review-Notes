"""Prep 3 Synthesize

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module contains an illustration of *inheritance* through an abstract
Employee class that defines a common interface for all of its subclasses.
"""
from datetime import date


class Employee:
    """An employee of a company.

    This is an abstract class. Only child classes should be instantiated.

    === Public attributes ===
    id_: This employee's ID number.
    name: This employee's name.
    
    === Private attributes ===
    _paid_amount: This is the amount of salary employess has received
    
    === Representation invariants ===
    - _paid_amount >= 0
    """
    id_: int
    name: str
    _paid_amount: float

    def __init__(self, id_: int, name: str) -> None:
        """Initialize this employee.

        Note: This initializer is meant for internal use only;
        Employee is an abstract class and should not be instantiated directly.
        """
        self.id_ = id_
        self.name = name
        self._paid_amount = 0.0

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        raise NotImplementedError

    def pay(self, pay_date: date) -> None:
        """Pay this Employee on the given date and record the payment.

        (Assume this is called once per month.)
        """
        payment = self.get_monthly_payment()
        self._paid_amount += payment
        print(f'An employee was paid {payment} on {pay_date}.')

    def total_pay(self) -> float:
        """Return the total amount of pay this Employee has received.

        >>> e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
        >>> e.pay(date(2018, 6, 28))
        An employee was paid 100.0 on 2018-06-28.
        >>> e.pay(date(2018, 7, 28))
        An employee was paid 100.0 on 2018-07-28.
        >>> e.pay(date(2018, 8, 28))
        An employee was paid 100.0 on 2018-08-28.
        >>> e.total_pay()
        300.0
        """
        return self._paid_amount


class SalariedEmployee(Employee):
    """An employee whose pay is computed based on an annual salary.

    === Public attributes ===
    salary: This employee's annual salary

    === Representation invariants ===
    - salary >= 0
    """
    id_: int
    name: str
    salary: float

    def __init__(self, id_: int, name: str, salary: float) -> None:
        """Initialize this salaried Employee.

        >>> e = SalariedEmployee(14, 'Fred Flintstone', 5200.0)
        >>> e.salary
        5200.0
        """
        # Note that to call the superclass' initializer, we need to use the
        # full name '__init__'. This is the only time we write '__init__'
        # explicitly.
        super().__init__(id_, name)
        self.salary = salary

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = SalariedEmployee(99, 'Mr Slate', 120000.0)
        >>> e.get_monthly_payment()
        10000.0
        """
        return round(self.salary / 12, 2)


class HourlyEmployee(Employee):
    """An employee whose pay is computed based on an hourly rate.

    === Public attributes ===
    hourly_wage:
        This employee's hourly rate of pay.
    hours_per_month:
        The number of hours this employee works each month.

    === Representation invariants ===
    - hourly_wage >= 0
    - hours_per_month >= 0
    """
    id_: int
    name: str
    hourly_wage: float
    hours_per_month: float

    def __init__(self, id_: int, name: str, hourly_wage: float,
                 hours_per_month: float) -> None:
        """Initialize this HourlyEmployee.

        >>> barney = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> barney.hourly_wage
        1.25
        >>> barney.hours_per_month
        50.0
        """
        super().__init__(id_, name)
        self.hourly_wage = hourly_wage
        self.hours_per_month = hours_per_month

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> e.get_monthly_payment()
        62.5
        """
        monthly_total = self.hours_per_month * self.hourly_wage
        return round(monthly_total, 2)


class Company:
    """A company with employees.

    We use this class mainly as a client for the various Employee classes
    we defined in employee.

    === Attributes ===
    employees: the employees in the company.
    """
    employees: list[Employee]

    def __init__(self, employees: list[Employee]) -> None:
        self.employees = employees

    def pay_all(self, pay_date: date) -> None:
        """Pay all employees at this company."""
        for employee in self.employees:
            employee.pay(pay_date)

    def total_payroll(self) -> float:
        """Return the total of all payments ever made to all employees.

        >>> my_corp = Company([\
        SalariedEmployee(24, 'Gilbert the cat', 1200.0), \
        HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
        >>> my_corp.pay_all(date(2022, 6, 28))
        An employee was paid 100.0 on 2022-06-28.
        An employee was paid 500.25 on 2022-06-28.
        >>> my_corp.total_payroll()
        600.25
        """
        total_paid = 0.0
        for employee in self.employees:
            total_paid += employee.total_pay()
        return total_paid


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    # Remember: you'll need to *run this file* to actually get the lines below
    # to run. This is different than just running doctests.
    # To run this file in PyCharm, right-click in the file and select
    # "Run...", and then select "prep3" from the menu that appears.
    # DON'T select "Doctests in prep3", as that command will not actually
    # run this file, but instead only run its doctests.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['datetime'],
        'allowed-io': ['Employee.pay', 'pay']
    })
