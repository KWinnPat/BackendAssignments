from flask import Flask, jsonify, request
import psycopg2
import os

database_name = os.environ.get('DATABASE_NAME')
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_tables(cursor, conn):
    print("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR NOT NULL UNIQUE,
        company_id INT,
        description VARCHAR,
        price FLOAT,
        active BOOLEAN DEFAULT true
        );
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Warranties (
        warranty_id SERIAL PRIMARY KEY,
        warranty_months INT NOT NULL,
        product_id INT,
        );
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Companies (
        company_id SERIAL PRIMARY KEY,
        company_name VARCHAR NOT NULL UNIQUE,
        active BOOLEAN DEFAULT true
        );
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR NOT NULL UNIQUE,
        active BOOLEAN DEFAULT true
        );
    """)
    conn.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
        product_id INT,
        category_id INT
        );
    """)
    conn.commit()

    print("Tables created")

app = Flask(__name__)

@app.route('/companies', methods=['POST'])
def create_company():
    post_data = request.form if request.form else request.get_json()

    company_name = post_data.get('company_name')

    if not company_name:
        return jsonify({"message": "company_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM Companies
            WHERE company_name=%s;
        """,
        (company_name,)
    )
    
    result = cursor.fetchone()
    
    if result:
        return jsonify({"message": 'company already exists'}), 400

    cursor.execute("""
        INSERT INTO Companies (company_name) VALUES (%s);
        """,
        (company_name,)
    )
    
    conn.commit()
    return jsonify({"message": "company created"}), 201

@app.route('/category', methods=['POST'])
def create_category():
    post_data = request.form if request.form else request.get_json()

    category_name = post_data.get('category_name')

    if not category_name:
        return jsonify({"message": "category_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM Categories
            WHERE category_name=%s;
        """,
        (category_name,)
    )
    
    result = cursor.fetchone()
    
    if result:
        return jsonify({"message": 'category already exists'}), 400

    cursor.execute("""
        INSERT INTO Categories (category_name) VALUES (%s);
        """,
        (category_name,)
    )
    
    conn.commit()
    return jsonify({"message": "category created"}), 201

@app.route('/product', methods=['POST'])
def create_product():
    post_data = request.form if request.form else request.get_json()

    product_name = post_data.get('product_name')
    company_id = post_data.get('company_id')
    description = post_data.get('description')
    price = post_data.get('price')

    if not product_name:
        return jsonify({"message": "product_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM Products
            WHERE product_name=%s;
        """,
        (product_name,)
    )
    
    result = cursor.fetchone()
    
    if result:
        return jsonify({"message": 'product already exists'}), 400

    cursor.execute("""
        INSERT INTO Products (product_name, company_id, description, price) VALUES (%s, %s, %s, %s);
        """,
        (product_name, company_id, description, price)
    )
    
    conn.commit()
    return jsonify({"message": "product created"}), 201

@app.route('/warranty', methods=['POST'])
def create_warranty():
    post_data = request.form if request.form else request.get_json()

    warranty_months = post_data.get('warranty_months')
    product_id = post_data.get('product_id')

    if not warranty_months:
        return jsonify({"message": "warranty_months is a required field"}), 400

    cursor.execute("""
        INSERT INTO Warranties (warranty_months, product_id) VALUES (%s, %s);
        """,
        (warranty_months, product_id)
    )
    
    conn.commit()
    return jsonify({"message": "warranty created"}), 201

@app.route('/product_category', methods=['POST'])
def create_product_category():
    post_data = request.form if request.form else request.get_json()

    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')

    p_result = cursor.execute("""
        SELECT * FROM Products
            WHERE product_id=%s;
        """,
        (product_id,)
    )
    
    p_result = cursor.fetchone()

    if not p_result:
        return jsonify({"message": "product_id must reference an existing record"}), 400
    
    c_result = cursor.execute("""
        SELECT * FROM Categories
            WHERE category_id=%s;
        """,
        (category_id,)
    )
    
    c_result = cursor.fetchone()

    if not c_result:
        return jsonify({"message": "category_id must reference an existing record"}), 400

    cursor.execute("""
        INSERT INTO ProductsCategoriesXref (product_id, category_id) VALUES (%s, %s);
        """,
        (product_id, category_id)
    )
    
    conn.commit()
    return jsonify({"message": "product category created"}), 201



@app.route('/companies', methods=['GET'])
def read_companies():
    result = cursor.execute("""
        SELECT * FROM Companies;
    """)
    
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'company_id': record[0],
            'company_name': record[1],
            'active': record[2]
        }
        
        record_list.append(record)

    return jsonify({"message": "companies found", "results": record_list}), 200

@app.route('/categories', methods=['GET'])
def read_categories():
    result = cursor.execute("""
        SELECT * FROM Categories;
    """)
    
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'category_id': record[0],
            'category_name': record[1]
        }
        
        record_list.append(record)

    return jsonify({"message": "categories found", "results": record_list}), 200

@app.route('/products', methods=['GET'])
def read_products():
    result = cursor.execute("""
        SELECT * FROM Products;
    """)
    
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'product_name': record[1],
            'company_id': record[2],
            'description': record[3],
            'price': record[4],
            'active': record[5]
        }
        
        record_list.append(record)

    return jsonify({"message": "products found", "results": record_list}), 200

@app.route('/warranties', methods=['GET'])
def read_warranties():
    result = cursor.execute("""
        SELECT * FROM Warranties;
    """)
    
    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'warranty_id': record[0],
            'warranty_months': record[1],
            'product_id': record[2]
        }
        
        record_list.append(record)

    return jsonify({"message": "warranties found", "results": record_list}), 200

@app.route('/products/active', methods=['GET'])
def read_active_products():
    result = cursor.execute("""
        SELECT * FROM Products
            WHERE active = true;
    """)
    
    result = cursor.fetchall()

    if not result:
        return jsonify({"message": "no active products found"}), 404
    
    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'product_name': record[1],
            'company_id': record[2],
            'description': record[3],
            'price': record[4],
            'active': record[5]
        }
        
        record_list.append(record)

    return jsonify({"message": "products found", "results": record_list}), 200

@app.route('/products/<company_id>', methods=['GET'])
def read_products_by_company_id(company_id):
    result = cursor.execute("""
        SELECT * FROM Products
            WHERE company_id = %s;
    """,
        (company_id,))
    
    result = cursor.fetchall()
    
    if not result:
        return jsonify({"message": "no products found"}), 404
    
    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'product_name': record[1],
            'company_id': record[2],
            'description': record[3],
            'price': record[4],
            'active': record[5]
        }
        
        record_list.append(record)

    return jsonify({"message": "products found", "results": record_list}), 200

@app.route('/company/<company_id>', methods=['GET'])
def read_company_by_id(company_id):
    result = cursor.execute("""
        SELECT * FROM Companies
            WHERE company_id = %s;
    """,
        (company_id,))
    
    result = cursor.fetchone()
    
    if not result:
        return jsonify({"message": "no company found"}), 404
    
    record_list = []

    for record in result:
        record = {
            'company_id': record[0],
            'company_name': record[1],
            'active': record[2]
        }
        
        record_list.append(record)

    return jsonify({"message": "company found", "results": record_list}), 200

@app.route('/category/<category_id>', methods=['GET'])
def read_category_by_id(category_id):
    result = cursor.execute("""
    SELECT * FROM Categories JOIN ProductsCategoriesXref ON category_id = category_id JOIN Products ON product_id = product_id WHERE category_id = %s;
    """, (category_id,))
    
    result = cursor.fetchall()
    
    if not result:
        return jsonify({"message": "no category found"}), 404
    
    record_list = []

    for record in result:
        record = {
            'category_id': record[0],
            'category_name': record[1],
            'active': record[2],
            'product_id': record[3],
            'product_name': record[4],
            'company_id': record[5],
            'description': record[6],
            'price': record[7],
            'active': record[8]
        }
        
        record_list.append(record)

    return jsonify({"message": "category found", "results": record_list}), 200

@app.route('/product/<product_id>', methods=['GET'])
def read_product_by_id(product_id):
    result = cursor.execute("""
        SELECT * FROM Products JOIN Warranties ON product_id = product_id JOIN ProductsCategoriesXref ON product_id = product _id JOIN Categories ON category_id = category_id WHERE product_id = %s;

    """,
        (product_id,))
    
    result = cursor.fetchall()
    
    if not result:
        return jsonify({"message": "no product found"}), 404
    
    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'product_name': record[1],
            'company_id': record[2],
            'description': record[3],
            'price': record[4],
            'active': record[5],
            'warranty_id': record[6],
            'warranty_months': record[7],
            'category_id': record[8],
            'category_name': record[9]
        }
        
        record_list.append(record)

    return jsonify({"message": "product found", "results": record_list}), 200

@app.route('/warranty/<warranty_id>', methods=['GET'])
def read_warranty_by_id(warranty_id):
    result = cursor.execute("""
        SELECT * FROM Warranties
            WHERE warranty_id = %s;

    """,
        (warranty_id,))
    
    result = cursor.fetchone()
    
    if not result:
        return jsonify({"message": "no warranty found"}), 404
    
    record_list = []

    for record in result:
        record = {
            'warranty_id': record[0],
            'warranty_months': record[1],
            'product_id': record[2]
        }
        
        record_list.append(record)

    return jsonify({"message": "warranty found", "results": record_list}), 200



@app.route('/company/<company_id>', methods=['PUT'])
def update_company(company_id):
    updated_fields = request.get_json()

    record_exists = cursor.execute("""
        SELECT * FROM Companies
            WHERE company_id = %s;
    """,
        (company_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no company found"}), 404
    
    cursor.execute("""
        UPDATE Companies SET %s WHERE company_id = %s;
        """,
        (updated_fields, company_id)
    )

    conn.commit()
    return jsonify({"message": "company updated"}), 200


@app.route('/category/<category_id>', methods=['PUT'])
def update_category(category_id):
    updated_fields = request.get_json()

    record_exists = cursor.execute("""
        SELECT * FROM Categories
            WHERE category_id = %s;
    """,
        (category_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no category found"}), 404
    
    cursor.execute("""
        UPDATE Categories SET %s WHERE category_id = %s;
        """,
        (updated_fields, category_id)
    )

    conn.commit()
    return jsonify({"message": "category updated"}), 200

@app.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    updated_fields = request.get_json()

    record_exists = cursor.execute("""
        SELECT * FROM Products
            WHERE product_id = %s;
    """,
        (product_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no product found"}), 404
    
    cursor.execute("""
        UPDATE Products SET %s WHERE product_id = %s;
        """,
        (updated_fields, product_id)
    )

    conn.commit()
    return jsonify({"message": "product updated"}), 200

@app.route('/warranty/<warranty_id>', methods=['PUT'])
def update_warranty(warranty_id):
    updated_fields = request.get_json()

    record_exists = cursor.execute("""
        SELECT * FROM Warranties
            WHERE warranty_id = %s;
    """,
        (warranty_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no warranty found"}), 404
    
    cursor.execute("""
        UPDATE Warranties SET %s WHERE warranty_id = %s;
        """,
        (updated_fields, warranty_id)
    )

    conn.commit()
    return jsonify({"message": "warranty updated"}), 200

@app.route('/product_category/<product_id>/<category_id>', methods=['PUT'])
def update_product_category(product_id, category_id):
    updated_fields = request.get_json()

    record_exists = cursor.execute("""
        SELECT * FROM ProductsCategoriesXref
            WHERE product_id = %s AND category_id = %s;
    """,
        (product_id, category_id))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no product category found"}), 404
    
    cursor.execute("""
        UPDATE ProductsCategoriesXref SET %s WHERE product_id = %s AND category_id = %s;
        """,
        (updated_fields, product_id, category_id)
    )

    conn.commit()
    return jsonify({"message": "product category updated"}), 200




@app.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    record_exists = cursor.execute("""
        SELECT * FROM Products
            WHERE product_id = %s;
    """,
        (product_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no product found"}), 404
    
    cursor.execute("""
        DELETE FROM Products WHERE product_id = %s; 
        DELETE FROM Warranties WHERE product_id = %s;
        DELETE FROM ProductsCategoriesXref WHERE product_id = %s;
        """,
        (product_id, product_id, product_id)
    )

    conn.commit()
    return jsonify({"message": "product deleted"}), 200

@app.route('/category/delete/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    record_exists = cursor.execute("""
        SELECT * FROM Categories
            WHERE category_id = %s;
    """,
        (category_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no category found"}), 404
    
    cursor.execute("""
        DELETE FROM Categories WHERE category_id = %s; 
        DELETE FROM ProductsCategoriesXref WHERE category_id = %s;
        """,
        (category_id, category_id)
    )

    conn.commit()
    return jsonify({"message": "category deleted"}), 200

@app.route('/company/delete/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    record_exists = cursor.execute("""
        SELECT * FROM Companies
            WHERE company_id = %s;
    """,
        (company_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no company found"}), 404
    
    cursor.execute("""
        DELETE FROM Companies WHERE company_id = %s; 
        DELETE FROM Products WHERE company_id = %s; 
        """,
        (company_id,)
    )

    conn.commit()
    return jsonify({"message": "company deleted"}), 200

@app.route('/warranty/delete/<warranty_id>', methods=['DELETE'])
def delete_warranty(warranty_id):
    record_exists = cursor.execute("""
        SELECT * FROM Warranties
            WHERE warranty_id = %s;
    """,
        (warranty_id,))
    
    record_exists = cursor.fetchone()

    if not record_exists:
        return jsonify({"message": "no warranty found"}), 404
    
    cursor.execute("""
        DELETE FROM Warranties WHERE warranty_id = %s; 
        """,
        (warranty_id,)
    )

    conn.commit()
    return jsonify({"message": "warranty deleted"}), 200

if __name__ == '__main__':
    create_tables()
    app.run(port='8086', host='0.0.0.0')