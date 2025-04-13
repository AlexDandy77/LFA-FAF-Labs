# Regular Expressions

### Course: Formal Languages & Finite Automata

### Author: Alexei Pavlovschii

## Theory

Regular expressions (regex) are a formal method for describing patterns in strings. They are used to search, match, and manipulate text in a wide variety of applications including lexical analysis, data validation, and text processing. In the context of formal languages, regular expressions describe regular languages and serve as the basis for designing finite automata.

## Objectives

1. Explain what regular expressions are and their practical applications.
2. Generate valid combinations of symbols that conform to specified regular expressions.
3. Implement a code solution that produces all valid strings for given regular expressions, with a repetition limit of 5 for unbounded parts.
4. **Bonus:** Develop a function to demonstrate the step-by-step processing of a regular expression.

## Regular Expressions

### Variant 4

For Variant 4, the following three complex regular expressions were considered:

1. **Expression 1:** `(S|T)(U|V)W*Y+24`  
   - **(S|T):** The first character is either `S` or `T`.
   - **(U|V):** The second character is either `U` or `V`.
   - **W\*:** Zero or more occurrences of `W` (limited to 5 repetitions).
   - **Y+:** At least one occurrence of `Y` (limited to 5 repetitions).
   - **24:** The literal substring `24` at the end.

2. **Expression 2:** `L(M|N)O^3P*Q(2|3)`  
   - **L:** A literal `L`.
   - **(M|N):** Either `M` or `N`.
   - **O^3:** Exactly three occurrences of `O`.
   - **P\*:** Zero or more occurrences of `P` (limited to 5 repetitions).
   - **Q:** A literal `Q`.
   - **(2|3):** Either `2` or `3`.

3. **Expression 3:** `R*S(T|U|V)W(X|Y|Z)^2`  
   - **R\*:** Zero or more occurrences of `R` (limited to 5 repetitions).
   - **S:** A literal `S`.
   - **(T|U|V):** Either `T`, `U`, or `V`.
   - **W:** A literal `w`.
   - **(X|Y|Z)^2:** Exactly two characters, each chosen from `x`, `y`, or `z`.

## Implementation
### Step 1: Function of generating valid strings
```python
def generate_valid_strings():
    # 1. (S|T)(U|V)W*Y+24
    first_part = []
    for first_letter in ['S', 'T']:
        for second_letter in ['U', 'V']:
            for w_count in range(6):
                for y_count in range(1, 6):
                    w_part = 'W' * w_count
                    y_part = 'Y' * y_count
                    combo = f"{first_letter}{second_letter}{w_part}{y_part}24"
                    first_part.append(combo)

    # 2) L(M|N)O^3P*Q(2|3)
    second_part = []
    for letter in ['M', 'N']:
        for p_count in range(3):
            p_part = 'P' * p_count
            for digit in ['2', '3']:
                combo = f"L{letter}000{p_part}Q{digit}"
                second_part.append(combo)

    # 3) R*S(T|U|V)W(X|Y|Z)^2
    third_part = []
    xyz_pairs = []
    for c1 in ['X', 'Y', 'Z']:
        for c2 in ['X', 'Y', 'Z']:
            xyz_pairs.append(c1 + c2)

    for r_count in range(6):
        r_part = 'R' * r_count

        for middle_letter in ['T', 'U', 'V']:
            for pair in xyz_pairs:
                combo = f"{r_part}S{middle_letter}W{pair}"
                third_part.append(combo)
    
    return first_part, second_part, third_part
```
The main function defines regexes and using for cycles makes combinations of letters and registers number of occurrencies. It then combines letters and attaches the word to a list for storing.

