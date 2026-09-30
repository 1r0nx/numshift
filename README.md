# Numshift — Universal Base Converter

Numshift is a simple and lightweight command-line tool that converts numbers
between multiple numeral systems: **binary**, **octal**, **decimal**, and **hexadecimal**.

It allows seamless conversion from *any supported base to any other*, making it
useful for programmers, CTF players, and anyone working with low-level data.

---

## 🚀 Features

- Convert numbers between:
  - Binary (base 2)
  - Octal (base 8)
  - Decimal (base 10)
  - Hexadecimal (base 16)
- Two modes: a scriptable command-line interface and an interactive prompt
- Numbers list separated by commas/spaces (from arguments or stdin)
- Negative numbers keep their sign
- Robust: invalid inputs are reported and skipped, never crash the tool
- Works on Linux, macOS, and Windows (with Python installed)

---

## 🧱 Requirements
You need to have pyinstaller to compile the source code into binary. You can install it with:
```
pip3 install pyinstaller
```

---

## 🔧 Installation

Clone the repository and build a standalone binary with PyInstaller:
```bash
git clone https://github.com/yourusername/numshift.git
cd numshift
pyinstaller --onefile numshift.py
sudo cp dist/numshift /usr/bin/
```
The executable will be in dist/

Or run it as a script:
```bash
git clone https://github.com/yourusername/numshift.git
cd numshift
chmod +x numshift.py
./numshift.py
```

---

## 🖥️ Usage

**Command-line mode** (scriptable, pipe-friendly) — give an input base, an
output base, and the numbers. Bases accept a name (`bin`/`oct`/`dec`/`hex`) or a
radix (`2`/`8`/`10`/`16`):

```bash
numshift -f hex -t dec FF AB          # -> 255 171
numshift --from bin --to hex 1010 1111 # -> A F
echo "FF,AB" | numshift -f hex -t dec  # reads numbers from stdin
numshift -f dec -t bin -- -10          # negative numbers keep their sign: -1010
```

Invalid numbers are reported on stderr and skipped; the converted values are
printed on stdout, space-separated, in input order.

**Interactive mode** — run with no arguments:

```bash
numshift
```

You pick an input and output base **once** (by name `bin/oct/dec/hex` or radix
`2/8/10/16`), then keep entering numbers. Type `b` to change bases, `q` to quit.
Pick `all` as the output base to convert to every base at once.

```text
❯ numshift

  numshift — base converter (bin/oct/dec/hex)

Input base  [bin/2  oct/8  dec/10  hex/16 | q quit] > hex
Output base [bin/2  oct/8  dec/10  hex/16  all | q quit] > dec

hex → dec   (numbers to convert; 'b' to change bases, 'q' to quit)
> FF AB
  hex(FF) → dec: 255
  hex(AB) → dec: 171
  spaces: 255 171   commas: 255, 171
> b
Input base  [bin/2  oct/8  dec/10  hex/16 | q quit] > dec
Output base [bin/2  oct/8  dec/10  hex/16  all | q quit] > all

dec → all   (numbers to convert; 'b' to change bases, 'q' to quit)
> 255
  dec(255) = bin 11111111 | oct 377 | dec 255 | hex FF
> q

Bye :)
```


## 📜 License

MIT License

---

## 🙋 Contributing

Pull Requests and suggestions are welcome. Please follow standard coding practices and document your changes.
