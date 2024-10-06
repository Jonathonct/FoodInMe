Developed by Jonathon Teague, last updated in September 2024.

This is a simple program that can be used to keep track of the foods eaten
over the course of a day, and is intended to help the user with their personal
nutritional goals. Based on the data in data/foods.csv which they must manually curate,
it tallies up the total number of calories and the relative amount in grams
of fats, proteins and carbohydrates that has been consumed on a given date.

Future iterations could consider:
- Implementing web crawling to provide a curated database, rather than requiring the user to define it one at a time.
- Aggregate nutritional results over periods of days / weeks / months and allow for users to explicitly set their goals.
- Rewriting as a mobile application with a better graphical user interface for adding/removing items.
- Scaling to serve multiple users, rather than being localized to a single user.