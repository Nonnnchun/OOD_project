from typing import Tuple, Dict, List, Union

# ---- Rule classes ----

class Rule:
   """Abstract base class for hotel rules"""
   def apply(self, guest: int) -> int:
      raise NotImplementedError
   def inverse(self, room: int) -> int:
      raise NotImplementedError


class Shift(Rule):
   def __init__(self, k: int):
      self.k = k
   def apply(self, guest: int) -> int:
      return guest + self.k
   def inverse(self, room: int) -> int:
      return room - self.k


class Scale2(Rule):
   def apply(self, guest: int) -> int:
      return guest * 2
   def inverse(self, room: int) -> int:
      if room % 2 != 0:
         raise ValueError(f"Room {room} not occupied under Scale2 rule")
      return room // 2


class Rebalance(Rule):
   def __init__(self, aisles_old: int, aisles_new: int):
      self.a_old = aisles_old
      self.a_new = aisles_new
   def apply(self, guest: int) -> int:
      # map guest under old aisles -> new aisles
      aisle = guest % self.a_old
      index = guest // self.a_old
      return index * self.a_new + aisle
   def inverse(self, room: int) -> int:
      aisle = room % self.a_new
      index = room // self.a_new
      return index * self.a_old + aisle


# ---- Hotel class ----

class Hotel:
   def __init__(self, aisles: int = 1):
      self.aisles = aisles
      self.rules: List[Rule] = []
      self.g2s: Dict[int, Tuple[int,int]] = {}   # guest → slot
      self.s2g: Dict[Tuple[int,int], int] = {}   # slot → guest

   def add_rule(self, rule: Rule):
      self.rules.append(rule)

   def apply_rules(self, guest: int) -> int:
      x = guest
      for r in self.rules:
         x = r.apply(x)
      return x

   def room_of(self, guest: int) -> Tuple[int,int]:
      # Pinned?
      if guest in self.g2s:
         return self.g2s[guest]

      # Otherwise, compute under rules
      slot = self.apply_rules(guest)
      aisle = slot % self.aisles
      index = slot // self.aisles
      return (aisle, index)

   def guest_of(self, slot: Tuple[int,int]) -> Union[int,None]:
      # Pinned?
      if slot in self.s2g:
         return self.s2g[slot]

      linear = slot[1] * self.aisles + slot[0]
      x = linear
      for r in reversed(self.rules):
         x = r.inverse(x)
      return x

   def pin(self, guest: int, slot: Tuple[int,int]) -> None:
      # If already pinned to someone else, evict them
      if slot in self.s2g and self.s2g[slot] != guest:
         evicted = self.s2g[slot]
         del self.g2s[evicted]
         del self.s2g[slot]
         new_slot = self.room_of(evicted)
         print(f"Evicted guest {evicted}, reassigned to {new_slot}")

      # Apply pin
      self.g2s[guest] = slot
      self.s2g[slot] = guest

   def snapshot(self, guests: List[int]) -> List[Tuple[int,Tuple[int,int]]]:
      return [(g, self.room_of(g)) for g in guests]


# ---- Example usage ----

if __name__ == "__main__":
   hotel = Hotel(aisles=3)

   # Add some rules
   hotel.add_rule(Shift(1))     # everyone moves forward by 1
   hotel.add_rule(Scale2())     # spread them out
   hotel.add_rule(Rebalance(3, 4)) # rebalance aisles

   # Pin a guest into a room (with eviction)
   hotel.pin(42, (0, 1))

   # Get room of some guests
   print("Guest 5 ->", hotel.room_of(5))
   print("Guest 42 ->", hotel.room_of(42))

   # Take a snapshot
   snapshot = hotel.snapshot([0,1,2,3,42])
   print("Snapshot:", snapshot)