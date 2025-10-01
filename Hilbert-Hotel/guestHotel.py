from typing import List
from functools import reduce

class GuestTravel:
    deleted_guest = set()
    deleted_room = set()
    manually_added_guest = {}
    def __init__(self, first_guest_index: int, travel : List[int]):
        self.last_guest_index = first_guest_index
        self.travel = travel
        self.shift = 0
        self.guest_count = reduce(lambda x, y: x * y, travel) + first_guest_index

    def Shift(self, n):
        self.shift += n

    def room_index(self, guest_id):
        return guest_id + self.shift
    
    def last_guest(self):
        return self.last_guest

    def print_index(self):
        guests_data = []
        if len(self.travel) == 4:
            for m in range(self.travel[0]):
                offset_a = m * self.travel[1] * self.travel[2] * self.travel[3]
                for l in range(self.travel[1]):
                    offset_b = offset_a + l * self.travel[2] * self.travel[3]
                    for k in range(self.travel[2]):
                        offset_c = offset_b + k * self.travel[3]
                        for j in range(self.travel[3]):
                            offset_d = offset_c + j
                            for i in range(1):
                                guest_id = i + offset_d
                                room_index = self.room_index(guest_id)
                                if guest_id not in GuestTravel.deleted_guest and room_index not in self.deleted_room:
                                    final_guest_id = guest_id + self.last_guest_index
                                    guests_data.append((final_guest_id, room_index))
        for guest_id, room_num in guests_data:
            print(f"  Guest #{guest_id:<10} → Room {room_num:>6}")
        return len(guests_data)