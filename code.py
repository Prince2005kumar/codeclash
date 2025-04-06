from datetime import datetime, timedelta

def calculate_earliest_date(n, y, d, absences):
    # Convert absences into datetime objects
    absence_periods = []
    for start, end in absences:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")
        absence_periods.append((start_date, end_date))
    
    # Sort absences by start date
    absence_periods.sort()
    
    # Calculate the total days required
    required_days = y * d
    
    # Start checking from the last date in the absences list
    last_absence_date = max(end for _, end in absence_periods)
    current_date = last_absence_date + timedelta(days=1)
    
    # Iterate backward to find the earliest date meeting the requirement
    while True:
        # Calculate the 5-year window
        start_window = current_date - timedelta(days=5 * 365)
        days_present = 0
        
        # Calculate days present in the 5-year window
        current = start_window
        for start, end in absence_periods:
            if end < start_window:
                continue
            if start > current_date:
                break
            if current < start:
                days_present += (start - current).days
            current = max(current, end + timedelta(days=1))
        
        # Add remaining days in the window
        if current <= current_date:
            days_present += (current_date - current).days + 1
        
        # Check if the days present meet the requirement
        if days_present >= required_days:
            return current_date.strftime("%Y-%m-%d")
        
        # Move to the next day
        current_date += timedelta(days=1)

# Input reading
n, y, d = map(int, input().split())
absences = [input().split() for _ in range(n)]

# Solve the problem
result = calculate_earliest_date(n, y, d, absences)
print(result)







#second problem 







from collections import deque

# Directions for moving up, down, left, right
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

def is_valid(x, y, board, visited):
    """Check if the cell is valid and unvisited."""
    return 0 <= x < 10 and 0 <= y < 10 and board[x][y] == 0 and not visited[x][y]

def bfs(start_x, start_y, board, visited):
    """Perform BFS to find the size of a hole."""
    queue = deque([(start_x, start_y)])
    visited[start_x][start_y] = True
    size = 0

    while queue:
        x, y = queue.popleft()
        size += 1

        # Explore all 4 directions
        for i in range(4):
            new_x, new_y = x + dx[i], y + dy[i]
            if is_valid(new_x, new_y, board, visited):
                visited[new_x][new_y] = True
                queue.append((new_x, new_y))

    return size

def find_holes(board):
    """Find all holes in the checkerboard and their sizes."""
    visited = [[False for _ in range(10)] for _ in range(10)]
    hole_sizes = []

    for i in range(10):
        for j in range(10):
            if board[i][j] == 0 and not visited[i][j]:
                # Start BFS for each unvisited white square
                hole_size = bfs(i, j, board, visited)
                hole_sizes.append(hole_size)

    return hole_sizes

# Input the checkerboard
print("Enter the 10x10 checkerboard (1 for black, 0 for white):")
board = []
for _ in range(10):
    row = list(map(int, input().split()))
    board.append(row)

# Find holes and their sizes
hole_sizes = find_holes(board)

# Output the results
print("Number of holes:", len(hole_sizes))
print("Sizes of holes:", " ".join(map(str, hole_sizes)))





#third problem




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