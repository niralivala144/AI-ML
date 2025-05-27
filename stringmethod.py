def string_methods_demo():
    s = "Hello, World!"
    print(f"\nExample String: s = '{s}'")
    print("1. s.upper()           # Converts all characters to uppercase")
    print("   Output:", s.upper())
    print("2. s.lower()           # Converts all characters to lowercase")
    print("   Output:", s.lower())
    print("3. s.replace('World', 'Python')  # Replaces 'World' with 'Python'")
    print("   Output:", s.replace('World', 'Python'))
    print("4. s.count('l')        # Counts occurrences of 'l'")
    print("   Output:", s.count('l'))
    print("5. s.split(',')        # Splits the string at ','")
    print("   Output:", s.split(','))

def list_methods_demo():
    lst = [1, 2, 3, 2, 4]
    print(f"\nExample List: lst = {lst}")
    print("1. lst.append(5)       # Adds 5 at the end")
    lst.append(5)
    print("   Output:", lst)
    print("2. lst.count(2)        # Counts occurrences of 2")
    print("   Output:", lst.count(2))
    print("3. lst.remove(3)       # Removes first occurrence of 3")
    lst.remove(3)
    print("   Output:", lst)
    print("4. lst.reverse()       # Reverses the list")
    lst.reverse()
    print("   Output:", lst)
    print("5. lst.sort()          # Sorts the list")
    lst.sort()
    print("   Output:", lst)

def tuple_methods_demo():
    t = (1, 2, 3, 2, 4)
    print(f"\nExample Tuple: t = {t}")
    print("1. t.count(2)          # Counts occurrences of 2")
    print("   Output:", t.count(2))
    print("2. t.index(3)          # Returns index of first occurrence of 3")
    print("   Output:", t.index(3))
    print("Note: Tuples are immutable, so methods like append, remove, etc. are not available.")

if __name__ == "__main__":
    print("What do you want to learn?")
    print("1. String-methods")
    print("2. List-Methods")
    print("3. Tuple-Methods")
    choice = input("Enter your choice (String/List/Tuple): ").strip().lower()

    if choice == "string":
        string_methods_demo()
    elif choice == "list":
        list_methods_demo()
    elif choice == "tuple":
        tuple_methods_demo()
    else:
        print("Invalid choice. Please enter String, List, or Tuple.")