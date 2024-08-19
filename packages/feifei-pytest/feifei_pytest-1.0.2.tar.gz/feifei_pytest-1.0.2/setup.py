from setuptools import setup, find_packages

setup(
    name="feifei-pytest",
    version="1.0.2",
    author="roger813",
    author_email="roger813@163.com",
    description="A pytest tools box for testing.",
    long_description="A pytest tools box for testing.",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        "allure-pytest==2.13.5",
        "openpyxl==3.1.5",
        "pandas==2.2.2",
        "pip==24.2",
        "playwright==1.39.0",
        "psycopg2==2.9.9",
        "pyodbc==5.1.0",
        "pytest-assume==2.4.3",
        "pytest-bdd==7.2.0",
        "requests==2.32.3"
    ]
)