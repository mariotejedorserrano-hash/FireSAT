import streamlit as st
import pandas as pd
from simulator import load_launchers, calculate

st.set_page_config(page_title='FireSAT | Launch Trade-off',page_icon='🚀',layout='wide')
st.title('FireSAT · Launch Trade-off')
st.caption('Fase 0/A · Comparación de lanzadores, compatibilidad orbital preliminar y desglose económico')
st.warning('Los precios, la capacidad orbital y la disponibilidad comercial son hipótesis editables. 🟢 no garantiza una plaza rideshare ni una órbita contratada. La SSO, LTAN, RAAN y los OTV requieren verificación específica.')
with st.sidebar:
 st.header('1 · Constelación')
 unit=st.selectbox('Formato CubeSat',['2U','4U','6U','8U'],index=3)
 n=st.number_input('Número de satélites',1,30,6)
 mass=st.number_input('Masa por satélite (kg)',0.5,100.,float({'2U':4,'4U':8,'6U':12,'8U':16}[unit]),0.5)
 planes=st.number_input('Planos orbitales',1,int(n),min(2,int(n)))
 st.header('2 · Órbita')
 alt=st.number_input('Altitud (km)',200,1500,525,25)
 inc=st.number_input('Inclinación (°)',0.,180.,97.5,0.5)
 inc_tol=st.slider('Tolerancia inclinación (°)',0.,10.,1.,0.5)
 alt_tol=st.slider('Tolerancia altitud (km)',0,200,50,10)
 st.header('3 · Estrategia')
 strategy=st.selectbox('Despliegue',['Una campaña por plano','Todos juntos + OTV','Dedicado por plano'])
 origin=st.selectbox('Origen de transporte',['Spain','France','USA','Other'])
 with st.expander('Hipótesis económicas',expanded=False):
  deployer=st.number_input('Dispensador e integración por satélite ($)',0,1000000,35000,5000)
  campaign_fee=st.number_input('Gestión de campaña ($)',0,2000000,75000,5000)
  otv_fee=st.number_input('OTV por plano adicional ($)',0,20000000,800000,50000)
  reserve=st.slider('Reserva (%)',0,50,10)

catalog=load_launchers()
tab1,tab2,tab3=st.tabs(['Resultados','Desglose de costes','Catálogo de lanzadores'])
with tab3:
 st.caption('Modifica la tabla para comparar hipótesis. Los cambios se aplican al resto de pestañas.')
 catalog=st.data_editor(catalog,num_rows='dynamic',hide_index=True,use_container_width=True,key='catalog')
result=calculate(catalog,n=n,unit=unit,mass=mass,planes=planes,alt=alt,inc=inc,inc_tol=inc_tol,alt_tol=alt_tol,strategy=strategy,origin=origin,deployer=deployer,campaign_fee=campaign_fee,otv_fee=otv_fee,reserve_pct=reserve)
valid=result[~result['Estado'].str.contains('Incompatible')]
with tab1:
 c1,c2,c3=st.columns(3)
 c1.metric('Opciones evaluadas',len(result));c2.metric('Superan filtro orbital',len(valid));c3.metric('Menor coste filtrado',f"${valid['TOTAL $'].min():,.0f}" if len(valid) else '—')
 st.subheader('Alternativas orbitalmente compatibles')
 st.dataframe(valid[['Estado','Proveedor','Lanzador','Base','Campañas','TOTAL $','Coste/sat $','Estado comercial']],hide_index=True,use_container_width=True)
 if len(valid):st.bar_chart(valid.set_index('Lanzador')['TOTAL $'],horizontal=True)
 st.subheader('Opciones descartadas')
 st.dataframe(result[result['Estado'].str.contains('Incompatible')][['Proveedor','Lanzador','Base','Motivo']],hide_index=True,use_container_width=True)
with tab2:
 st.subheader('Desglose de todas las alternativas')
 st.dataframe(result,hide_index=True,use_container_width=True)
 st.download_button('Descargar resultados CSV',result.to_csv(index=False).encode('utf-8-sig'),'resultados_firesat.csv','text/csv')
 st.caption('Modelo: lanzamiento + dispensadores + integración + transporte + aduanas + OTV + reserva. El transporte se calcula por campaña y destino. Las aduanas son un supuesto fijo de $12.000/campaña.')
