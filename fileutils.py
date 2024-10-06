import datetime
import os
import status

CUSTOM_DATA_FILEPATH='data/'
USER_CONSUMPTION_FILEPATH='user/'

# Returns the filepath to the provided path string, relative to the script's directory.
def custom_filepath(path):
    path_directory = os.path.dirname(__file__)
    filepath = os.path.join(path_directory, CUSTOM_DATA_FILEPATH + path)
    return filepath

# Creates a directory path to dirpath if it does not already exist.
def instantiate_path_if_necessary(dirpath):
    if not os.path.exists(dirpath):
        try:
            os.makedirs(dirpath)
        except FileExistsError: #Dirpath exists betweeen check and create
            pass

# Returns the directory path to the user provided custom data, instantiating if necessary.
def user_consumption_dirpath():
    dirpath = custom_filepath(USER_CONSUMPTION_FILEPATH)
    instantiate_path_if_necessary(dirpath)
    return dirpath

# Converts the provided datetime object into a string formatted mm-dd-yyyy,
# optionally ending in a provided suffix.
def datetime_to_string(date, suffix=''):
    date_string = '{0}-{1}-{2}'.format(date.month, date.day, date.year)
    return date_string + suffix

# Securely replaces the previous_file with the contents of overwriting_file using a backup.
# Both filenames are relative to the custom_filepath root directory.
# Returns a Status indicating whether the operation succeeded.
def replace_file(previous_file, overwriting_file):
    try:
        os.rename(custom_filepath(previous_file), custom_filepath('backup.csv'))
        os.rename(custom_filepath(overwriting_file), custom_filepath(previous_file))
        os.remove(custom_filepath('backup.csv'))
        return status.Status(True)
    except Exception as error:
        return status.Status(False, error)