# =====================================================
# Validations
# All input validation functions for the application
# Each function returns an error string or None (if valid)
# (Unchanged from the Tkinter version — this module never
#  depended on tkinter, so it moves over untouched)
# =====================================================

import re


# =====================================================
# REQUIRED FIELDS CHECK
# =====================================================

def validate_required_fields(data):
    """
    Accepts a dict of {field_name: value}.
    Returns a list of field names that are empty.
    Returns an empty list if all fields are filled.
    """

    missing_fields = []

    for field_name, value in data.items():

        # CHECK IF FIELD IS EMPTY AFTER STRIPPING WHITESPACE
        if not str(value).strip():
            missing_fields.append(field_name)

    return missing_fields


# =====================================================
# ROLL NUMBER VALIDATION
# =====================================================

def validate_roll_no(roll_no):
    """
    Validates roll number input.
    Must be a non-empty positive integer (digits only).
    Returns error string if invalid, None if valid.
    """

    roll_no = roll_no.strip()

    # EMPTY CHECK
    if roll_no == "":
        return "Please enter a roll number."

    # NEGATIVE NUMBER CHECK — checked separately from the generic
    # digits-only check below, since "-1000".isdigit() is False
    # for the wrong reason (the minus sign isn't a digit) — this
    # gives a clearer, more specific message instead of the vague
    # "must contain digits only" for something that IS digits,
    # just negative ones.
    if roll_no.startswith("-"):
        return "Roll number cannot be negative."

    # DIGITS ONLY CHECK
    if not roll_no.isdigit():
        return "Roll number must contain digits only."

    # MUST BE GREATER THAN ZERO
    if int(roll_no) == 0:
        return "Roll number must be greater than 0."


# =====================================================
# FULL NAME VALIDATION
# =====================================================

def validate_name(full_name):
    """
    Validates full name input.
    - Must contain letters and spaces only
    - Must have at least 2 words (first + last name)
    - Each word must be at least 3 characters
    Returns error string if invalid, None if valid.
    """

    full_name = full_name.strip()

    # EMPTY CHECK
    if full_name == "":
        return "Please enter the student's full name."

    # ONLY LETTERS AND SPACES ALLOWED
    if not all(char.isalpha() or char.isspace() for char in full_name):
        return "Name can contain letters and spaces only."

    # SPLIT INTO WORDS
    words = full_name.split()

    # REQUIRE AT LEAST FIRST AND LAST NAME
    if len(words) < 2:
        return "Please enter first and last name.\n Example: Rahul Sharma."

    # EACH WORD MUST BE AT LEAST 3 CHARACTERS
    for word in words:
        if len(word) < 3:
            return "Each part of the name must contain at least 3 letters."


# =====================================================
# AGE VALIDATION
# =====================================================

def validate_age(age):
    """
    Validates age input.
    - Must be digits only
    - Must be between 5 and 50
    Returns error string if invalid, None if valid.
    """

    age = age.strip()

    # EMPTY CHECK
    if age == "":
        return "Please enter age."

    # NEGATIVE NUMBER CHECK — same reasoning as validate_roll_no:
    # "-5".isdigit() is False for the wrong reason (the minus sign),
    # so this catches it separately for a clearer message.
    if age.startswith("-"):
        return "Age cannot be negative."

    # DIGITS ONLY CHECK
    if not age.isdigit():
        return "Age must contain digits only."

    age = int(age)

    # RANGE CHECK
    if age < 5 or age > 50:
        return "Age must be between 5 and 50 years."


# =====================================================
# GENDER VALIDATION
# =====================================================

def validate_gender(gender):
    """
    Validates gender input.
    - Must be one of: Male, Female, Other (case-insensitive)
    Returns error string if invalid, None if valid.
    """

    # EMPTY CHECK
    if gender.strip() == "":
        return "Please enter gender."

    # LETTERS ONLY
    if not all(char.isalpha() for char in gender):
        return "Gender can contain letters only."

    # MUST MATCH VALID OPTIONS
    if gender.strip().lower() not in ["male", "female", "other"]:
        return "Please enter Male, Female, or Other."


# =====================================================
# COURSE VALIDATION
# =====================================================

