import tkinter as tk
from tkinter import ttk
from data import Data

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Tracker Login")

        # Set initial and minimum window size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        initial_width = screen_width
        initial_height = screen_height
        self.root.minsize(screen_width - 20, screen_height - 20)
        self.root.geometry(f'{initial_width}x{initial_height}')
        self.root.configure(background='#F8F9FA')

        self.font_size = 14  # Base font size
        self.checkbox_font_size = 10  # Smaller font size for checkboxes

        self.data_object = Data()
        self.checkbox_labels = ["Map", "STN", "INP", "OUT", "TABLE", "U-VIEW", "V-VIES", "GCFR"]
        self.create_login_widgets()

    def create_login_widgets(self):
        self.label = tk.Label(
            self.root, text="INVENTORY TRACKER TOOL", width=50,
            font=("TkHeadingFont", int(self.font_size * 1.5), "bold"), bg='#DEE2E6'
        )
        self.label.pack(pady=50)
        # Create CID and Password labels and entry boxes
        self.login_frame = tk.Frame(self.root, bg='#F8F9FA')
        self.login_frame.pack(pady=(10, 50))

        self.cid_label = tk.Label(self.login_frame, text="CID", font=("TkHeadingFont", self.font_size), bg='#DEE2E6')
        self.cid_label.grid(row=0, column=0, padx=20, pady=20)
        self.cid_entry = tk.Entry(self.login_frame, font=("TkHeadingFont", self.font_size), width=20)
        self.cid_entry.grid(row=0, column=1, padx=20, pady=20)

        self.password_label = tk.Label(self.login_frame, text="Password", font=("TkHeadingFont", self.font_size), bg='#DEE2E6')
        self.password_label.grid(row=1, column=0, padx=20, pady=40)
        self.password_entry = tk.Entry(self.login_frame, font=("TkHeadingFont", self.font_size), width=20, show='*')
        self.password_entry.grid(row=1, column=1, padx=20, pady=40)

        # Create InventoryUpdate and InventoryCount buttons
        self.button_frame = tk.Frame(self.root, bg='#F8F9FA')
        self.button_frame.pack(pady=(40, 150))

        self.update_button = tk.Button(self.button_frame, text="InventoryUpdate", font=("TkHeadingFont", self.font_size), command=self.inventory_update)
        self.update_button.grid(row=0, column=0, padx=100)

        self.count_button = tk.Button(self.button_frame, text="InventoryCount", font=("TkHeadingFont", self.font_size), command=self.inventory_count)
        self.count_button.grid(row=0, column=1, padx=100)

        # Create the message display area
        self.message_display = tk.Text(self.root, font=("TkHeadingFont", self.font_size), height=4, state=tk.DISABLED)
        self.message_display.pack(pady=(10, 40), padx=40, fill=tk.BOTH)

    def inventory_update(self):
        """Handle the InventoryUpdate button click event."""
        cid = self.cid_entry.get().strip()
        password = self.password_entry.get().strip()

        if not cid or not password:
            self.display_message("CID and Password cannot be empty.", "ERROR")
            return

        self.data_object.teradata_username = cid
        self.data_object.teradata_password = password

        connection_status = self.data_object.connect_teradata()

        if connection_status:
            self.display_message("Connection successful. Opening Inventory Tracker...", "INFO")
            self.open_inventory_tracker()
        else:
            self.display_message("Connection failed. Please check your credentials.", "ERROR")

    def inventory_count(self):
        """Handle the InventoryCount button click event."""
        cid = self.cid_entry.get().strip()
        password = self.password_entry.get().strip()

        if not cid or not password:
            self.display_message("CID and Password cannot be empty.", "ERROR")
            return
        
        self.data_object.teradata_username = cid
        self.data_object.teradata_password = password

        connection_status = self.data_object.connect_teradata()

        if connection_status:
            self.display_message("Connection successful. Opening Inventory Count...", "INFO")
            self.open_inventory_count()
        else:
            self.display_message("Connection failed. Please check your credentials.", "ERROR")

    def display_message(self, message, message_type="INFO"):
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete("1.0", tk.END)
        if message_type == "ERROR":
            message = "Error: " + message
        self.message_display.insert(tk.END, message)
        self.message_display.config(state=tk.DISABLED)

    def open_inventory_tracker(self):
        """Open the Inventory Tracker window after successful login."""
        self.login_frame.destroy()
        self.button_frame.destroy()
        self.message_display.destroy()

        # Create the old Inventory Tracker UI here
        self.root.title("Inventory Tracker")
        self.create_inventory_widgets()

    def open_inventory_count(self):
        """Open the Inventory Count window after successful login."""
        self.login_frame.destroy()
        self.button_frame.destroy()
        self.message_display.destroy()

        # Create the Inventory Count UI here
        self.root.title("Inventory Count")
        self.create_inventory_count_widgets()

    def create_inventory_widgets(self):
        # self.label = tk.Label(
        #     self.root, text="INVENTORY TRACKER TOOL", width=50,
        #     font=("TkHeadingFont", int(self.font_size * 1.5), "bold"), bg='#DEE2E6'
        # )
        # self.label.pack(pady=50)

        self.frame = tk.Frame(self.root, bg='#DEE2E6')
        self.frame.pack(pady=(10, 5), padx=20, fill=tk.BOTH, expand=True)
        self.initialize_frame_grid()
        self.initialize_entries_and_labels()
        self.initialize_checkbox_area()
        self.initialize_submit_and_message_display()

    def create_inventory_count_widgets(self):
        # Set up the Inventory Count UI
        # self.label = tk.Label(
        #     self.root, text="INVENTORY COUNT", width=50,
        #     font=("TkHeadingFont", int(self.font_size * 1.5), "bold"), bg='#DEE2E6'
        # )
        # self.label.pack(pady=50)

        self.frame = tk.Frame(self.root, bg='#DEE2E6')
        self.frame.pack(pady=(10, 5), padx=20, fill=tk.BOTH, expand=True)
        self.initialize_frame_grid()

        # Fetch values for dropdowns from the database
        release_values = self.data_object.fetch_values("Release", limit=10) 
        program_values = self.data_object.fetch_values("Program")
        object_values = self.checkbox_labels 

        # Creating dropdowns with labels
        tk.Label(self.frame, text="Release:", font=("TkHeadingFont", self.font_size), bg='#DEE2E6').grid(row=0, column=1, padx=(20, 20), pady=(40, 20), sticky=tk.W)
        tk.Label(self.frame, text="Program:", font=("TkHeadingFont", self.font_size), bg='#DEE2E6').grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky=tk.W)
        tk.Label(self.frame, text="Object:", font=("TkHeadingFont", self.font_size), bg='#DEE2E6').grid(row=2, column=1, padx=(20, 20), pady=(20, 40), sticky=tk.W)


        self.dropdown_release = ttk.Combobox(self.frame, values=release_values, font=("TkHeadingFont", self.font_size), state="readonly")
        self.dropdown_program = ttk.Combobox(self.frame, values=program_values, font=("TkHeadingFont", self.font_size), state="readonly")
        self.dropdown_object = ttk.Combobox(self.frame, values=object_values, font=("TkHeadingFont", self.font_size), state="readonly")


        self.dropdown_release.grid(row=0, column=2, pady=(40, 20))
        self.dropdown_program.grid(row=1, column=2, pady=(20, 20))
        self.dropdown_object.grid(row=2, column=2, pady=(20, 40))

        # self.initialize_submit_and_message_display()

        self.submit_button = tk.Button(self.frame, text="Submit", font=("TkHeadingFont", self.font_size), command=self.inventory_count_submit)
        self.submit_button.grid(row=4, column=0, columnspan=4, pady=(50, 40))

        self.message_display = tk.Text(self.frame, font=("TkHeadingFont", self.font_size), height=4, state=tk.DISABLED)
        self.message_display.grid(row=5, column=0, columnspan=4, pady=(50, 40), padx=20, sticky="ew")
        # Create the message display area
    
    def inventory_count_submit(self):
        release_value = self.dropdown_release.get()
        program_value = self.dropdown_program.get()
        object_value = self.dropdown_object.get()

        if not release_value:
            self.display_message("Release is a mandatory field.", "Error")
            return

        if program_value:
            result = self.data_object.query_database("Program", release_value, program_value)
        elif object_value:
            result = self.data_object.query_database("Object", release_value, object_value)
        else:
            result = self.data_object.query_database("Release", release_value)

        self.display_message(result, "INFO")

    def initialize_frame_grid(self):
        for i in range(4):
            self.frame.grid_columnconfigure(i, weight=1)
        self.frame.update_idletasks()

    def initialize_entries_and_labels(self):
        self.labels_texts = ["Sprint", "Release", "Team", "Program", "Env", "Source System", "Object"]
        self.entries = []
        self.sprint_values = self.load_data_from_file('Sprint.txt', "Sprint configuration file not found.")
        self.team_values = self.load_data_from_file('Team.txt', "Team configuration file not found.")
        self.source_systems = self.load_data_from_file('Source_System.txt', "Source System configuration file not found.")

        for i, text in enumerate(self.labels_texts):
            label = tk.Label(self.frame, text=text, font=("TkHeadingFont", self.font_size), bg='#CED4DA', width=15)
            entry = self.create_entry_widget(text)
            self.place_widgets_in_grid(i, label, entry)

    def create_entry_widget(self, label_text):
        if label_text == "Password":
            return tk.Entry(self.frame, font=("TkHeadingFont", self.font_size), width=20, show='*')
        elif label_text == "Sprint":
            entry = ttk.Combobox(self.frame, values=self.sprint_values, font=("TkHeadingFont", self.font_size), state="readonly")
            return entry
        elif  label_text == "Team":
            values = self.team_values
            entry = ttk.Combobox(self.frame, values=values, font=("TkHeadingFont", self.font_size))
            entry.bind('<KeyRelease>', lambda e: self.update_combobox_values(entry, values))
            entry.bind("<FocusOut>", lambda e, cb=entry: self.validate_combobox_selection(cb))
            return entry
        elif label_text == "Object":
            return tk.Text(self.frame, font=("TkHeadingFont", self.font_size), width=30, height=4)
        else:
            return tk.Entry(self.frame, font=("TkHeadingFont", self.font_size), width=20)

    def update_combobox_values(self, combobox, values):
        typed_value = combobox.get().lower()
        if typed_value == "":
            combobox['values'] = values
        else:
            filtered_values = [value for value in values if value.lower().startswith(typed_value)]
            combobox['values'] = filtered_values
        combobox.event_generate('<Down>')  # Automatically open the dropdown menu

    def validate_combobox_selection(self, combobox):
        value = combobox.get()
        if value not in self.team_values:
            combobox.set('')  # Clear the combobox if the value is not valid

    def place_widgets_in_grid(self, index, label, entry):
        if index < 4:  # Place first 5 fields on the left
            row = index + 1
            col = 0
        else:  # Place the rest on the right
            row = index - 3
            col = 2

        label.grid(row=row, column=col, padx=(50, 5), pady=30, sticky=tk.W)
        entry.grid(row=row, column=col+1, padx=(5, 50), pady=5, sticky=tk.EW)
        self.entries.append(entry)

    def initialize_checkbox_area(self):
        self.checkbox_frame = tk.Frame(self.frame, bg='#DEE2E6')
        self.checkbox_frame.grid(row=4, column=3, columnspan=4, padx=10, pady=(5, 5), sticky=tk.W)
        self.checkbox_vars = []

        for index, label in enumerate(self.checkbox_labels):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(
                self.checkbox_frame, text=label, variable=var,
                font=("TkHeadingFont", self.checkbox_font_size), bg='#DEE2E6'
            )
            checkbox.grid(row=index // 4, column=index % 4, padx=5, pady=5, sticky=tk.W)
            self.checkbox_vars.append(var)

    def initialize_submit_and_message_display(self):
        self.submit_button = tk.Button(self.frame, text="Submit", font=("TkHeadingFont", self.font_size), command=self.submit)
        self.submit_button.grid(row=5, column=0, columnspan=4, pady=(20, 10))
        self.message_display = tk.Text(self.frame, font=("TkHeadingFont", self.font_size), height=4, state=tk.DISABLED)
        self.message_display.grid(row=6, column=0, columnspan=4, pady=(30, 40), padx=40, sticky="ew")

    def load_data_from_file(self, file_name, error_message):
        try:
            with open(file_name, "r") as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            self.display_message(f"{error_message}\n", "ERROR")
            return []

    def submit(self):
        """Handle form submission by validating and processing data."""
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete("1.0", tk.END)  # Clear previous messages

        data = {}
        all_filled = True  # Track if all fields are filled

        for i, entry in enumerate(self.entries):
            content = entry.get("1.0", tk.END).strip() if isinstance(entry, tk.Text) else entry.get()
            if not content:
                self.display_message(f"'{self.labels_texts[i]}' field cannot be empty.\n", "ERROR")
                all_filled = False
                return 

            if self.labels_texts[i] != "Password":
                content = content.upper()

            if self.labels_texts[i] == "Source System" and content not in self.source_systems:
                self.display_message(f"'{content}' is not a valid source system.\n", "ERROR")
                all_filled = False
                return 

            data[self.labels_texts[i]] = content

        checkbox_values = {label: var.get() for label, var in zip(self.checkbox_labels, self.checkbox_vars)}
        if not any(checkbox_values.values()):
            self.display_message("At least one checkbox must be selected.\n", "ERROR")
            return

        if all_filled:
            self.data_object.validate_data(data)

    # Remaining methods would be similar to the ones in your original `InventoryTracker` class,
    # except for removing the CID and Password fields.

    # ...

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
