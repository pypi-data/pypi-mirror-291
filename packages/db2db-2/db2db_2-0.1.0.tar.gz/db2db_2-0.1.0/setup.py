from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="db2db-2",
    version="0.1.0",  
    author="Akhtar Raza",
    author_email="akhtar.decy@gmail.com",
    description="A package to transfer data between SQL databases like PostgreSQL, MySQL, MSSQL.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akhtar21yr/db2db",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "SQLAlchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "mysql-connector-python>=8.0.0",
        "pyodbc>=4.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
