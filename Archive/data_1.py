from datetime import datetime
import teradata
from logging import info, warning, exception
import os

class Data:
    def __init__(self):
        self.message = ""
        self.user_credentials_valid, self.credentials_entry_chance, self.answerset, self.udaExec, self.connection_status = 0, 0, "", None, False
        self.teradata_username, self.teradata_password = "", ""
        self.combined_data = []
    
    def validate_data(self, insert_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        objects = insert_data.pop("Object").split(",")

        self.message = ""
        self.combined_data = []
        for obj in objects:
            combined_dict = {**insert_data, "Object": obj.strip(), "Timestamp": timestamp}
            self.combined_data.append(combined_dict)
            # self.message += ", ".join([f"{key}: {value}" for key, value in combined_dict.items()]) + "\n"
        
        self.teradata_username = insert_data.get("CID", self.teradata_username)
        self.teradata_password = insert_data.get("Password", self.teradata_password)

        self.connection_status = self.connect_teradata()
        if self.connection_status:
            self.insert_data()
        else:
            self.message += "Connect to Teradata failed. Please check your credentials and try again."

    def connect_teradata(self):
        '''
        Connect to Teradata using udaExec Function
        '''
        self.udaExec = teradata.UdaExec(appName="DB_Connect", version=1, logLevel="WARNING", logConsole=True)
        self.user_credentials_valid = 0
        # while self.user_credentials_valid == 0 and self.credentials_entry_chance < 3:
        try:
            with self.udaExec.connect(method="odbc", system="TDPREP01", Authentication="LDAP", username=self.teradata_username, password=self.teradata_password, driver="Teradata") as session:
                self.user_credentials_valid = 1
                self.connection_status = True
                self.session = session
                self.message += "Teradata Connection Successfully established with the credentials provided\n"
        except teradata.DatabaseError as db_error:
            self.credentials_entry_chance += 1
            self.message += f"Database error occurred: {str(db_error)}\n"
            self.message += f"\nAttempts remaining {3 - self.credentials_entry_chance}\n"
            self.log_error_to_file(f"DatabaseError: {str(db_error)}")
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
                self.message += "No attempts remaining.\n"
        return self.user_credentials_valid
    
    def insert_data(self):
        if not self.connection_status:
            self.message += "No existing connection. Attempting to reconnect to Teradata...\n"
            self.connection_status = self.connect_teradata()

            if not self.connection_status:
                self.message += "Cannot insert data because the connection to Teradata was not established"
                return
    
        table_name = "D1T_UTIL.IDL_LOAN_INVENTORY_TRACKER"
        try:
            with self.udaExec.connect(method="odbc", system="TDPREP01", Authentication="LDAP", username=self.teradata_username, password=self.teradata_password, driver="Teradata") as session:
                for data in self.combined_data:
                    obj = data["Object"]
                    # Validate the object
                    validation_query = f"SELECT * FROM D1V_GCFR.GCFR_PROCESS WHERE PROCESS_NAME LIKE '%{obj}%'"
                    is_valid_object = False
                    for row in session.execute(validation_query):
                        is_valid_object = True
                        break
                    
                    if not is_valid_object:
                        self.message += f"Object: '{obj}' is not a valid object\n"
                        continue

            
                    query = f"""
                    INSERT INTO {table_name} (CID, SPRINT, TEAM, SOURCE_SYSTEM, OBJECT_NAME, UPDATE_TS, MAP, STN, INP, TableUpdated, UpdateView, ReadView, PARAM, Stats) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    update_ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    session.execute(query, (
                        self.teradata_username,
                        data["Sprint"],
                        data["Team"],
                        data["Source_System"],
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
                    self.message += f"Data for Object: {data['Object']} inserted successfully.\n"
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
            (os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.join.isfile(os.path.join(folder_path, f))),
            key=os.path.getmtime
        )

        if len(log_files) > 30:
            files_to_delete = log_files[:-30]
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                except Exception as e:
                    continue