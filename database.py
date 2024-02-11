import sqlite3

def create_table(table_name, schema_query):
    conn = sqlite3.connect('Blockchain_based_order_management_system.db')
    cursor = conn.cursor()

    # Define the table schema
    cursor.execute(schema_query)

    # Commit and close the connection
    conn.commit()
    conn.close()

# Function to create 'Sub_contracts_info' table
def create_sub_contracts_info_table():
    schema_query = '''
    CREATE TABLE IF NOT EXISTS Sub_Contractors_Information (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Item_name_AND_avalibality TEXT,
        Item_name_Production_capacity_cost TEXT
    )
    '''


    create_table('Sub_Contractors_Information', schema_query)

# Function to create 'customer' table
def create_customer_table():
    schema_query = '''
    CREATE TABLE IF NOT EXISTS Customer_Information (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Customer_name TEXT,
        Item_Name TEXT,
        Item_quantity INTEGER,
        Due_date TEXT,
        Contractor_name TEXT
    )
    '''


    create_table('Customer_Information', schema_query)

# Function to create 'OEM_Info_system' table
def create_oem_info_system_table():
    schema_query = '''
    CREATE TABLE IF NOT EXISTS Origional_Equipment_Manufacturer_Information (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Item_name TEXT,
        available_items INTEGER,
        Production_capacity INTEGER,
        Contractor_name TEXT,
        Cost INTEGER,
        Customer_ID INTEGER,
        Customer_name TEXT,
        C_Item_Name TEXT,
        Item_quantity INTEGER,
        Due_date TEXT
    )
    '''

    create_table('Origional_Equipment_Manufacturer_Information', schema_query)


# Call the functions to create the tables and insert dummy data
create_sub_contracts_info_table()
create_customer_table()
create_oem_info_system_table()
