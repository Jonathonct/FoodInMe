import datetime
import fileutils
import food_item
import os
import status

PREEXISTING_ITEM='preexisting item'
CUSTOM_FOOD_ITEM_FILENAME='custom_foods.csv'

# If the custom food file does not already exist, create it and fill out the first CSV line.
def instantiate_custom_food_file_if_necessary():
    dirpath = fileutils.custom_filepath('')
    fileutils.instantiate_path_if_necessary(dirpath)
    if not os.path.exists(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME)):
        with open(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME), 'w') as file_output:
            file_output.write(food_item.CSV_HEADER + '\n')

# Performs a simple linear search through the custom food name file searching
# for whether the food item with the given food_name has already been added.
def food_item_already_added(food_name):
    if not os.path.exists(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME)):
        return False
    with open(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME), 'r') as file_input:
        for line in file_input:
            if line.split(',')[0] == food_name:
                file_input.close()
                return True
    return False

# Simply adds the provided food item to the bottom of the existing custom food item file.
def add_food_item(fooditem):
    instantiate_custom_food_file_if_necessary()
    with open(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME), 'a') as file_output:
        file_output.write(fooditem.to_csv() + '\n')
    return status.Status(True)

# Replaces the provided food item within the custom food name file to use the new values.
# If the food item does not already exist, this does nothing.
def replace_food_item(fooditem):
    if not os.path.exists(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME)):
        return status.Status(False, 'List of food items cannot be found. Add food items with the "add-food" command.')
    added = False
    with open(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME), 'r') as file_input:
        with open(fileutils.custom_filepath('temp.csv'), 'w') as file_output:
            for line in file_input:
                if line.split(',')[0] == fooditem.name:
                    added = True
                    file_output.write(fooditem.to_csv() + '\n')
                else:
                    file_output.write(line)
    if not added:
        return status.Status(False, 'Food item {0} was not found and could not be replaced.'.format(fooditem.name))
    return fileutils.replace_file(CUSTOM_FOOD_ITEM_FILENAME, 'temp.csv')
        
# Stores that the given amount of food was consumed by the user in a file matching the date string.
def process_food_eaten(fooditem, consumed_percent, consumed_date_filename):
    multiplier = float(consumed_percent) / 100.0
    output_str = fooditem.name
    output_str += ',' + str(fooditem.calories() * multiplier)
    output_str += ',' + str(fooditem.carbs() * multiplier)
    output_str += ',' + str(fooditem.fats() * multiplier)
    output_str += ',' + str(fooditem.proteins() * multiplier) + '\n'
    dirpath = fileutils.user_consumption_dirpath()
    with open(dirpath + consumed_date_filename, 'a') as output:
        output.write(output_str)
        
# Searches through the list of known food items for the one corresponding to the given food_name.
# Returns it if it can be found or a None object otherwise.    
def try_get_food_item(food_name):
    if not os.path.exists(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME)):
        return None
    with open(fileutils.custom_filepath(CUSTOM_FOOD_ITEM_FILENAME), 'r') as file_input:
        for line in file_input:
            if line.split(',')[0] == food_name:
                fooditem = food_item.parse_food_item(line, ',')
                file_input.close()
                return fooditem
    return None
    

### ---------------------------------- PUBLIC functions ---------------------------------------------- ###

# Attempts to parse the provided `food_item_text` into a food item. If successful, and the food item
# does not already exist, it will be added to the file. If it already exists, an error will be returned
# unless `overwrite` is true, in which case the new values will be used instead.
def try_add_food_item(food_item_text, overwrite=False):
    fooditem = food_item.parse_food_item(food_item_text, '-')
    if fooditem is None:
        return status.Status(False, 'Failed to parse "{0}" as a food item. Type "help add-food" to learn usage.'.format(food_item_text))
    if food_item_already_added(fooditem.name):
        if not overwrite:
            return status.Status(False, PREEXISTING_ITEM)
        return replace_food_item(fooditem)
    return add_food_item(fooditem)

# Records the percent of the given food item as being consumed on the provided day.
# Returns False if food_name is not in the food name file, the percent is not a positive number
# or if the date is invalid (expected datetime.date)
def try_process_food_eaten(food_name, consumed_percent, consumed_date):
    if consumed_percent < 0:
        return status.Status(False, 'Invalid consumed_percentage: {0}'.format(consumed_percent))
    if not isinstance(consumed_date, datetime.date):
        return status.Status(False, 'Invalid consumed_date. Expected a datetime.date object')
    consumed_date_filename = fileutils.datetime_to_string(consumed_date, '.csv')
    fooditem = try_get_food_item(food_name)
    if fooditem is not None:
        process_food_eaten(fooditem, consumed_percent, consumed_date_filename)
        return status.Status(True)
    else:
        return status.Status(False, 'Unable to find food item named "{0}". Did you add it to the list with the "add-food" command?'.format(food_name))