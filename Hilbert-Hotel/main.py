from Hotel import Hotel
import tracemalloc

def print_menu():
   print("\n" + "=" * 60)
   print("🏨  HOTEL MANAGEMENT SYSTEM".center(60))
   print("=" * 60)
   print("  1. ➕ Add guest group")
   print("  2. 👤 Add room and people manually")
   print("  3. 📋 Print sorted room list")
   print("  4. 🔍 Search room")
   print("  5. 🗑️  Remove room")
   print("  6. ⏱️  Print all code runtime")
   print("  7. 🏪 Print memory usage")
   print("  8. 💾 Save to file")
   print("  x. 🚪 Exit")
   print("=" * 60)

def main():
   control = True
   hotel = Hotel()
   tracemalloc.start()

   print("\n" + "=" * 60)
   print("🏨  Welcome to Hotel Management System".center(60))
   print("=" * 60)
   print("\n📝 Please enter initial guest configuration")
   print("   (Format: 4 numbers separated by spaces)")
   print("   Example: 2 3 4 5")
   print("-" * 60)

   INPUT_INITIAL = True
   while INPUT_INITIAL:
      try:
         initial_guest = list(map(int, input("➤  Initial guest: ").split()))

         if any(i <= 0 for i in initial_guest):
            print("❌ Error Input! All numbers must be positive.")
            continue

         INPUT_INITIAL = False
      except ValueError:
         print("❌ Invalid input! Please enter only numbers separated by spaces.")

   hotel.add_guest(initial_guest)

   while control:
      print_menu()
      opt = input("\n➤  Select option: ").strip()
      print()

      if opt == '1':
         print("📝 Enter guest configuration ")
         print("   Example: 2 3 4 5")
         try:
            inp_ppl = list(map(int, input("➤  Guest configuration: ").split()))
            if any(i <= 0 for i in inp_ppl):
               print("❌ Error Input! All numbers must be positive.")
               continue
            hotel.code_runtime(hotel.add_guest, inp_ppl)
         except ValueError:
            print("❌ Invalid input! Please enter only numbers separated by spaces.")
            
      elif opt == '2':
            try:
               inp_mul = int(input("➤  Enter room number: "))
               if inp_mul <= 0:
                  print("❌ Room number must be a positive integer.")
                  continue
               hotel.code_runtime(hotel.manual_add_guest, inp_mul)
            except ValueError:
               print("❌ Invalid input! Please enter a valid number.")

      elif opt == '3':
         hotel.code_runtime(hotel.print_sorted_room)

      elif opt == '4':
         # # debugging
         # for i in range(hotel.guestHotel[-1].guest_count):
         #    hotel.search_room(i)
         try:
            search_room = int(input("➤  Enter room number to search: "))
            hotel.code_runtime(hotel.search_room, search_room)
         except:
            print()
            print("❌ Invalid Input".center(20))

      elif opt == '5':
         guest_number = int(input("➤  Enter room number to remove: "))
         try:
            hotel.code_runtime(hotel.remove_room, guest_number)
         except:
            print()
            print("❌ Invalid Input".center(20))

      elif opt == '6':
         hotel.print_total_runtime()

      elif opt == '7':
         hotel.memory_used()

      elif opt == '8':
         filename = input("➤  Enter filename (default: hotel_rooms): ").strip()
         if not filename:
               filename = "hotel_rooms"
         hotel.code_runtime(hotel.save_to_file, filename)

      elif opt == 'x' or opt == 'X':
         print("\n" + "=" * 60)
         print("👋  Thank you for using Hotel Management System!".center(60))
         print("=" * 60 + "\n")
         control = False

      else:
         print("❌ Invalid selection! Please try again.")

   tracemalloc.stop()

if __name__ == "__main__":
   main()