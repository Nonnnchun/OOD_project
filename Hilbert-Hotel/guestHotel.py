from typing import List
from functools import reduce

class GuestTravel:
    deleted_room = []
    manually_added_guest = {}
    manually_added_guest_deleted = []
    add_deleted = set()
    def __init__(self, first_guest_index: int, travel: List[int]):
        self.last_guest_index = first_guest_index
        self.travel = travel
        self.shift = 0
        self.guest_count = reduce(lambda x, y: x * y, travel) + first_guest_index

    def Shift(self, n):
        self.shift += n

    def room_index(self, guest_id):
        return guest_id + self.shift

    def last_guest(self):
        return self.last_guest_index

    def print_index(self):
        guests_data = []
        total_guests = reduce(lambda x, y: x * y, self.travel)
        for guest_id in range(total_guests):
            room_index = self.room_index(guest_id)
            if room_index not in self.deleted_room:
                final_guest_id = guest_id + self.last_guest_index
                print(f"  Guest #{final_guest_id:<10} → Room {room_index:>6}")
            if(room_index in self.manually_added_guest_deleted):
                res = dict((v,k) for k,v in self.manually_added_guest.items())
                print(f"  Guest #{res[room_index]:<10} → Room {room_index:>6}")
        return len(guests_data)