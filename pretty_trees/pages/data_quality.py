from pathlib import Path

import pandas as pd
import streamlit as st

st.title("SF Trees Data Quality App")
st.write(
    "Edit privately maintained trees with known coordinates, then download the full "
    "dataset. All other rows are preserved. The bundled CSV is never overwritten."
)

trees_df = pd.read_csv(Path(__file__).resolve().parents[1] / "trees.csv")
editable = (trees_df["legal_status"] == "Private") & trees_df[
    ["longitude", "latitude"]
].notna().all(axis=1)

# Keep the original index: edits must return to the same rows in the full dataset.
edited_df = st.data_editor(
    trees_df.loc[editable].copy(),
    key="tree_edits",
    disabled=["tree_id"],
    num_rows="fixed",
)
updated_trees = trees_df.copy()
updated_trees.loc[edited_df.index, edited_df.columns] = edited_df
st.download_button(
    "Download complete edited CSV",
    updated_trees.to_csv(index=False).encode("utf-8"),
    file_name="trees_edited.csv",
    mime="text/csv",
)
st.caption(f"Export includes all {len(updated_trees):,} rows, including missing coordinates.")
