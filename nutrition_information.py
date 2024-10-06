# Simple class to represent a nutrition information.
class NutritionInformation:
    def __init__(self, calories, carbs, fats, proteins):
        self.calories = calories
        self.carbs = carbs
        self.fats = fats
        self.proteins = proteins

    def to_csv(self):
        return '{0},{1},{2},{3}'.format(self.calories, self.carbs, self.fats, self.proteins)

    # Returns a string comparing the nutrition information of this object to another.
    def compare(self, other):
        calorie_delta = self.calories - other.calories
        carb_delta = self.carbs - other.carbs
        fats_delta = self.fats - other.fats
        protein_delta = self.proteins - other.proteins
        return '{0} {1}, {2} {3}, {4} {5}, {6} {7}'.format(
            abs(calorie_delta),
            'more calories' if calorie_delta > 0 else 'less calories',
            abs(carb_delta),
            'more grams of carbs' if carb_delta > 0 else 'less grams of carbs',
            abs(fats_delta),
            'more grams of fat' if fats_delta > 0 else 'less grams of fat',
            abs(protein_delta),
            'more grams of protein' if protein_delta > 0 else 'less grams of protein',
        )