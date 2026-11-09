# Logic Gate Truth Table Simulator

A Python command-line program that evaluates Boolean expressions and prints their truth tables.

## Supported gates

- Unary: `NOT` and `BUF` (buffer, which copies its input)
- Binary: `AND`, `NAND`, `OR`, `NOR`, `XOR` and `XNOR`
- `BUFFER` is accepted as an alias for `BUF`
- The constants `0` and `1` can be used in expressions

Gate words are recognized without regard to capitalization. Input variable names are kept as entered.

## Expression rules

Use spaces between inputs and gate names. Parentheses can group parts of an expression.

Operator precedence, from highest to lowest:

1. `NOT` and `BUF`
2. `AND` and `NAND`
3. `XOR` and `XNOR`
4. `OR` and `NOR`

Binary gates at the same precedence level are evaluated from left to right. Use parentheses when you want a different grouping. For example, write `NOT (A AND B AND C)` for a three-input NAND.

Input names must start with a letter or underscore. Up to eight distinct input variables are allowed.

## Examples

```text
(A AND B) OR (NOT C)
NOT (A AND B AND C)
BUFFER A XOR B
```

## Show gate tables

Run the program and type `gates` to display the one-input and two-input truth tables and brief descriptions of all supported gates. Type `quit` to exit.

## Requirements

- Python 3
- No external packages required

## Run

```bash
python logic_gate_simulator.py
```
