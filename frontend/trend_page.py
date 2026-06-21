import streamlit as st
import requests
import pandas as pd

st.title("Health Trend Analysis")

tests = [
    "LDL Cholesterol",
    "Cholesterol / HDL",
    "LDL / HDL"
]

for test in tests:

    st.subheader(test)

    data = requests.get(
        f"http://127.0.0.1:8000/trend-history/2/{test}"
    ).json()

    if len(data) == 0:
        st.warning(f"No data for {test}")
        continue

    df = pd.DataFrame(data)

    df["report"] = [
        f"Report {i}"
        for i in range(1, len(df)+1)
    ]

    st.line_chart(
        df.set_index("report")["value"]
    )