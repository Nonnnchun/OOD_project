# hilbert_hotel.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional, List, Dict, Tuple, Iterable
import csv, gzip

Slot = Tuple[int, int]  # (aisle, index)  index starts at 1

# ---------- Utilities: φ_A, ψ_A ----------
def phi(A: int, n: int) -> Slot:
   """Map linear index n -> (aisle, index) under A aisles."""
   if n < 0: raise ValueError("n must be >= 0")
   return (n % A, n // A + 1)

def psi(A: int, a: int, r: int) -> int:
   """Inverse: (aisle, index) -> linear index n under A aisles."""
   if not (0 <= a < A and r >= 1):
      raise ValueError("invalid (aisle, index)")
   return (r - 1) * A + a

# ---------- Rule primitives (bijective over ℕ: n -> n') ----------
@dataclass
class Rule:
   apply: Callable[[int], int]
   invert: Callable[[int], Optional[int]]
   name: str = "rule"

def Shift(k: int) -> Rule:
   return Rule(
      apply=lambda n: n + k,
      invert=lambda x: x - k if x - k >= 0 else None,
      name=f"shift({k})"
   )

def Scale2() -> Rule:
   # n -> 2n  (frees half the rooms; inverse valid only for even x)
   return Rule(
      apply=lambda n: 2 * n,
      invert=lambda x: (x // 2) if x % 2 == 0 else None,
      name="scale2"
   )

def Rebalance(A_old: int, A_new: int) -> Rule:
   # map linear index under A_old to linear index under A_new, preserving (aisle, index)
   def _apply(n: int) -> int:
      a, r = phi(A_old, n)
      return psi(A_new, a, r)
   def _invert(x: int) -> Optional[int]:
      a, r = phi(A_new, x)
      return psi(A_old, a, r)
   return Rule(apply=_apply, invert=_invert, name=f"rebalance({A_old}->{A_new})")

# ---------- Composition helpers ----------
def apply_compose(rules: List[Rule], n: int) -> int:
   x = n
   for rule in rules:
      x = rule.apply(x)
   return x

def invert_compose(rules: List[Rule], x: int) -> Optional[int]:
   y = x
   for rule in reversed(rules):
      y = rule.invert(y)
      if y is None:
         return None
   return y

# ---------- Hotel model ----------
class Hotel:
   def __init__(self, aisles: int):
      if aisles <= 0: raise ValueError("aisles must be >= 1")
      self.A: int = aisles
      self.rules: List[Rule] = []  # compose left->right
      # overrides / pins
      self.g2s: Dict[int, Slot] = {}
      self.s2g: Dict[Slot, int] = {}

   # ---- system-wide transforms (O(1)) ----
   def shift(self, k: int = 1) -> None:
      self.rules.append(Shift(k))

   def scale2(self) -> None:
      self.rules.append(Scale2())

   def set_aisles(self, new_A: int) -> None:
      """Change number of aisles with a bijection (no per-guest moves)."""
      if new_A <= 0: raise ValueError("new_A must be >= 1")
      if new_A == self.A: return
      self.rules.append(Rebalance(self.A, new_A))
      self.A = new_A

   # ---- overrides (manual pin/unpin) ----
   def pin(self, guest: int, slot: Slot) -> None:
      """Force a guest to a particular slot."""
      # maintain bijection in override layer
      if slot in self.s2g and self.s2g[slot] != guest:
         raise ValueError(f"slot {slot} already pinned to guest {self.s2g[slot]}")
      if guest in self.g2s and self.g2s[guest] != slot:
         raise ValueError(f"guest {guest} already pinned to {self.g2s[guest]}")
      self.g2s[guest] = slot
      self.s2g[slot] = guest

   def unpin_guest(self, guest: int) -> None:
      if guest in self.g2s:
         slot = self.g2s.pop(guest)
         self.s2g.pop(slot, None)

   def unpin_slot(self, slot: Slot) -> None:
      if slot in self.s2g:
         guest = self.s2g.pop(slot)
         self.g2s.pop(guest, None)

   # ---- queries ----
   def room_of(self, guest: int) -> Slot:
      """guest -> (aisle, index)"""
      if guest in self.g2s:
         return self.g2s[guest]
      n_prime = apply_compose(self.rules, guest)
      return phi(self.A, n_prime)

   def guest_in(self, slot: Slot) -> Optional[int]:
      """(aisle, index) -> guest, or None if not in image of rules."""
      if slot in self.s2g:
         return self.s2g[slot]
      n_prime = psi(self.A, slot[0], slot[1])
      guest = invert_compose(self.rules, n_prime)
      return guest

   # ---- batch views (lazy generators) ----
   def iter_guests(self, start: int, end_inclusive: int) -> Iterable[Tuple[int, Slot]]:
      for g in range(start, end_inclusive + 1):
         yield g, self.room_of(g)

   def iter_rooms(self, a0: int, a1_inclusive: int, r0: int, r1_inclusive: int) -> Iterable[Tuple[Slot, Optional[int]]]:
      for a in range(a0, a1_inclusive + 1):
         for r in range(r0, r1_inclusive + 1):
               yield (a, r), self.guest_in((a, r))

   # ---- export snapshots (streaming) ----
   def write_guest_snapshot_csv(self, start_guest: int, end_guest_inclusive: int, path: str, gz: bool=False) -> None:
      op = gzip.open if gz else open
      with op(path, "wt", newline="") as f:
         w = csv.writer(f)
         w.writerow(["guest", "aisle", "index"])
         for g, (a, r) in self.iter_guests(start_guest, end_guest_inclusive):
               w.writerow([g, a, r])

   def write_room_snapshot_csv(self, a0: int, a1_inclusive: int, r0: int, r1_inclusive: int, path: str, gz: bool=False) -> None:
      op = gzip.open if gz else open
      with op(path, "wt", newline="") as f:
         w = csv.writer(f)
         w.writerow(["aisle", "index", "guest"])
         for (a, r), g in self.iter_rooms(a0, a1_inclusive, r0, r1_inclusive):
               w.writerow([a, r, "" if g is None else g])

# ---------- example usage ----------
if __name__ == "__main__":
   hotel = Hotel(aisles=3)             # เริ่มมี 3 ทางเดิน
   hotel.shift(1)                      # เว้น 1 ห้องแรก
   hotel.scale2()                      # แยกคู่/คี่ เพื่อรับแขกอนันต์
   hotel.pin(guest=7, slot=(2, 3))     # ปักแขก 7 ไว้ที่ทางเดิน 2 ห้องที่ 3
   hotel.set_aisles(4)                 # เปลี่ยนเป็น 4 ทางเดิน (O(1))

   # ตัวอย่าง query
   print("guest 10 ->", hotel.room_of(10))  # (aisle, index)
   print("room (0,1) ->", hotel.guest_in((0,1)))

   # เขียน snapshot ตัวอย่าง
   hotel.write_guest_snapshot_csv(0, 100000, "guest_to_room.csv.gz", gz=False)
   # hotel.write_room_snapshot_csv(0, hotel.A-1, 1, 200, "room_to_guest.csv.gz", gz=True)