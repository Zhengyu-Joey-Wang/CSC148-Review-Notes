## CSC148 Midterm1 Review

[点击这里查看中文版](./zh/CSC148-期中1-笔记.md)

[Back to the home page](../README.md)

### Memory Model

+ Variables
    + Variables store the memory address of instances (objects) `id(var)`
    + The equal sign `=` is used to assign values to variables, for example: `a = 1` assigns `id(1)` to the variable `a`

+ Storage Patterns

    + When creating a "container" — `list`, `dict`, `object`
        + Create outer variables first, then inner variables.

+ Copy Logic
    ```python
    lst = [[1], [2]]
    new_lst = lst  
    # new_lst stores id(lst)
    # Changing new_lst[i] will also change lst[i]
    
    shallow_copy = lst[:] 
    # Here, shallow_copy = [id([1]), id([2])] 
    # This is a shallow copy, only allocates a new list address to new_lst
    # Instances in new_lst are not copied
    shallow_copy[1][0] = 3
    print(lst) # [[3], [2]]
    ```
+ Python Features
    + When creating immutable instances, Python, to save memory, does not create new instances actively. It first looks in memory to see if the instance exists. If it does, it directly references the address of that instance; otherwise, it creates a new instance.
        + For example, Python pre-creates instances of numbers `1~256` in memory, and when used, Python directly uses these pre-created instances of numbers.
    + `lst.extend([1,2,3])` is equivalent to `lst += [1,2,3]`
        + Both do not change the id of `lst`

### Object-Oriented Programming (OOP)

The ability to model - turning business into several organic entities

#### Modeling Process

+ Observe the model description, identify how many "things" exist here, and whether there are relationships between them.
    + Distinguish whether an entity is an object or data.
        + Observe if it has subclass data (attributes) and actions.
    + Relationships between entities
        + Inheritance — specialization and generalization of a class
            + A subclass `extant` form parent class
        + Composition — one object is a part of another object (attribute)
            + Object holds another Object's variable
        + Usage — one object is the parameter of an action in another object
            + For example, when calling a method, the method may need an Object parameter

+ Determine data and actions
    + What type of data is each object's attribute, and are there default values?
    + What parameters does each object's action use, and what type does it return?

#### Basic Concepts of Class

+ Inside a class is a unified whole
    + All attributes can be called anywhere in the class using `self.xxx`
    + Similarly, all actions can be called anywhere in the class
    + The class is the process of designing objects, without directly using objects

+ Creating instances and calling methods

    ```python
    class A:
        def __init__(self):
            ...
            
        def foo(self, item):
            ....

    # Create an instance
    a = A()

    # Use the instance
    a.foo("test")
    A.foo(a, "test")
    ```

#### Inheritance
+ `python` is a single-inheritance language — each class has only one parent class
+ Subclasses can use all attributes of the parent class (attributes)
    + Can call attributes and methods defined in the parent class
    + But if some method are redefined, then use the updated definition (override)
        + Always use the definition closest to itself.
    + Force calling an overridden parent class method:
        + `Parent.foo(self, xxx, xxxx)`
        + `super().foo(xxx,xxxx)`
+ Private concept
    + Anything that cannot be used externally is private — cannot be used by instances
    + Use an underscore before the variable name to indicate privacy 
        + `self._id`
        + `def _foo(self, xxx)`
+ Type and instance:
    + Type checks directly by type, unrelated to inheritance
    + Instance checks depend on the type of the instance, influenced by inheritance
    
    ```Python 
    class A:
        pass
    class B(A):
        pass
    
    a = A()
    b = B()

    type(a) == type(b) # False
    isinstance(b, A) # True Here because B is a subclass of A

    # Other cases of isinstance():
    isinstance(a, B) # False
    isinstance(B, A) # False
    isinstance(A, B) # False
    ```

#### Polymorphism
+ Polymorphism generally has two possibilities
    + One is that a method is overridden from the parent class

        ```Python
        class A:
            def foo(self):
                pass
        
        class B(A):
            @overrides(A)
            def foo(self):
                pass
        ```
    + Another is having methods with the same name but different parameters in one class, known as overloading

        ```Python
        class A:

            @overload
            def foo(self, a: str):
                pass

            @overload
            def foo(self, a: str, b: int):
                pass
        ```

#### Abstract class

