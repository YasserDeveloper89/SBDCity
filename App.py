import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
import joblib
import requests
from io import StringIO

# ---------------------- Configuración ----------------------
st.set_page_config(page_title="Seguridad Sabadell", layout="wide")

# ---------------------- Carga de Datos Públicos ----------------------
def cargar_datos():
    urls = {
        "demografia": "https://opendata.sabadell.cat/data/demografia.csv",
        "servicios": "https://opendata.sabadell.cat/data/serveis-publics.csv",
        "economia": "https://opendata.sabadell.cat/data/economia.csv",
    }
    datos = {}
    for nombre, url in urls.items():
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'
            df = pd.read_csv(StringIO(response.text))
            datos[nombre] = df
        except:
            datos[nombre] = pd.DataFrame()
    return datos

# ---------------------- Visualización en Mapa ----------------------
def mapa_servicios(df):
    m = folium.Map(location=[41.5463, 2.1086], zoom_start=13)
    for _, row in df.iterrows():
        try:
            folium.Marker(
                location=[row['lat'], row['lon']],
                popup=row['nom'],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        except:
            continue
    return m

# ---------------------- Modelo Predictivo ----------------------
def entrenar_modelo(df):
    if 'lat' in df.columns and 'lon' in df.columns:
        X = df[['lat', 'lon']]
        modelo = KMeans(n_clusters=5)
        modelo.fit(X)
        joblib.dump(modelo, "models/modelo_prediccion.pkl")
        return modelo
    return None

def predecir_incidente(lat, lon, modelo):
    cluster = modelo.predict([[lat, lon]])
    return int(cluster[0])

# ---------------------- Panel Principal ----------------------
def panel():
    st.title("🚨 Plataforma de Seguridad Ciudadana - Sabadell")
    datos = cargar_datos()

    st.sidebar.header("Datos en Tiempo Real")
    seccion = st.sidebar.radio("Seleccionar Sección", ["Demografía", "Servicios Públicos", "Economía", "Mapa y Análisis"])

    if seccion == "Demografía":
        df = datos["demografia"]
        st.subheader("🌐 Datos Demográficos")
        st.dataframe(df)

    elif seccion == "Servicios Públicos":
        df = datos["servicios"]
        st.subheader("🚧 Servicios Públicos")
        st.dataframe(df)

    elif seccion == "Economía":
        df = datos["economia"]
        st.subheader("💰 Datos Económicos")
        st.dataframe(df)

    elif seccion == "Mapa y Análisis":
        df = datos["servicios"]
        st.subheader("Mapa de Servicios")
        if not df.empty:
            mapa = mapa_servicios(df)
            st_folium(mapa, width=800, height=600)

            modelo = entrenar_modelo(df)
            if modelo:
                st.subheader("🧰 Predicción de Zona Crítica")
                lat = st.number_input("Latitud", value=41.5463)
                lon = st.number_input("Longitud", value=2.1086)
                if st.button("Predecir Zona"):
                    zona = predecir_incidente(lat, lon, modelo)
                    st.success(f"Zona de Riesgo Estimada: Grupo {zona}")

# ---------------------- Ejecutar ----------------------
if __name__ == "__main__":
    panel()
