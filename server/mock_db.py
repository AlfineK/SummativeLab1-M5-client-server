from product import Product

MOCK_OPENFOODFACTS_DB = [
    {
        "id": 1,
        "quantity": 20,
        "price": 3.99,
        "status": 1,
        "product": {
            "code": "0025293600270",
            "product_name": "Organic Almond Milk",
            "brands": "Silk",
            "categories": "Plant-based milks, Almond milks",
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, locust bean gum."
        }
    },
    {
        "id": 2,
        "quantity": 15,
        "price": 5.49,
        "status": 1,
        "product": {
            "code": "3017620422003",
            "product_name": "Nutella Hazelnut Spread",
            "brands": "Ferrero",
            "categories": "Breakfasts, Spreads, Chocolate spreads",
            "ingredients_text": "Sugar, palm oil, hazelnuts, skimmed milk powder, cocoa, lecithins, vanillin."
        }
    },
    {
        "id": 3,
        "quantity": 35,
        "price": 2.89,
        "status": 1,
        "product": {
            "code": "7394376616228",
            "product_name": "Oat Drink Barista Edition",
            "brands": "Oatly",
            "categories": "Dairy substitutes, Oat milks",
            "ingredients_text": "Water, oats, rapeseed oil, acidity regulator, calcium carbonate, salt."
        }
    }
]

def search_mock_openfoodfacts(barcode="",name=""):
    clean_barcode=(barcode or "").strip()
    clean_name=(name or "").strip().lower()

    for record in MOCK_OPENFOODFACTS_DB:
        prod=record.get("product",{})
        rec_code=str(prod.get("code","")).strip()
        rec_name=str(prod.get("product_name","")).lower()

        if clean_barcode and rec_code ==clean_barcode:
            return record
        if clean_name and clean_name in rec_name:
            return record

    return None

def create_initial_inventory_array():
    inventory_array=[]
    for record in MOCK_OPENFOODFACTS_DB:
        prod=record["product"]
        item=Product(
            id=record["id"],
            product_name=prod["product_name"],
            barcode=prod["code"],
            categories=prod["categories"],
            ingredients=prod["ingredinets"],
            quantity=record["quantity"],
            price=record["price"]
        )
        inventory_array.append(item)
    return inventory_array