import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description


class CSV:
    CSV_FILE = "finance_file.csv"
    CSV_COLUMNS = ["date", "amount", "category", "description"]

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)

        except FileNotFoundError:
            data = pd.DataFrame(columns=cls.CSV_COLUMNS)
            data.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.CSV_COLUMNS)
            writer.writerow(new_entry)

        print(f"new entry added: {new_entry}")


def add():
    CSV.initialize_csv()
    date = get_date(
        "Please enter the date in dd-mm-yyyy format, or hit Enter to get today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    category = get_category()
    description = get_description()

    CSV.add_entry(date, amount, category, description)


if __name__ == "__main__":
    while True:
        add()
        print("-" * 20)
        another = input("Add another entry? (y/n): ").lower()
        if another != "y":
            break
