from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# ── App ────────────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[
    dbc.themes.DARKLY,
    "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap"
])

# ── Estilos globales ───────────────────────────────────────────────────────────
COLORS = {
    "bg":        "#0a0c10",
    "surface":   "#111318",
    "border":    "#1e2230",
    "accent":    "#f0a500",
    "accent2":   "#e05c2a",
    "green":     "#22c55e",
    "red":       "#ef4444",
    "muted":     "#6b7280",
    "text":      "#e2e8f0",
}

FONT_DISPLAY = "Barlow Condensed, sans-serif"
FONT_MONO    = "JetBrains Mono, monospace"

CARD_STYLE = {
    "background":    COLORS["surface"],
    "border":        f"1px solid {COLORS['border']}",
    "borderRadius":  "4px",
    "padding":       "20px 24px",
    "height":        "100%",
}

TICKER_MAP = {
    "CL=F":  "WTI Crude",
    "BZ=F":  "Brent Crude",
    "SLB":   "SLB Corp",
    "NG=F":  "Natural Gas",
    "XOM":   "ExxonMobil",
}

# ── Helper: precio actual ──────────────────────────────────────────────────────
def get_price(ticker: str):
    try:
        t   = yf.Ticker(ticker)
        hist = t.history(period="2d")
        if hist.empty:
            return None, None
        price   = hist["Close"].iloc[-1]
        prev    = hist["Close"].iloc[-2] if len(hist) > 1 else price
        change  = ((price - prev) / prev) * 100
        return round(price, 2), round(change, 2)
    except Exception:
        return None, None

# ── Helper: gráfico histórico ──────────────────────────────────────────────────
def build_chart(ticker: str, period: str):
    try:
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            return go.Figure()

        color_line  = COLORS["accent"]
        color_fill  = "rgba(240,165,0,0.08)"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"],
            mode="lines",
            line=dict(color=color_line, width=2),
            fill="tozeroy",
            fillcolor=color_fill,
            name="Precio",
            hovertemplate="<b>%{x|%d %b %Y}</b><br>USD %{y:.2f}<extra></extra>"
        ))

        # Media móvil 20 días
        if len(hist) >= 20:
            ma = hist["Close"].rolling(20).mean()
            fig.add_trace(go.Scatter(
                x=hist.index, y=ma,
                mode="lines",
                line=dict(color=COLORS["accent2"], width=1.5, dash="dot"),
                name="MA 20",
                hovertemplate="MA20: %{y:.2f}<extra></extra>"
            ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family=FONT_MONO, color=COLORS["muted"], size=11),
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color=COLORS["text"], size=11)
            ),
            xaxis=dict(
                showgrid=True, gridcolor=COLORS["border"],
                showline=False, zeroline=False,
                tickfont=dict(family=FONT_MONO, size=10, color=COLORS["muted"])
            ),
            yaxis=dict(
                showgrid=True, gridcolor=COLORS["border"],
                showline=False, zeroline=False,
                tickprefix="$",
                tickfont=dict(family=FONT_MONO, size=10, color=COLORS["muted"])
            ),
            hovermode="x unified",
            hoverlabel=dict(
                bgcolor=COLORS["surface"],
                bordercolor=COLORS["border"],
                font=dict(family=FONT_MONO, color=COLORS["text"])
            )
        )
        return fig
    except Exception:
        return go.Figure()

# ── Helper: card de precio ─────────────────────────────────────────────────────
def price_card(title: str, price_id: str, change_id: str, spark_id):
    return dbc.Col(html.Div([
        html.P(title, style={
            "fontFamily": FONT_MONO,
            "fontSize":   "11px",
            "color":      COLORS["muted"],
            "letterSpacing": "0.12em",
            "textTransform": "uppercase",
            "marginBottom": "8px",
        }),
        html.Div(id=price_id, style={
            "fontFamily": FONT_DISPLAY,
            "fontSize":   "36px",
            "fontWeight": "700",
            "color":      COLORS["text"],
            "lineHeight": "1",
            "marginBottom": "6px",
        }),
        html.Div(id=change_id, style={
            "fontFamily": FONT_MONO,
            "fontSize":   "12px",
            "color":      "black",  # Se actualizará dinámicamente
        }),
        dcc.Graph(
            id=spark_id,
            config={"displayModeBar": False},
            style={"height": "60px", "margin": "8px -8px -12px -8px"}
        )
    ], style=CARD_STYLE), width=12, md=6, xl=True, className="mb-3")

