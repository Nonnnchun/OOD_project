from HashMap import HashMap
from Hotel import Hotel
import time
import tracemalloc

all_mem = 0
all_size = 0
start_time = time.perf_counter()
tracemalloc.start()
hotel = Hotel()
initial_guest = int(input("Initial Guest: "))
for i in range(initial_guest):
   # hotel.add_room(x,x,x,x)
   pass
print("runtime:", hotel.code_runtime())
while (True) :
   print("============================================")
   print("MENU: ")
   print("1. add guest")
   print("2. add guest to room manually")
   print("6. remove room")
   print("3. print sorted room")
   print("5. search room")
   # print("4. print empty room") --> ไม่ต้อง
   print("7. print all runtime of code")
   print("8. print memory used")
   print("9. save to file")
   print("x. exit..")

   opt = input("Option: ")
   if opt == '1' :
      # add ppl
      pass

   elif opt == '2' :
      print("add guest to room manually:", ())
   elif opt == '3' :
      print("Sorted Rooms:", hotel.sort_rooms())
   elif opt == '4' :
      print("Empty Rooms:", hotel.empty_rooms())
   elif opt == '5' :
      room_number = int(input("room number : "))
      print("Search room",room_number,":", ())
   elif opt == '6' :
      room_number = int(input("room number : "))
      hotel.remove_room(room_number)
   elif opt == '7' :
      print("print all runtime of code:", hotel.code_runtime())
   elif opt == '8' :
      print(hotel.memory_used(all_mem, all_size))
   elif opt == '9' :
      hotel.save_to_file("./hotel_rooms.csv")
   elif opt == 'x' :
      break
   else :
      print("selection invalid!")