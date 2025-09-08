import requests
from requests.auth import HTTPBasicAuth


print("----------------------------------------------")
print("ESHOP queue processing ....")
print("----------------------------------------------")

username = "emco"
password = "!Em50_%Str0nGPsw"
#api_url = "https://api.esa-logistics.eu/v2/item-master?item_number=1380130"

def get_api_url(item_number):
    base_url = "https://api.esa-logistics.eu/v2/item-master"
    return f"{base_url}?item_number={item_number}"

#item_number = "1470300"
item_number = input("Zadejte item_number: ")
api_url = get_api_url(item_number)


try:
    response = requests.get(api_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        print("Q-Proces ... úspěšně zavoláno, kód 200.")
        print("-" * 20)

        data = response.json()
        
        for item in data:
            warehouse = item.get("warehouse", "N/A")
            company = item.get("company", "N/A")
            item_number = item.get("item_number", "N/A")
            item_name = item.get("item_name", "N/A")
            ean_main = item.get("ean_main", "N/A")
            quality_code = item.get("quality_code", "N/A")
            unit_of_measure = item.get("unit_of_measure", "N/A")

            print(f"Warehouse: {warehouse}")
            print(f"Company: {company}")
            print(f"Item Number: {item_number}")
            print(f"Item Name: {item_name}")
            print(f"EAN main: {ean_main}")
            print(f"Vychozi status: {quality_code}")
            print(f"ZMJ: {unit_of_measure}")
            print("-" * 20)        
    else:
        print(f"Chyba při volání API. Status kód: {response.status_code}")
        
except Exception as e:
    print(f"Chyba: {e}")

ok_cont = input("Pokračuj po stisku ...")

