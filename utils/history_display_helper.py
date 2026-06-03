from datetime import datetime

# FORMAT DATETIME
def format_datetime(date_time):

    dt = datetime.strptime(
        date_time,
        "%Y-%m-%d %H:%M:%S"
    )

    return dt.strftime(
        "%d-%m-%Y %I:%M:%S %p"
    )


def display_updated_history(record):

    print("\n========== Updated Students History ==========")

    print(f"Update ID   : {record['update_id']}")

    print(f"Roll No     : {record['roll_no']}")

    print(f"Old Name    : {record['old_full_name']}")

    print(f"Old Age     : {record['old_age']}")

    print(f"Old Gender  : {record['old_gender']}")

    print(f"Old Course  : {record['old_course']}")

    print(f"Old Email   : {record['old_email']}")

    print(f"Old Phone   : {record['old_phone']}")

    print(f"Old Address : {record['old_address']}")

    print(f"Updated At  : {format_datetime(record['updated_at'])}")
    
    print(f"Updated Field : {record['updated_field']}")
    
    print(f"New Value : {record['new_value']}")

    print("----------------------------------")


def display_deleted_history(record):

    print("\n========== Deleted Students History ==========")

    print(f"Delete ID   : {record['delete_id']}")

    print(f"Roll No     : {record['roll_no']}")

    print(f"Name        : {record['full_name']}")

    print(f"Age         : {record['age']}")

    print(f"Gender      : {record['gender']}")

    print(f"Course      : {record['course']}")

    print(f"Email       : {record['email']}")

    print(f"Phone       : {record['phone']}")

    print(f"Address     : {record['address']}")

    print(f"Deleted At  : {format_datetime(record['deleted_at'])}")

    print("----------------------------------")