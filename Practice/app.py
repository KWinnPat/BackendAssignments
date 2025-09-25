from flask import Flask, jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_tables():
    print("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR NOT NULL UNIQUE,
        description VARCHAR,
        price FLOAT,
        active BOOLEAN DEFAULT true
        );
    """)
    
    conn.commit()
    print("Tables created")

app = Flask(__name__)

@app.route('/products', methods=['POST'])
def add_product():
    post_data = request.form if request.form else request.get_json()

    product_name = post_data.get('product_name')
    description = post_data.get('description')
    price = post_data.get('price')

    if not product_name:
        return jsonify({"message": "product_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM products
            WHERE product_name=%s
        """,
        (product_name,)
    )
    
    result = cursor.fetchone()
    
    if result:
        return jsonify({"message": 'Product already exists'}), 400

    cursor.execute("""
        INSERT INTO products
            (product_name, description, price)
            VALUES(%s, %s, %s)
        """,
        (product_name, description, price)
    )
    
    conn.commit()
    return jsonify({"message": f"Product {product_name} added to DB"}), 201


@app.route('/products', methods=["GET"])
def get_product():
    result = cursor.execute("""
        SELECT * FROM Products;
    """)
    
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'product_name': record[1],
            'description': record[2],
            'price': record[3],
            'active': record[4]
        }
        
        record_list.append(record)

    return jsonify({"message": "products found", "results": record_list}), 200

if __name__ == '__main__':
    create_tables()
    app.run(host=app_host, port=app_port)