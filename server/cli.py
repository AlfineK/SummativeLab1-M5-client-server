import requests

BASE_URL="http://127.0.0.1:5000"

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
            res=requests.get(url)
        elif method=="POST":
            res=requests.post(url,json=json_data)
        elif method=="PATCH":
            res=requests.patch(url, json=json_data)
        elif method=="DELETE":
            res=requests.delete(url)
        else:
          print(f"Unsupported HTTP method:{method}")
          return None
    except requests.ConnectionError:
        print("Error:Cannot connect to Flask API.Make sure 'python3 app.py'is running")
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