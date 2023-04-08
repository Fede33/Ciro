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

st.set_page_config(page_title='Ciro', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')


numero_tavoli = st.text_input("Numero di tavoli da inserire")
stato_tavolo = "Libero"
tavoli = st.button('Inserisci tavoli')

doc_ref = db.collection("tavoli")
docs = doc_ref.stream()
tav = []

for doc in docs:
    tav.append(doc.to_dict()['id'])


print("eccoci qui")
print(tav)


if numero_tavoli and tavoli:
    i = 0
    if tav!=[]:
        for l in range(0, len(tav)):
            print(l)
            db.collection(u'tavoli').document(str(tav[l])).delete()

    for i in range(1, int(numero_tavoli)+1):
        id_tav = str(i)
        doc_reff = db.collection(u"tavoli").document(id_tav)
        doc = doc_reff.get()
        doc_reff.set({
            'id': i,
            'stato': stato_tavolo
        })
    
    st.success('Inserimento avvenuto con successo')

if numero_tavoli == "" and tavoli == "":
    st.warning('Inserisci numero di tavoli corretto ⚠️')

st.write("\n") #solo per una migliore interfaccia
st.write("\n")
st.write("\n")

st.write("Cambia stato del tavolo")
docs = db.collection(u'tavoli').stream()
tavoli = []
for doc in docs:
    tavoli.append(doc.to_dict()['id'])

col5, col6 = st.columns(2)
with col5:
    choice1 = st.selectbox("Scegli il tavolo", tavoli)
    butt = st.button("Aggiorna tavolo")

with col6:
    stato = ["Occupato", "Libero", "Prenotato"]
    choice2 = st.selectbox("Scegli lo stato", stato)

if choice1 and choice2!=" " and choice2 and butt:
    db.collection(u"tavoli").document(str(choice1)).update({
        'stato': choice2,
                        })

    st.success('Modifica effettuata con successo')

if choice1 == "" or choice2 =="":
    st.warning("Seleziona tavolo e stato ⚠️")

