# TOPSIS CLI

Python command-line implementation of the TOPSIS method.

## Install
```bash
pip install .
```

## Run
```bash
topsis <input.csv> "<weights>" "<impacts>" <output.csv>
```

### Example
```bash
topsis data.csv "1,1,1" "+,+,+" result.csv
```

## Input
- CSV file
- First column: alternatives
- Remaining columns: numeric criteria

## Output
- Adds `Topsis Score` and `Rank`

## Author
Harditya Vir Singh Ghuman