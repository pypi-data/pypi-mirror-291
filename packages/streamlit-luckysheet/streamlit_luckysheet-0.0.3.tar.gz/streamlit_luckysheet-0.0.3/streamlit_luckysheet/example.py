import streamlit as st
from streamlit_luckysheet import streamlit_luckysheet
import base64
import os

st.set_page_config(layout="wide")
st.subheader("Component with constant args")

name = "streamlit_luckysheet"
key = "excelsheet"
height = 1000
excel_path = r".\streamlit_luckysheet\excel\Employee Sample Data.xlsx"

def excel_to_file(path):
    try:
        if not os.path.exists(path):
            return ""

        with open(path, 'rb') as file:
            file_data = file.read() 
            if file_data:
                return base64.b64encode(file_data).decode('utf-8')
            else:
                st.warning("File is empty or could not be read.")
                return ""
    except Exception as e:
        st.warning(f"An error occurred while processing the file: {e}")
        return ""

encodedFile = excel_to_file(excel_path)

resut = streamlit_luckysheet(name=name, height=height, encodedFile=encodedFile, key=key, default=0)
