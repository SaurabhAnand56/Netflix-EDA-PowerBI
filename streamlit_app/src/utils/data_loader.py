"""
data_loader.py — Load, clean, and cache the Netflix titles CSV.
"""

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    """
    Load netflix_titles.csv, clean it, and return a tidy DataFrame.

    Cleaning steps
    --------------
    1. Strip whitespace from all string columns
    2. Parse date_added → datetime; extract year_added / month_added
    3. Extract numeric duration_min for Movies
    4. Extract numeric seasons for TV Shows
    5. Fill missing director / cast / country with 'Unknown'
    6. Drop rows with missing rating
    7. Drop duplicates
    """
    df = pd.read_csv(path)

    # 1. Whitespace
    str_cols = df.select_dtypes("object").columns
    df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())

    # 2. Dates
    df["date_added"]  = pd.to_datetime(df["date_added"], errors="coerce")
    df["year_added"]  = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month

    # 3. Movie duration (minutes)
    movies_mask = df["type"] == "Movie"
    df.loc[movies_mask, "duration_min"] = (
        df.loc[movies_mask, "duration"]
        .str.replace(" min", "", regex=False)
        .astype(float)
    )

    # 4. TV Show seasons
    shows_mask = df["type"] == "TV Show"
    df.loc[shows_mask, "seasons"] = (
        df.loc[shows_mask, "duration"]
        .str.extract(r"(\d+)")[0]
        .astype(float)
    )

    # 5. Fill missing
    for col in ("director", "cast", "country"):
        df[col].fillna("Unknown", inplace=True)

    # 6. Drop missing rating
    df.dropna(subset=["rating"], inplace=True)

    # 7. Duplicates
    df.drop_duplicates(inplace=True)

    return df


def apply_filters(
    df: pd.DataFrame,
    content_type: list,
    ratings: list,
    year_range: tuple,
    countries: list,
) -> pd.DataFrame:
    """Return a filtered view of the DataFrame based on sidebar selections."""
    if content_type:
        df = df[df["type"].isin(content_type)]
    if ratings:
        df = df[df["rating"].isin(ratings)]
    df = df[df["release_year"].between(*year_range)]
    if countries:
        df = df[df["country"].isin(countries)]
    return df
