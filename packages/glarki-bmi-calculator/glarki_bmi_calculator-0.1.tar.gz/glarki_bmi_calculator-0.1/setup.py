from setuptools import setup, find_packages

setup(
    name='glarki_bmi_calculator',
    version='0.1',
    description='Calculate Body-Mass Index',
    author='Gijs Luijten',
    packages=find_packages(),
    install_requires=[
        # Add dependencies here.
        # e.g. 'numpy>=1.11.1'
    ],
    entry_points={
        'console_scripts':[
            'any_name_possible = glarki_bmi_calculator:hello',
        ],
    },
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