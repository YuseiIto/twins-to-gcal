import csv


def readCsvFromFile(file):
    print(f"Reading {file}...")
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        content = [row for row in reader]
        return content