def validate_course(course):
    """
    Validates course input.
    - Must be at least 2 characters
    - Cannot be digits only
    - Can contain letters, spaces, and dots (e.g. B.Sc)
    Returns error string if invalid, None if valid.
    """

    course = course.strip()

    # EMPTY CHECK
    if course == "":
        return "Please enter a course name."

    # MINIMUM LENGTH
    if len(course) < 2:
        return "Course name must contain at least 2 characters."

    # CANNOT BE ONLY DIGITS
    if course.isdigit():
        return "Course name must contain at least one letter."

    # ONLY LETTERS, SPACES, AND DOTS ALLOWED
    if not all(
        char.isalpha() or
        char.isspace() or
        char == "."
        for char in course
    ):
        return "Course name can contain letters, spaces, and dots only."


# =====================================================
# EMAIL VALIDATION
# =====================================================

def validate_email(email):
    """
    Validates email address using a regex pattern.
    Must match standard email format: user@domain.ext
    Returns error string if invalid, None if valid.
    """

    # EMPTY CHECK
    if email.strip() == "":
        return "Please enter an email address."

    email = email.strip()

    # REGEX PATTERN FOR VALID EMAIL FORMAT
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(pattern, email):
        return "Please enter a valid email address.\n Example: abc123@gmail.com"


# =====================================================
# PHONE VALIDATION
# =====================================================

def validate_phone(phone):
    """
    Validates phone number input.
    - Must be digits only
    - Must be exactly 10 digits
    Returns error string if invalid, None if valid.
    """

    phone = phone.strip()

    # EMPTY CHECK
    if phone == "":
        return "Please enter a phone number."

    # NEGATIVE NUMBER CHECK — same reasoning as validate_roll_no
    if phone.startswith("-"):
        return "Phone number cannot be negative."

    # DIGITS ONLY
    if not phone.isdigit():
        return "Phone number must contain digits only."

    # MUST BE EXACTLY 10 DIGITS
    if len(phone) != 10:
        return "Phone number must be exactly 10 digits."


# =====================================================
# ADDRESS VALIDATION
# =====================================================

def validate_address(address):
    """
    Validates address input.
    - Must not be empty
    - Must be at least 2 characters
    - Cannot be digits only
    Returns error string if invalid, None if valid.
    """

    address = address.strip()

    # EMPTY CHECK
    if address == "":
        return "Please enter an address."

    # MINIMUM LENGTH
    if len(address) < 2:
        return "Address must contain at least 2 characters."

    # CANNOT BE DIGITS ONLY
    if address.isdigit():
        return "Address must contain letters and cannot be numbers only."


# =====================================================
# USERNAME VALIDATION
# =====================================================

def validate_username(username):
    """
    Validates admin username.
    - Letters, digits, and underscore (_) only
    - Cannot be digits only
    - Minimum 3 characters
    Returns error string if invalid, None if valid.
    """

    username = username.strip()

    # EMPTY CHECK
    if username == "":
        return "Please enter a username."

    # ONLY LETTERS, DIGITS, AND UNDERSCORE ALLOWED
    if not all(char.isalnum() or char == "_" for char in username):
        return (
            "Username can only contain letters, "
            "numbers, and underscore (_). "
            "Example: admin_1"
        )

    # CANNOT BE ONLY DIGITS
    if username.isdigit():
        return "Username must contain at least one letter."

    # MINIMUM 3 CHARACTERS
    if len(username) < 3:
        return "Username must be at least 3 characters long."


# =====================================================
# PASSWORD VALIDATION
# =====================================================

def validate_password(password):
    """
    Validates admin password.
    - Minimum 8 characters
    - At least one letter
    - At least one digit
    - At least one special character
    Returns error string if invalid, None if valid.
    """

    password = password.strip()

    # EMPTY CHECK
    if password == "":
        return "Please enter a password."

    # MINIMUM 8 CHARACTERS
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # AT LEAST ONE LETTER
    if not any(char.isalpha() for char in password):
        return "Password must contain at least one letter (A-Z or a-z)."

    # AT LEAST ONE DIGIT
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number (0-9)."

    # AT LEAST ONE SPECIAL CHARACTER
    if not any(not char.isalnum() for char in password):
        return (
            "Password must contain at least "
            "one special character "
            "(@, #, $, %, etc.)."
        )


# =====================================================
# SEARCH QUERY VALIDATION (FIELD-AWARE)
# Used by the Search page and the Delete-by-criteria
# search. Catches obviously-wrong input for the chosen
# field BEFORE running the database query — e.g. typing
# "22" while searching by Full Name — so the person gets
# a specific, helpful message ("enter letters only for
# Full Name") instead of a generic "No Student Found"
# that leaves them wondering if the feature is broken.
# =====================================================

