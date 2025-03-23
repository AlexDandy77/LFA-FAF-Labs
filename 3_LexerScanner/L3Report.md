# Lexer & Scanner

### Course: Formal Languages & Finite Automata

### Author: Alexei Pavlovschii

## Theory

Lexical analysis is the process of converting a sequence of characters into a sequence of **tokens** — the smallest meaningful units in a language. This process is a crucial first step in the interpretation or compilation of a programming language or domain-specific language (DSL). A lexer recognizes patterns like identifiers, numbers, strings, operators, IP addresses, and reserved keywords.

**Regular expressions** are commonly used to define patterns that identify these tokens. A lexer applies these expressions to the input text to match and extract tokens efficiently.

This lab work focuses on implementing a lexer using the **Pyparsing** library to tokenize a custom DSL designed for configuring network systems, which includes keywords, parameters, IP addresses, MAC addresses, and user-defined identifiers.

## Objectives

1. Understand lexical analysis and tokenization.
2. Learn how to build a lexer using `pyparsing`.
3. Recognize the importance of token ordering and pattern matching.
4. Implement a complete lexer that can tokenize a network-oriented DSL.

## Lexer Design and Implementation

### Step 1: Importing Required Classes from Pyparsing

```python
from pyparsing import (
    Word, alphas, alphanums, Regex, Keyword, Group, ZeroOrMore, nums,
    MatchFirst, ParseException, White
)
```
This block imports all the necessary tools for defining tokens using the `pyparsing` library.

- `Word` and `Regex` are used to define token patterns.
- `Keyword` is for reserved words.
- `MatchFirst` is used to prioritize token matching.
- `ParseException` is used to handle any unrecognized input.

---

### Step 2: Defining Token Patterns

```python
ID = Word(alphas + "_", alphanums + "_-" ).setName("ID")
```
Defines a generic identifier that starts with a letter or underscore and can include letters, digits, underscores, or hyphens.

```python
NUMBER = Word(nums).setName("NUMBER")
```
Matches any sequence of digits (e.g., 10, 300).

```python
STRING = Regex(r'"[^"]*"').setName("STRING")
```
Matches text inside double quotes.

```python
IPV4_ADDRESS = Regex(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}").setName("IPV4_ADDRESS")
```
Captures IPv4 addresses like `192.168.0.1` using regular expressions.

```python
MAC_ADDRESS = Regex(r"[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}").setName("MAC_ADDRESS")
```
Captures MAC addresses formatted as `abcd.ef12.3456`.

---

### Step 3: Declaring Keywords

```python
keyword_list = ["network", "device", "module", "slot", "interface", "vlan", "route", "dhcp",
    "acl", "link", "coordinates", "power", "gateway", "dns", "bandwidth",
    "allow", "deny", "from", "to", "pool", "name", "desc", "cable",
    "length", "functional", "static", "ip"]
```
List of DSL-specific reserved words.

```python
keywords = [(kw.upper(), Keyword(kw).setName(f"KEYWORD_{kw.upper()}")) for kw in keyword_list]
```
Converts each keyword to a case-sensitive parser and assigns a proper token name.

---

### Step 4: Ordering Tokens Correctly

```python
token_definitions = [
    ("IPV4_ADDRESS", IPV4_ADDRESS),
    ("MAC_ADDRESS", MAC_ADDRESS),
    ("STRING", STRING),
    ("NUMBER", NUMBER),
] + keywords + [
    ("ID", ID),
]
```
This is crucial. Specific patterns like IP and MAC must come **before** general patterns like ID to avoid false matches.

---

### Step 5: Building the Token Parser

```python
token_expr = MatchFirst([
    tok.setParseAction(lambda s, l, t, name=name: (name, t[0]))
    for name, tok in token_definitions
])
```
Creates a master expression that matches the first applicable token at each position and assigns a named tuple like `("KEYWORD_DEVICE", "device")`.

---

### Step 6: The Tokenizer Function

```python
def tokenize(text):
    pos = 0
    tokens = []
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text):
            break
        try:
            match = list(token_expr.scanString(text[pos:], maxMatches=1))
            if not match:
                raise ParseException(f"Unknown token at position {pos}")
            result, start, end = match[0]
            tokens.append(result[0])  # (TOKEN_TYPE, VALUE)
            pos += end
        except ParseException as pe:
            print(pe)
            break
    return tokens
```
This function walks through the input text:
- Skips whitespace
- Uses the master token expression to match the next valid token
- Returns a list of `(TOKEN_TYPE, VALUE)` tuples

---

### Step 7: Optional Block Parser

```python
def IndentedBlock(expr):
    return ZeroOrMore(Group(expr))
```
Unused in this lab, but useful for future cases where DSL supports grouped or indented blocks.

---

### Step 8: Example Usage

```python
if __name__ == "__main__":
    sample = '''
    device router1 interface eth0 ip 192.168.0.1
    mac 00ab.cd34.ef56 vlan 10 desc "Main uplink"
    '''

    result = tokenize(sample)
    for token in result:
        print(token)
```
Test string to demonstrate how the lexer works in action.

---

### Output

```python
(
 ('KEYWORD_DEVICE', 'device'),
 ('ID', 'router1'),
 ('KEYWORD_INTERFACE', 'interface'),
 ('ID', 'eth0'),
 ('KEYWORD_IP', 'ip'),
 ('IPV4_ADDRESS', '192.168.0.1'),
 ('KEYWORD_MAC', 'mac'),
 ('MAC_ADDRESS', '00ab.cd34.ef56'),
 ('KEYWORD_VLAN', 'vlan'),
 ('NUMBER', '10'),
 ('KEYWORD_DESC', 'desc'),
 ('STRING', '"Main uplink"')
)
```

## Conclusions / Results

This lab demonstrates the creation of a complete lexer for a network-oriented DSL using Pyparsing. The lexer handles various input types including keywords, identifiers, IPs, MACs, strings, and numbers, correctly recognizing their patterns through prioritized rules.

The experience shows how **lexical analysis** forms the foundational phase of any language processing system, and how **rule order**, **regex precision**, and **fallback strategies** like `ID` are essential for a robust implementation.

The full implementation is available in the `lexer.py` file, and its behavior is illustrated in the provided test input/output examples.

## Bibliography

[1] [Pyparsing Documentation](https://pyparsing-docs.readthedocs.io/)

[2] [Formal Language Theory](https://en.wikipedia.org/wiki/Formal_language)

[3] [Regular Expressions - Python Docs](https://docs.python.org/3/library/re.html)
