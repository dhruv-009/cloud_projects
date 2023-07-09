from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
rds_host = "networks-db.cluster-ctmbbn7bpyml.us-east-1.rds.amazonaws.com"
rds_dbname = "networks"
rds_user = "admin"
rds_password = "qwerabcd"
rds_port = 3306

conn = pymysql.connect(
    host=rds_host,
    database=rds_dbname,
    user=rds_user,
    password=rds_password,
    port=rds_port
)
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS products (name VARCHAR(100), price VARCHAR(100), availability BOOLEAN)"
)


def insert_product(name, price, availability):
    try:
        cursor.execute(
            "INSERT INTO products (name, price, availability) VALUES (%s, %s, %s)",
            (name, price, availability)
        )
        conn.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


def get_all_products():
    try:
        cursor.execute("SELECT name, price, availability FROM products")
        all_products = cursor.fetchall()

        product_list = []
        for product in all_products:
            name, price, availability = product
            product_list.append({
                "name": name,
                "price": price,
                "availability": availability
            })
        return product_list
    except Exception as e:
        print(str(e))
        return []


@app.route("/store-products", methods=["POST"])
def store_products():
    try:
        data = request.get_json()

        for product in data["products"]:
            name = product["name"]
            price = product["price"]
            availability = product["availability"]

            insert_product(name, price, availability)

        return jsonify({"message": "Success."}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400


@app.route("/list-products", methods=["GET"])
def list_products():
    try:
        product_list = get_all_products()
        return jsonify({"products": product_list}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
    conn.close()