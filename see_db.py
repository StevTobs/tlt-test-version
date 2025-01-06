# see_db.py

import os
import django
import sqlite3
import json
from datetime import datetime
from django.utils.dateparse import parse_datetime

# Step 1: Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tltApp.settings')  # Replace with your actual settings module

# Step 2: Initialize Django
django.setup()

# Now, import your Django models
from core.models import Province, Amphure, Tambon

def list_tables(db_path='db.sqlite3'):
    """
    Connects to the SQLite database and prints all table names.
    
    :param db_path: Path to the SQLite database file.
    """
    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Execute a query to retrieve all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if tables:
            print("Tables in the database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in the database.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Ensure the connection is closed even if an error occurs
        if connection:
            connection.close()

def show_table_details(table_name, db_path='db.sqlite3'):
    """
    Shows all rows and schema information for a given table in the specified SQLite database.

    :param table_name: Name of the table to inspect.
    :param db_path: Path to the SQLite database file (default: 'db.sqlite3').
    """
    connection = None
    try:
        # Connect to the database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # 1. Check if the table exists
        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
              AND name=?;
        """, (table_name,))
        
        table_found = cursor.fetchone()
        if not table_found:
            print(f"Table '{table_name}' does not exist in the database.")
            return

        # 2. Fetch and display all rows
        print(f"\n--- Data from '{table_name}' ---")
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print(f"No rows found in table '{table_name}'.")

        # 3. Fetch and display the schema (column definitions)
        print(f"\n--- Schema for '{table_name}' ---")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        # PRAGMA table_info returns:
        # (cid, name, type, notnull, dflt_value, pk)

        if columns:
            print("{:<5} {:<20} {:<15} {:<10} {:<15} {:<5}".format(
                "cid", "name", "type", "notnull", "default_value", "pk"
            ))
            for col in columns:
                cid, name, col_type, notnull, dflt_value, pk = col
                print("{:<5} {:<20} {:<15} {:<10} {:<15} {:<5}".format(
                    cid, name, col_type, notnull, str(dflt_value), pk
                ))
        else:
            print(f"No schema information found for '{table_name}'.")
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()

def test_area_data():
    """
    Tests and prints area data using Django ORM.
    """
    # List all provinces
    provinces = Province.objects.all()
    print(provinces[:5])
    for province in provinces[:5]:
        print("จังหวัด " + province.name_th)
        for amphure in province.amphures.all():
            print(f"  อำเภอ{amphure.name_th}")
            for tambon in amphure.tambons.all():
                print(f"    ตำบล{tambon.name_th}")

def load_json_data(json_file_path):
    """
    Loads data from a JSON file into the database using Django ORM.

    :param json_file_path: Path to the JSON file.
    """
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        return

    for province_data in data:
        # Parse datetime fields if they exist
        created_at = parse_datetime(province_data.get('created_at'))
        updated_at = parse_datetime(province_data.get('updated_at'))
        deleted_at = parse_datetime(province_data.get('deleted_at')) if province_data.get('deleted_at') else None

        # Create or update Province
        province, created = Province.objects.update_or_create(
            id=province_data['id'],
            defaults={
                'name_th': province_data['name_th'],
                'name_en': province_data['name_en'],
                'geography_id': province_data['geography_id'],
                'created_at': created_at,
                'updated_at': updated_at,
                'deleted_at': deleted_at,
            }
        )
        if created:
            print(f"Created Province: {province.name_en}")
        else:
            print(f"Updated Province: {province.name_en}")

        # Handle Amphure
        for amphure_data in province_data.get('amphure', []):
            amphure_created_at = parse_datetime(amphure_data.get('created_at'))
            amphure_updated_at = parse_datetime(amphure_data.get('updated_at'))
            amphure_deleted_at = parse_datetime(amphure_data.get('deleted_at')) if amphure_data.get('deleted_at') else None

            amphure, amphure_created = Amphure.objects.update_or_create(
                id=amphure_data['id'],
                defaults={
                    'name_th': amphure_data['name_th'],
                    'name_en': amphure_data['name_en'],
                    'province': province,
                    'created_at': amphure_created_at,
                    'updated_at': amphure_updated_at,
                    'deleted_at': amphure_deleted_at,
                }
            )
            if amphure_created:
                print(f"  Created Amphure: {amphure.name_en}")
            else:
                print(f"  Updated Amphure: {amphure.name_en}")

            # Handle Tambon
            for tambon_data in amphure_data.get('tambon', []):
                tambon_created_at = parse_datetime(tambon_data.get('created_at'))
                tambon_updated_at = parse_datetime(tambon_data.get('updated_at'))
                tambon_deleted_at = parse_datetime(tambon_data.get('deleted_at')) if tambon_data.get('deleted_at') else None

                tambon, tambon_created = Tambon.objects.update_or_create(
                    id=tambon_data['id'],
                    defaults={
                        'zip_code': tambon_data['zip_code'],
                        'name_th': tambon_data['name_th'],
                        'name_en': tambon_data['name_en'],
                        'amphure': amphure,
                        'lat': tambon_data.get('lat'),
                        'lng': tambon_data.get('lng'),
                        'created_at': tambon_created_at,
                        'updated_at': tambon_updated_at,
                        'deleted_at': tambon_deleted_at,
                    }
                )
                if tambon_created:
                    print(f"    Created Tambon: {tambon.name_en}")
                else:
                    print(f"    Updated Tambon: {tambon.name_en}")

    print("JSON data loaded successfully.")

def parse_datetime(dt_str):
    """
    Parses an ISO 8601 datetime string to a datetime object.

    :param dt_str: The datetime string.
    :return: datetime object or None.
    """
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except ValueError:
        print(f"Invalid datetime format: {dt_str}")
        return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Utility script for database operations.")
    parser.add_argument('--list-tables', action='store_true', help='List all tables in the database.')
    parser.add_argument('--show-table', type=str, help='Show details of a specific table.')
    parser.add_argument('--test-data', action='store_true', help='Test and display area data.')
    parser.add_argument('--load-json', type=str, help='Path to the JSON file to load data from.')

    args = parser.parse_args()

    if args.list_tables:
        list_tables()
    
    if args.show_table:
        show_table_details(args.show_table)
    
    if args.test_data:
        test_area_data()
    
    if args.load_json:
        load_json_data(args.load_json)

    # If no arguments are provided, run test_area_data by default
    if not any(vars(args).values()):
        test_area_data()
