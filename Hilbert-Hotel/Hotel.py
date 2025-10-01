# from HashMap import HashMap
# import time
# from main import start_time
# import tracemalloc
from guestHotel import GuestTravel
import math
from functools import reduce



def printHotel():
   for i in GuestTravel.manually_added:
      if(hilbert.guestHotel[-1].guest_count>=i):
         GuestTravel.manually_added.remove(i)
         
   for i in hilbert.guestHotel:
      print("guest, room")
      i.print_index()
      print(i.shift)
   
   print(*GuestTravel.manually_added)

class Hotel:
   def __init__(self, guestHotel:list =[]):
      self.guestHotel = []

   def remove_guest(self, guest_id: int):
      if guest_id in GuestTravel.deleted_guest:
         print("Delete หาแม่มึงหรอ")
      GuestTravel.deleted_guest.add(guest_id)

   def add_room(self,room_num):
         if(self.guestHotel[-1].guest_count>=room_num or room_num in GuestTravel.manually_added): 
            print("Already Exist")
         else:
            GuestTravel.manually_added.append(room_num)
            print(f"Added Room {room_num}")
   
   def shift_All(self,shift_value:int):
      # print(f"KUY {GuestTravel.deleted_guest}")
      GuestTravel.deleted_guest = set(map(lambda x : x + shift_value, GuestTravel.deleted_guest))
      # print(f"KUY {GuestTravel.deleted_guest}")
      for guest in self.guestHotel:
         guest.Shift(shift_value)

   def add_guest(self,guest:list[int]):
      if(len(self.guestHotel)==0):
         self.guestHotel.append(GuestTravel(0,guest))
      else:
         self.shift_All(reduce(lambda x, y: x + y, guest))
         self.guestHotel.append(GuestTravel(self.guestHotel[-1].guest_count,guest))

   def sort_room():
      pass

   def find_path(self,room_num,travel):
      if(travel[0]!=1):  
         quay = math.ceil((room_num/(travel[1]*travel[2]*travel[3])))
         quay_seat = room_num %(travel[1]*travel[2]*travel[3])
         boat = math.ceil(quay_seat/(travel[2]*travel[3]))
         boat_seat = quay_seat % (travel[2]*travel[3])
         bus = math.ceil(boat_seat/travel[3])
         bus_seat = boat_seat % travel[3]
         return quay,boat,bus,bus_seat+1
      elif(travel[1]!=1):
         quay_seat = 1 
         boat = math.ceil(room_num/(travel[2]*travel[3]))
         boat_seat = room_num % (travel[2]*travel[3])
         bus = math.ceil(boat_seat/travel[3])
         bus_seat = boat_seat % travel[3]
         return 1,boat,bus,bus_seat+1
      elif(travel[2]!=1):
         bus = math.ceil(room_num/travel[3])
         bus_seat = room_num % travel[3]
         return 1,1,bus,bus_seat+1
      elif(travel[3]!=1):
         return 1,1,1,room_num+1

   def find_insert(self, target: int) -> int:
      if not self.guestHotel:
         return 0
      lo, hi = 0, len(self.guestHotel) - 1
      while lo <= hi:
         mid = (lo + hi) // 2
         mid_val = self.guestHotel[mid].shift
         seed_range = self.guestHotel[mid].guest_count - self.guestHotel[mid].last_guest_index
         if mid_val < target <seed_range + mid_val:
            return mid
         if mid_val > target:
            lo = mid + 1
         elif mid_val < target:
            hi = mid - 1
         else:
            return mid

   def search_room(self,room_num):
      idx = (self.find_insert(room_num))
      detial = self.find_path(room_num-self.guestHotel[idx].shift,self.guestHotel[idx].travel)
      print((room_num-self.guestHotel[idx].shift)+self.guestHotel[idx].last_guest_index,end=" ")
      print(detial[0],detial[1],detial[2],detial[3])


   def code_runtime():
      pass

   def memory_used():
      pass

   def save_to_file():
      pass

   print("1. add guest")
   print("2. add guest to room manually")
   print("3. print sorted room")
   print("4. print empty room")
   print("5. search room")
   print("6. remove room")
   print("7. print all runtime of code")
   print("8. print memory used")
   print("9. save to file")

hilbert = Hotel()
hilbert.add_guest((1,10))
hilbert.remove_guest(5)
hilbert.remove_guest(5)
print(f"KUY {GuestTravel.deleted_guest}")
hilbert.add_guest((1,1,1,10))
hilbert.add_room(40)
hilbert.add_room(40)
hilbert.add_guest((1,1,1,60))
print(f"KUY {GuestTravel.deleted_guest}")
printHotel()

# hilbert.guestHotel[0].print_index()
# print("addnew_ppl")
# print(hilbert.guestHotel[0].shift)
# hilbert.guestHotel[1].print_index()
# print("addnew_ppl2")
# print(hilbert.guestHotel[1].shift)
# hilbert.guestHotel[2].print_index()
# print(hilbert.guestHotel[2].shift)
