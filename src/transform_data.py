import pandas as pd
from pathlib import Path
import json

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'weather_data.json' # tem o mesmo sentido de '../data/weather_data.json', mas de uma forma que ao trocar de sistema ou outra pessoa executar, não quebrará o código
columns_name_to_drop = ['weather','weather_icon','sys.type']
columns_names_to_rename = {
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id",
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds",
    "sys.type": "sys_type",
    "sys.id": "sys_id",
    "sys.country": "country",
    "sys.sunrise": "sunrise",
    "sys.sunset": "sunset",
}
columns_to_normalize_datetime = ['datetime','sunrise','sunset']

def create_dataframe(path_name:str) -> pd.DataFrame:
    logging.info(f"-> Criando Dataframe do arquivo JSON...")

    path = path_name

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path) as f:
        data = json.load(f)
    # achata as colunas que vem da API, fazendo com que uma coluna de dicionario(infor: temperatura) vire uma unica coluna (info.temperatura), alem de tambem lidar com listas e preservar metadados
    df = pd.json_normalize(data)
    logging.info(f"\n✅ Dataframe criado com {len(df)} linha(s)")

    return df

def normalize_weather_columns(df:pd.DataFrame) -> pd.DataFrame:
    df_weather = pd.json_normalize(df['weather'])

    df_weather = df_weather.rename(columns={
        'id':'weather_id',
        'main':'weather_main',
        'description':'weather_description',
        'icon':'weather_icon'
    })

    df = pd.concat([df,df_weather], axis=1)

    logging.info(f"\n Coluna 'weather' normalizada - {len(df.columns)} colunas")
    return df

def drop_columns(df: pd.DataFrame, columns_names:list[str]) -> pd.DataFrame:
    logging.info(f"\n-> Removendo colunas: {columns_names}")
    df = df.drop(columns=columns_names)
    return df

def rename_columns(df:pd.DataFrame, columns_names:dict[str,str]) -> pd.DataFrame:
    logging.info(f"\n-> Renomeando colunas: {len(columns_names)} colunas")
    df = df.rename(columns=columns_names_to_rename)
    logging.info(f"\n-> Colunas renomeadas")
    return df

def normalize_datetime_columns(df:pd.DataFrame, columns_names: list[str])-> pd.DataFrame:
    logging.info(f"\n-> Convertendo colunas para datetime: {columns_names}")
    for name in columns_names:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')

    logging.info(f"\n-> Colunas convertidas")
    return df   

def date_transformation():
    print("\n Iniciando transformações")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df,columns_name_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(f"\n Transformações comcluídas")
    return df