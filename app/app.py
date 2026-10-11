import os
import time
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=5432
    )

def initialize_database():
    for attempt in range(15):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id SERIAL PRIMARY KEY,
                    product VARCHAR(100) NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price NUMERIC(10, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            connection.commit()
            cursor.close()
            connection.close()
            print("Sales database is ready")
            return

        except psycopg2.OperationalError:
            print("Waiting for PostgreSQL...")
            time.sleep(2)

    raise RuntimeError("Could not connect to PostgreSQL")

@app.route("/health", methods=["GET"])
def health():
    try:
        connection = get_connection()
        connection.close()
        return jsonify({"status": "healthy", "database": "connected"})
    except psycopg2.Error:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 503

@app.route("/sales", methods=["GET"])
def get_sales():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, product, quantity, unit_price, created_at
        FROM sales ORDER BY id
    """)

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    result = []
    for row in rows:
        item = dict(row)
        item["unit_price"] = float(item["unit_price"])
        item["created_at"] = item["created_at"].isoformat()
        result.append(item)

    return jsonify(result)

@app.route("/sales", methods=["POST"])
def add_sale():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a JSON object"}), 400

    product = data.get("product")
    quantity = data.get("quantity")
    unit_price = data.get("unit_price")

    if not isinstance(product, str) or not product.strip():
        return jsonify({"error": "Product is required"}), 400

    if type(quantity) is not int or quantity <= 0:
        return jsonify({"error": "Quantity must be a positive integer"}), 400

    try:
        price = float(unit_price)
        if price < 0 or price != price or price == float("inf"):
            raise ValueError()
        if price == float("-inf"):
            raise ValueError()
    except (TypeError, ValueError, OverflowError):
        return jsonify({"error": "Unit price must be a valid non-negative number"}), 400

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO sales (product, quantity, unit_price)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (product.strip(), quantity, price))

    sale_id = cursor.fetchone()[0]
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({
        "message": "Sale added successfully",
        "sale_id": sale_id
    }), 201

@app.route("/summary", methods=["GET"])
def summary():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(quantity), 0) AS units_sold,
            COALESCE(SUM(quantity * unit_price), 0) AS total_revenue
        FROM sales
    """)

    row = cursor.fetchone()
    cursor.close()
    connection.close()

    return jsonify({
        "total_orders": row[0],
        "units_sold": row[1],
        "total_revenue": float(row[2])
    })

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)
