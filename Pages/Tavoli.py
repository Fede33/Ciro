from bokeh.models.widgets import Div
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import time
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from functions import return_id


if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title='Ciro', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')

st.markdown('# <span style="color: #983C8E;">Ordinazione tavoli</span>', unsafe_allow_html=True)

doc_ref = db.collection(f"menu")
docs = doc_ref.stream()



for doc in docs:
    menu_dict = {"Nome"}
doc_ref3 = db.collection(f"ordini_correnti")
docs3 = doc_ref3.stream()
azione_da_compiere = ""

#controlla se il tavolo ha già effettuato un ordine
for doc in docs3:
    if return_id() == str(doc.to_dict()['tavolo']):
        azione_da_compiere = "Visualizzazione"
    else:
        pass




#se tavolo ha già effettuato ordine
if azione_da_compiere == "Visualizzazione":
    pass





#tavolo ancora non ha effettuato nessun ordine
else:
    pass



doc_ref = db.collection(f"menu")
docs = doc_ref.stream()

#liste per suddividere piatti a seconda della portata
antipasti = []
primi = []
secondi = []
contorni = []
dolci = []
non_disponibili = ""

for doc in docs:
    if doc.to_dict()['stato'] == "Disponibile":
        if doc.to_dict()['portata'] == "Antipasto":
            menu_dict = {"Piatto" : doc.to_dict()['nome'],"Prezzo": doc.to_dict()['prezzo']}
            antipasti.append(menu_dict)

        if doc.to_dict()['portata'] == "Primo":
            menu_dict = {"Piatto" : doc.to_dict()['nome'],"Prezzo": doc.to_dict()['prezzo']}
            primi.append(menu_dict)

        if doc.to_dict()['portata'] == "Secondo":
            menu_dict = {"Piatto" : doc.to_dict()['nome'],"Prezzo": doc.to_dict()['prezzo']}
            secondi.append(menu_dict)

        if doc.to_dict()['portata'] == "Contorno":
            menu_dict = {"Piatto" : doc.to_dict()['nome'],"Prezzo": doc.to_dict()['prezzo']}
            contorni.append(menu_dict)

        if doc.to_dict()['portata'] == "Dolce":
            menu_dict = {"Piatto" : doc.to_dict()['nome'],"Prezzo": doc.to_dict()['prezzo']}
            dolci.append(menu_dict)
    else:
        if len(non_disponibili) > 2:
            non_disponibili = non_disponibili + ", " + str(doc.to_dict()['nome'])
        else:
            non_disponibili = str(doc.to_dict()['nome'])



#visualizzazione pagina suddivisa per portata
#--------------------------------------ANTIPASTO-------------------------------------
col1, col2 = st.columns(2)
with col1:
    st.header("Antipasti")
    if antipasti != []:
        for a in range(0, int(len(antipasti)/2)+1):
            st.number_input(f"{antipasti[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=antipasti[a]["Piatto"])


with col2:
    if antipasti != [] and int(len(antipasti)/2)+1<len(antipasti):
        for a in range(int(len(antipasti)/2)+1, len(antipasti)):
            st.number_input(f"{antipasti[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=antipasti[a]["Piatto"])


#--------------------------------------PRIMO------------------------------------
col3, col4 = st.columns(2)
with col3:
    st.header("Primi")
    if primi != []:
        for a in range(0, int(len(primi)/2)+1):
            st.number_input(f"{primi[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=primi[a]["Piatto"])

with col4:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    if primi != [] and int(len(primi)/2)+1<len(primi):
        for a in range(int(len(primi)/2)+1, len(primi)):
            st.number_input(f"{primi[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=primi[a]["Piatto"])


#--------------------------------------SECONDO-------------------------------------
col5, col6 = st.columns(2)
with col5:
    st.header("Secondi")
    if secondi != []:
        for a in range(0, int(len(secondi)/2)+1):
            st.number_input(f"{secondi[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=secondi[a]["Piatto"])


with col6:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    if secondi != [] and int(len(secondi)/2)+1<len(secondi):
        for a in range(int(len(secondi)/2)+1, len(secondi)):
            st.number_input(f"{secondi[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=secondi[a]["Piatto"])



#--------------------------------------CONTORNO-------------------------------------
col7, col8 = st.columns(2)
with col7:
    st.header("Contorni")
    if contorni != []:
        for a in range(0, int(len(contorni)/2)+1):
            st.number_input(f"{contorni[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=contorni[a]["Piatto"])


with col8:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    if contorni != [] and int(len(contorni)/2)+1<len(contorni):
        for a in range(int(len(contorni)/2)+1, len(contorni)):
            st.number_input(f"{contorni[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=contorni[a]["Piatto"])




#--------------------------------------DOLCE-------------------------------------
col9, col10 = st.columns(2)
with col9:
    st.header("Dolci")
    if dolci != []:
        for a in range(0, int(len(dolci)/2)+1):
            st.number_input(f"{dolci[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=dolci[a]["Piatto"])


with col10:
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    if dolci != [] and int(len(dolci)/2)+1<len(dolci):
        for a in range(int(len(dolci)/2)+1, len(dolci)):
            st.number_input(f"{dolci[a]['Piatto']}: ", min_value=0, step=1, 
            format=None, key=dolci[a]["Piatto"])


for b in range(0, len(primi)):
    if st.session_state[primi[b]["Piatto"]] > 0:
        st.write("ciao")
        prod_id = return_id()



st.write("\n")
st.write("\n")
st.write("\n")
st.write(f"Non sono attualmente diponibili i seguenti piatti: {non_disponibili}")



conferma = st.button("Conferma ordine")
if conferma:
    pass

st.write("\n")
st.write("\n")
home = st.button("Home 🏠")

if home:
    js = "window.open('http://localhost:8501/Sala')"  # New tab or window
    js = "window.location.href = 'http://localhost:8501/Sala'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

