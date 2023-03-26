import streamlit as st
import pandas as pd
import numpy as np
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# TO-DO:
# Gestire eliminazione ordine completato da "ordini_cameriere"
# Gestire spostamente ordine completato in "ordini_cameriere_completati"

# Accedo al database di Ciro
if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

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

if(len(db.collection("ordini_cameriere").get()) != 4): # solo documento dummy -> runnato solo la prima volta
    db.collection("ordini_cameriere").document("ordine1").set(ordine1)
    db.collection("ordini_cameriere").document("ordine2").set(ordine2)
    db.collection("ordini_cameriere").document("ordine3").set(ordine3)

# Contatore ordini completati e numero ordini totali
ordini_completati = 0
if "ordini_completati" not in st.session_state:
    st.session_state.ordini_completati = ordini_completati

ordini_totali = len(db.collection("ordini_cameriere").get())

# Funzione per mostrare gli ordini
def display_orders():
    st.header("Lista degli ordini")
    docs = db.collection("ordini_cameriere").stream()
    for doc in docs:
        doc_data = doc.to_dict()
        print(doc_data)
        if("dummy" not in doc_data.keys()):
            header = doc_data['timestamp'] + "\n" + doc_data["nome"] + "\n" + "Tavolo: " + str(doc_data["tavolo"])
            with st.expander(header):
                button = st.button("Completato! [" + str(doc_data["id"]) + "]")
                if button:
                    st.success("Ordine completato!")
                    # ordine eliminato dal database e spostato in apposita collezione per ordini completati  --TO-DO
                    st.session_state.ordini_completati += 1
    
display_orders()

# Mostra numero di ordini completati su totali
st.write(f"## Numero di Ordini Completati: {st.session_state.ordini_completati}/{ordini_totali - 1}")

""" --DEBUG
docs = db.collection("ordini_cameriere_completati").stream()
for doc in docs:
    doc.reference.delete()
db.collection("ordini_cameriere_completati").document().delete()

for collection_ref in db.collections():
    st.write(f"Collection: {collection_ref.id}")
    # Get all documents in the collection
    docs = collection_ref.stream()
    # Loop through each document and print its attributes
    for doc in docs:
        st.write(f"Document: {doc.id}")
        doc_data = doc.to_dict()
        for key, value in doc_data.items():
            st.write(f"{key}: {value}")  """
    
