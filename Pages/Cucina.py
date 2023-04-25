import streamlit as st
import pandas as pd
import numpy as np
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import schedule

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

#docs = db.collection("ordini_cameriere").stream()
#for doc in docs:
#    doc.reference.delete()
#db.collection("ordini_cameriere").document().delete() 

# Ogni giorno, ad una certa ora, svuota le collezioni ordini_cameriere ed ordini_cameriere_completati
def clearDatabase(db):
    docs = db.collection("ordini_cameriere").stream()
    for doc in docs:
        doc.reference.delete()
    db.collection("ordini_cameriere").document().delete()

    docs = db.collection("ordini_cameriere_completati").stream()
    for doc in docs:
        doc.reference.delete()
    db.collection("ordini_cameriere_completati").document().delete()

    print("Collections cleared")
    return

schedule.every().day.at("00:00").do(clearDatabase, db)

# Test
def test():
    print("Ha funzionato")
schedule.every().day.at("14:40").do(test)

# Inserimento dati
ordine1 = {
    "tavolo":1,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Antipasto fritti, carbonara", 
    "cameriere":1
}

ordine2 = {
    "tavolo":2,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Pasta scampi, vino rosso",
    "cameriere":2
}

ordine3 = {
    "tavolo":3,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Zuppa di cipolle, tiramisu",
    "cameriere":3
}

ordine4 = {
    "tavolo":4,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Arrosto, strudel",
    "cameriere":4
}

ordine5 = {
    "tavolo":5,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Amatriciana, cavoletti Bruxelles",
    "cameriere":5
}

ordine6 = {
    "tavolo":6,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Fagiolata, cocktail",
    "cameriere":6
}

ordine7 = {
    "tavolo":7,
    "timestamp": time.strftime("%H:%M:%S"),
    "comanda":"Pizza mortazza, coca cola",
    "cameriere":7
}

# Contatore ordini completati
ordini_completati = 0
if "ordini_completati" not in st.session_state:
    st.session_state.ordini_completati = ordini_completati

# Contatore ordini totali
ordini_totali = len(db.collection("ordini_cameriere").get())-1
if "ordini_totali" not in st.session_state:
    st.session_state.ordini_totali = ordini_totali

# Contatore ordini restanti
ordini_restanti = st.session_state.ordini_totali
if "ordini_restanti" not in st.session_state:
    st.session_state.ordini_restanti = ordini_restanti


if(st.session_state.ordini_totali == 0):
    db.collection("ordini_cameriere").document("ordine1").set(ordine1)
    db.collection("ordini_cameriere").document("ordine2").set(ordine2)
    db.collection("ordini_cameriere").document("ordine3").set(ordine3)
    db.collection("ordini_cameriere").document("ordine4").set(ordine4)
    db.collection("ordini_cameriere").document("ordine5").set(ordine5)
    db.collection("ordini_cameriere").document("ordine6").set(ordine6)
    db.collection("ordini_cameriere").document("ordine7").set(ordine7)


def display_orders():

    st.header("Lista Ordini")

    c1, c2, c3, c4, c5 = st.columns((1, 2, 1, 1, 1))
    with c1: st.subheader("Orario")
    with c2: st.subheader("Comanda")
    with c3: st.subheader("Tavolo")
    with c4: st.subheader("Cameriere")

    docs = db.collection("ordini_cameriere").stream()
    k = 0
    for doc in docs:
        k += 1
        doc_data = doc.to_dict()
        print(doc_data)
        c1, c2, c3, c4, c5 = st.columns((1, 2, 1, 1, 1))
        if("dummy" not in doc_data.keys()):
            with c1:
                st.write("Alle " + doc_data['timestamp'])
            with c2:
                st.write(doc_data['comanda'])
            with c3:
                st.write("Tavolo " + str(doc_data['tavolo']))
            with c4:
                st.write("Cameriere " + str(doc_data['cameriere']))
            with c5:
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
                st.session_state.ordini_restanti -= 1
                st.experimental_rerun()
                

display_orders()

# E' restato solo il dummy in "ordini_cameriere" => ordini terminati
if(st.session_state.ordini_completati == st.session_state.ordini_totali):
    st.session_state.ordini_totali = 0
    st.session_state.ordini_completati = 0
    st.session_state.ordini_restanti = 0
    st.success("Non ci sono altri ordini")

st.write(f"## Ordini Completati: {st.session_state.ordini_completati}/{st.session_state.ordini_totali}")



print("====== ORDINI_CAMERIERE ======")
docs = db.collection("ordini_cameriere").stream()
for doc in docs:
    doc_data = doc.to_dict()
    print(doc_data)

print("====== ORDINI_CAMERIERE_COMPLETATI ======")
docs = db.collection("ordini_cameriere_completati").stream()
for doc in docs:
    doc_data = doc.to_dict()
    print(doc_data)

print("\n\n\n")


#docs = db.collection("ordini_cameriere_completati").stream()
#for doc in docs:
#    doc.reference.delete()
#db.collection("ordini_cameriere_completati").document().delete()



  
