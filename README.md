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
- Clear CLI interface
- Numbers list separed by commas/spaces
- Error handling for invalid inputs
- Works on Linux, macOS, and Windows (with Python installed)

---

## 🧱 Requirements
You need to have pyinstaller to compile the source code into binary. You can install it with:
```
pip3 install pyinstaller
```

---

## 🔧 Installation

Clone the repository and create a binary:
```bash
git clone https://github.com/yourusername/numshift.git
cd numshift
chmod +x build.sh
./build.sh
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


## ⚙️ Example

```bash
numshift
```

Output:

```bash
❯ numshift
Choose an input base
1. bin
2. oct
3. dec
4. hex
q. quit
base: 2


Choose an output base
1. bin
2. oct
3. dec
4. hex
q. quit
base: 1

oct > bin
Enter oct number(s) separated by spaces or commas: 12 34 09 34

===== Conversion Results =====
oct(12) → bin: 1010
oct(34) → bin: 11100
09: is not a oct number
oct(34) → bin: 11100


List separed by spaces: 1010 11100 11100
List separed by commas: 1010, 11100, 11100
==============================

Choose an input base
1. bin
2. oct
3. dec
4. hex
q. quit
base: q

Bye :)
```

Another example with error handling:

```bash
❯ ./numshift.py
Choose an input base
1. bin
2. oct
3. dec
4. hex
q. quit
base: 3


Choose an output base
1. bin
2. oct
3. dec
4. hex
q. quit
base: 4

dec > hex
Enter dec number(s) separated by spaces or commas: 12 4 45 FF AA 34

===== Conversion Results =====
dec(12) → hex: C
dec(4) → hex: 4
dec(45) → hex: 2D
FF: is not a dec number
AA: is not a dec number
dec(34) → hex: 22


List separed by spaces: C 4 2D 22
List separed by commas: C, 4, 2D, 22
==============================

Choose an input base
1. bin
2. oct
3. dec
4. hex
q. quit
base: q

Bye :)

```

## 📜 License

MIT License

---

## 🙋 Contributing

Pull Requests and suggestions are welcome. Please follow standard coding practices and document your changes.
