import base64
import os
from db_connection import get_connection

# Functions for managing products
def add_product(name, price, description, image_url=None):
    """
    Adds a new product to the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO products (name, price, description, image_url) VALUES (?, ?, ?, ?)"
    params = (name, price, description, image_url)
    print(f"SQL Query: {sql}")
    print(f"Parameters: {params}")
    cursor.execute(sql, params)
    conn.commit()
    cursor.close()
    conn.close()
    
def delete_product(product_id, image_url):
    """
    Deletes a product from the database and removes its associated image file.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Step 1: Delete related comments
    cursor.execute("DELETE FROM comments WHERE product_id=?", (product_id,))

    # Step 2: Delete the product
    cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

    # Step 3: Delete the image file if it exists
    if image_url:
        image_path = os.path.join("static/uploads", os.path.basename(image_url))
        try:
            os.remove(image_path)
        except FileNotFoundError:
            print(f"Image not found: {image_path}")
        except Exception as e:
            print(f"Error deleting image: {e}")

def update_product(product_id, name, price, description, image_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name=?, price=?, description=?, image_url=? WHERE id=?",
                   (name, price, description, image_url, product_id))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_products():
    """
    Retrieves all products from the database.
    """
    conn = get_connection()  # Get the database connection
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description, image_url FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    products = []
    for row in rows:
        product = {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
            "image_url": row[4]
        }
        products.append(product)
    return products

def fetch_product_by_id(product_id):
    """
    Retrieves a product based on its ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description, image_url FROM products WHERE id=?", (product_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "description": row[3],
            "image_url": row[4]
        }
    return None

def save_image_to_db(image_content):
    """
    Processes and validates an uploaded image, returning its type and binary data.
    """
    from PIL import Image
    import io, base64

    content_type, content_string = image_content.split(',')
    image_data = base64.b64decode(content_string)

    # Detect file type using PIL
    try:
        image = Image.open(io.BytesIO(image_data))
        if image.format is None:
            raise ValueError("The uploaded file has an unrecognized image format.")
        image_type = image.format.lower()  # Get the image format (e.g., 'jpeg', 'png')
    except Exception as e:
        raise ValueError("The uploaded file is not a valid image.")

    return image_type, image_data

def save_comment_to_db(product_id, comment, stars):
    """
    Saves a comment to the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO comments (product_id, text, stars, timestamp)
        VALUES (?, ?, ?, GETDATE())
        """,
        (product_id, comment, stars)
    )
    conn.commit()
    cursor.close()

def fetch_comments_by_product_id(product_id):
    """
    Fetches comments for a specific product from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, text, stars, timestamp FROM comments WHERE product_id = ? ORDER BY timestamp DESC",
        (product_id,)
    )
    rows = cursor.fetchall()
    cursor.close()

    return [{"id": row[0], "text": row[1], "stars": row[2], "timestamp": row[3]} for row in rows]

def generate_comment_list(comments):
    """
    Generates a list of HTML elements for displaying comments.
    """
    from dash import html  # Import here to avoid circular imports
    return [
        html.Div(
            className="border p-3 mb-2 rounded",
            children=[
                html.Div("★" * c["stars"] + "☆" * (5 - c["stars"]), className="text-warning mb-1"),  # Star rating
                html.P(c["text"], className="mb-1"),
                html.Small(f"Data: {c['timestamp']}", className="text-muted"),
                html.Button(
                    "Șterge",
                    id={'type': 'delete-comment', 'index': c["id"]},
                    className="btn btn-danger btn-sm mt-2"
                )
            ]
        )
        for c in comments
    ]

def delete_comment_from_db(comment_id):
    """
    Deletes a comment from the database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    cursor.close()

def initialize_orders_table():
    conn = get_connection()
    cursor = conn.cursor()
    # Check if the table exists and create it if it doesn't
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'orders')
        BEGIN
            CREATE TABLE orders (
                id INT IDENTITY(1,1) PRIMARY KEY,
                product_name NVARCHAR(255) NOT NULL,
                price DECIMAL(10, 2) NOT NULL,
                order_date DATETIME NOT NULL
            )
        END
    """)
    conn.commit()
    cursor.close()
    conn.close()

initialize_orders_table()  # Ensure the table exists