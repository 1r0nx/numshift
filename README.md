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
base: 1

Enter number(s) separated by spaces or commas: 12 23 34 45

===== Conversion Results =====
dec(12) → bin: 1100
dec(23) → bin: 10111
dec(34) → bin: 100010
dec(45) → bin: 101101
List separed by spaces: 1100 10111 100010 101101
List separed by commas: 1100, 10111, 100010, 101101
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
Choose an input base
1. bin
2. oct
3. dec
4. hex
q. quit
base: 1


Choose an output base
1. bin
2. oct
3. dec
4. hex
q. quit
base: 3

Enter number(s) separated by spaces or commas: 1110 0234 1121 1000

===== Conversion Results =====
bin(1110) → dec: 14
0234: is not a bin number
1121: is not a bin number
bin(1000) → dec: 8
List separed by spaces: 14 8
List separed by commas: 14, 8
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
