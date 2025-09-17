from HashMap import HashMap
from Hotel import Hotel

hotel = Hotel()
initial_guest = int(input("Initial Guest: "))
for i in range(initial_guest):
   # hotel.add_room(x,x,x,x)
   pass
print(hotel.table)
while (True) :
   print("============================================")
   print("MENU: ")
   print("1. add guest")
   print("2. add guest to room manually")
   print("3. print sorted room")
   print("4. print empty room")
   print("5. search room")
   print("6. remove room")
   print("7. print all runtime of code")
   print("8. print memory used")
   print("9. save to file")
   print("x. exit..")

   opt = input("Option: ")
   if opt == '1' :
      print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
      print("1.  add n guest")
      print("2.  add n guest on m bus")
      print("3.  add n guest on m bus on l ship")
      print("4.  add n guest on m bus on l ship in k fleet")
      opt = input("select: ")
      if opt == "1" :
         print("add n guest")
         n = int(input("n = "))
         for a in range(n) : hotel.add_room(0, 0, 0, a)
      elif opt == "2" :
         print("add n guest on m bus")
         n = int(input("n = "))
         m = int(input("m = "))
         for b in range(m) :
               for a in range(n) : hotel.add_room(0, 0, b, a)
      elif opt == "3" :
         print("add n guest on m bus on l ship")
         n = int(input("n = "))
         m = int(input("m = "))
         l = int(input("l = "))
         for c in range(l) :
               for b in range(m) :
                  for a in range(n) : hotel.add_room(0, c, b, a)
      elif opt == "4" :
         print("add n guest on m bus on l ship in k fleet")
         n = int(input("n = "))
         m = int(input("m = "))
         l = int(input("l = "))
         k = int(input("k = "))
         for d in range(k) :
               for c in range(l) :
                  for b in range(m) :
                     for a in range(n) : hotel.add_room(d, c, b, a)

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
      print("print all runtime of code:", hotel.())
   elif opt == '8' :
      print("print memory used:", hotel.())
   elif opt == '9' :
      hotel.save_to_file("./hotel_rooms.csv")
   elif opt == 'x' :
      break
   else :
      print("selection invalid!")