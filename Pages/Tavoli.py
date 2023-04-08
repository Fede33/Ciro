from bokeh.models.widgets import Div
import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import time
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from functions import redirect

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



home = st.button("Home 🏠")

if home:
    js = "window.open('http://localhost:8501/Sala')"  # New tab or window
    js = "window.location.href = 'http://localhost:8501/Sala'"  # Current tab
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

