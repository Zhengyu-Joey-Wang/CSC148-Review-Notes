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
import time
import datetime
from call import Call
from customer import Customer


class Filter:
    """ A class for filtering customer data on some criterion. A filter is
    applied to a set of calls.

    This is an abstract class. Only subclasses should be instantiated.
    """
    def __init__(self) -> None:
        pass

    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all calls from <data>, which match the filter
        specified in <filter_string>.

        The <filter_string> is provided by the user through the visual prompt,
        after selecting this filter.
        The <customers> is a list of all customers from the input dataset.

         If the filter has
        no effect or the <filter_string> is invalid then return the same calls
        from the <data> input.

        Note that the order of the output matters, and the output of a filter
        should have calls ordered in the same manner as they were given, except
        for calls which have been removed.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        - all calls included in <data> are valid calls from the input dataset
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        raise NotImplementedError


class ResetFilter(Filter):
    """
    A class for resetting all previously applied filters, if any.
    """
    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Reset all of the applied filters. Return a List containing all the
        calls corresponding to <customers>.
        The <data> and <filter_string> arguments for this type of filter are
        ignored.

        Precondition:
        - <customers> contains the list of all customers from the input dataset
        """
        filtered_calls = []
        for c in customers:
            customer_history = c.get_history()
            # only take outgoing calls, we don't want to include calls twice
            filtered_calls.extend(customer_history[0])
        return filtered_calls

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Reset all of the filters applied so far, if any"


class CustomerFilter(Filter):
    """
    A class for selecting only the calls from a given customer.
    """
    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all unique calls from <data> made or
        received by the customer with the id specified in <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains a valid
        customer ID.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.

        Do not mutate any of the function arguments!
        """
        if len(filter_string) != 4 or not filter_string.isdigit():
            return data
        cid = int(filter_string)
        cust = []
        for customer in customers:
            if customer is None:
                continue
            if cid == customer.get_id():
                if customer not in cust:
                    cust.append(customer)
        if len(cust) == 0:
            return data

        unique_call = []
        for customer in cust:
            history_calls = customer.get_history()
            for call_made in history_calls[0]:
                if call_made in data and call_made not in unique_call:
                    unique_call.append(call_made)
            for call_recive in history_calls[1]:
                if call_recive in data and call_recive not in unique_call:
                    unique_call.append(call_recive)

        return unique_call

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter events based on customer ID"


class DurationFilter(Filter):
    """
    A class for selecting only the calls lasting either over or under a
    specified duration.
    """
    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all unique calls from <data> with a duration
        of under or over the time indicated in the <filter_string>.

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains the following
        input format: either "Lxxx" or "Gxxx", indicating to filter calls less
        than xxx or greater than xxx seconds, respectively.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.

        Do not mutate any of the function arguments!
        """
        if len(filter_string) != 4 or \
                (filter_string[0] != "L" and filter_string[0] != "G"):
            return data
        target_time = filter_string[1:]
        counter = 0
        for d in target_time:
            if d != '0':
                break
            counter += 1
        if counter == len(target_time):
            counter -= 1
        target_time = target_time[counter:]
        filter_key = filter_string[0]
        if not target_time.isdigit():
            return data
        target_time = int(target_time)
        unique_call = []
        for call in data:
            if filter_key == "L" and call.duration < target_time:
                if call not in unique_call:
                    unique_call.append(call)
            elif filter_key == "G" and call.duration > target_time:
                if call not in unique_call:
                    unique_call.append(call)
        return unique_call

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls based on duration; " \
               "L### returns calls less than specified length, G### for greater"


class LocationFilter(Filter):
    """
    A class for selecting only the calls that took place within a specific area
    """
    def apply(self, customers: list[Customer],
              data: list[Call],
              filter_string: str) \
            -> list[Call]:
        """ Return a list of all unique calls from <data>, which took
        place within a location specified by the <filter_string>
        (at least the source or the destination of the event was
        in the range of coordinates from the <filter_string>).

        The <customers> list contains all customers from the input dataset.

        The filter string is valid if and only if it contains four valid
        coordinates within the map boundaries.
        These coordinates represent the location of the lower left corner
        and the upper right corner of the search location rectangle,
        as 2 pairs of longitude/latitude coordinates, each separated by
        a comma and a space:
          lowerLong, lowerLat, upperLong, upperLat
        Calls that fall exactly on the boundary of this rectangle are
        considered a match as well.
        - If the filter string is invalid, return the original list <data>
        - If the filter string is invalid, your code must not crash, as
        specified in the handout.

        Do not mutate any of the function arguments!
        """
        separater = filter_string.split(",")
        if len(separater) != 4:
            return data
        low_bound = (separater[0].strip(), separater[1].strip())
        up_bound = (separater[2].strip(), separater[3].strip())

        try:
            low_bound = (float(low_bound[0]), float(low_bound[1]))
            up_bound = (float(up_bound[0]), float(up_bound[1]))
        except ValueError:
            return data
        except TypeError:
            return data

        if not self._is_valid(low_bound, up_bound):
            return data

        unique_call = []
        for call in data:
            src_cor = (call.src_loc[0], call.src_loc[1])
            dst_cor = (call.dst_loc[0], call.dst_loc[1])
            if self._bound_checker_helper(low_bound, up_bound, src_cor) or \
                    self._bound_checker_helper(low_bound, up_bound, dst_cor):

                if call not in unique_call:
                    unique_call.append(call)
        return unique_call

    def _bound_checker_helper(self,
                              lb: tuple[float, float],
                              ub: tuple[float, float],
                              target: tuple[float, float]) -> bool:
        check_low = lb[0] <= target[0] <= ub[0]
        check_up = lb[1] <= target[1] <= ub[1]
        return check_low and check_up

    def _map_bound_checker_helper(self,
                                  low: float,
                                  high: float,
                                  target1: float,
                                  target2: float) -> bool:
        return low <= target1 <= high and low <= target2 <= high

    def _is_valid(self,
                  low_bound: tuple[float, float],
                  up_bound: tuple[float, float]) -> bool:
        low_long, low_lat = low_bound[0], low_bound[1]
        up_long, up_lat = up_bound[0], up_bound[1]
        if low_long > up_long or low_lat > up_lat:
            return False
        low_map = (-79.697878, 43.576959)
        up_map = (-79.196382, 43.799568)
        check_long = self._map_bound_checker_helper(low_map[0],
                                                    up_map[0],
                                                    low_long,
                                                    up_long)
        check_lat = self._map_bound_checker_helper(low_map[1],
                                                   up_map[1],
                                                   low_lat,
                                                   up_lat)
        return check_long and check_lat

    def __str__(self) -> str:
        """ Return a description of this filter to be displayed in the UI menu
        """
        return "Filter calls made or received in a given rectangular area. " \
               "Format: \"lowerLong, lowerLat, " \
               "upperLong, upperLat\" (e.g., -79.6, 43.6, -79.3, 43.7)"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'time', 'datetime', 'call', 'customer'
        ],
        'max-nested-blocks': 4,
        'allowed-io': ['apply', '__str__'],
        'disable': ['W0611', 'W0703'],
        'generated-members': 'pygame.*'
    })
