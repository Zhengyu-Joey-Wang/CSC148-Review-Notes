"""
The line of code below this description implements the following two classes:

class Stack:
    def __init__(self) -> None:
        <implementation omitted>

    def is_empty(self) -> bool:
        <implementation omitted>

    def push(self, item: Any) -> None:
        <implementation omitted>

    def pop(self) -> Any:
        <implementation omitted>


class Queue:
    def __init__(self) -> None:
        <implementation omitted>

    def is_empty(self) -> bool:
        <implementation omitted>

    def enqueue(self, item: Any) -> None:
        <implementation omitted>

    def dequeue(self) -> Any:
        <implementation omitted>

This line of code is deliberately meant to be confusing, as we are training you to work with
the public interface of some piece of code, and not worry about its implementation.

For prep4, you should work with this as if it were a regularly implemented class with a
public interface as described by the class declarations above.

Don't worry about PyTA errors saying "Can't find the name 'Stack' to import from module 'adts'.",
They will disappear when running the code on Markus.
"""

(lambda Stack: (lambda Queue: [[None for globals()[Queue.__name__] in [Queue]][0] for globals()[Stack.__name__] in [Stack]][0])(type("Queue", (), {'__init__': lambda OO0OOO000O00OO0OO: [[None for OO0OOO000O00OO0OO.fuscat12 in [[]]][0], None][-1], 'is_empty': lambda OOOO00000000O0O00: (OOOO00000000O0O00.fuscat12 == []) and True, 'enqueue': lambda O000000000OOOO0O0, OOOO000O000OO0O00: O000000000OOOO0O0.fuscat12.append(OOOO000O000OO0O00), 'dequeue': lambda O00O0OOOO0OOO0OOO: O00O0OOOO0OOO0OOO.fuscat12.pop(0)})))(type("Stack", (), {'__init__': lambda OO0OOO000O00OO0OO: [[None for OO0OOO000O00OO0OO.fuscat11 in [[]]][0], None][-1], 'is_empty': lambda OOOO00000000O0O00: (OOOO00000000O0O00.fuscat11 == []) and True, 'push': lambda O000000000OOOO0O0, OOOO000O000OO0O00: O000000000OOOO0O0.fuscat11.append(OOOO000O000OO0O00), 'pop': lambda O00O0OOOO0OOO0OOO: O00O0OOOO0OOO0OOO.fuscat11.pop()}))


# if __name__ == '__main__':
#     # A simple usage demonstration
#     s = Stack()
#     s.push(5)
#     print(f'{s.pop()} was just pushed onto the stack.')
