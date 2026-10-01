"""AC sizer: recommends a split/window AC size for a room using common Indian
rules of thumb.

Rules used:
  * Base load: 80 BTU/hr per sq ft for a 10 ft ceiling (roughly the usual
    Indian "1 ton per 150 sq ft" guideline), scaled by ceiling height / 10.
  * People: the first 2 are included in the base; add 600 BTU/hr for each extra person.
  * Direct afternoon sun (west-facing or top floor): add 15% to the total.
  * 1 ton = 12,000 BTU/hr. Pick the smallest standard size that covers the load.

Example runs:

  1) Small bedroom
     Room length (ft): 10
     Room width (ft): 10
     Ceiling height (ft): 10
     Number of people: 2
     Direct afternoon sun? (y/n): n
     -> Recommended AC size: 0.75 ton
        Estimated cooling load: 8,000 BTU/hr
        Why: 100 sq ft room, 2 people, no direct afternoon sun needs about
        8,000 BTU/hr, which a 0.75 ton AC (9,000 BTU/hr) covers.

  2) Master bedroom with afternoon sun
     Room length (ft): 14
     Room width (ft): 12
     Ceiling height (ft): 10
     Number of people: 3
     Direct afternoon sun? (y/n): y
     -> Recommended AC size: 1.5 ton
        Estimated cooling load: 16,146 BTU/hr
        Why: 168 sq ft room, 3 people, with direct afternoon sun (+15%) needs
        about 16,146 BTU/hr, which a 1.5 ton AC (18,000 BTU/hr) covers.

  3) Large living room
     Room length (ft): 20
     Room width (ft): 15
     Ceiling height (ft): 11
     Number of people: 5
     Direct afternoon sun? (y/n): n
     -> Recommended AC size: 2.5 ton
        Estimated cooling load: 28,200 BTU/hr
        Why: 300 sq ft room, 5 people, no direct afternoon sun needs about
        28,200 BTU/hr, which a 2.5 ton AC (30,000 BTU/hr) covers.
"""

import sys

BTU_PER_SQFT = 80          # for a 10 ft ceiling
STANDARD_CEILING_FT = 10
BTU_PER_EXTRA_PERSON = 600
PEOPLE_IN_BASE = 2
SUN_FACTOR = 1.15
BTU_PER_TON = 12000
AC_SIZES_TONS = [0.75, 1, 1.5, 2, 2.5]


def ask_number(prompt, low, high, integer=False):
    """Keep asking until the user enters a number between low and high."""
    while True:
        try:
            raw = input(prompt).strip()
        except EOFError:
            sys.exit("\nNo input received. Exiting.")
        try:
            value = int(raw) if integer else float(raw)
        except ValueError:
            kind = "a whole number" if integer else "a number"
            print(f"  Please enter {kind}.")
            continue
        if not low <= value <= high:
            print(f"  Please enter a value between {low} and {high}.")
            continue
        return value


def ask_yes_no(prompt):
    while True:
        try:
            raw = input(prompt).strip().lower()
        except EOFError:
            sys.exit("\nNo input received. Exiting.")
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Please enter y or n.")


def cooling_load(length, width, height, people, sunny):
    area = length * width
    load = area * BTU_PER_SQFT * (height / STANDARD_CEILING_FT)
    load += max(0, people - PEOPLE_IN_BASE) * BTU_PER_EXTRA_PERSON
    if sunny:
        load *= SUN_FACTOR
    return load


def pick_size(load):
    """Return (tons, fits) for the smallest standard size that covers the load."""
    for tons in AC_SIZES_TONS:
        if tons * BTU_PER_TON >= load:
            return tons, True
    return AC_SIZES_TONS[-1], False


def main():
    print("AC Size Calculator (Indian rules of thumb)\n")
    length = ask_number("Room length (ft): ", 3, 100)
    width = ask_number("Room width (ft): ", 3, 100)
    height = ask_number("Ceiling height (ft): ", 7, 20)
    people = ask_number("Number of people: ", 1, 50, integer=True)
    sunny = ask_yes_no("Direct afternoon sun? (y/n): ")

    load = cooling_load(length, width, height, people, sunny)
    tons, fits = pick_size(load)
    area = length * width
    sun_text = "with direct afternoon sun (+15%)" if sunny else "no direct afternoon sun"

    print()
    print(f"Recommended AC size: {tons:g} ton")
    print(f"Estimated cooling load: {load:,.0f} BTU/hr")
    if fits:
        print(f"Why: {area:g} sq ft room, {people} people, {sun_text} needs about "
              f"{load:,.0f} BTU/hr, which a {tons:g} ton AC "
              f"({tons * BTU_PER_TON:,.0f} BTU/hr) covers.")
    else:
        print(f"Why: {load:,.0f} BTU/hr is more than the largest 2.5 ton unit "
              f"({2.5 * BTU_PER_TON:,.0f} BTU/hr) can handle, so use two ACs "
              f"or a ducted/commercial system for this room.")


if __name__ == "__main__":
    main()
