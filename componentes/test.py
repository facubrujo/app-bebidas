import requests

def tragos_con_alcohol():
    try:
        url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
        #print(data['drinks'])
        return data['drinks']
    except:
        print("NO SE ECNONTRARON ")
        return []

def tragos_sin_alcohol():
    try:
        url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?a=Non_Alcoholic"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
        #print(data['drinks'])
        return data['drinks']
    except:
        print("NO SE ECNONTRARON ")
        return []

def tragos_alfabetico(letra):
    try:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letra}"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
        #print(data['drinks'])
        return data['drinks']
    except:
        print("NO SE ECNONTRARON ")
        return []

def tragos_busqueda(palabra):
    try:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={palabra}"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
        #print(data['drinks'])
        return data['drinks']
    except:
        print("NO SE ECNONTRARON ")
        return []

def tragos_id(id_trago):
    try:
        url = f"https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={id_trago}"
        data = requests.get(url)
        if data.status_code == 200:
            data = data.json()
        #print(data['drinks'])
        return data['drinks']
    except:
        print("NO SE ECNONTRARON ")
        return []
