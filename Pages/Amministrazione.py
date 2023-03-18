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

st.markdown('# <span style="color: #983C8E;">Amministrazione</span>', unsafe_allow_html=True)

choice = st.selectbox('Scegli che azione eseguire', ['','Inserimento', 'Aggiornamento', 'Eliminazione'])


if choice == '':
    st.info('Puoi scegliere se inserire, aggiungere o eliminare un piatto dal menù', icon="ℹ️")

if choice == 'Inserimento':
    # --- Inserimento campi del prodotto ---
    prod_nome = st.text_input('Nome del piatto')
    prod_disp = st.number_input('Disponibilità', step=1, min_value=1, value=1)
    prod_prezzo = st.number_input('Prezzo del piatto', min_value=0.00)
    prod_stato = st.selectbox('Quale è lo stato del piatto?',('Disponibile', 'NON Disponibile'))
    
    bottone_inser = st.button('Inserisci')
    if bottone_inser:
        if prod_nome=='':
            st.warning('⚠️ Inserisci un nome valido')
        elif prod_disp=='':
            st.warning('⚠️ Inserisci una disponibilità valida')
        elif prod_prezzo=='':
            st.warning('⚠️ Inserisci un prezzo valido')
        elif prod_stato=='':
            st.warning('⚠️ Inserisci uno stato valido')
        else:
            prod_id = prod_nome + '-codice'
            # --- Inserimento di nuovi campi all'interno della collection partecipanti ---
            db.collection(u"menu").document(prod_id).set({   
                            'nome': str(prod_nome),
                            'prezzo': float(prod_prezzo),
                            'disponibilità': int(prod_disp),
                            'stato': str(prod_stato)
                            })
    
            st.success('Inserimento avvenuto con successo')
            
if choice == 'Aggiornamento':
    # --- Inserimento campi del prodotto ---
    prod_nome = st.text_input('Nome del piatto')
    prod_disp = st.number_input('Disponibilità', step=1, min_value=1, value=1)
    prod_prezzo = st.number_input('Prezzo del piatto', min_value=0.00)
    prod_stato = st.selectbox('Quale è lo stato del piatto?',('Disponibile', 'NON Disponibile'))
    
    bottone_mod = st.button('Aggiorna')
    if bottone_mod:
        if prod_nome=='':
            st.warning('⚠️ Inserisci un nome valido')
        elif prod_disp!='':
            prod_id = prod_nome + '-codice'
            db.collection(u"menu").document(prod_id).set({   
                        'disponibilità': prod_disp
                        })
        elif prod_prezzo!='':
            prod_id = prod_nome + '-codice'
            db.collection(u"menu").document(prod_id).update({   
                        'prezzo': prod_prezzo
                        })
        elif prod_stato!='':
            prod_id = prod_nome + '-codice'
            db.collection(u"menu").document(prod_id).update({   
                        'stato': prod_stato
                        })
    
        st.success('Modifica effettuata con successo')
        
if choice == 'Eliminazione':
    # --- Inserimento campi del prodotto ---
    prod_nome = st.text_input('Nome del piatto')
    bottone_del = st.button('Elimina')
    if bottone_del:
        if prod_nome=='':
            st.warning('⚠️ Inserisci un nome valido')
        else:
            prod_id = prod_nome + '-codice'
            db.collection(u"menu").document(prod_id).delete()

            st.success('Eliminazione avvenuta con successo')
            
###############################################################################################

doc_ref = db.collection("menu")

docs = doc_ref.stream()

# --- Costruzione di una tabella dei dati del database
piatti = []
for doc in docs:
    st.write(doc)
    menu_dict = {'Nome': doc.to_dict()['nome'], 'Prezzo': doc.to_dict()['prezzo'], 'disp': doc.to_dict()['disponibilità'], 'Stato': doc.to_dict()['stato']}
    piatti.append(menu_dict)

if piatti!=[]:
    data = pd.DataFrame(piatti)
    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_selection(selection_mode='multiple', use_checkbox=True)
    gd.configure_grid_options(enableCellTextSelection=True)
    gd.configure_grid_options(ensureDomOrder=True)
    gd.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=6)

    gridOptions = gd.build()

    table = AgGrid(data, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, enable_enterprise_modules=False, height=270, fit_columns_on_grid_load=True)

    selected = table['selected_rows']
    
    col1, col2 = st.columns(2)
    elimina_selezionati = col1.button('Elimina selezionati')
    if elimina_selezionati:
        if selected == []:
            st.warning('⚠️ Seleziona almeno un piatto')
        else:
            for dictionary in selected:
                nome_d = dictionary['Nome'] + '-codice'
                db.collection(u'menu').document(nome_d).delete()
            st.success(f'Eliminazione avvenuta')
            time.sleep(1)
            st.experimental_rerun()
            
    oscura_selezionati = col2.button('Oscura selezionati')


else:
    st.warning('Nessun piatto registrato')
