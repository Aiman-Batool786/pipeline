import pyodbc

# Use your local IP and the instance name
import pyodbc

# Use the IP and Port you just configured
SERVER = "192.168.1.30,1288" 
DATABASE = "ProductDB"

def create_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={SERVER};" 
            f"DATABASE={DATABASE};"
            f"UID=Aiman;"
            f"PWD=StrongPassword123!;"
            "TrustServerCertificate=yes;" # Keep this! Driver 18 requires it.
            "Connection Timeout=30;"
        )
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def create_table():
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects 
            WHERE name='products' AND xtype='U'
        )
        CREATE TABLE products (
            id INT IDENTITY(1,1) PRIMARY KEY,
            url NVARCHAR(MAX),
            title NVARCHAR(MAX),
            description NVARCHAR(MAX),
            improved_title NVARCHAR(MAX),
            improved_description NVARCHAR(MAX),
            bullet_points NVARCHAR(MAX),
            category_id INT,
            category_name NVARCHAR(255),
            confidence FLOAT
        )
        """)
        conn.commit()
        conn.close()

def insert_product(data):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        # Check for duplicate URL
        cursor.execute("SELECT COUNT(*) FROM products WHERE url = ?", data[0])
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute("""
            INSERT INTO products (
                url, title, description, 
                improved_title, improved_description, 
                bullet_points, 
                category_id, category_name, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            print("Product inserted successfully.")
        else:
            print("Product already exists, skipping:", data[0])
        conn.close()


# import pyodbc

# SERVER = "DESKTOP-M7OGK16\\SQLEXPRESS"
# DATABASE = "ProductDB"

# def create_connection():
#     conn = pyodbc.connect(
#     "DRIVER={ODBC Driver 18 for SQL Server};"
#     "SERVER=DESKTOP-M7OGK16\\SQLEXPRESS;"
#     "DATABASE=ProductDB;"
#     "UID=Aiman;"
#     "PWD=StrongPassword123!"
# )

#     return conn

# def create_table():
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("""
#     IF NOT EXISTS (
#         SELECT * FROM sysobjects
#         WHERE name='products' AND xtype='U'
#     )
#     CREATE TABLE products (
#         id INT IDENTITY(1,1) PRIMARY KEY,
#         url NVARCHAR(MAX),
#         title NVARCHAR(MAX),
#         description NVARCHAR(MAX),
#         improved_title NVARCHAR(MAX),
#         improved_description NVARCHAR(MAX),
#         bullet_points NVARCHAR(MAX),
#         category_id INT,
#         category_name NVARCHAR(255),
#         confidence FLOAT
#     )
#     """)
#     conn.commit()
#     conn.close()

# def insert_product(data):
#     conn = create_connection()
#     cursor = conn.cursor()

#     # Check for duplicate URL
#     cursor.execute("SELECT COUNT(*) FROM products WHERE url = ?", data[0])
#     count = cursor.fetchone()[0]

#     if count == 0:
#         cursor.execute("""
#         INSERT INTO products (
#             url, title, description,
#             improved_title, improved_description,
#             bullet_points,
#             category_id, category_name, confidence
#         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, data)
#         conn.commit()
#     else:
#         print("Product already exists, skipping:", data[0])

#     conn.close()


