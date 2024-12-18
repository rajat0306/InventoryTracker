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

        #Create CID and Password labels and entry boxes
        self.login_frame = tk.Frame(self.root, bg='#F8F9FA')
        self.login_frame.pack(pady=(10, 40))

        self.cid_label = tk.Label(self.login_frame, text="CID", font=("TkHeadingFont", self.font_size), bg='#DEE2E6')
        self.cid_label.grid(row=0, column=0, padx=20, pady=20)
        self.cid_entry = tk.Entry(self.login_frame, font=("TkHeadingFont", self.font_size), width=20)
        self.cid_entry.grid(row=0, column=1, padx=20, pady=20)

        self.password_label = tk.Label(self.login_frame, text="Password", font=("TkHeadingFont", self.font_size), bg='#DEE2E6')
        self.password_label.grid(row=1, column=0, padx=20, pady=20)
        self.password_entry = tk.Entry(self.login_frame, font=("TkHeadingFont", self.font_size), width=20)
        self.password_entry.grid(row=1, column=1, padx=20, pady=20)

        # Create InventoryUpdate and InventoryCount buttons
        self.button_frame = tk.Frame(self.root, bg='#F8F8FA')
        self.button_frame.pack(pady=(40, 100))

        self.update_button = tk.Button(self.button_frame, text="Inventory Update", font=("TkHeadingFont", self.font_size), command=self.inventory_update)
        self.update_button.grid(row=1, column=0, padx=100)

        self.count_button = tk.Button(self.button_frame, text="Inventory Count", font=("TkHeadingFont", self.font_size), command=self.inventory_count)
        self.count_button.grid(row=1, column=1, padx=100)

        # Pre-fill saved CID and password from self.data_object
        if self.data_object.teradata_username:
            self.cid_entry.insert(0, self.data_object.teradata_username)

        if self.data_object.teradata_password:
            self.password_entry.insert(0, self.data_object.teradata_password)

        #Message Display Area
        self.message_display = tk.Text(self.root, font=("TkHeadingFont", self.font_size), height=4, state=tk.DISABLED)
        self.message_display.pack(pady=(10, 20), padx=40, fill=tk.BOTH)
    
    def inventory_update(self):
        """Handle the Inventory Update button click event."""
        cid = self.cid_entry.get().strip()
        password = self.password_entry.get().strip()

        if not cid or not password:
            self.display_message("CID and Password cannot be empty.", "ERROR")
            return

        self.data_object.teradata_username = cid
        self.data_object.teradata_password = password

        connection_status = self.data_object.connect_teradata()

        if not connection_status:
            message = self.data_object.getData()
            self.message_display.delete("1.0", tk.END)
            self.display_message(message, "ERROR")
            if self.data_object.credentials_entry_chance >= 3:
                self.update_button.config(state=tk.DISABLED)
                self.count_button.config(state=tk.DISABLED)
            else:
                self.open_inventory_tracker()
    
    def inventory_count(self):
        """Handle the Inventory Count button click event."""
        cid = self.cid_entry.get().strip()
        password = self.password_entry.get().strip()

        if not cid or not password:
            self.display_message("CID and Password cannot be empty.", "ERROR")
            return
        
        self.data_object.teradata_username = cid
        self.data_object.teradata_password = password

        connection_status = self.data_object.connect_teradata()

        if not connection_status:
            message = self.data_object.getData()
            self.message_display.delete("1.0", tk.END)
            self.display_message(message, "ERROR")
            if self.data_object.credentials_entry_chance >= 3:
                self.update_button.config(state=tk.DISABLED)
                self.count_button.config(state=tk.DISABLED)
            else:
                self.open_inventory_count()
    
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

        #Create the Inventory Tracker UI
        self.root.title("Inventory Update")
        self.create_inventory_update_widgets()
    
    def open_inventory_count(self):
        """Open the Inventory Count window after successful login."""
        self.login_frame.destroy()
        self.button_frame.destroy()
        self.message_display.destroy()

        #Create the Inventory Tracker UI
        self.root.title("Inventory Update")
        self.create_inventory_count_widgets()

    def go_back_to_login(self):
        """Destroy the current screen and return to the login screen with pre-filled credentials."""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_login_widgets()

    def create_inventory_update_widgets(self):
        self.frame = tk.Frame(self.root, bg='#DEE2E6')
        self.frame.pack(pady=(10, 5), padx=20, fill=tk.BOTH, expand=True)
        self.initialize_frame_grid()
        self.initialize_entries_and_labels()
        self.initialize_checkbox_area()
        self.initialize_submit_and_message_display()
    
    def create_inventory_count_widgets(self):
        self.frame = tk.Frame(self.root, bg='#DEE2E6')
        self.frame.pack(pady=(10, 5), padx=20, fill=tk.BOTH, expand=True)
        self.initialize_frame_grid()

        #Fetch values for dropdowns from the database
        release_values = self.data_object.fetch_values("Release", limit=10)
        program_values = ['None'] + self.data_object.fetch_values("Program")
        object_values = ['None'] + self.checkbox_labels

        #Creating dropdown with labels
        tk.Label(self.frame, text="Release", font=("TkHeadingFont", self.font_size), bg='#DEE2E6').grid(row=0, column=1, padx=20, pady=(30, 20), sticky=tk.W)
        tk.Label(self.frame, text="Program", font=("TkHeadingFont", self.font_size), bg='#DEE2E6').grid(row=1, column=1, padx=20, pady=(30, 20), sticky=tk.W)
        tk.Label(self.frame, text="Object", font=("TkHeadingFont", self.font_size), bg='#DEE2E6').grid(row=2, column=1, padx=20, pady=(30, 20), sticky=tk.W)

        self.dropdown_release = ttk.Combobox(self.frame, values=release_values, font=("TkHeadingFont", self.font_size), state="readonly")
        self.dropdown_program = ttk.Combobox(self.frame, values=program_values, font=("TkHeadingFont", self.font_size), state="readonly")
        self.dropdown_object = ttk.Combobox(self.frame, values=object_values, font=("TkHeadingFont", self.font_size), state="readonly")

        self.dropdown_release.grid(row=0, column=2, padx=20, pady=(30, 20))
        self.dropdown_program.grid(row=1, column=2, padx=20, pady=(30, 20))
        self.dropdown_object.grid(row=2, column=2, padx=20, pady=(30, 20))

        # Bind the program and object dropdowns to reset the other when one is selected
        self.dropdown_program.bind("<<ComboboxSelected>>", self.reset_object_on_program_select)
        self.dropdown_object.bind("<<ComboboxSelected>>", self.reset_program_on_object_select)

        self.submit_button = tk.Button(self.frame, text="Submit", font=("TkHeadingFont", self.font_size), command=self.inventory_count_submit)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=(40, 30))
        
        self.back_button = tk.Button(self.frame, text="Back", font=("TkHeadingFont", self.font_size), command=self.go_back_to_login, bg='#CED4DA')
        self.back_button.grid(row=4, column=1, columnspan=2, pady=10)

        self.message_display = tk.Text(self.frame, font=("TkHeadingFont", self.font_size), height=4, state=tk.DISABLED)
        self.message_display.grid(row=5, column=0, columnspan=4, pady=(40, 30), padx=20, sticky="ew")
    
    def reset_object_on_program_select(self, event):
        """Reset the object dropdown when program is selected."""
        selected_program = self.dropdown_program.get()
        if selected_program != "None":
            self.dropdown_object.set("None")

    def reset_program_on_object_select(self, event):
        """Reset the program dropdown when object is selected."""
        selected_object = self.dropdown_object.get()
        if selected_object != "None":
            self.dropdown_program.set("None")

    def inventory_count_submit(self):
        release_value = self.dropdown_release.get()
        program_value = self.dropdown_program.get()
        object_value = self.dropdown_object.get()

        if not release_value:
            self.display_message("Release is a mandatory field.", "ERROR")
            return
        
        if program_value == "None":
            program_value = None
        if object_value == "None":
            object_value = None

        if program_value and not object_value:
            result = self.data_object.query_database("Program", release_value, program_value)
        elif object_value and not program_value:
            result = self.data_object.query_database("Object", release_value, object_value)
        else:
            result = self.data_object.query_database("Release", release_value)

        i = result.index(':')
        count = result[i+1:].strip()
        if "Program" in result:
            message = f"The count of Objects for Program {program_value} in Release {release_value} is {count}."
        elif "Object" in result:
            message = f"The count of {object_value} Objects in Release {release_value} is {count}."
        else:
            message = f"The count of Objects in Release {release_value} is {count}."
        self.display_message(message,"INFO")

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
        self.release_values = ['Future Release','R25.1', 'R25.2', 'R25.3', 'R25.4', 'R25.5', 'R25.6', 'R25.7', 'R25.8', 'R25.9', 'R25.10', 'R25.11']

        for i, text in enumerate(self.labels_texts):
            label = tk.Label(self.frame, text=text, font=("TkHeadingFont", self.font_size), bg='#CED4DA', width=15)
            entry = self.create_entry_widget(text)
            self.place_widgets_in_grid(i, label, entry)

    def create_entry_widget(self, label_text):
        if label_text == "Sprint":
            entry = ttk.Combobox(self.frame, values=self.sprint_values, font=("TkHeadingFont", self.font_size), state="readonly")
            return entry
        elif label_text == "Team":
            values = self.team_values
            entry = ttk.Combobox(self.frame, values=values, font=("TkHeadingFont", self.font_size))
            entry.bind('<KeyRelease>', lambda e: self.update_combobox_values(entry, values))
            entry.bind("<FocusOut>", lambda e, cb=entry: self.validate_combobox_selection(cb))
            return entry
        elif label_text == "Object":
            return tk.Text(self.frame, font=("TkHeadingFont", self.font_size), width=30, height=4)
        elif label_text == "Release":
            return ttk.Combobox(self.frame, values=self.release_values, font=("TkHeadingFont", self.font_size), state="readonly")
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
        if index < 4: 
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
        self.submit_button = tk.Button(self.frame, text="Submit", font=("TkHeadingFont", self.font_size), command=self.submit, bg='#CED4DA')
        self.submit_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.back_button = tk.Button(self.frame, text="Back", font=("TkHeadingFont", self.font_size), command=self.go_back_to_login, bg='#CED4DA')
        self.back_button.grid(row=5, column=1, columnspan=2, pady=10)
        self.message_display = tk.Text(self.frame, font=("TkHeadingFont", self.font_size), height=4, state=tk.DISABLED)
        self.message_display.grid(row=6, column=0, columnspan=4, pady=(10, 40), padx=40, sticky="ew")

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
        self.frame.update_idletasks()

        data = {}
        all_filled = True  # Track if all fields are filled

        for i, entry in enumerate(self.entries):
            content = entry.get("1.0", tk.END).strip() if isinstance(entry, tk.Text) else entry.get()
            if not content:
                self.display_message(f"Error: '{self.labels_texts[i]}' field cannot be empty.\n", "ERROR")
                all_filled = False
                return 

            content = content.upper()

            if self.labels_texts[i] == "Source System" and content not in self.source_systems:
                self.display_message(f"'{content}' is not a valid source system.\n", "ERROR")
                all_filled = False
                return 

            data[self.labels_texts[i]] = content

        checkbox_values = {label: var.get() for label, var in zip(self.checkbox_labels, self.checkbox_vars)}
        if not any(checkbox_values.values()):
            self.display_message("Error: At least one checkbox must be selected.\n", "ERROR")
            return
        data.update(checkbox_values)

        if all_filled:
            confirm_needed = self.data_object.validate_data(data)
            if confirm_needed is False:
                self.display_message(self.data_object.message, "INFO")
                self.submit_button.config(command=self.update_existing_records(data))
            else:
                self.display_message(self.data_object.message, "INFO")

    def update_existing_records(self, data):
        self.message_display.config(state=tk.NORMAL)
        self.message_display.delete("1.0", tk.END)

        # Proceed with data update
        self.data_object.update_existing_data(data)

        message = self.data_object.getData()
        self.display_message(message, "INFO")

        self.submit_button.config(command=self.submit)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()