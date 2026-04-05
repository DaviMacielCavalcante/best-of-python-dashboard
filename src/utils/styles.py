import streamlit as st

def apply_styles():
    # NOTE: These selectors use Streamlit's internal data-testid attributes,
    # which are not part of the public API and may break on Streamlit upgrades.
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

        * {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background: #202020;
            padding: 1.3rem;
            border-radius: 0.375rem;
        }
        
        [data-testid="stSidebarCollapseButton"] span {
            display: none !important;
        }
        
        [data-testid="stSidebar"] * {
            font-size: 1rem !important;
        }

        [data-testid="stMetricLabel"] p {
            font-size: 1rem;
            letter-spacing: 0.08em;
            color: #98CBFF;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] p {
            font-size: 1.75rem !important;
            letter-spacing: -0.02em;
            color: #ffffff;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #1B1B1C;
        }

        /* Selectbox container */
        [data-testid="stSelectbox"] > div,
        [data-testid="stMultiSelect"] > div {
            background-color: #202020 !important;
            border-radius: 0.375rem !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* Label acima do selectbox */
        [data-testid="stSelectbox"] label,
        [data-testid="stMultiSelect"] label {
            font-size: 0.6875rem !important;
            letter-spacing: 0.08em;
            color: #98CBFF !important;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }

        /* Texto dentro dos selectboxes */
        [data-testid="stSelectbox"] div,
        [data-testid="stMultiSelect"] div {
            color: #ffffff !important;
            font-size: 0.875rem !important;
        }

        /* Tags do multiselect */
        [data-testid="stMultiSelect"] span[data-baseweb="tag"],
        [data-baseweb="tag"] {
            background-color: #3776AB !important;
            color: #ffffff !important;
        }

        /* Plotly chart background */
        .js-plotly-plot .plotly {
            background: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)