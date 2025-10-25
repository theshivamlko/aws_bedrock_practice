import streamlit as st
import  main as main

st.set_page_config(page_title="HR Policy App", layout="wide")

new_title="<h1>HR Policy Document Query Application</h1>"
st.markdown(new_title,unsafe_allow_html=True)

if 'vector_index' not in st.session_state:
    with st.spinner("Waiting...."):
        st.session_state.vector_index=main.hr_index_and_store()

input_text=st.text_input("Input your query here:",label_visibility="collapsed")
go_button=st.button("Learn GenAi",type="primary")

if go_button:
    with st.spinner("Getting your response..."):
        response=main.hr_rag_query(st.session_state.vector_index,input_text)
        print("spinner ===> Done")

        if not response:
            st.write("Not found")
        else:
            st.write(response)