from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide")


@st.cache_data(ttl=3600, max_entries=8)
def load_lottieurl(url: str):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        animation = response.json()
    except (requests.RequestException, ValueError):
        return None
    return animation if isinstance(animation, dict) and "layers" in animation else None


file_url = "https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json"
lottie_book = load_lottieurl(file_url)
if lottie_book is not None:
    st_lottie(lottie_book, speed=1, height=200, key="initial")
else:
    st.caption("Optional animation unavailable; the lesson works without it.")

st.title("Analyzing Your Goodreads Reading Habits")
st.subheader("A Web App by [Tyler Richards](http://www.tylerjrichards.com)")

"""
Hey there! Welcome to Tyler's Goodreads Analysis App. This app analyzes (and never stores!)
the books you've read using the popular service Goodreads, including looking at the distribution
of the age and length of books you've read. Give it a go by uploading your data below!
"""

goodreads_file = st.file_uploader("Please Import Your Goodreads Data")
try:
    books_df = pd.read_csv(goodreads_file if goodreads_file is not None else DATA_DIR / "goodreads_history.csv")
except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as error:
    st.error(f"Please upload a readable Goodreads CSV: {error}")
    st.stop()
required = {"Book Id", "Author", "Date Read", "Date Added", "Exclusive Shelf",
            "Number of Pages", "Original Publication Year", "My Rating", "Average Rating"}
if not required.issubset(books_df.columns) or books_df.empty:
    st.error("Upload a nonempty Goodreads export with columns: " + ", ".join(sorted(required)))
    st.stop()
for column in ["Number of Pages", "Original Publication Year", "My Rating", "Average Rating"]:
    books_df[column] = pd.to_numeric(books_df[column], errors="coerce")
for column in ["Date Read", "Date Added"]:
    books_df[column] = pd.to_datetime(books_df[column], errors="coerce", format="mixed")
if not (books_df["Exclusive Shelf"] == "read").any():
    st.info("This export has no finished books yet. Mark a book as read to analyze reading history.")
    st.stop()


def rounded_or_unknown(value):
    return round(value) if pd.notna(value) else "unknown"


# year finished
books_df["Year Finished"] = pd.to_datetime(books_df["Date Read"]).dt.year
books_per_year = books_df.groupby("Year Finished")["Book Id"].count().reset_index()
books_per_year.columns = ["Year Finished", "Count"]
fig_year_finished = px.bar(
    books_per_year, x="Year Finished", y="Count", title="Books Finished per Year"
)


# time difference
books_df["days_to_finish"] = (
    pd.to_datetime(books_df["Date Read"]) - pd.to_datetime(books_df["Date Added"])
).dt.days
books_finished_filtered = books_df[
    (books_df["Exclusive Shelf"] == "read") & (books_df["days_to_finish"] >= 0)
]
fig_days_finished = px.histogram(
    books_finished_filtered,
    x="days_to_finish",
    title="Time Between Date Added And Date Finished",
    labels={"days_to_finish": "days"},
)

# num pages
fig_num_pages = px.histogram(
    books_df, x="Number of Pages", title="Book Length Histogram"
)

# publication year
books_publication_year = (
    books_df.groupby("Original Publication Year")["Book Id"].count().reset_index()
)
books_publication_year.columns = ["Year Published", "Count"]

fig_year_published = px.bar(
    books_publication_year, x="Year Published", y="Count", title="Book Age Plot"
)
fig_year_published.update_xaxes(range=[1850, pd.Timestamp.today().year])

# rating
books_rated = books_df[books_df["My Rating"].fillna(0) != 0]
fig_my_rating = px.histogram(books_rated, x="My Rating", title="User Rating")

fig_avg_rating = px.histogram(
    books_rated, x="Average Rating", title="Average Goodreads Rating"
)
avg_difference = np.round(
    np.mean(books_rated["My Rating"] - books_rated["Average Rating"]), 2
)
if avg_difference >= 0:
    sign = "higher"
else:
    sign = "lower"

if goodreads_file is None:
    st.subheader("Tyler's Analysis Results:")
else:
    st.subheader("Your Analysis Results:")
books_finished = books_df[books_df["Exclusive Shelf"] == "read"]
u_books = len(books_finished["Book Id"].unique())
u_authors = len(books_finished["Author"].unique())
mode_author = next(iter(books_finished["Author"].mode()), "unknown")
st.write(
    f"It looks like you have finished {u_books} books with a total of {u_authors} unique authors. Your most read author is {mode_author}!"
)
st.write(
    f"Your app results can be found below, we have analyzed everything from your book length distribution to how you rate books. Take a look around, all the graphs are interactive!"
)

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2 = st.columns(2)

with row1_col1:
    mode_year_finished = rounded_or_unknown(next(iter(books_df["Year Finished"].mode()), float("nan")))
    st.plotly_chart(fig_year_finished)
    st.write(f"You finished the most books in {mode_year_finished}. Awesome job!")
with row1_col2:
    st.plotly_chart(fig_days_finished)
    mean_days_to_finish = rounded_or_unknown(books_finished_filtered["days_to_finish"].mean())
    st.write(
        f"It took you an average of {mean_days_to_finish} days between when the book was added to Goodreads and when you finished the book. This is not a perfect metric, as you may have added this book to a to-read list!"
    )
with row2_col1:
    st.plotly_chart(fig_num_pages)
    avg_pages = rounded_or_unknown(books_df["Number of Pages"].mean())
    st.write(
        f"Your books are an average of {avg_pages} pages long, check out the distribution above!"
    )
with row2_col2:
    st.plotly_chart(fig_year_published)
    st.write(
        "This chart starts at 1850 and ends in the current year; zoom to explore other periods."
    )
with row3_col1:
    st.plotly_chart(fig_my_rating)
    avg_my_rating = round(books_rated["My Rating"].mean(), 2)
    st.write(f"You rate books an average of {avg_my_rating} stars on Goodreads.")
with row3_col2:
    st.plotly_chart(fig_avg_rating)
    if pd.notna(avg_difference):
        st.write(f"You rate books {sign} than the average Goodreads user by {abs(avg_difference)}!")
    else:
        st.info("No comparable ratings in this export.")
