import argparse
import sqlite3
import json
from database import *

def connect_database():
    conn = sqlite3.connect('Blockchain_based_order_management_system.db')
    cursor = conn.cursor()
    return cursor

def insert_into_customer_info(customer_name, item_name, item_quantity, due_date):
    cursor = connect_database()
    data = f"INSERT INTO Customer_Information (Customer_name, Item_Name, Item_quantity, Due_date) VALUES ('{customer_name}', '{item_name}', {item_quantity}, '{due_date}')"
    cursor.execute(data)
    cursor.connection.commit()
    cursor.connection.close()

    return data

def oem_information_system(customer_name, item_name, item_quantity, due_date):
    # Call insert_into_customer_info from within oem_information_system
    data = insert_into_customer_info(customer_name, item_name, item_quantity, due_date)
    print(f"Value of data[1]: {item_name}")

    cursor = connect_database()
    # Use a parameterized query to avoid SQL injection
    cursor.execute("SELECT available_items, Production_capacity FROM Origional_Equipment_Manufacturer_Information WHERE Item_name = ?", (item_name,))
    result = cursor.fetchone()

    if result:
        available_items, production_capacity = result

        # Sum the available_items and Production_capacity
        total_items = available_items + production_capacity

        # Calculate the resulting quantity
        resulting_quantity = total_items - item_quantity

        print(f'resulting_quantity: {resulting_quantity}')

        if resulting_quantity < 0:
            # Call off_chain_computation function if resulting quantity is negative
            off_chain_computation(customer_name, item_name, item_quantity, due_date, resulting_quantity)
        else:
            # Call on_chain_smart_contract function if resulting quantity is non-negative
            remaining_item = available_items - item_quantity
            on_chain_smart_contract(customer_name, item_name, item_quantity, due_date, remaining_item)

def on_chain_smart_contract(customer_name, item_name, item_quantity, due_date, remaining_item):
    print('on chain smart contract')
    print(f'Customer_name: {customer_name}, Item_name: {item_name}, Item_quantity: {item_quantity}, Due_date: {due_date}, Remaining_item: {remaining_item}')

    cursor = connect_database()
    # Update the OEM_Info_system table with new values
    cursor.execute("UPDATE Origional_Equipment_Manufacturer_Information SET available_items = ?, Customer_name = ?, C_Item_Name = ?, Item_quantity = ?, Due_date = ? WHERE Item_name = ?", 
                   (remaining_item, customer_name, item_name, item_quantity, due_date, item_name))
    cursor.connection.commit()

def off_chain_computation(customer_name, item_name, item_quantity, due_date, resulting_quantity):
    print('off chain computation')
    print(f'Customer_name: {customer_name}, Item_name: {item_name}, Item_quantity: {item_quantity}, Due_date: {due_date}, Resulting_quantity: {resulting_quantity}')

    cursor = connect_database()
    # Search for item name in the Item_name_AND_avalibality column
    cursor.execute("SELECT ID, Name, Item_name_AND_avalibality, Item_name_Production_capacity_cost FROM Sub_Contractors_Information WHERE Item_name_AND_avalibality LIKE ?", (f'%{item_name}%',))
    matching_rows = cursor.fetchall()

    lowest_cost_contractor = None
    lowest_cost = float('inf')  # Set to positive infinity initially

    for row in matching_rows:
        contractor_id, contractor_name, item_avalibality_json, item_production_capacity_cost_json = row
        item_avalibality = json.loads(item_avalibality_json).get(item_name, {})
        item_production_capacity_cost = json.loads(item_production_capacity_cost_json).get(item_name, {})

        # Check if the contractor has the specified item
        if item_avalibality:
            cost = item_avalibality.get('cost', float('inf'))  # Get the cost value, default to positive infinity if not present

            # Update lowest cost and contractor if the current cost is lower
            if cost < lowest_cost:
                lowest_cost = cost
                lowest_cost_contractor = (contractor_id, contractor_name, item_avalibality, item_production_capacity_cost)

    if lowest_cost_contractor:
        contractor_id, contractor_name, item_avalibality, item_production_capacity_cost = lowest_cost_contractor
        print(f'Lowest Cost Contractor - Contractor ID: {contractor_id}, Contractor Name: {contractor_name}')
        print(f'Item_name_AND_avalibality: {item_avalibality}')
        print(f'Item_name_Production_capacity_cost: {item_production_capacity_cost}')
        print('-' * 50)

        # Update the specified columns in the OEM_Info_system table for the specific item
        cursor.execute("UPDATE Origional_Equipment_Manufacturer_Information SET available_items = ?, Customer_name = ?, C_Item_Name = ?, Item_quantity = ?, Due_date = ?, Contractor_name = ?, Cost = ? WHERE Item_name = ?", 
                       (0, customer_name, item_name, item_quantity, due_date, contractor_name, item_avalibality['cost'], item_name))
        cursor.connection.commit()

        # Update the specified columns in the customer table for the specific item
        cursor.execute("UPDATE Customer_Information SET Contractor_name = ? WHERE Item_Name = ?", (contractor_name, item_name))
        cursor.connection.commit()
    else:
        print('No contractor found with the specified item.')


def main():

    print('WELCOME TO MY BLOCK CHAIN SYSTEM')

    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--Customer_name', type=str, help='Customer name')
    parser.add_argument('--Item_Name', type=str, help='Item name')
    parser.add_argument('--Item_quantity', type=int, help='Item quantity')
    parser.add_argument('--Due_date', type=str, help='Due date')

    args = parser.parse_args()

    if any(vars(args).values()):
        oem_information_system(args.Customer_name, args.Item_Name, args.Item_quantity, args.Due_date)
    else:
        print("No arguments provided.")

if __name__ == "__main__":
    main()

