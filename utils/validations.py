import re
from .messages import error_message

# ========== PAGINATION VALIDATION ==========
def validate_pagination_choice(choice):

    choice = choice.lower().strip()

    valid_choices = ["n", "p", "e"]

    if choice not in valid_choices:
        error_message(
            "Please Enter Only N, P Or E"
        )
        return False

    return True

# ROLL NUMBER VALIDATION
def validate_roll_no(roll_no):

    # EMPTY CHECK
    if roll_no.strip() == "":
        error_message(
            "Roll Number Cannot Be Empty."
        )
        return False

    # NUMERIC CHECK
    if not roll_no.isdigit():
        error_message(
            "Roll Number Must Be Numeric POSITIVE VALUE."
        )
        return False
    
    roll_no_int = int(roll_no)
    
    # POSITIVE CHECK
    if roll_no_int == 0:
        error_message("Roll Number Must Be Greater Than 0.")
        return False

    return True


# NAME VALIDATION
def validate_name(full_name):
    
    full_name = full_name.strip()

    # EMPTY CHECK
    if full_name == "":
        error_message(
            "Name Cannot Be Empty."
        )
        return False
    
    # ONLY ALPHABETS + SPACES ALLOWED
    if not all(
        char.isalpha() or char.isspace()
        for char in full_name
    ):
        error_message(
            "Name Must Contain Only Alphabets"
        )
        return False
    
    # SPLIT WORDS
    words = full_name.split()

    # REQUIRE FIRST + LAST NAME
    if len(words) < 2:  # checks the number of words, not the number of characters
        error_message(
            "Enter Full Name (First And Last Name)"
        )
        return False

    # EACH WORD MINIMUM 3 CHARACTERS
    for word in words:

        if len(word) < 3:
            error_message(
                "Each Name Must Contain At Least 3 Characters"
            )
            return False

    return True


# AGE VALIDATION
def validate_age(age):

    if age.strip() == "":
        error_message("Age Cannot Be Empty")
        return False

    # DIGIT CHECK
    if not age.isdigit():
        error_message(
            "Age Must Be Numeric POSITIVE VALUE."
        )
        return False

    age = int(age)

    # RANGE CHECK
    if age < 5 or age > 50:
        error_message(
            "Age Must Be Between 5 And 50"
        )
        return False

    return True

# GENDER VALIDATION
def validate_gender(gender):
    
    # EMPTY CHECK
    if gender.strip() == "":
        error_message(
            "Gender Cannot Be Empty"
        )
        return False
    
    # ONLY ALPHABETS
    if not all(char.isalpha() for char in gender):
        error_message(
            "Gender Must Contain Only Alphabets"
        )
        return False
    
    gender = gender.strip().lower()

    valid_genders = ["male", "female", "other"]

    if gender not in valid_genders:
        error_message("Gender Must Be Male, Female Or Other")
        return False

    return True

# COURSE VALIDATION
def validate_course(course):

    course = course.strip()

    # EMPTY CHECK
    if course == "":
        error_message(
            "Course Cannot Be Empty"
        )
        return False

    # MINIMUM LENGTH
    if len(course) < 2:
        error_message(
            "Course Name Must Contain At Least 2 Characters"
        )
        return False
    
    # SHOULD NOT BE ONLY NUMBERS
    if course.isdigit():
        error_message(
            "Course Name Cannot Be Only Numbers"
        )
        return False

    # ALLOW LETTERS, SPACES, DOTS
    if not all(
        char.isalpha() or
        char.isspace() or
        char == "."
        for char in course
    ):
        error_message(
            "Course Name Contains Invalid Characters"
        )
        return False

    return True


# EMAIL VALIDATION
def validate_email(email):

    # EMPTY CHECK
    if email.strip() == "":
        error_message(
            "Email Cannot Be Empty"
        )
        return False

    email = email.strip()

    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if re.match(pattern, email):
        return True

    error_message("Invalid Email Format (Example: abc123@gmail.com or abc@yahoo.com)")

    return False


