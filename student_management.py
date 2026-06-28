from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass
from pathlib import Path


# File locations used by the whole application.
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "students.csv"
JSON_FILE = BASE_DIR / "students.json"
LOG_FILE = BASE_DIR / "student_system.log"


class StudentRecordError(Exception):
    """Base exception for student record problems."""


class DuplicateRegistrationError(StudentRecordError):
    """Raised when a registration number already exists."""


class StudentNotFoundError(StudentRecordError):
    """Raised when a student record cannot be found."""


class ValidationError(StudentRecordError):
    """Raised when input validation fails."""


@dataclass
class StudentRecord:
    # Core fields live in the CSV file, while the extra fields are stored in JSON.
    reg_no: str
    first_name: str
    last_name: str
    age: str
    gender: str
    address: str
    contact: str
    program: str


def setup_logging() -> logging.Logger:
    """Configure file logging for user actions and system errors."""
    logger = logging.getLogger("student_system")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    )
    logger.addHandler(file_handler)
    return logger


LOGGER = setup_logging()


def ensure_storage_files() -> None:
    """Create the data files if they do not already exist."""
    if not CSV_FILE.exists():
        # Write the CSV header so the file is ready for student rows.
        with CSV_FILE.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=["reg_no", "first_name", "last_name", "age", "gender"],
            )
            writer.writeheader()

    if not JSON_FILE.exists():
        # Start the JSON file as an empty dictionary keyed by registration number.
        with JSON_FILE.open("w", encoding="utf-8") as json_file:
            json.dump({}, json_file, indent=4)


