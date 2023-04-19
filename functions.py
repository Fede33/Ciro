import streamlit as st


#per creare griglia pagina Sala
def make_grid(cols,rows):
    grid = [0]*cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid


def get_id(id_tav):
    global tempo
    tempo = id_tav


def return_id():
    return tempo