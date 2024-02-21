# Importar la librería Pandas
import pandas as pd

df_airbnb = pd.read_csv("airbnb.csv")

# Caso 1
df_alicia = df_airbnb.query("reviews > 10 and overall_satisfaction > 4 and bedrooms >= 2")

df_alicia = df_alicia.sort_values(by=["overall_satisfaction", "reviews"], ascending=False)

df_alicia = df_alicia.head(n=3)

print("Estas son las 3 mejores opciones para Alicia:")
print(df_alicia.to_markdown())

# Caso 2
df_roberto = df_airbnb.query("room_id == 97503 or room_id == 90387")

df_roberto.to_excel("roberto.xlsx", index=False)

# Caso 3
df_diana = df_airbnb.query("price <= 50")

df_diana = df_diana.sort_values(by=["room_type", "overall_satisfaction"], ascending=False)

df_diana = df_diana.head(n=10)

print("Estas son las 10 opciones más baratas para Diana:")
print(df_diana.to_markdown())
