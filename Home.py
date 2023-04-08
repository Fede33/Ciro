import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


if not firebase_admin._apps:
    cred = credentials.Certificate('ciro-1375d-firebase.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.set_page_config(page_title='Ciro', layout = 'wide', page_icon = "", initial_sidebar_state = 'auto')
hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if True:
    def add_bg_from_url():
            st.markdown(
                f"""
                <style>
                .stApp {{
                    background-image: url("https://media-assets.vanityfair.it/photos/614c92be36677578deda08d7/16:9/pass/alimentazione-ver.jpg");
                    background-attachment: fixed;
                    background-size: cover
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

    add_bg_from_url()



st.markdown('# <span style="color: #983C8E;">Ciro</span>', unsafe_allow_html=True)

