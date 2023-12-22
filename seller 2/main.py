# # main.py
# import asyncio
# from flask import Flask, jsonify, request
# from db import get_products, add_product, delete_product_by_id, update_product_quantity
# from multiprocessing import Process
# app = Flask(__name__)

# def log_response(microservice_name, response):
#     print(f"Received response from {microservice_name}: {response}")

# @app.route('/', methods=['POST', 'GET'])
# def products():
#     if request.method == 'POST':
#         if not request.is_json:
#             return jsonify({"error": "Missing JSON in request"}), 400  

#         try:
#             data = request.get_json()
#             add_product(data)
#             return 'Product Added'
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500

#     response = get_products()
#     log_response("get_products", response)
#     return response

# @app.route('/products/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     try:
#         response = delete_product_by_id(product_id)
#         log_response("delete_product_by_id", response)
#         return 'Product Deleted'
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# @app.route('/buy', methods=['POST'])
# def buy_product():
#     if not request.is_json:
#         return jsonify({"error": "Missing JSON in request"}), 400  

#     try:
#         data = request.get_json()
#         product_name = data.get('product_name')
#         quantity_to_buy = data.get('quantity')

#         if not product_name or not quantity_to_buy:
#             return jsonify({"error": "Product name and quantity are required"}), 400

#         response = update_product_quantity(product_name, -quantity_to_buy)
#         log_response("update_product_quantity", response)
#         return f'{quantity_to_buy} units of {product_name} bought successfully'
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# async def asynchronous_calls():
#     tasks = []

#     for _ in range(10):
#         tasks.append(get_products())
#         tasks.append(add_product({"product_name": "AsyncProduct", "product_description": "AsyncDescription", "quantity": 1, "seller_name": "AsyncSeller"}))
#         tasks.append(delete_product_by_id(1))

#     responses = await asyncio.gather(*tasks)
#     for i, response in enumerate(responses):
#         log_response(f"Asynchronous Call {i + 1}", response)

# if __name__ == '__main__':
#     # Synchronous call in a separate process
#     sync_process = Process(target=app.run, kwargs={'debug': True})
#     sync_process.start()

#     # Asynchronous call
#     asyncio.run(asynchronous_calls())

#     # Wait for the synchronous process to finish
#     sync_process.join()
import asyncio
from flask import Flask, jsonify, request
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Int, Schema, List, Field
from multiprocessing import Process
from db import get_products, add_product, delete_product_by_id, update_product_quantity
from db import get_product_by_id

app = Flask(__name__)

# Define a GraphQL schema
class Product(ObjectType):
    id = Int()
    product_name = String()
    product_description = String()
    quantity = Int()
    seller_name = String()

class Query(ObjectType):
    products = List(Product)
    product = Field(Product, id=Int())

    def resolve_products(self, info):
        return get_products()

    def resolve_product(self, info, id):
        product_data = get_product_by_id(id)
        
        if product_data:
            return Product(
                id=product_data['id'],
                product_name=product_data['product_name'],
                product_description=product_data['product_description'],
                quantity=product_data['quantity'],
                seller_name=product_data['seller_name']
            )
        else:
            return None

schema = Schema(query=Query)

# Add GraphQL endpoint
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

def log_response(microservice_name, response):
    print(f"Received response from {microservice_name}: {response}")

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

    response = get_products()
    log_response("get_products", response)
    return response

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        response = delete_product_by_id(product_id)
        log_response("delete_product_by_id", response)
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

        response = update_product_quantity(product_name, -quantity_to_buy)
        log_response("update_product_quantity", response)
        return f'{quantity_to_buy} units of {product_name} bought successfully'
    except Exception as e:
        return jsonify({"error": str(e)}), 500

async def asynchronous_calls():
    tasks = []

    for _ in range(10):
        tasks.append(get_products())
        tasks.append(add_product({"product_name": "AsyncProduct", "product_description": "AsyncDescription", "quantity": 1, "seller_name": "AsyncSeller"}))
        tasks.append(delete_product_by_id(1))

    responses = await asyncio.gather(*tasks)
    for i, response in enumerate(responses):
        log_response(f"Asynchronous Call {i + 1}", response)

if __name__ == '__main__':
    sync_process = Process(target=app.run, kwargs={'debug': True})
    sync_process.start()

    asyncio.run(asynchronous_calls())

    sync_process.join()
