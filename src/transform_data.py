import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json' # tem o mesmo sentido de '../data/weather_data.json', mas de uma forma que ao trocar de sistema ou outra pessoa executar, não quebrará o código


def create_dataframe(path_name:str) -> pd.DataFrame:
    logging.info(f"-> Criando Dataframe do arquivo JSON...")

    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"\n✅ Dataframe criado com {len(df)} linha(s)")

    return df

def normalize_weather_columns(df:pd.DataFrame) -> pd.DataFrame:
    