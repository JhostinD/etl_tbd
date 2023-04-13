from cfg import CLIENT_ID, CLIENT_SECRET, SCOPE, SPOTIPY_REDIRECT_URI
import psycopg2
import pandas as pd
import datetime
import spotipy
import requests
import io
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# Función extraer
def extract(date, limit=50):
    yesterday_unix_timestamp = int(date.timestamp()) * 1000
    return sp.current_user_recently_played(limit=limit, after=yesterday_unix_timestamp)

# Función transformar
def transform(data_raw):

    data_clean = {
        "album_name": [],
        "song_name": [],
        "album_image": [],
        "played_at": []
    }

    for song in data_raw["items"]:

        # Obtener a partir de la url la imagen
        url = song["track"]["album"]["images"][0]["url"]
        response = requests.get(url)

        # Crear un objeto de bytes en memoria
        img_bytes = io.BytesIO(response.content)

        # Rellenamos las listas de los campos que nos interesan
        data_clean["album_name"].append(song["track"]["album"]["name"])
        data_clean["song_name"].append(song["track"]["name"])
        data_clean["album_image"].append(img_bytes.getvalue())
        data_clean["played_at"].append(song["played_at"])
    
    # Creamos el DataFrame con el diccionario limpio
    clean_df = pd.DataFrame(data_clean, columns=["album_name", "song_name", "album_image", "played_at"])

    print(clean_df)
    return clean_df

# Función cargar
def load(conn, df):
    # SQL de inserción de datos
    sql_insert = """
                 INSERT INTO public.recent_played_tracks(
                 album_name, song_name, album_image, played_at)
                 VALUES (%s, %s, %s, %s);
                 """
    
    # De la conexión sacamos un cursor para ejecutar sentencias SQL
    with conn.cursor() as cursor:
        # Iterar por las diferentes filas del dataframe e insertándolas
        for index, row in df.iterrows():
            cursor.execute(sql_insert, (row["album_name"], row["song_name"], row["album_image"], row["played_at"]))

    # Guardamos los cambios en la BD
    conn.commit()
    

if __name__ == "__main__":

    # Convertir el tiempo a timestamp de Unix en milisegundos
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=7)
    
    # Paso EXTRACT: extracción de datos en crudo de la API de Spotify
    data_raw = extract(yesterday)

    # PASO TRANSFORM: transformación y limpieza de datos
    clean_df = transform(data_raw)

    # Aquí hay que poner el nombre de la bd, el user y la password de tu bd
    # Conexión a BD
    
    conn = psycopg2.connect(dbname="tbd_etl", user="postgres", password="1234")

    # Paso LOAD: carga de datos en BD
    load(conn, clean_df)

    # Cierre de la conexión a la BD
    
    conn.close()
