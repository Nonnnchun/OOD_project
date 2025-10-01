from Hotel import Hotel

control = True

hotel = Hotel()
initial_guest = list(map(int, (input("Add initial guest:").split())))
hotel.add_guest(initial_guest)

while (control) :
   print("============================================")
   print("MENU: ")
   print("1. Add guest")
   print("2. Add room and people manually")
   print("3. Print sorted room")
   print("4. Search room")
   print("5. Remove room")
   print("6. Print all code runtime")
   print("7. Print memory used")
   print("8. Save to file")
   print("x. exit..")

   opt = input("Option: ")
   if opt == '1' :
      inp_ppl = list(map(int, (input("Add people to the room: ").split())))
      hotel.add_guest(inp_ppl)

   elif opt == '2' :
      hotel.manual_add_guest(int(input("Add room manually: ")))

   elif opt == '3' :
      hotel.print_sorted_room()

   elif opt == '4' :
      hotel.search_room(int(input("Search room : ")))

   elif opt == '5' :
      room_number = int(input("room number : "))
      hotel.remove_room(room_number)

   elif opt == '6' :
      print("print all runtime of code:", hotel.code_runtime())

   elif opt == '7' :
      print(hotel.memory_used())

   elif opt == '8' :
      hotel.save_to_file("./hotel_rooms.csv")

   elif opt == 'x' :
      control = False

   else :
      print("selection invalid!")