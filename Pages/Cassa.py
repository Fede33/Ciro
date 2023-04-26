import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np
import time
from bokeh.models.widgets import Div
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title='Ciro', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')

st.markdown('# <span style="color: #983C8E;">Cassa</span>', unsafe_allow_html=True)


docs = db.collection(u'tavoli').stream()
tavoli = ['']
numeri = []
for doc in docs:
    x = int(doc.id)
    numeri.append(x)
    numeri.sort()
for i in numeri:
    i = str(i)
    tavoli.append(i)
selezione_tavolo = st.selectbox("Seleziona il tavolo per il conto: ", tavoli)



if selezione_tavolo != '':
    st.header('Tavolo ' + selezione_tavolo)
    
    doc_ref = db.collection("ordini_cameriere")
    docs = doc_ref.stream()

    lista = []
    for doc in docs:
        doc_data = doc.to_dict()
        if("dummy" not in doc_data.keys()):
            if str(doc_data['tavolo']) == selezione_tavolo:
                lista.append(doc_data['comanda'])


    doc_ref = db.collection(f"menu")
    docs = doc_ref.stream()
    cassa = []
    cassa_dict = {}
    lista_comanda = []
    for i in lista:
        comanda = i
        lista_comanda = comanda.split(",")
    st.write('--------------------------------')
    for j in lista_comanda:
        
        for doc in docs:
            if doc.to_dict()['nome'] == j:
                prezzo = doc.to_dict()['prezzo']
                st.write(prezzo)
        cassa_dict = {"Piatto": j}
        cassa.append(cassa_dict)
        
    if cassa!=[]:
        data = pd.DataFrame(cassa)
        gd = GridOptionsBuilder.from_dataframe(data)
        gd.configure_selection(selection_mode='multiple', use_checkbox=True)
        gd.configure_grid_options(enableCellTextSelection=True)
        gd.configure_grid_options(ensureDomOrder=True)
        gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=6)

        gridOptions = gd.build()

        table = AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, enable_enterprise_modules=False, height=270, fit_columns_on_grid_load=True)
    else:
        st.warning("Non ci sono ordini per questo tavolo")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Il conto totale è: ")

    with col2:
        st.subheader("")
    st.write('--------------------------------') 
     
    coll1, coll2 = st.columns(2)

    with coll1:
        st.button("Paga Selezionati")

    with coll2:
        st.button("Paga Tutto")  
st.sidebar.title("Funzioni Utili")
with st.sidebar.expander("Pagamento alla Romana"):
    #st.write("funzione del pagamento alla romana")
    numero_clienti=st.number_input("inserisci il numero dei clienti!", step=1)
    if st.button("Invio", key="romana"):
        st.write("Il costo per ogni persona è: ")
with st.sidebar.expander("Applica Sconto"):
    #st.write("funzione dello sconto")
    age = st.slider('Inserisci la percentuale di sconto', 0, 100, 0, step=5)
    if st.button("Invio", key="sconto"):
        st.write("Il totale con lo sconto applicato è di: ")
