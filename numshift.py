#!/usr/bin/env python3

import sys

BASES = {
    "1": ("bin", 2),
    "2": ("oct", 8),
    "3": ("dec", 10),
    "4": ("hex", 16),
}


def ask_base(prompt):
    while True:
        print(prompt)
        print("1. bin\n2. oct\n3. dec\n4. hex\nq. quit")
        choice = input("base: ").strip()
        if choice == "q":
            print("\nBye :)")
            sys.exit(0)
        if choice in BASES:
            return choice
        print("\nWrong base!\n")


def convert(value: str, from_base: int, to_base: int):
    try:
        n = int(value, from_base)
    except ValueError:
        return None

    if to_base == 2:
        return bin(n)[2:]
    elif to_base == 8:
        return oct(n)[2:]
    elif to_base == 10:
        return str(n)
    elif to_base == 16:
        return hex(n)[2:].upper()


def main():
    for i in range(10):
        in_choice = ask_base("Choose an input base")
        print("\n")
        out_choice = ask_base("Choose an output base")

        if in_choice == out_choice:
            print("\nYou chose the same base twice!\n")
            continue

        in_name, in_base = BASES[in_choice]
        out_name, out_base = BASES[out_choice]

        print(f"\n{in_name} > {out_name}")
        raw = input(f"Enter {in_name} number(s) separated by spaces or commas: ")
        numbers = [x.strip() for x in raw.replace(",", " ").split() if x.strip()]

        result_list = []
        print("\n===== Conversion Results =====")
        for num in numbers:
            result = convert(num, in_base, out_base)
            if result is None:
                print(f"{num}: is not a {in_name} number")
                continue
            else:
                print(f"{in_name}({num}) → {out_name}: {result}")
                result_list.append(result)

        print("\n")
        if result_list:
            print(f"List separed by spaces: {" ".join(result_list)}")
            print(f"List separed by commas: {", ".join(result_list)}")
        print("==============================\n")


if __name__ == "__main__":
    main()
