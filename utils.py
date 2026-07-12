import streamlit as st

def success_message(msg):
    st.success(msg)

def error_message(msg):
    st.error(msg)

def info_message(msg):
    st.info(msg)