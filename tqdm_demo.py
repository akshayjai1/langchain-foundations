#!/usr/bin/env python3
"""Demo to understand how range and tqdm work"""

print("="*60)
print("1. WHAT IS range(50)?")
print("="*60)
result = range(50)
print(f"range(50) = {result}")
print(f"Type: {type(result)}")
print(f"As a list: {list(range(50))}")

print("\n" + "="*60)
print("2. WHAT HAPPENS IN A FOR LOOP WITH range(50)?")
print("="*60)
print("for item in range(50):")
print("  print(item)")
print("\nOutput:")
for item in range(50):
    if item < 5:
        print(f"  {item}", end=" ")
    elif item == 5:
        print(f"{item} ... (skipping to show all 50)")
        break

print("\n\n" + "="*60)
print("3. WHAT IS tqdm(range(50))?")
print("="*60)
try:
    from tqdm import tqdm

    result = tqdm(range(50))
    print(f"tqdm(range(50)) = {result}")
    print(f"Type: {type(result)}")
    print("\nIt's a WRAPPER object that wraps the range object.")
    print("It does two things:")
    print("  1. Yields each number from range(50)")
    print("  2. Tracks progress and prints a progress bar")

except ImportError:
    print("tqdm not installed, installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "tqdm"])
    from tqdm import tqdm

    result = tqdm(range(50))
    print(f"tqdm(range(50)) = {result}")
    print(f"Type: {type(result)}")

print("\n" + "="*60)
print("4. SIMPLE ITERATION WITH tqdm(range(5))")
print("="*60)
print("Code:")
print("for item in tqdm(range(5)):")
print("    time.sleep(0.5)")
print("\nOutput (showing progress bar):")

import time
for item in tqdm(range(5)):
    time.sleep(0.5)

print("\n" + "="*60)
print("5. WHAT HAPPENS IN EACH ITERATION?")
print("="*60)
print("for item in tqdm(range(5)):")
print("    print(f'Item: {item}')")
print("    time.sleep(0.5)")
print("\nOutput:")

for item in tqdm(range(5)):
    print(f"  Item: {item}")
    time.sleep(0.3)

print("\n" + "="*60)
print("6. WHAT IS tqdm(50)? (no range)")
print("="*60)
try:
    result = tqdm(50)
    print(f"tqdm(50) = {result}")
    print(f"Type: {type(result)}")
except TypeError as e:
    print(f"Error: {e}")
    print("\ntqdm(50) FAILS because 50 is not iterable.")
    print("tqdm expects something it can loop through (like range, list, etc.)")
    print("You MUST do: tqdm(range(50)) or tqdm([0,1,2,...])")

print("\n" + "="*60)
print("7. WHAT tqdm ACTUALLY DOES INSIDE THE LOOP")
print("="*60)
print("""
When you do:
  for item in tqdm(range(5)):
      time.sleep(0.5)

Each iteration:
  1. tqdm checks: "How many items done? X out of 5"
  2. tqdm prints: "20%|██        | 1/5 [00:00<00:02, 2.00it/s]"
  3. Python gives you the current item (0, 1, 2, 3, 4)
  4. Your code runs: time.sleep(0.5)
  5. Loop repeats

The progress bar UPDATES by reprinting the same line with new numbers.
That's why it looks like it's "moving" - it's actually overwriting the previous line.
""")
