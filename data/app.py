import pandas as pd
from pathlib import Path

import dash
from dash import dcc, html
import plotly.express as px

DATA_PATH = Path("output/final_output.csv")

df = pd.read_csv(DATA_PATH)

df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

df = df.sort_values("Date")

df_daily = df.groupby("Date", as_index=False)["Sales"].sum()

PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")

fig = px.line(
    df_daily,
    x="Date",
    y="Sales",
    title="Pink Morsels Sales Over Time",
    labels={"Date": "Date", "Sales": "Total Sales"},
)

fig.add_vline(
    x=PRICE_INCREASE_DATE,
    line_width=2,
    line_dash="dash",
)

fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=1,
    xref="x",
    yref="paper",
    text="Price increase (15 Jan 2021)",
    showarrow=False,
)

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"maxWidth": "1100px", "margin": "0 auto", "padding": "20px"},
    children=[
        html.H1("Soul Foods – Pink Morsels Sales Visualiser"),
        html.P(
            "This chart shows total daily sales of Pink Morsels. "
            "The dashed line marks the price increase on 15 January 2021."
        ),
        dcc.Graph(figure=fig),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)
