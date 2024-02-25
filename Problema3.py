import pandas as pd
import requests

df = pd.read_csv("reactiva1.csv", sep=";")

# Crear una función de limpieza
def limpiar(df):
    df.columns = df.columns.str.replace(" ", "_").str.replace("á", "a").str.replace("é", "e").str.replace("í", "i").str.replace("ó", "o").str.replace("ú", "u").str.lower()
    df = df.drop(columns=["id", "tipo_moneda"], axis=1, errors="ignore")
    try:
        df["dispositivo_legal"] = df["dispositivo_legal"].str.replace(",", "")
    except AttributeError:
        print("La columna dispositivo_legal no es de tipo string")
    return df

df = limpiar(df)

tipo_cambio = 3.777

df["monto_de_inversion_dolares"] = df["monto_de_inversión"] / tipo_cambio
df["monto_de_transferencia_2020_dolares"] = df["monto_de_transferencia_2020"] / tipo_cambio

df["estado"] = df["estado"].replace({"Actos Previos": "Actos Previos", "Concluido": "Concluido", "Resuelto": "Resuelto", "Ejecución": "Ejecucion"})

df["puntaje_estado"] = df["estado"].map({"Actos Previos": 1, "Resuelto": 0, "Ejecucion": 2, "Concluido": 3})


import sqlalchemy

engine = sqlalchemy.create_engine("postgresql://postgres:5432@localhost/reactiva", echo=True)
ubigeo_df = df[["ubigeo", "region", "provincia", "distrito"]].drop_duplicates()
ubigeo_df.to_sql("ubigeo", engine, index=False, if_exists="replace")


urbano_df = df[(df["tipologia"] == "Pista y Vereda") & (df["puntaje_estado"].isin([1, 2, 3]))]

urbano_df = urbano_df.reset_index(drop=True)

urbano_df = urbano_df.groupby("region").apply(lambda x: x.sort_values("monto_de_inversion_dolares", ascending=False)).reset_index(drop=True)

# Obtener el top 5 de cada región usando el método head
top_urbano_df = urbano_df.groupby("region").head(5)

for region in top_urbano_df["region"].unique():
    region_df = top_urbano_df[top_urbano_df["region"] == region]
    region_df.to_excel(f"{region}.xlsx", index=False)




import smtplib
from email.message import EmailMessage

def enviar_correo(region):
    mensaje = EmailMessage()
    mensaje["Subject"] = f"Reporte de la región {region}"
    mensaje["From"] = "copilot@reactiva.com"
    mensaje["To"] = "usuario@reactiva.com"
    mensaje.set_content(f"Estimado usuario, \n\nAdjunto encontrará el reporte de la región {region} con el top 5 de costo inversión de las obras de tipo Urbano en estado 1,2,3. \n\nSaludos, \nCopilot")
    with open(f"{region}.xlsx", "rb") as archivo:
        contenido = archivo.read()
        mensaje.add_attachment(contenido, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=f"{region}.xlsx")
    with smtplib.SMTP("localhost") as servidor:
        servidor.send_message(mensaje)

import procesamiento
import envio_correo
for region in procesamiento.urbano_df["region"].unique():
    envio_correo.enviar_correo(region)
