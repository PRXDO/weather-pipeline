import requests
import json
from pathlib import Path 

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_weather_data(url:str) ->list:
    response = requests.get(url)
    data = response.json()# converte as informações vindas da url em um dicionario python

    if response.status_code != 200:
        logging.error("Erro na requisição")
        return []

    if not data:
        logging.warn("Nenhum dado retornado")
        return []

    output_path = 'data/weather_data.json'
    output_dir = Path(output_path).parent #parent serve para que ele suba um nivel nas pastas e ache a pasta data
    output_dir.mkdir(parents=True, exist_ok=True)

# função para abrir o arquivo json criado
    with open(output_path, 'w') as f:
        json.dump(data,f, indent=4) # pega as informações do dicionario e escreve no arquivo
    
    logging.info(f"Arquivo salvo em {output_path}")

    return data

