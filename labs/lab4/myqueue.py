"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2024 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
In this module, you will develop an implementation of the Queue ADT.
It will be helpful to review the stack implementation from lecture.

After you've implemented the Queue, you'll write two different functions that
operate on a queue, paying attention to whether or not the queue should be
modified.
"""
from typing import Any, Optional


# TODO: implement this class! Note that you'll need at least one private
# attribute to store items.

class QueueEmptyError(Exception):
    """ Error raise if the accsess queue is empty """

class Queue:
    """A first-in-first-out (FIFO) queue of items.

    Stores data in a first-in, first-out order. When removing an item from the
    queue, the most recently-added item is the one that is removed.
    
    === Private varierble ===
    - _itmes - A list use to store queue itme
    """
    _itmes: list[Any]
    
    def __init__(self) -> None:
        """Initialize a new empty queue."""
        self._itmes = []

    def is_empty(self) -> bool:
        """Return whether this queue contains no items.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        return len(self._itmes) == 0

    def enqueue(self, item: Any) -> None:
        """Add <item> to the back of this queue.
        """
        self._itmes.append(item)

    def dequeue(self) -> Optional[Any]:
        """Remove and return the item at the front of this queue.

        Return None if this Queue is empty.
        (We illustrate a different mechanism for handling an erroneous case.)

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        if self.is_empty():
            raise QueueEmptyError
        return self._itmes.pop(0)


def product(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Remove all items from the queue.

    Precondition: integer_queue contains only integers.

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> q.enqueue(6)
    >>> product(q)
    48
    >>> q.is_empty()
    True
    """
    ans = 1
    while not integer_queue.is_empty():
        ans *= integer_queue.dequeue()
    return ans


def product_star(integer_queue: Queue) -> int:
    """Return the product of integers in the queue.

    Precondition: integer_queue contains only integers.

    >>> primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> prime_line = Queue()
    >>> for prime in primes:
    ...     prime_line.enqueue(prime)
    ...
    >>> product_star(prime_line)
    6469693230
    >>> prime_line.is_empty()
    False
    """
    q = Queue()
    ans = 1
    while not integer_queue.is_empty():
        temp = integer_queue.dequeue()
        q.enqueue(temp)
        ans *= temp
    while not q.is_empty():
        integer_queue.enqueue(q.dequeue())
    return ans
        


if __name__ == '__main__':
    import doctest
    doctest.testmod()
