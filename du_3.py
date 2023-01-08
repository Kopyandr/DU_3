import json
from pyproj import Transformer
from math import sqrt, inf
import sys
from statistics import mean, median
import json.decoder
from json.decoder import JSONDecodeError


try:
    with open('adresy.geojson', 'r',encoding="UTF-8") as f: # Otevře json 
        adresy = json.load(f)

    with open('kontejnery.geojson','r',encoding='utf-8') as f: 
        kontejnery=json.load(f)
        
except FileNotFoundError:
    sys.exit("chybná vstupní data nebo špatný adresář")
except PermissionError:
    sys.exit("program nemá právo číst vstupní soubor")
except JSONDecodeError:
    sys.exit("vstupní soubor není validní")
except IOError:
    sys.exit("vstupní soubor nelze přečíst")
except:
    sys.exit("někde se stala chyba")
    
wgs2jtsk = Transformer.from_crs(4326, 5514, always_xy=True) # transformace WGS souřadnice na S-JTSK souřadnice


min_vzdalenost=None # Vzdálenost k nejbližšímu kontejneru 
list_k_ulozeni=[] #list, který poslouží k převedení do geojsonu 

nejblizsi_kontejner=None #sem se bude ukládat id nejbližšího kontejner 
max_vzdalenost=0
adresa_nejdale=None 

LIMIT=10000 #maximalní vzdalenost nejméně vzdaleneho koše 
    
  
for adresa in adresy["features"]: #prochází adresy a získavá potřebné informace (souřadnice atd.)
    krovak_x = adresa["geometry"]["coordinates"][0]                       
    krovak_y = adresa["geometry"]["coordinates"][1]
    krovak = wgs2jtsk.transform(krovak_x,krovak_y)  #převádí souřadnice z WGS84 do SJTSK 
    street_a_num = f"{adresa['properties']['addr:street']} {adresa['properties']['addr:housenumber']}"
    adress_id = adresa['properties']['@id']
   
    
    for container in kontejnery['features']: # obdobně prochází kontejnery, kde získává souřadnice a typ přístupu 
        kontak_x=container['geometry']["coordinates"][0]
        kontak_y=container['geometry']["coordinates"][1]
        adresa_kontejneru = str(container['properties']['STATIONNAME'])
        pristup=container['properties']['PRISTUP']
        id_kontejneru=container['properties']['ID']
        #print(id_kontejneru)
        
        # kontejnery v se stejnou adresou přístupné pouze obyvatelům domu maj vzdálenost 0 
        if pristup=="obyvatelům domu" and adresa_kontejneru == street_a_num: 
            min_vzdalenost = 0
            nejblizsi_kontejner=id_kontejneru
            break
        
        if pristup=="volně": # Volně přístupné kontejnery 
            vzdalenost = float(sqrt((krovak[0]-kontak_x)**2+(krovak[1]-kontak_y)**2)) # spočíta se vzdálenost pomocí pythagorovy věty 
    
            if min_vzdalenost is None or min_vzdalenost > vzdalenost:  #Pokud je vzdalenost iterovaného kontejneru menší než byli vzdalenosti doposud, zapíše se 
                min_vzdalenost=vzdalenost
                nejblizsi_kontejner=id_kontejneru
                
    if min_vzdalenost > LIMIT: # pokud je vzdalenost více než 10 km, program se ukončí 
        raise Exception("Kontejner je podezřele daleko, nahrajte více bodů")
    
                
    if min_vzdalenost > max_vzdalenost: #zaznamená nejdelší vzdálenost k nejbližšímu kontejneru 
        max_vzdalenost=min_vzdalenost
        adresa_nejdale=street_a_num
        nejvzdalenejsi_kontejner=id_kontejneru
    
       
    adresa["properties"]["k_popelnici"] = round(min_vzdalenost)  #Do slovníku se připíše nový klíč s nejmenší vzdáleností kontaineru               
    adresa["properties"]["kontejner"] = nejblizsi_kontejner    # nový klíč s ID kontejneru  
    list_k_ulozeni.append(adresa)        #Přidá danou adresu do seznamu 
            
    min_vzdalenost=None #Vynuluje se minimalní vzdálenost v iteraci pro práci s další adresou 
    

#novy soubor s pridanymi idcky a vzdalenostmi k dannému kontejneru               
with open("adresy_kontejnery.geojson","w", encoding="utf-8") as out:                   
    json.dump(list_k_ulozeni, out, ensure_ascii = False, indent = 2)
    
vzdalenosti = [adresa["properties"]["k_popelnici"] for adresa in adresy["features"]]  # Sem se vypisují vypočítane nejmenší vzdalenosti 


print(f"Prumerna vzdalenost ke kontejnerům je : {round(mean(vzdalenosti))} m")    
print(f"Median vzdaleností ke kontejnerům je: {round(median(vzdalenosti))} m")
print(f"Nejdále ke kontejneru je z adresy {adresa_nejdale} a to {round(max_vzdalenost)} m.")
        