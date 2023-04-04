import streamlit as st
import pandas as pd
import numpy as np
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Accedo al database di Ciro
if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Layout di pagina
st.set_page_config(layout="wide")
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

'''
if(len(db.collection("ordini_cameriere").get()) != 4): # solo documento dummy -> runnato solo la prima volta
    db.collection("ordini_cameriere").document("ordine1").set(ordine1)
    db.collection("ordini_cameriere").document("ordine2").set(ordine2)
    db.collection("ordini_cameriere").document("ordine3").set(ordine3)
'''

# Contatore ordini completati e numero ordini totali
ordini_completati = 0
if "ordini_completati" not in st.session_state:
    st.session_state.ordini_completati = ordini_completati

ordini_totali = len(db.collection("ordini_cameriere").get())

st.markdown("#")
st.markdown("""---""")

def display_orders():
    st.header("Lista Ordini")
    c1, c2, c3, c4 = st.columns((1, 2, 1, 1))

    docs = db.collection("ordini_cameriere").stream()
    k = 0
    for doc in docs:
        k += 1
        doc_data = doc.to_dict()
        print(doc_data)
        if("dummy" not in doc_data.keys()):
            header = doc_data['timestamp'] + "\n" + doc_data["nome"] + "\n" + "Tavolo: " + str(doc_data["tavolo"])
            with c1:
                st.write("Alle " + doc_data['timestamp'])
            with c2:
                st.write(doc_data['nome'])
            with c3:
                st.write("Tavolo " + str(doc_data['tavolo']))
            with c4:
                button = st.button("Completato!", key=k)
            if button:

                # Remove doc from collection "ordini_cameriere"
                doc.reference.delete()

                # Add doc to collection "ordini_cameriere_completati"
                collection_ref = db.collection("ordini_cameriere_completati")
                docName = "ordine" + str(st.session_state.ordini_completati + 1) + " - " + doc_data['timestamp']
                collection_ref.document(docName).set(doc_data)

                st.success("Ordine completato!")
                st.session_state.ordini_completati += 1
                st.experimental_rerun()
                

display_orders()

# E' restato solo il dummy in "ordini_cameriere" => ordini terminati
if(ordini_totali == 1):
    st.success("Non ci sono ordini")
else:
    st.write(f"## Ordini Completati: {st.session_state.ordini_completati}/{ordini_totali + st.session_state.ordini_completati - 1}")

st.markdown("#")
st.markdown("""---""")

'''
docs = db.collection("ordini_cameriere_completati").stream()
for doc in docs:
    doc.reference.delete()
db.collection("ordini_cameriere_completati").document().delete()
'''

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
  
