import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import time
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

numero_tavoli = st.text_input("Numero di tavoli da inserire")
stato_tavolo = "Libero"
tavoli = st.button('Inserisci tavoli')

if numero_tavoli and tavoli:
    i = 0
    for i in range(1, int(numero_tavoli)+1):
        id_tav = str(i)
        doc_reff = db.collection(u"tavoli").document(id_tav)
        doc = doc_reff.get()
        doc_reff.set({
            'id': i,
            'stato': stato_tavolo
        })
    
    st.success('Inserimento avvenuto con successo')

else:
    st.warning('Inserisci numero di tavoli corretto ⚠️')