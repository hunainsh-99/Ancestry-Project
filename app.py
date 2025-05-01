import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import nnls
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ancestry Composition", layout="wide")
st.title("🧬 Ancestry Composition")

@st.cache_data
def load_data():
    raw = pd.read_csv("data/reference.csv", dtype=str)
    if raw.columns[0].strip().lower() != "population":
        raw = pd.read_csv("data/reference.csv", dtype=str, header=None)
        header = raw.iloc[0].tolist()
        raw = raw.iloc[1:]
        raw.columns = header

    raw = raw.dropna(how="all")
    raw = raw[raw.iloc[:,0].str.strip().str.lower() != "population"]

    pop_col = raw.columns[0]
    df = raw.rename(columns={pop_col: "population"}).set_index("population")
    df = df.apply(pd.to_numeric, errors="coerce")

    df = df.dropna(how="all")
    if df.isna().any().any():
        raise ValueError("Reference panel still contains non-numeric entries.")

    ev = pd.read_csv("data/eigenvalues.csv", header=None).iloc[0].to_numpy(dtype=float)
    if ev.size != df.shape[1]:
        raise ValueError(f"Expected {df.shape[1]} eigenvalues, got {ev.size}.")
    if (ev <= 0).any() or np.isnan(ev).any():
        raise ValueError("Eigenvalues must be positive numbers.")

    w = np.sqrt(ev)
    X_ref = df.values * w[np.newaxis, :]
    return df.index.tolist(), X_ref, w

try:
    pops, X_ref, pc_w = load_data()
except Exception as e:
    st.error(f"Data load error: {e}")
    st.stop()

n = X_ref.shape[1]

vector_input = st.text_area(
    "Paste your vector (label,PC1,…,PC25):",
    value="",
    height=100,
    placeholder="e.g. me,0.073985,-0.001016,…,-0.006227"
)

if st.button("Compute Composition"):
    parts = [p.strip() for p in vector_input.split(",")]
    if len(parts) != n + 1:
        st.error(f"Expected {n+1} values (1 label + {n} numbers), got {len(parts)}.")
    else:
        label, *coords = parts
        try:
            vec = np.array(coords, dtype=float)
        except:
            st.error("All coordinates must be numeric.")
            st.stop()
        if np.isnan(vec).any() or np.isinf(vec).any():
            st.error("Your input vector contains NaN or Inf values.")
            st.stop()

        y = vec * pc_w
        coefs, _ = nnls(X_ref.T, y)
        comp = pd.Series(coefs, index=pops)
        comp = comp.div(comp.sum()).mul(100).sort_values(ascending=False).head(8)

        st.subheader("Top 8 DNA Composition (%)")
        st.dataframe(comp.to_frame("percentage"))

        fig, ax = plt.subplots(figsize=(8, 4))
        comp.plot.bar(ax=ax)
        ax.set_ylabel("Percentage (%)")
        ax.set_xticklabels(comp.index, rotation=45, ha="right")
        st.pyplot(fig)
