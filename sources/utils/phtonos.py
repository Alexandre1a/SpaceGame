# The money manager, named after the Greek god of greed.

class Phtonos:
    def __init__(self) -> None:
        pass

    def add(self, target, amount) -> int:
        target.amount += amount
        return amount

    def remove(self, target, amount) -> int:
        target.amount -= amount
        return amount

    def transfer(self, source, destination, amount) -> int:
        self.add(destination, (self.remove(source, amount)))
        return amount

class Account:
    def __init__(self) -> None:
        self.amount = 0