# ── Layout ─────────────────────────────────────────────────────────────────────
app.layout = html.Div(style={"background": COLORS["bg"], "minHeight": "100vh"}, children=[

    # Topbar
    html.Div(style={
        "borderBottom": f"1px solid {COLORS['border']}",
        "padding": "0 32px",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "space-between",
        "height": "60px",
        "background": COLORS["surface"],
    }, children=[
        html.Div([
            html.Span("⬡ ", style={"color": COLORS["accent"], "fontSize": "18px"}),
            html.Span("OIL & GAS", style={
                "fontFamily": FONT_DISPLAY,
                "fontSize":   "20px",
                "fontWeight": "700",
                "letterSpacing": "0.15em",
                "color":      COLORS["text"],
            }),
            html.Span(" MARKET INTELLIGENCE", style={
                "fontFamily": FONT_DISPLAY,
                "fontSize":   "20px",
                "fontWeight": "300",
                "letterSpacing": "0.1em",
                "color":      COLORS["muted"],
            }),
        ]),
        html.Div(id="last-update", style={
            "fontFamily": FONT_MONO,
            "fontSize":   "11px",
            "color":      COLORS["muted"],
        }),
    ]),

    # Contenido principal
    html.Div(style={"padding": "28px 32px"}, children=[

        # Cards de precios
        dbc.Row([
            price_card("WTI Crude Oil",     "price-wti",  "change-wti", "spark-wti"),
            price_card("Brent Crude",       "price-brent","change-brent", "spark-brent"),
            price_card("Natural Gas",       "price-ng",   "change-ng", "spark-ng"),
            price_card("SLB Corp",          "price-slb",  "change-slb", "spark-slb"),
            price_card("ExxonMobil",        "price-xom",  "change-xom", "spark-xom"),
        ], className="mb-4"),

        # Gráfico histórico
        html.Div(style=CARD_STYLE | {"padding": "24px"}, children=[

            # Header del gráfico
            html.Div(style={
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "marginBottom": "20px",
                "flexWrap": "wrap",
                "gap": "12px",
            }, children=[
                html.Div([
                    html.P("HISTORICAL PRICE", style={
                        "fontFamily": FONT_MONO,
                        "fontSize":   "11px",
                        "color":      COLORS["muted"],
                        "letterSpacing": "0.12em",
                        "margin":     "0 0 4px 0",
                    }),
                    html.Div(id="chart-title", style={
                        "fontFamily": FONT_DISPLAY,
                        "fontSize":   "24px",
                        "fontWeight": "600",
                        "color":      COLORS["text"],
                    }),
                ]),
                html.Div(style={"display": "flex", "gap": "12px", "flexWrap": "wrap"}, children=[
                    dcc.Dropdown(
                        id="ticker-select",
                        options=[{"label": v, "value": k} for k, v in TICKER_MAP.items()],
                        value="CL=F",
                        clearable=False,
                        style={
                            "width":      "180px",
                            "fontFamily": FONT_MONO,
                            "fontSize":   "12px",
                            "background": COLORS["bg"],
                            "color":      "Black",
                            "border":     f"1px solid {COLORS['border']}",
                        }
                    ),
                    dcc.Dropdown(
                        id="period-select",
                        options=[
                            {"label": "1 Semana",  "value": "5d"},
                            {"label": "1 Mes",     "value": "1mo"},
                            {"label": "3 Meses",   "value": "3mo"},
                            {"label": "6 Meses",   "value": "6mo"},
                            {"label": "1 Año",     "value": "1y"},
                            {"label": "2 Años",    "value": "2y"},
                        ],
                        value="3mo",
                        clearable=False,
                        style={
                            "width":      "140px",
                            "fontFamily": FONT_MONO,
                            "fontSize":   "12px",
                            "background": COLORS["bg"],
                            "color":      "black",
                            "border":     f"1px solid {COLORS['border']}",
                        }
                    ),
                ]),
            ]),

            dcc.Graph(
                id="main-chart",
                config={"displayModeBar": False},
                style={"height": "380px"}
            ),
        ]),

    ]),

    dcc.Interval(id="interval", interval=10000, n_intervals=0),
])

# ── Helper: sparkline ──────────────────────────────────────────────────────────
def build_sparkline(ticker: str, change: float):
    try:
        hist = yf.Ticker(ticker).history(period="7d")
        if hist.empty:
            return go.Figure()

        color = COLORS["green"] if change >= 0 else COLORS["red"]
        fill  = "rgba(34,197,94,0.1)" if change >= 0 else "rgba(239,68,68,0.1)"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"],
            mode="lines",
            line=dict(color=color, width=1.5),
            fill="tozeroy",
            fillcolor=fill,
            hoverinfo="skip"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            showlegend=False,
        )
        return fig
    except Exception:
        return go.Figure()


# ── Callbacks ──────────────────────────────────────────────────────────────────

# Cards de precios
@app.callback(
    Output("price-wti",   "children"), Output("change-wti",   "children"),
    Output("price-brent", "children"), Output("change-brent", "children"),
    Output("price-ng",    "children"), Output("change-ng",    "children"),
    Output("price-slb",   "children"), Output("change-slb",   "children"),
    Output("price-xom",   "children"), Output("change-xom",   "children"),
    Output("last-update", "children"),
    Input("interval", "n_intervals")
)
def update_cards(n):
    from datetime import datetime

    results = []
    for ticker in ["CL=F", "BZ=F", "NG=F", "SLB", "XOM"]:
        price, change = get_price(ticker)
        if price is None:
            results += ["—", html.Span("N/A", style={"color": COLORS["muted"]})]
            continue

        color  = COLORS["green"] if change >= 0 else COLORS["red"]
        symbol = "▲" if change >= 0 else "▼"

        results += [
            f"${price:,.2f}",
            html.Span(f"{symbol} {abs(change):.2f}%", style={
                "color":      color,
                "fontFamily": FONT_MONO,
                "fontSize":   "12px",
            })
        ]

    now = datetime.now().strftime("Updated %H:%M:%S")
    return (*results, now)

# Sparklines
@app.callback(
    Output("spark-wti",   "figure"),
    Output("spark-brent", "figure"),
    Output("spark-ng",    "figure"),
    Output("spark-slb",   "figure"),
    Output("spark-xom",   "figure"),
    Input("interval", "n_intervals")
)
def update_sparklines(n):
    tickers = ["CL=F", "BZ=F", "NG=F", "SLB", "XOM"]
    figures = []
    for ticker in tickers:
        _, change = get_price(ticker)
        figures.append(build_sparkline(ticker, change or 0))
    return figures

# Gráfico histórico
@app.callback(
    Output("main-chart",  "figure"),
    Output("chart-title", "children"),
    Input("ticker-select", "value"),
    Input("period-select", "value"),
)
def update_chart(ticker, period):
    title = TICKER_MAP.get(ticker, ticker)
    return build_chart(ticker, period), title


if __name__ == "__main__":
    app.run(debug=True)