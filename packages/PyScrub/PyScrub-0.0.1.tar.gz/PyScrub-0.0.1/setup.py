from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Automated data transformation workflow with pipeline integration.'
LONG_DESCRIPTION = """
PyScrub is a powerful Python library designed to streamline data preprocessing and pipeline automation. 
It provides efficient tools for data cleaning, transformation, feature engineering, and visualization, 
all integrated into a reproducible and scalable pipeline framework.
"""

# Setting up
setup(
    name="PyScrub",
    version=VERSION,
    author="Fasugba Ayomide",
    author_email="fasugbapaul@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scikit-learn'
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
