import sqlite3
import json  # Added import for JSON handling

def connect_database():
    conn = sqlite3.connect('Blockchain_based_order_management_system.db')
    return conn

def insert_into_Sub_contracts_info(name, item_availability, item_production_capacity_cost):
    conn = connect_database()
    cursor = conn.cursor()

    # Convert dictionaries to JSON strings for storage
    availability_json = json.dumps(item_availability)
    capacity_cost_json = json.dumps(item_production_capacity_cost)

    data = f"INSERT INTO Sub_Contractors_Information (Name, Item_name_AND_avalibality, Item_name_Production_capacity_cost) VALUES ('{name}', '{availability_json}', '{capacity_cost_json}')"

    cursor.execute(data)
    conn.commit()
    conn.close()

# Example usage:
insert_into_Sub_contracts_info('Contractor_1', {'Product_A': {'quantity': 2, 'cost': 3}, 'Product_B': {'quantity': 6, 'cost': 5}, 'Product_N': {'quantity': 1, 'cost': 5}}, {'Product_A': {'capacity': 4, 'cost': 7}, 'Product_B': {'capacity': 1, 'cost': 2}, 'Product_N': {'capacity': 9, 'cost': 1}})
insert_into_Sub_contracts_info('Contractor_2', {'Product_C': {'quantity': 3, 'cost': 4}, 'Product_B': {'quantity': 1, 'cost': 8}, 'Product_N': {'quantity': 2, 'cost': 5}}, {'Product_C': {'capacity': 6, 'cost': 4}, 'Product_B': {'capacity': 8, 'cost': 3}, 'Product_N': {'capacity': 7, 'cost': 6}})
insert_into_Sub_contracts_info('Contractor_3', {'Product_A': {'quantity': 5, 'cost': 5}, 'Product_C': {'quantity': 2, 'cost': 3}, 'Product_N': {'quantity': 5, 'cost': 5}}, {'Product_A': {'capacity': 6, 'cost': 1}, 'Product_C': {'capacity': 9, 'cost': 5}, 'Product_N': {'capacity': 7, 'cost': 7}})
insert_into_Sub_contracts_info('Contractor_N', {'Product_A': {'quantity': 10, 'cost': 5}, 'Product_B': {'quantity': 7, 'cost': 4}, 'Product_C': {'quantity': 6, 'cost': 5}, 'Product_N': {'capacity': 2, 'cost': 6}}, {'Product_A': {'capacity': 9, 'cost': 4}, 'Product_B': {'capacity': 3, 'cost': 5}, 'Product_C': {'capacity': 5, 'cost': 5}, 'Product_N': {'capacity': 2, 'cost': 5}})
