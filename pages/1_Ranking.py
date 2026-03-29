from plotly.express import bar
from src.cache.manager import get_or_set_value_from_cache, get_last_update
from src.data.loader import load
from src.data.github_client import get_repos
from src.data.pypi_client import get_libs
import polars as pl
import streamlit as st

categories_data = get_or_set_value_from_cache("projects", load)

category_options = ["All"] + [category["title"] for category in categories_data["categories"]]

sort_options = [
    "Stars",
    "Downloads",
    "Forks"
]

filters_cols = st.columns(2)

category_filter= filters_cols[0].selectbox(label="Category", options=category_options)
sort_by_filter = filters_cols[1].selectbox(label="Sort By", options=sort_options)

cols = st.columns(3)

lib_counts = len(categories_data["projects"])

projects_with_github = [
    project for project in categories_data["projects"] 
    if "github_id" in project
]

libs_with_pypi_id = [lib for lib in categories_data["projects"]  if "pypi_id" in lib]

github_ids = [project["github_id"] for project in projects_with_github]

pypi_ids = [lib["pypi_id"] for lib in libs_with_pypi_id]

libs = get_or_set_value_from_cache("py_pi_libs", lambda: get_libs(pypi_ids))

repos = get_or_set_value_from_cache("github_projects", lambda: get_repos(github_ids))

slugs_to_titles = {
    category["category"]: category["title"]
    for category in categories_data["categories"]
}

projects_categories = {
    project["name"]: slugs_to_titles.get(project.get("category"))
    for project in projects_with_github
}

libs_to_repos = {
    lib["pypi_id"]: lib["name"]
    for lib in libs_with_pypi_id
}

libs_and_downloads = {}

for pypi_id, lib_data in zip(pypi_ids, libs):
    
    if lib_data is None:
        continue
    
    filtered_list = [item for item in lib_data["data"] if item["category"] == "without_mirrors"]
    
    most_recent_info = max(filtered_list, key=lambda x: x["date"]) 
    
    libs_and_downloads[libs_to_repos.get(pypi_id)] = most_recent_info["downloads"]


repo_stats_list = [
    {
    "name": repo["name"],
    "stars": repo["stargazers_count"],
    "forks": repo["forks_count"],
    "downloads": libs_and_downloads.get(repo["name"]),
    "category": projects_categories.get(repo["name"])
    }
    for repo in repos if repo is not None
]

df_repos = pl.DataFrame(repo_stats_list)

sort_column = {
    "Stars": "stars",
    "Forks": "forks",
    "Downloads": "downloads"
}[sort_by_filter]

if sort_column == "Downloads":
    df_repos_chart = df_repos.filter(pl.col("downloads").is_not_null()).sort(sort_column)
    df_repos_table = df_repos.filter(pl.col("downloads").is_not_null()).sort(sort_column, descending=True)
else:
    df_repos_chart = df_repos.sort(sort_column)
    df_repos_table = df_repos.sort(sort_column, descending=True)

if category_filter != "All":
    df_repos_chart = df_repos_chart.filter(pl.col("category") == category_filter)
    df_repos_table = df_repos_table.filter(pl.col("category") == category_filter)
    cols[0].metric(label="Total Libraries".upper(), value=df_repos_table.shape[0])
    cols[1].metric(label="Total Categories".upper(), value=df_repos_table["category"].n_unique())
    cols[2].metric(label="Last Updated".upper(), value=get_last_update("projects"))
    
else:
    cols[0].metric(label="Total Libraries".upper(), value=len(categories_data["projects"]))
    cols[1].metric(label="Total Categories".upper(), value=len(categories_data["categories"]) - 1)
    cols[2].metric(label="Last Updated".upper(), value=get_last_update("projects"))

st.plotly_chart(bar(y="name", x=sort_column, orientation="h", data_frame=df_repos_chart.tail(20).to_pandas()))

st.dataframe(df_repos_table.head(20).to_pandas(), hide_index=True)