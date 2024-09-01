from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# In-memory storage for demonstration
products = []
categories = []
currencies = {"USD": 1.0, "SGD": 1.35}  # Example exchange rates (1 USD = 1.35 SGD)
default_currency = "USD"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_category', methods=['POST'])
def add_category():
    data = request.json
    if not data.get('name'):
        return jsonify({"error": "Category name is required"}), 400

    category_name = data['name']

    # Check if category already exists
    if any(category['name'] == category_name for category in categories):
        return jsonify({"error": "Category already exists"}), 400

    categories.append({'name': category_name})
    return jsonify({"message": "Category added", "category": category_name}), 201

@app.route('/edit_category/<old_name>', methods=['PUT'])
def edit_category(old_name):
    data = request.json
    new_name = data.get('name')

    if not new_name:
        return jsonify({"error": "New category name is required"}), 400

    # Find the category to edit
    for category in categories:
        if category['name'] == old_name:
            category['name'] = new_name
            return jsonify({"message": "Category updated", "category": new_name}), 200

    return jsonify({"error": "Category not found"}), 404

@app.route('/delete_category/<name>', methods=['DELETE'])
def delete_category(name):
    global categories, products

    categories = [category for category in categories if category['name'] != name]
    products = [product for product in products if product['category'] != name]

    return jsonify({"message": "Category deleted"}), 200

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    price = data.get('price')
    category = data.get('category')
    currency = data.get('currency', default_currency)  # Default to USD if not provided

    if not name or not price or not category:
        return jsonify({"error": "Name, price, and category are required"}), 400

    # Check if category exists
    if not any(cat['name'] == category for cat in categories):
        return jsonify({"error": "Category does not exist"}), 400

    products.append({
        'name': name,
        'price': float(price),
        'currency': currency,
        'category': category
    })
    return jsonify({"message": "Product added", "product": name}), 201

@app.route('/edit_product/<old_name>', methods=['PUT'])
def edit_product(old_name):
    data = request.json
    new_name = data.get('name')
    new_price = data.get('price')
    new_category = data.get('category')
    new_currency = data.get('currency', default_currency)  # Default to USD if not provided

    if not new_name or not new_price or not new_category:
        return jsonify({"error": "Name, price, category, and currency are required"}), 400

    # Find the product to edit
    for product in products:
        if product['name'] == old_name:
            product['name'] = new_name
            product['price'] = float(new_price)
            product['currency'] = new_currency
            product['category'] = new_category
            return jsonify({"message": "Product updated", "product": new_name}), 200

    return jsonify({"error": "Product not found"}), 404

@app.route('/delete_product/<name>', methods=['DELETE'])
def delete_product(name):
    global products

    products = [product for product in products if product['name'] != name]

    return jsonify({"message": "Product deleted"}), 200

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products), 200

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories), 200

if __name__ == '__main__':
    app.run(debug=True)
