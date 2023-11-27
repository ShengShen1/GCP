
# main.py
from flask import Flask, jsonify, request
from db import get_products, add_product, delete_product_by_id, update_product_quantity

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def products():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400  

        try:
            data = request.get_json()
            add_product(data)
            return 'Product Added'
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return get_products()    

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        delete_product_by_id(product_id)
        return 'Product Deleted'
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/buy', methods=['POST'])
def buy_product():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400  

    try:
        data = request.get_json()
        product_name = data.get('product_name')
        quantity_to_buy = data.get('quantity')

        if not product_name or not quantity_to_buy:
            return jsonify({"error": "Product name and quantity are required"}), 400

        update_product_quantity(product_name, -quantity_to_buy)
        return f'{quantity_to_buy} units of {product_name} bought successfully'
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

