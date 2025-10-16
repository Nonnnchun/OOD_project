from Hotel_cantor import Hotel
import tracemalloc

def print_menu():
    print("\n" + "=" * 60)
    print("🏨  HOTEL MANAGEMENT SYSTEM".center(60))
    print("=" * 60)
    print("  1. ➕ Add guest group (buses)")
    print("  2. 👤 Add room manually")
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
    print("\n📝 Please enter initial bus configuration")
    print("   Format: number/number/number (e.g., 10/9/8/7)")
    print("   This means: Bus 1 has 10 people, Bus 2 has 9 people, etc.")
    print("-" * 60)

    INPUT_INITIAL = True
    while INPUT_INITIAL:
        try:
            bus_input = input("➤  Bus configuration: ").strip()
            initial_buses = hotel.parse_bus_input(bus_input)

            if any(i <= 0 for i in initial_buses):
                print("❌ Error! All bus capacities must be positive.")
                continue

            INPUT_INITIAL = Falsez
        except ValueError:
            print("❌ Invalid input! Please use format: 10/9/8/7")

    hotel.add_guest(initial_buses)

    while control:
        print_menu()
        opt = input("\n➤  Select option: ").strip()
        print()

        if opt == '1':
            print("📝 Enter bus configuration")
            print("   Format: number/number/number (e.g., 10/9/8/7)")
            try:
                bus_input = input("➤  Bus configuration: ").strip()
                new_buses = hotel.parse_bus_input(bus_input)
                
                if any(i <= 0 for i in new_buses):
                    print("❌ Error! All bus capacities must be positive.")
                    continue
                
                hotel.code_runtime(hotel.add_guest, new_buses)
            except ValueError:
                print("❌ Invalid input! Please use format: 10/9/8/7")
            
        elif opt == '2':
            try:
                inp_mul = int(input("➤  Enter room number: "))
                if inp_mul < 0:
                    print("❌ Room number must be a non-negative integer.")
                    continue
                hotel.code_runtime(hotel.manual_add_guest, inp_mul)
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")

        elif opt == '3':
            hotel.code_runtime(hotel.print_sorted_room)

        elif opt == '4':
            try:
                search_room = int(input("➤  Enter room number to search: "))
                hotel.code_runtime(hotel.search_room, search_room)
            except ValueError:
                print("❌ Invalid Input")

        elif opt == '5':
            try:
                guest_number = int(input("➤  Enter room number to remove: "))
                hotel.code_runtime(hotel.remove_room, guest_number)
            except ValueError:
                print("❌ Invalid Input")

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