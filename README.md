# FireSAT Launch Trade-off — versión web

Conversión de `FireSAT_simulador_sin_widgets.ipynb` a Streamlit. Se reutiliza el catálogo de 27 combinaciones y la lógica de coste de la versión Jupyter, separados en `launchers.csv` y `simulator.py`.

## Publicación sin Anaconda
1. Crea un repositorio en GitHub.
2. Sube `app.py`, `simulator.py`, `launchers.csv`, `requirements.txt` y `README.md` a la **raíz** del repositorio.
3. Ve a https://share.streamlit.io y selecciona **Create app → Deploy from GitHub**.
4. Selecciona tu repositorio, rama `main`, archivo principal `app.py` y pulsa **Deploy**.
5. Comparte la URL `.streamlit.app` que se genere.

## Ejecución local opcional
`pip install -r requirements.txt` y `streamlit run app.py`.

## Advertencias
Todos los costes son supuestos editables de fase 0/A. El filtro de inclinación/altitud/familia orbital es simplificado y **no** confirma acceso al corredor de lanzamiento, LTAN/RAAN, capacidad másica específica, dispensador ICD, maniobra OTV ni reserva de plaza. Las opciones '🟡 Por confirmar' requieren solicitud de oferta (RFQ). El color verde solo señala que se superó el cribado preliminar.
