# main.py
def hello():
    print("hello this is a test package")

# import sys

# class Class_01_BMIcalc:
#     """
#     A class to calculate Body Mass Index (BMI) based on weight and height.

#     Methods
#     -------
#     __init__(gender: str, weight: float, height: float, unit: str = "metric")
#         Initializes the BMICalculator class with gender, weight, height, and unit system.
#     calculate_bmi() -> float
#         Calculates the BMI based on the provided weight and height.
#     bmi_category() -> str
#         Categorizes the BMI into standard categories.
#     get_bmi_info() -> str
#         Provides a summary of the BMI calculation and its category.
#     """
#     def __init__(self, gender: str, weight: float, height: float, unit: str = "metric"):
#         """
#         Initialize the BMICalculator class with gender, weight, height, and unit system.

#         :param gender: str - 'male' or 'female'
#         :param weight: float - weight in kilograms (for metric) or pounds (for imperial)
#         :param height: float - height in meters (for metric) or inches (for imperial)
#         :param unit: str - 'metric' or 'imperial' (default is 'metric')
#         """
#         self.gender = gender.lower()
#         self.weight = weight
#         self.height = height
#         self.unit = unit.lower()

#     def calculate_bmi(self) -> float:
#         """
#         Calculate the BMI based on the provided weight and height.

#         :return: float - BMI value
#         """
#         if self.unit == "metric":
#             bmi = self.weight / (self.height ** 2)
#         elif self.unit == "imperial":
#             bmi = (self.weight / (self.height ** 2)) * 703
#         else:
#             raise ValueError("Unit must be 'metric' or 'imperial'.")
#         return round(bmi, 2)

#     def bmi_category(self) -> str:
#         """
#         Categorize the BMI into standard categories.

#         :return: str - Category of BMI
#         """
#         bmi = self.calculate_bmi()
#         if bmi < 18.5:
#             return "Underweight"
#         elif 18.5 <= bmi < 24.9:
#             return "Normal weight"
#         elif 25.0 <= bmi < 29.9:
#             return "Overweight"
#         else:
#             return "Obesity"

#     def get_bmi_info(self) -> str:
#         """
#         Provide a summary of the BMI calculation and its category.

#         :return: str - Summary of BMI calculation and category
#         """
#         bmi = self.calculate_bmi()
#         category = self.bmi_category()
#         return f"Gender: {self.gender.capitalize()}, BMI: {bmi}, Category: {category}"
    
# def print_help():
#     """
#     Prints the help message explaining how to use the BMICalculator script.
#     """
#     help_message = """
#     BMICalculator Script

#     This script calculates the Body Mass Index (BMI) based on the user's gender, weight, and height.
#     You can use it by creating instances of the BMICalculator class.

#     Example usage:

#         # Example with metric units
#         person1 = BMICalculator(gender="female", weight=68, height=1.65)
#         print(person1.get_bmi_info())

#         # Example with imperial units
#         person2 = BMICalculator(gender="male", weight=150, height=65, unit="imperial")
#         print(person2.get_bmi_info())

#     Arguments:
#         gender : 'male' or 'female' (required)
#         weight : float - weight in kilograms (for metric) or pounds (for imperial) (required)
#         height : float - height in meters (for metric) or inches (for imperial) (required)
#         unit   : 'metric' or 'imperial' (optional, default is 'metric')

#     Methods:
#         calculate_bmi()   : Returns the calculated BMI value.
#         bmi_category()    : Returns the category of the BMI (Underweight, Normal weight, Overweight, Obesity).
#         get_bmi_info()    : Returns a string summary of gender, BMI, and category.
#     """
#     print(help_message)

# if __name__ == "__main__":
#     # Check if the user asked for help
#     if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
#         print_help()
#     else:
#         # Example usage
#         person1 = Class_01_BMIcalc(gender="female", weight=68, height=1.65)
#         print(person1.get_bmi_info())  # This will print the BMI info

#         person2 = Class_01_BMIcalc(gender="male", weight=150, height=65, unit="imperial")
#         print(person2.get_bmi_info())  # This will print the BMI info


