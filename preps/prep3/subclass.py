class Printer:
    """A Printer.

    === Attributes ===
    message: the message to print
    """
    message: str

    def __init__(self, message: str) -> None:
        print("ss")
        self.message = message

    def print_message(self):
        """Prints a message.
        """
        print(self.message)


class MysteryPrinter(Printer):
    def __init__(self, message: str) -> None:
        Printer.__init__(self, message + message)


class DoublePrinter(MysteryPrinter):
    def print_message(self):
        print(self.message + self.message)


if __name__ == '__main__':
    # m1 = Printer('hello')
    # m2 = MysteryPrinter('good')
    m3 = DoublePrinter('bye')
    # m1.print_message()
    # m2.print_message()
    m3.print_message()