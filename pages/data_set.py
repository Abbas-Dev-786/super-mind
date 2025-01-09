import os
import streamlit as st
import pandas as pd

st.title("Sample Dataset")

file_path = "./../dataset.csv" 

if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.write("CSV file loaded successfully:")
else:
    st.write(f"File not found: {file_path}")