from plotly.express import bar
from src.cache.manager import get_or_set_value_from_cache
from src.data.loader import load
from src.data.github_client import get_repos
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

cols[0].metric(label="Total Libraries".upper(), value=lib_counts)
cols[1].metric(label="Total Categories".upper(), value=len(category_options) - 1)
cols[2].metric(label="Last Updated".upper(), value="N/A")

projects_with_github = [
    project for project in categories_data["projects"] 
    if "github_id" in project
]

github_ids = [project["github_id"] for project in projects_with_github]

repos = get_or_set_value_from_cache("github_projects", lambda: get_repos(github_ids))

slugs_to_titles = {
    category["category"]: category["title"]
    for category in categories_data["categories"]
}

projects_categories = {
    project["name"]: slugs_to_titles.get(project.get("category"))
    for project in projects_with_github
}

repo_stats_list = [
    {
    "name": repo["name"],
    "stars": repo["stargazers_count"],
    "forks": repo["forks_count"],
    "category": projects_categories.get(repo["name"])
    }
    for repo in repos if repo is not None
]

df_repos = pl.DataFrame(repo_stats_list)


if sort_by_filter == "Downloads":
    st.info("Downloads ainda não disponível!")
else:
    sort_column = {
        "Stars": "stars",
        "Forks": "forks"
    }[sort_by_filter]

    df_repos_chart = df_repos.sort(sort_column)
    df_repos_table = df_repos.sort(sort_column, descending=True)

    if category_filter != "All":
        df_repos_chart = df_repos_chart.filter(pl.col("category") == category_filter)
        df_repos_table = df_repos_table.filter(pl.col("category") == category_filter)

    st.plotly_chart(bar(y=df_repos_chart["name"], x=sort_column, orientation="h", data_frame=df_repos_chart.head(20)))

    st.dataframe(df_repos_table.head(20))