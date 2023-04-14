# TBD_ETL

## Creación de la app en Spotify for Developers
URL para documentación de Spotify API: https://developer.spotify.com/documentation/web-api/reference/get-recently-played

1. Es necesario crearse una cuenta en spotify (es gratuito).
2. Acceder al siguiente enlace e iniciar sesión: https://developer.spotify.com/dashboard.
3. Pulsar el botón "Create app" y colocar un nombre y descripción. En "Redirect URI" colocamos una página web cualquiera (importante poner la misma en el campo "SPOTIPY_REDIRECT_URI" settings.ini, se explicará más adelante) y pulsamos en "save".
4. Una vez creada la app nos dirigimos a settings dentro de la app y en la pestaña "basic information" nos guardamos "CLIENT_ID" y "CLIENT_SECRET", las cuales guardaremos en "settings.ini".

## Settings.ini
1. Crear en la raíz del proyecto el fichero "settings.ini", el cual contendrá las variables de entorno del programa.
2. Guardar las variables necesarias (en nuestro caso: CLIENT_ID, CLIENT_SECRET, SCOPE, SPOTIFY_REDIRECT_URI).
3. **IMPORTANTE:** por temas de seguridad, NO subir este fichero al repositorio.

El formato del fichero settings.ini es:
[settings]
CLIENT_ID=id_de_tu_app
CLIENT_SECRET=secret_de_tu_app
SCOPE=user-read-recently-played
SPOTIPY_REDIRECT_URI=https://www.google.es/

## Crear el entorno virtual (venv) de python en VS Code:
1. En el menú de opciones, accedemos a "View/Command Palette".
2. En el buscador, seleccionamos la opción "Python: Create Enviroment" y elegimos nuestro intérprete de python (es necesario tener una versión de python instalada).
3. Permitimos la ejecución de scripts para "Activate.ps1" mediante el siguiente comando en la terminal de PS: <br>
 **Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser**
4. ejecutamos "Activate.ps1" mediante el comando: <br>
**& "RESTO_DEL_PATH_COMPLETO_DEL_PROYECTO/TBD_ETL/.venv/Scripts/Activate.ps1"**

## Gestión de dependencias instaladas (Requirements.txt):
- Para ver dependencias usamos el comando: <br>
**py -m pip freeze**
- Para instalar una nueva dependencia usamos: <br>
**py -m pip install paquete==version**, donde paquete es el nombre de la librería y version es la que deseamos (1.0.7, por ejemplo). Indicar la versión es opcional.
- Para actualizar el archivo requirements.txt es necesario usar el siguiente comando: <br>
**py -m pip freeze > requirements.txt**
- Para instalar todas las dependencias de requirements.txt usamos el siguiente comando: <br>
**py -m pip install -r requirements.txt**

## PostgreSQL
Se necesita tener configurada la base de datos postgreSQL 15 con pgAdmin 4, instalarlo e inicializar desde pgAdmin 4.
Para este ejemplo se ha creado una base de datos llamada "tbd_etl", con username "postgres".

Se ha creado una tabla dentro del schema "public" la tabla "recent_played_tracks", con 5 columnas:
1. id_song: id autonumérico (generado automáticamente) que actúa como PK.
2. album_name: nombre del álbum.
3. song_name: nombre de la canción.
4. album_image: columna de array de bytes que guarda la imagen de formato BLOB.
5. played_at: fecha en la que se ha reproducido la canción.


## Al ejecutar
Hay que tener en cuenta que al ejecutar el programa la primera vez este nos redirigirá a la uri que especificamos tanto en la app como en settings.ini. Cuando ocurra esto, es necesario copiar la url completa de la página a la que se nos ha redirigido y pulsar enter. Una vez hecho esto, se generará un fichero ".cache" que contiene el token de acceso a la app.
