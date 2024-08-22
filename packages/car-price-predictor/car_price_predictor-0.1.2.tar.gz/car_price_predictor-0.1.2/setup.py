from setuptools import setup, find_packages

setup(
    name="car_price_predictor",  # Name of your package
    version="0.1.2",  # Initial release version
    packages=find_packages(),  # Automatically find packages in the project
    include_package_data=True,  # Include data files specified in MANIFEST.in
    install_requires=[
        # Include dependencies listed in requirements.txt
        "pandas",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "joblib",
        "pyyaml",
    ],
    author="Mrugank Jadhav",
    author_email="mrugankjadhav@gmail.com",
    description="A package to predict car rental prices.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mj301296/CarRentalPricingPrediction",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