def validate_search_query(field, query):
    """
    Checks whether `query` is a sensible value to search the
    given `field` by. Returns an error string if it obviously
    isn't (wrong characters, out-of-range, or not a real value
    for that field), or None if it's fine to run the search.

    Note: this is intentionally lighter than the full add/update
    validators in one specific way — it allows PARTIAL text (e.g.
    "sha" to find "Rahul Sharma", "MCo" to find "MCom") rather
    than requiring a complete, valid value. But it still rejects
    characters or values that could never belong in that field
    at all, so a typo or nonsense input gets a specific message
    instead of a generic "No Student Found".
    """

    query = query.strip()

    if query == "":
        return None  # AN EMPTY QUERY IS HANDLED SEPARATELY BY THE CALLER

    # ==========================================
    # ROLL NUMBER — DIGITS ONLY
    # ==========================================
    if field == "roll_no":
        if query.startswith("-"):
            return "Roll Number cannot be negative."
        if not query.isdigit():
            return "Please enter digits only for Roll Number."
        return None

    # ==========================================
    # AGE — DIGITS ONLY, AND WITHIN THE SAME
    # 5–50 RANGE ENFORCED WHEN ADDING/UPDATING
    # A STUDENT (see validate_age above)
    # ==========================================
    if field == "age":
        if query.startswith("-"):
            return "Age cannot be negative."
        if not query.isdigit():
            return "Please enter digits only for Age."
        age_value = int(query)
        if age_value < 5 or age_value > 50:
            return "Age must be between 5 and 50."
        return None

    # ==========================================
    # PHONE — DIGITS ONLY
    # ==========================================
    if field == "phone":
        if query.startswith("-"):
            return "Phone Number cannot be negative."
        if not query.isdigit():
            return "Please enter digits only for Phone."
        return None

    # ==========================================
    # FULL NAME — LETTERS AND SPACES ONLY
    # (no digits, no special characters)
    # ==========================================
    if field == "full_name":
        if not all(char.isalpha() or char.isspace() for char in query):
            return "Full Name can contain letters and spaces only."
        return None

    # ==========================================
    # GENDER — LETTERS ONLY, AND MUST BE THE START
    # OF ONE OF THE THREE VALID GENDER VALUES (so
    # "Mal", "fem", "Other" are fine, but random
    # text isn't).
    #
    # This must be a "starts with" check — NOT
    # "is contained anywhere" — because "male" is
    # literally a substring of "female" (Fe-male).
    # A "contains" check would let "male" validate
    # successfully but then also incorrectly match
    # Female students once it reaches the database
    # (see search_students() in student_service.py,
    # which uses the same starts-with rule).
    # ==========================================
    if field == "gender":
        if not query.isalpha():
            return "Please enter letters only for Gender."
        valid_genders = ("male", "female", "other")
        if not any(valid.startswith(query.lower()) for valid in valid_genders):
            return "Please enter a valid gender: Male, Female, or Other."
        return None

    # ==========================================
    # COURSE — LETTERS, SPACES, AND DOTS ONLY
    # (matches validate_course's allowed charset,
    # e.g. "B.Sc", "M.Com")
    # ==========================================
    if field == "course":
        if not all(char.isalpha() or char.isspace() or char == "." for char in query):
            return "Course can contain letters, spaces, and dots only."
        return None

    # ==========================================
    # EMAIL — LETTERS, DIGITS, AND THE HANDFUL OF
    # SYMBOLS THAT ACTUALLY APPEAR IN EMAIL
    # ADDRESSES (@ . _ -). This still allows a
    # partial search like "rahul101" or "@gmail"
    # while rejecting anything that could never be
    # part of a real email, like spaces or "#".
    # ==========================================
    if field == "email":
        if not re.match(r'^[\w.@-]+$', query):
            return "Email search can contain letters, numbers, and @ . _ - only."
        return None

    # ==========================================
    # ADDRESS — LETTERS, DIGITS, SPACES, AND BASIC
    # PUNCTUATION (real addresses legitimately
    # contain numbers, e.g. "221B Baker Street" or
    # "Flat 4, MG Road") — but no symbols like
    # @ # $ % that could never belong in one.
    # ==========================================
    if field == "address":
        if not re.match(r'^[A-Za-z0-9\s,./-]+$', query):
            return "Address can contain letters, numbers, spaces, and basic punctuation only (no symbols like @, #, or $)."
        return None

    return None