from datetime import datetime
import teradata
import os

class Data:
    def __init__(self):
        self.message = ""
        self.user_credentials_valid, self.credentials_entry_chance, self.answerset, self.udaExec, self.connection_status = 0, 0, "", None, False
        self.teradata_username, self.teradata_password = "", ""
        self.combined_data = []
        self.connection_status = False
        self.udaExec = teradata.UdaExec(appName="DB_Connect", version=1, logLevel="WARNING", logConsole=True)

    def connect_teradata(self):
        '''
        Connect to Teradata using udaExec Function
        '''
        try:
            self.message = ""
            with self.udaExec.connect(method="odbc", system="TDPREP01", Authentication="LDAP", username=self.teradata_username, password=self.teradata_password, driver="Teradata") as session:            
                self.connection_status = True
                self.session = session
                self.message += "Teradata Connection Successfully established with the credentials provided\n"
        except teradata.DatabaseError as db_error:
            self.credentials_entry_chance += 1
            self.message += f"Database error occurred: Incorrect ID and Password. Please check your credentials."
            self.message += f"\nAttempts remaining {3 - self.credentials_entry_chance}\n"
            self.log_error_to_file(f"Exception: {str(db_error)}")
            self.connection_status = False

            if self.credentials_entry_chance >= 3:
                self.message += "No attempts remaining.\n"
        except Exception as e:
            self.credentials_entry_chance += 1
            self.message += f"An unexpected error occurred: {str(e)}\n"
            
            self.message += f"\nAttempts remaining {3 - self.credentials_entry_chance}\n"
            self.log_error_to_file(f"Exception: {str(e)}")
            self.connection_status = False

            if self.credentials_entry_chance >= 3:
                self.message += "No attempts remaining. Restart the application.\n"
        return self.connection_status

    def validate_data(self, insert_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        raw_objects = insert_data.pop("Object", "")
        objects = [obj.strip() for obj in raw_objects.replace("\n", ",").split(",") if obj.strip()]

        self.message = ""
        self.combined_data = []
        self.existing_records = []
        self.new_records = []
        for obj in objects:
            obj_name = obj.strip()
            if not self.validate_object_in_gcfr(obj_name):
                self.message += f"Object: '{obj_name}' is not a valid object in GCFR_PROCESS\n"
                continue
            combined_dict = {**insert_data, "Object": obj.strip(), "Timestamp": timestamp}
            self.combined_data.append(combined_dict)
        if not self.combined_data:
            self.message += "No valid objects to process.\n"
            return True
        
        for record in self.combined_data:
            if self.check_existing_record(record):
                self.existing_records.append(record)
            else:
                self.new_records.append(record)
        
        if self.existing_records:
            self.message += "Some reocrds already exist:\n"
            for obj in self.existing_records:
                print("processing " + obj['Object'])
                self.message += f"Record found for Object {obj['Object']} inserted by {self.teradata_username} in " \
                    f"Sprint {obj['Sprint']} and Release {obj['Release']} by Team {obj['Team']}.\n"
            self.message += "If you want to update these records, please click Submit again.\n"
            return False
        else:
            print("processing: ", self.combined_data)
            self.insert_or_update_data(self.combined_data)
            return True
    
    def update_existing_data(self, insert_data):
        """Update the existing records if the user confirms and handle newly added objects"""

        self.message = ""
        if self.existing_records:
            self.insert_or_update_data(self.existing_records, update_existing=True)

        if self.new_records:
            self.insert_or_update_data(self.new_records, update_existing=False)

        # Check if any objects were added/removed between submits
        # Parse the current textbox input to get the updated list of objects
        raw_objects = insert_data.pop("Object", "")
        current_textbox_value = [obj.strip() for obj in raw_objects.replace("\n", ",").split(",") if obj.strip()]
        current_objects = [obj.strip() for obj in current_textbox_value.replace("\n", ",").split(",") if obj.strip()]

        # Identify objects that were added after the first submit
        newly_added_objects = [
            obj for obj in current_objects if obj not in [rec["Object"] for rec in self.existing_records]
        ]

        # Identify objects that were removed from the textbox
        removed_objects = [
            rec["Object"] for rec in self.existing_records if rec["Object"] not in current_objects
        ]

        # Handle newly added objects as new entries
        for obj_name in newly_added_objects:
            new_record = {
                "Object": obj_name,
                # Add other required fields for the new record here
                "Sprint": self.sprint_value,
                "Release": self.release_value,
                "Team": self.team_value
            }
            self.new_records.append(new_record)

        # Insert or update the new records
        if newly_added_objects:
            self.insert_or_update_data(self.new_records, update_existing=False)

        # Log any removed objects
        if removed_objects:
            self.message += f"The following objects were removed and will not be updated: {', '.join(removed_objects)}\n"

        if not self.existing_records and not self.new_records:
            self.message += "No records to update or insert.\n"

    
    def check_existing_record(self, record):
        """Check if records with the Same CID, Sprint, Release, Team and Object already exist."""
        try:
            with self.udaExec.connect(method="odbc", system="TDPREP01", Authentication="LDAP", username=self.teradata_username, password=self.teradata_password, driver="Teradata") as session:
                query = f"""
                SELECT * FROM D1F_UTIL.IDL_LOAN_INVENTORY_TRACKER WHERE CID = '{self.teradata_username.upper()}' AND SPRINT = '{record['Sprint']}' AND REL = '{record['Release']}' AND TEAM = '{record['Team']}' AND OBJECT_NAME = '{record['Object']}';
                """
                for row in session.execute(query):
                    return True
                return False
        except teradata.DatabaseError as db_error:
            self.message += f"Database error occurred during existing record check: {str(db_error)}\n"
        except Exception as e:
            self.message += f"An unexpected error occurred during existing record check: {str(e)}\n" 

    def validate_object_in_gcfr(self, obj_name):
        """Check if the object exists in the GCFR_PROCESS table."""
        try:
            with self.udaExec.connect(method="odbc", system="TDPREP01", Authentication="LDAP", username=self.teradata_username, password=self.teradata_password, driver="Teradata") as session:
                validation_query = f"SELECT * FROM D1V_GCFR.GCFR_PROCESS WHERE PROCESS_NAME = '{obj_name}'"
                for row in session.execute(validation_query):
                    return True
                return False
        except teradata.DatabaseError as db_error:
            self.message += f"Database error occurred during GCFR_PROCESS validation: {str(db_error)}\n"
        except Exception as e:
            self.message += f"An unexpected error occurred during GCFR_PROCESS validation: {str(e)}\n" 

    def insert_or_update_data(self, data, update_existing=False):
        if not self.connection_status:
            self.message += "No existing connection. Attempting to reconnect to Teradata...\n"
            self.connection_status = self.connect_teradata()

            if not self.connection_status:
                self.message += "Cannot insert data because the connection to Teradata was not established"
                return
    
        table_name = "D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER"
        try:
            with self.udaExec.connect(method="odbc", system="TDPREP01", Authentication="LDAP", username=self.teradata_username, password=self.teradata_password, driver="Teradata") as session:
                for obj in data:
                    update_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    if update_existing:
                        query = f"""
                        UPDATE {table_name}
                        SET UPDATE_TS = ?, MAPVIEW = ?, STNVIEW = ?, INPVIEW = ?, OUTVIEW = ?,
                        TABLEUPDATED = ?, V_VIEW = ?, V_VIEW = ?, GCFR = ?
                        WHERE CID = ? AND REL = ? AND SPRINT = ? AND TEAM = ? AND OBJECT_NAME = ?;
                        """

                        session.execute(query, (update_ts, obj["MAP"], obj["STN"], obj["INP"], obj["OUT"],
                                                obj["TABLE"], obj["U-VIEW"], obj["V-VIEW"], obj["GCFR"], 
                                                self.teradata_username.upper(), obj["Release"], obj["Sprint"], obj["Team"], obj["Object"]))
                        self.message += f"Data for Object: {obj['Object']} updated successfully.\n"
                        self.message = self.message.replace("Teradata Connection Successfully established with the credentials provided\n", "")
                    else:
                        query = f"""
                        INSERT INTO {table_name} (CID, SPRINT, TEAM, SOURCE_SYSTEM, OBJECT_NAME, UPDATE_TS, MAP, STN, INP, TableUpdated, UpdateView, ReadView, PARAM, Stats) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        session.execute(query, (
                            self.teradata_username.upper(),
                            data["Env"],
                            data["Program"],
                            data["Release"],
                            data["Sprint"],
                            data["Team"],
                            data["Source System"],
                            data["Object"],
                            update_ts,
                            data["MAP"],
                            data["STN"],
                            data["INP"],
                            data["Out"],
                            data["Table"],
                            data["U-VIEW"],
                            data["V-VIEW"],
                            data["GCFR"]
                        ))
                        self.message += f"Inserted data for Object: {data['Object']} successfully.\n"
                        self.message = self.message.replace("Teradata Connection Successfully established with the credentials provided\n", "")
                    self.check_and_delete_old_logs("DeployLogs")

        except teradata.DatabaseError as db_error:
            self.message += f"Database error occurred during data insertion: {str(db_error)}\n"
            self.log_error_to_file(str(db_error))
        except Exception as e:
            self.message += f"An unexpected error occurred during data insertion: {str(e)}\n"
            self.log_error_to_file(str(e))
    
    def getData(self):
        return self.message

    def log_error_to_file(self, error_message):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_folder = "DeployLogs"
        os.makedirs(log_folder, exist_ok=True)
        log_filename = f"TeradataError_{timestamp}.log"
        log_filepath = os.path.join(log_folder, log_filename)

        with open(log_filepath, "w") as log_file:
            log_file.write(f"Error occurred at {timestamp}\n")
            log_file.write(f"Error Details: {error_message}\n")

    def check_and_delete_old_logs(self, folder_path):
        log_files = sorted(
            (os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))),
            key=os.path.getmtime
        )

        if len(log_files) > 30:
            files_to_delete = log_files[:-30]
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                except Exception as e:
                    continue
    
    def fetch_values(self, field_name, limit=None):
        # SQL to fetch distinct values for specified field
        if limit and field_name=="Release":
            query = f"SELECT TOP {limit} REL (SELECT DISTINCT REL FROM D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER)  AS SubQuery ORDER BY REL DESC;"
        else:
            query = f"SELECT DISTINCT {field_name} FROM D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER ORDER BY {field_name}"
        try:
            with self.udaExec.connect(method="odbc", system="your_system", username=self.teradata_username, password=self.teradata_password) as session:
                result = session.execute(query)
                return [row[0] for row in result]
        except Exception as e:
            return []
    
    def query_database(self, label, release_value, value=None):
        # SQL based on label and value

        if label == "Release":
            query = f"SELECT COUNT(*) FROM D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER WHERE Release = '{release_value.upper()}'"
        elif label == "Program":
            query = f"SELECT COUNT(*) FROM D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER WHERE Program = '{value}' AND Release = '{release_value.upper()}'"
        elif label == "Object":
            if value == 'TABLE':
                value += 'UPDATED'
            elif value == 'U-VIEW' or value == 'V-VIEW':
                value = value.replace('-', '_')
            elif value != 'GCFR':
                value += 'VIEW'
            query = f"SELECT COUNT(DISTINCT Object) FROM D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER WHERE Release = '{release_value}'"

        try:
            with self.udaExec.connect(method="odbc", system="your_system", username=self.teradata_username, password=self.teradata_password) as session:
                result = session.execute(query)
                for row in result:
                    return f"{label} count: {row[0]}"
        except Exception as e:
            return "Failed to execute query."
        return ""