class ContactManager:
    def __init__(self):
        # Each contact is a dict: {"name": ..., "phone": ..., "email": ...}
        self.contacts = []

    # Validation helpers

    def _is_valid_phone(self, phone: str) -> bool:
        """
        Phone must contain only digits, hyphens, and optionally leading '+'.
        Example: "+256-701"
        """
        if not phone:
            return False

        # Allow leading '+'
        if phone[0] == '+':
            core = phone[1:]
        else:
            core = phone

        for ch in core:
            if not (ch.isdigit() or ch == '-'):
                return False
        return True

    def _is_valid_email(self, email: str | None) -> bool:
        """
        Email is valid if:
        - It is empty/None (optional field), OR
        - It contains both '@' and '.'
        """
        if not email:
            return True
        return ('@' in email) and ('.' in email)

    # Core CRUD operations

    def add_contact(self, name: str, phone: str, email: str | None = None) -> None:
        """Add a new contact after validation."""
        if not self._is_valid_phone(phone):
            print("Error: Phone number can only contain digits, hyphens, and optional leading '+'.")
            return

        if not self._is_valid_email(email):
            print("Error: Invalid email format. Email must contain '@' and '.'.")
            return

        self.contacts.append({
            "name": name.strip(),
            "phone": phone.strip(),
            "email": email.strip() if email else ""
        })
        print("Contact added successfully.")

    def list_contacts(self) -> list[dict]:
        """Return all contacts."""
        return self.contacts

    def view_contact(self, name: str) -> dict | None:
        """Return the first contact that matches the given name (case-insensitive)."""
        name = name.strip().lower()
        for c in self.contacts:
            if c["name"].lower() == name:
                return c
        return None

    def update_contact(self, old_name: str, new_name: str | None = None,
                       new_phone: str | None = None, new_email: str | None = None) -> None:
        """Update an existing contact by name."""
        contact = self.view_contact(old_name)
        if not contact:
            print("Contact not found.")
            return

        # Validate phone if provided
        if new_phone is not None:
            if not self._is_valid_phone(new_phone):
                print("Error: Phone number can only contain digits, hyphens, and optional leading '+'.")
                return

        # Validate email if provided
        if new_email is not None:
            if not self._is_valid_email(new_email):
                print("Error: Invalid email format. Email must contain '@' and '.'.")
                return

        if new_name is not None and new_name.strip():
            contact["name"] = new_name.strip()
        if new_phone is not None and new_phone.strip():
            contact["phone"] = new_phone.strip()
        if new_email is not None:
            contact["email"] = new_email.strip()

        print("Contact updated successfully.")

    def delete_contact(self, name: str) -> None:
        """Delete a contact by name."""
        name = name.strip().lower()
        for i, c in enumerate(self.contacts):
            if c["name"].lower() == name:
                del self.contacts[i]
                print("Contact deleted successfully.")
                return
        print("Contact not found.")

    #Advanced search

    def search_contacts(self, query: str) -> list[dict]:
        """Search contacts by name, phone, or email (case-insensitive)."""
        query = query.strip().lower()
        results = []
        for c in self.contacts:
            if (query in c["name"].lower()
                or query in c["phone"].lower()
                or query in c["email"].lower()):
                results.append(c)
        return results

    def print_contacts(self, contacts: list[dict]) -> None:
        """Nicely formatted printout of a list of contacts."""
        if not contacts:
            print("No contacts found.")
            return

        print("\nContacts")
        for idx, c in enumerate(contacts, start=1):
            print(f"{idx}. Name : {c['name']}")
            print(f"   Phone: {c['phone']}")
            print(f"   Email: {c['email'] if c['email'] else '(none)'}")
        print("----------------\n")


#CLI Menu 

def main():
    manager = ContactManager()

    while True:
<<<<<<< HEAD
        print("=== Contact Manager Menu ===")
=======
        print(" Contact Manager Menu ")
>>>>>>> 5c2d582 (added assignment)
        print("1. Add Contact")
        print("2. View Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. Search Contacts")
        print("6. List All Contacts")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            # Add Contact
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email (optional): ").strip()
            email = email if email else None
            manager.add_contact(name, phone, email)

        elif choice == "2":
            # View Contact
            name = input("Enter name to view: ").strip()
            contact = manager.view_contact(name)
            if contact:
                manager.print_contacts([contact])
            else:
                print("Contact not found.")

        elif choice == "3":
            # Update Contact
            old_name = input("Enter the name of the contact to update: ").strip()
            print("Leave a field blank to keep it unchanged.")
            new_name = input("New name (or press Enter to keep current): ").strip()
            new_phone = input("New phone (or press Enter to keep current): ").strip()
            new_email = input("New email (or press Enter to keep current): ").strip()

            manager.update_contact(
                old_name,
                new_name if new_name else None,
                new_phone if new_phone else None,
                new_email if new_email else None
            )

        elif choice == "4":
            # Delete Contact
            name = input("Enter name of contact to delete: ").strip()
            manager.delete_contact(name)

        elif choice == "5":
            # Search Contacts
            query = input("Enter search term (name, phone, or email): ").strip()
            results = manager.search_contacts(query)
            manager.print_contacts(results)

        elif choice == "6":
            # List All Contacts
            all_contacts = manager.list_contacts()
            manager.print_contacts(all_contacts)

        elif choice == "7":
            print("Exiting Contact Manager. Goodbye!")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 7.")

        input("Press Enter to continue...")  # Pause before showing menu again
        print()


if __name__ == "__main__":
    main()
