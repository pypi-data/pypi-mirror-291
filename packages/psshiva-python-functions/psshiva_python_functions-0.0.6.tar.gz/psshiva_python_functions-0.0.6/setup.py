from setuptools import setup, find_packages

VERSION = "0.0.6"
DESCRIPTION = "PS.Shiva's Python Functions"
LONG_DESCRIPTION = "Package containing all the latest algorithms and functions by PS.Shiva"

setup(
    name="psshiva_python_functions",
    version=VERSION,
    author="Pratik Satpathy",
    author_email="satpathypratik@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",  # Specify the format for long description
    packages=find_packages(),
    install_requires=[
        "pandas>=2.2.2,<3.0.0",      # Specify version range for pandas
        "sqlalchemy>=2.0.32,<3.0.0", # Specify version range for SQLAlchemy
        "openai>=1.42.0,<2.0.0",     # Specify version range for openai
        "typing; python_version<'3.5'"  # Include typing for Python versions < 3.5
    ],
    keywords=['psshiva', 'ps.shiva', 'PS.Shiva', 'PSSHIVA', 'python', 'functions', 'algorithms'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
