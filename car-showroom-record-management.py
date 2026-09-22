import json
import os

DATA_FILE = "cars.json"


def load_records():
    """Load car records from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Invalid data format. Starting with an empty record list.")
            return []

        return data

    except json.JSONDecodeError:
        print("The JSON file is malformed. Starting with an empty record list.")
        return []

    except OSError as error:
        print(f"Unable to read the data file: {error}")
        return []


def save_records(records):
    """Save car records to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

    except OSError as error:
        print(f"Unable to save records: {error}")


def get_non_empty_input(prompt):
    """Read a required text value."""
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_non_negative_float(prompt):
    """Read a non-negative floating-point number."""
    while True:
        try:
            value = float(input(prompt).strip())

            if value < 0:
                print("Value cannot be negative.")
            else:
                return value

        except ValueError:
            print("Please enter a valid non-negative number.")


def get_non_negative_integer(prompt):
    """Read a non-negative integer."""
    while True:
        try:
            value = int(input(prompt).strip())

            if value < 0:
                print("Value cannot be negative.")
            else:
                return value

        except ValueError:
            print("Please enter a valid non-negative integer.")


def get_existing_car_id(records, prompt="Enter car ID: "):
    """Read an existing car ID."""
    while True:
        try:
            car_id = int(input(prompt).strip())

        except ValueError:
            print("Please enter a valid car ID.")
            continue

        if any(car["id"] == car_id for car in records):
            return car_id

        print("Car record not found.")


def get_new_car_id(records):
    """Read a unique car ID."""
    while True:
        try:
            car_id = int(input("Enter car ID: ").strip())

            if car_id < 0:
                print("Car ID cannot be negative.")
                continue

            if any(car["id"] == car_id for car in records):
                print("This car ID already exists.")
                continue

            return car_id

        except ValueError:
            print("Please enter a valid car ID.")


def add_car(records):
    """Add a new car record."""

    car = {
        "id": get_new_car_id(records),
        "brand": get_non_empty_input("Enter car brand: "),
        "model": get_non_empty_input("Enter car model: "),
        "price": get_non_negative_float("Enter car price: "),
        "stock": get_non_negative_integer("Enter stock quantity: ")
    }

    records.append(car)
    save_records(records)

    print("Car record added successfully.")


def view_cars(records):
    """Display all car records."""

    if not records:
        print("No car records available.")
        return

    print("\nCar Records")
    print("-" * 50)

    for car in records:
        print(f"ID: {car['id']}")
        print(f"Brand: {car['brand']}")
        print(f"Model: {car['model']}")
        print(f"Price: {car['price']:.2f}")
        print(f"Stock: {car['stock']}")
        print("-" * 50)


def search_car(records):
    """Search for a car by ID, brand, or model."""

    if not records:
        print("No car records available.")
        return

    search_value = input(
        "Enter car ID, brand, or model to search: "
    ).strip().lower()

    matches = []

    for car in records:
        if (
            str(car["id"]) == search_value
            or search_value in car["brand"].lower()
            or search_value in car["model"].lower()
        ):
            matches.append(car)

    if not matches:
        print("No matching car records found.")
        return

    print("\nMatching Car Records")
    print("-" * 50)

    for car in matches:
        print(f"ID: {car['id']}")
        print(f"Brand: {car['brand']}")
        print(f"Model: {car['model']}")
        print(f"Price: {car['price']:.2f}")
        print(f"Stock: {car['stock']}")
        print("-" * 50)


def update_car(records):
    """Update an existing car record."""

    if not records:
        print("No car records available.")
        return

    car_id = get_existing_car_id(
        records,
        "Enter car ID to update: "
    )

    for car in records:
        if car["id"] == car_id:
            print("Enter the new details.")

            car["brand"] = get_non_empty_input(
                "Enter new car brand: "
            )

            car["model"] = get_non_empty_input(
                "Enter new car model: "
            )

            car["price"] = get_non_negative_float(
                "Enter new car price: "
            )

            car["stock"] = get_non_negative_integer(
                "Enter new stock quantity: "
            )

            save_records(records)

            print("Car record updated successfully.")
            return


def delete_car(records):
    """Delete an existing car record after confirmation."""

    if not records:
        print("No car records available.")
        return

    car_id = get_existing_car_id(
        records,
        "Enter car ID to delete: "
    )

    confirmation = input(
        "Are you sure you want to delete this record? (y/n): "
    ).strip().lower()

    if confirmation not in ("y", "yes"):
        print("Deletion cancelled.")
        return

    for car in records:
        if car["id"] == car_id:
            records.remove(car)
            save_records(records)

            print("Car record deleted successfully.")
            return


def display_menu():
    """Display the main menu."""

    print("\n====================================")
    print("       CAR SHOWROOM MANAGEMENT")
    print("====================================")
    print("1. Add Car")
    print("2. View Cars")
    print("3. Search Car")
    print("4. Update Car")
    print("5. Delete Car")
    print("6. Exit")
    print("====================================")


def main():
    """Run the car showroom management system."""

    records = load_records()

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_car(records)

        elif choice == "2":
            view_cars(records)

        elif choice == "3":
            search_car(records)

        elif choice == "4":
            update_car(records)

        elif choice == "5":
            delete_car(records)

        elif choice == "6":
            print("Exiting the application.")
            break

        else:
            print(
                "Invalid choice. Please select a number from 1 to 6."
            )


if __name__ == "__main__":
    main()
