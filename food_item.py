import nutrition_information

CSV_HEADER='name,calories (in grams),carbohydrates (in grams),fats (in grams),proteins (in grams)'

# Simple class to represent a food item, and its associated NutritionInformation.
class FoodItem:
    def __init__(self, name, calories, carbs, fats, proteins):
        self.name = name
        self.nutrition_information = nutrition_information.NutritionInformation(calories, carbs, fats, proteins)
        
    def __add__(self, other):
        combined_nutrition = self.nutrition_information + other.nutrition_information
        return FoodItem(self.name, combined_nutrition.calories(), combined_nutrition.carbs, combined_nutrition.fats, combined_nutrition.proteins)

    def name(self):
        return self.name

    def calories(self):
        return self.nutrition_information.calories

    def carbs(self):
        return self.nutrition_information.carbs

    def fats(self):
        return self.nutrition_information.fats

    def proteins(self):
        return self.nutrition_information.proteins

    def to_csv(self):
        return '{0},{1}'.format(self.name, self.nutrition_information.to_csv())
        
    def to_string(self):
        return '{0}: {1} calories, {2}g carbs, {3}g fat, {4}g protein'.format(
        self.name.replace('_', ' '), self.calories(), self.carbs(), self.fats(), self.proteins())

# Attempts to parse the given string into a food item format. 'string' is expected to be in the format:
# 'name-cal-carbs-fats-proteins' where 'name' is a string and the rest are integers.
def parse_food_item(string, splitter):
    args = string.split(splitter)
    if len(args) != 5:
        return None
    try:
        name = args[0]
        cal = float(args[1])
        carbs = float(args[2])
        fats = float(args[3])
        proteins = float(args[4])
        return FoodItem(name, cal, carbs, fats, proteins)
    except Exception as e:
        return None