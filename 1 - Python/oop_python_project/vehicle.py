class Vehicle:
    __numbers_of_vehicles = 0

    def __init__(self, name, capacity, supplier):
        self.name = name
        self.capacity = capacity
        self.supplier = supplier
        Vehicle.__numbers_of_vehicles += 1

    @classmethod
    def get_numbers_of_vehicles(cls):
        return cls.__numbers_of_vehicles

    def show(self):
        print("Name:", self.name)
        print("Capacity:", self.capacity)
        print("Supplier:", self.supplier)
        print("Vehicle Type:", self.__class__.__name__)


class Truck(Vehicle):
    __numbers_of_trucks = 0

    def __init__(self, name, capacity, supplier, truck_type, weight):
        super().__init__(name, capacity, supplier)
        self.truck_type = truck_type
        self.weight = weight
        Truck.__numbers_of_trucks += 1

    @classmethod
    def get_numbers_of_trucks(cls):
        return cls.__numbers_of_trucks

    def show(self):
        super().show()
        print("Truck Type:", self.truck_type)
        print("Weight:", self.weight)


class Bus(Vehicle):
    __numbers_of_buses = 0

    def __init__(self, name, capacity, supplier, person_capacity):
        super().__init__(name, capacity, supplier)
        self.person_capacity = person_capacity
        Bus.__numbers_of_buses += 1

    @classmethod
    def get_numbers_of_buses(cls):
        return cls.__numbers_of_buses

    def show(self):
        super().show()
        print("Person Capacity:", self.person_capacity)


vehicles = [
    Truck("Truck1", 1000, "Supplier1", "Heavy", 5000),
    Truck("Truck2", 2000, "Supplier2", "Light", 3000),
    Bus("Bus1", 50, "Supplier3", 30),
    Bus("Bus2", 60, "Supplier4", 40)
]

for vehicle in vehicles:
    vehicle.show()
    print()

print("Total Vehicles:", Vehicle.get_numbers_of_vehicles())
print("Total Trucks:", Truck.get_numbers_of_trucks())
print("Total Buses:", Bus.get_numbers_of_buses())
