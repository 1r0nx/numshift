#!/usr/bin/env python3

import argparse
import sys

# Interactive menu choice -> (canonical name, radix)
MENU = {
    "1": ("bin", 2),
    "2": ("oct", 8),
    "3": ("dec", 10),
    "4": ("hex", 16),
}
NAME_TO_RADIX = {"bin": 2, "oct": 8, "dec": 10, "hex": 16}
RADIX_TO_NAME = {2: "bin", 8: "oct", 10: "dec", 16: "hex"}


def convert(value: str, from_base: int, to_base: int):
    """Convert a number string from one base to another. Returns the converted
    string, or None if `value` is not a valid number in `from_base`. Negative
    numbers keep their sign."""
    try:
        n = int(value, from_base)
    except ValueError:
        return None
    sign = "-" if n < 0 else ""
    n = abs(n)
    body = {2: "b", 8: "o", 10: "d", 16: "X"}[to_base]
    return sign + format(n, body)


def resolve_base(token):
    """Resolve a base given as a name (bin/oct/dec/hex) or a radix (2/8/10/16).
    Returns (radix, name) or (None, None) if invalid."""
    t = token.strip().lower()
    if t in NAME_TO_RADIX:
        return NAME_TO_RADIX[t], t
    if t.isdigit() and int(t) in RADIX_TO_NAME:
        return int(t), RADIX_TO_NAME[int(t)]
    return None, None


def split_numbers(raw):
    """Split a raw string into number tokens on spaces and commas."""
    return [x for x in raw.replace(",", " ").split() if x]


# ─── non-interactive CLI ────────────────────────────────────────────────────--

def run_cli(parser, args):
    from_base, from_name = resolve_base(args.from_base)
    to_base, to_name = resolve_base(args.to_base)
    if from_base is None:
        parser.error(f"invalid input base: {args.from_base!r} (use bin/oct/dec/hex or 2/8/10/16)")
    if to_base is None:
        parser.error(f"invalid output base: {args.to_base!r} (use bin/oct/dec/hex or 2/8/10/16)")

    raw = " ".join(args.numbers)
    if not raw and not sys.stdin.isatty():
        raw = sys.stdin.read()
    numbers = split_numbers(raw)
    if not numbers:
        parser.error("no numbers to convert (pass them as arguments or on stdin)")

    results, had_error = [], False
    for num in numbers:
        res = convert(num, from_base, to_base)
        if res is None:
            print(f"[!] {num!r} is not a {from_name} number", file=sys.stderr)
            had_error = True
        else:
            results.append(res)

    if results:
        print(" ".join(results))
    return 1 if had_error and not results else 0


# ─── interactive mode ─────────────────────────────────────────────────────────

def ask_base(prompt):
    """Prompt for a base from the menu. Returns a MENU key, or None to quit."""
    while True:
        print(prompt)
        print("1. bin\n2. oct\n3. dec\n4. hex\nq. quit")
        try:
            choice = input("base: ").strip().lower()
        except EOFError:
            return None
        if choice in ("q", "quit"):
            return None
        if choice in MENU:
            return choice
        print("\nWrong base!\n")


def interactive():
    while True:
        in_choice = ask_base("Choose an input base")
        if in_choice is None:
            break
        print()
        out_choice = ask_base("Choose an output base")
        if out_choice is None:
            break

        if in_choice == out_choice:
            print("\nYou chose the same base twice!\n")
            continue

        in_name, in_base = MENU[in_choice]
        out_name, out_base = MENU[out_choice]

        print(f"\n{in_name} > {out_name}")
        try:
            raw = input(f"Enter {in_name} number(s) separated by spaces or commas: ")
        except EOFError:
            break

        numbers = split_numbers(raw)
        result_list = []
        print("\n===== Conversion Results =====")
        for num in numbers:
            result = convert(num, in_base, out_base)
            if result is None:
                print(f"{num}: is not a {in_name} number")
            else:
                print(f"{in_name}({num}) → {out_name}: {result}")
                result_list.append(result)

        print()
        if result_list:
            print(f"List separated by spaces: {' '.join(result_list)}")
            print(f"List separated by commas: {', '.join(result_list)}")
        print("==============================\n")

    print("\nBye :)")


def main():
    parser = argparse.ArgumentParser(
        prog="numshift",
        description="Convert numbers between binary, octal, decimal and hexadecimal.",
        epilog="examples:\n"
               "  numshift -f hex -t dec FF AB\n"
               "  numshift --from bin --to hex 1010 1111\n"
               "  echo 'FF,AB' | numshift -f hex -t dec\n"
               "  numshift            # no args -> interactive menu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-f", "--from", dest="from_base", metavar="BASE",
                        help="input base: bin/oct/dec/hex or 2/8/10/16")
    parser.add_argument("-t", "--to", dest="to_base", metavar="BASE",
                        help="output base: bin/oct/dec/hex or 2/8/10/16")
    parser.add_argument("numbers", nargs="*",
                        help="numbers to convert (space/comma separated); read from stdin if omitted")
    args = parser.parse_args()

    try:
        if args.from_base or args.to_base:
            if not (args.from_base and args.to_base):
                parser.error("both --from and --to are required for non-interactive mode")
            return run_cli(parser, args)
        if args.numbers:
            parser.error("--from and --to are required when passing numbers on the command line")
        interactive()
        return 0
    except KeyboardInterrupt:
        print("\nBye :)")
        return 130


if __name__ == "__main__":
    sys.exit(main())
