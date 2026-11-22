class Product:
    def __init__(self, id,product_name,barcode="",brands="Unknown",categories="Uncategorized",ingredients="N/A",quantity=0,price=0.0,):
      self.id=id
      self.product_name = product_name
      self.barcode=barcode
      self.brands=brands
      self.categories=categories
      self.ingredients=ingredients
      self.quantity = quantity
      self.price=price

   
      

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.product_name,
            "barcode":self.barcode,
            "brands":self.brands,
            "categories":self.categories,
            "ingredients":self.ingredients,
            "quantity":self.quantity,
            "price":self.price
        }
