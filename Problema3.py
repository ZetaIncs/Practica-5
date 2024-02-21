# Importar pandas y requests
import pandas as pd
import requests

# Leer el archivo reactiva.csv
df = pd.read_csv("reactiva1.csv", sep=";")

# Crear una función de limpieza
def limpiar(df):
    # Renombrar las columnas eliminando espacios, tildes y convirtiendo a minúscula
    df.columns = df.columns.str.replace(" ", "_").str.replace("á", "a").str.replace("é", "e").str.replace("í", "i").str.replace("ó", "o").str.replace("ú", "u").str.lower()
    # Eliminar la columna id y tipo_moneda que se encuentre repetida
    df = df.drop(columns=["id", "tipo_moneda"], axis=1, errors="ignore")
    # Eliminar el carácter coma ',' del texto de la columna "dispositivo_legal"
    try:
        df["dispositivo_legal"] = df["dispositivo_legal"].str.replace(",", "")
    except AttributeError:
        # Manejar el caso de que la columna no sea de tipo string
        print("La columna dispositivo_legal no es de tipo string")
    # Retornar el dataframe limpio
    return df

# Aplicar la función de limpieza al dataframe
df = limpiar(df)

# Asignar el valor del tipo de cambio del dólar que me has dado
tipo_cambio = 3.777

# Crear dos nuevas columnas con los montos de inversión y transferencia en dólares
df["monto_de_inversion_dolares"] = df["monto_de_inversión"] / tipo_cambio
df["monto_de_transferencia_2020_dolares"] = df["monto_de_transferencia_2020"] / tipo_cambio

# Cambiar los valores de la columna "estado" a: Actos Previos, Concluido, Resuelto y Ejecucion
df["estado"] = df["estado"].replace({"Actos Previos": "Actos Previos", "Concluido": "Concluido", "Resuelto": "Resuelto", "Ejecución": "Ejecucion"})

# Crear una nueva columna que puntue el estado según: ActosPrevios -> 1, Resuelto->0, Ejecución 2 y Concluido 3
df["puntaje_estado"] = df["estado"].map({"Actos Previos": 1, "Resuelto": 0, "Ejecucion": 2, "Concluido": 3})

# Almacenar en una base de datos una tabla de ubigeos a partir de los datos sin duplicados de las columnas “ubigeo”, “Region”, “Provincia”, “Distrito”
# Importar sqlalchemy para crear una conexión con la base de datos
import sqlalchemy
# Crear una conexión con la base de datos usando el método create_engine
# Se asume que la base de datos se llama "reactiva_db" y se encuentra en el servidor local
engine = sqlalchemy.create_engine("postgresql://username:password@localhost/reactiva_db")
# Crear un dataframe con los datos sin duplicados de las columnas de ubigeo
ubigeo_df = df[["ubigeo", "region", "provincia", "distrito"]].drop_duplicates()
# Almacenar el dataframe en la base de datos como una tabla llamada "ubigeo"
ubigeo_df.to_sql("ubigeo", engine, index=False, if_exists="replace")

# Por cada región genere un Excel con el top 5 costo inversión de las obras de tipo Urbano en estado 1,2,3
# Filtrar el dataframe por las obras de tipo Urbano en estado 1,2,3
urbano_df = df[(df["tipologia"] == "Pista y Vereda") & (df["puntaje_estado"].isin([1, 2, 3]))]
# Agrupar el dataframe por región y ordenar los valores por el monto de inversión en dólares de forma descendente
urbano_df = urbano_df.groupby("region").apply(lambda x: x.sort_values("monto_de_inversion_dolares", ascending=False))
# Obtener el top 5 de cada región usando el método head
urbano_df = urbano_df.groupby("region").head(5)
# Por cada región, generar un Excel con el nombre de la región y guardar el dataframe correspondiente
for region in urbano_df["region"].unique():
    region_df = urbano_df[urbano_df["region"] == region]
    region_df.to_excel(f"{region}.xlsx", index=False)

# Crear un modulo envio_correo.py que se encargue de la parte de envio de correo
# Importar smtplib para enviar correos electrónicos
import smtplib
# Importar email para crear el mensaje del correo
from email.message import EmailMessage

# Crear una función para enviar un correo con el archivo adjunto de una región
def enviar_correo(region):
    # Crear el mensaje del correo
    mensaje = EmailMessage()
    # Establecer el asunto del correo
    mensaje["Subject"] = f"Reporte de la región {region}"
    # Establecer el remitente del correo
    mensaje["From"] = "copilot@reactiva.com"
    # Establecer el destinatario del correo
    mensaje["To"] = "usuario@reactiva.com"
    # Establecer el contenido del correo
    mensaje.set_content(f"Estimado usuario, \n\nAdjunto encontrará el reporte de la región {region} con el top 5 de costo inversión de las obras de tipo Urbano en estado 1,2,3. \n\nSaludos, \nCopilot")
    # Abrir el archivo de Excel de la región
    with open(f"{region}.xlsx", "rb") as archivo:
        # Leer el contenido del archivo
        contenido = archivo.read()
        # Agregar el archivo como adjunto al mensaje
        mensaje.add_attachment(contenido, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{region}.xlsx")
    # Crear una conexión con el servidor de correo usando SMTP
    with smtplib.SMTP("localhost") as servidor:
        # Enviar el mensaje
        servidor.send_message(mensaje)

# Integrar los módulos y tomar captura al menos de uno de los correos enviados mediante código
# Importar el módulo procesamiento.py
import procesamiento
# Importar el módulo envio_correo.py
import envio_correo
# Por cada región, enviar un correo con el archivo adjunto
for region in procesamiento.urbano_df["region"].unique():
    envio_correo.enviar_correo(region)
