import requests
from requests.auth import HTTPBasicAuth

print("----------------------------------------------")
print("ESHOP queue processing ....")
print("----------------------------------------------")

username = "extapp"
password = "Heslo567"
api_url = "http://192.168.224.33:8080/emco/eshop/import"

try:
    response = requests.post(api_url, auth=HTTPBasicAuth(username, password))
    if response.status_code == 200:
        print("Q-Proces ... úspěšně zavoláno, kód 200.")
    else:
        print(f"Chyba při volání API. Status kód: {response.status_code}")
        
except Exception as e:
    print(f"Chyba: {e}")

print("----------------------------------------------")
ok_cont = input("Pokračuj po stisku ...")
