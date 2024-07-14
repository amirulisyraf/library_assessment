from datetime import datetime
from prettytable import PrettyTable

class Customer:
    def __init__(self, id, name, address, contact_no):
        self.id = id
        self.name = name
        self.address = address
        self.contact_no = contact_no
        self.rentals = []

    def add_rental(self, book_name, author_name, rental_date, due_date):
        self.rentals.append({
            "book_name": book_name,
            "author_name": author_name,
            "rental_date": rental_date,
            "due_date": due_date
        })

    def edit_customer(self, name=None, address=None, contact_no=None):
        if name:
            self.name = name
        if address:
            self.address = address
        if contact_no:
            self.contact_no = contact_no

    def edit_rental(self, rental_index, book_name=None, author_name=None, rental_date=None, due_date=None):
        if rental_index < len(self.rentals):
            if book_name:
                self.rentals[rental_index]['book_name'] = book_name
            if author_name:
                self.rentals[rental_index]['author_name'] = author_name
            if rental_date:
                self.rentals[rental_index]['rental_date'] = rental_date
            if due_date:
                self.rentals[rental_index]['due_date'] = due_date
            return True
        return False

    def calculate_penalty(self):
        current_date = datetime.now().date()
        rentals_info = []

        for rental in self.rentals:
            due_date = datetime.strptime(rental["due_date"], "%d/%m/%y").date()
            if current_date > due_date:
                overdue_days = (current_date - due_date).days
                if overdue_days > 30:
                    penalty_amount = 5 * overdue_days  # RM 5 for each overdue day beyond 30 days
                elif overdue_days > 14:
                    penalty_amount = 4 * overdue_days  # RM 4 for each overdue day beyond 14 days
                elif overdue_days > 7:
                    penalty_amount = 3.5 * overdue_days  # RM 3.50 for each overdue day beyond 7 days
                elif overdue_days > 5:
                    penalty_amount = 2 * overdue_days  # RM 2 for each overdue day beyond 5 days
                else:
                    penalty_amount = 0  # No penalty for less than or equal to 5 days overdue

                rentals_info.append({
                    "book_name": rental["book_name"],
                    "author_name": rental["author_name"],
                    "penalty_amount": penalty_amount,
                    "overdue_days": overdue_days
                })

        return rentals_info

class Library:
    def __init__(self):
        self.customers = []
        self.next_id = 1  # Init next customer ID
        self.initialize_customers()

    def initialize_customers(self):
        init_customers = [
            {
                "name": "Ali",
                "address": "14, WDC, Washington DC",
                "contact_no": "+6012345678",
                "rentals": [
                    {
                        "book_name": "The Glass Castle",
                        "author_name": "Jeannette Walls",
                        "rental_date": "27/07/23",
                        "due_date": "27/06/24"
                    },
                    {
                        "book_name": "Lion King",
                        "author_name": "Ahmad Albab",
                        "rental_date": "27/07/23",
                        "due_date": "29/06/24"
                    }
                ]
            },
            {
                "name": "Abu",
                "address": "14, CA, California",
                "contact_no": "+6012345611",
                "rentals": [
                    {
                        "book_name": "Harry Potter",
                        "author_name": "J.K Rowling",
                        "rental_date": "09/05/24",
                        "due_date": "01/07/24"
                    },
                    {
                        "book_name": "Columbine",
                        "author_name": "Dave Cullen",
                        "rental_date": "09/07/24",
                        "due_date": "31/08/24"
                    }
                ]
            }
        ]

        for customer_data in init_customers:
            customer = Customer(self.next_id, customer_data["name"], customer_data["address"], customer_data["contact_no"])
            for rental in customer_data["rentals"]:
                customer.add_rental(rental["book_name"], rental["author_name"], rental["rental_date"], rental["due_date"])
            self.customers.append(customer)
            self.next_id += 1

    def add_customer(self, name, address, contact_no):
        customer = Customer(self.next_id, name, address, contact_no)
        self.customers.append(customer)
        self.next_id += 1  # Auto increment customer_id

    def edit_customer(self, customer_id, name=None, address=None, contact_no=None):
        for customer in self.customers:
            if customer.id == customer_id:
                customer.edit_customer(name, address, contact_no)
                return True
        return False

    def edit_rental(self, customer_id, rental_index, book_name=None, author_name=None, rental_date=None, due_date=None):
        for customer in self.customers:
            if customer.id == customer_id:
                return customer.edit_rental(rental_index, book_name, author_name, rental_date, due_date)
        return False

    def list_customers(self):
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Address", "Contact No", "Total Penalty Amount", "Book Name", "Author", "Rental Date", "Due Date", "Overdue Duration", "Penalty Amount", "Status"]
        
        current_date = datetime.now().date() # Today's date

        for customer in self.customers:
            rentals_info = customer.calculate_penalty()
            total_penalty_amount = sum(rental["penalty_amount"] for rental in rentals_info)
            
            for idx, rental in enumerate(customer.rentals):
                due_date = datetime.strptime(rental["due_date"], "%d/%m/%y").date()
                is_overdue = current_date > due_date
                if is_overdue:
                    penalty_info = next((info for info in rentals_info if info["book_name"] == rental["book_name"]), None)
                    penalty_amount = penalty_info["penalty_amount"]
                    overdue_days = penalty_info["overdue_days"]
                else:
                    penalty_amount = 0
                    overdue_days = 0

                status = "! Overdue !" if is_overdue else "OK"
                table.add_row([
                    customer.id if idx == 0 else "", 
                    customer.name if idx == 0 else "", 
                    customer.address if idx == 0 else "", 
                    customer.contact_no if idx == 0 else "", 
                    f"RM {total_penalty_amount:.2f}" if idx == 0 else "",  # Total penalty amount for each customer
                    rental["book_name"], 
                    rental["author_name"], 
                    rental["rental_date"], 
                    rental["due_date"], 
                    f"{overdue_days} days" if is_overdue else "",  # Overdue duration if overdue
                    f"RM {penalty_amount:.2f}",  # Penalty amount for each book
                    status
                ])

        print(table)


