from pathlib import Path
import pandas as pd

import dash
from dash import dcc, html, Input, Output
import plotly.express as px

BASE_DIR = Path(__file__).resolve().parent  # Gets the 'data' directory
DATA_PATH = BASE_DIR / "output" / "final_output.csv"
PRICE_INCREASE_DATE = pd.to_datetime("2021-01-15")

app = dash.Dash(__name__)
# Load once at startup
df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

# Normalize region text to make filtering reliable (e.g., "North", "north ", etc.)
df["Region"] = df["Region"].astype(str).str.strip().str.lower()

# Dash app
app = dash.Dash(__name__)

# ---------- Styling (simple but nice) ----------
PAGE_STYLE = {
    "minHeight": "100vh",
    "padding": "28px",
    "background": "linear-gradient(135deg, #f7f7ff 0%, #eef6ff 100%)",
    "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif",
}

CARD_STYLE = {
    "maxWidth": "1100px",
    "margin": "0 auto",
    "background": "white",
    "borderRadius": "18px",
    "padding": "22px 22px",
    "boxShadow": "0 10px 30px rgba(0,0,0,0.08)",
}

HEADER_STYLE = {
    "margin": "0 0 6px 0",
    "fontSize": "30px",
    "letterSpacing": "-0.2px",
}

SUBTITLE_STYLE = {"margin": "0 0 18px 0", "color": "#334155", "lineHeight": "1.5"}

CONTROL_ROW_STYLE = {
    "display": "flex",
    "gap": "18px",
    "alignItems": "center",
    "flexWrap": "wrap",
    "padding": "14px 16px",
    "borderRadius": "14px",
    "background": "#f8fafc",
    "border": "1px solid #e2e8f0",
    "marginBottom": "14px",
}

LABEL_STYLE = {"fontWeight": 600, "color": "#0f172a"}

RADIO_CONTAINER_STYLE = {"display": "flex", "gap": "12px", "flexWrap": "wrap"}

GRAPH_STYLE = {
    "borderRadius": "14px",
    "border": "1px solid #e2e8f0",
    "overflow": "hidden",
}

FOOTER_STYLE = {"marginTop": "14px", "color": "#64748b", "fontSize": "13px"}

# ---------- Layout ----------
app.layout = html.Div(
    style=PAGE_STYLE,
    children=[
        html.Div(
            style=CARD_STYLE,
            children=[
                html.H1("Soul Foods – Pink Morsels Sales Visualiser", style=HEADER_STYLE),
                html.P(
                    "Use the region filter to explore Pink Morsels sales trends. "
                    "The dashed line marks the price increase on 15 January 2021.",
                    style=SUBTITLE_STYLE,
                ),
                html.Div(
                    style=CONTROL_ROW_STYLE,
                    children=[
                        html.Div("Filter by region:", style=LABEL_STYLE),
                        dcc.RadioItems(
                            id="region-radio",
                            options=[
                                {"label": "All", "value": "all"},
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                            ],
                            value="all",
                            inline=True,
                            style=RADIO_CONTAINER_STYLE,
                        ),
                    ],
                ),
                html.Div(
                    style=GRAPH_STYLE,
                    children=[
                        dcc.Graph(id="sales-line-chart", config={"displayModeBar": False}),
                    ],
                ),
                html.Div(
                    style=FOOTER_STYLE,
                    children="Tip: If your dataset contains more region names than these four, only matching rows will appear when filtered.",
                ),
            ],
        )
    ],
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
)
def update_chart(region_value: str):
    if region_value == "all":
        filtered = df.copy()
        title_region = "All regions"
    else:
        filtered = df[df["Region"] == region_value].copy()
        title_region = region_value.title()


    filtered = filtered.sort_values("Date")
    daily = filtered.groupby("Date", as_index=False)["Sales"].sum()

    fig = px.line(
        daily,
        x="Date",
        y="Sales",
        title=f"Pink Morsels Daily Sales – {title_region}",
        labels={"Date": "Date", "Sales": "Total Sales"},
    )

    # Price increase marker
    fig.add_vline(x=PRICE_INCREASE_DATE, line_width=2, line_dash="dash")
    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase (15 Jan 2021)",
        showarrow=False,
        xanchor="left",
    )

    fig.update_layout(
        margin=dict(l=30, r=20, t=55, b=40),
        title=dict(x=0.03),
        hovermode="x unified",
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
