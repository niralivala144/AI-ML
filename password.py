# Ask for password
password = input("Enter your password: ")

# Initialize flags
has_number = any(char.isdigit() for char in password)
has_special = any(char in '!@#$' for char in password)

# Check conditions
if len(password) < 8:
    print("Password too short! Must be at least 8 characters.")
elif not has_number:
    print("Password must contain at least one number.")
elif not has_special:
    print("Password must include at least one special character (!@#$).")
else:
    print("Password is strong!")
