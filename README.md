# TOPSIS – Decision Support System

This project implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) method for multi criteria decision making.

---

## Part I — Command Line Interface (CLI)

### Install (local)
pip install .

### Run
topsis <input.csv> "<weights>" "<impacts>" <output.csv>

### Example
topsis data.csv "1,1,1" "+,+,+" result.csv

### Input
- CSV file
- First column: alternatives
- Remaining columns: numeric criteria

### Output
- Adds `Topsis Score` and `Rank` columns to the CSV

---

## Part II — Python Package (PyPI)

The project is packaged and published on PyPI.

### Install from PyPI
pip install Topsis-Harditya-102303230

### Run
topsis data.csv "1,1,1" "+,+,+" result.csv

---

## Part III — Web Service (Streamlit)

A public web service is implemented using Streamlit.

### Live Web App
https://topsis-gkmcunhxhys67pydcuxma2.streamlit.app/

### Features
- Upload CSV file or download sample CSV file
- Enter weights and impacts
- Preview inputs
- Can provide email address to get results sent via mail
- Preview inputs and outputs

---

## Author
Harditya Vir Singh Ghuman