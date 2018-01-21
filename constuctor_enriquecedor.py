import requests
import urllib
import json
import time
import pandas as pd

### Construir Data Mart ###

with open("categoria_all.json", "r") as fksdmla:
    for linea in fksdmla:
        dic = json.loads(linea)

with open("car.csv", "w") as fichero:
    fichero.write("zipcode,mes,int_txs,int_customers,int_merchants,num_avg,num_max,num_gross,num_avg_per_customer\n")
    for key, lista_meses in dic.items():
        zipcode = key.split(",")[0]
        for dm in lista_meses:
            if len(dm.keys()) == 12:
                mes = dm["date"]
                int_txs = dm["txs"]
                int_customers = dm["cards"]
                int_merchants = dm["merchants"]
                #
                num_avg = round(dm["avg"], 2)
                num_max = dm["max"]
                #
                num_gross = round(int_txs * num_avg, 2)
                num_avg_per_customer = round(num_gross / int_customers, 2)
                #
                registro = [zipcode, mes, int_txs, int_customers, int_merchants, num_avg, num_max,
                         num_gross, num_avg_per_customer]
            else:
                registro = [zipcode, mes, "", "", "", "", "", "", ""]
            linea = [str(x) for x in registro]
            fichero.write(",".join(linea))
            fichero.write("\n")
    fichero.close()

### Enriquecer Data Mart ###

dic_out = {}
lista = ["es_hotelservices", "es_travel", "es_barsandrestaurants", "es_transportation"]
    
for cat in lista:
    with open("xxx_%s.json" % cat, "r") as fksdmla:
        for linea in fksdmla:
            dic = json.loads(linea)
    
    for key, lista_meses in dic.items():
        zipcode = key.split(",")[0]
        for dm in lista_meses:
            if dm["date"] == "201507":
                print(1)
                if len(dm.keys()) == 12:
                    int_txs = dm["txs"]
                    num_avg = round(dm["avg"], 2)
                    num_gross = str(round(int_txs * num_avg, 2))
                else:
                    num_gross = ""
                
                if not zipcode in list(dic_out.keys()):
                    dic_out[zipcode] = {}
                    dic_out[zipcode][cat] = num_gross
                else:
                    dic_out[zipcode][cat] = num_gross

with open("car_enriquecido.csv", "w") as fichero:
    fichero.write("zipcode,num_gross_es_hotelservices,num_gross_es_travel,num_gross_es_barsandrestaurants,num_gross_es_transportation\n")
    for key, d in dic_out.items():
        for k in ["es_hotelservices", "es_travel", "es_barsandrestaurants", "es_transportation"]:
            if k not in list(d.keys()):
                d[k] = ""
        lista = [key, d["es_hotelservices"], d["es_travel"], d["es_barsandrestaurants"], d["es_transportation"]]
        fichero.write(",".join(lista))
        fichero.write("\n")