### Step 2: Bonus point function. 
```python
def sequence_processing(string):
    explanation = []
    idx = 0

    # Step 1: (S|T)
    if len(string) < 1 or string[0] not in ['S', 'T']:
        return "Does not match step 1"
    explanation.append(f"Step 1: Matched '{string[0]}' as (S|T)")
    idx += 1

    # Step 2: (U|V)
    if len(string) < 2 or string[1] not in ['U', 'V']:
        return "Does not match step 2"
    explanation.append(f"Step 2: Matched '{string[1]}' as (U|V)")
    idx += 1

    # Step 3: W*
    w_count = 0
    while idx < len(string) and string[idx] == 'W':
        w_count += 1
        idx += 1
    explanation.append(f"Step 3: Matched 'W' repeated {w_count} times")

    # Step 4: Y+
    y_count = 0
    while idx < len(string) and string[idx] == 'Y':
        y_count += 1
        idx += 1
    if y_count < 1:
        return "Does not match step 4"
    explanation.append(f"Step 4: Matched 'Y' repeated {y_count} times")

    # Step 5: 24
    if idx + 2 <= len(string) and string[idx:idx + 2] == '24':
        explanation.append("Step 5: Matched '24'")
        idx += 2
    else: return "Does not match step 5"

    # Final check
    if idx == len(string):
        explanation.append("String fully matched expression 1!")
    else: explanation.append("String has extra chars beyond the pattern.")

    return "\n".join(explanation)
```
The bonus point functions shows step by step how a given string is parsed according to: (S|T)(U|V)W*Y+24. If any mismatches occur, function returns what exactly misses. If a string matches til the end, but has some more symbols, the respective message is printed to user.

### Step 3: Testing
```python
p1, p2, p3 = generate_valid_strings()
print("===== Expression 1 matches =====")
for s in p1[:10]: # last 10 elements
    print(s)
print("Total count", len(p1))

print("\n===== Expression 2 matches =====")
for s in p2[:10]:  # last 10 elements
    print(s)
print("Total count", len(p2))

print("\n===== Expression 3 matches =====")
for s in p3[:10]:  # last 10 elements
    print(s)
print("Total count", len(p3))

print("\n===== Bonus point test string =====")
test_string = input("Enter test string for expression 1 (ex. SUWWYY24): ")
print(sequence_processing(test_string))
```
The testing code calls main function and for every three regexes displays the last 10 valid strings generated by loops. Total count of elements in the list is displayed. The bonus task returns explanations and prints every step of string validating.

## Output
### 1. Main function piece of code:
```
===== Expression 1 matches =====
SUY24
SUYY24
SUYYY24
SUYYYY24
SUYYYYY24
SUWY24
SUWYY24
SUWYYY24
SUWYYYY24
SUWYYYYY24
Total count 120
```
### 2. Bonus task:
```
===== Bonus point test string =====
Enter test string for expression 1 (ex. SUWWYY24): SUWWYY241
Step 1: Matched 'S' as (S|T)
Step 2: Matched 'U' as (U|V)
Step 3: Matched 'W' repeated 2 times
Step 4: Matched 'Y' repeated 2 times
Step 5: Matched '24'
String has extra chars beyond the pattern.
```

## Conclusions / Results

This lab demonstrates the generation of valid strings based on complex regular expressions. The implementation covers three different expressions by generating combinations that conform to the given patterns, while enforcing a repetition limit of 5 for unbounded sections and ensuring minimum occurrences where required (e.g., at least one `Y` in Expression 1). Additionally, a bonus function illustrates the step-by-step matching process for one of the expressions, thereby deepening the understanding of how regular expressions are applied in practice.

The approach highlights the importance of precise regex design, controlled repetition to avoid combinatorial explosion, and the value of a systematic process for matching and validation. The complete solution and its behavior are detailed in the provided code examples.

## Bibliography

[1] [Regular Expressions - Python Docs](https://docs.python.org/3/library/re.html)

[2] [Formal Language Theory](https://en.wikipedia.org/wiki/Formal_language)

[3] [Regular Expressions Tutorial](https://www.regular-expressions.info/)
