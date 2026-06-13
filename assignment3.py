# Assignment 3: Real world application of loop control statements
# Write a program that simulates a simple country that will win world cup 2026.
# Use a while loop to control the flow of the program and use break, continue,
# and pass statements to manage the flow of the loop based on user input.

def main():
    countries = ["Brazil", "France", "Argentina", "USA", "Spain"]
    predicted_winner = "USA"

    print("Welcome to the World Cup 2026 prediction game.")
    print("Choose a country from the list below or type 'exit' to quit.")
    print(", ".join(countries))

    while True:
        choice = input("Enter your predicted winner: ").strip()

        if choice.lower() == "exit":
            print("Exiting the game. Goodbye.")
            break

        if not choice:
            print("No country entered. Please try again.")
            continue

        country = choice.title()
        if country not in countries:
            print("That country is not in the list. Please select a valid country.")
            continue

        if country == predicted_winner:
            print(f"Correct! {predicted_winner} will win World Cup 2026.")
            break
        else:
            print(f"{country} is not the predicted winner. Try again.")
            pass

    print("Thank you for playing.")

if __name__ == "__main__":
    main()
