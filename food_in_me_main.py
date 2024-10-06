import datetime
import food_item
import food_processor
import nutrition_accessor
import status

GENERAL_USAGE = 'Type "help --command" for more info on a particular command. Supported commands are: "add-food", "eat", "report", "set-goal".'
ADD_FOOD_USAGE = '''To add a new food item to the list of supported food items, type "add-food name-cal-carbs-fats-proteins".
The food item will be saved as the string "name", with "cal" number of calories, "carbs" number of
carbohydrates (in grams), "fats" number of fats (in grams) and "proteins" number of proteins (in grams).
If successful in parsing the new food item, you will be asked whether to save or overwrite the existing one.
If unable to parse the new food item due to invalid numbers, a failure message will be displayed instead.'''
EAT_USAGE = '''To record a food as being eaten, type "eat name", where "name" is what was consumed. 
The food must already exist in the list of supported food items.  If it has not been added yet, first use the "add-food" command.
Optionally, you can specify the amount consumed if it was less than the full amount, e.g. "eat pizza percent=25"
Optionally, you can specify the date it was consumed if not today, e.g. "eat pineapple date=9-20-2024".'''
SET_GOAL_USAGE = 'To set your daily nutrition goal, type "set-goal cal-carbs-fats-proteins". Each of the arguments must be a number.'
REPORT_USAGE = 'Provides a report of the nutritional impact of all foods eaten on a given date, e.g. "report 9-20-2024".'

# Returns True if the user has accepted the prompt, or False otherwise.
def accepted(string):
    s = str(string).lower()
    if s == 'y' or s == 'yes':
        return True
    return False

# Handles the "help" command to instruct how to use the CLI.
def handle_help(args):
    if len(args) == 2:
        mode = str(args[1].lower())
        if mode == 'add-food':
            print(ADD_FOOD_USAGE)
        elif mode == 'eat':
            print(EAT_USAGE)
        elif mode == 'report':
            print(REPORT_USAGE)
        elif mode == 'set-goal':
            print(SET_GOAL_USAGE)
        else:
            print(GENERAL_USAGE)
    else:
        print(GENERAL_USAGE)
        
# Handles the "add-food" command to add new food items to the saved list.
def handle_add_food(args):
    if len(args) == 2:
        food_name = args[1].split('-')[0]
        status = food_processor.try_add_food_item(args[1].lower())
        if status.okay():
            print('Success! {0} was added to the food inventory.'.format(food_name))
        elif status.error() == food_processor.PREEXISTING_ITEM:
            overwrite = input('{0} already exists. Overwrite with new values?\n'.format(food_name))
            if accepted(overwrite):
                status = food_processor.try_add_food_item(args[1].lower(), True)
                if status.okay():
                    print('{0} was updated with new values!'.format(food_name))
                else:
                    print(status.error())
            else: 
                print('{0} was not updated.'.format(food_name))
        else:
            print(status.error())
    else:
        print(ADD_FOOD_USAGE)

# Handles the "eat" command to record new foods eaten.        
def handle_eat(args):
    if len(args) < 2 or len(args) > 4:
        print(EAT_USAGE)
        return
    food_name = args[1]
    consumed_date = datetime.datetime.today()
    consumed_percent = 100
    valid_command = True

    for i in range (2, len(args)):
        optional_arg = args[i].split('=')
        if len(optional_arg) != 2:
            valid_command = False
        elif optional_arg[0].lower() == 'date':
            d = optional_arg[1].split('-')
            if len(d) != 3:
                valid_command = False
            else:
                try:
                    month = int(d[0])
                    day = int(d[1])
                    year = int(d[2])
                    consumed_date = datetime.datetime(year, month, day)
                except:
                    valid_command = False
        elif optional_arg[0].lower() == 'percent':
            try:
                consumed_percent = int(optional_arg[1])
            except:
                valid_command = False
        else:
            valid_command = False
    if valid_command:
        status = food_processor.try_process_food_eaten(food_name, consumed_percent, consumed_date)
        if not status.okay():
            print(status.error())
        else:
            print("Success!")
    else:
        print(EAT_USAGE)
        
# Handles the "report" command to print out the report for foods eaten on a given date.
def handle_report(args):
    if len(args) == 2:
        d = args[1].split('-')
        if len(d) != 3:
            print(REPORT_USAGE)
            return 
        try:
            month = int(d[0])
            day = int(d[1])
            year = int(d[2])
            status_date = datetime.datetime(year, month, day)
        except:
            print(REPORT_USAGE)
            return
        status_date = datetime.datetime(year, month, day)
        status = nutrition_accessor.print_status_report(status_date)
        if not status.okay():
            print(status.error())
    else:
        print(REPORT_USAGE)
        
# Handles the "set-goal" command to set a target for daily nutrition.
def handle_set_goal(args):
    if len(args) == 2:
        goals = args[1].split('-')
        if len(goals) != 4:
            print(SET_GOAL_USAGE)
            return
        try:
            calories = int(goals[0])
            carbs = int(goals[1])
            fats = int(goals[2])
            proteins = int(goals[3])
        except:
            print(SET_GOAL_USAGE)
            return
        nutrition_accessor.set_goals(calories, carbs, fats, proteins)
        print('Your new daily nutrition goal has been recorded!')
    else:
        print(SET_GOAL_USAGE)

# Example program invocation: python food_in_me_main.py
# This main loop provides a simple command line interface to interact with the program.
if __name__ == '__main__':
    while True:
        inp = input('Please enter a command with arguments, "help" to learn more, or "quit" to exit:\n')
        args = inp.split(' ')
        if inp.lower() == 'quit':
            quit()
        elif args[0].lower() == 'help':
            handle_help(args)
        elif args[0].lower() == 'add-food' or args[0].lower() == 'add-drink':
            handle_add_food(args)
        elif args[0].lower() == 'eat' or args[0].lower() == 'drink':
            handle_eat(args)
        elif args[0].lower() == 'report':
            handle_report(args)
        elif args[0].lower() == 'set-goal':
            handle_set_goal(args)
        else:
            print('Invalid command: {0}'.format(inp))
            print(GENERAL_USAGE)
        print('------------------------------------------')