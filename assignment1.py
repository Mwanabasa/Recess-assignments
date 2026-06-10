def get_positive_float(prompt):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value <= 0:
            print("Value must be greater than zero.")
            continue
        return value


def get_positive_int(prompt):
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("Please enter a whole number.")
            continue
        value = int(raw)
        if value <= 0:
            print("Number of people must be at least 1.")
            continue
        return value


def get_tip_percentage():
    choices = {
        "1": 10,
        "2": 15,
        "3": 20,
        "4": None,
    }

    print("Choose a tip percentage:")
    print("  1) 10%")
    print("  2) 15%")
    print("  3) 20%")
    print("  4) Custom tip percentage")

    while True:
        choice = input("Enter 1, 2, 3, or 4: ").strip()
        if choice not in choices:
            print("Please choose 1, 2, 3, or 4.")
            continue
        if choices[choice] is not None:
            return float(choices[choice])

        custom = input("Enter custom tip percentage (e.g. 18.5): ").strip()
        try:
            tip_value = float(custom)
        except ValueError:
            print("Please enter a valid number for the tip percentage.")
            continue
        if tip_value < 0:
            print("Tip percentage cannot be negative.")
            continue
        return tip_value


def format_currency(amount):
    return f"UGX {amount:,.2f}"


def main():
    print("Bill Split Calculator")
    total_amount = get_positive_float("Total bill amount: UGX ")
    people = get_positive_int("Number of people: ")
    tip_percentage = get_tip_percentage()

    tip_amount = total_amount * tip_percentage / 100
    grand_total = total_amount + tip_amount
    per_person = grand_total / people

    print("\n Receipt ")
    print(f"Bill amount:      {format_currency(total_amount)}")
    print(f"Tip percentage:   {tip_percentage:.2f}%")
    print(f"Tip amount:       {format_currency(tip_amount)}")
    print(f"Total with tip:   {format_currency(grand_total)}")
    print(f"People splitting: {people}")
    print(f"Each person pays: {format_currency(per_person)}")
    print("End of receipt.")


if __name__ == "__main__":
    main()
