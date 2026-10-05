"""
Análisis de sensores industriales
Primer parcial - Manejo Masivo de Datos (UPQ)
Autor: Yuliana Elizabeth Banda Del Angel

Este programa lee el archivo data/sensores_industriales.csv y calcula:
  1) Cantidad de registros y de sensores distintos
  2) Temperatura promedio por planta
  3) Temperatura máxima con sensor y fecha
  4) Cantidad de lecturas con temperatura > 85 °C
  5) Planta con más alertas (soporta empates)
  6) Exporta todas las alertas a resultados/alertas.csv
"""

import pandas as pd
from pathlib import Path

# ---------- Configuración de rutas (relativas) ----------
RUTA_CSV = Path("data") / "sensores_industriales.csv"
RUTA_SALIDA = Path("resultados") / "alertas.csv"
UMBRAL_TEMPERATURA = 85  # °C, según regla didáctica del examen

# ---------- Lectura del archivo ----------
print("=" * 60)
print("ANÁLISIS DE SENSORES INDUSTRIALES")
print("=" * 60)

df = pd.read_csv(RUTA_CSV)

# ---------- 1) Cantidad de registros y sensores distintos ----------
total_registros = len(df)
sensores_distintos = df["id_sensor"].nunique()

print(f"\n1) Total de registros: {total_registros}")
print(f"   Sensores distintos: {sensores_distintos}")

# ---------- 2) Temperatura promedio por planta ----------
promedio_por_planta = df.groupby("planta")["temperatura_c"].mean().round(2)

print("\n2) Temperatura promedio por planta (°C):")
for planta, promedio in promedio_por_planta.items():
    print(f"   {planta}: {promedio}")

# ---------- 3) Temperatura máxima (sensor y fecha) ----------
temp_max = df["temperatura_c"].max()
# Filtramos todas las filas con esa temp máxima (por si hay empates)
filas_max = df[df["temperatura_c"] == temp_max]

print(f"\n3) Temperatura máxima registrada: {temp_max} °C")
for _, fila in filas_max.iterrows():
    print(f"   Sensor: {fila['id_sensor']}  |  Fecha: {fila['fecha_hora']}  |  Planta: {fila['planta']}")

# ---------- 4) Lecturas con temperatura > 85 °C ----------
alertas = df[df["temperatura_c"] > UMBRAL_TEMPERATURA]
total_alertas = len(alertas)

print(f"\n4) Lecturas con temperatura > {UMBRAL_TEMPERATURA} °C: {total_alertas}")

# ---------- 5) Planta con más alertas (soporta empates) ----------
alertas_por_planta = alertas["planta"].value_counts()
max_alertas = alertas_por_planta.max()
plantas_top = alertas_por_planta[alertas_por_planta == max_alertas]

print(f"\n5) Planta(s) con más alertas ({max_alertas} alertas cada una):")
for planta, cantidad in plantas_top.items():
    print(f"   {planta}: {cantidad}")

# ---------- 6) Exportar alertas a CSV ----------
RUTA_SALIDA.parent.mkdir(exist_ok=True)  # Asegura que la carpeta exista
alertas.to_csv(RUTA_SALIDA, index=False)

print(f"\n6) Alertas exportadas a: {RUTA_SALIDA} ({total_alertas} filas)")
print("\n" + "=" * 60)
print("Análisis completado ✓")
print("=" * 60)
