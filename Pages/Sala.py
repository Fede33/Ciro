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



col1, col2, col3, col4 = st.columns(4)

with col1:
    but1 = st.button("Tavolo 1 🍽")
    st.write(" ")
    but5 = st.button("Tavolo 5 🍽")
    st.write(" ")
    but9 = st.button("Tavolo 9 🍽")
    st.write(" ")
    but13 = st.button("Tavolo 13 🍽")
    st.write(" ")
    but17 = st.button("Tavolo 17 🍽")
    st.write(" ")

with col2:
    but2 = st.button("Tavolo 2 🍽")
    st.write(" ")
    but6 = st.button("Tavolo 6 🍽")
    st.write(" ")
    but10 = st.button("Tavolo 10 🍽")
    st.write(" ")
    but14 = st.button("Tavolo 14 🍽")
    st.write(" ")
    but18 = st.button("Tavolo 18 🍽")
    st.write(" ")

with col3:
    but3 = st.button("Tavolo 3 🍽")
    st.write(" ")
    but7 = st.button("Tavolo 7 🍽")
    st.write(" ")
    but11 = st.button("Tavolo 11 🍽")
    st.write(" ")
    but15 = st.button("Tavolo 15 🍽")
    st.write(" ")
    but19 = st.button("Tavolo 19 🍽")
    st.write(" ")

with col4:
    but4 = st.button("Tavolo 4 🍽")
    st.write(" ")
    but8 = st.button("Tavolo 8 🍽")
    st.write(" ")
    but12 = st.button("Tavolo 12 🍽")
    st.write(" ")
    but16 = st.button("Tavolo 16 🍽")
    st.write(" ")
    but20 = st.button("Tavolo 20 🍽")
    st.write(" ")

st.write("Cambia stato del tavolo")
docs = db.collection(u'tavoli').stream
tavoli = [" "]
for doc in docs:
    tavoli.append(doc.to_dict()['numero'])

col5, col6 = st.columns(2)
with col5:
    choice1 = st.selectbox("Scegli il tavolo", tavoli)

with col6:
    stato = [" ", "Occupato", "Libero", "Prenotato"]
    choice2 = st.selectbox("Scegli lo stato", stato)

if choice1 and choice2:
    docs = db.collection(u'tavoli').stream
else:
    st.warning("Seleziona tavolo e stato ⚠️")



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