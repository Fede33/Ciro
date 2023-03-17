import streamlit as st

# TO-DO
# Vedere come sfruttare gli indici e i numeri dei tavoli -> indice != numero tavolo

# Lista dove inserire gli ordini
orders = ["Panino, pizza, coca cola [T1]", 
          "Pasta scampi, vino rosso [T2]",
          "Bistecca, birra [T3]"]

# Creo copia statica degli ordini [NON USATA]
orders_copy = orders.copy

# Funzione per mostrare gli ordini
def display_orders():
    st.write("## Lista degli Ordini:")
    if not st.session_state.lista_ordini:
        st.write("Ancora nessun ordine!")
    else:
        i = 1
        for order in st.session_state.lista_ordini:
            st.write(i, ". ", order, "\n")
            i += 1
            
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
        order_number = st.number_input("Inserisci l'ID dell'ordine completato:", min_value=1, max_value=len(st.session_state.lista_ordini), step=1)
        if st.button("Completato!"):

            #Caso: non ci sono più ordini
            if(st.session_state.tot_ordini - len(st.session_state.lista_ordini) == st.session_state.tot_ordini):
                st.error("Non ci sono ancora ordini!")

            #Caso: ci sono ordini da soddisfare
            else: 
                complete_order(order_number)
                st.success("Ordine marcato come completato")
                st.experimental_rerun()
    
    # Mostra il numero di ordini compeltati su totali
    st.write(f"## Numero di Ordini Completati: {st.session_state.tot_ordini - len(st.session_state.lista_ordini)}/{st.session_state.tot_ordini}")

if __name__ == "__main__":
    app()
