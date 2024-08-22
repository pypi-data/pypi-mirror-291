# BMICalculator
**BMICalculator** is a Python package that allows users to calculate their Body Mass Index (BMI) based on their weight, height, and unit system (metric or imperial). It also categorizes the BMI into standard categories such as Underweight, Normal weight, Overweight, and Obesity.

## Installation
You can install the package using pip:
```bash
pip install glarki-bmi-calculator
```

## Usage
**Import**
``` python
from glarki_bmi_calculator import Class_01_BMIcalc as bmi
```

**Example with metric units**
```Python
person1 = bmi(gender="female", weight=68, height=1.65)
print(person1.get_bmi_info())  # Output: Gender: Female, BMI: 24.98, Category: Normal weight
```
**Example with imperial units**
``` Python
person2 = bmi(gender="male", weight=150, height=65, unit="imperial")
print(person2.get_bmi_info())  # Output: Gender: Male, BMI: 24.96, Category: Normal weight
```

## Help
In python:
```Python
print(bmi.__doc__)
print(bmi.{method}.__doc__)
```
In Command Line Interface
```Bash
glarki_bmi_help
```

<!-- <p> Some text that explains stuff </p>  -->