def load_students() -> dict[str, StudentRecord]:
    """Load and merge the CSV and JSON files into a single record dictionary."""
    records: dict[str, StudentRecord] = {}

    try:
        # Load the CSV first because it contains the main identity details.
        with CSV_FILE.open("r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                reg_no = row.get("reg_no", "").strip()
                if not reg_no:
                    continue
                records[reg_no] = StudentRecord(
                    reg_no=reg_no,
                    first_name=row.get("first_name", "").strip(),
                    last_name=row.get("last_name", "").strip(),
                    age=row.get("age", "").strip(),
                    gender=row.get("gender", "").strip(),
                    address="",
                    contact="",
                    program="",
                )
    except FileNotFoundError:
        LOGGER.error("CSV file was not found while loading records.")
    except csv.Error as exc:
        LOGGER.error("CSV read error: %s", exc, exc_info=True)

    try:
        # Overlay the JSON-only fields onto the same registration numbers.
        with JSON_FILE.open("r", encoding="utf-8") as json_file:
            extra_data = json.load(json_file)
            if isinstance(extra_data, dict):
                for reg_no, extras in extra_data.items():
                    if reg_no not in records:
                        records[reg_no] = StudentRecord(
                            reg_no=reg_no,
                            first_name="",
                            last_name="",
                            age="",
                            gender="",
                            address="",
                            contact="",
                            program="",
                        )
                    if isinstance(extras, dict):
                        records[reg_no].address = str(extras.get("address", "")).strip()
                        records[reg_no].contact = str(extras.get("contact", "")).strip()
                        records[reg_no].program = str(extras.get("program", "")).strip()
    except FileNotFoundError:
        LOGGER.error("JSON file was not found while loading records.")
    except json.JSONDecodeError as exc:
        LOGGER.error("JSON read error: %s", exc, exc_info=True)

    return records


def save_students(records: dict[str, StudentRecord]) -> None:
    """Persist the current records back to CSV and JSON."""
    try:
        # Rebuild the CSV file from the in-memory records.
        with CSV_FILE.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(
                csv_file,
                fieldnames=["reg_no", "first_name", "last_name", "age", "gender"],
            )
            writer.writeheader()
            for record in records.values():
                writer.writerow(
                    {
                        "reg_no": record.reg_no,
                        "first_name": record.first_name,
                        "last_name": record.last_name,
                        "age": record.age,
                        "gender": record.gender,
                    }
                )

        # Rebuild the JSON file from the same records so both files stay in sync.
        with JSON_FILE.open("w", encoding="utf-8") as json_file:
            extra_data = {
                record.reg_no: {
                    "address": record.address,
                    "contact": record.contact,
                    "program": record.program,
                }
                for record in records.values()
            }
            json.dump(extra_data, json_file, indent=4)
    except OSError as exc:
        LOGGER.error("Failed to save student files: %s", exc, exc_info=True)
        raise


def prompt_text(message: str, allow_empty: bool = False) -> str:
    """Read a text value from the user with simple validation."""
    while True:
        try:
            # Re-prompt until the user enters a non-empty value unless empties are allowed.
            value = input(message).strip()
            if value or allow_empty:
                return value
            raise ValidationError("This field cannot be empty.")
        except ValidationError as exc:
            print(exc)
            LOGGER.warning("Validation failed: %s", exc)


def prompt_age(message: str, allow_empty: bool = False) -> str:
    """Read and validate an age value."""
    while True:
        try:
            # Keep age input numeric so records remain consistent.
            value = input(message).strip()
            if not value and allow_empty:
                return value
            age = int(value)
            if age <= 0 or age > 120:
                raise ValidationError("Age must be between 1 and 120.")
            return str(age)
        except ValueError:
            print("Please enter a valid whole number for age.")
            LOGGER.warning("Invalid age input was entered.")
        except ValidationError as exc:
            print(exc)
            LOGGER.warning("Validation failed: %s", exc)


def prompt_contact(message: str, allow_empty: bool = False) -> str:
    """Read and validate a contact number."""
    while True:
        try:
            # Require a digit-only contact number with a reasonable minimum length.
            value = input(message).strip()
            if not value and allow_empty:
                return value
            if not value.isdigit() or len(value) < 7:
                raise ValidationError("Contact number must contain at least 7 digits.")
            return value
        except ValidationError as exc:
            print(exc)
            LOGGER.warning("Validation failed: %s", exc)


def prompt_gender(message: str, allow_empty: bool = False) -> str:
    """Read and validate gender input."""
    options = {"M", "F", "O"}
    while True:
        try:
            # Normalize the input so the stored value uses one consistent format.
            value = input(message).strip().upper()
            if not value and allow_empty:
                return value
            if value not in options:
                raise ValidationError("Enter M, F, or O for gender.")
            return value
        except ValidationError as exc:
            print(exc)
            LOGGER.warning("Validation failed: %s", exc)


def print_student(record: StudentRecord) -> None:
    """Display one student record in a friendly format."""
    # Keep the output aligned so each record is easy to scan.
    print("-" * 60)
    print(f"Registration Number : {record.reg_no}")
    print(f"Name                : {record.first_name} {record.last_name}")
    print(f"Age                 : {record.age}")
    print(f"Gender              : {record.gender}")
    print(f"Address             : {record.address}")
    print(f"Contact             : {record.contact}")
    print(f"Program             : {record.program}")


def add_student(records: dict[str, StudentRecord]) -> None:
    """Add a new student to the system."""
    print("\nAdd New Student")
    try:
        # Registration number is the unique key used across both storage files.
        reg_no = prompt_text("Enter registration number: ")
        if reg_no in records:
            raise DuplicateRegistrationError("A student with that registration number already exists.")

        record = StudentRecord(
            reg_no=reg_no,
            first_name=prompt_text("Enter first name: "),
            last_name=prompt_text("Enter last name: "),
            age=prompt_age("Enter age: "),
            gender=prompt_gender("Enter gender (M/F/O): "),
            address=prompt_text("Enter address: "),
            contact=prompt_contact("Enter contact number: "),
            program=prompt_text("Enter program: "),
        )
        records[reg_no] = record
        save_students(records)
        LOGGER.info("Added student %s", reg_no)
        print("Student record added successfully.")
    except StudentRecordError as exc:
        print(exc)
        LOGGER.error("Add student failed: %s", exc, exc_info=True)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        LOGGER.error("Unexpected add student error: %s", exc, exc_info=True)
    finally:
        print()


def view_students(records: dict[str, StudentRecord]) -> None:
    """Show all students currently stored in the system."""
    print("\nAll Students")
    try:
        # Handle the empty-state cleanly instead of printing a blank list.
        if not records:
            print("No student records found.")
            LOGGER.info("Viewed students: no records available")
            return

        # Sort by registration number to keep the list deterministic.
        for record in sorted(records.values(), key=lambda item: item.reg_no):
            print_student(record)
        print("-" * 60)
        LOGGER.info("Viewed all student records")
    except Exception as exc:
        print(f"Unable to display records: {exc}")
        LOGGER.error("View students error: %s", exc, exc_info=True)
    finally:
        print()


def search_student(records: dict[str, StudentRecord]) -> None:
    """Search for a student using the registration number."""
    print("\nSearch Student")
    try:
        # A registration number lookup is the fastest way to find one record.
        reg_no = prompt_text("Enter registration number to search: ")
        if reg_no not in records:
            raise StudentNotFoundError("Student record not found.")
        print_student(records[reg_no])
        LOGGER.info("Searched for student %s", reg_no)
    except StudentRecordError as exc:
        print(exc)
        LOGGER.error("Search student failed: %s", exc, exc_info=True)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        LOGGER.error("Unexpected search error: %s", exc, exc_info=True)
    finally:
        print()


def update_student(records: dict[str, StudentRecord]) -> None:
    """Update existing student information."""
    print("\nUpdate Student")
    try:
        reg_no = prompt_text("Enter registration number to update: ")
        if reg_no not in records:
            raise StudentNotFoundError("Student record not found.")

        record = records[reg_no]
        # Empty input keeps the current value so the user can edit only one field.
        print("Press Enter to keep the current value.")
        record.first_name = prompt_text(f"First name [{record.first_name}]: ", allow_empty=True) or record.first_name
        record.last_name = prompt_text(f"Last name [{record.last_name}]: ", allow_empty=True) or record.last_name
        record.age = prompt_age(f"Age [{record.age}]: ", allow_empty=True) or record.age
        record.gender = prompt_gender(f"Gender [{record.gender}] (M/F/O): ", allow_empty=True) or record.gender
        record.address = prompt_text(f"Address [{record.address}]: ", allow_empty=True) or record.address
        record.contact = prompt_contact(f"Contact [{record.contact}]: ", allow_empty=True) or record.contact
        record.program = prompt_text(f"Program [{record.program}]: ", allow_empty=True) or record.program

        save_students(records)
        LOGGER.info("Updated student %s", reg_no)
        print("Student record updated successfully.")
    except StudentRecordError as exc:
        print(exc)
        LOGGER.error("Update student failed: %s", exc, exc_info=True)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        LOGGER.error("Unexpected update error: %s", exc, exc_info=True)
    finally:
        print()


def delete_student(records: dict[str, StudentRecord]) -> None:
    """Delete a student record from both data files."""
    print("\nDelete Student")
    try:
        reg_no = prompt_text("Enter registration number to delete: ")
        if reg_no not in records:
            raise StudentNotFoundError("Student record not found.")

        # Ask for confirmation before removing the record permanently.
        confirmation = prompt_text("Are you sure you want to delete this record? (y/n): ").lower()
        if confirmation != "y":
            print("Delete cancelled.")
            LOGGER.info("Delete cancelled for student %s", reg_no)
            return

        del records[reg_no]
        save_students(records)
        LOGGER.info("Deleted student %s", reg_no)
        print("Student record deleted successfully.")
    except StudentRecordError as exc:
        print(exc)
        LOGGER.error("Delete student failed: %s", exc, exc_info=True)
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")
        LOGGER.error("Unexpected delete error: %s", exc, exc_info=True)
    finally:
        print()


def display_menu() -> None:
    """Print the main menu."""
    # The menu keeps the program interactive and simple for the user.
    print("Student Record Management System")
    print("1. Add a new student")
    print("2. View all students")
    print("3. Search for a student")
    print("4. Update student details")
    print("5. Delete a student record")
    print("6. Exit")


def main() -> None:
    """Run the menu-driven student management application."""
    # Make sure the storage files exist before any action tries to read or write them.
    ensure_storage_files()
    records = load_students()
    LOGGER.info("Application started")

    try:
        # Keep showing the menu until the user chooses to exit.
        while True:
            display_menu()
            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                add_student(records)
            elif choice == "2":
                view_students(records)
            elif choice == "3":
                search_student(records)
            elif choice == "4":
                update_student(records)
            elif choice == "5":
                delete_student(records)
            elif choice == "6":
                LOGGER.info("Application exited by user")
                print("Goodbye.")
                break
            else:
                # Invalid choices are handled locally so the loop can continue safely.
                print("Please choose a number between 1 and 6.\n")
                LOGGER.warning("Invalid menu choice: %s", choice)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        LOGGER.warning("Program interrupted by user")
    except Exception as exc:
        print(f"A system error occurred: {exc}")
        LOGGER.error("Fatal application error: %s", exc, exc_info=True)
    finally:
        LOGGER.info("Application closed")


if __name__ == "__main__":
    main()