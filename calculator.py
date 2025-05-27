import statistics

# Step 1: Ask how many numbers
count = int(input("How many numbers do you want to enter? "))

# Step 2: Collect numbers
numbers = []
print(f"Enter {count} numbers one by one:")
for _ in range(count):
    num = float(input("Enter number: "))
    numbers.append(num)

# Step 3: Ask what to calculate
print("\nWhat would you like to calculate?")
print("1. Mean")
print("2. Median")
print("3. Mode")
choice = input("Enter your choice (Mean/Median/Mode): ").strip().lower()

# Step 4: Perform calculation
if choice == "mean":
    result = sum(numbers) / len(numbers)
    print(f"The Mean is: {result}")
elif choice == "median":
    result = statistics.median(numbers)
    print(f"The Median is: {result}")
elif choice == "mode":
    try:
        result = statistics.mode(numbers)
        print(f"The Mode is: {result}")
    except statistics.StatisticsError:
        print("No unique mode found (all values might be equally frequent).")
else:
    print("Invalid choice. Please select Mean, Median, or Mode.")
