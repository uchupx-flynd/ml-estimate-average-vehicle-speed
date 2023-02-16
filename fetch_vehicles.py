from dotenv import dotenv_values
import mysql.connector
import csv
from mysql.connector import Error


config = dotenv_values(".env")
field_names = ['id', 'company_id', 'product_category_id', 'vendor_id', 'geozone_id', 'contract_id', 'pool_id', 'vehicle_model_id', 'year', 'license_plate', 'mileage', 'last_odometer_update_id', 'required_license', 'status',
               'created_by', 'updated_by', 'created_at', 'updated_at', 'deleted_at', 'deleted_by', 'expiration_date', 'keur_number', 'keur_expiry_date', 'rating', 'vehicle_import_id', 'organization_id', 'specification_id', 'old_model_id']
vehicles = None


try:
    connection = mysql.connector.connect(
        host=config['HOST'],
        port=config['PORT'],
        database=config['DATABASE'],
        user=config['USERNAME'],
        password=config['PASSWORD'],
    )

    if connection.is_connected():
        sql_select_Query = "SELECT * FROM vehicles WHERE deleted_at IS NULL OR deleted_by IS NULL"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query)
        # get all records
        vehicles = cursor.fetchall()
        print("Total number of rows in table: ", cursor.rowcount)

except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

with open('data/vehicles.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(vehicles)
# print(config['DATABASE'])
