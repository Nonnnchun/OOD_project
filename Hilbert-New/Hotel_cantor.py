import tracemalloc
from guestHotel_cantor import GuestTravel
import time
from typing import Dict, List, Tuple

class Hotel:
    def __init__(self):
        self.guest_groups: List[GuestTravel] = []  
        self.room_to_guest: Dict[int, Tuple[int, int]] = {}  
        self.manual_guests: Dict[int, str] = {}  
        self.deleted_rooms: set = set()  
        self.total_runtime = 0
        self.guest_id_offset = []  

    def parse_bus_input(self, bus_string: str) -> List[int]:
        return [int(x.strip()) for x in bus_string.split('/')]

    def add_guest(self, buses: List[int]):
        group_id = len(self.guest_groups)
        if group_id == 0:
            offset = 0
        else:
            offset = sum(grp.total_guests for grp in self.guest_groups)
        
        self.guest_id_offset.append(offset)

        new_group = GuestTravel(group_id, buses)
        self.guest_groups.append(new_group)

        for guest_index in range(new_group.total_guests):
            room_num = new_group.get_room_number(guest_index)
            self.room_to_guest[room_num] = (group_id, guest_index)
        
        new_manual = dict()
        for guest in self.manual_guests.values():
            room_num = new_group.triple_pair(0,0,int(guest[1:]))
            new_manual[room_num] = guest
        self.manual_guests = new_manual
        
        total_guests = new_group.total_guests
        print(f"\n✅ Added {total_guests} guests successfully!")
        print(f"   Bus configuration: {buses}")
        print(f"   Number of buses: {len(buses)}")
        print(f"   Group ID: {group_id}")

        for i, capacity in enumerate(buses, 1):
            print(f"   Bus {i}: {capacity} people")
    
    def manual_add_guest(self, room_num: int):
        if room_num in self.room_to_guest and room_num not in self.deleted_rooms:
            print("❌ Room is already occupied!")
            return
        if room_num in self.manual_guests:
            print("❌ Room is already occupied by a manual guest!")
            return
        if room_num in self.room_to_guest:
            del self.room_to_guest[room_num]
        
        guest_id = f"M{len(self.manual_guests)}"
        self.manual_guests[room_num] = guest_id
        print(f"✅ Successfully added manual guest {guest_id} to room {room_num}")
    
    def remove_room(self, room_num: int):
        if room_num in self.manual_guests:
            guest_id = self.manual_guests[room_num]
            del self.manual_guests[room_num]
            print(f"✅ Successfully removed manual guest {guest_id} from room {room_num}")
            return
        if room_num not in self.room_to_guest:
            print("❌ Room does not exist!")
            return
        if room_num in self.deleted_rooms:
            print("❌ Room already deleted!")
            return
        
        self.deleted_rooms.add(room_num)
        print(f"✅ Successfully removed room {room_num}")
    
    def print_sorted_room(self):
        """Print all room assignments sorted by room number"""
        print("\n" + "=" * 70)
        print("🏨  HOTEL ROOM STATUS REPORT".center(70))
        print("=" * 70)
        
        all_rooms = []
        
        for group_id, group in enumerate(self.guest_groups):
            for guest_index in range(group.total_guests):
                room_num = group.get_room_number(guest_index)
                
                if room_num in self.deleted_rooms:
                    continue

                if room_num in self.manual_guests:
                    continue
                
                guest_id = self.guest_id_offset[group_id] + guest_index
                bus_num, seat_num = group.get_bus_and_seat(guest_index)
                
                all_rooms.append({
                    'room': room_num,
                    'guest_id': guest_id,
                    'group': group_id,
                    'bus': bus_num,
                    'seat': seat_num,
                    'type': 'Auto'
                })
        
        for room_num, guest_id in self.manual_guests.items():
            all_rooms.append({
                'room': room_num,
                'guest_id': guest_id,
                'group': '-',
                'bus': '-',
                'seat': '-',
                'type': 'Manual'
            })
        
        
        timsort(all_rooms, key=lambda x: x['room'])
        
        print(f"\n{'Guest ID':<12} {'Room':<12} {'Group':<8} {'Bus':<8} {'Seat':<8} {'Type':<8}")
        print("-" * 70)
        
        display_limit = min(50, len(all_rooms))
        for room in all_rooms[:display_limit]:
            print(f"{str(room['guest_id']):<12} {room['room']:<12} {str(room['group']):<8} "
                    f"{str(room['bus']):<8} {str(room['seat']):<8} {room['type']:<8}")
        
        if len(all_rooms) > display_limit:
            print(f"\n... and {len(all_rooms) - display_limit} more rooms")
        
        print("\n" + "=" * 70)
        print(f"📊 Total Occupied Rooms: {len(all_rooms)}")
        print("=" * 70 + "\n")
    
    def search_room(self, room_num: int):
        print(f"\n🔍 Searching for room {room_num}...")
        print("-" * 60)
        
        if room_num in self.manual_guests:
            guest_id = self.manual_guests[room_num]
            print(f"\n✅ Room Found!")
            print(f"   Guest ID      : {guest_id}")
            print(f"   Room Number   : {room_num}")
            print(f"   Type          : Manual")
            print("-" * 60 + "\n")
            return
        
        if room_num in self.deleted_rooms:
            print(f"\n❌ Room Deleted!")
            print(f"   Room Number   : {room_num}")
            print("-" * 60 + "\n")
            return
        
        if room_num not in self.room_to_guest:
            print(f"\n❌ Room {room_num} not found in hotel!")
            print("-" * 60 + "\n")
            return
        
        group_id, guest_index = self.room_to_guest[room_num]
        group = self.guest_groups[group_id]
        guest_id = self.guest_id_offset[group_id] + guest_index #ไอดีคนเฉยๆ
        bus_num, seat_num = group.get_bus_and_seat(guest_index)
        
        print(f"\n✅ Room Found!")
        print(f"   Guest ID      : {guest_id}")
        print(f"   Room Number   : {room_num}")
        print(f"   Group ID      : {group_id}")
        print(f"   Bus Number    : {bus_num}")
        print(f"   Seat Number   : {seat_num}")
        print(f"   Bus Config    : {group.buses}")
        print("-" * 60 + "\n")
    
    def code_runtime(self, func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        self.total_runtime += runtime
        print(f"⏱️  Runtime: {runtime:.6f} seconds")
        return result
    
    def print_total_runtime(self):
        print("\n" + "=" * 50)
        print(f"⏱️  Total Runtime: {self.total_runtime:.6f} seconds")
        print("=" * 50 + "\n")
    
    def memory_used(self):
        current, peak = tracemalloc.get_traced_memory()
        print("\n" + "=" * 50)
        print("💾  Memory Usage Report")
        print("=" * 50)
        print(f"   Peak Memory   : {peak / 1024:.2f} KB")
        print(f"   Current Memory: {current / 1024:.2f} KB")
        print("=" * 50 + "\n")
    
    def save_to_file(self, filename: str):
        try:
            all_data = []
            for group_id, group in enumerate(self.guest_groups):
                for guest_index in range(group.total_guests):
                    room_num = group.get_room_number(guest_index)
                    
                    
                    if room_num in self.deleted_rooms:
                        continue
                    
                    
                    if room_num in self.manual_guests:
                        continue
                    
                    guest_id = self.guest_id_offset[group_id] + guest_index
                    bus_num, seat_num = group.get_bus_and_seat(guest_index)
                    
                    all_data.append({
                        'guest_id': str(guest_id),
                        'room_num': str(room_num),
                        'group': str(group_id),
                        'bus': str(bus_num),
                        'seat': str(seat_num),
                        'type': 'Auto'
                    })
            
            
            for room_num, guest_id in sorted(self.manual_guests.items()):
                all_data.append({
                    'guest_id': guest_id,
                    'room_num': str(room_num),
                    'group': '-',
                    'bus': '-',
                    'seat': '-',
                    'type': 'Manual'
                })
                
            timsort(all_data, key=lambda x: int(x['room_num']))
            
            with open(filename + '.csv', 'w', encoding='utf-8') as f:
                
                f.write("GuestID,RoomNumber,Group,Bus,Seat,Type\n")
                
                
                for row in all_data:
                    f.write(f"{row['guest_id']},{row['room_num']},{row['group']},"
                            f"{row['bus']},{row['seat']},{row['type']}\n")
            
            print(f"\n✅ Hotel data successfully saved to '{filename}.csv'")
            print(f"   Total records: {len(all_data)}")
        
        except IOError as e:
            print(f"\n❌ Error saving file: {e}")
            
def insertion_sort(arr, left, right, key):
    """Simple insertion sort used on small subarrays (runs)."""
    for i in range(left + 1, right + 1):
        temp = arr[i]
        j = i - 1
        while j >= left and key(arr[j]) > key(temp):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = temp


def merge(arr, l, m, r, key):
    """Merge two sorted subarrays arr[l:m] and arr[m:r]."""
    left = arr[l:m]
    right = arr[m:r]
    i = j = 0
    k = l

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1


def timsort(arr, key=lambda x: x, min_run=32):
    """Perform Timsort on arr using given key function."""
    n = len(arr)

    # Step 1: Sort small subarrays (runs) using insertion sort
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end, key)

    # Step 2: Merge sorted runs
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n, left + size)
            right = min((left + 2 * size), n)
            merge(arr, left, mid, right, key)
        size *= 2