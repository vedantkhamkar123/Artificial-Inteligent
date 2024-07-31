import tkinter as tk
from tkinter import messagebox
import random
import time

class NumberPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Puzzle Game")
        
        self.size = 3
        self.empty_tile = (self.size - 1, self.size - 1)
        self.board = self.create_puzzle()
        self.buttons = {}
        self.create_ui()

        # Automatically solve the puzzle
        self.solve_puzzle()

    def create_puzzle(self):
        """Create a solvable random puzzle"""
        numbers = list(range(self.size * self.size))
        random.shuffle(numbers)
        return [numbers[i * self.size:(i + 1) * self.size] for i in range(self.size)]

    def create_ui(self):
        # Create a frame for the puzzle and button
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configure the grid to resize with the window
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.frame.grid_rowconfigure(tuple(range(self.size)), weight=1)
        self.frame.grid_columnconfigure(tuple(range(self.size)), weight=1)
        
        self.update_ui()

    def update_ui(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        button_size = 1  # Button size is managed by grid layout

        for i in range(self.size):
            for j in range(self.size):
                tile_value = self.board[i][j]
                if tile_value != 0:
                    button = tk.Button(self.frame, text=str(tile_value), width=button_size, height=button_size,
                                       command=lambda i=i, j=j: self.move_tile(i, j))
                    button.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                    self.buttons[(i, j)] = button
                else:
                    self.empty_tile = (i, j)

    def move_tile(self, i, j):
        """Move the tile at (i, j) if possible"""
        empty_i, empty_j = self.empty_tile

        if (abs(empty_i - i) == 1 and empty_j == j) or (abs(empty_j - j) == 1 and empty_i == i):
            self.board[empty_i][empty_j], self.board[i][j] = self.board[i][j], self.board[empty_i][empty_j]
            self.empty_tile = (i, j)
            self.update_ui()
            if self.is_solved():
                messagebox.showinfo("Puzzle Solved", "Congratulations! You have solved the puzzle.")

    def is_solved(self):
        """Check if the puzzle is solved"""
        expected = list(range(1, self.size * self.size)) + [0]
        current = [self.board[i][j] for i in range(self.size) for j in range(self.size)]
        return expected == current

    def solve_puzzle(self):
        """Automatically solve the puzzle"""
        from collections import deque

        def get_blank_position(board):
            for i in range(self.size):
                for j in range(self.size):
                    if board[i][j] == 0:
                        return (i, j)
            return None

        def get_neighbors(board, blank_pos):
            i, j = blank_pos
            neighbors = []
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

            for di, dj in directions:
                ni, nj = i + di, j + dj
                if 0 <= ni < self.size and 0 <= nj < self.size:
                    new_board = [row[:] for row in board]
                    new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j]
                    neighbors.append((new_board, (ni, nj)))

            return neighbors

        def bfs_solve(start_board):
            queue = deque([(start_board, get_blank_position(start_board), [])])
            visited = set()
            visited.add(tuple(tuple(row) for row in start_board))

            while queue:
                current_board, blank_pos, path = queue.popleft()

                if self.is_solved():
                    return path

                for neighbor, new_blank_pos in get_neighbors(current_board, blank_pos):
                    neighbor_tuple = tuple(tuple(row) for row in neighbor)
                    if neighbor_tuple not in visited:
                        visited.add(neighbor_tuple)
                        queue.append((neighbor, new_blank_pos, path + [neighbor]))

            return None

        solution_path = bfs_solve(self.board)

        if not solution_path:
            messagebox.showinfo("No Solution", "No solution found for the current puzzle.")
            return

        self.play_solution(solution_path)

    def play_solution(self, path):
        """Animate the solution"""
        for board in path:
            self.board = board
            self.update_ui()
            self.root.update()
            time.sleep(1)  # Adjust the delay as needed

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Number Puzzle")
    root.geometry("500x500")  # Set an appropriate size for the window
    app = NumberPuzzle(root)
    root.mainloop()
