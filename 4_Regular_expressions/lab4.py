def generate_valid_strings():
    """
    Main function, generates all valid strings for Variant 4 REGEXs:
    1) (S|T)(U|V)W*Y+24
    2) L(M|N)O^3P*Q(2|3)
    3) R*S(T|U|V)W(X|Y|Z)^2
    repetition of '*' parts limited to 5 occurrences
    """

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

def sequence_processing(string):
    """
    Bonus point function. Shows how a given string is parsed according to:
    (S|T)(U|V)W*Y+24
    """
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

if __name__ == "__main__":
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
