import tkinter as tk
from tkinter import messagebox

class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Tower of Hanoi")

        # Canvas setup
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)

        # Initialize poles and disks
        self.poles = {"A": 100, "B": 300, "C": 500}
        self.disk_height = 20
        self.disk_width = [60, 50, 40]
        self.disk_color = ["red", "green", "blue"]
        self.disk_ids = []
        self.disk_positions = {"A": [], "B": [], "C": []}
        self.selected_disk = None
        self.move_count = 0
        self.max_moves = 15  # Set a limit for the maximum number of moves

        # Create UI elements
        self.create_poles()
        self.create_disks()
        self.create_labels()

        # Bind mouse click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def create_poles(self):
        for pole, x in self.poles.items():
            self.canvas.create_line(x, 350, x, 100, width=5)
            self.canvas.create_text(x, 360, text=pole, font=("Arial", 16, "bold"))

    def create_disks(self):
        self.disk_ids = []
        self.disk_positions = {"A": [], "B": [], "C": []}
        for i in range(3):
            x = self.poles["A"]
            y = 350 - (i + 1) * self.disk_height
            w = self.disk_width[i]
            disk_id = self.canvas.create_rectangle(x - w // 2, y, x + w // 2, y + self.disk_height,
                                                   fill=self.disk_color[i], tags="disk")
            self.disk_ids.append(disk_id)
            self.disk_positions["A"].append(disk_id)

    def create_labels(self):
        self.move_label = tk.Label(self.root, text=f"Moves left: {self.max_moves}")
        self.move_label.grid(row=1, column=0)

        self.instructions = tk.Label(self.root, text="Click on a disk to select it, then click on the target pole.")
        self.instructions.grid(row=1, column=1, columnspan=2)

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        clicked_disk = self.get_clicked_disk(x, y)
        to_pole = self.get_pole_from_coords(x)

        if clicked_disk:
            if self.selected_disk:
                # Attempt to move the selected disk
                if to_pole and self.is_valid_move(self.selected_disk, to_pole):
                    self.move_disk(self.selected_disk, to_pole)
                    self.move_count += 1
                    self.update_move_label()
                    if self.check_victory():
                        messagebox.showinfo("Congratulations!", "You have solved the Tower of Hanoi!")
                else:
                    messagebox.showerror("Invalid Move", "The move is not valid!")
                self.selected_disk = None
            else:
                # Select the disk if it's not already selected
                self.selected_disk = clicked_disk
        else:
            if self.selected_disk:
                # Attempt to move the selected disk to a pole
                if to_pole and self.is_valid_move(self.selected_disk, to_pole):
                    self.move_disk(self.selected_disk, to_pole)
                    self.move_count += 1
                    self.update_move_label()
                    if self.check_victory():
                        messagebox.showinfo("Congratulations!", "You have solved the Tower of Hanoi!")
                else:
                    messagebox.showerror("Invalid Move", "The move is not valid!")
                self.selected_disk = None

    def get_clicked_disk(self, x, y):
        for disk_id in reversed(self.disk_ids):
            coords = self.canvas.coords(disk_id)
            if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                return disk_id
        return None

    def get_pole_from_coords(self, x):
        for pole, pole_x in self.poles.items():
            if abs(x - pole_x) < 50:
                return pole
        return None

    def is_valid_move(self, disk_id, to_pole):
        from_pole = self.find_pole_of_disk(disk_id)
        if from_pole == to_pole:
            return False

        if not self.disk_positions[from_pole]:
            return False

        disk_index = self.disk_ids.index(disk_id)
        if self.disk_positions[to_pole] and self.disk_width[disk_index] > self.disk_width[self.disk_ids.index(self.disk_positions[to_pole][-1])]:
            return False

        return True

    def find_pole_of_disk(self, disk_id):
        for pole, disks in self.disk_positions.items():
            if disk_id in disks:
                return pole
        return None

    def move_disk(self, disk_id, to_pole):
        from_pole = self.find_pole_of_disk(disk_id)
        self.disk_positions[from_pole].remove(disk_id)
        self.disk_positions[to_pole].append(disk_id)
        x = self.poles[to_pole]
        y = 350 - len(self.disk_positions[to_pole]) * self.disk_height
        self.canvas.move(disk_id, x - self.canvas.coords(disk_id)[0] - self.disk_width[self.disk_ids.index(disk_id)] // 2, y - self.canvas.coords(disk_id)[1])
        self.canvas.update()

    def update_move_label(self):
        moves_left = self.max_moves - self.move_count
        self.move_label.config(text=f"Moves left: {moves_left}")
        if moves_left <= 0:
            messagebox.showinfo("Game Over", "You have run out of moves!")
            self.canvas.unbind("<Button-1>")

    def check_victory(self):
        return len(self.disk_positions["C"]) == 3

if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()
