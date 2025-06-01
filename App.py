# App.py
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime
import json
import os

st.set_page_config(page_title="SmartCity Sabadell", layout="wide")

# Cargar datos locales (desde carpeta datasets)
def cargar_datos():
    base_path = os.path.join(os.path.dirname(__file__), 'datasets')

    with open(os.path.join(base_path, 'obras.json'), 'r', encoding='utf-8') as f:
        obras = json.load(f)

    incidentes = pd.read_csv(os.path.join(base_path, 'incidentes.csv'))

    with open(os.path.join(base_path, 'eventos.json'), 'r', encoding='utf-8') as f:
        eventos = json.load(f)

    zonas_verdes = pd.read_json(os.path.join(base_path, 'zonas_verdes.geojson'))

    return obras, incidentes, eventos, zonas_verdes

obras, incidentes, eventos, zonas_verdes = cargar_datos()

st.title("🌆 SmartCity Sabadell - Plataforma de Seguridad y Datos Urbanos")
st.markdown("""Esta plataforma permite visualizar en tiempo real datos abiertos de Sabadell relacionados con:
- Incidentes urbanos y de seguridad
- Obras públicas
- Eventos
- Zonas verdes
""")

# Mapa de obras
st.subheader("🚧 Obras públicas activas")
mapa = folium.Map(location=[41.5463, 2.1086], zoom_start=13)
for o in obras['features']:
    coords = o['geometry']['coordinates']
    desc = o['properties'].get('descripcio', 'Obra')
    folium.Marker(location=[coords[1], coords[0]], tooltip=desc, icon=folium.Icon(color="orange")).add_to(mapa)

st_data = st_folium(mapa, width=800)

# Tabla y análisis de incidentes
st.subheader("🚒 Estadísticas de incidentes ciudadanos")
st.dataframe(incidentes)

col1, col2 = st.columns(2)
with col1:
    fig1 = px.histogram(incidentes, x='tipo', color='tipo', title='Incidentes por tipo')
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    fig2 = px.line(incidentes.groupby('fecha').size().reset_index(name='conteo'), x='fecha', y='conteo', title='Evolución temporal')
    st.plotly_chart(fig2, use_container_width=True)

# Eventos
st.subheader("🎉 Eventos y actividades en Sabadell")
for ev in eventos['features'][:5]:
    props = ev['properties']
    st.markdown(f"- **{props.get('title', 'Evento')}**: {props.get('description', 'Sin descripción')}")

# Zonas verdes
st.subheader("🌿 Parques y zonas verdes")
st.map(zonas_verdes)

st.success("Plataforma funcional cargada con datos reales y lista para ampliarse con modelos predictivos y alertas.")
    