# Example usage
library = Library()

def main_menu():
    while True:
        option = ""
        while option not in ['1', '2', '3']:
            print("\n==================")
            print("BOOK RENTAL SYSTEM")
            print("==================")
            print("1) Add rental")
            print("2) Edit rental")
            print("3) List rental")            
            print("==================")
            option = input("Enter option: ")

        if option == '1':
            add_rental()
        elif option == '2':
            edit_rental()
        elif option == '3':
            list_rentals()

def add_rental():
    name = input("\nEnter name: ")
    address = input("Enter address: ")
    contact_no = input("Enter contact number: ")

    library.add_customer(name, address, contact_no)
    customer = library.customers[-1]  # Get last added customer

    while True:
        book_name = input("Enter book name: ")
        author_name = input("Enter author name: ")
        rental_date = input("Enter rental date (dd/mm/yy) <eg:14/07/24> : ")
        due_date = input("Enter due date (dd/mm/yy) <eg:14/07/24> : ")
        customer.add_rental(book_name, author_name, rental_date, due_date)

        cont = input("Continue to add book rental (press 1) or press any key to exit: ")
        if cont != '1':
            break

    print("\nRental added successfully.")


def edit_rental():
    list_rentals()
    print("\nEdit rental")
    print("---------------")
    customer_id = int(input("\nEnter customer ID: "))

    # Check if customer exists
    customer_exists = False
    customer = None
    for cust in library.customers:
        if cust.id == customer_id:
            customer_exists = True
            customer = cust
            break
    
    if not customer_exists:
        print(f"\nError: Customer with ID {customer_id} not found.")
        return

    edit_customer = input("\nDo you want to edit customer information (Y/N)? ").strip().lower()
    if edit_customer == 'y':
        new_name = input("Enter new name: ").strip()
        new_address = input("Enter new address: ").strip()
        new_contact_no = input("Enter new contact number: ").strip()

        # Edit customer information
        library.edit_customer(customer_id, name=new_name, address=new_address, contact_no=new_contact_no)
        print("\nCustomer information updated successfully.")

    # List book rented by the customer
    print("\nBooks rented by the customer")
    print("--------------------------------")
    for idx, rental in enumerate(customer.rentals):
        print(f"{idx + 1}. {rental['book_name']} by {rental['author_name']}")

    while True:
        try:
            selection = int(input("\nEnter the number of the book you want to edit (or 0 to skip): "))
            if 0 <= selection <= len(customer.rentals):
                break
            else:
                print("Invalid selection. Please enter a number from the list or 0 to skip.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    if selection == 0:
        print("\nNo rental selected to edit.")
        return

    book_name = input("Enter new book name: ").strip()
    author_name = input("Enter new author name: ").strip()
    rental_date = input("Enter new rental date (dd/mm/yy): ").strip()
    due_date = input("Enter new due date (dd/mm/yy): ").strip()

    success = library.edit_rental(customer_id, selection - 1, book_name, author_name, rental_date, due_date)
    if success:
        print("\nRental edited successfully.")
    else:
        print("\nError: Failed to edit rental.")


def list_rentals():
    print("\n")
    library.list_customers()

main_menu()
