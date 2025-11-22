import psycopg
from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
# Load environment variables
load_dotenv()

# Get the connection string from environment
CONNECTION_STRING = os.getenv("CONNECTION_STRING")

def connect_to_database():
    try:
        conn = psycopg.connect(CONNECTION_STRING)
        print("✅ Successfully connected to Neon database!")
        
        # Get server version
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"Server version: {version[:50]}...")
        return conn
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nMake sure you created a .env file with your CONNECTION_STRING")

def generate_chat_completion(prompt):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def format_dataframe_for_insertion(df):
    """
    Format DataFrame data for database insertion.
    
    Converts a pandas DataFrame to a list of tuples, where each tuple represents
    a row of data ready for database insertion using parameterized queries.
    """
    # Convert DataFrame to list of tuples
    # Each row becomes a tuple of values in column order
    formatted_data = [tuple(row) for row in df.values]
    
    return formatted_data

def drop_all_tables():
    """
    Drop all tables from the database.
    
    This function connects to the database, retrieves all table names,
    and drops them one by one. It handles foreign key constraints by
    using CASCADE option.
    
    Returns:
        str: Success or error message
    """
    try:
        conn = connect_to_database()
        
        if conn is None:
            return "❌ Failed to connect to the database"
        
        with conn.cursor() as cur:
            # Get all table names from the current database
            cur.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            
            tables = cur.fetchall()
            
            # Drop each table with CASCADE to handle foreign key constraints
            dropped_tables = []
            for table in tables:
                table_name = table[0]
                try:
                    cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")
                    dropped_tables.append(table_name)
                except Exception as e:
                    print(f"❌ Failed to drop table {table_name}: {e}")
            
            conn.commit()
            
            if dropped_tables:
                print(f"✅ Successfully dropped {len(dropped_tables)} tables: {', '.join(dropped_tables)}")
                return f"Successfully dropped {len(dropped_tables)} tables"
            else:
                return "No tables were dropped"
                
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return f"Error dropping tables: {e}"
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def upload_data(df):

    create_table_prompt = """
    Using the sample data below, create a SQL query to create a table in the database. Return ONLY the SQL query, no other text. Make sure not to include "```sql" or "```" at the beginning or end of the query.

    Sample SQL query:
    CREATE TABLE IF NOT EXISTS table_name (
        column1 data_type,
        column2 data_type,
        column3 data_type,
        ...
    );

    Sample data:
    {df}
    """

    insert_data_prompt = """
    Using the table definition below, create a SQL query to insert the data into the table. Return ONLY the SQL query, no other text. Make sure not to include "```sql" or "```" at the beginning or end of the query.

    Table definition:
    {table_definition}

    Sample SQL query:
    INSERT INTO table_name (column1, column2, column3, ...) VALUES (%s, %s, %s, ...);
    """
    # Format the prompt with the sample data
    prompt = create_table_prompt.format(df=df.head().to_markdown())

    # Get the create table query from the LLM
    create_table_query = generate_chat_completion(prompt)

    # Format the prompt with the table definition
    insert_data_prompt = insert_data_prompt.format(table_definition=create_table_query)

    # Get the insert data query from the LLM
    insert_data_query = generate_chat_completion(insert_data_prompt)

    # Convert the dataframe to the proper format for database insertion
    formatted_data = format_dataframe_for_insertion(df)

    print(formatted_data[:5])

    # Execute the SQL query
    conn = connect_to_database()

    if conn is not None:
        with conn.cursor() as cur:
            try:
                cur.execute(create_table_query)
                cur.executemany(insert_data_query, formatted_data)
                conn.commit()
                print("✅ SQL queries executed successfully!")
            except Exception as e:
                print(f"❌ Failed to execute SQL queries: {e}")
    else:
        print("❌ Failed to connect to the database")
    return "Data uploaded successfully! Click on the button below to continue."

def get_database_schema():
    """
    Retrieve the database schema as a formatted string.
    
    This function connects to the database and executes a query to get
    information about all tables and their columns in the public schema.
    
    Returns:
        str: Formatted string containing the database schema information,
             or error message if the operation fails
    """
    try:
        conn = connect_to_database()
        
        if conn is None:
            return "❌ Failed to connect to the database"
        
        with conn.cursor() as cur:
            # Execute the schema query
            schema_query = """
            SELECT 
                table_name, 
                column_name, 
                data_type, 
                character_maximum_length,
                column_default,
                is_nullable
            FROM 
                information_schema.columns
            WHERE 
                table_schema = 'public'
            ORDER BY 
                table_name, 
                ordinal_position;
            """
            
            cur.execute(schema_query)
            results = cur.fetchall()
            
            if not results:
                return "No tables found in the public schema"
            
            # Format the results into a readable string
            schema_str = "DATABASE SCHEMA\n" + "="*50 + "\n\n"
            current_table = None
            
            for row in results:
                table_name, column_name, data_type, max_length, default_value, is_nullable = row
                
                # Add table header when we encounter a new table
                if current_table != table_name:
                    if current_table is not None:
                        schema_str += "\n"
                    schema_str += f"Table: {table_name}\n"
                    schema_str += "-" * (len(table_name) + 7) + "\n"
                    current_table = table_name
                
                # Format column information
                type_info = data_type
                if max_length:
                    type_info += f"({max_length})"
                
                nullable = "NULL" if is_nullable == "YES" else "NOT NULL"
                default_info = f", DEFAULT: {default_value}" if default_value else ""
                
                schema_str += f"  {column_name:<30} {type_info:<20} {nullable}{default_info}\n"
            
            return schema_str
                
    except Exception as e:
        error_msg = f"❌ Error retrieving database schema: {e}"
        print(error_msg)
        return error_msg
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()

    