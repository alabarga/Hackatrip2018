import requests
import urllib
import json
import time
import pandas as pd

def get_token_bbva():
    key = 'YXBwLmJidmEuaWJlcmlhcnVsZXM6Tmt3V1FEJUZvSGtqWkdHem95eVZVc0l2SDBRWEg2ZDdkRW15byplUHVJM08wWWJtZUprcjlvd1I2YUclJEgxWQ=='
    headers = {}
    headers["Accept"] = "application/json"
    headers["Authorization"] = 'Basic ' + key
    r = requests.post('https://connect.bbva.com/token?grant_type=client_credentials', headers=headers)
    dic = json.loads(r.text)
    token = dic['access_token']
    return token

token = get_token_bbva()

def get_basicstats(token, params, periodo):
    headers = {
        "Accept"        : "application/json",
        "Content-type"  : "application/json",
        "Authorization" : 'jwt ' + token 
    }
    url = 'https://apis.bbva.com/paystats_sbx/4/zipcodes/%s/basic_stats?' % params['zipcode']
    del params['zipcode']
    
    if periodo != "año":
        params["min_date"], params["max_date"] = periodo, periodo
        parqparams = urllib.parse.urlencode(params)
        r = requests.get(url + parqparams, headers = headers)
        return r.text                                       ### Raise Error si el code no es 200
    
    if periodo == "año":
        params["min_date"], params["max_date"] = "201501", "201512"
        parqparams = urllib.parse.urlencode(params)
        r = requests.get(url + parqparams, headers = headers)
        return r.text                                       ### Raise Error si el code no es 200

### Crear Fichero de Merchants ###

def get_merchants():
    headers = {}
    headers["Accept"] = "application/json"
    headers["Accept-Language"] = "es"
    headers["Authorization"] = 'jwt ' + get_token_bbva() # TODO - Si esto tarda, no hacerlo siempre
    
    g_paystats = requests.get('https://apis.bbva.com/paystats_sbx/4/info/merchants_categories', 
                headers = headers)
    return json.loads(g_paystats.text) ### Raise Error si el code no es 200

categorias = get_merchants()["data"][0]["categories"]

with open("merchant_categories.csv", "w") as fichero:
    fichero.write("categoria,subcategoria\n")
    for c in categorias:
        for sc in c["subcategories"]:
            fichero.write(c["code"])
            fichero.write(",")
            fichero.write(sc["code"])
            fichero.write("\n")
fichero.close()

### Lanzar Extractor de la API ###

df_cat = pd.read_csv("merchant_categories.csv")
categorias = list(df_cat['categoria'].unique())

df_zip = pd.read_csv("zipcodes.csv")
zipcodes = [str(z)[:-2] for z in list(df_zip['zipcode'].unique())]

cards = ["all", "bbva", "national", "foreign"]
channel = ["pos", "bbva_pos"]

token = get_token_bbva()
for categoria in categorias:
    t_ini = time.time()
    lista_dics = {}
    for zipcode in zipcodes:
        subcategoria = "all"
        params = {'channel':'pos', 'cards':'all', 'category':categoria, 'zipcode':zipcode}
        clave = ",".join([zipcode, categoria, subcategoria, params['channel'], params['cards']])
        json_string = get_basicstats(token, params, "año")
        dic = json.loads(json_string)
        
        if dic['result']['code'] == 200 and dic['result']['info'] == "OK":
            lista_dics[clave] = dic['data']

        # OJO, hay valores (zipcode, mes) para los cuales (supongo que porque no hay datos) el diccionario
        # que te devuelve solo tiene el par ("date", "YYYYMM")
            
    with open("xxx_" + categoria + ".json", "w") as fichero:
        fichero.write(json.dumps(lista_dics))
        fichero.close()
    
    duracion = time.time() - t_ini
    print("Ha tardado %.2f segundos en descargar la categoria %s" % (duracion, categoria))