# PHONE VALIDATION
def validate_phone(phone):

    phone = phone.strip()

    # EMPTY CHECK
    if phone == "":
        error_message(
            "Phone number Cannot Be Empty"
        )
        return False

    # ONLY DIGITS
    if not phone.isdigit():
        error_message(
            "Phone Number Must Contain Only Digits"
        )
        return False

    # LENGTH CHECK
    if len(phone) != 10:
        error_message(
            "Phone Number Must Be 10 Digits"
        )
        return False

    return True


# ADDRESS VALIDATION
def validate_address(address):

    address = address.strip()

    # EMPTY CHECK
    if address == "":
        error_message("Address Cannot Be Empty")
        return False
    
    # MINIMUM LENGTH
    if len(address) < 2:
        error_message("Address Must Contain At Least 2 Characters")
        return False
    
    # SHOULD NOT BE ONLY NUMBERS
    if address.isdigit():
        error_message("Address Cannot Be Only Numbers")
        return False

    return True


def validate_username(username):

    username = username.strip()
    
    # EMPTY CHECK
    if username == "":
        error_message("Username Cannot Be Empty")
        return False
    
    # LETTERS + DIGITS + UNDERSCORE
    if not all(
        char.isalnum() or char == "_"
        for char in username
    ):
        error_message(
            "Username Can Contain Only Letters, Digits And Underscore"
        )
        return False
    
    # CANNOT BE ONLY DIGITS
    if username.isdigit():
        error_message(
            "Username Cannot Contain Only Numbers"
        )
        return False
    
        # MINIMUM LENGTH
    if len(username) < 3:
        error_message("Username Must Be At Least 3 Characters")
        return False

    return True


def validate_password(password):

    password = password.strip()

    if password == "":
        error_message("Password Cannot Be Empty\n")
        return False

    # AT LEAST ONE LETTER
    if not any(char.isalpha() for char in password):
        error_message(
            "Password Must Contain At Least One Letter\n"
        )
        return False
    
    # AT LEAST ONE NUMBER
    if not any(char.isdigit() for char in password):
        error_message(
            "Password Must Contain At Least One Number\n"
        )
        return False
    
    if len(password) < 4:
        error_message("Password Must Contain At Least 4 Characters\n")
        return False
    
    # AT LEAST ONE SPECIAL CHARACTER
    if not any(
        not char.isalnum()
        for char in password
    ):
        error_message(
            "Password Must Contain At Least One Special Character\n"
        )
        return False

    return True


# ========== SEARCH VALIDATION ==========
def validate_search_name(name):

    name = name.strip()

    # EMPTY CHECK
    if name == "":
        error_message(
            "Name Cannot Be Empty"
        )
        return False

    # ALPHABET CHECK
    if not all(
        char.isalpha() or char.isspace()
        for char in name
    ):
        error_message(
            "Name Must Contain Only Alphabets"
        )
        return False

    return True

def validate_search_course(course):

    course = course.strip()

    # EMPTY CHECK
    if course == "":
        error_message(
            "Course Name Cannot Be Empty"
        )
        return False
    
    # ONLY LETTERS + SPACES
    if not all(
        char.isalpha() or char.isspace()
        for char in course
    ):
        error_message(
            "Course Name Must Contain Only Alphabets"
        )
        return False

    return True

def validate_search_gender(gender):

    gender = gender.strip()

    # EMPTY CHECK
    if gender == "":
        error_message(
            "Gender Cannot Be Empty"
        )
        return False

    # ONLY LETTERS
    if not gender.isalpha():
        error_message(
            "Gender Must Contain Only Alphabets"
        )
        return False

    return True

def validate_search_email(email):

    email = email.strip()

    # EMPTY CHECK
    if email == "":
        error_message(
            "Email Cannot Be Empty"
        )
        return False

    # NO SPACES ALLOWED
    if " " in email:
        error_message(
            "Email Cannot Contain Spaces"
        )
        return False

    return True