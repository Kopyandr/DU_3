import json
import json
from pyproj import Transformer
from math import sqrt, inf
import statistics
import json.decoder
import sys
from geojson import dump
from json.decoder import JSONDecodeError

with open("adresy_try1.json", encoding="utf-8") as a:
    adresy = json.load(a)

with open("kontejnery_try.json", encoding="utf-8") as k:
    kontejnery = json.load(k)


gs2jtsk = Transformer.from_crs(4326, 5514, always_xy=True)



def parse_addresa(adresa):
    # získá potřebné informace ze souboru s adresami
    ulice_cislo = f"{adresa['properties']['addr:street']} {adresa['properties']['addr:housenumber']}"
    adresa_x, adresa_y = adresa['geometry']['coordinates']
    id_adresy = adresa['properties']['@id']
    return adresa_x, adresa_y, ulice_cislo, id_adresy




def parse_kontejner(kontejner):
    # získá potřebné informace ze souboru s kontejnery
    id_kontejneru = kontejner['properties']['ID']
    adresa_kontejneru = str(kontejner['properties']['STATIONNAME'])
    kontejner_x, kontejner_y = kontejner['geometry']['coordinates']
    pristup = kontejner['properties']['PRISTUP']
    return adresa_kontejneru, id_kontejneru, kontejner_x, kontejner_y, pristup


# uloží potřebné informace o adresách do seznamu n-tic
parsovane_adresy = [parse_addresa(x) for x in adresy['features']]
# uloží potřebné informace o kontejnerech do seznamu n-tic
parsovane_kontejnery = [parse_kontejner(x) for x in kontejnery['features']]

print (type(parsovane_adresy))
print(parsovane_adresy[1])
print (len(parsovane_adresy))

for x1,y1, ulice_adress,id_adress in parsovane_adresy:
    print (x1,y1)
    print(ulice_adress)








#def split_adresy(adresa): 


#    ulice_cislo = f"{adresa['properties']['addr:street']} {adresa['properties']['addr:housenumber']}"
#    adresa_x, adresa_y = adresa['geometry']['coordinates']
#    id_adresy = adresa['properties']['@id']
#    return adresa_x,adresa_y = adresa['geometry']['coordinates']

        