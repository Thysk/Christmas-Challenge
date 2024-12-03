import timeit
from random import randrange
from collections import Counter
from multiprocessing import Pool, cpu_count
from concurrent.futures import ProcessPoolExecutor as PPE
from concurrent.futures import as_completed


class ChristmasHamper:

    def __init__(self, varieties:int, count: int):
        self.hamper: list = self._populate_hamper(varieties,count)
        self.action_count: int = 0

    def __str__(self) -> str:
        return f"In the Hamper: {str(self.hamper)}\nAction Count: {self.action_count}"
    
    def __len__(self) -> int:
        return len(self.hamper)
    
    def contents(self) -> list:
        return self.hamper

    def _populate_hamper(self,varieties: int,count: int) -> list:
        """
        Takes the initialisation varieties and count and populates the hamper list with alphabetical items
        """
        _hamper = []
        variety_label = "A"
        for _ in range(varieties):
            for _ in range(count):
                _hamper.append(variety_label)
            variety_label = bytes(variety_label, "utf-8")
            variety_label = str(bytes([variety_label[0] + 1]))[2]
        return _hamper

    def hamper_tracker(self) -> None:
        print(self.hamper)

    def take_item(self,index: int) -> str:
        self.action_count += 1
        return self.hamper.pop(index)
    
    def return_item(self, item: str) -> None:
        self.hamper.append(item)

    def return_action_count(self):
        return self.action_count


class Hands:
    def __init__(self, varieties, count):
        self.hamper = ChristmasHamper(varieties=varieties,count=count)
        self.picking_hand = []
        self.holding_hand = []
        self.last_consumed = ""


    def __str__(self) -> str:
        return f"In the Hand:   {str(self.holding_hand)}\n"
    
    def whats_in_the_hand(self) -> list:
        return self.holding_hand
    
    def pick_up_random_item(self) -> None:
        hamper_size = len(self.hamper.contents())
        self.picking_hand.append(self.hamper.take_item(randrange(0,hamper_size)))
    
    def hold_item(self) -> None:
        self.holding_hand.append(self.picking_hand.pop())

    
    def hamper_binge(self):
        self.phase_1()
        self.phase_2()
        return self.hamper.return_action_count()

    def return_item(self, item) -> None:
        self.hamper.return_item(self.picking_hand.pop())

    def return_items(self) -> None:
        while len(self.holding_hand) > 0:
            self.hamper.return_item(self.holding_hand.pop())

    def status_report(self):
        print(
            f"""
            In hamper:       {self.hamper.contents()}
            In picking hand: {self.picking_hand}
            In holding hand: {self.holding_hand}
            Actions:         {self.hamper.return_action_count()}
            Last consumed:   {self.last_consumed}
            """
        )

    def check_for_duplicates(self) -> bool:
        if self.holding_hand and self.picking_hand:
            if self.picking_hand[0] in self.holding_hand:
                return True
            else:
                return False
        return False
        
    def try_to_consume(self):
        if self.picking_hand[0] == self.last_consumed:
            self.hold_item()
        else:
            self.last_consumed = self.picking_hand[0]
            self.picking_hand.clear()
            self.return_items()



    def max_count_of_items(self, location):
        return max(list(Counter(location).values()))

    def phase_1(self):
        """
        Take items out of the hamper until you are holding 2 of the same, 
        if they do not match the previously consumed item, consume, 
        if they do, continue taking items
        """

        while  self.max_count_of_items(self.hamper.contents()) > 1:
            self.pick_up_random_item()
            if self.check_for_duplicates():
                self.try_to_consume()
            else:
                self.hold_item()

    def phase_2(self):
        """
        Take items out of the hamper until there is one that was not consumed last, 
        consume it and return the rest
        """
        while len(self.hamper.contents()) > 0:
            self.pick_up_random_item()
            self.try_to_consume()

def christmas_hamper_simulator(varieties: int, count: int) -> list:
    hand = Hands(varieties=varieties, count=count)
    return hand.hamper_binge()



if __name__ == "__main__":
    repeats = 300000
    varieties = 10
    count = 2
    results = []

    start = timeit.default_timer()

    for _ in range(repeats):
        results.append(christmas_hamper_simulator(varieties=varieties, count=count))

    end = timeit.default_timer()
    minimum = (min(results))
    maximum = (max(results))
    print(f"Took {end-start} seconds for {repeats} repeats to find the min ({minimum}) and max ({maximum}) of {varieties} varieties and {count} of each")