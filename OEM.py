import sqlite3

def connect_database():
    conn = sqlite3.connect('Blockchain_based_order_management_system.db')
    return conn

def insert_into_OEM_info_system(item_name, available_items, production_capacity):
    conn = connect_database()
    cursor = conn.cursor()

    data = f"INSERT INTO Origional_Equipment_Manufacturer_Information (Item_name, available_items, Production_capacity) VALUES ('{item_name}', {available_items}, {production_capacity})"

    cursor.execute(data)
    conn.commit()
    conn.close()

# Example usage:
insert_into_OEM_info_system('Product_A', 2, 1)
insert_into_OEM_info_system('Product_B', 5, 3)
insert_into_OEM_info_system('Product_C', 7, 5)
insert_into_OEM_info_system('Product_N', 3, 9)

