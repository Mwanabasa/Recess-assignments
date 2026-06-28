# Student Record Management System Report

## Program Design
The application is a menu-driven Python program that manages student records across two file formats. Core student fields such as registration number, names, age, and gender are stored in a CSV file, while extra details such as address, contact, and program are stored in a JSON file. The program loads both files into memory, merges them by registration number, and writes updates back to both files after each change.

## Key Functions
The main functions are `add_student`, `view_students`, `search_student`, `update_student`, and `delete_student`. Supporting functions handle loading and saving data, input validation, menu display, and logging setup. The program also includes a `StudentRecord` data class to keep each student’s information organized and easy to update.

## Exception Handling Strategy
The system uses `try`, `except`, and `finally` throughout the code. Custom exceptions were added for duplicate registration numbers, missing student records, and validation problems. File errors, invalid input, and unexpected failures are caught and written to `student_system.log` so that the application does not crash unexpectedly and the user gets a clear message.

## Testing Results
The program was tested with valid and invalid menu selections, successful student searches, duplicate registration checks, update operations, delete confirmation, and invalid age/contact input. The tests showed that valid records are saved correctly, invalid input is rejected with friendly messages, and both user actions and system errors are recorded in the log file.