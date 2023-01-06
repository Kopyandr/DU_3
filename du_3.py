import json
import json
from pyproj import Transformer
from math import sqrt,inf
import statistics
import json.decoder
import sys
from geojson import dump
from json.decoder import JSONDecodeError
import geopy 

with open("adresy_try1.json", encoding="utf-8") as a:
    adresy = json.load(a)

with open("kontejnery_try.json", encoding="utf-8") as k:
    kontejnery = json.load(k)


wgs2jtsk = Transformer.from_crs(4326, 5514, always_xy=True)

max_vzadalenost= 1000
min_vzdalenost={}

id_adresy_id_kontejneru={}



def parse_addresa(adresa):
    ulice_cislo = f"{adresa['properties']['addr:street']} {adresa['properties']['addr:housenumber']}"
    adresa_x, adresa_y = adresa['geometry']['coordinates']
    id_adresy = adresa['properties']['@id']
    return adresa_x, adresa_y, ulice_cislo, id_adresy


def parse_kontejner(kontejner):
    
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
print(len(parsovane_kontejnery))

for adresa_x,adresa_y,ulice_cislo,id_adresy in parsovane_adresy:
    #print (adresa_x,adresa_y)
    #print(ulice_cislo)
    #převedení souřadnic z WGS do JTSK 
    krovak_x, krovak_y = wgs2jtsk.transform(adresa_x, adresa_y)
    min_vzdalenost[ulice_cislo]=float("inf")
    
    for adresa_kontejneru, id_kontejneru, kontejner_x, kontejner_y, pristup in parsovane_kontejnery:
        
        if pristup == "obyvatelům domu" and adresa_kontejneru is ulice_cislo:
           min_vzdalenost[ulice_cislo]=0
           
           id_adresy_id_kontejneru[id_adresy]=id_kontejneru
           break
           
        
        if pristup == "volně":
            
            vzdalenost=sqrt((kontejner_x-krovak_x)**2+(kontejner_y-krovak_y)**2)
    
            #vzdalenost= sqrt(abs(((krovak_x)-(kontejner_x))**2+((krovak_y)-(kontejner_y)**2)
            
            #print(krovak_x,adresa_x,krovak_y,adresa_y)
            if vzdalenost<min_vzdalenost[ulice_cislo]:
                
                min_vzdalenost[ulice_cislo]=vzdalenost
                
                id_adresy_id_kontejneru[id_adresy]=id_kontejneru 
                
    #if min_vzdalenost==max_vzadalenost:
        #print("Nejbližší popelnice je příliž daleko,nahrajte více kontejnerů")

print(min_vzdalenost)
print(type(min_vzdalenost))

with open("hotovson.json", "w", encoding="utf-8") as b:
    json.dump(min_vzdalenost, b) 

        
#print(min_vzdalenost)
#print(id_adresy_id_kontejneru)
            
            
            
        
            
            
        








#def split_adresy(adresa): 


#    ulice_cislo = f"{adresa['properties']['addr:street']} {adresa['properties']['addr:housenumber']}"
#    adresa_x, adresa_y = adresa['geometry']['coordinates']
#    id_adresy = adresa['properties']['@id']
#    return adresa_x,adresa_y = adresa['geometry']['coordinates']

        