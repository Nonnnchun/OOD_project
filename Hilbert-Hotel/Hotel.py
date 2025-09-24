# from HashMap import HashMap
# import time
# from main import start_time
# import tracemalloc
from guestHotel import GuestTravel
import math



class Hotel:
   def __init__(self, guestHotel:list =[]):
      self.guestHotel = []

   def shift_All(self,shift_value):
      for guest in self.guestHotel:
         guest.Shift(shift_value)

   def add_guest(self,guest:list[int]):
      if(len(self.guestHotel)==0):
         self.guestHotel.append(GuestTravel(0,guest))
      else:
         self.shift_All(guest[0]*guest[1]*guest[2]*guest[3])
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
      print(self.find_insert(room_num))
      detial = self.find_path(room_num-self.guestHotel[1].shift,self.guestHotel[1].travel)
      print((room_num-self.guestHotel[1].shift)+self.guestHotel[1].last_guest_index,end=" ")
      print(detial[0],detial[1],detial[2],detial[3])

   def remove_room():
      pass

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
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))
hilbert.add_guest((1,1,1,10))
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))
hilbert.add_guest((1,1,1,10))
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))
hilbert.add_guest((1,1,1,10))
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))
hilbert.add_guest((1,1,1,10))
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))
hilbert.add_guest((1,1,1,10))
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))
hilbert.add_guest((1,1,1,10))
hilbert.add_guest((1,1,1,20))
hilbert.add_guest((1,1,1,30))

for i in hilbert.guestHotel:
   print("guest, room")
   i.print_index()
   print("addnew_ppl")
   print(i.shift)

# hilbert.guestHotel[0].print_index()
# print("addnew_ppl")
# print(hilbert.guestHotel[0].shift)
# hilbert.guestHotel[1].print_index()
# print("addnew_ppl2")
# print(hilbert.guestHotel[1].shift)
# hilbert.guestHotel[2].print_index()
# print(hilbert.guestHotel[2].shift)
hilbert.search_room(389)
hilbert.find_insert(389)