def decode_barcode(case_number, m, bar_widths):
    # Encoding table for Code-11
    encoding_table = {
        "0": "00001", "1": "10001", "2": "01001", "3": "11000",
        "4": "00101", "5": "10100", "6": "01100", "7": "00011",
        "8": "10010", "9": "10000", "-": "00100", "start/stop": "00110"
    }
    reverse_table = {v: k for k, v in encoding_table.items()}  # Reverse lookup table

    # Normalize bar widths to narrow (0) or wide (1)
    narrow_width = min(bar_widths)
    wide_width = max(bar_widths)
    normalized = ["1" if width > (narrow_width + wide_width) / 2 else "0" for width in bar_widths]

    # Group into characters (5 bars per character)
    if len(normalized) % 5 != 0:
        print(f"Case {case_number}: bad code")
        return

    characters = ["".join(normalized[i:i + 5]) for i in range(0, len(normalized), 5)]

    # Decode characters
    decoded = []
    for char in characters:
        if char in reverse_table:
            decoded.append(reverse_table[char])
        else:
            print(f"Case {case_number}: bad code")
            return

    # Validate start/stop characters
    if decoded[0] != "start/stop" or decoded[-1] != "start/stop":
        print(f"Case {case_number}: bad code")
        return

    # Remove start/stop characters
    decoded = decoded[1:-1]

    # Validate C check character
    if len(decoded) < 2:
        print(f"Case {case_number}: bad code")
        return

    c_check = decoded[-2]
    k_check = decoded[-1]
    message = decoded[:-2]

    # Compute C check character
    weights = list(range(1, 11))  # Weights for C check
    c_weighted_sum = sum((weights[(len(message) - i - 1) % 10] * int(encoding_table[message[i]])) for i in range(len(message)))
    computed_c_check = c_weighted_sum % 11

    if str(computed_c_check) != c_check:
        print(f"Case {case_number}: bad C")
        return

    # Compute K check character
    weights = list(range(1, 11))  # Weights for K check
    k_weighted_sum = sum((weights[(len(message) + 1 - i - 1) % 9] * int(encoding_table[message[i]])) for i in range(len(message) + 1))
    computed_k_check = k_weighted_sum % 11

    if str(computed_k_check) != k_check:
        print(f"Case {case_number}: bad K")
        return

    # If everything is valid, print the decoded message
    print(f"Case {case_number}: {''.join(message)}")


def main():
    case_number = 1
    while True:
        m = int(input())
        if m == 0:
            break

        bar_widths = list(map(int, input().split()))
        decode_barcode(case_number, m, bar_widths)
        case_number += 1


if __name__ == "__main__":
    main()