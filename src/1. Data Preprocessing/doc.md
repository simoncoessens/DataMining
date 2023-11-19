# Data Preprocessing

This folder contains Jupyter Notebooks responsible for the initial processing of the raw dataset provided by the National Railway Company of Belgium (SNCB).

## Contents
- `db_creation.sql`: This code loads in the csv file into a postgres database for easier use in the following functions
- `duplicate_values_removal.ipynb`: this notebook checks if there are exact duplicates in the given data. Result: no duplicates
- `check_locational_data.ipynb`: this notebook checks if the locational data is correct, it checks if entries that follow each another based on time are actually close to each another location wise

## Objective
The goal of these notebooks is to prepare the raw data for further analysis, ensuring it is clean, consistent, and in a usable format.

## How to Use
Run these notebooks in sequence to load, clean, and transform the raw data into a processed format, ready for exploration and analysis.
