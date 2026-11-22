from flask import Flask,request,jsonify
# from flask_cors import CORS
import requests
from product import Product
from mock_db import create_initial_inventory_array,search_mock_openfoodfacts


app=Flask(__name__)
# CORS(app)


      
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



if __name__==("__main__"):
    app.run(port=5000,debug=True)