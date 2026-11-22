from flask import Flask,request,jsonify
from flask_cors import CORS
import requests
from product import Product
from mock_db import create_initial_inventory_array,search_mock_openfoodfacts


app=Flask(__name__)
CORS(app)


      
inventory=create_initial_inventory_array()
next_id=max((item.id for item in inventory),default=0)+1

def find_product_by_id(id):
    for product in inventory:
        if product.id==id:
            return product
    return None

def fetch_openfoodfacts(barcode="",name=""):
    barcode=(barcode or "").strip()
    name=(name or "").strip()

    try:
        if barcode:
            url=f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
            res=requests.get(url)
            if res.status_code==200:
                data=res.json()
                if data.get("status")==1 and data.get("product"):
                    return {"status":1, "product":data["product"]}

        elif name:
            clean_url_name=name.replace(" ", "+")
            url=(
                f"https://world.openfoodfacts.org/cgi/search.pl"
                f"?search_terms={clean_url_name}&search_simple=1&action=process&json=1&page_size=1"
            )
            res=requests.get(url)
            if res.status_code==200:
                products=res.json().get("products",[])
                if products:
                    return {"status":1, "product":products[0]}
    except requests.RequestException:
        pass
    return search_mock_openfoodfacts(barcode=barcode,name=name)

@app.route("/")
def index():
    return "<h1>Open Food Facts</h1>"

@app.route("/inventory",methods=['GET'])
def get_all_inventory():
    return jsonify ([item.to_dict() for item in inventory]),200


@app.route("/inventory/<int:id>", methods=['GET'])
def get_one_inventory(id):
    product=find_product_by_id(id)
    if product is None:
        return jsonify({"Error":f"Item with ID {id} not found"}),404
    return jsonify(product.to_dict()),200

@app.route("/inventory",methods=['POST'])
def add_inventory_item():
    global next_id
    data=request.get_json()
    if not data:
        return jsonify({"error":"Request body must be valid json"}),400

    product_name=str(data.get("product_name","")).strip()
    barcode=str(data.get("barcode","")).strip()

    if not product_name or not barcode:
        return jsonify({"error":"Please provide atleast barcode or product_name"}),400

    try:
        quantity=int(data.get("quantity",0))
        price=float(data.get("price",0.0))
    except (ValueError,TypeError):
        return jsonify({"error":"'quantity 'must be an interger and 'price' must be a number"}),400
    if quantity<0 or price<0:
        return jsonify({"error":"'quantity' and 'price' cannot be negative"})
    new_product=Product(
        id=next_id,
        product_name=product_name,
        barcode=barcode,
        brands=str(data.get("brands","")).strip() or "Unknown",
        categories=str(data.get("categories","")).strip() or "Uncategorized",
        ingredients_text=str(data.get("ingredients_text","")).strip() or "N/A",
        quantity=quantity,
        price=price
    )

    inventory.append(new_product)
    next_id +=1
    return jsonify(new_product.to_dict()),201


@app.route('/inventory/<int:id>',methods=['PATCH'])
def update_inventory_item(id):
    product=find_product_by_id(id)
    if product ==None:
        return jsonify({"error":f"Item with ID {id} not found"}),404
    data=request.get_json()
    if not data:
        return jsonify({"error":"Provide JSON fields to update"}),400
    if "quantity" in data:
        try:
            new_qty=int(data["quantity"])
        except (ValueError,TypeError):
            return jsonify({"error":"Quantity must be an interger"}),400
        if new_qty<0:
            return jsonify({"error":"Quantity cannot be negative"}),400
        product.quantity=new_qty

    if "price" in data:
        try:
            new_price=float(data["price"])
        except (ValueError,TypeError):
            return jsonify({"error":"price must be a number"}),400
        if new_price <0:
            return jsonify({"error":"Price cannot be negative"}),400
        product.price=new_price

    if "product_name" in data and str(data["product_name"]).strip():
        product.product_name=str(data["product_name"]).strip()
    if "barcode" in data :
        product.barcode=str(data["barcode"]).strip()
    if "brands" in data and str(data["brands"]).strip():
        product.brands=str(data["brands"]).strip()
    if "categories" in data and str(data["categories"]).strip():
        product.categories=str(data["categories"]).strip()

    return jsonify(product.to_dict()),200

@app.route('/inventory/<int:id>',methods=['DELETE'])
def delete_inventory_item(id):
    product=find_product_by_id(id)
    if product ==None:
        return jsonify({"error":f"Item with ID {id} not found"}),404
    inventory.remove(product)
    return jsonify({"message":f"Deleted item #{id}"}),200


@app.route('/external/lookup', methods=['GET'])
def external_lookup():
    barcode=request.args.get("barcode","").strip()
    name=request.args.get("name","").strip()

    if not barcode or not name:
        return jsonify({"error": "Pass 'barcode' or 'name' as a query parameter"}),400
    off_data=fetch_openfoodfacts(barcode=barcode,name=name)
    if not off_data or off_data.get("status") !=1:
        return jsonify({"error":"Product not found in OpenFoodFacts or mock database"}),404
    return jsonify(off_data),200




if __name__==("__main__"):
    app.run(port=5555,debug=True)