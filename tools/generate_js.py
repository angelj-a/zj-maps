import json
import random
from pprint import pprint

from extract_geojson import *
from zonajobs_stats import *
from decode import *


params = {
    'comunas': {
        'filename': 'comunas.csv',
        'delimiter': ';',
        'name': 'comuna',
        'geojson': 'geojson'
        },
    'barrios': {
        'filename': 'barrios.csv',
        'delimiter': ',',
        'name': 'BARRIO',
        'geojson': 'GEOJSON'
        }
    }
    
area_sector_programacion = "sistemas-tecnologia-it-programacion"
  

def main():

    # Get stats
    publications = publications_by_sector(area_sector_programacion)
    
    
    rows_as_dict = csvfile_to_dict_list('barrios.csv',
                                        params['barrios']['delimiter'])
    
    geojson_list = {
        "type" : "FeatureCollection",
        "features" : []
        }
           
    for elem in rows_as_dict:
        barrio_code = elem[params['barrios']['name']].decode('utf8')
        barrio_name = codename_to_name[barrio_code]
        
        feature = {
            "type": "Feature",
            "properties": {
                "name": elem[params['barrios']['name']],
                "publications": publications[barrio_name]
                },
            "geometry": json.loads(elem[params['barrios']['geojson']])
            }
        
        geojson_list['features'].append(feature)
            
    with open("barrios.js",'w') as f:
        f.write("var barriosData = ")
        f.write(json.dumps(geojson_list))


if __name__ == '__main__':
    main()
