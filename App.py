import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide", page_title="SBD City - Smart City Sabadell")

st.title("🌐 SBD City - Plataforma de Datos Urbanos de Sabadell")

st.markdown("Esta plataforma recoge y visualiza datos públicos en tiempo real para seguridad, transporte, medio ambiente y más en Sabadell.")

# -----------------------------
# FUNCIONES DE CARGA DE DATOS
# -----------------------------

@st.cache_data(ttl=3600)
def cargar_datos_api():
    data = {}

    try:
        # 1. Calidad del aire - Generalitat
        aire_url = "https://analisi.transparenciacatalunya.cat/resource/tasf-thgu.json?$limit=1000"
        aire_data = requests.get(aire_url).json()
        df_aire = pd.DataFrame(aire_data)
        df_aire = df_aire[df_aire["municipi_nom"] == "Sabadell"]
        data["aire"] = df_aire
    except Exception as e:
        data["aire"] = None
        st.warning("⚠️ No se pudo cargar la calidad del aire.")

    try:
        # 2. Transporte público - AMB
        tmb_url = "https://api.tmb.cat/v1/transit/linies/bus"
        # No usamos token, asumimos un ejemplo (esto puede ajustarse a otras fuentes abiertas reales sin auth)
        tmb_data = requests.get("https://opendata-ajuntament.barcelona.cat/data/api/action/datastore_search?resource_id=76f1f8d5-daa7-4a4c-a63e-1e2b8e63b1a4&limit=100").json()
        df_tmb = pd.DataFrame(tmb_data["result"]["records"])
        data["transporte"] = df_tmb
    except Exception:
        data["transporte"] = None
        st.warning("⚠️ No se pudo cargar la información de transporte público.")

    try:
        # 3. Datos IDESCAT - Población, vivienda, economía
        idescat_url = "https://api.idescat.cat/emex/v1/dades.json?id=08202"
        idescat_data = requests.get(idescat_url).json()
        data["idescat"] = idescat_data
    except Exception:
        data["idescat"] = None
        st.warning("⚠️ No se pudo cargar la información estadística municipal.")

    try:
        # 4. Incidentes o eventos públicos (simulado con eventos)
        eventos_url = "https://analisi.transparenciacatalunya.cat/resource/qh7u-hdsk.json?$limit=1000"
        eventos_data = requests.get(eventos_url).json()
        df_eventos = pd.DataFrame(eventos_data)
        df_eventos = df_eventos[df_eventos["municipi"] == "Sabadell"]
        data["eventos"] = df_eventos
    except Exception:
        data["eventos"] = None
        st.warning("⚠️ No se pudo cargar la información de eventos.")

    try:
        # 5. Catálogo Open Data Sabadell
        catalogo_url = "https://opendata-ajuntament.sabadell.cat/data/api/3/action/package_list"
        catalogo_data = requests.get(catalogo_url).json()
        data["catalogo"] = catalogo_data["result"]
    except Exception:
        data["catalogo"] = None
        st.warning("⚠️ No se pudo cargar el catálogo de datasets.")

    return data

datos = cargar_datos_api()

# -----------------------------
# VISUALIZACIONES
# -----------------------------

st.subheader("📊 Calidad del Aire en Sabadell")
if datos["aire"] is not None and not datos["aire"].empty:
    st.dataframe(datos["aire"][["codi_captador", "magnitud", "valor", "unitats", "hora", "data"]].sort_values("data", ascending=False).head(10))
else:
    st.info("Sin datos recientes de calidad del aire.")

st.subheader("🚍 Transporte Público (AMB/TMB)")
if datos["transporte"] is not None and not datos["transporte"].empty:
    st.dataframe(datos["transporte"][["linia", "nomlinia", "sentit", "origen", "desti"]].head(10))
else:
    st.info("Sin datos de transporte público disponibles.")

st.subheader("📈 Estadísticas de Sabadell (IDESCAT)")
if datos["idescat"]:
    estats = datos["idescat"]["fitxes"]
    for estat in estats[:5]:
        st.write(f"📌 {estat['titol']}: {estat['valor']} {estat.get('unitat', '')}")
else:
    st.info("No se encontraron estadísticas municipales.")

st.subheader("🎉 Eventos Públicos y Actividades")
if datos["eventos"] is not None and not datos["eventos"].empty:
    st.dataframe(datos["eventos"][["nom", "data_inici", "lloc", "adreca"]].head(10))
else:
    st.info("Sin eventos registrados actualmente.")

st.subheader("📚 Catálogo de Datos Abiertos")
if datos["catalogo"]:
    for ds in datos["catalogo"][:5]:
        st.markdown(f"🔗 [{ds}](https://opendata-ajuntament.sabadell.cat/data/dataset/{ds})")
else:
    st.info("No se pudo mostrar el catálogo de datasets.")

# -----------------------------
# MAPA DE UBICACIONES (Ejemplo)
# -----------------------------

st.subheader("🗺️ Mapa interactivo de Sabadell")
m = folium.Map(location=[41.5463, 2.1086], zoom_start=13)

if datos["aire"] is not None:
    for _, row in datos["aire"].iterrows():
        try:
            lat = float(row["latitud"])
            lon = float(row["longitud"])
            folium.Marker(location=[lat, lon], tooltip=f"{row['magnitud']} - {row['valor']} {row['unitats']}").add_to(m)
        except:
            continue

st_folium(m, width=1000, height=500)
