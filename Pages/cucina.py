import streamlit as st

# TO-DO
# Mettere contatori e variabili varie nel session state
# Capire come mai non mostra gli ordini!!

# Lista dove inserire gli ordini
orders = ["[1] Panino, pizza, coca cola", 
          "[2] Pasta scampi, vino rosso",
          "[3] Bistecca, birra"]

# Funzione per mostrare gli ordini
def display_orders():
    st.write("## Lista degli Ordini:")
    if not st.session_state.lista_ordini:
        st.write("Ancora nessun ordine!")
    else:
        for order in st.session_state.lista_ordini:
            st.write(order, "\n")
            
# Funzione per marcare gli ordini come completati
def complete_order(order_number):
    if order_number > 0 and order_number <= len(orders):
        del st.session_state.lista_ordini[order_number-1]

# Aggiungere le variabili che saranno modificate nel session state
if "lista_ordini" not in st.session_state:
    st.session_state["lista_ordini"] = orders

if "tot_ordini" not in st.session_state:
    st.session_state["tot_ordini"] = len(orders)

# Corpo principale applicazione
def app():
    st.title("CIRO")
    
    # Una sidebar con un selector per le due funzionalità offerte
    menu_options = ["Visualizza Ordini", "Marca come Completato"]
    menu_choice = st.sidebar.selectbox("Scegli un'opzione:", menu_options)
    
    # Mostra ordini
    if menu_choice == "Visualizza Ordini":
        display_orders()
    
    # Marca ordine come completato
    elif menu_choice == "Marca come Completato":
        st.header("Marca come Completato")
        order_number = st.number_input("Inserisci l'ID dell'ordine completato:", min_value=1, max_value=len(orders), step=1)
        if st.button("Completato!"):
            complete_order(order_number)
            st.success("Ordine marcato come completato")
    
    # Mostra il numero di ordini compeltati su totali
    st.write(f"## Numero di Ordini Completati: {st.session_state.tot_ordini - len(st.session_state.lista_ordini)}/{st.session_state.tot_ordini}")

if __name__ == "__main__":
    app()
