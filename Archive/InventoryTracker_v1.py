import tkinter as tk
from tkinter import ttk
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Tracker")
        
        # Set initial and minimum window size
        initial_width = int(self.root.winfo_screenwidth() * 0.8)
        initial_height = int(self.root.winfo_screenheight() * 0.8)
        self.root.minsize(800, 800)
        self.root.geometry(f'{initial_width}x{initial_height}')

        self.root.configure(background='#EDEDE9')
        # self.root.bind("<Escape>", self.quit_app)

        self.font_size = 14  # Base font size
        self.create_widgets()
        # self.root.bind("<Configure>", self.resize_widgets)

    def create_widgets(self):
        # Center label
        self.label = tk.Label(
            self.root, text="INVENTORY TRACKER TOOL", width=50, 
            font=("TkHeadingFont", int(self.font_size * 1.5), "bold"), bg='#CED4DA'
        )
        self.label.pack(pady=50)

        # Frame for input fields
        self.frame = tk.Frame(self.root, bg='#CED4DA')
        self.frame.pack(pady=50, padx=20, fill=tk.BOTH, expand=True)

        # Labels and entry fields
        self.labels_texts = ["CID", "Password", "Sprint", "Team", "Object"]
        self.entries = []

        # Define values for dropdowns
        self.sprint_values = ["21.1", "21.2", "21.3", "21.4", "22.1", "22.2", "22.3", "22.4", "23.1", "23.2"]
        self.team_values = ["Owl", "Cuckoo", "Humming", "Phoenix", "Kingfisher", "Raven"]

        # Create left side labels and entries (first 3)
        self.labels_entries = []
        for i, text in enumerate(self.labels_texts):
            label = tk.Label(self.frame, text=text, font=("TkHeadingFont", self.font_size), bg='#fff', anchor='w', width=10)
            if text == "Password":
                entry = tk.Entry(self.frame, font=("TkHeadingFont", int(self.font_size * 0.8)), width=20, show='*')
            elif text == "Sprint":
                entry = ttk.Combobox(self.frame, values=self.sprint_values, font=("TkHeadingFont", int(self.font_size * 0.8)), state="readonly")
                entry.current(0)  # set the default value
            elif text == "Team":
                entry = ttk.Combobox(self.frame, values=self.team_values, font=("TkHeadingFont", int(self.font_size * 0.8)))
                entry.bind("<KeyRelease>", lambda e, cb=entry: self.auto_complete(cb))
            elif text == "Object":
                entry = tk.Text(self.frame, font=("TkHeadingFont", int(self.font_size * 0.8)), width=30, height=4)  # Changed to Text widget
            else:
                entry = tk.Entry(self.frame, font=("TkHeadingFont", int(self.font_size * 0.8)), width=20)

            if i < 3:
                label.grid(row=i, column=0, padx=(50, 5), pady=30, sticky=tk.W)
                entry.grid(row=i, column=1, padx=(5, 250), pady=5, sticky=tk.W)
            else:
                label.grid(row=i-3, column=2, padx=(250, 5), pady=30, sticky=tk.W)
                entry.grid(row=i-3, column=3, padx=(5, 5), pady=5, sticky=tk.W) 

            self.entries.append(entry)
            self.labels_entries.append((label, entry))

        # Submit button
        self.submit_button = tk.Button(self.root, text="Submit", font=("TkHeadingFont", self.font_size, "bold"), command=self.submit, bg='#CED4DA')
        self.submit_button.pack(pady=(5, 40))  # Adjusted padding to move up

        # Message display box
        self.message_box = tk.Text(self.root, font=("TkHeadingFont", int(self.font_size * 0.8)), height=4, state=tk.DISABLED)
        self.message_box.pack(pady=20, padx=(5, 40), fill=tk.BOTH, expand=True)

        # Force layout update
        self.frame.update_idletasks()

    def submit(self):
        data = {f"{self.labels_texts[i]}": entry.get() if i != 4 else entry.get("1.0", tk.END).strip() for i, entry in enumerate(self.entries)}
        objects = data["Object"].split(",")
        del data["Object"]
        data['Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.message_box.config(state=tk.NORMAL)
        self.message_box.delete("1.0", tk.END)

        for obj in objects:
            combination = data.copy()
            combination["Object"] = obj.strip()
            self.message_box.insert(tk.END, str(combination) + "\n")

        self.message_box.config(state=tk.DISABLED)

    def auto_complete(self, combobox):
        value = combobox.get().strip().lower()
        if value == '':
            combobox['values'] = self.team_values
        else:
            filtered_values = [item for item in self.team_values if item.lower().startswith(value)]
            combobox['values'] = filtered_values
        combobox.event_generate('<Down>')  # open the dropdown menu to show the filtered values

    def resize_widgets(self, event):
        screen_width = self.root.winfo_width()
        screen_height = self.root.winfo_height()

        # Adjust font size based on window size
        adjusted_font_size = max(10, int(self.font_size * screen_height / 800))
        adjusted_heading_size = max(15, int(self.font_size * 1.5 * screen_height / 800))

        self.label.config(font=("TkHeadingFont", adjusted_heading_size, "bold"))

        for i, (label, entry) in enumerate(self.labels_entries):
            label.config(font=("TkHeadingFont", adjusted_font_size))
            entry.config(font=("TkHeadingFont", adjusted_font_size))

            if i < 3:
                label.grid_configure(padx=(max(10, int(screen_width * 0.05)), 5))
                entry.grid_configure(padx=(5, max(10, int(screen_width * 0.05))), pady=5)
            else:
                label.grid_configure(padx=(max(10, int(screen_width * 0.05)), 5))
                entry.grid_configure(padx=(5, max(10, int(screen_width * 0.05))), pady=5)

        # Adjust the submit button
        self.submit_button.config(font=("TkHeadingFont", adjusted_font_size))

    def quit_app(self, event=None):
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
