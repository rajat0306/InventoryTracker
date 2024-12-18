import tkinter as tk
from tkinter import ttk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Tracker")
        
        # Set initial and minimum window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        initial_width = screen_width
        initial_height = screen_height
        self.root.minsize(screen_width - 20, screen_height - 20)
        self.root.geometry(f'{initial_width}x{initial_height}')

        self.font_size = 14  # Base font size

        self.frame = tk.Frame(self.root, bg='darkgrey')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        # Configure grid columns to expand equally
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=0)
        self.frame.grid_columnconfigure(2, weight=1)

        # Center label
        self.label = tk.Label(
            self.frame, text="INVENTORY TRACKER TOOL", width=30, 
            font=("TkHeadingFont", int(self.font_size * 1.5), "bold"), bg='#CED4DA', anchor='center'
        )
        self.label.grid(row=0, column=1, pady=50, sticky='ew')

        # Labels and entry fields 
        self.labels_texts = ["CID", "Password", "Sprint", "Team", "Source System",  "Object"]
        self.entries = []

        # Define values for dropdowns
        self.sprint_values = ["21.1", "21.2", "21.3", "21.4", "22.1", "22.2", "22.3", "22.4", "23.1", "23.2"]
        self.team_values = ["Owl", "Cuckoo", "Humming", "Phoenix", "Kingfisher", "Raven"]

        # Create labels and entries
        for i, text in enumerate(self.labels_texts):
            label = tk.Label(self.frame, text=text, font=("TkHeadingFont", self.font_size), bg='#fff', width=15)
            entry = tk.Entry(self.frame, font=("TkHeadingFont", int(self.font_size * 0.8)), width=20)
            
            if text == "Password":
                entry.config(show='*')
            elif text == "Sprint":
                entry = ttk.Combobox(self.frame, values=self.sprint_values, font=("TkHeadingFont", int(self.font_size * 0.8)), state="readonly")
                entry.current(0)  # set the default value
            elif text == "Team":
                entry = ttk.Combobox(self.frame, values=self.team_values, font=("TkHeadingFont", int(self.font_size * 0.8)))
                entry.bind("<KeyRelease>", lambda e, cb=entry: self.auto_complete(cb))
            elif text == "Object":
                entry = tk.Text(self.frame, font=("TkHeadingFont", int(self.font_size * 0.8)), width=30, height=4)  # Changed to Text widget

# i 0 1 2 3 4 5
# r 1 2 3 1 2 3

            if i < 3:
                label.grid(row=i+1, column=0, padx=(50, 5), pady=10, sticky=tk.W)
                entry.grid(row=i+1, column=1, padx=(5, 50), pady=10, sticky=tk.W)
            else:
                label.grid(row=i-2, column=2, padx=(50, 5), pady=10, sticky=tk.W)
                entry.grid(row=i-2, column=3, padx=(5, 50), pady=10, sticky=tk.W)

            self.entries.append(entry)

    def auto_complete(self, combobox):
        value = combobox.get().strip().lower()
        if value == '':
            combobox['values'] = self.team_values
        else:
            filtered_values = [item for item in self.team_values if item.lower().startswith(value)]
            combobox['values'] = filtered_values
        combobox.event_generate('<Down>')  # open the dropdown menu to show the filtered values

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
