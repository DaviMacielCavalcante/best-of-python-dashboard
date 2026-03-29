from dotenv import load_dotenv
from src.cache.manager import get_or_set_value_from_cache, get_last_update
from src.utils.styles import apply_styles
from src.data.loader import load
import src.utils.logger
import streamlit as st

apply_styles()

st.set_page_config(page_title="Home", page_icon="🐍", layout="wide")

load_dotenv()
st.title("Welcome to the Best-of-python Visualizer!")
st.markdown("""
            
    ## About this project
    
    It aims to be a simple dashboard for people in the TI community to have a visual facilitator!
    
    ## About me
    
    I'm a undergraduate at CESUPA on Computer Science course. I love to solve problems, my family and my cats.    
    
    ## Feel free
    
    - To open issues to improve the dashboard
    - To contact me trough my email
""")

categories_data = get_or_set_value_from_cache("projects", load)

category_options = [category["title"] for category in categories_data["categories"]]

cols = st.columns(3)

lib_counts = len(categories_data["projects"])

cols[0].metric(label="Total Libraries".upper(), value=lib_counts)
cols[1].metric(label="Total Categories".upper(), value=len(category_options) - 1)
cols[2].metric(label="Last Updated".upper(), value=get_last_update("projects"))