import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Match")
        
        # 1. Setup Game Data
        self.emojis = ["🍎", "🍌", "🍒", "🍇", "🍉", "🍍", "🍓", "🥝"] * 2
        random.shuffle(self.emojis)
        
        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.matches = 0
        self.time_left = 60
        self.game_running = True
        
        # 2. Build UI
        self.timer_label = tk.Label(root, text=f"Time: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack(pady=10)
        
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack()
        
        for i in range(16):
            btn = tk.Button(self.grid_frame, text="?", width=6, height=3, font=("Arial", 20),
                           command=lambda idx=i: self.on_click(idx))
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
            self.buttons.append(btn)
            
        self.update_timer()

    def on_click(self, idx):
        # Prevent clicking already revealed cards or during a match check
        if not self.game_running or self.buttons[idx]['text'] != "?" or self.second_card is not None:
            return
            
        self.buttons[idx].config(text=self.emojis[idx], state="disabled")
        
        if self.first_card is None:
            self.first_card = idx
        else:
            self.second_card = idx
            self.root.after(600, self.check_match)

    def check_match(self):
        if self.emojis[self.first_card] == self.emojis[self.second_card]:
            self.buttons[self.first_card].config(bg="lightgreen")
            self.buttons[self.second_card].config(bg="lightgreen")
            self.matches += 1
            if self.matches == 8:
                self.end_game(True)
        else:
            self.buttons[self.first_card].config(text="?", state="normal")
            self.buttons[self.second_card].config(text="?", state="normal")
            
        self.first_card = None
        self.second_card = None

    def update_timer(self):
        if self.game_running and self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        elif self.time_left <= 0:
            self.end_game(False)

    def end_game(self, won):
        self.game_running = False
        msg = "🎉 You Won!" if won else "⏰ Time's Up!"
        messagebox.showinfo("Game Over", msg)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
