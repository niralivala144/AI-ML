# Student Report Card Generator

def input_marks(subjects):
    marks = {}
    for subject in subjects:
        while True:
            try:
                score = float(input(f"Enter marks for {subject}: "))
                if 0 <= score <= 100:
                    marks[subject] = score
                    break
                else:
                    print("Marks should be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")
    return marks

def calculate_results(marks):
    total = sum(marks.values())
    average = total / len(marks)
    cgpa = average / 9.5  # Typical CGPA conversion
    is_pass = all(mark >= 35 for mark in marks.values())
    return total, average, cgpa, is_pass

def display_report(name, marks, total, average, cgpa, is_pass):
    print("\n--- Student Report Card ---")
    print(f"Name: {name}")
    print("Marks:")
    for subject, mark in marks.items():
        print(f"  {subject}: {mark}")
    print(f"Total: {total}")
    print(f"Average: {average:.2f}")
    print(f"CGPA: {cgpa:.2f}")
    if is_pass:
        print("Congratulations, you have cleared the exam!")
    else:
        print("You have failed the exam.")

if __name__ == "__main__":
    name = input("Enter student name: ")
    subjects = ["Math", "Science", "English", "History", "Computer"]
    marks = input_marks(subjects)
    total, average, cgpa, is_pass = calculate_results(marks)
    display_report(name, marks, total, average, cgpa, is_pass)