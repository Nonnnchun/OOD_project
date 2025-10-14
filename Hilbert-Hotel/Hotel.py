import tracemalloc
from guestHotel import GuestTravel
from functools import reduce
import time

class Hotel:
   def __init__(self, guestHotel: list = []):
      self.guestHotel = []
      self.tempShift = []
      self.travel = 0
      self.total_runtime = 0

   def remove_room(self, room_id: int):
      if room_id in GuestTravel.deleted_room:
         print("❌ Room already deleted!")
         return
      if room_id in GuestTravel.manually_added_guest.values():
         for k, v in GuestTravel.manually_added_guest.items():
               if v == room_id:
                  del GuestTravel.manually_added_guest[k]
                  break
      GuestTravel.deleted_room.append(room_id)
      print(f"✅ Successfully removed room {room_id}")

   def shift_TheManuallyAdded(self, shift_value):
      for i in range(len(GuestTravel.manually_added_guest_deleted)):
         GuestTravel.manually_added_guest_deleted[i] += shift_value
      for key, value in GuestTravel.manually_added_guest.items():
         GuestTravel.manually_added_guest[key] = value + shift_value

   def shift_All(self, shift_value: int):
      self.tempShift.append(shift_value)

      self.shift_TheManuallyAdded(shift_value)
      for guest in self.guestHotel:
         guest.Shift(shift_value)
      for i in range(len(guest.deleted_room)):
         guest.deleted_room[i] += shift_value

   def add_guest(self, guest: list[int]):
      if len(self.guestHotel) == 0:
         new_guest = GuestTravel(0, guest)
         self.shift_TheManuallyAdded(reduce(lambda x, y: x * y, guest))
         self.guestHotel.append(new_guest)
      else:
         self.shift_All(reduce(lambda x, y: x * y, guest))
         new_guest = GuestTravel(self.guestHotel[-1].guest_count, guest)
         self.guestHotel.append(new_guest)

      total_guests = reduce(lambda x, y: x * y, guest)
      print(f"\n✅ Added {total_guests} guests successfully!")
      print(f"   Travel configuration: {guest}")
      print(f"   Dimensions: {len(guest)}")

   def manual_add_guest(self, room_num):
      room = False
      if room_num in GuestTravel.deleted_room:
         # GuestTravel.deleted_room.remove(room_num)
         GuestTravel.manually_added_guest_deleted.append(room_num)
         room = True
      if not room and (len(self.guestHotel) > 0 and self.guestHotel[-1].guest_count - 1 >= room_num) or room_num in GuestTravel.manually_added_guest.values():
         print("❌ Room is already occupied!")
         return

      else:
         guest_id = "M" + str(len(GuestTravel.manually_added_guest))
         GuestTravel.manually_added_guest[guest_id] = room_num
         print(f"✅ Successfully added manual guest {guest_id} to room {room_num}")

   def print_sorted_room(self):
      print("\n" + "=" * 60)
      print("🏨  HOTEL ROOM STATUS REPORT".center(60))
      print("=" * 60)

      total_rooms = 0

      for idx, group in enumerate(reversed(self.guestHotel)):
         group_num = len(self.guestHotel) - idx
         print(f"\n┌{'─' * 58}┐")
         print(f"│  📋 Guest Group #{group_num:<40}│")
         print(f"│  Configuration: {str(group.travel):<38}│")
         print(f"│  Dimensions: {len(group.travel):<43}│")
         print(f"└{'─' * 58}┘")

         guest_count = group.print_index()
         total_rooms += guest_count

      if GuestTravel.manually_added_guest:
         print(f"\n┌{'─' * 58}┐")
         print(f"│  👤 Manually Added Guests{' ' * 31}│")
         print(f"└{'─' * 58}┘")
         for guest_id, room_num in sorted(GuestTravel.manually_added_guest.items(), key=lambda x: x[1]):
               print(f"  Guest {guest_id:<12} → Room {room_num:>6}")
         total_rooms += len(GuestTravel.manually_added_guest)

      print("\n" + "=" * 60)
      print(f"📊 Total Occupied Rooms: {total_rooms}")
      print("=" * 60 + "\n")

   def find_path(self, room_num, travel):
      room_idx = room_num
      path = []
      for i in range(len(travel) - 1, -1, -1):
         position = (room_idx % travel[i]) + 1
         path.append(position)
         room_idx //= travel[i]
      
      return tuple(reversed(path))

   def format_travel_path(self, path, travel):
      """Format the travel path with dimension labels"""
      if len(travel) == 4:
         labels = ["Quay", "Boat", "Bus", "Seat"]
      elif len(travel) == 3:
         labels = ["Level", "Section", "Seat"]
      elif len(travel) == 2:
         labels = ["Floor", "Room"]
      else:
         labels = [f"Dim{i+1}" for i in range(len(travel))]
      
      return ", ".join([f"{label} {pos}" for label, pos in zip(labels, path)])

   def find_insert(self, target: int) -> int:
      if not self.guestHotel:
         return 0
      lo, hi = 0, len(self.guestHotel) - 1
      while lo <= hi:
         mid = (lo + hi) // 2
         mid_val = self.guestHotel[mid].shift
         seed_range = self.guestHotel[mid].guest_count - self.guestHotel[mid].last_guest_index
         if mid_val <= target < seed_range + mid_val:
               return mid
         if mid_val > target:
               lo = mid + 1
         elif mid_val < target:
               hi = mid - 1
      return mid

   def search_room(self, room_num):
      print(f"\n🔍 Searching for room {room_num}...")
      print("-" * 50)

      if room_num in GuestTravel.manually_added_guest.values():
         keys = [key for key, val in GuestTravel.manually_added_guest.items() if val == room_num]
         print(f"\n✅ Room Found!")
         print(f"   Guest ID      : {keys[0]}")
         print(f"   Room Number   : {room_num}")
         print(f"   Type          : Manual")
         print("-" * 50 + "\n")
         return
      if room_num in GuestTravel.deleted_room:
         print(f"\n❌ Room Deleted!")
         print(f"   Room Number   : {room_num}")
         print(f"   Type          : Manually Deleted")
         print("-" * 50 + "\n")
         return
      if room_num > self.guestHotel[-1].guest_count - 1:
         print(f"\n❌ Room {room_num} not found in hotel!")
         print("-" * 50 + "\n")
         return

      idx = self.find_insert(room_num)
      self.travel = idx
      detail = self.find_path(room_num - self.guestHotel[idx].shift, self.guestHotel[idx].travel)
      guest_id = (room_num - self.guestHotel[idx].shift) + self.guestHotel[idx].last_guest_index

      print(f"\n✅ Room Found!")
      print(f"   Guest ID      : {guest_id}")
      print(f"   Room Number   : {room_num}")
      print(f"   Group Index   : {idx+1}")
      print(f"   Dimensions    : {len(self.guestHotel[idx].travel)}")
      print(f"   Travel Path   : {self.format_travel_path(detail, self.guestHotel[idx].travel)}")
      print("-" * 50 + "\n")

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
         for idx, group in enumerate(self.guestHotel):
            total_guests = reduce(lambda x, y: x * y, group.travel)
            for guest_id in range(total_guests):
               room_index = group.room_index(guest_id)
               if room_index not in GuestTravel.deleted_room:
                  final_guest_id = guest_id + group.last_guest_index
                  positions = []
                  temp_id = guest_id
                  for dim in range(len(group.travel) - 1, -1, -1):
                     position = (temp_id % group.travel[dim]) + 1
                     positions.insert(0, position)
                     temp_id //= group.travel[dim]
                  
                  travel_path = f"({','.join(map(str, positions))})"
                  
                  all_data.append({
                     'guest_id': str(final_guest_id),
                     'room_num': str(room_index),
                     'group': str(idx + 1),
                     'travel_path': travel_path,
                     'type': 'Auto'
                  })

         for guest_id, room_num in sorted(GuestTravel.manually_added_guest.items(), key=lambda x: x[1]):
            all_data.append({
               'guest_id': guest_id,
               'room_num': str(room_num),
               'group': '-',
               'travel_path': '-',
               'type': 'Manual'
            })

         max_guest_id = max(len(row['guest_id']) for row in all_data) if all_data else 7
         max_room_num = max(len(row['room_num']) for row in all_data) if all_data else 10
         max_group = max(len(row['group']) for row in all_data) if all_data else 5
         max_travel = max(len(row['travel_path']) for row in all_data) if all_data else 11
         max_type = 6

         max_guest_id = max(max_guest_id, 7)
         max_room_num = max(max_room_num, 10)
         max_group = max(max_group, 5)
         max_travel = max(max_travel, 11)

         with open(filename + '.csv', 'w', encoding='utf-8') as f:
            header = f"{'GuestID':^{max_guest_id}} | {'RoomNumber':^{max_room_num}} | {'Group':^{max_group}} | {'TravelPath':^{max_travel}} | {'Type':^{max_type}}\n"
            separator = f"{'-'*max_guest_id}-+-{'-'*max_room_num}-+-{'-'*max_group}-+-{'-'*max_travel}-+-{'-'*max_type}\n"
            f.write(header)
            f.write(separator)

            for row in all_data:
               line = f"{row['guest_id']:>{max_guest_id}} | {row['room_num']:>{max_room_num}} | {row['group']:>{max_group}} | {row['travel_path']:^{max_travel}} | {row['type']:^{max_type}}\n"
               f.write(line)

         print(f"\n✅ Hotel data successfully saved to '{filename}.csv'")
         print(f"   Total records: {len(all_data)}")
      except IOError as e:
         print(f"\n❌ Error saving file: {e}")