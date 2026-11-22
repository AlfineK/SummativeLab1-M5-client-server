import requests

BASE_URL="http://127.0.0.1:5555"

def ask_int(prompt,min_value=None,allow_blank=False):
    while True:
        text=input(prompt).strip()
        if allow_blank and text=="":
            return None
        try:
            num=int(text)
            if min_value is not None and num<min_value:
                print(f"Please enter a number greater than or equal to {min_value}")
                continue
            return num
        except (ValueError):
            print ("Invalid input.Please enter a whole number")

def ask_float(prompt,min_value=None,allow_blank=False):
    while True:
        text=input(prompt).strip()
        if allow_blank and text=="":
            return None
        try:
            num=float(text)
            if min_value is not None and num<min_value:
                print(f"Please enter a number greater than or equal to {min_value}")
                continue
            return num
        except (ValueError):
            print ("Invalid input.Please enter a number (like 4.44)")

def call_api(method,path,json_data=None):
    url=f"{BASE_URL}{path}"
    try:
        if method=="GET":
            res=requests.get(url,timeout=6)
        elif method=="POST":
            res=requests.post(url,json=json_data,timeout=6)
        elif method=="PATCH":
            res=requests.patch(url, json=json_data,timeout=6)
        elif method=="DELETE":
            res=requests.delete(url,timeout=6)
        else:
          print(f"Unsupported HTTP method:{method}")
          return None
    except requests.ConnectionError:
        print("Error:Cannot connect to Flask API.Make sure 'python3 app.py'is running")
        return None
    except requests.Timeout:
        print("Error:The request timed out")
        return None
    except requests.RequestException as err:
        print(f"Network error:{err}")
        return None

    try:
        data=res.json()
    except ValueError:
        data=None
    if not res.ok:
        msg=data.get("error") if isinstance(data,dict)and "error" in data else "Request Failed"
        print(f"API error({res.status_code}):{msg}")
        return None

    return data

def add_item():
    print("\n--- Add new Inventory Item---")
    name=input("Product name (optional if barcode given): ").strip()
    barcode=input("Barcode (optional if name given): ").strip()
    if not name and not barcode:
        print("You must enter a barcode or product name")
        return
    quantity=ask_int("Quantity : ",min_value=0)
    price=ask_float("Price: ",min_value=0.0)

    payload={
        "product_name": name,
        "barcode": barcode,
        "quantity": quantity,
        "price": price
    }
    created=call_api("POST","/inventory",json_data=payload)
    if created:
        print("Added item:",created)

def view_items():
    print("\n---View Inventory Items---")
    print("a.View all items")
    print("b.View single item by id")
    mode=input("Choose (a/b): ").strip().lower()

    if mode=="a":
        items=call_api("GET","/inventory")
        if items is None:
            return
        if not items:
            print("Inventory is empty")
            return
        for item in items:
            print(f"[{item['id']}] {item['product_name']} Brand:{item['brands']} Qty: {item['quantity']} Price:{item['price']:.2f}")
    elif mode=="b":
        item_id=ask_int("Enter item ID: ", min_value=1)
        item=call_api("GET",f"/inventory/{item_id}")
        if item:
            for k,v in item.items():
                print(f" {k} :{v}")
    else:
        print("Please choose 'a' or 'b'. ")

def update_price_or_stock():
    print("\n--- Update Price or Stock Level ---")
    item_id = ask_int("Enter item ID: ", min_value=1)
    current = call_api("GET", f"/inventory/{item_id}")
    if not current:
        return

    print(f"Editing [{current['id']}] {current['product_name']} (Qty: {current['quantity']}, Price: ${current['price']:.2f})")
    new_price = ask_float("New price (press Enter to keep current): ", min_value=0.0, allow_blank=True)
    new_qty = ask_int("New quantity (press Enter to keep current): ", min_value=0, allow_blank=True)

    changes = {}
    if new_price is not None:
        changes["price"] = new_price
    if new_qty is not None:
        changes["quantity"] = new_qty

    if not changes:
        print("No changes made.")
        return

    updated = call_api("PATCH", f"/inventory/{item_id}", json_data=changes)
    if updated:
        print("Updated item:", updated)


def delete_item():
    print("\n--- Delete Product ---")
    item_id = ask_int("Enter item ID to delete: ", min_value=1)
    confirm = input(f"Delete item #{item_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    result = call_api("DELETE", f"/inventory/{item_id}")
    if result:
        print(result.get("message", "Deleted."))

def find_on_api():
    print("\n--- Find Item on OpenFoodFacts ---")
    print("1. Search by barcode")
    print("2. Search by product name")
    choice = input("Choose (1/2): ").strip()

    query_string = ""
    if choice == "1":
        barcode = input("Enter barcode: ").strip()
        if not barcode:
            print("Barcode cannot be blank.")
            return
        query_string = f"?barcode={barcode}"
    elif choice == "2":
        name = input("Enter product name: ").strip()
        if not name:
            print("Product name cannot be blank.")
            return
        query_string = f"?name={name.replace(' ', '+')}"
    else:
        print("Invalid choice.")
        return

    data = call_api("GET", f"/external/lookup{query_string}")
    if data:
        prod = data.get("product", {})
        print("Found Product:")
        print(f"  Name:        {prod.get('product_name', 'N/A')}")
        print(f"  Barcode:     {prod.get('code', 'N/A')}")
        print(f"  Brand:       {prod.get('brands', 'Unknown')}")
        print(f"  Category:    {prod.get('categories', 'Uncategorized')}")
        print(f"  Ingredients: {prod.get('ingredients_text', 'N/A')}")

def main():
    while True:
        print("\n=== Inventory CLI Menu ===")
        print("1. Add new inventory item")
        print("2. View inventory details")
        print("3. Update item price or stock level")
        print("4. Delete a product")
        print("5. Find item on external API")
        print("0. Exit")

        choice = input("Select an option (0-5): ").strip()
        if choice == "1":
            add_item()
        elif choice == "2":
            view_items()
        elif choice == "3":
            update_price_or_stock()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            find_on_api()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose 0-5.")


if __name__ == "__main__":
    main()