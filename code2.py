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