# Imports needed for the PIP package
from setuptools import setup, find_packages

# read README.md file to variable desciption
with open('README.md', 'r') as f:
    description = f.read()

# Setup information
setup(
    name='glarki_bmi_calculator',
    version='0.3.2',
    description='Calculate Body-Mass Index',
    author='Gijs Luijten',
    packages=find_packages(),
    
    # Requirements and dependancies -> you can use this for the requirements.txt
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],

    # CLI mapping 'name' to 'function/method'
    entry_points={
        'console_scripts':[
            'glarki_bmi_help = glarki_bmi_calculator:print_help',
        ],
    },

    ## Add README.md file to desciption page using variable description
    long_description=description,
    long_description_content_type='text/markdown',
)

# setup(
#     name='BMICalculator',
#     version='0.1',
#     description='Calculate Body-Mass Index',
#     author='Gijs Luijten',
#     packages=find_packages(),
#     zip_safe=False,
#     setup_requires=[
#         'setuptools>=42',
#         'wheel'
#     ]
# )