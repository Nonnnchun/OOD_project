from typing import List

class GuestTravel:
    def __init__(self, group_id: int, buses: List[int]):
        self.group_id = group_id
        self.buses = buses  
        self.total_guests = sum(buses)  
        self.bus_start_indices = []
        cumulative = 0
        for capacity in buses:
            self.bus_start_indices.append(cumulative)
            cumulative += capacity

    def cantor_pair(self, a: int, b: int) -> int:
        return ((a + b) * (a + b + 1)) // 2 + b

    def triple_pair(self, a: int, b: int, c: int) -> int:
        return self.cantor_pair(self.cantor_pair(a, b), c)
    
    def get_bus_and_seat(self, guest_index: int) -> tuple:
        for bus_num in range(len(self.buses)):
            bus_start = self.bus_start_indices[bus_num]
            bus_end = bus_start + self.buses[bus_num]
            
            if bus_start <= guest_index < bus_end:
                seat_number = guest_index - bus_start + 1  
                return (bus_num + 1, seat_number)  
        return (0, 0)  

    def get_room_number(self, guest_index: int) -> int:
        bus_num, seat_num = self.get_bus_and_seat(guest_index)
        room = self.triple_pair(self.group_id, bus_num, seat_num)
        return room

    def get_guest_id(self, guest_index: int) -> int:
        return guest_index