import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(page_title="Seguridad Ciudadana Sabadell", layout="wide")

st.title("🔒 Seguridad Ciudadana Sabadell")

# Cargar datos de sensores ambientales
@st.cache_data
def cargar_sensores_ambientales():
    url = "https://opendata.sabadell.cat/dataset/qualitat-aire/resource/ID_DEL_RECURSO/download/qualitat-aire.csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# Cargar datos de movilidad urbana
@st.cache_data
def cargar_mobilitat():
    url = "https://opendata.sabadell.cat/dataset/mobilitat/resource/ID_DEL_RECURSO/download/mobilitat.csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# Cargar datos de seguridad ciudadana
@st.cache_data
def cargar_seguridad():
    url = "https://opendata.sabadell.cat/dataset/seguretat-ciutadana/resource/ID_DEL_RECURSO/download/seguretat-ciutadana.csv"
    try:
        df = pd.read_csv(url)
        return df
    except:
        return pd.DataFrame()

# Visualizar mapa con datos
def mostrar_mapa(df, lat_col, lon_col, popup_col):
    m = folium.Map(location=[41.5463, 2.1086], zoom_start=13)
    for _, row in df.iterrows():
        try:
            folium.Marker(
                location=[row[lat_col], row[lon_col]],
                popup=row[popup_col],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        except:
            continue
    st_folium(m, width=700, height=500)

# Menú lateral
menu = st.sidebar.selectbox("Selecciona una opción", ["Sensores Ambientales", "Movilidad Urbana", "Seguridad Ciudadana"])

if menu == "Sensores Ambientales":
    st.header("🌬️ Sensores Ambientales")
    df_sensores = cargar_sensores_ambientales()
    if not df_sensores.empty:
        st.dataframe(df_sensores)
        mostrar_mapa(df_sensores, 'latitud', 'longitud', 'nom_sensor')
    else:
        st.warning("No se pudieron cargar los datos de sensores ambientales.")

elif menu == "Movilidad Urbana":
    st.header("🚌 Movilidad Urbana")
    df_mobilitat = cargar_mobilitat()
    if not df_mobilitat.empty:
        st.dataframe(df_mobilitat)
        mostrar_mapa(df_mobilitat, 'latitud', 'longitud', 'nom_parada')
    else:
        st.warning("No se pudieron cargar los datos de movilidad urbana.")

elif menu == "Seguridad Ciudadana":
    st.header("🚓 Seguridad Ciudadana")
    df_seguridad = cargar_seguridad()
    if not df_seguridad.empty:
        st.dataframe(df_seguridad)
        mostrar_mapa(df_seguridad, 'latitud', 'longitud', 'tipus_incident')
    else:
        st.warning("No se pudieron cargar los datos de seguridad ciudadana.")
