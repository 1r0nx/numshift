#!/usr/bin/env python3

import argparse
import sys

NAME_TO_RADIX = {"bin": 2, "oct": 8, "dec": 10, "hex": 16}
RADIX_TO_NAME = {2: "bin", 8: "oct", 10: "dec", 16: "hex"}

# ─── colours (disabled when output is not a terminal) ───────────────────────--
_RESET, _BOLD, _DIM = "\033[0m", "\033[1m", "\033[2m"
_GREEN, _RED, _CYAN, _YELLOW = "\033[92m", "\033[91m", "\033[96m", "\033[93m"
USE_COLOR = sys.stdout.isatty()

def c(text, *codes):
    return ("".join(codes) + str(text) + _RESET) if (USE_COLOR and codes) else str(text)


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

def ask_base(label, allow_all=False):
    """Compact one-line base prompt. Accepts a name (bin/oct/dec/hex) or a radix
    (2/8/10/16); 'q' quits; 'all' when allowed. Returns (radix, name), the string
    "all", or None to quit. (No 1-4 keys: '2' would be ambiguous with radix 2.)"""
    opts = "bin/2  oct/8  dec/10  hex/16" + ("  all" if allow_all else "")
    prompt = c(f"{label.ljust(11)} ", _BOLD) + c(f"[{opts} | q quit] ", _DIM) + "> "
    while True:
        try:
            choice = input(prompt).strip().lower()
        except EOFError:
            return None
        if choice in ("q", "quit"):
            return None
        if allow_all and choice == "all":
            return "all"
        radix, name = resolve_base(choice)     # name or radix
        if radix is not None:
            return radix, name
        print(c("  invalid base — use a name (hex) or a radix (16)", _RED))


def _print_conversion(num, in_base, in_name, out_choice):
    """Print one number converted, coloured. out_choice is (radix, name) or 'all'."""
    if out_choice == "all":
        vals = []
        for radix in (2, 8, 10, 16):
            res = convert(num, in_base, radix)
            if res is None:
                print("  " + c(f"{num}: is not a {in_name} number", _RED))
                return None
            vals.append(f"{RADIX_TO_NAME[radix]} {res}")
        print("  " + c(f"{in_name}({num})", _CYAN) + " = " + c(" | ".join(vals), _GREEN))
        return None

    out_base, out_name = out_choice
    res = convert(num, in_base, out_base)
    if res is None:
        print("  " + c(f"{num}: is not a {in_name} number", _RED))
        return None
    print("  " + c(f"{in_name}({num}) → {out_name}: ", _DIM) + c(res, _GREEN))
    return res


def interactive():
    print(c("\n  numshift — base converter (bin/oct/dec/hex)\n", _BOLD, _CYAN))
    need_bases = True
    in_base = in_name = out_choice = None

    while True:
        if need_bases:
            r = ask_base("Input base")
            if r is None:
                break
            in_base, in_name = r
            r = ask_base("Output base", allow_all=True)
            if r is None:
                break
            out_choice = r
            out_label = "all" if out_choice == "all" else out_choice[1]
            print(c(f"\n{in_name} → {out_label}", _YELLOW) +
                  c("   (numbers to convert; 'b' to change bases, 'q' to quit)", _DIM))
            need_bases = False

        try:
            raw = input(c("> ", _BOLD))
        except EOFError:
            break
        cmd = raw.strip().lower()
        if cmd in ("q", "quit"):
            break
        if cmd == "b":
            need_bases = True
            continue

        numbers = split_numbers(raw)
        if not numbers:
            continue

        results = [r for r in (_print_conversion(n, in_base, in_name, out_choice)
                               for n in numbers) if r is not None]
        if out_choice != "all" and results:
            print(c(f"  spaces: {' '.join(results)}   commas: {', '.join(results)}", _DIM))

    print(c("\nBye :)\n", _CYAN))


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
