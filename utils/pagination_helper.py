from utils.messages import error_message, success_message
from utils.validations import validate_pagination_choice


def paginate_records(records, display_function):

    # ======================================
    # CHECK EMPTY RECORDS
    # ======================================

    if len(records) == 0:
        error_message("No Records Found")
        return

    # ======================================
    # SINGLE RECORD
    # ======================================

    if len(records) == 1:
        success_message("There is only one record found:")
        display_function(records[0])
        return

    # ======================================
    # PAGINATION VARIABLES
    # ======================================

    current_index = 0

    total_records = len(records)

    # ======================================
    # PAGINATION LOOP
    # ======================================

    while True:

        # DISPLAY CURRENT RECORD
        display_function(records[current_index])

        # RECORD INFO
        print(
            f"\nRecord {current_index + 1} Of {total_records}"
        )

        # OPTIONS
        print("\n========== Options ==========")

        print("N -> Next Record")
        print("P -> Previous Record")
        print("E -> Exit")

        while True:
            # USER INPUT
            choice = input(
                "\nEnter Choice: "
            ).lower().strip()

            if validate_pagination_choice(choice):
                break

        # NEXT RECORD
        if choice == "n":

            if current_index == total_records - 1:
                error_message(
                    "Already On Last Record"
                )
            else:
                current_index += 1

        # PREVIOUS RECORD
        elif choice == "p":

            if current_index == 0:
                error_message(
                    "Already On First Record"
                )
            else:
                current_index -= 1

        # EXIT
        elif choice == "e":
            break

        # INVALID CHOICE
        else:

            error_message("Invalid Choice")