from datetime import datetime
from dateutil.relativedelta import relativedelta
from plotly.express import line
from src.cache.manager import get_or_set_value_from_cache
from src.data.loader import load
from src.data.pypi_client import get_libs
import polars as pl
import streamlit as st

st.title("Growth")

categories_data = get_or_set_value_from_cache("projects", load)

category_options = ["All"] + [category["title"] for category in categories_data["categories"]]

filter_options = [
    "Last 6 Months",
    "Last Year",
    "All time"
]

libs_with_pypi_id = [lib for lib in categories_data["projects"]  if "pypi_id" in lib]


pypi_ids = [lib["pypi_id"] for lib in libs_with_pypi_id]

libs_names = [
    lib["name"] for lib in libs_with_pypi_id
] 

libs = get_or_set_value_from_cache("py_pi_libs", lambda: get_libs(pypi_ids))

slugs_to_titles = {
    category["category"]: category["title"]
    for category in categories_data["categories"]
}

projects_categories = {
    project["name"]: slugs_to_titles.get(project.get("category"))
    for project in libs_with_pypi_id
}

filters_cols = st.columns(2)

period_filter= filters_cols[0].selectbox(label="Period", options=filter_options)
category_filter = filters_cols[1].selectbox(label="Category", options=category_options)

if category_filter != "All":
    libs_names = [name for name in libs_names if projects_categories.get(name) == category_filter]


libs_selected = st.multiselect(label="Libraries",options=libs_names, max_selections=5)

libs_and_downloads = {}

pypi_to_name = {
    lib["pypi_id"]: lib["name"] for lib in libs_with_pypi_id
}

for pypi_id, lib_data in zip(pypi_ids, libs):
    
    name = pypi_to_name.get(pypi_id)
    
    if lib_data is None or name not in libs_selected:
        continue
    
    filtered_list = [item for item in lib_data["data"] if item["category"] == "without_mirrors"]
    
    libs_and_downloads[name] = filtered_list

if libs_selected:

    libs_stats_list = [
        {
        "name": lib,
        "date": item["date"],
        "downloads": item["downloads"]}
        for lib, items in libs_and_downloads.items()
        for item in items
    ]

    df_libs = pl.DataFrame(libs_stats_list)

    if period_filter == "Last 6 Months":
        df_libs = df_libs.filter(pl.col("date").cast(pl.Date) >= pl.lit(datetime.now() - relativedelta(months=6)))
    elif period_filter == "Last Year":
        df_libs = df_libs.filter(pl.col("date").cast(pl.Date) >= pl.lit(datetime.now() - relativedelta(months=12)))

    st.plotly_chart(line(x="date", y="downloads", color="name", data_frame=df_libs.to_pandas()))
else:
    st.info("Choose some libs")