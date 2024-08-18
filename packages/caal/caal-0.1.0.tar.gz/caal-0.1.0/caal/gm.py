# Simple Python Script Demo

# Function to greet a user
def greet_user(name):
    print(f"Hello, {name}!")

# Function to check if a number is even or odd
def check_even_odd(number):
    if number % 2 == 0:
        return "even"
    else:
        return "odd"

# Main function
def main():
    # Variable to store user name
    user_name = "Alice"

    # Greet the user
    greet_user(user_name)

    # List of numbers
    numbers = [1, 2, 3, 4, 5]

    # Loop through the list and check if each number is even or odd
    for num in numbers:
        result = check_even_odd(num)
        print(f"The number {num} is {result}.")

# Run the main function
if __name__ == "__main__":
    main()