A class with abstract methods

+ Abstract method: In a method, if there is only one line `raise NotImplementedError`, it is called an abstract method
    + It's worth noting that a method that only raises `NotImplementedError` is not a true abstract method, as Python will not prevent us from creating an instance of this method (in other words, Python will not prevent us from creating an instance of this abstract class). The correct way to create an abstract method is to use the `@abstractmethod` decorator to create an abstract method.

        ```Python 
        class A:
            def foo():
                raise NotImplementedError

        class B(A):
            def foo():
                ... # some code here
        ```

        In the above example, class A is an abstract class because it has an abstract method foo().

#### Representation Invariant

Every attribute in a class needs to meet specific conditions

+ For regular variables and methods, we need to specify the type of the variable and the return value of the method

    ```Python
    class A:
        num: int
        name: str

        def foo(self, num: int, name: str) -> None:
            ...
    ```
+ For conditional variables, such as the length of a tweet not exceeding 280 characters, there are three ways to limit this condition
    + By limiting the precondition
        + When using this method, we assume that all inputs are correct, and the person using our method needs to confirm whether the conditions are met before inputting, for example:
        
        ```Python
        class Tweet:
            """
            === Representation Invariant ===
            content: len(content) <= 280
            """
            content: str

            def set_content(self, content: str) -> None:
                """
                Precondition: len(content) <= 280
                """
                self.content = content
        ```
    + If the input parameters do not meet the conditions, do nothing
        + This method is also called failing silently

        ```Python
        class Tweet:
            """
            === Representation Invariant ===
            content: len(content) <= 280
            """
            content: str

            def set_content(self, content: str) -> None:
                if len(content) <= 280:
                    self.content = content
        ```
    + Implicitly fix the problem within the method
        + When using this method, we do not impose any conditions on the input, but when processing the input, we repair the input that does not meet the conditions to meet the conditions (for example: using a qualified parameter to replace, deleting part of the input that does not meet the conditions, etc.)

        ```Python
        class Tweet:
            """
            === Representation Invariant ===
            content: len(content) <= 280
            """
            content: str

            def set_content(self, content: str) -> None:
                self.content = content[:280]
        ```

### Exception Handling

Exceptions are also objects, and the parent class of common exceptions is `Exception`. So, any class that inherits from the `Exception` class can be recognized by the system as an exception type.

+ Creating an exception object does not affect program execution, only when the exception object is thrown does it affect program execution.
    + Common ways to throw exceptions: `raise XXXXError`
        + Creating a custom error:

        ```Python 
        class MyError(Exception):
            """ This is an example error """
            pass
        ```

+ Assert statement (usually used in unit tests):
    + `assert expression, [msg]` If the value of the expression is `False`, an assertion exception is thrown.
        + Example: `assert 0 == 1, "error msg"` This line of code will raise `AssertionError: error msg`

#### Try Module

+ The try module is divided into four parts: `try`, `except`, `else`, and `finally`
    + `try`: Code that needs verification, when an error occurs here, it will not throw an error directly but will jump to the `except` section to run the code.
    + `except`: It is the error handling solution. One try module can have multiple except modules.
        + Its catch logic is: `isinstance(e, XXXError)`
        + From top to bottom, it captures, if any one is successful, the error is consumed
        + If all processing modules do not succeed in catching the error, the error will be thrown into the system
    + `else`, `finally` are not necessary
        + `else`: When no error is generated in the code block of `try`, the code here is executed
        + `finally`: Regardless of whether an exception is thrown in the `try` block, the code here will be executed.
    + Example:
        ```Python 
        try:
            # Code here that may throw an exception
        except ExceptionType1:
            # Code here will be executed when the code in the try block throws a specific type of exception
        except ExceptionType2:
            # Code here will be executed when the code in the try block throws a specific type of exception
        else:
            # If the code in the try block does not throw an exception, the code here will be executed
        finally:
            # This code will be executed regardless of whether the code in the try block throws an exception
        ```

### Abstract Data Types (ADT)

Abstract Data Types (ADTs) only define the functionality (actions) of the data structure but do not specify how to implement it.

+ For example, we can define a Stack ADT, which may include the following operations:
    + `push(item)`: Add an element to the top of the stack.
    + `pop()`: Remove and return the element at the top of the stack.
    + `peek()`: Return the element at the top of the stack without removing it.
    + `is_empty()`: Check if the stack is empty.

