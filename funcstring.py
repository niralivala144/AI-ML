def analyze_string(user_input):
    # 1. Length
    length = len(user_input)
    
    # 2. Starts with vowel or consonant
    first_char = user_input.strip()[0].lower() if user_input.strip() else ''
    if not first_char.isalpha():
        start_type = "Does not start with an alphabet character"
    elif first_char in 'aeiou':
        start_type = "Starts with a vowel"
    else:
        start_type = "Starts with a consonant"
    
    # 3. Reversed string
    reversed_str = user_input[::-1]

    # 4. Apply common string methods
    string_methods = {
        "original": user_input,
        "upper": user_input.upper(),
        "lower": user_input.lower(),
        "title": user_input.title(),
        "capitalize": user_input.capitalize(),
        "swapcase": user_input.swapcase(),
        "isalpha": user_input.isalpha(),
        "isdigit": user_input.isdigit(),
        "isalnum": user_input.isalnum(),
        "isspace": user_input.isspace(),
        "startswith_vowel": start_type,
        "reversed": reversed_str,
        "length": length
    }

    return string_methods
