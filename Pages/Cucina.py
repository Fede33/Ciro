import streamlit as st
import pandas as pd
import numpy as np
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# TO-DO:
# Gestire eliminazione dei record alle 00.00 di ogni giorno sia in 'ordini_cameriere' che 'ordini_cameriere_completati'
# Gestire il refresh della pagina periodico per non "perdersi" nuovi ordini provenienti da Sala.py

# Accedo al database di Ciro
if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Imposto il layout di pagina
st.set_page_config(page_title='Ciro', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')

# Creo una nuova collezione 'ordini_cameriere'
if "ordini_cameriere" not in db.collections():
    db.collection("ordini_cameriere").document("dummy").set({"dummy":"dummy"})

# Creo una nuova collezione 'ordini_cameriere_completati'
if "ordini_cameriere_completati" not in db.collections():
    db.collection("ordini_cameriere_completati").document("dummy").set({"dummy":"dummy"})

# Definisco due classi per i due tipi di ordine  --UNUSED
class OrdineCameriere:
    def __init__(self, id, timestamp, nome, tavolo) -> None:
        self.id = id
        self.timestamp = timestamp
        self.nome = nome
        self.tavolo = tavolo

ordine1 = {
    "id":0, # normalmente sarebbe ordini_cameriere.length - 1 (fornito dalla sala)
    "timestamp": time.strftime("%H:%M:%S"),
    "nome":"Antipasto fritti, carbonara",
    "tavolo":1 # fornito dalla sala
}

ordine2 = {
    "id":1, # normalmente sarebbe ordini_cameriere.length - 1 (fornito dalla sala)
    "timestamp": time.strftime("%H:%M:%S"),
    "nome":"Pasta scampi, vino rosso",
    "tavolo":2 # fornito dalla sala
}

ordine3 = {
    "id":2, # normalmente sarebbe ordini_cameriere.length - 1 (fornito dalla sala)
    "timestamp": time.strftime("%H:%M:%S"),
    "nome":"Zuppa di cipolle, tiramisu",
    "tavolo":3 # fornito dalla sala
}

""" # --DEBUG - riempio la collezione 'ordini_cameriere'
if(len(db.collection("ordini_cameriere").get()) != 4): # solo documento dummy -> runnato solo la prima volta
    db.collection("ordini_cameriere").document("ordine1").set(ordine1)
    db.collection("ordini_cameriere").document("ordine2").set(ordine2)
    db.collection("ordini_cameriere").document("ordine3").set(ordine3)
"""
st.markdown("##")
st.markdown("""---""")

# Contatore ordini completati e numero ordini totali
ordini_completati = 0
if "ordini_completati" not in st.session_state:
    st.session_state.ordini_completati = ordini_completati

ordini_totali = len(db.collection("ordini_cameriere").get())

# Costruisco la UI
st.header("Lista degli ordini")
docs = db.collection("ordini_cameriere").stream()
k = 0
for doc in docs:
    k += 1
    doc_data = doc.to_dict()
    print(doc_data)
    c1, c2, c3, c4 = st.columns((1, 2, 1, 1))

    if("dummy" not in doc_data.keys()):
        with c1:
            st.write(doc_data['timestamp'])
        with c2:
            st.write(doc_data['nome'])
        with c3:
            st.write("Tavolo " + str(doc_data['tavolo']))
        with c4:
            button = st.button("Completato!", key=k)
        if button:
                
            # Ordine eliminato dal database
            doc.reference.delete()

            # Aggiungo elemento agli ordini completati
            collection_ref = db.collection("ordini_cameriere_completati")
            docName = "ordine" + str(st.session_state.ordini_completati)
            doc_data['ora_completato'] = time.strftime("%H:%M:%S")
            collection_ref.document(docName).set(doc_data)

            # Aggiorno UI
            st.success("Ordine completato!")
            st.session_state.ordini_completati += 1
            st.experimental_rerun()


# Se un solo elemento in 'ordini_completati' => solo il dummy
if(ordini_totali == 1):
    st.session_state.ordini_completati = 0
    st.success("Tutti gli ordini sono stati completati!")
else:
    st.write(f"## Numero di Ordini Completati: {st.session_state.ordini_completati}/{ordini_totali - 1 + st.session_state.ordini_completati}")

st.markdown("""---""")
st.markdown("##")

#--DEBUG Scommentare per ricondursi al caso in cui non ci sono ancora ordini completati
#--DEBUG Scommentando sia questo che il codice precedente si ci riconduce al caso base con 3 ordini
#--DEBUG Dopo run con commenti scommentati, ricommentarli
"""
docs = db.collection("ordini_cameriere_completati").stream()
for doc in docs:
    doc.reference.delete()
db.collection("ordini_cameriere_completati").document().delete()
"""
# --DEBUG Display di tutti gli elementi nel database, poco carino ma funziona
for collection_ref in db.collections():
    st.write(f"Collection: {collection_ref.id}")
    # Get all documents in the collection
    docs = collection_ref.stream()
    # Loop through each document and print its attributes
    for doc in docs:
        st.write(f"Document: {doc.id}")
        doc_data = doc.to_dict()
        for key, value in doc_data.items():
            st.write(f"{key}: {value}")
    