+ In Python, we can use classes to implement this ADT:
    ```Python 
    class Stack:
        def __init__(self):
            self.items = []

        def push(self, item):
            self.items.append(item)

        def pop(self):
            return self.items.pop()

        def peek(self):
            return self.items[-1]

        def is_empty(self):
            return not bool(self.items)
    ```
    Here we can understand that this stack is implemented using a list, and we also know that the optimal solution for a stack is to implement it using a binary tree. This is the concept of ADT; it only defines what operations exist in the data structure but does not specify how these operations are implemented.

### Stack and Queue

They are Abstract Data Types (ADTs)

#### Stack
A last-in, first-out (LIFO) data structure

+ Defined actions: `push(item)`, `pop()`, `is_empty()`
    + `push(item)`: Add an element to the top of the stack
    + `pop()`: Remove and return the element at the top of the stack
    + `is_empty()`: Check if the stack is empty

+ As of tt1, we have learned how to implement a stack using a regular list and a linked list.
    + Regular list time complexity:
        + `push(item)`: Best O(1); Worst O(n); Average O(1)
        + `pop()`: Best O(1); Worst O(1); Average O(1)
        + `is_empty()`: Best O(1); Worst O(1); Average O(1)
    + Linked list time complexity:
        + `push(item)`: Best O(1); Worst O(n); Average O(1)
        + `pop()`: Best O(1); Worst O(1); Average O(1)
        + `is_empty()`: Best O(1); Worst O(1); Average O(1)

#### Queue
A first-in, first-out (FIFO) data structure

+ Defined actions: `enqueue(item)`, `dequeue()`, `is_empty()`
    + `enqueue(item)`: Add an element to the end of the queue
    + `dequeue()`: Remove and return the element at the front of the queue
    + `is_empty()`: Check if the queue is empty

+ As of tt1, we have learned how to implement a queue using a regular list and a linked list.
    + Regular list time complexity:
        + `enqueue(item)`: Best O(1); Worst O(n); Average O(1)
        + `dequeue()`: Best O(1); Worst O(n); Average O(n)
        + `is_empty()`: Best O(1); Worst O(1); Average O(1)
    + Linked list time complexity:
        + `enqueue(item)`: Best O(1); Worst O(n); Average O(1)
        + `dequeue()`: Best O(1); Worst O(n); Average O(n) or O(1) (depending on the implementation of the linked list)
        + `is_empty()`: Best O(1); Worst O(1); Average O(1)

### Singly Linked List

A singly linked list is a one-dimensional list structure composed of a group of nodes.

#### Node
In Python, a node is a private class consisting of `item` and `next`.
```Python 
from __future__ import annotations
from typing

 import Any, Optional

class _Node:
    item: Any
    next: Optional[_Node]
```

#### Code for a Singly Linked List

```Python
class LinkedList:
    _first: Optional[_Node]
    
    def __init__(self):
        self._first = None
    
    def append(self, item: Any) -> None:
        if _first is None:
            self._first = None
            return
        curr = self._first
        while curr.next is not None:
            curr = curr.next
        curr.next = _Node(item)
    
    def __len__(self) -> int:
        counter = 0
        curr = self._first
        while curr is not None:
            counter += 1
            curr = curr.next
        return counter

    def __contains__(self, target: Any) -> bool:
        curr = self._first
        while curr is not None:
            if curr.item == target:
                return True
        return False
    
    def __eq__(self, other: LinkedList) -> bool:
        curr1 = self._first
        curr2 = other._first
        while curr1 is not None and curr2 is not None:
            if curr1.item != curr2.item:
                return False
            curr1 = curr1.next
            curr2 = curr2.next
        return curr1 == curr2

    def __getitem__(self, index: int) -> Any:
        curr = self._first
        i = 0
        while i < index:
            if curr None:
                raise IndexError
            curr = curr.next
            i += 1
        return curr.item
    
    def __setitem__(self, index: int, new_item: Any) -> None:
        if self._first None:
            return IndexError
        curr = self._first
        i = 0
        while i < index:
            if curr None:
                raise IndexError
            curr = curr.next
            i += 1
        curr.item = new_item
```


### Conclusion
Good luck to everyone on the exam! Best wishes to all the examiners for a smooth exam!!