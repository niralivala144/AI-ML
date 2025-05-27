from datetime import datetime

def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def calculate_age(birthdate):
    now = datetime.now()
    age_delta = now - birthdate
    years = now.year - birthdate.year - ((now.month, now.day) < (birthdate.month, birthdate.day))
    months = years * 12 + now.month - birthdate.month
    days = age_delta.days
    hours = age_delta.total_seconds() // 3600
    seconds = int(age_delta.total_seconds())
    return years, months, days, int(hours), seconds

if __name__ == "__main__":
    # Input from user
    birth_day = int(input("Enter your birth day (DD): "))
    birth_month = int(input("Enter your birth month (MM): "))
    birth_year = int(input("Enter your birth year (YYYY): "))

    # Create birthdate object
    try:
        birthdate = datetime(birth_year, birth_month, birth_day)
    except ValueError:
        print("Invalid date entered.")
        exit()

    # Check leap year
    if is_leap_year(birth_year):
        print(f"{birth_year} is a Leap Year.")
    else:
        print(f"{birth_year} is not a Leap Year.")

    # Calculate age
    years, months, days, hours, seconds = calculate_age(birthdate)
    print(f"Your Age:")
    print(f"Years: {years}")
    print(f"Months: {months}")
    print(f"Days: {days}")
    print(f"Hours: {hours}")
    print(f"Seconds: {seconds}")