import tracemalloc
from guestHotel import GuestTravel
from functools import reduce
import time

class Hotel:
   def __init__(self, guestHotel:list =[]):
      self.guestHotel = []
      self.tempShift = []
      self.travel = 0
      self.total_runtime = 0

   def remove_guest(self, guest_id: int):
      if guest_id in GuestTravel.deleted_guest:
         print("❌ Guest already deleted!")
         return
      GuestTravel.deleted_guest.add(guest_id)
      print(f"✅ Successfully removed guest from room {guest_id}")

   def remove_room(self, room_id: int):
      if room_id in GuestTravel.deleted_room:
         print("❌ Room already deleted!")
         return
      if room_id in GuestTravel.manually_added_guest.values():
         for k, v in GuestTravel.manually_added_guest.items():
            if v == room_id:
               del GuestTravel.manually_added_guest[k]
               break
      GuestTravel.deleted_room.add(room_id)
      print(f"✅ Successfully removed room {room_id}")

   def shift_TheManuallyAdded(self, shift_value):
      for key, value in GuestTravel.manually_added_guest.items():
         GuestTravel.manually_added_guest[key] = value + shift_value

   def shift_All(self, shift_value:int):
      self.tempShift.append(shift_value)
      #GuestTravel.deleted_guest = set(map(lambda x : x + shift_value, GuestTravel.deleted_guest))
      self.shift_TheManuallyAdded(shift_value)
      for guest in self.guestHotel:
         guest.Shift(shift_value)

   def add_guest(self, guest:list[int]):
      for g in guest:
         if g < 0:
            return "❌ Invalid Input"
      if(len(guest) !=4):
         return "❌ Invalid Input"
      if(len(self.guestHotel) == 0):
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

   def manual_add_guest(self, room_num):
      if(room_num in GuestTravel.deleted_guest):
         print("❌ Room is already destroyed!")
      if((len(self.guestHotel) > 0 and self.guestHotel[-1].guest_count >= room_num) or room_num in GuestTravel.manually_added_guest.values()): 
         print("❌ Room is already occupied!")
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
      if room_num == 0:
         return 1, 1, 1, 1

      room_idx = room_num 

      if travel[0] != 1:  
         quay = (room_idx // (travel[1] * travel[2] * travel[3])) + 1
         quay_seat = room_idx % (travel[1] * travel[2] * travel[3])

         boat = (quay_seat // (travel[2] * travel[3])) + 1
         boat_seat = quay_seat % (travel[2] * travel[3])

         bus = (boat_seat // travel[3]) + 1
         bus_seat = (boat_seat % travel[3]) + 1  

         return quay, boat, bus, bus_seat

      elif travel[1] != 1:
         boat = (room_idx // (travel[2] * travel[3])) + 1
         boat_seat = room_idx % (travel[2] * travel[3])

         bus = (boat_seat // travel[3]) + 1
         bus_seat = (boat_seat % travel[3]) + 1

         return 1, boat, bus, bus_seat

      elif travel[2] != 1:
         bus = (room_idx // travel[3]) + 1
         bus_seat = (room_idx % travel[3]) + 1

         return 1, 1, bus, bus_seat

      elif travel[3] != 1:
         return 1, 1, 1, room_num

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

      if(room_num > self.guestHotel[-1].guest_count):
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
      print(f"   Group Index   : {idx}")
      print(f"   Travel Path   : Quay {detail[0]}, Boat {detail[1]}, Bus {detail[2]}, Seat {detail[3]}")
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
            if len(group.travel) == 4:
               for m in range(group.travel[0]):
                  offset_a = m * group.travel[1] * group.travel[2] * group.travel[3]
                  for l in range(group.travel[1]):
                     offset_b = offset_a + l * group.travel[2] * group.travel[3]
                     for k in range(group.travel[2]):
                        offset_c = offset_b + k * group.travel[3]
                        for j in range(group.travel[3]):
                           offset_d = offset_c + j
                           guest_id = offset_d
                           room_index = group.room_index(guest_id)
                           if guest_id not in GuestTravel.deleted_guest and room_index not in GuestTravel.deleted_room:
                              final_guest_id = guest_id + group.last_guest_index
                              travel_path = f"({m+1},{l+1},{k+1},{j+1})"
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

         print(f"\n✅ Hotel data successfully saved to '{filename}'")
         print(f"   Total records: {len(all_data)}")
      except IOError as e:
         print(f"\n❌ Error saving file: {e}")