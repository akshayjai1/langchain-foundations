#!/usr/bin/env python3
"""Demo to understand how range works and how tqdm would work"""

print("="*70)
print("1. WHAT IS range(50)?")
print("="*70)
result = range(50)
print(f"\nrange(50) returns: {result}")
print(f"Type: {type(result)}")
print(f"\nWhen converted to list: {list(range(50))}")

print("\n" + "="*70)
print("2. SIMPLE FOR LOOP WITH range(5)")
print("="*70)
print("\nCode:")
print("for item in range(5):")
print("    print(item)")
print("\nOutput:")
for item in range(5):
    print(item)

print("\n" + "="*70)
print("3. HOW ITERATION WORKS - WHAT HAPPENS EACH ITERATION")
print("="*70)
print("\nCode:")
print("for item in range(5):")
print("    print(f'Iteration {item}: value is {item}')")
print("\nOutput:")
for item in range(5):
    print(f"Iteration {item}: value is {item}")

print("\n" + "="*70)
print("4. WHAT DOES tqdm(range(50)) DO?")
print("="*70)
print("""
tqdm is a WRAPPER around range.

Code:
    for item in tqdm(range(5)):
        print(item)

tqdm does TWO things:
  1. It yields each number (0, 1, 2, 3, 4) just like range
  2. It ALSO prints a progress bar to show how many done

Each iteration:
    Iteration 1:
      tqdm prints: "20%|██        | 1/5 [00:00<00:02, 2.00it/s]"
      Your code gets: item = 0
      Your code runs

    Iteration 2:
      tqdm prints: "40%|████      | 2/5 [00:00<00:01, 2.00it/s]" (overwrites line 1)
      Your code gets: item = 1
      Your code runs

    ...and so on
""")

print("\n" + "="*70)
print("5. WHAT ABOUT tqdm(50)? (without range)")
print("="*70)
print("""
tqdm(50) FAILS because:
  - 50 is just a number
  - tqdm needs something iterable (a list, range, etc.)
  - You need: tqdm(range(50))

Example:
  tqdm(50)              ← ERROR: 50 is not iterable
  tqdm(range(50))       ← OK: range is iterable
  tqdm([0,1,2,...,49])  ← OK: list is iterable
""")

print("\n" + "="*70)
print("6. SIMULATING tqdm BEHAVIOR WITHOUT USING tqdm")
print("="*70)
print("\nCode:")
print("""
import time
for i, item in enumerate(range(5)):
    # This simulates what tqdm does
    progress = (i + 1) / 5 * 100
    bar = '█' * (i + 1) + '░' * (5 - i - 1)
    print(f"\\r{progress:.0f}%|{bar}| {i+1}/5", end='', flush=True)
    time.sleep(0.5)
print()  # New line at end
""")
print("\nOutput:")
import time
for i, item in enumerate(range(5)):
    # This simulates what tqdm does
    progress = (i + 1) / 5 * 100
    bar = '█' * (i + 1) + '░' * (5 - i - 1)
    print(f"\r{progress:.0f}%|{bar}| {i+1}/5", end='', flush=True)
    time.sleep(0.3)
print()  # New line at end

print("\n" + "="*70)
print("7. KEY INSIGHTS")
print("="*70)
print("""
range(50):
  - Returns: range(0, 50)
  - Type: <class 'range'>
  - When looped: gives numbers 0, 1, 2, ..., 49

for item in range(50):
  - Each iteration gets the next number
  - item = 0, then 1, then 2, etc.

tqdm(range(50)):
  - Wraps the range object
  - ALSO tracks progress and prints a bar
  - Still yields 0, 1, 2, ..., 49
  - But ADDS visual feedback for each iteration

tqdm(50):
  - ERROR! 50 is just a number, not iterable
  - tqdm MUST wrap something iterable

Why loop if you could just time.sleep(5)?
  - Without loop: one sleep, no feedback
  - With loop: 50 sleeps, 50 updates to progress bar
  - You see progress instead of just waiting silently
""")
