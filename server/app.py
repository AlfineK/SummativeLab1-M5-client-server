from flask import Flask,request,jsonify

app=Flask(__name__)

class Product:
    def __init__(self, id,name, quantity,packaging,brands,categories,origin):
      self.id=id
      self.name = name
      self.quantity = quantity
      self.packaging=packaging
      self.brands=brands
      self.categories=categories
      self.origin=origin

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "quantity":self.quantity,
            "packaging":self.packaging,
            "brands":self.brands,
            "categories":self.categories,
            "origin":self.origin

        }

url="https://world.openfoodfacts.org/"
      


@app.route('/')
def index():
    return "<h1>Welcome to Open Food Facts</h1>"

@app.route('/products',methods=['GET'])
def get_products():
    data=request.get_json(url)
    return jsonify(data)



if __name__==("__main__"):
    app.run(port=5000,debug=True)