import datetime
import fileutils
import food_item
import nutrition_information
import os
import status

USER_GOAL_FILENAME='goals.csv'

# Returns the filepath to the user's nutrition goals.
def goals_filepath():
    return fileutils.user_consumption_dirpath() + USER_GOAL_FILENAME

# Adds item to map if not already existing, or increments otherwise.
def add_or_increment(dictionary, key, value):
    if key in dictionary:
        dictionary[key] += value
    else:
        dictionary[key] = value

# Returns a NutritionInformation object aggregating the food consumed in the provided status_filepath,
# or an error status indicating a failed precondition.
# If detailed_results is provided as an empty vector, each individual item name will be added.
def get_daily_nutrition_information(status_date_string, detailed_results=None):
    dirpath = fileutils.user_consumption_dirpath()
    status_filepath = dirpath + status_date_string + '.csv'
    if not os.path.exists(status_filepath):
        return status.Status(False, 'No entries recorded for {0}'.format(status_date_string))

    total_calories = 0
    total_carbs = 0
    total_fats = 0
    total_proteins = 0
    
    with open(status_filepath, 'r') as input:
        for line in input:
            if line == '': continue # Skip empty lines
            fooditem = food_item.parse_food_item(line.strip(), ',')
            if fooditem is None:
                return status.Status(False, 'Failed to parse "{0}" from data/custom_foods.csv as a food item'.format(line.strip()))
            try:
                total_calories += float(fooditem.calories())
                total_carbs += float(fooditem.carbs())
                total_fats += float(fooditem.fats())
                total_proteins += float(fooditem.proteins())
            except Exception as e:
                return status.Status(False, 'Failed to parse "{0}" from data/custom_foods.csv as a valid food item'.format(line.strip()))
            if detailed_results is not None:
                add_or_increment(detailed_results, fooditem.name, fooditem.nutrition_information)
    return nutrition_information.NutritionInformation(total_calories, total_carbs, total_fats, total_proteins)
    
# Returns a NutritionInformation object representing the daily nutrition goals of the user,
# or a Status object indicating that information could not be retrieved.
def get_goal_nutrition_information():
    goal_filepath = goals_filepath()
    if os.path.exists(goal_filepath):
        with open(goal_filepath, 'r') as input:
            goal_text = input.readline()
            try:
                numbers = goal_text.split(',')
                goal_calories = float(numbers[0])
                goal_carbs = float(numbers[1])
                goal_fats = float(numbers[2])
                goal_proteins = float(numbers[3])
            except:
                return status.Status(False, 'Invalid goal file. Reset your nutrition goal with the "set-goal" command.')
            return nutrition_information.NutritionInformation(goal_calories, goal_carbs, goal_fats, goal_proteins)
    else:
        return status.Status(False, 'Missing goal file. Consider setting your nutrition goals with the "set-goal" command.')

### ---------------------------------- PUBLIC functions ---------------------------------------------- ###

# Sets the daily goal nutritional values for the user, overriding the previous entry if applicable.
def set_goals(calories, carbs, fats, proteins):
    daily_goal = '{0},{1},{2},{3}'.format(calories, carbs, fats, proteins)
    with open(goals_filepath(), 'w') as output:
        output.write(daily_goal)

# Prints the status report for a given date, for the amount of calories and other nutrients consumed.
def print_status_report(status_date, detailed_report):
    if not isinstance(status_date, datetime.date):
        return status.Status(False, 'Invalid status date. Expected a datetime.date object')
    status_date_string = fileutils.datetime_to_string(status_date)

    detailed_results = {} if detailed_report else None
    daily_nutrition_info = get_daily_nutrition_information(status_date_string, detailed_results)
    if isinstance(daily_nutrition_info, status.Status):
        return daily_nutrition_info
    print('On {0}, you reported consuming {1} calories, {2} grams of carbs, {3} grams of fats and {4} grams of protein'.format(
        status_date_string, daily_nutrition_info.calories, daily_nutrition_info.carbs, daily_nutrition_info.fats, daily_nutrition_info.proteins))
    
    goal_nutrition_info = get_goal_nutrition_information()
    if isinstance(goal_nutrition_info, nutrition_information.NutritionInformation):
        print('Compared to your daily goals, this represents:\n{0}'.format(daily_nutrition_info.compare(goal_nutrition_info).replace(', ', '\n')))
    else:
        print(goal_nutrition_info.error())
    
    if detailed_results is not None:    
        print('Detailed breakdown of each item:')
        for k, v in detailed_results.items():
            print('{0}: {1}'.format(k.replace('_', ' '), v.to_string()))

    return status.Status(True)