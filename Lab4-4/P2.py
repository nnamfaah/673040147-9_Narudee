"""
Narudee Chakitdee
673040147-9
Lab4 P2
"""

from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, make, model, year):
        """
        Initialize a Vehicle with make, model, and year.
        
        Args:
            make (str): The manufacturer of the vehicle
            model (str): The model of the vehicle
            year (int): The year of manufacture
            is_running (boolean) default to False
        """
        if not make or not model:
            raise ValueError("Make or Model must be Non-Empty String.")
        if year <= 0:
            raise ValueError("Year must be Positive integer.")
        
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    @abstractmethod
    def start_engine(self):
        """Abstract method to start the vehicle engine."""
        pass
    
    @abstractmethod
    def stop_engine(self):
        """Abstract method to stop the vehicle engine."""
        pass
    
    def get_info(self) -> str: # concrete methods
        return f"Vehicle's year as {self.year}, make with {self.make}, and model by {self.model}."

class CommercialVehicle(Vehicle):
    """
    Represents a commercial vehicle capable of carrying cargo.
    """
    def __init__(self, make, model, year, license_number: str, max_load: float):
        super().__init__(make, model, year)
        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0

    def start_engine(self): # Start the commercial vehicle engine.
        self.is_running = True
        return f"Commercial vehicle engine started !-!"
    
    def stop_engine(self): # Stop the commercial vehicle engine.
        self.is_running = False
        return f"Commercial vehicle engine stopped > <"
    
    def load_cargo(self, weight: float) -> bool:
        if weight <= 0:
            raise ValueError("Weight must be Positive.")
        
        if self.current_load + weight <= self.max_load:
            self.current_load += weight
            return True
        return False
    
    def unload_cargo(self, weight: float) -> float:
        if weight < 0 or weight > self.current_load:
            self.current_load = 0
        else:
            self.current_load -= weight
        return self.current_load


class Car(Vehicle):
    """
    Represents a passenger car.
    """
    def __init__(self, make, model, year, num_doors):
        super().__init__(make, model, year)
        if num_doors <= 0:
            raise ValueError("doors must be Positive.")
        self.num_doors = num_doors
    
    def start_engine(self):
        self.is_running = True
        return f"{self.make} {self.model} engine started !-!"
    
    def stop_engine(self):
        self.is_running = False
        return f"{self.make} {self.model} engine stopped > <"


class Trailer(CommercialVehicle):
    """
    Represents a trailer used for hauling cargo.
    """
    def __init__(self, make, model, year, license_number, max_load, num_axles: int = 2):
        super().__init__(make, model, year, license_number, max_load)
        if num_axles <= 0:
            raise ValueError("Number of axles must be Positive.")
        self.num_axles = num_axles
    
    def get_weight_per_axle(self):
        if self.num_axles == 0:
            return 0
        return self.current_load / self.num_axles


class DeliveryVan(Car, CommercialVehicle):
    def __init__(self, make, model, year, num_doors, license_number, max_load):
        Vehicle.__init__(self, make, model, year)
        self.num_doors = num_doors
        self.license_number = license_number
        self.max_load = max_load
        self.current_load = 0
        self.delivery_mode = False
    
    def toggle_delivery_mode(self) -> str:
        self.delivery_mode = not self.delivery_mode
        return f"Delivery mode: {'ON' if self.delivery_mode else 'OFF'}"
    
    def begin_service(self):
        print("Starting Delivery at your service :) ")
        print(self.get_info())

        print("Loading Cargo.....")
        self.load_cargo(50)

        print(self.start_engine())
        print(self.toggle_delivery_mode())
        print(self.stop_engine())
        
        print(f"Unloading... Remaining: {self.unload_cargo(50)} kg")
        
        print(self.toggle_delivery_mode())
        print("Delivery Service completely !")

    def get_info(self) -> str:
        return (
            f"{self.year} {self.make} {self.model}"
            f"\n Doors: {self.num_doors}"
            f"\n License: {self.license_number}"
            f"\n Load: {self.current_load} / {self.max_load}"
        )

if __name__ == "__main__":
    print("--- Testing Car ---")
    car = Car("Toyota", "Corolla", 2022, 4)
    print(car.start_engine())
    print(car.stop_engine())
    print(car.get_info())
    
    print("\n --- Testing Trailer ---")
    trailer = Trailer("Volvo", "XT", 2021, "TRL123", 1000, 4)
    trailer.load_cargo(400)
    print("Weight per axle:", trailer.get_weight_per_axle())
    
    print("\n --- Testing Delivery Van ---")
    van = DeliveryVan("Ford", "Transit", 2023, 4, "VAN999", 500)
    van.begin_service()