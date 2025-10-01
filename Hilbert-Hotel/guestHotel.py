from typing import List
from functools import reduce


class GuestTravel:
    deleted_guest = set()
    manually_added_guest = {}
    def __init__(self, first_guest_index: int, travel : List[int]):
        self.last_guest_index = first_guest_index
        self.travel = travel
        self.shift = 0
        self.guest_count = reduce(lambda x, y: x + y, travel) +first_guest_index
        

    def Shift(self, n):
        self.shift += n

    def room_index(self, guest_id):
        return guest_id + self.shift
    
    def last_guest(self):
        return self.last_guest

    def print_index(self):
        main_path = []
        print(len(self.travel))
        if len(self.travel) == 0:
            for i in range(1):
                guest_id = i
                room_index = self.room_index(guest_id)
                if room_index not in GuestTravel.deleted_guest:
                    print(guest_id+self.last_guest_index, self.room_index(guest_id))
        elif len(self.travel) == 1:
            for j in range(self.travel[0]):
                offset =  j
                for i in range(self.guest_count):
                    guest_id = i + offset
                    room_index = self.room_index(guest_id)
                    if room_index not in GuestTravel.deleted_guest:
                        print(guest_id+self.last_guest_index, self.room_index(guest_id))
        elif len(self.travel) == 2:
            for k in range(self.travel[0]):
                offset_a = k * self.travel[1] 
                for j in range(self.travel[1]):
                    offset_b = offset_a + (j)
                    # print(f"egwgwwg{offset_b}")
                    for i in range(1):
                        guest_id = i+offset_b
                        room_index = self.room_index(guest_id)
                        if room_index not in GuestTravel.deleted_guest:
                            print(guest_id+self.last_guest_index, self.room_index(guest_id))
        elif len(self.travel) == 3:
            for l in range(self.travel[0]):
                offset_a = l*self.travel[1]*self.travel[2]
                for k in range(self.travel[1]):
                    offset_b = offset_a + k*self.travel[2]
                    for j in range(self.travel[2]):
                        offset_c = offset_b + j
                        for i in range(1):
                            guest_id = i+ offset_c
                            room_index = self.room_index(guest_id)
                            if room_index not in GuestTravel.deleted_guest:
                                print(guest_id+self.last_guest_index, self.room_index(guest_id))
        elif len(self.travel) == 4:
            for m in range(self.travel[0]):
                offset_a = m*self.travel[1]*self.travel[2] * self.travel[3]
                for l in range(self.travel[1]):
                    offset_b = offset_a + l*self.travel[2]*self.travel[3]
                    for k in range(self.travel[2]):
                        offset_c = offset_b + k*self.travel[3]
                        for j in range(self.travel[3]):
                            offset_d = offset_c + j
                            for i in range(1):
                                guest_id = i+offset_d
                                room_index = self.room_index(guest_id)
                                if room_index not in GuestTravel.deleted_guest:
                                    print(guest_id+self.last_guest_index, self.room_index(guest_id))

# hotel = [GuestTravel(0,(1,1,1,100))]


# hotel.append(GuestTravel(100, (1,1,1,80)))
# hotel[0].Shift(80)
# hotel.append(GuestTravel(0, (1,1,1,50)))
# hotel[0].Shift(50)
# hotel[1].Shift(50)

# # print(hotel[0])
# # hotel[0].Shift(80)
# # hotel.append(GuestTravel(180, 1, ([1,1,20,30])))
# # hotel[0].Shift(20)
# # hotel[1].Shift(600)


# hotel[0].print_index()
# print("----------------------------------------")
# hotel[1].print_index()
# print("----------------------------------------")
# hotel[2].print_index()