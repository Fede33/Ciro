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

doc_ref = db.collection("tavoli")
docs = doc_ref.stream()
tav = []

#creazione dizionari aggiunti poi a lista tav
for doc in docs:
	prodotti_dict = {"Numero" : doc.to_dict()['id'],"Stato": doc.to_dict()['stato']} 
	tav.append(prodotti_dict)


num_tavoli = len(tav)
#visualizzazione griglia sala
rows = 5
cols = int(num_tavoli/5)+1
grid = make_grid(cols,rows)

sorted(tav, key=lambda x: x['Numero'])

var = 0
for i in range(0, cols):
    for l in range(0, rows):
        if var<len(tav):
            if tav[var]['Stato']== "Occupato":
                if grid[i][l].button(f"Tavolo {tav[var]['Numero']} 👨‍👩‍👧‍👦", key=f"{tav[var]['Numero']}"):
                    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
                    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
                    html = '<img src onerror="{}">'.format(js)
                    div = Div(text=html)
                    st.bokeh_chart(div)


            if tav[var]['Stato'] == "Libero":
                if grid[i][l].button(f"Tavolo {tav[var]['Numero']} 🍽", key=f"{tav[var]['Numero']}"):
                    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
                    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
                    html = '<img src onerror="{}">'.format(js)
                    div = Div(text=html)
                    st.bokeh_chart(div)

            if tav[var]['Stato'] == "Prenotato":
                if grid[i][l].button(f"Tavolo {tav[var]['Numero']} 🕓", key=f"{tav[var]['Numero']}"):
                    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
                    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
                    html = '<img src onerror="{}">'.format(js)
                    div = Div(text=html)
                    st.bokeh_chart(div)

        else:
            pass
        var = var+1


"""

if but1:
    n_tav = "1"
    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

if but2:
    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

if but3:
    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

if but4:

    js = "window.open('http://localhost:8501/Tavoli')"  # New tab or window
    js = "window.location.href = 'http://localhost:8501/Tavoli'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

"""