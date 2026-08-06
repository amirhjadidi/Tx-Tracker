import pandas as pd
import csv
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description


class CSV:
    CSV_FILE = "finance_file.csv"
    CSV_COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

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

    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            data = pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            print(f"file {cls.CSV_FILE} not found. please add transactions first!")
            return pd.DataFrame()
        # print(data)
        data["date"] = pd.to_datetime(data["date"], format=cls.FORMAT)
        # print(data["date"])

        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (data["date"] >= start_date) & (data["date"] <= end_date)
        filtered_data = data.loc[mask]

        if filtered_data.empty:
            print("no TXs found within givin dates")
        else:
            print(f"transactions from  {start_date} to {end_date}")

            print(filtered_data.to_string(index=False))

            total_income = filtered_data[filtered_data["category"] == "Income"][
                "amount"
            ].sum()

            total_expense = filtered_data[filtered_data["category"] == "Expense"][
                "amount"
            ].sum()
            print("\n Summary")
            print(f"total income: {total_income}")
            print(f"total expense: {total_expense}")
            print(f"net saving: {total_income - total_expense}")

        return filtered_data


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


# CSV.get_transactions("20-1-2025", "20-1-2027")


def main():
    while True:
        print("\n1. Add new Transaction")
        print("2. view transactions summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
            print("*" * 50)
        elif choice == "2":
            start_date = get_date("Enter the start date: ")

            end_date = get_date("Enter the end date: ")

            CSV.get_transactions(start_date, end_date)
            print("*" * 50)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("invalid choice")


if __name__ == "__main__":
    main()
