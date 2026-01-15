"""
Narudee Chakitdee
673040147-9
Lab4 P1
"""

from abc import ABC, abstractmethod

class Room(ABC):
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    @abstractmethod
    def get_purpose(self):
        """Returns a string describing purposes of the room"""
        pass

    @abstractmethod
    def get_recommended_lighting(self):
        """Returns recommended lighting in lumens per square foot"""
        pass

    def calculate_area(self):
        return self.length * self.width
    
    def describe_room(self):
        area = self.calculate_area()
        return f"A {self.__class__.__name__} of {area} sq ft used for {self.get_purpose()}"

class Bedroom(Room):
    def __init__(self, length, width, bed_size):
        super().__init__(length, width)
        self.bed_size = bed_size

    def get_purpose(self):
        return "Sleeping time is coming ja"
    
    def get_recommended_lighting(self):
        return 10


class Kitchen(Room) :
    def __init__(self, length, width, has_island = True):
        super().__init__(length, width)
        self.has_island = has_island

    def get_purpose(self):
        return "Cooking mama"
    
    def get_recommended_lighting(self):
        return 70
    
    def calculate_counter_space(self):
        """
        Calculates the area of island counter and the wall counter.
        Base on check about it has an island or not.

        Return :
            tuple: A tuple containing:
                - island_counter (float): The area of the island counter.
                - wall_counter (float): The area of the wall counter.

        Examples :
            >>> kitchen = Kitchen(10, 20, has_island=True)
            >>> kitchen.calculate_counter_space()
            (40.0, 50.0)
        """
        area = self.calculate_area()

        if self.has_island:
            island_counter = area / 5
            wall_counter = area / 4
        else:
            island_counter = 0
            wall_counter = area / 2
        return island_counter, wall_counter