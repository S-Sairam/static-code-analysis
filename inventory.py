"""
A simple command-line inventory management system.

This script allows users to add, remove, and track items in an inventory,
which is persisted to a JSON file. It avoids mutable global state by
passing the inventory data as function parameters.
"""
import json
import logging
from datetime import datetime

# Configure logging for informative output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def add_item(data, item, qty, logs=None):
    """
    Adds a specified quantity of an item to the stock data.

    Args:
        data (dict): The dictionary representing the inventory.
        item: The item to add.
        qty: The quantity of the item to add.
        logs (list, optional): A list to append log messages to. Defaults to None.
    """
    if logs is None:
        logs = []
    try:
        data[item] = data.get(item, 0) + qty
        logs.append(f"{datetime.now()}: Added {qty} of {item}")
        logging.info("Added %s of %s", qty, item)
    except TypeError:
        logging.error("Invalid data type for item or quantity. Could not add '%s'.", item)

def remove_item(data, item, qty):
    """
    Removes a specified quantity of an item from the stock data.

    Args:
        data (dict): The dictionary representing the inventory.
        item: The item to remove.
        qty: The quantity of the item to remove.
    """
    try:
        if item in data:
            data[item] -= qty
            if data[item] <= 0:
                del data[item]
            logging.info("Removed %s of %s", qty, item)
        else:
            logging.warning("Attempted to remove an item that does not exist: %s", item)
    except TypeError:
        logging.error("Invalid quantity type for item '%s'.", item)

def get_qty(data, item):
    """Returns the current quantity of a specified item from the stock data."""
    return data.get(item, 0)

def load_data(file="inventory.json"):
    """
    Loads stock data from a JSON file.

    Returns:
        dict: The loaded inventory data. Returns an empty dict on failure.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            logging.info("Inventory data loaded successfully from %s.", file)
            return json.load(f)
    except FileNotFoundError:
        logging.warning("%s not found. Starting with an empty inventory.", file)
        return {}
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from %s. Starting fresh.", file)
        return {}

def save_data(data, file="inventory.json"):
    """Saves the current stock data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        logging.info("Inventory data saved successfully to %s.", file)

def print_data(data):
    """Prints a formatted report of all items in the provided stock data."""
    print("\n--- Items Report ---")
    if not data:
        print("Inventory is empty.")
    else:
        for item, quantity in data.items():
            print(f"{item} -> {quantity}")
    print("--------------------\n")

def check_low_items(data, threshold=5):
    """Returns a list of items with quantities below the specified threshold."""
    return [item for item, quantity in data.items() if quantity < threshold]

def main():
    """Main function to initialize and run inventory management operations."""
    inventory_data = load_data()

    add_item(inventory_data, "apple", 10)
    add_item(inventory_data, "banana", 2)
    add_item(inventory_data, 123, "ten")
    remove_item(inventory_data, "apple", 3)
    remove_item(inventory_data, "orange", 1)

    print(f"Apple stock: {get_qty(inventory_data, 'apple')}")
    print(f"Low items: {check_low_items(inventory_data)}")

    save_data(inventory_data)
    print_data(inventory_data)

if __name__ == "__main__":
    main() 