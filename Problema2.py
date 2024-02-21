# Importar la librería Pandas
import pandas as pd

# Leer el archivo csv con los datos de las reseñas
df_vinos = pd.read_csv("winemag-data-130k-v2.csv")

# Explorar el dataframe según lo visto en clase
df_vinos.head() # Mostrar las primeras 5 filas
df_vinos.info() # Mostrar información general del dataframe
df_vinos.describe() # Mostrar estadísticas descriptivas de las columnas numéricas
df_vinos.shape # Mostrar el número de filas y columnas
df_vinos.columns # Mostrar los nombres de las columnas
df_vinos.dtypes # Mostrar los tipos de datos de las columnas

# Renombrar algunas columnas según criterio
df_vinos = df_vinos.rename(columns={"country": "país", "description": "descripción", "points": "puntos", "price": "precio"})

# Crear algunas columnas nuevas según criterio

# Definir una función que lea el archivo paises.csv y devuelva el continente de cada país
def asignar_continente(pais):
    # Leer el archivo paises.csv como un dataframe
    df_paises = pd.read_csv("https://gist.githubusercontent.com/kintero/7d1db891401f56256c79/raw/a61f6d0dda82c3f04d2e6e76c3870552ef6cf0c6/paises.csv")
    # Buscar el país en el dataframe y extraer el continente
    continente = df_paises.loc[df_paises["name"] == pais, "continente"].values[0]
    # Devolver el continente
    return continente

# Definir una función que clasifique el vino según su puntuación
def clasificar_calidad(puntos):
    # Definir los rangos de puntos para cada etiqueta
    if puntos >= 90:
        calidad = "excelente"
    elif puntos >= 80:
        calidad = "bueno"
    elif puntos >= 70:
        calidad = "regular"
    else:
        calidad = "malo"
    # Devolver la etiqueta
    return calidad

# Crear la columna "continente" usando la función asignar_continente
df_vinos = df_vinos.assign(continente = df_vinos["país"].apply(asignar_continente))

# Crear la columna "calidad" usando la función clasificar_calidad
df_vinos = df_vinos.assign(calidad = df_vinos["puntos"].apply(clasificar_calidad))

# Crear la columna "relación" usando una expresión que divida el precio entre los puntos y multiplique por 100
df_vinos = df_vinos.assign(relación = (df_vinos["precio"] / df_vinos["puntos"]) * 100)

# Generar algunos reportes por agrupamiento de datos

# Reporte 1: Promedio de precio y cantidad de reseñas obtenidas según el país, ordenado de mejor a peor
reporte_1 = df_vinos.groupby("país").agg({"precio": "mean", "descripción": "count"}).rename(columns={"precio": "precio_promedio", "descripción": "número_de_reseñas"}).sort_values(by=["precio_promedio", "número_de_reseñas"], ascending=False)
print("Reporte 1:")
print(reporte_1.to_markdown())

# Reporte 2: Los vinos mejor puntuados por continente
reporte_2 = df_vinos.groupby("continente").max()[["país", "puntos", "precio", "taster_name", "title", "variety", "winery"]]
print("Reporte 2:")
print(reporte_2.to_markdown())

# Reporte 3: La distribución de la calidad del vino por país
reporte_3 = df_vinos.groupby("país")["calidad"].value_counts().unstack().fillna(0)
print("Reporte 3:")
print(reporte_3.to_markdown())

# Reporte 4: El top 10 de los vinos con mejor relación entre precio y puntuación
reporte_4 = df_vinos.nlargest(n=10, columns="relación")[["país", "puntos", "precio", "relación", "taster_name", "title", "variety", "winery"]]
print("Reporte 4:")
print(reporte_4.to_markdown())

# Guardar alguno de estos datos agrupados en excel o csv
# Por ejemplo, guardar el reporte 1 como un archivo excel llamado "reporte_1.xlsx"
reporte_1.to_excel("reporte_1.xlsx", index=False)
