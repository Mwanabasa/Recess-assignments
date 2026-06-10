def main():
    try:
        num = int(input("Enter a number (1-7) for the day of the week: "))
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    match num:
        case 1:
            print("Monday")
        case 2:
            print("Tuesday")
        case 3:
            print("Wednesday")
        case 4:
            print("Thursday")
        case 5:
            print("Friday")
        case 6:
            print("Saturday")
        case 7:
            print("Sunday")
        case _:
            print("Number must be between 1 and 7.")

if __name__ == "__main__":
    main()
