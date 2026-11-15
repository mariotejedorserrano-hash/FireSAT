"""Modelo económico derivado de FireSAT_simulador_sin_widgets.ipynb.
Los precios y corredores orbitales son supuestos de planificación, no cotizaciones.
"""
from pathlib import Path
import pandas as pd

SHIPPING={
'Spain':{'USA':32000,'French Guiana':23000,'New Zealand':50000,'India':42000,'Japan':48000,'Norway':26000,'United Kingdom':22000,'Brazil':46000,'China':65000,'Other':45000},
'France':{'USA':30000,'French Guiana':18000,'New Zealand':48000,'India':40000,'Japan':46000,'Norway':24000,'United Kingdom':20000,'Brazil':45000,'China':65000,'Other':45000},
'USA':{'USA':12000,'French Guiana':35000,'New Zealand':47000,'India':44000,'Japan':42000,'Norway':39000,'United Kingdom':35000,'Brazil':38000,'China':65000,'Other':45000},
'Other':{'USA':40000,'French Guiana':40000,'New Zealand':45000,'India':45000,'Japan':45000,'Norway':40000,'United Kingdom':38000,'Brazil':42000,'China':65000,'Other':45000}}
UNCONFIRMED=('DEVELOPMENT','UNCONFIRMED','SITE TBD','EXPORT RESTRICTIONS','PROGRAM STATUS','SITE / MANIFEST','RFQ')
NUMERIC=['Site latitude °','Min inclination °','Max inclination °','Min altitude km','Max altitude km','Rideshare minimum USD','Included kg','Extra USD/kg','Dedicated USD']

def load_launchers():
    df=pd.read_csv(Path(__file__).with_name('launchers.csv'))
    for col in NUMERIC: df[col]=pd.to_numeric(df[col],errors='coerce')
    return df

def calculate(df,n=6,unit='8U',mass=16.,planes=2,alt=525,inc=97.5,inc_tol=1.,alt_tol=50,strategy='Una campaña por plano',origin='Spain',deployer=35000,campaign_fee=75000,otv_fee=800000,reserve_pct=10):
    if not (1<=planes<=n): raise ValueError('Los planos deben estar entre 1 y el número de satélites')
    if mass<=0: raise ValueError('La masa debe ser positiva')
    family='SSO' if 96<=inc<=102 else 'Polar' if inc>=85 else 'Mid-LEO'
    campaigns=1 if strategy=='Todos juntos + OTV' else planes
    allocation=[n//campaigns+int(i<n%campaigns) for i in range(campaigns)]
    records=[]
    for _,r in df.iterrows():
        issues=[]
        if pd.isna(r['Min inclination °']) or pd.isna(r['Max inclination °']) or not (r['Min inclination °']-inc_tol<=inc<=r['Max inclination °']+inc_tol):issues.append('Inclinación')
        if pd.isna(r['Min altitude km']) or pd.isna(r['Max altitude km']) or not (r['Min altitude km']-alt_tol<=alt<=r['Max altitude km']+alt_tol):issues.append('Altitud')
        if family not in str(r['Orbit families']).split(','):issues.append('Familia orbital')
        speculative=any(x in str(r['Commercial status']).upper() for x in UNCONFIRMED)
        status='🔴 Incompatible' if issues else '🟡 Por confirmar' if speculative else '🟢 Filtro superado'
        try:
            launch=sum(float(r['Dedicated USD']) if strategy=='Dedicado por plano' else float(r['Rideshare minimum USD'])+max(0,c*mass-float(r['Included kg']))*float(r['Extra USD/kg']) for c in allocation)
        except (TypeError,ValueError):launch=float('nan')
        disp=n*deployer;integ=campaigns*campaign_fee
        shipping=campaigns*SHIPPING.get(origin,SHIPPING['Other']).get(str(r['Country']),45000)
        customs=campaigns*12000
        otv=(planes-1)*otv_fee if campaigns==1 else 0
        subtotal=launch+disp+integ+shipping+customs+otv
        reserve=subtotal*reserve_pct/100
        records.append({'Estado':status,'Proveedor':r['Provider'],'Lanzador':r['Launcher'],'Base':r['Spaceport'],'Campañas':campaigns,'Sat/campaña':'+'.join(map(str,allocation)),'Lanzamiento $':launch,'Dispensadores $':disp,'Integración $':integ,'Transporte $':shipping,'Aduanas $':customs,'OTV $':otv,'Reserva $':reserve,'TOTAL $':subtotal+reserve,'Coste/sat $':(subtotal+reserve)/n,'Motivo':', '.join(issues),'Estado comercial':r['Commercial status'],'Familia calculada':family})
    return pd.DataFrame(records).sort_values('TOTAL $').reset_index(drop=True)
