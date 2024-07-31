import tkinter as tk
from tkinter import messagebox

# DFS function to find all paths
def dfs_paths(graph, start, goal, path=None):
    if path is None:
        path = [start]
    if start == goal:
        yield path
    for next_node in graph[start] - set(path):
        yield from dfs_paths(graph, next_node, goal, path + [next_node])

# Tkinter application
class DFSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DFS Path Finder")

        # Graph input
        self.graph = {
            'A': {'B', 'C'},
            'B': {'A', 'D', 'E'},
            'C': {'A', 'F'},
            'D': {'B'},
            'E': {'B', 'F'},
            'F': {'C', 'E'}
        }

        # GUI components
        self.start_label = tk.Label(root, text="Start Node:")
        self.start_label.grid(row=0, column=0)
        self.start_entry = tk.Entry(root)
        self.start_entry.grid(row=0, column=1)

        self.goal_label = tk.Label(root, text="Goal Node:")
        self.goal_label.grid(row=1, column=0)
        self.goal_entry = tk.Entry(root)
        self.goal_entry.grid(row=1, column=1)

        self.find_button = tk.Button(root, text="Find Paths", command=self.find_paths)
        self.find_button.grid(row=2, column=0, columnspan=2)

        self.result_text = tk.Text(root, height=10, width=50)
        self.result_text.grid(row=3, column=0, columnspan=2)

    def find_paths(self):
        start = self.start_entry.get().strip()
        goal = self.goal_entry.get().strip()

        if start not in self.graph or goal not in self.graph:
            messagebox.showerror("Error", "Invalid start or goal node.")
            return

        paths = list(dfs_paths(self.graph, start, goal))
        self.result_text.delete(1.0, tk.END)
        if paths:
            for path in paths:
                self.result_text.insert(tk.END, f"Path: {' -> '.join(path)}\n")
        else:
            self.result_text.insert(tk.END, "No path found.")

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DFSApp(root)
    root.mainloop()
