import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SBDCity - Datos Abiertos de Sabadell", layout="wide")

st.title("🌐 SBDCity - Plataforma de Datos Abiertos de Sabadell")
st.markdown("Esta aplicación muestra información en tiempo real desde fuentes públicas para Sabadell.")

@st.cache_data
def cargar_datos():
    datos = {}

    # 1. Open Data Sabadell - Lista de datasets
    try:
        url_sabadell = "https://opendata.sabadell.cat/api/3/action/package_list"
        response = requests.get(url_sabadell)
        response.raise_for_status()
        datos["sabadell"] = response.json()
    except Exception as e:
        st.error(f"Error al cargar datos de Open Data Sabadell: {e}")
        datos["sabadell"] = None

    # 2. Generalitat de Catalunya - Calidad del aire
    try:
        url_aire = "https://analisi.transparenciacatalunya.cat/resource/7rq3-m6zv.json?$limit=100"
        response = requests.get(url_aire)
        response.raise_for_status()
        datos["aire"] = response.json()
    except Exception as e:
        st.error(f"Error al cargar datos de calidad del aire: {e}")
        datos["aire"] = None

    # 3. Idescat - Datos de Sabadell
    try:
        url_idescat = "https://api.idescat.cat/emex/v1/dades.json?lang=es&id=08202"
        response = requests.get(url_idescat)
        response.raise_for_status()
        datos["idescat"] = response.json()
    except Exception as e:
        st.error(f"Error al cargar datos de Idescat: {e}")
        datos["idescat"] = None

    # 4. AMB - Transporte público
    try:
        url_amb = "https://opendata.amb.cat/api/3/action/package_list"
        response = requests.get(url_amb)
        response.raise_for_status()
        datos["amb"] = response.json()
    except Exception as e:
        st.error(f"Error al cargar datos de AMB: {e}")
        datos["amb"] = None

    # 5. Datos.gob.es - Catálogo de datos
    try:
        url_datosgob = "https://datos.gob.es/apidata/catalog/dataset"
        response = requests.get(url_datosgob)
        response.raise_for_status()
        datos["datosgob"] = response.json()
    except Exception as e:
        st.error(f"Error al cargar datos de datos.gob.es: {e}")
        datos["datosgob"] = None

    return datos

datos = cargar_datos()

if datos["sabadell"]:
    st.subheader("📦 Datasets disponibles en Open Data Sabadell")
    st.json(datos["sabadell"])

if datos["aire"]:
    st.subheader("🌫 Calidad del aire - Generalitat de Catalunya")
    df_aire = pd.DataFrame(datos["aire"])
    st.dataframe(df_aire)

if datos["idescat"]:
    st.subheader("📊 Estadísticas de Sabadell - Idescat")
    st.json(datos["idescat"])

if datos["amb"]:
    st.subheader("🚌 Transporte público - AMB")
    st.json(datos["amb"])

if datos["datosgob"]:
    st.subheader("📚 Catálogo de datos - datos.gob.es")
    st.json(datos["datosgob"])
