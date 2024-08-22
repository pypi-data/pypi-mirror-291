from setuptools import setup, find_packages

setup(
    name='spark_insights',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'jinja2',
        'pyspark',
    ],
    description='A package to generate HTML reports for Spark DataFrames with detailed data health checks.',
    author='Adhi',
    author_email='adhiyaman1705@gmail.com', # Replace with your repository URL
)
