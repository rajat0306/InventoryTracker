import tkinter as tk
from tkinter import ttk

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Padding")

        # Frame for input fields
        self.frame = tk.Frame(self.root, bg='lightblue')
        self.frame.pack(pady=50, padx=20, fill=tk.BOTH, expand=True)

        # Label and entry with padding
        self.label = tk.Label(self.frame, text="Label", font=("TkHeadingFont", 14), bg='lightblue', anchor='w', width=12)
        self.entry = tk.Entry(self.frame, font=("TkHeadingFont", 12), width=20)

        # Apply padding
        self.label.grid(row=0, column=0, padx=(150, 5), pady=30, sticky=tk.W)  # Left margin of 50
        self.entry.grid(row=0, column=1, padx=(5, 50), pady=5, sticky=tk.W)  # Right margin of 50

        # Label and entry with padding
        self.label2 = tk.Label(self.frame, text="Label", font=("TkHeadingFont", 14), bg='lightblue', anchor='w', width=12)
        self.entry2 = tk.Entry(self.frame, font=("TkHeadingFont", 12), width=20)

        # Apply padding
        self.label2.grid(row=0, column=2, padx=(350, 5), pady=30, sticky=tk.W)  # Left margin of 50
        self.entry2.grid(row=0, column=3, padx=(5, 50), pady=5, sticky=tk.W)  # Right margin of 50

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()
