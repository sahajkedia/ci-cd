import numpy as np
import pandas as pd
import streamlit as st

st.title("Sample Streamlit App")


data = pd.DataFrame(np.random.randn(10, 3), columns=["A", "B", "C"])

st.write("## Sample Data")
st.dataframe(data)

st.write("## Line Chart")
st.line_chart(data)
