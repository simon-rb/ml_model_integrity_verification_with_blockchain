# The shutil module offers a number of high-level operations on files. In particular,
# functions are provided which support file copying and removal.
import shutil


# Backup the original model data
def backup_model_data():
    shutil.copy(src="model_data.json", dst="model_data_backup.json")
    print("Backup created as 'model_data_backup.json'.")


# Restore the model data from the backup
def restore_model_data():
    shutil.copy(src="model_data_backup.json", dst="model_data.json")
    print("Original model data restored as 'model_data.json'.")


# Uncomment one of these lines to perform the desired action:
backup_model_data()
# restore_model_data()
