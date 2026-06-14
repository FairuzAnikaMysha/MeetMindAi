import pandas as pd
import plotly.express as px

data = pd.DataFrame({
    "Category":["Summary","Tasks","Owners"],
    "Count":[1,10,4]
})

fig = px.bar(
    data,
    x="Category",
    y="Count"
)

st.plotly_chart(fig)
