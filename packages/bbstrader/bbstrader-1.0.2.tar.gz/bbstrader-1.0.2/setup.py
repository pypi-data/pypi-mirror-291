from setuptools import setup
import codecs 
import sys, os

if sys.version_info < (3,9):
    sys.exit("Only Python 3.9 and greater is supported") 

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

VERSION = '1.0.2'
DESCRIPTION = 'Simplified Investment & Trading Toolkit'

# Setting up
setup(
    name="bbstrader",
    version=VERSION,
    packages=["bbstrader"],
    author="Bertin Balouki SIMYELI",
    maintainer="Bertin Balouki SIMYELI",
    author_email="<bbalouki@outlook.com>",
    license = "MIT",
    description=DESCRIPTION,
    url='https://github.com/bbalouki/BBSTrade',
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[
        "Metatrader5",
        "pandas",
        "numpy==1.26.4",
        "yfinance",
        "scipy",
        "hmmlearn",
        "pmdarima",
        "arch",
        "seaborn",
        "statsmodels",
        "matplotlib",
        "filterpy",
        "pytest",
        "sphinx",
        "sphinx-rtd-theme",
        "CurrencyConverter",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows",
    ],
    keywords = [
    "Finance",
    "Financial",
    "Analysis",
    "Trading",
    "Metatrader5",
    "MT5"
    "Quantitative",
    "Equities",
    "Currencies",
    "Economics",
    "ETFs",
    "Indices",
    "Commodities",
    "Cryptos"
    ]

)