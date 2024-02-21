# Importar la librería Pandas
import pandas as pd

df_vinos = pd.read_csv("winemag-data-130k-v2.csv", encoding="latin-1")

df_paises = pd.read_csv("https://gist.githubusercontent.com/kintero/7d1db891401f56256c79/raw/a61f6d0dda82c3f04d2e6e76c3870552ef6cf0c6/paises.csv")

df_vinos = pd.merge(df_vinos, df_paises, left_on="país", right_on="name")

df_vinos = df_vinos.rename(columns={"country": "país", "description": "descripción", "points": "puntos", "price": "precio"})


def clasificar_calidad(puntos):
    if puntos >= 90:
        calidad = "excelente"
    elif puntos >= 80:
        calidad = "bueno"
    elif puntos >= 70:
        calidad = "regular"
    else:
        calidad = "malo"
    return calidad

df_vinos = df_vinos.assign(calidad = df_vinos["puntos"].apply(clasificar_calidad))

df_vinos = df_vinos.assign(relación = (df_vinos["precio"] / df_vinos["puntos"]) * 100)


reporte_1 = df_vinos.groupby("país").agg({"precio": "mean", "descripción": "count"}).rename(columns={"precio": "precio_promedio", "descripción": "número_de_reseñas"}).sort_values(by=["precio_promedio", "número_de_reseñas"], ascending=False)
print("Reporte 1:")
print(reporte_1.to_markdown())

reporte_2 = df_vinos.groupby("continente").max()[["país", "puntos", "precio", "taster_name", "title", "variety", "winery"]]
print("Reporte 2:")
print(reporte_2.to_markdown())

reporte_3 = df_vinos.groupby("país")["calidad"].value_counts().unstack().fillna(0)
print("Reporte 3:")
print(reporte_3.to_markdown())

reporte_4 = df_vinos.nlargest(n=10, columns="relación")[["país", "puntos", "precio", "relación", "taster_name", "title", "variety", "winery"]]
print("Reporte 4:")
print(reporte_4.to_markdown())

reporte_1.to_excel("reporte_1.xlsx", index=False)
