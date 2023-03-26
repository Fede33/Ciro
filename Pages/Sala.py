import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
import numpy as np
import cv2
from  PIL import Image, ImageEnhance
import time
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()


table_options = ["Tavolo 1", "Tavolo 2", "Tavolo 3"]
table_choice = st.sidebar.selectbox("Scegli il tavolo:", table_options)

st.markdown("[![Foo](http://www.google.com.au/images/nav_logo7.png)](http://localhost:8501/Amministrazione#amministrazione)")

image = Image.open('tavolo.jpg')

if table_choice== "Tavolo 1":
    pass