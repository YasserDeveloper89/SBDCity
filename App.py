import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import json

st.set_page_config(page_title="Sabadell SmartCity", layout="wide")
st.title("🌐 Plataforma de Control - SmartCity Sabadell")

# ---------------- Carga de Datos ----------------
def cargar_datos():
    obras = json.load(open("obras.json", encoding="utf-8"))
    incidentes = pd.read_csv("incidentes.csv")
    eventos = json.load(open("eventos.json", encoding="utf-8"))
    zonas_verdes = json.load(open("zonas_verdes.geojson", encoding="utf-8"))
    return obras, incidentes, eventos, zonas_verdes

try:
    obras, incidentes, eventos, zonas_verdes = cargar_datos()
except Exception as e:
    st.error(f"No se pudieron cargar los datos: {e}")
    st.stop()

# ---------------- Visualización ----------------
st.header("🛠️ Obras Activas")
for o in obras:
    st.markdown(f"- {o['titulo']} ({o['estado']})")

st.header("🚨 Últimos Incidentes Reportados")
st.dataframe(incidentes)

st.header("🎉 Eventos Públicos")
for e in eventos:
    st.markdown(f"- {e['nombre']} - {e['fecha']} ({e['ubicacion']})")

st.header("🗺️ Mapa Interactivo")
m = folium.Map(location=[41.548, 2.107], zoom_start=14)
for z in zonas_verdes["features"]:
    folium.Polygon(z["geometry"]["coordinates"][0], color="green", tooltip=z["properties"]["nombre"]).add_to(m)
for o in obras:
    folium.Marker(location=[o["lat"], o["lon"]], tooltip=o["titulo"], icon=folium.Icon(color="orange")).add_to(m)
st_folium(m, width=1000, height=500)